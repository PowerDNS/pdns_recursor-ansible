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
