# Ansible Role: PowerDNS Recursor

[![Build Status](https://github.com/PowerDNS/pdns_recursor-ansible/actions/workflows/main.yml/badge.svg)](https://github.com/PowerDNS/pdns_recursor-ansible)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-PowerDNS.pdns_recursor-blue.svg)](https://galaxy.ansible.com/PowerDNS/pdns_recursor)
[![GitHub tag](https://img.shields.io/github/tag/PowerDNS/pdns_recursor-ansible.svg)](https://github.com/PowerDNS/pdns_recursor-ansible/tags)

An Ansible role created by the folks behind PowerDNS to setup the [PowerDNS Recursor](https://docs.powerdns.com/recursor/).

## Requirements

An Ansible 2.15 or higher installation.

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

# Install the PowerDNS Recursor from the '5.3.x' official repository
- hosts: pdns_recursors
  roles:
  - { role: powerdns.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_53 }}" }

# Install the PowerDNS Recursor from the '5.4.x' official repository
- hosts: pdns_recursors
  roles:
  - { role: powerdns.pdns_recursor,
      pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_54 }}" }
```

The examples above, show how to install the PowerDNS Recursor from the official PowerDNS repositories
(see the complete list of pre-defined repos in `vars/main.yml`).

The roles also supports custom repositories

```yaml
- hosts: all
  vars:
    pdns_rec_install_repo:
      name: "powerdns-rec"  # the name of the repository
      apt_version: rec-master # deb822 suites suffix (appended to release codename)
      apt_repo_origin: "repo.example.com"   # used to pin the PowerDNS packages to the provided repository
      gpg_key: "http://repo.example.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
      yum_repo_baseurl: "http://repo.example.com/el/$basearch/$releasever/pdns-recursor"
      yum_repo_debug_symbols_baseurl: "http://repo.example.com/el/$basearch/$releasever/pdns-recursor/debug"
  roles:
  - { role: powerdns.pdns_recursor }
```

It is also possible to install the PowerDNS Recursor from custom repositories as demonstrated in the example above.

```yaml
pdns_rec_install_epel: true
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
pdns_rec_package_state: "present"
```

The desired state of the PowerDNS Recursor packages. Use `"present"` (default) to install, `"latest"` to upgrade, or `"absent"` to uninstall.

```yaml
pdns_rec_install_debug_symbols_package: false
```

Install the PowerDNS Recursor debug symbols.

```yaml
pdns_rec_debug_symbols_package_name: "{{ default_pdns_rec_debug_symbols_package_name }}"
```

The name of the PowerDNS Recursor debug package to be installed when `pdns_install_debug_symbols_package` is `true`,
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
pdns_rec_bin_name: "pdns_recursor"
```

The name of the PowerDNS Recursor binary.

```yaml
pdns_rec_service_state: "started"
pdns_rec_service_enabled: true
pdns_rec_service_masked: false
```

Allow to specify the desired state of the PowerDNS Recursor service.
E.g. This allows to install and configure the PowerDNS Recursor without automatically starting the service.

```yaml
pdns_rec_disable_handlers: false
```

Disable automated service restart on configuration changes.

```yaml
pdns_rec_flush_handlers: false
```

Run the notified handlers at the end of the role instead of at the end of the play. See
[Handlers](#handlers).

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

```yaml
pdns_rec_service_overrides: {}
```

Dict with overrides for the service (systemd only).
This can be used to change any systemd settings in the `[Service]` category.

## Role Tags

Tags for `--tags` / `--skip-tags`:

- `repository`: repo and GPG key setup, APT pinning, removal of stale versioned repo files.
- `install`: package installation and removal.
- `config`: config file and directories, additional files, systemd overrides, validation.
- `service`: service state.
- `always`: OS variable import.

The repository tasks and the fact deriving the repository name are tagged both `install` and
`repository`, so `--tags install` also sets up the repository it needs.

Contributors: tags belong on the tasks inside `install-{{ ansible_system }}.yml`, `configure.yml`
and `repo-*.yml`, not only on the `include_tasks` in `tasks/main.yml`. A dynamic `include_tasks`
does not pass its tags to included tasks, so a narrow `--tags` run would execute the include and
skip its body, silently, with `rc=0`.

## Check Mode

Supported only on a host where this role already ran successfully.

Converged host: `--check` reports real drift only. Config validation is skipped
(`when: not ansible_check_mode`) since it needs the rendered file on disk.

Fresh host: `--check` is expected to fail. It installs neither the repository, `python3-debian`
nor the `pdns-recursor` package, so later tasks have nothing to inspect.

## Package and Service State

- `pdns_rec_package_state`: `present`, `latest`, `absent`, ...
- `pdns_rec_service_state` (`started`, `stopped`, `restarted`, `reloaded`),
  `pdns_rec_service_enabled`, `pdns_rec_service_masked`.

`pdns_rec_package_state: absent` removes the packages, but the config and service tasks still run,
so a full run fails validating the config because `/usr/sbin/pdns_recursor` is gone. Remove via
the install path only:

```bash
ansible-playbook site.yml -e pdns_rec_package_state=absent --tags install
```

## Handlers

Handlers run at the end of the play, and Ansible shares them between invocations of the same role.
A role parameter read inside a handler resolves to the value of the *last* invocation, so with more
than one invocation in a play the restart targets the wrong service or is collapsed into a single
run. Set `pdns_rec_flush_handlers: true` to run `meta: flush_handlers` as the last task of the role,
which restarts `pdns_rec_service_name` of that invocation:

Every instance needs its own service name and configuration file; `pdns-recursor@<instance>` runs
`pdns_recursor --config-name=<instance>`, which reads `<config dir>/recursor-<instance>.conf`:

```yaml
- hosts: recursors
  tasks:
    - name: Instance a, port 5301
      ansible.builtin.include_role:
        name: PowerDNS.pdns_recursor
      vars:
        pdns_rec_service_name: pdns-recursor@a
        pdns_rec_config_file: recursor-a.conf
        pdns_rec_flush_handlers: true
        pdns_rec_config:
          incoming:
            listen: [127.0.0.1]
            port: "5301"

    - name: Instance b, port 5302
      ansible.builtin.include_role:
        name: PowerDNS.pdns_recursor
      vars:
        pdns_rec_service_name: pdns-recursor@b
        pdns_rec_config_file: recursor-b.conf
        pdns_rec_flush_handlers: true
        pdns_rec_config:
          incoming:
            listen: [127.0.0.1]
            port: "5302"
```

`meta: flush_handlers` is play-wide: it also runs handlers that earlier roles in the same play
notified. `pdns_rec_disable_handlers: true` skips the restart handlers entirely.

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

## Release notes

See the [CHANGELOG.md](https://github.com/PowerDNS/pdns_recursor-ansible/blob/master/CHANGELOG.md).

## Contributing

- Every pull request must include a [changelog fragment](https://docs.ansible.com/ansible/devel/community/collection_development_process.html#creating-a-changelog-fragment).
- Each changelog entry must include a link to the pull request.
- If the pull request addresses an issue, also include a link to the related issue.
- Ensure each changelog entry starts with a lowercase letter (immediately after the dash) and ends with a period.
- Copy [`fragment-example.yaml`](changelogs/fragment-example.yaml) into [`changelogs/fragments`](changelogs/fragments) and name it `num-pr-title.yaml`, where:
  - `num` is the pull request number
  - `pr-title` is the pull request title (use a short, filesystem-friendly version)

## Testing

Tests are performed by [Molecule](http://molecule.readthedocs.org/en/latest/).

```bash
$ pip install tox
```

To test all the scenarios run

```bash
$ tox
```

To run a custom molecule command

```bash
$ tox -e ansible216 -- molecule test -s pdns-rec-54
```

## License

See [LICENSE](https://github.com/PowerDNS/pdns_recursor-ansible/blob/master/LICENSE).
