PowerDNS Recursor Role
======================
An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Recursor.

This role is considered alpha quality at the moment, issues and pull requests
are accepted.

Requirements
------------
An Ansible installation.

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
How to install PowerDNS, either 'packages' or 'source'. 'packages' by default.
Source installations are not supported yet.

### pdns_rec_repo_provider
When using 'packages' for pdns_rec_installation_type, use operating system packages
('os') or the PowerDNS repository ('PowerDNS'). This is 'os' by default.

### pdns_rec_repo_branch
When installing from the PowerDNS repository, what branch should be installed?
Currently only 'master' is supported.

### pdns_rec_user
The user to run the PowerDNS Recursor as, this is 'pdns' by default on Debian
systems and 'pdns-recursor' on CentOS/RHEL. This user is not created.

### pdns_rec_group
The group to run the PowerDNS Recursor as, this is 'pdns' by default on Debian
systems and 'pdns-recursor' on CentOS/RHEL. This group is not created.

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
