PowerDNS Recursor Role
======================

An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Recursor.

This role is considered alpha quality at the moment, issues and pull requests
are accepted.

Requirements
------------

An Ansible 2.0 or higher installation.

Dependencies
------------

This role depends on [`atosatto.package-extras`](https://galaxy.ansible.com/atosatto/package-extras/).

Role Variables
--------------

### pdns_rec_config
A dict detailing the configuration of PowerDNS. You should not set the following
options here (other variables set these):
 * config-dir
 * set-uid
 * set-gid

### pdns_rec_config_dir
The directory where the configuration (`recursor.conf`) is stored. '/etc/powerdns'
by default.

### pdns_rec_installation_type
How to install the PowerDNS Recursor, either 'packages', 'source' or 'url'.
'packages' by default. Source installations are not supported yet.

### pdns_rec_repo_provider
When using 'packages' for pdns_rec_installation_type, use operating system packages
('os') or the PowerDNS repository ('powerdns'). This is 'os' by default.

### pdns_rec_repo_branch
When installing from the PowerDNS repository, what branch should be installed?
Currently only 'master' and '40' (latest 4.0.x release) are supported.

### pdns_rec_url
When `pdns_rec_installation_type` is 'url'. This is the URL to be fetched for the
package.

### pdns_rec_url_checksum
When `pdns_rec_installation_type` is 'url'. This is the checksum of the package
that is fetched from `pdns_rec_url` This should be in the format for the `checksum`
option of the [`get_url module`](http://docs.ansible.com/ansible/get_url_module.html).

### pdns_rec_user
The user to run the PowerDNS Recursor as, this is 'pdns' by default on Debian
systems and 'pdns-recursor' on CentOS/RHEL. This user is not created.

### pdns_rec_group
The group to run the PowerDNS Recursor as, this is 'pdns' by default on Debian
systems and 'pdns-recursor' on CentOS/RHEL. This group is not created.

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

Bind to 203.0.113.53, port 5300 and allow only traffic from the 198.51.100.0/24
subnet:
```
- hosts: rec.example.net
  roles:
    - role: PowerDNS.pdns_recursor
  vars:
    pdns_rec_config:
      'allow-from': '198.51.100.0/24'
      'local-address': '203.0.113.53:5300'
```

Allow from multiple networks:
```
- hosts: rec.example.net
  roles:
    - role: PowerDNS.pdns_recursor
  vars:
    pdns_rec_config:
      'allow-from':
        - '198.51.100.0/24'
        - '203.0.113.53/24'
      'local-address': '203.0.113.53:5300'
```

License
-------

GPLv2

Author Information
------------------

Pieter Lexis <pieter.lexis@powerdns.com>
Andrea Tosatto <andrea.tosatto@open-xchange.com>s
