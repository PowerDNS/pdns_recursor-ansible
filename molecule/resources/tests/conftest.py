import os

import pytest
import yaml

debian_os = ['debian', 'ubuntu']
rhel_os = ['redhat', 'centos', 'ol', 'rocky', 'almalinux']
# 'archarm' is what the Arch Linux ARM images report.
arch_os = ['arch', 'archarm', 'archlinux', 'arch linux']


@pytest.fixture()
def distro_family(host):
    """Return 'debian', 'rhel' or 'arch' for the host under test."""
    distribution = host.system_info.distribution.lower()
    if distribution in debian_os:
        return 'debian'
    if distribution in rhel_os:
        return 'rhel'
    if distribution in arch_os:
        return 'arch'
    raise AssertionError('unsupported distribution {}'.format(distribution))


@pytest.fixture()
def component_version():
    """The release under test, as named by the PowerDNS repositories."""
    # A set-but-empty variable must fall back, which os.environ.get does not do.
    return os.environ.get('PDNS_REC_VERSION') or '54'


@pytest.fixture()
def component_version_string(component_version):
    """The release under test as the recursor reports it, for example '5.4'."""
    if not component_version.isdigit() or len(component_version) != 2:
        # Release names such as 'master' have no dotted form.
        return component_version
    return '{}.{}'.format(component_version[0], component_version[1])


@pytest.fixture()
def repo_file(host, distro_family):
    """The repository file the role writes. Its name carries no version."""
    if distro_family == 'debian':
        return host.file('/etc/apt/sources.list.d/powerdns-recursor.sources')
    return host.file('/etc/yum.repos.d/powerdns-recursor.repo')


@pytest.fixture()
def config_dir(distro_family):
    if distro_family == 'rhel':
        return '/etc/pdns-recursor'
    return '/etc/powerdns'


@pytest.fixture()
def config_file(host, config_dir):
    """The configuration file of the default instance."""
    name = os.getenv('REC_CONFIG_FILE', 'recursor.conf')
    return host.file('{}/{}'.format(config_dir, name))


@pytest.fixture()
def ansible_vars(host, distro_family):
    """The role defaults for the host, as the role itself would load them."""
    vars_files = ['../../vars/main.yml']
    if distro_family == 'debian':
        vars_files.append('../../vars/Debian.yml')
    elif distro_family == 'rhel':
        vars_files.append('../../vars/RedHat.yml')
    elif distro_family == 'arch':
        vars_files.append('../../vars/Archlinux.yml')

    values = {}
    for path in vars_files:
        with open(path, 'r') as stream:
            values.update(yaml.safe_load(stream))

    return values
