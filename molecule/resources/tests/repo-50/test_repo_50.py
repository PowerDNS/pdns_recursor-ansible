
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol']


def test_repo_file(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-rec-50.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-rec-50.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pdns_repo(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-rec-50.list')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-rec-50.repo')

    assert f.exists
    assert f.contains('rec-50')


def test_pdns_version(host):
    cmd = host.run('/usr/sbin/pdns_recursor --version')

    assert 'PowerDNS Recursor' in cmd.stderr
    assert '5.0' in cmd.stderr


def systemd_override(host):
    fname = '/etc/systemd/system/pdns-recursor.service.d/override.conf'
    f = host.file(fname)

    assert not f.contains('User=')
    assert not f.contains('Group=')
