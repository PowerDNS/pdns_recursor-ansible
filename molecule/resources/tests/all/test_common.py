import re


def test_distribution(distro_family):
    assert distro_family in ('debian', 'rhel', 'arch')


def test_repo_pinning_file(host, distro_family):
    if distro_family == 'debian':
        f = host.file('/etc/apt/preferences.d/pdns-recursor')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        assert f.contains('Package: pdns-recursor')
        assert f.contains('Pin: origin repo.powerdns.com')
        assert f.contains('Pin-Priority: 600')


def test_package(host, distro_family):
    if distro_family == 'arch':
        # testinfra does not map every Arch flavour to ArchPackage, so query
        # pacman directly.
        assert host.run('pacman -Q powerdns-recursor').rc == 0
        return

    assert host.package('pdns-recursor').is_installed


def test_distribution_package_is_the_running_one(host, distro_family):
    """On the distribution packages there is no repository to attribute, so
    check that the installed package is what answers."""
    if distro_family != 'arch':
        return

    package_version = host.check_output("pacman -Q powerdns-recursor | awk '{print $2}'")
    cmd = host.run('/usr/bin/pdns_recursor --version')
    output = '{}\n{}'.format(cmd.stdout, cmd.stderr)

    # pacman reports 5.4.5-1 where the recursor reports 5.4.5
    assert package_version.split('-')[0] in output


def test_service(host):
    # Using Ansible to mitigate some issues with the service test on debian-8
    s = host.ansible('service', 'name=pdns-recursor state=started enabled=yes')
    assert s["changed"] is False


def test_config(host, config_file, ansible_vars):
    with host.sudo():
        assert config_file.exists
        assert config_file.user == 'root'
        assert config_file.group == ansible_vars['default_pdns_rec_group']
        assert config_file.mode == 0o640


def test_config_vaulted_api_key(host, config_file):
    """Verify that the vaulted api_key is decrypted and written as plaintext in the config."""
    with host.sudo():
        assert config_file.exists
        # The vaulted value must be decrypted to the plaintext "powerdns".
        # to_nice_yaml may quote the value, so match with or without quotes.
        assert config_file.contains('api_key:.*powerdns'), \
            "Vaulted api_key was not decrypted properly in the rendered config"
        # Ensure no vault marker leaked into the config file
        assert not config_file.contains('ANSIBLE_VAULT'), \
            "Vault-encrypted blob found in rendered config - decryption failed"


def test_dns_resolution(host):
    with host.sudo():
        cmd = host.run("""python3 -c "
import sys
import socket
try:
    import dns.resolver
except ImportError:
    print('dnspython not installed', file=sys.stderr)
    sys.exit(1)

def _resolve(resolver, name, rtype):
    try:
        return resolver.resolve(name, rtype)  # dnspython >=2
    except AttributeError:
        return resolver.query(name, rtype)    # dnspython 1.x

resolver = dns.resolver.Resolver()
resolver.nameservers = ['127.0.0.1']

# Test IPv4
try:
    answers_a = _resolve(resolver, 'example.com', 'A')
    if len(answers_a) > 0:
        print(f'A record: {answers_a[0].address}')
except Exception as e:
    print(f'Error querying IPv4 record: {e}')
    sys.exit(1)

# Test IPv6
try:
    answers_aaaa = _resolve(resolver, 'example.com', 'AAAA')
    if len(answers_aaaa) > 0:
        print(f'AAAA record: {answers_aaaa[0].address}')
except Exception as e:
    print(f'Error querying IPv6 record: {e}')
    sys.exit(1)
" """)
        assert cmd.rc == 0, f"DNS resolution script failed rc={cmd.rc}\nstdout:\n{cmd.stdout}\nstderr:\n{cmd.stderr}"


def test_dns_resolution_rpz(host):
    with host.sudo():
        cmd = host.run("""python3 -c "
import sys
import socket
try:
    import dns.resolver
except ImportError:
    print('dnspython not installed', file=sys.stderr)
    sys.exit(1)

def _resolve(resolver, name, rtype):
    try:
        return resolver.resolve(name, rtype)  # dnspython >=2
    except AttributeError:
        return resolver.query(name, rtype)    # dnspython 1.x

resolver = dns.resolver.Resolver()
resolver.nameservers = ['127.0.0.1']

# Test test-rpz.com expects 127.0.0.2
try:
    answers_test2 = _resolve(resolver, 'test-rpz.com', 'A')
    addrs = [r.address for r in answers_test2]
    if '127.0.0.2' not in addrs:
        print(f'Unexpected A record(s) for test-rpz.com: {addrs}')
        sys.exit(1)
    else:
        print('test-rpz.com A record OK')
except Exception as e:
    print(f'Error querying test-rpz.com A record: {e}')
    sys.exit(1)
" """)
        assert cmd.rc == 0, f"RPZ script failed rc={cmd.rc}\nstdout:\n{cmd.stdout}\nstderr:\n{cmd.stderr}"


def test_daemon_runs_as_the_service_account(host, ansible_vars):
    """The daemon must not be running as root.

    What this guards is the outcome, not one mechanism. Two things enforce it and
    either is enough: the packaged unit's User=/Group=, and `recursor.setuid` /
    `recursor.setgid` in the configuration the role writes. So on a systemd host
    this does not prove the settings took effect - it proves that between them
    nothing left the daemon privileged, which is what an operator cares about, and
    it catches an override or a unit change that hands it back to root.

    Asserted on the running process because a configuration file carrying the
    settings says nothing about whether they applied. The uid comes from the
    ownership of /proc/<pid> rather than from ps: these images do not all ship
    procps.
    """
    if not host.exists('systemctl'):
        return

    state = host.run('systemctl is-active pdns-recursor')
    assert state.stdout.strip() == 'active', \
        'the recursor is {}, so there is no process to check'.format(state.stdout.strip())

    pid = host.run('systemctl show pdns-recursor -p MainPID --value').stdout.strip()
    assert pid.isdigit() and pid != '0', 'no MainPID for a unit reported active'

    proc = host.file('/proc/{}'.format(pid))
    assert proc.exists, 'the process exited between reading its pid and its owner'
    assert proc.user == ansible_vars['default_pdns_rec_user']
    assert proc.user != 'root'


def test_webservice_api_dir(host, config_file, ansible_vars):
    """The directory named by webservice.api_dir has to exist and be writable.

    The recursor reads api_dir whether or not the webserver is enabled and refuses
    to start when it names a directory that is not there, so the role creates it -
    owned by the account the daemon runs as, because the REST API writes into it.
    The scenario deliberately does not list it in pdns_rec_config_additional_dirs,
    so what is checked here is the role creating it on its own.
    """
    match = re.search(r'^\s+api_dir:\s*(\S+)\s*$', config_file.content_string,
                      re.MULTILINE)
    if not match:
        return

    api_dir = host.file(match.group(1).strip('"\''))
    assert api_dir.exists, '{} was not created'.format(match.group(1))
    assert api_dir.is_directory
    assert api_dir.user == ansible_vars['default_pdns_rec_user']


def test_webservice_api_dir_contents_are_left_to_the_daemon(host, config_file):
    """Whatever the recursor writes into api_dir keeps the mode it chose.

    The role does not walk api_dir: the daemon writes `apizones` as 0644, so
    applying the recursive directory mode to it would reset it, notify a restart,
    and the restart would write it back - a change on every converge, for ever.
    """
    match = re.search(r'^\s+api_dir:\s*(\S+)\s*$', config_file.content_string,
                      re.MULTILINE)
    if not match:
        return

    apizones = host.file('{}/apizones'.format(match.group(1).strip('"\'')))
    if not apizones.exists:
        return

    assert apizones.mode == 0o644
