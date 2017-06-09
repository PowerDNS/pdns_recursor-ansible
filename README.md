PowerDNS Recursor Role
======================

An Ansible role created by the folks behind PowerDNS to install and configure
the PowerDNS Recursor.

Requirements
------------

An Ansible 2.0 or higher installation.

Dependencies
------------

This role depends on [`atosatto.packages-extras`](https://galaxy.ansible.com/atosatto/packages-extras/).
See the `requirements.yml` file for further details.

Role Variables
--------------

Available variables are listed below, along with default values (see `defaults/main.yml`):

    pdns_rec_install_repo: "" 

By default the PowerDNS Recursor is installed from the os default repositories.
You can install the PowerDNS Recursor package from official PowerDNS repository
overriding the `pdns_rec_install_repo` variable value as follows:

    # Install the PowerDNS Recursor from the 'master' branch
    - hosts: pdns-recursors
      roles:
      - { role: PowerDNS.pdns_recursor,
          pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_master }}"

    # Install the PowerDNS Recursor from the '40' branch
    - hosts: pdns-recursors
      roles:
      - { role: PowerDNS.pdns_recursor,
          pdns_rec_install_repo: "{{ pdns_rec_powerdns_repo_40 }}"

The roles also supports custom repositories

    - hosts: all
      vars:
        pdns_rec_install_repo:
          apt_repo_origin: "my.repo.com"  # used to pin the pdns-recursor to the provided PowerDNS repository
          apt_repo: "deb http://my.repo.com/{{ ansible_distribution | lower }} {{ ansible_distribution_release | lower }}/pdns-recursor main"
          gpg_key: "http://my.repo.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
          gpg_key_id: "MYREPOGPGPUBKEYID" # to avoid to reimport the key each time the role is executed
          yum_repo_baseurl: "http://my.repo.com/centos/$basearch/$releasever/pdns-recursor"
          yum_repo_name: "powerdns-rec"   # used to select only the pdns-recursor packages coming from this repo
      roles:
      - { role: PowerDNS.pdns_recursor }

If targeting only a specific platform (e.g. Debian) it's not needed to provide other platform (e.g. yum) repositories informations.

    pdns_rec_install_epel: True

By default the role installs also the EPEL repository.
EPEL is needed to satisfy some PowerDNS Recursor dependencies like `protobuf`.
If these dependencies are included into other repositories already configured in the
host or in the custom `pdns_rec_install_epel`, override this variable to `False`
to skip EPEL installation.

    pdns_rec_user: pdns   # pdns-recursor on CentOS/RHEL
    pdns_rec_group: pdns  # pdns-recursor on CentOS/RHEL

The user and group the PowerDNS Recursor will run as.
**NOTE**: This role does not create any user or group as we assume that they're created
by the package or other roles.

    pdns_rec_service_name: "pdns-recursor"

The name of the PowerDNS Recursor service.

    pdns_rec_flush_handlers: False

Force the execution of the flushing of the handlers at the end of the role.
**NOTE:** This is required if using this role to configure multiple recursor instances
in a single play to make sure that on configuration changes the correct pnds_recursor instance is restarted.

    pdns_rec_config_dir: "/etc/powerdns"
    pdns_rec_config_file: "recursor.conf"
    pdns_rec_config_lua: "{{ pdns_rec_config_dir }}/config.lua"
    pdns_rec_config_dns_script: "{{ pdns_rec_config_dir }}/dns-script.lua"

The PowerDNS Recursor configuration files and directories.

    pdns_rec_config: { }

A dict containing in YAML format the custom configuration of PowerDNS Recursor.
**NOTE**: You should not set the `config-dir`, `set-uid` and `set-gid` because are set by other role variables (respectively `pdns_rec_config_dir`, `pdns_rec_user`, `pdns_rec_group`).

    # pdns_rec_lua_config_file_content: ""

String containing the content of the lua-config-file file.
This will create a file called `config.lua` into the `pdns_rec_config_dir`
and add the configuration to the `recursor.conf` configuration file.

    # pdns_rec_lua_dns_script_content: ""

String containing the content of the lua-dns-script file.
This will create a file called `dns-script.lua` into the `pdns_rec_config_dir`
and add the configuration to load this script to the `recursor.conf`
configuration file.

Example Playbook
----------------

Here we show some examples of usage of the `PowerDNS.pdns_recursor` role.

Bind to `203.0.113.53` on port `5300` and allow only traffic from the `198.51.100.0/24` subnet:

    - hosts: pdns-recursors
      vars:
        pdns_rec_config:
          'allow-from': '198.51.100.0/24'
          'local-address': '203.0.113.53:5300'
      roles:
        - { role: PowerDNS.pdns_recursor }

Allow from multiple networks:

    - hosts: pdns-recursors
      vars:
        pdns_rec_config:
          'allow-from':
            - '198.51.100.0/24'
            - '203.0.113.53/24'
          'local-address': '203.0.113.53:5300'
      roles:
        - { role: PowerDNS.pdns_recursor }


License
-------

MIT
