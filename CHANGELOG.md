## v1.1.1 (2010-01-29)

BUG FIXES:
- Fix an issue with the recursor.conf Jinja2 template resulting in the `threads` configuration being rendered wrongly

## v1.1.0 (2018-12-02)

NEW FEATURES:
- Add an option (`pdns_rec_disable_handlers`) to disable the automated restart of the service on configuration changes ([\#43](https://github.com/PowerDNS/pdns_recursor-ansible/pull/43))

BUG FIXES:
- Handle correctly the `threads` variable in the PowerDNS Recursor configuration template ([\#41](https://github.com/PowerDNS/pdns_recursor-ansible/pull/41))
- Ensure that lists are correctly expanded in the PowerDNS Recursor configuration template ([\#42](https://github.com/PowerDNS/pdns_recursor-ansible/pull/42))

## v1.0.0 (2018-07-13)

__BREAKING CHANGES__:
- Rename the `pdns_rec_lua_config_file_content` to `pdns_rec_config_lua_file_content`
- Rename the `pdns_rec_lua_dns_script_content` to `pdns_rec_config_lua_dns_script_file_content`

NEW FEATURES:
- Continuos testing with molecule 2.14.0 ([\#39](https://github.com/PowerDNS/pdns_recursor-ansible/pull/39))
- Install debuginfo packages ([\#38](https://github.com/PowerDNS/pdns_recursor-ansible/pull/38))
- Allow to manage systemd overrides ([\#37](https://github.com/PowerDNS/pdns_recursor-ansible/pull/37))

IMPROVEMENTS:
- Improved documentation ([\#39](https://github.com/PowerDNS/pdns_recursor-ansible/pull/39))

BUG FIXES:
- Fix the examples in the README file ([\#31](https://github.com/PowerDNS/pdns_recursor-ansible/pull/31))
- Handle different version string for Debian and CentOS ([\#30](https://github.com/PowerDNS/pdns_recursor-ansible/pull/30))

## v0.1.1 (2017-09-29)

NEW FEATURES:
- Install specific PowerDNS Recursor versions ([\#29](https://github.com/PowerDNS/pdns_recursor-ansible/pull/29))

IMPROVEMENTS:
- Add support to the PowerDNS Recursor 4.1.x releases ([\#28](https://github.com/PowerDNS/pdns_recursor-ansible/pull/28))
- Fixing minor linter issues with whitespace ([\#30](https://github.com/PowerDNS/pdns_recursor-ansible/pull/30))

BUG FIXES:
- Handle correctly the `include-dir` configuration setting when defined

## v0.1.0 (2017-06-09)

Initial release.

NEW FEATURES:
- PowerDNS Recursor installation and configuration with Red-Hat and Debian support

IMPROVEMENTS:
- Switch to the MIT License ([\#27](https://github.com/PowerDNS/pdns_recursor-ansible/pull/27))
- Overall role refactoring ([\#19](https://github.com/PowerDNS/pdns_recursor-ansible/pull/19))
