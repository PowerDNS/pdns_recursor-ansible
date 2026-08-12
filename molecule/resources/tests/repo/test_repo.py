def test_repo_file(host, distro_family, repo_file):
    if distro_family == 'debian':
        # The role writes deb822 and removes the one-line format.
        assert not host.file('/etc/apt/sources.list.d/powerdns-recursor.list').exists

    assert repo_file.exists
    assert repo_file.user == 'root'
    assert repo_file.group == 'root'


def test_repo_release(repo_file, component_version):
    assert repo_file.contains('rec-{}'.format(component_version))


def test_repo_architecture(host, distro_family, repo_file):
    if distro_family == 'debian':
        apt_arch = host.check_output('dpkg --print-architecture').strip()

        assert repo_file.contains('Architectures: {}'.format(apt_arch))


def test_component_version(host, component_version_string):
    cmd = host.run('/usr/sbin/pdns_recursor --version')
    output = '{}\n{}'.format(cmd.stdout, cmd.stderr)

    assert 'PowerDNS Recursor' in output
    assert component_version_string in output
