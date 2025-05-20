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
        fc = fr = None
        if host.system_info.distribution.lower() in debian_os:
            fc = host.file('/etc/powerdns/recursor.conf')
            fr = host.file('/etc/powerdns/rpz.lua')
        if host.system_info.distribution.lower() in rhel_os:
            fc = host.file('/etc/pdns-recursor/recursor.conf')
            fr = host.file('/etc/pdns-recursor/rpz.lua')

        assert fc.exists
        assert fc.user == 'root'
        assert fc.group == AnsibleVars['default_pdns_rec_group']
        assert fc.mode == 0o640
        assert fc.contains('lua-config-file=' + fr.path)
        assert fc.contains(
                'allow-from=127.0.0.0/24,127.0.1.0/24,2001:DB8:10::/64')
        assert fc.contains("forward-zones=foo.example=192.0.2.1;192.0.2.2" +
                           ",bar.example=192.0.2.224:5300")
        assert fc.contains("forward-zones-recurse=quux.example=192.0.2.15")

        assert fr.exists
        assert fr.user == 'root'
        assert fr.group == AnsibleVars['default_pdns_rec_group']
        assert fr.mode == 0o640

def test_dns_resolution(host):
    import socket
    import subprocess

    # testing URL - powerdns.com :)
    test_url = "powerdns.com"
    
    with host.sudo():
        cmd = host.run("""python3 -c "
import socket
import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = ['127.0.0.1']

# Test IPv4
try:
    answers_a = resolver.resolve('powerdns.com', 'A')
    if len(answers_a) > 0:
        print(f'A record: {answers_a[0].address}')
except Exception as e:
    print(f'Error querying IPv4 record: {e}')
    exit(1)

# Test IPv6
try:
    answers_aaaa = resolver.resolve('powerdns.com', 'AAAA')
    if len(answers_aaaa) > 0:
        print(f'AAAA record: {answers_aaaa[0].address}')
    else:
    print(f'Error querying IPv6 record: {e}')
    exit (1)
""")

