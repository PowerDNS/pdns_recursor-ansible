## v1.8.0 (2025-10-29)

NEW FEATURES:
- Add support for Ubuntu 24.04 in CI / Molecule tests ([\#176](https://github.com/PowerDNS/pdns_recursor-ansible/pull/176))
- Add Recursor 5.1 ([\#186](https://github.com/PowerDNS/pdns_recursor-ansible/pull/186))
- Add “archlinux” variable file for an Arch scenario ([\#196](https://github.com/PowerDNS/pdns_recursor-ansible/pull/196))
- Implement yaml config ([\#197](https://github.com/PowerDNS/pdns_recursor-ansible/pull/197))
- Add rec-52 ([\#200](https://github.com/PowerDNS/pdns_recursor-ansible/pull/200)
- Add role-specific tags to enable selective execution of tasks in large playbooks ([\#216](https://github.com/PowerDNS/pdns_recursor-ansible/pull/216))
- Add pre-flight checks (configuration validation before service restart) to avoid boot-loops ([\#214](https://github.com/PowerDNS/pdns_recursor-ansible/pull/214))
- Use YAML default config ([\#217](https://github.com/PowerDNS/pdns_recursor-ansible/pull/217))

IMPROVEMENTS:
- Bump docker from 6.1.3 to 7.0.0 ([\#170](https://github.com/PowerDNS/pdns_recursor-ansible/pull/170))
- Bump yamllint from 1.32.0 to 1.35.1 ([\#171](https://github.com/PowerDNS/pdns_recursor-ansible/pull/171))
- Small file permission fix ([\#174](https://github.com/PowerDNS/pdns_recursor-ansible/pull/174))
- Change default configuration format to YAML (instead of e.g. old format) ([\#195](https://github.com/PowerDNS/pdns_recursor-ansible/pull/195))
- CI tests: upgraded version of molecule and ansible-core packages ([\#202](https://github.com/PowerDNS/pdns_recursor-ansible/pull/202))
- Test configuration before restarting ([\#215](https://github.com/PowerDNS/pdns_recursor-ansible/pull/215))
- Update Molecule & CI: scenario rec-52, switch tests to YAML, update CI to ansible-core compatible, use HTTP for gpg_key to support Python 3.12 / Ansible 2.14 ([\#219](https://github.com/PowerDNS/pdns_recursor-ansible/pull/219))
- Clean up linting and CI issues in scenario rec-52 ([\#210](https://github.com/PowerDNS/pdns_recursor-ansible/pull/210))
- Improve CI pipeline for end-to-end sanity checks and more reliable builds ([\#211](https://github.com/PowerDNS/pdns_recursor-ansible/pull/211))


FIXED:
- GH Actions: fix issues with CI ([\#190](https://github.com/PowerDNS/pdns_recursor-ansible/pull/190))
- Fix regex to extract version of pdns_recursor (previous logic incorrectly captured “BV” etc) ([\#222](https://github.com/PowerDNS/pdns_recursor-ansible/pull/222))
- Fix Ansible version-comparison logic: avoid comparing to integer 0 (use string) to support newer versions correctly ([\#221](https://github.com/PowerDNS/pdns_recursor-ansible/pull/221))
- Fix pipeline stability after removing EOL platforms from test matrix ([\#191](https://github.com/PowerDNS/pdns_recursor-ansible/pull/191))

REMOVED / DEPRECATED: 
- Remove support for RHEL 7 and Debian 10 from the CI/test matrix (they have reached EOL) ([\#191](https://github.com/PowerDNS/pdns_recursor-ansible/pull/191))
- Remove pdns-recursor 4.8.x and 4.9.x from testing scenarios (EOL) ([\#219](https://github.com/PowerDNS/pdns_recursor-ansible/pull/219))
- Remove Ubuntu 20.04 from the CI/test matrix (EOL) ([\#219](https://github.com/PowerDNS/pdns_recursor-ansible/pull/219))
- repo-Debian: remove installing apt-transport-https ([\#220](https://github.com/PowerDNS/pdns_recursor-ansible/pull/220))

REVERTED:
- Revert PR “Recursor 2.0” (#225) — the large feature bump (support for 5.1/5.2/5.3, deb822 repos, min Ansible 2.15, handlers) was merged but immediately reverted; none of its changes are included in v1.8.0. ([\#225](https://github.com/PowerDNS/pdns_recursor-ansible/pull/225))

## v1.7.1 (2024-04-04)

NEW FEATURES:
- Added OL9, Rocky9 AlmaLinux8 and AlamLinux9 to CI ([\#157](https://github.com/PowerDNS/pdns_recursor-ansible/pull/157))

IMPROVEMENTS:
- Bump CI actions/checkout from 3 to 4 ([\#140](https://github.com/PowerDNS/pdns_recursor-ansible/pull/140))
- Replace the deprecated include with include_task ([\#152](https://github.com/PowerDNS/pdns_recursor-ansible/pull/152))
- Bump CI actions/setup-python from 4 to 5 ([\#160](https://github.com/PowerDNS/pdns_recursor-ansible/pull/160))
- Bump CI pytest-testinfra from 8.1.0 to 10.1.0 ([\#165](https://github.com/PowerDNS/pdns_recursor-ansible/pull/165))
- Fix all non line-length related ansible linting errors ([\#166](https://github.com/PowerDNS/pdns_recursor-ansible/pull/166))
- Bump CI ansible-lint from 6.18.0 to 24.2.1 ([\#167](https://github.com/PowerDNS/pdns_recursor-ansible/pull/167))

## v1.7.0 (2024-01-12)

NEW FEATURES:
- Added 4.9 repositories ([\#131](https://github.com/PowerDNS/pdns_recursor-ansible/pull/131))
- Added Ubuntu 22.04 to CI ([\#132](https://github.com/PowerDNS/pdns_recursor-ansible/pull/132))
- Added 5.0 repositories ([\#154](https://github.com/PowerDNS/pdns_recursor-ansible/pull/154))
- Added Debian bullseye and bookworm to CI ([\#155](https://github.com/PowerDNS/pdns_recursor-ansible/pull/155))

IMPROVEMENTS:
- Bump CI pytest-testinfra ([\#105](https://github.com/PowerDNS/pdns_recursor-ansible/pull/105))
- Fix indentation for pdns_rec_service_overrides. ([\#109](https://github.com/PowerDNS/pdns_recursor-ansible/pull/109))
- Bump CI ([\#130](https://github.com/PowerDNS/pdns_recursor-ansible/pull/130))
- Bump CI ansible-lint ([\#130](https://github.com/PowerDNS/pdns_recursor-ansible/pull/137))

REMOVED FEATURES:
- EOL repositories (v4.6) have been removed - CI have been modified as well ([\#129](https://github.com/PowerDNS/pdns_recursor-ansible/pull/129))
- EOL repositories (v4.7) have been removed - CI have been modified as well ([\#154](https://github.com/PowerDNS/pdns_recursor-ansible/pull/154))
- EOL Ubuntu 18.04 removed from CI ([\#154](https://github.com/PowerDNS/pdns_recursor-ansible/pull/154))

## v1.6.0 (2023-03-08)

NEW FEATURES:
- Added 4.6 and 4.7 repositories ([\#77](https://github.com/PowerDNS/pdns_recursor-ansible/pull/77))
- Added 4.8 repositories ([\#93](https://github.com/PowerDNS/pdns_recursor-ansible/pull/93))
- Replaced centos8 with OracleLinux8 in CI ([\#78](https://github.com/PowerDNS/pdns_recursor-ansible/pull/78))
- rec: add copy files for *-from-file configuration directives ([\#94](https://github.com/PowerDNS/pdns_recursor-ansible/pull/94))

IMPROVEMENTS:
- Bump CI checkout actions to v3 ([\#79](https://github.com/PowerDNS/pdns_recursor-ansible/pull/79))
- Bump CI setup Python to v4 ([\#80](https://github.com/PowerDNS/pdns_recursor-ansible/pull/80))
- Bump CI yamllint to 1.28.0 ([\#84](https://github.com/PowerDNS/pdns_recursor-ansible/pull/84))

REMOVED FEATURES:
- EOL repositories (v4.3 v4.4 v4.5) have been removed - CI have been modified as well ([\#93](https://github.com/PowerDNS/pdns_recursor-ansible/pull/93))

## v1.5.0 (2021-07-02)

NEW FEATURES:
- Add 4.5 repositories ([\#72](https://github.com/PowerDNS/pdns_recursor-ansible/pull/72))

IMPROVEMENTS:
- Fix check-mode ([\#71](https://github.com/PowerDNS/pdns_recursor-ansible/pull/71), [\#73](https://github.com/PowerDNS/pdns_recursor-ansible/pull/73))

REMOVED FEATURES:
- Remove 4.0, 4.1, 4.2 repositories ([\#68](https://github.com/PowerDNS/pdns_recursor-ansible/pull/68) and [\#72](https://github.com/PowerDNS/pdns_recursor-ansible/pull/72))

## v1.4.0 (2020-09-16)

NEW FEATURES:
- FreeBSD support created by @Godwottery ([\#47](https://github.com/PowerDNS/pdns_recursor-ansible/pull/47) and [\#64](https://github.com/PowerDNS/pdns_recursor-ansible/pull/64))
- Support for "Other" distributions ([\#61](https://github.com/PowerDNS/pdns_recursor-ansible/pull/61))

IMPROVEMENTS:
- Repositories for PowerDNS Recursor 4.4 added ([\#62](https://github.com/PowerDNS/pdns_recursor-ansible/pull/62))

## v1.3.2 (2020-03-06)

IMPROVEMENTS:
- Use HTTPs everywhere to connect to the PowerDNS repositories ([\#55](https://github.com/PowerDNS/pdns_recursor-ansible/pull/55),[\#57](https://github.com/PowerDNS/pdns_recursor-ansible/pull/57))

BUG FIXES:
- Fix the default `pdns_rec_service_overrides` to work with the Recursor 4.3.x ([\#56](https://github.com/PowerDNS/pdns_recursor-ansible/pull/56))

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
