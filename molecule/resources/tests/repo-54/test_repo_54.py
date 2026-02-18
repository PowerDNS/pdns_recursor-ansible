
debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']


def _deb_repo_path(host):
    distro = (host.system_info.distribution or "").lower()
    if distro == 'ubuntu':
        rel = host.system_info.release or ""

        def _parse(v):
            try:
                parts = v.split('.')
                major = int(parts[0])
                minor = int(parts[1]) if len(parts) > 1 else 0
                return (major, minor)
            except Exception:
                return (0, 0)
        if _parse(rel) < (22, 4):
            return '/etc/apt/sources.list.d/powerdns-rec-54.list'
    # Debian and Ubuntu >= 22.04 use deb822
    return '/etc/apt/sources.list.d/powerdns-rec-54.sources'


def test_repo_file(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file(_deb_repo_path(host))
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-rec-54.repo')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_pdns_repo(host):
    f = None
    if host.system_info.distribution.lower() in debian_os:
        f = host.file(_deb_repo_path(host))
    if host.system_info.distribution.lower() in rhel_os:
        f = host.file('/etc/yum.repos.d/powerdns-rec-54.repo')

    assert f.exists
    assert f.contains('rec-54')


def test_pdns_version(host):
    cmd = host.run('/usr/sbin/pdns_recursor --version')

    assert 'PowerDNS Recursor' in cmd.stderr or 'PowerDNS Recursor' in cmd.stdout
    assert '5.4' in cmd.stderr or '5.4' in cmd.stdout


def systemd_override(host):
    fname = '/etc/systemd/system/pdns-recursor.service.d/override.conf'
    f = host.file(fname)

    assert not f.contains('User=')
    assert not f.contains('Group=')
