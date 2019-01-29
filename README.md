# Ansible Role: PowerDNS Recursor

[![Build Status](https://travis-ci.org/PowerDNS/pdns_recursor-ansible.svg?branch=master)](https://travis-ci.org/PowerDNS/pdns_recursor-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.pdns_recursor-blue.svg)](https://galaxy.ansible.com/PowerDNS/pdns_recursor)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/pdns_recursor-ansible.svg)](https://github.com/PowerDNS/pdns_recursor-ansible/tags)

An Ansible role created by the folks behind PowerDNS to setup the [PowerDNS Recursor](https://docs.powerdns.com/recursor/).

## Requirements

An Ansible 2.2 or higher installation.

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
- hosts: pdns-recursors
  roles:
  - { role: PowerDNS.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_master }}" }

# Install the PowerDNS Recursor from the '4.0.x' official repository
- hosts: pdns-recursors
  roles:
  - { role: PowerDNS.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_40 }}" }

# Install the PowerDNS Recursor from the '4.1.x' official repository
- hosts: pdns-recursors
  roles:
  - { role: PowerDNS.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_41 }}" }
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
  - { role: PowerDNS.pdns_recursor }
```

It is also possible to install the PowerDNS Recursor from custom repositories as demonstrated in the example above.

```yaml
pdns_rec_install_epel: True
```

By default, install EPEL to satisfy some PowerDNS Recursor dependencies like `protobuf`.
To skip the installtion of EPEL set `pdns_rec_install_epel` to `False`.

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
pdns_rec_service_name: "pdns_recursor-recursor"
```

The name of the PowerDNS Recursor service.

```yaml
pdns_rec_flush_handlers: False
```

Force the execution of the flushing of the handlers at the end of the role. <br />
**NOTE:** This is required if using this role to configure multiple recursor instances in a single play

```yaml
pdns_rec_service_state: "started"
pdns_rec_service_enabled: "yes"
```

Allow to specify the desired state of the PowerDNS Recursor service.
E.g. This allows to install and configure the PowerDNS Recursor without automatically starting the service.

```yaml
pdns_rec_disable_handlers: False
```

Disable automated service restart on configuration changes.

```yaml
pdns_rec_config_dir: "/etc/powerdns"
pdns_rec_config_file: "recursor.conf"
```

The PowerDNS Recursor configuration files and directories.

```yaml
pdns_rec_config: { }
```

Dictionary containing in YAML format the custom configuration of PowerDNS Recursor.
**NOTE**: You should not set the `config-dir`, `set-uid` and `set-gid` because are set by other role variables (respectively `pdns_rec_config_dir`, `pdns_rec_user`, `pdns_rec_group`).

```yaml
pdns_res_config_lua: "{{ pdns_rec_config_dir }}/config.lua"
pdns_rec_config_lua_file_content: ""
```

If `pdns_rec_config_lua_file_content` is not `""`, this will dump
the content of this variable to the `pdns_res_config_lua` file and
define accordingly the `lua-config-file` setting in the `recursor.conf` configuration file.

```yaml
pdns_rec_config_dns_script: "{{ pdns_rec_config_dir }}/dns-script.lua"
pdns_rec_config_dns_script_file_content: ""
```

If `pdns_rec_config_dns_script_file_content` is not `""`, this will dump
the content of this variable to the `pdns_rec_config_dns_script` file and
define accordingly the `lua-dns-script` setting in the `recursor.conf` configuration file.

```yaml
pdns_rec_service_overrides: {}
```

Dict with overrides for the service (systemd only).
This can be used to change any systemd settings in the `[Service]` category

## Example Playbooks

Bind to `203.0.113.53` on port `5300` and allow only traffic from the `198.51.100.0/24` subnet:

```yaml
- hosts: pdns-recursors
  vars:
    pdns_rec_config:
      allow-from: "198.51.100.0/24"
      local-address: "203.0.113.53:5300"
  roles:
    - { role: PowerDNS.pdns_recursor }
```

Allow traffic from multiple networks and set some custom ulimits overriding the default systemd service:

```yaml
- hosts: pdns-recursors
  vars:
    pdns_rec_config:
      allow-from:
        - "198.51.100.0/24"
        - "203.0.113.53/24"
      local-address: "203.0.113.53:5300"
      pdns_rec_service_overrides:
        LimitNOFILE: 10000
  roles:
    - { role: PowerDNS.pdns_recursor }
```

## Changelog

A detailed changelog of all the changes applied to the role is available [here](./CHANGELOG.md).

## Testing

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

    $ pip install tox

To test all the scenarios run

    $ tox

To run a custom molecule command

    $ tox -e py27-ansible22 -- molecule test -s pdns-rec-41

## License

MIT
