import os
import yaml
import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos']


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
            ansibleVars.update(yaml.load(stream))

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
        assert oct(fc.mode) == '0640'
        assert 'lua-config-file=' + fr.path in fc.content
        assert 'allow-from=127.0.0.0/24,127.0.1.0/24,2001:DB8:10::/64' in \
            fc.content

        assert fr.exists
        assert fr.user == 'root'
        assert fr.group == AnsibleVars['default_pdns_rec_group']
        assert oct(fr.mode) == '0640'


def systemd_override(host):
    smgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]
    if smgr == 'systemd':
        fname = '/etc/systemd/system/pdns-recursor.service.d/override.conf'
        f = host.file(fname)

        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        assert 'LimitCORE=infinity' in f.content
