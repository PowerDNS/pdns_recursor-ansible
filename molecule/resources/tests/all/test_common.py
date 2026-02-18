import os
import yaml
import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']


@pytest.fixture()
def AnsibleVars(host):
    varsFiles = ["../../vars/main.yml"]
    if host.system_info.distribution.lower() in debian_os:
        varsFiles.append("../../vars/Debian.yml")
    if host.system_info.distribution.lower() in rhel_os:
        varsFiles.append("../../vars/RedHat.yml")

    ansibleVars = {}
    for f in varsFiles:
        with open(f, 'r') as stream:
            ansibleVars.update(yaml.load(stream, Loader=yaml.FullLoader))

    return ansibleVars


def test_distribution(host):
    assert host.system_info.distribution.lower() in debian_os + rhel_os


def test_repo_pinning_file(host):
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/preferences.d/pdns-recursor')
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        f.contains('Package: pdns-recursor')
        f.contains('Pin: origin repo.powerdns.com')
        f.contains('Pin-Priority: 600')


def test_package(host):
    p = host.package('pdns-recursor')
    assert p.is_installed


def test_service(host):
    # Using Ansible to mitigate some issues with the service test on debian-8
    s = host.ansible('service', 'name=pdns-recursor state=started enabled=yes')
    assert s["changed"] is False

def test_config(host, AnsibleVars):
    with host.sudo():
        rec_config_file = os.getenv('REC_CONFIG_FILE', 'recursor.conf')
        fc = None
        if host.system_info.distribution.lower() in debian_os:
            fc = host.file(f'/etc/powerdns/{ rec_config_file }')
        if host.system_info.distribution.lower() in rhel_os:
            fc = host.file(f'/etc/pdns-recursor/{ rec_config_file }')

        assert fc.exists
        assert fc.user == 'root'
        assert fc.group == AnsibleVars['default_pdns_rec_group']
        assert fc.mode == 0o640


def test_config_vaulted_api_key(host):
    """Verify that the vaulted api_key is decrypted and written as plaintext in the config."""
    with host.sudo():
        rec_config_file = os.getenv('REC_CONFIG_FILE', 'recursor.conf')
        fc = None
        if host.system_info.distribution.lower() in debian_os:
            fc = host.file(f'/etc/powerdns/{ rec_config_file }')
        if host.system_info.distribution.lower() in rhel_os:
            fc = host.file(f'/etc/pdns-recursor/{ rec_config_file }')

        assert fc.exists
        # The vaulted value must be decrypted to the plaintext "powerdns".
        # to_nice_yaml may quote the value, so match with or without quotes.
        assert fc.contains('api_key:.*powerdns'), \
            "Vaulted api_key was not decrypted properly in the rendered config"
        # Ensure no vault marker leaked into the config file
        assert not fc.contains('ANSIBLE_VAULT'), \
            "Vault-encrypted blob found in rendered config — decryption failed"

def test_dns_resolution(host):
    import socket
    import subprocess

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
    import socket
    import subprocess

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
