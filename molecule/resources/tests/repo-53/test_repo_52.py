
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']


def test_repo_file(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-recursor.sources')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-rec-53.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pdns_repo(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file('/etc/apt/sources.list.d/powerdns-recursor.sources')
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-rec-53.repo')

    assert f.exists
    assert f.contains('rec-53')


def test_pdns_version(host):
    cmd = host.run('/usr/sbin/pdns_recursor --version')

    assert 'PowerDNS Recursor' in cmd.stderr or 'PowerDNS Recursor' in cmd.stdout
    assert '5.3' in cmd.stderr or '5.3' in cmd.stdout


def systemd_override(host):
    fname = '/etc/systemd/system/pdns-recursor.service.d/override.conf'
    f = host.file(fname)

    assert not f.contains('User=')
    assert not f.contains('Group=')
