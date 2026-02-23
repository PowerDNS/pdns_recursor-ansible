# PowerDNS Recursor Ansible Role Release Notes

**Topics**

- <a href="#v2-1-0">v2\.1\.0</a>
    - <a href="#documentation-changes">Documentation Changes</a>
    - <a href="#major-changes">Major Changes</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#major-changes-1">Major Changes</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide-1">Breaking Changes / Porting Guide</a>
    - <a href="#removed-features-previously-deprecated">Removed Features \(previously deprecated\)</a>
    - <a href="#bugfixes-1">Bugfixes</a>
This changelog describes changes after version 1\.8\.0\.

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="documentation-changes"></a>
### Documentation Changes

* document <code>pdns\_rec\_package\_state</code>\, <code>pdns\_rec\_bin\_name</code>\, and <code>pdns\_rec\_service\_overrides</code> variables in the README \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* fix YAML boolean conventions in README examples \(<code>True</code>/<code>False</code> → <code>true</code>/<code>false</code>\) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* update README with PowerDNS Recursor 5\.4\.x repository installation example \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* update custom repository example to reflect deb822 migration \(removed <code>apt\_repo</code> and <code>gpg\_key\_id</code>\, added <code>apt\_version</code>\) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="major-changes"></a>
### Major Changes

* add type\-normalizing Jinja2 macro to <code>recursor\.conf\.j2</code> that automatically converts stringified integers\, floats\, booleans\, and lists to their native YAML types when rendering the configuration \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="minor-changes"></a>
### Minor Changes

* add <code>pdns\_rec\_package\_state</code> variable to allow controlling the desired state of the PowerDNS Recursor packages \(present\, latest\, or absent\) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* add support for PowerDNS Recursor 5\.4\.x repository including repo definition\, molecule test scenario\, and CI integration\. \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* normalize <code>ansible\_architecture</code> to lowercase when mapping to APT architecture names to handle inconsistent facts \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* use Ansible Vault for the webservice <code>api\_key</code> in molecule test variables to verify that vaulted values are correctly decrypted and rendered into the configuration file \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* Ubuntu 20\.04 has been removed from molecule test scenarios \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* the Debian repository setup now exclusively uses <code>ansible\.builtin\.deb822\_repository</code> — the legacy <code>apt\_key</code>/<code>apt\_repository</code> fallback for Ubuntu \< 22\.04 has been removed\. This requires <code>python3\-debian</code> on target hosts and Ansible \>\= 2\.15 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* the <code>apt\_repo</code> and <code>gpg\_key\_id</code> keys are no longer used in custom repository definitions\; use <code>apt\_version</code> and <code>gpg\_key</code> instead \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* the <code>powerdns\-recursor\.sources\.j2</code> template has been removed \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="bugfixes"></a>
### Bugfixes

* fix <code>recursor\.conf\.j2</code> template to coerce <code>AnsibleVaultEncryptedUnicode</code> values to plain strings before type\-normalisation\, allowing <code>\!vault</code> encrypted values to be used directly inside configuration dicts \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* fix typo in debug symbols package variable name <code>default\_pdns\_recorsor\_debug\_symbols\_package\_name</code> to <code>default\_pdns\_rec\_debug\_symbols\_package\_name</code> in Archlinux\, Debian\, and Other vars files \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="major-changes-1"></a>
### Major Changes

* added support for Recursor 5\.1\.x\, 5\.2\.x\, and 5\.3\.x \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* added support for the arm64 architecture when installing the Recursor via the role \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* added tests for Debian Trixie and Enterprise Linux 10 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* improved YAML\-based configuration for the Recursor \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* migrated the role to use handlers to restart processes and services on changes \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* switched Debian\-based platforms to deb822\-style APT repositories \(requires Ansible \>\= 2\.15\)\. Inspired by \@l00d3r in [https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/213](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/213) and \@lpmhouben in [https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/218](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/218) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* updated Molecule test configuration files to YAML \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="minor-changes-1"></a>
### Minor Changes

* added the ability to mask the service\. Useful for multi\-instance Recursor deployments \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="breaking-changes--porting-guide-1"></a>
### Breaking Changes / Porting Guide

* minimum supported Ansible version is 2\.15 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* the variable pdns\_rec\_service\_overrides now allows overriding any section in the service unit definition \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="removed-features-previously-deprecated"></a>
### Removed Features \(previously deprecated\)

* removed variables pdns\_rec\_custom\_config\, pdns\_rec\_config\_from\_files\, and pdns\_rec\_config\_from\_files\_dir\_mode \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="bugfixes-1"></a>
### Bugfixes

* fixed Molecule DNS resolution tests by ensuring the dnspython library is installed on hosts \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
