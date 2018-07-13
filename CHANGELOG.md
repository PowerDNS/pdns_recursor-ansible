## v1.0.0 (To be released)

__BREAKING CHANGES__:
- Rename the `pdns_rec_lua_config_file_content` to `pdns_rec_config_lua_file_content`
- Rename the `pdns_rec_lua_dns_script_content` to `pdns_rec_config_lua_dns_script_file_content`

IMPROVEMENTS:
- Continuos testing with molecule 2.14.0 ([\#39](https://github.com/PowerDNS/pdns-ansible/pull/39))
- Improved documentation ([\#39](https://github.com/PowerDNS/pdns-ansible/pull/39))
- Install debuginfo packages ([\#38](https://github.com/PowerDNS/pdns-ansible/pull/38))
- Add support for systemd overrides ([\#37](https://github.com/PowerDNS/pdns-ansible/pull/37))

BUG FIXES:
- Fix the examples in the README file ([\#31](https://github.com/PowerDNS/pdns-ansible/pull/31))
- Handle different version string for Debian and CentOS ([\#30](https://github.com/PowerDNS/pdns-ansible/pull/30))

## v0.1.1 (2017-09-29)

NEW FEATURES:
- Install specific PowerDNS Recursor versions ([\#29](https://github.com/PowerDNS/pdns-ansible/pull/29))

IMPROVEMENTS:
- Add support to the PowerDNS Recursor 4.1.x releases ([\#28](https://github.com/PowerDNS/pdns-ansible/pull/28))
- Fixing minor linter issues with whitespace ([\#30](https://github.com/PowerDNS/pdns-ansible/pull/30))

BUG FIXES:
- Handle correctly the `include-dir` configuration setting when defined

## v0.1.0 (2017-06-09)

Initial release.

NEW FEATURES:
- PowerDNS Recursor installation and configuration with Red-Hat and Debian support

IMPROVEMENTS:
- Switch to the MIT License ([\#27](https://github.com/PowerDNS/pdns-ansible/pull/27))
- Overall role refactoring ([\#19](https://github.com/PowerDNS/pdns-ansible/pull/19))
