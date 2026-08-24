# PowerDNS Recursor Ansible Role Release Notes

**Topics**

- <a href="#v2-2-0">v2\.2\.0</a>
    - <a href="#documentation-changes">Documentation Changes</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
    - <a href="#removed-features-previously-deprecated">Removed Features \(previously deprecated\)</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v2-1-0">v2\.1\.0</a>
    - <a href="#documentation-changes-1">Documentation Changes</a>
    - <a href="#major-changes">Major Changes</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide-1">Breaking Changes / Porting Guide</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#major-changes-1">Major Changes</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide-2">Breaking Changes / Porting Guide</a>
    - <a href="#removed-features-previously-deprecated-1">Removed Features \(previously deprecated\)</a>
    - <a href="#bugfixes-2">Bugfixes</a>
This changelog describes changes after version 1\.8\.0\.

<a id="v2-2-0"></a>
## v2\.2\.0

<a id="documentation-changes"></a>
### Documentation Changes

* document that <code>pdns\_rec\_user</code> and <code>pdns\_rec\_group</code> have to name the account the service starts as\, now that they are written to the configuration as <code>setuid</code> and <code>setgid</code>\. The packaged units already agree with them\; an override that changes <code>User\=</code>\, <code>Group\=</code> or <code>ExecStart</code> has to change them with it\, because a daemon asked to become an account other than the one it was started as exits rather than continue with the wrong privileges \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* document the baseline configuration\, the placement of <code>threads</code> and <code>max\_mthreads</code> under <code>recursor</code> rather than <code>outgoing</code>\, and the settings needed to enable the REST API \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* document the drop\-in removal\, the reload behaviour of the restart handler and that tag selection filters tasks but not handlers\, so <code>\-\-skip\-tags service</code> still restarts the service on a configuration change \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267)\)\.
* document the handler behaviour and the multi\-instance usage in the README \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264)\)\.
* document the role tags\, the check mode support \(converged hosts only\) and the package/service state variables in the README \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/263](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/263)\)\.

<a id="minor-changes"></a>
### Minor Changes

* add <code>incoming\.reuseport</code>\, <code>outgoing\.source\_address</code>\, <code>recursor\.extended\_resolution\_errors</code>\, <code>recursor\.threads</code> and <code>recursor\.max\_mthreads</code> to the baseline configuration the role merges <code>pdns\_rec\_config</code> over \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* add <code>pdns\_rec\_config\_dir\_mode</code> and <code>pdns\_rec\_config\_file\_mode</code>\. The directory mode is symbolic\, <code>u\=rwX\,g\=rX\,o\=</code>\, so that the capital <code>X</code> grants execute on directories\, and on files that already carry it\, but never marks a plain RPZ zone or include fragment executable \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* add <code>pdns\_rec\_flush\_handlers</code> to run the notified handlers at the end of the role instead of at the end of the play\, which is required when the role runs more than once in a play \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264)\)\.
* add the <code>multi\-instance</code> Molecule scenario\, which configures two instances in a single play \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264)\)\.
* apply the owner\, group and mode of every <code>pdns\_rec\_config\_additional\_dirs</code> entry to the whole tree\, so a file another role or the recursor itself placed there stays readable by the account the daemon runs as\. <code>pdns\_rec\_config\_dirs\_recurse</code> turns it off\, globally or per entry through a <code>recurse</code> key\. Symlinks are not followed\, so a link inside one of these directories \- an RPZ zone kept on shared storage\, say \- cannot turn the recursion into a chown and chmod of whatever it points at\. Three directories are never walked \- the configuration directory\, because it holds the <code>recursor\.yml\-dist</code> of the package\; the directory named by <code>recursor\.include\_dir</code>\, because it holds the operator\'s drop\-ins\; and the one named by <code>webservice\.api\_dir</code>\, because its contents are state the daemon rewrites \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* cap every collection in <code>requirements\.yml</code>\. A collection that raises its <code>requires\_ansible</code> in a new major would otherwise break the ansible\-core 2\.16 leg on the day it is published\, without a change in this repository \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* declare FreeBSD in the Galaxy metadata \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* declare the Arch Linux support the role already implements in the Galaxy metadata\, and cover it with a Molecule scenario that installs the recursor from the packages of the distribution \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* manage the service with <code>ansible\.builtin\.systemd\_service</code> on systemd hosts and with <code>ansible\.builtin\.service</code> on hosts without systemd\, instead of mixing the two modules across the service task and the handlers \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* read facts through <code>ansible\_facts</code> instead of the injected top\-level <code>ansible\_\*</code> variables\. ansible\-core deprecated that injection and removes it in 2\.24\, after which a role reading <code>ansible\_distribution</code> would break\. The Molecule configuration sets <code>inject\_facts\_as\_vars\: false</code>\, so a missed reference fails a test run instead of surfacing on a future ansible\-core \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* remove version suffixed apt and dnf repo files \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/258](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/258)\)
* rework apt and dnf repo file creation to stop using version suffixed file names which are not cleaned up on version changes \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/258](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/258)\)
* rewrite the duplicate test that decides whether <code>webservice\.api\_dir</code> needs an entry of its own\, from a membership test against a concatenated list to two separate comparisons\. The result is the same directory list\; the concatenation made <code>ansible\-lint</code> 26 fail the repository with a <code>jinja\[invalid\]</code> violation\, <code>can only concatenate str \(not \"list\"\) to str</code>\, because the rule renders the referenced variable to a string before evaluating the expression \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/269](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/269)\)\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* require ansible\-core 2\.16 or newer\. Support for 2\.15 is dropped\, and Enterprise Linux 8 targets must be managed with 2\.16 because their system Python is 3\.6 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* restrict <code>incoming\.allow\_from</code> to <code>127\.0\.0\.0/8</code>\. The recursor\'s own default is the RFC 1918 set plus loopback and link\-local \(<code>10\.0\.0\.0/8</code>\, <code>100\.64\.0\.0/10</code>\, <code>169\.254\.0\.0/16</code>\, <code>192\.168\.0\.0/16</code>\, <code>172\.16\.0\.0/12</code>\, <code>\:\:1/128</code>\, <code>fc00\:\:/7</code>\, <code>fe80\:\:/10</code>\)\, and the baseline now replaces it rather than adding to it\, because <code>ansible\.builtin\.combine</code> overwrites a list instead of merging it\. A deployment that relies on the default to serve clients on a private range therefore starts refusing them after this upgrade\, and one that serves IPv6 loses <code>\:\:1/128</code>\. Declare the ranges the host should answer for in <code>pdns\_rec\_config\.incoming\.allow\_from</code> \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.

<a id="removed-features-previously-deprecated"></a>
### Removed Features \(previously deprecated\)

* stop testing the <code>rec\-master</code> repository and the 5\.1 series\, and test the three most recent release series instead\. The <code>pdns\_rec\_powerdns\_repo\_master</code> and <code>pdns\_rec\_powerdns\_repo\_51</code> presets are unchanged and still usable \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.

<a id="bugfixes"></a>
### Bugfixes

* correct the FreeBSD service name\, configuration directory and daemon path\. The rc script is <code>pdns\_recursor</code>\, the configuration lives in <code>/usr/local/etc/pdns</code> and the daemon is <code>/usr/local/sbin/pdns\_recursor</code>\, following the <code>dns/powerdns\-recursor</code> port\. The configuration check no longer hardcodes <code>/usr/sbin</code> \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* create the directories named by <code>recursor\.include\_dir</code> and <code>webservice\.api\_dir</code>\. The recursor reads that setting whether or not the webserver is enabled and exits with <code>No such file or directory</code> when the directory is absent\, so a configuration that set it without also listing the directory in <code>pdns\_rec\_config\_additional\_dirs</code> left the daemon unable to start\. The same is true of <code>recursor\.include\_dir</code>\, which the baseline now declares\. The API directory is owned by <code>pdns\_rec\_user</code>\, because the REST API writes into it \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* install the recursor on FreeBSD\. <code>tasks/main\.yml</code> includes <code>install\-\{\{ ansible\_facts\.system \}\}\.yml</code> and only the Linux variant existed\, so a FreeBSD run failed at the installation step\. The new task installs through <code>ansible\.builtin\.package</code> and skips the debug symbols package\, which FreeBSD does not ship \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* keep <code>recursor\.include\_dir</code> in the configuration the role writes\. The role writes over the file the packages ship\, which declares it\, so the directory an operator keeps drop\-ins in was no longer read \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* read the service name and state from facts published per role invocation in the restart handlers\. Ansible shares handlers between invocations of the same role and resolves role parameters to the last invocation\, so a play with more than one instance restarted the wrong service\. Correct restarts also need <code>pdns\_rec\_flush\_handlers</code> set to <code>true</code> \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/264)\)\.
* reload the systemd units in the same task that restarts the service\. A restart can no longer run against a unit systemd has not read\, and a host left with a drop\-in systemd never loaded is repaired by the next change instead of restarting onto the stale unit \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267)\)\.
* reload the systemd units in the service task when this run changed the drop\-in\. Handlers flush at the end of the play\, so a service that was not running yet was started from the unit systemd had loaded before the run and kept the previous settings until the handler restarted it \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267)\)\.
* remove <code>/etc/systemd/system/\<service name\>\.service\.d/</code> when <code>pdns\_rec\_package\_state</code> is <code>absent</code>\, so a later reinstall does not inherit the overrides of the previous installation\. The task is tagged <code>install</code>\, because removal runs through the install path \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267)\)\.
* remove <code>/etc/systemd/system/\<service name\>\.service\.d/override\.conf</code> when the merged service overrides are empty\, and restart the service\. The file used to stay on disk\, so emptying <code>pdns\_rec\_service\_overrides</code> kept the previous overrides applied forever\. Other drop\-ins in that directory are left alone \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267)\)\.
* restart the service on hosts without systemd\. The restart handler and the <code>daemon\_reload</code> handler used the systemd module unconditionally\, so a FreeBSD run failed as soon as a configuration change notified them \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* restore <code>recursor\.setuid</code> and <code>recursor\.setgid</code> in the configuration the role writes\. They were dropped when the configuration moved to the <code>pdns\_rec\_config</code> dictionary\, so the file no longer told the recursor to drop privileges and a start that does not come from the packaged unit \- a hand\-written unit\, an <code>ExecStart</code> override installed through <code>pdns\_rec\_service\_overrides</code>\, or a run outside systemd \- left the daemon running as the account that launched it \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* skip the debug symbols package when the platform ships none\. Arch Linux has no <code>pdns\-recursor\-dbg</code> package\, so enabling <code>pdns\_rec\_install\_debug\_symbols\_package</code> there failed \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/266)\)\.
* skip the restart under <code>\-\-skip\-tags service</code>\. Ansible filters tasks by tag but not handlers\, so a run that deliberately left the service alone still restarted it on a configuration change \- and restarting an inactive unit starts it\. The handlers read <code>ansible\_skip\_tags</code> and still reload the units\, so a <code>\-\-tags config</code> run is unaffected \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267)\)\.
* stop marking supplementary files executable\. <code>pdns\_rec\_config\_additional\_files</code> were written with mode <code>0750</code>\, which is meaningless for files the recursor only ever reads\, such as RPZ zones and include fragments\. They are now written with <code>pdns\_rec\_config\_file\_mode</code>\, <code>0640</code> by default \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/268)\)\.
* tag the <code>Set fact for repo name</code> task with <code>install</code> and <code>repository</code> so that <code>pdns\_rec\_repo\_name</code> and <code>pdns\_rec\_repo\_regex</code> are defined in filtered runs \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/263](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/263)\)\.
* tag the tasks inside <code>configure\.yml</code>\, <code>install\-\*\.yml</code> and <code>repo\-\*\.yml</code> so that <code>\-\-tags config</code>\, <code>\-\-tags install</code> and <code>\-\-tags repository</code> no longer run the include and skip its body\. A dynamic <code>include\_tasks</code> does not pass its tags to the tasks it includes\, so filtered runs silently did nothing and still exited 0 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/263](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/263)\)\.
* write the drop\-in from the same value the template renders\. The task was skipped on an empty <code>pdns\_rec\_service\_overrides</code> while the template renders the merge of that variable with the platform defaults\. No shipped platform sets a default override today\, so this was latent\, but a default added later would not have reached the unit \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/267)\)\.

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="documentation-changes-1"></a>
### Documentation Changes

* document <code>pdns\_rec\_package\_state</code>\, <code>pdns\_rec\_bin\_name</code>\, and <code>pdns\_rec\_service\_overrides</code> variables in the README \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* fix YAML boolean conventions in README examples \(<code>True</code>/<code>False</code> → <code>true</code>/<code>false</code>\) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* update README with PowerDNS Recursor 5\.4\.x repository installation example \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* update custom repository example to reflect deb822 migration \(removed <code>apt\_repo</code> and <code>gpg\_key\_id</code>\, added <code>apt\_version</code>\) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="major-changes"></a>
### Major Changes

* add type\-normalizing Jinja2 macro to <code>recursor\.conf\.j2</code> that automatically converts stringified integers\, floats\, booleans\, and lists to their native YAML types when rendering the configuration \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="minor-changes-1"></a>
### Minor Changes

* add <code>pdns\_rec\_package\_state</code> variable to allow controlling the desired state of the PowerDNS Recursor packages \(present\, latest\, or absent\) \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* add support for PowerDNS Recursor 5\.4\.x repository including repo definition\, molecule test scenario\, and CI integration\. \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* normalize <code>ansible\_architecture</code> to lowercase when mapping to APT architecture names to handle inconsistent facts \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* use Ansible Vault for the webservice <code>api\_key</code> in molecule test variables to verify that vaulted values are correctly decrypted and rendered into the configuration file \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="breaking-changes--porting-guide-1"></a>
### Breaking Changes / Porting Guide

* Ubuntu 20\.04 has been removed from molecule test scenarios \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* the Debian repository setup now exclusively uses <code>ansible\.builtin\.deb822\_repository</code> — the legacy <code>apt\_key</code>/<code>apt\_repository</code> fallback for Ubuntu \< 22\.04 has been removed\. This requires <code>python3\-debian</code> on target hosts and Ansible \>\= 2\.15 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* the <code>apt\_repo</code> and <code>gpg\_key\_id</code> keys are no longer used in custom repository definitions\; use <code>apt\_version</code> and <code>gpg\_key</code> instead \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.
* the <code>powerdns\-recursor\.sources\.j2</code> template has been removed \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/245)\)\.

<a id="bugfixes-1"></a>
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

<a id="minor-changes-2"></a>
### Minor Changes

* added the ability to mask the service\. Useful for multi\-instance Recursor deployments \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="breaking-changes--porting-guide-2"></a>
### Breaking Changes / Porting Guide

* minimum supported Ansible version is 2\.15 \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
* the variable pdns\_rec\_service\_overrides now allows overriding any section in the service unit definition \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="removed-features-previously-deprecated-1"></a>
### Removed Features \(previously deprecated\)

* removed variables pdns\_rec\_custom\_config\, pdns\_rec\_config\_from\_files\, and pdns\_rec\_config\_from\_files\_dir\_mode \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.

<a id="bugfixes-2"></a>
### Bugfixes

* fixed Molecule DNS resolution tests by ensuring the dnspython library is installed on hosts \([https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234](https\://github\.com/PowerDNS/pdns\_recursor\-ansible/pull/234)\)\.
