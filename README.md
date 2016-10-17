PowerDNS Recursor Role
======================

An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Recursor.

Requirements
------------

An Ansible 2.0 or higher installation.

Dependencies
------------

This role depends on [`atosatto.package-extras`](https://galaxy.ansible.com/atosatto/package-extras/).

Role Variables
--------------

### pdns_rec_install_repo
By default the PowerDNS Recursor is installed using the os default repositories.
To install the PowerDNS Recursor package from the PowerDNS official repository
you can use the predefined settings located in the `vars/main.yml`:
`pdns_rec_install_repo: "{{ pdns_rec_official_pdns_repo }}"`.
It is also possible to pass to the role a custom repository location from
which install the packages.

### pdns_rec_repo_branch
When installing from the PowerDNS repository, the branch from which the packages
should be installed. Currently only 'master' and '40' (latest 4.0.x release) are supported.

### pdns_rec_user
The user to run the PowerDNS Recursor as, this is 'pdns' by default on Debian
systems and 'pdns-recursor' on CentOS/RHEL. This user is not created.

### pdns_rec_group
The group to run the PowerDNS Recursor as, this is 'pdns' by default on Debian
systems and 'pdns-recursor' on CentOS/RHEL. This group is not created.

### pdns_rec_config
A dict detailing the configuration of PowerDNS. You should not set the following
options here (other variables set these):
 * config-dir
 * set-uid
 * set-gid

### pdns_rec_config_dir
The directory where the configuration (`recursor.conf`) is stored. '/etc/powerdns'
by default.

### pdns_rec_lua_config_file_content
The content for the lua-config-file. This will place a file called `config.lua`
in [pdns_rec_config_dir](#pdns_rec_config_dir) and add the configuration to
`recursor.conf`.

### pdns_rec_lua_dns_script_content
The content for the lua-dns-script. This will place a file called `dns-script.lua`
in [pdns_rec_config_dir](#pdns_rec_config_dir) and add the configuration to load
this script to `recursor.conf`.

Example Playbook
----------------

Here we show some examples of usage of the PowerDNS.pdns_recursor role.

Install from custom repository:

> TODO

Bind to 203.0.113.53, port 5300 and allow only traffic from the 198.51.100.0/24
subnet:

```
- hosts: rec.example.net
  roles:
    - { role: PowerDNS.pdns_recursor,
        pdns_rec_config:
          'allow-from': '198.51.100.0/24'
          'local-address': '203.0.113.53:5300' }
```

Allow from multiple networks:

```
- hosts: rec.example.net
  roles:
    - { role: PowerDNS.pdns_recursor
        pdns_rec_config:
          'allow-from':
            - '198.51.100.0/24'
            - '203.0.113.53/24'
          'local-address': '203.0.113.53:5300' }
```

License
-------

GPLv2

Author Information
------------------

Pieter Lexis <pieter.lexis@powerdns.com>
Andrea Tosatto <andrea.tosatto@open-xchange.com>
