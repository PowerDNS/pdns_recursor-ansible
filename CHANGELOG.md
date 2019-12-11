## v1.3.1 (2019-12-11)

IMPROVEMENTS:
- Make sure to restart the PowerDNS Recursor in case of changes to the systemd unit overrides ([\#52](https://github.com/PowerDNS/pdns_recursor-ansible/pull/52))
- Update the CI infrastructure to test the role against the Ansible 2.7, 2.8 and 2.9 releases ([\#51](https://github.com/PowerDNS/pdns_recursor-ansible/pull/51))
- Update the CI infrastructure to test against Debian 10 and the PowerDNS Recursor 4.2 ([\#51](https://github.com/PowerDNS/pdns_recursor-ansible/pull/51))

## v1.3.0 (2019-12-09)

IMPROVEMENTS:
- Add support to the PowerDNS Recursor 4.2.x and 4.3.x releases ([\#48](https://github.com/PowerDNS/pdns_recursor-ansible/pull/48))
- Stop interpreting 0 & 1 as no & yes in the PowerDNS Recuror configuration template ([\#49](https://github.com/PowerDNS/pdns_recursor-ansible/pull/49))

BUG FIXES:
- Fix the restart of the PowerDNS Recursor service in case of instances with different `pdns_rec_service_name` being configured in the same play ([\#50](https://github.com/PowerDNS/pdns_recursor-ansible/pull/50))

## v1.2.1 (2019-02-18)

IMPROVEMENTS:
- Improved PowerDNS Recursor config files and directories permissions handling ([\#44](https://github.com/PowerDNS/pdns_recursor-ansible/pull/44))

## v1.2.0 (2019-02-13)

NEW FEATURES:
- Allow to configure the status of the PowerDNS Recursor service ([\#45](https://github.com/PowerDNS/pdns_recursor-ansible/pull/45))

## v1.1.1 (2019-01-29)

BUG FIXES:
- Fix an issue with the PowerDNS Recursor configuration template resulting in the `threads` configuration being rendered wrongly

## v1.1.0 (2018-12-02)

NEW FEATURES:
- Allow to disable automated restart of the service on configuration changes ([\#43](https://github.com/PowerDNS/pdns_recursor-ansible/pull/43))

BUG FIXES:
- Fix handling of the `threads` option in the PowerDNS Recursor configuration template ([\#41](https://github.com/PowerDNS/pdns_recursor-ansible/pull/41))
- Fix handling of lists expansion in the PowerDNS Recursor configuration template ([\#42](https://github.com/PowerDNS/pdns_recursor-ansible/pull/42))

## v1.0.0 (2018-07-13)

__BREAKING CHANGES__:
- Rename the `pdns_rec_lua_config_file_content` variable to `pdns_rec_config_lua_file_content`
- Rename the `pdns_rec_lua_dns_script_content` variable to `pdns_rec_config_lua_dns_script_file_content`

NEW FEATURES:
- Update the CI infrastructure to use molecule 2.14.0 ([\#39](https://github.com/PowerDNS/pdns_recursor-ansible/pull/39))
- Add support to debuginfo packages installation ([\#38](https://github.com/PowerDNS/pdns_recursor-ansible/pull/38))
- Add support to systemd overrides definitions ([\#37](https://github.com/PowerDNS/pdns_recursor-ansible/pull/37))

IMPROVEMENTS:
- Improved documentation ([\#39](https://github.com/PowerDNS/pdns_recursor-ansible/pull/39))

BUG FIXES:
- Fix the examples in the README file ([\#31](https://github.com/PowerDNS/pdns_recursor-ansible/pull/31))
- Fix PowerDNS Recursor versions pinning for Debian and CentOS ([\#30](https://github.com/PowerDNS/pdns_recursor-ansible/pull/30))

## v0.1.1 (2017-09-29)

NEW FEATURES:
- Allow to pin the PowerDNS Recursor version to be installed ([\#29](https://github.com/PowerDNS/pdns_recursor-ansible/pull/29))

IMPROVEMENTS:
- Add support to the PowerDNS Recursor 4.1.x releases ([\#28](https://github.com/PowerDNS/pdns_recursor-ansible/pull/28))
- Fix minor linter issues with whitespace ([\#30](https://github.com/PowerDNS/pdns_recursor-ansible/pull/30))

BUG FIXES:
- Fix handling of the `include-dir` configuration setting when defined

## v0.1.0 (2017-06-09)

Initial release.

NEW FEATURES:
- PowerDNS Recursor installation and configuration with RHEL/CentOS and Debian/Ubuntu support

IMPROVEMENTS:
- Switch to the MIT License ([\#27](https://github.com/PowerDNS/pdns_recursor-ansible/pull/27))
- Overall role refactoring ([\#19](https://github.com/PowerDNS/pdns_recursor-ansible/pull/19))
