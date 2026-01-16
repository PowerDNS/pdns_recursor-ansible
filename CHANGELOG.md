# PowerDNS Recursor Ansible Role Release Notes

**Topics**

- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#major-changes">Major Changes</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
    - <a href="#removed-features-previously-deprecated">Removed Features \(previously deprecated\)</a>
    - <a href="#bugfixes">Bugfixes</a>

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="major-changes"></a>
### Major Changes

* added support for Recursor 5\.1\.x\, 5\.2\.x\, and 5\.3\.x \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* added support for the arm64 architecture when installing the Recursor via the role \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* added tests for Debian Trixie and Enterprise Linux 10 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* improved YAML\-based configuration for the Recursor \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* migrated the role to use handlers to restart processes and services on changes \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* switched Debian\-based platforms to deb822\-style APT repositories \(requires Ansible \>\= 2\.15\)\. Inspired by \@l00d3r in [https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/213](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/213) and \@lpmhouben in [https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/218](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/218) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* updated Molecule test configuration files to YAML \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="minor-changes"></a>
### Minor Changes

* added the ability to mask the service\. Useful for multi\-instance Recursor deployments \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* minimum supported Ansible version is 2\.15 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* the variable pdns\_rec\_service\_overrides now allows overriding any section in the service unit definition \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="removed-features-previously-deprecated"></a>
### Removed Features \(previously deprecated\)

* removed variables pdns\_rec\_custom\_config\, pdns\_rec\_config\_from\_files\, and pdns\_rec\_config\_from\_files\_dir\_mode \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="bugfixes"></a>
### Bugfixes

* fixed Molecule DNS resolution tests by ensuring the dnspython library is installed on hosts \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
