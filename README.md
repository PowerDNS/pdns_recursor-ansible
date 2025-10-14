# Ansible Role: PowerDNS Recursor

[![Build Status](https://github.com/PowerDNS/pdns_recursor-ansible/actions/workflows/main.yml/badge.svg)](https://github.com/PowerDNS/pdns_recursor-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.pdns_recursor-blue.svg)](https://galaxy.ansible.com/PowerDNS/pdns_recursor)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/pdns_recursor-ansible.svg)](https://github.com/PowerDNS/pdns_recursor-ansible/tags)

An Ansible role created by the folks behind PowerDNS to setup the [PowerDNS Recursor](https://docs.powerdns.com/recursor/).

## Requirements

An Ansible 2.15 or higher installation. PowerDNS Recursor 5.1 or higher installation.

## Dependencies

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
pdns_rec_install_repo: ""
```

By default, the PowerDNS Recursor is installed from the software repositories configured on the target hosts.

```yaml
# Install the PowerDNS Recursor from the 'master' official repository
- hosts: pdns_recursors
  roles:
  - { role: powerdns.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_master }}" }

# Install the PowerDNS Recursor from the '5.0.x' official repository
- hosts: pdns_recursors
  roles:
  - { role: powerdns.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_50 }}" }

# Install the PowerDNS Recursor from the '5.1.x' official repository
- hosts: pdns_recursors
  roles:
  - { role: powerdns.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_51 }}" }

# Install the PowerDNS Recursor from the '5.2.x' official repository
- hosts: pdns_recursors
  roles:
  - { role: powerdns.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_52 }}" }
```

The examples above, show how to install the PowerDNS Recursor from the official PowerDNS repositories
(see the complete list of pre-defined repos in `vars/main.yml`).

The roles also supports custom repositories

```yaml
- hosts: all
  vars:
    pdns_rec_install_repo:
      name: "powerdns-rec"  # the name of the repository
      apt_repo_origin: "repo.example.com"   # used to pin the PowerDNS packages to the provided repository
      apt_repo: "deb http://repo.example.com/{{ ansible_distribution | lower }} {{ ansible_distribution_release | lower }}/pdns-recursor main"
      gpg_key: "http://repo.example.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
      gpg_key_id: "MYREPOGPGPUBKEYID" # to avoid to reimport the key each time the role is executed
      yum_repo_baseurl: "http://repo.example.com/centos/$basearch/$releasever/pdns-recursor"
      yum_repo_debug_symbols_baseurl: "http://repo.example.com/centos/$basearch/$releasever/pdns-recursor/debug"
  roles:
  - { role: powerdns.pdns_recursor }
```

It is also possible to install the PowerDNS Recursor from custom repositories as demonstrated in the example above.

```yaml
pdns_rec_install_epel: True
```

By default, install EPEL to satisfy some PowerDNS Recursor dependencies like `protobuf`.
To skip the installation of EPEL set `pdns_rec_install_epel` to `False`.

```yaml
pdns_rec_package_name: "{{ default_pdns_rec_package_name }}"
```

The name of the PowerDNS Recursor package, `pdns-recursor` on RedHat-like Debian-like systems.

```yaml
pdns_rec_package_version: ""
```

Optionally, allow to set a specific version of the PowerDNS Recursor package to be installed.

```yaml
pdns_rec_install_debug_symbols_package: False
```

Install the PowerDNS Recursor debug symbols.

```yaml
pdns_rec_debug_symbols_package_name: "{{ default_pdns_rec_debug_symbols_package_name }}"
```

The name of the PowerDNS Recursor debug package to be installed when `pdns_install_debug_symbols_package` is `True`,
`pdns-recursor-debuginfo` on RedHat-like systems and `pdns-recursor-dbg` on Debian-like systems.

```yaml
pdns_rec_user: "{{ default_pdns_rec_user }}"
pdns_rec_group: "{{ default_pdns_rec_group }}"
```

The user and group the PowerDNS Recursor will run as, `pdns-recursor` on RedHat-like systems and `pdns` on Debian-like systems <br />
**NOTE**: This role does not create any user or group as we assume that they're created
by the package or other roles.

```yaml
pdns_rec_file_owner: "root"
pdns_rec_file_group: "{{ default_pdns_file_group }}"
```

User and group owning the configuration files and directories.

```yaml
pdns_rec_service_name: "pdns-recursor"
```

The name of the PowerDNS Recursor service.

```yaml
pdns_rec_service_state: "started"
pdns_rec_service_enabled: true
pdns_rec_service_masked: false
```

Allow to specify the desired state of the PowerDNS Recursor service.
E.g. This allows to install and configure the PowerDNS Recursor without automatically starting the service.

```yaml
pdns_rec_disable_handlers: False
```

Disable automated service restart on configuration changes.

```yaml
pdns_rec_config_dir: "{{ default_pdns_rec_config_dir }}"
pdns_rec_config_file: "recursor.conf"
```

The PowerDNS Recursor configuration files and directories, where `default_pdns_rec_config_dir` is `/etc/powerdns` on Debian and `/etc/pdns-recursor` on RedHat.

```yaml
pdns_rec_config: {}
```

Dictionary containing in YAML format configuration of PowerDNS Recursor. See https://docs.powerdns.com/recursor/yamlsettings.html.

```yaml
pdns_rec_config_additional_dirs: []
# pdns_rec_config_additional_dirs:
#   - path: "{{ pdns_rec_config.webservice.api_dir }}"
#     mode: '0775'
#   - "{{ pdns_rec_config.recursor.include_dir }}"
#   - "/var/lib/pdns-recursor/rpz"
```

Additional directories for configuration or supplementary files.

```yaml
pdns_rec_config_additional_files: []
# pdns_rec_config_additional_files:
#   - dest: "/var/lib/pdns-recursor/rpz/test.rpz"
#     content: |
#       test.rpz.               60   IN SOA    ns.test.rpz. hostmaster.test.rpz. 1 10800 60 3600 3600
#       test-rpz.com.test.rpz.  60   IN A  127.0.0.2
```

Additional configuration or supplementary files for PowerDNS Recursor, e.g RPZ files.

## Example Playbooks

Bind to `203.0.113.53` on port `5300` and allow only traffic from the `198.51.100.0/24` subnet:

```yaml
- hosts: pdns_recursors
  vars:
    pdns_rec_config:
      incoming:
        listen:
          - 203.0.113.53:5300
        allow_from: [ 198.51.100.0/24 ]
  roles:
    - { role: powerdns.pdns_recursor }
```

Allow traffic from multiple networks and set some custom ulimits overriding the default systemd service:

```yaml
- hosts: pdns_recursors
  vars:
    pdns_rec_config:
      incoming:
        listen:
          - 203.0.113.53:5300
        allow_from: [ 198.51.100.0/24, 198.51.100.0/24 ]
    pdns_rec_service_overrides:
      LimitNOFILE: 10000
  roles:
    - { role: powerdns.pdns_recursor }
```

Forward queries for corp.example.net to a nameserver on localhost and queries for foo.example to other nameservers:

```yaml
- hosts: pdns_recursors
  vars:
    pdns_rec_config:
      recursor:
        forward_zones:
          - zone: corp.example.net
            forwarders:
              - 127.0.0.1:5300
          - zone: foo.example
            forwarders:
              - "192.0.2.3"
              - "[2001:db8::2:3]"
  roles:
    - { role: powerdns.pdns_recursor }
```

## Changelog

A detailed changelog of all the changes applied to the role is available [here](./CHANGELOG.md).

## Testing

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

    $ pip install tox

To test all the scenarios run

    $ tox

To run a custom molecule command

    $ tox -e ansible216 -- molecule test -s pdns-rec-52

## License

MIT
