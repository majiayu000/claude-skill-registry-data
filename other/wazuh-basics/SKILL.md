---
name: wazuh-basics
description: Use when deploying or operating Wazuh for host-based
  intrusion detection on infrastructure you are authorized to defend.
  Covers manager and agent architecture, agent enrollment, file integrity
  monitoring, security configuration assessment, custom rules and
  decoders, vulnerability detection, active response, and agent health
  monitoring. Use when the team needs EDR-lite visibility on servers and
  workstations, when tuning noisy Wazuh rules, or when onboarding new
  hosts to the Wazuh fleet.
version: 1.0.0
domain: soc
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [incident-response, forensics-fundamentals]
tools:
  - name: Wazuh
    version: 4.x
  - name: Sysmon
    version: 15.x
  - name: Python
    version: "3.12"
---

Wazuh is an open source security platform that combines host intrusion
detection, file integrity monitoring, log analysis, vulnerability
detection, and configuration assessment in one manager-plus-agents
architecture. This skill covers deploying and operating Wazuh 4.x
defensively: enrolling agents, writing rules and decoders, monitoring
file integrity, and responding with active response. Use it on your own
fleet or a client environment you are authorized to monitor.

## Quick Workflow

1. Install the Wazuh manager (single node for labs, cluster for
   production) and confirm the API and dashboard are reachable.
2. Enroll agents on a pilot group first, verify they check in and send
   logs.
3. Enable file integrity monitoring on critical paths and security
   configuration assessment with the CIS benchmark for your OS.
4. Review the default rules firing in the pilot, tune or disable the
   noisy ones with documented justification.
5. Write one custom rule and decoder for an application log your team
   cares about.
6. Enable vulnerability detection and review the first inventory for
   false positives before alerting on it.
7. Configure active response for high-confidence cases only (for
   example block an IP after repeated SSH brute force).
8. Roll out to the full fleet in waves, watching agent health and
   manager load at each step.

## 1. Architecture and installation

Wazuh has four parts: the manager (analysis engine), the indexer
(OpenSearch storage), the dashboard (web UI), and agents on endpoints.
For a lab, the all-in-one install is fastest:

```bash
# All-in-one install (lab only, single node)
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
sudo bash wazuh-install.sh -a

# After install, note the printed admin credentials and dashboard URL
# Dashboard: https://<manager-ip>  API: https://<manager-ip>:55000

# Check service health
sudo systemctl status wazuh-manager wazuh-indexer wazuh-dashboard
```

For production, split the roles across nodes and follow the official
cluster documentation. Keep the install script version pinned so
rebuilds are reproducible.

## 2. Agent enrollment

Agents authenticate to the manager with a key. Enroll securely:

```bash
# On the manager: create an agent entry and get its key
sudo /var/ossec/bin/manage_agents
# Choose (A)dd, enter name, IP (or 'any'), then (E)xtract key for the ID

# On the agent (Linux): install and enroll
sudo WAZUH_MANAGER='manager.internal' WAZUH_AGENT_NAME='web01' \
  dpkg -i wazuh-agent_4.14.0-1_amd64.deb
sudo /var/ossec/bin/agent-auth -m manager.internal -A web01

# Verify enrollment from the manager
sudo /var/ossec/bin/agent_control -l
```

For Windows agents, use the MSI with the same `agent-auth` step, or
pre-shared keys via the API for automation. Rotate agent keys if one
leaks, and never reuse one key across hosts.

Verify agents are alive and sending data:

```bash
# List agents with last keep-alive
sudo /var/ossec/bin/agent_control -l

# Check an agent's reported syscheck and rootcheck status
sudo /var/ossec/bin/agent_control -i 001
```

## 3. File integrity monitoring

FIM watches critical files and alerts on changes. Configure in the
agent's `ossec.conf` (or centralized agent configuration):

```xml
<syscheck>
  <frequency>7200</frequency>
  <directories check_all="yes" realtime="yes">/etc,/usr/bin,/usr/sbin</directories>
  <directories check_all="yes" realtime="yes">/bin,/sbin,/boot</directories>
  <ignore>/etc/mtab</ignore>
  <ignore>/etc/hosts.deny</ignore>
  <nodiff>/etc/ssl/private.key</nodiff>
</syscheck>
```

On Windows, monitor `C:\Windows\System32`, autorun registry keys, and
service binaries. Use `realtime="yes"` on small critical paths and
scheduled scans on large trees to control load.

Triage a FIM alert:

```bash
# Find what changed on web01 in the last day (dashboard or API)
curl -k -u wazuh:wazuhpass \
  "https://manager.internal:55000/syscheck/001?pretty" | head -40

# On the host, check package ownership of a changed binary
dpkg -S /usr/bin/suspicious 2>/dev/null || rpm -qf /usr/bin/suspicious
```

A changed system binary with no package update behind it is an
incident until proven otherwise.

## 4. Rules and decoders

Wazuh decodes logs with decoders, then matches rules. Write a custom
decoder and rule for your application log:

```xml
<!-- /var/ossec/etc/decoders/local_decoder.xml -->
<decoder>
  <prematch>myapp: login failed</prematch>
  <regex>myapp: login failed user=(\w+) src=(\d+\.\d+\.\d+\.\d+)</regex>
  <order>user, srcip</order>
</decoder>
```

```xml
<!-- /var/ossec/etc/rules/local_rules.xml, rule IDs 100000+ are local -->
<group name="myapp,">
  <rule id="100001" level="5">
    <decoded_as>myapp</decoded_as>
    <description>MyApp login failure</description>
  </rule>
  <rule id="100002" level="10" frequency="8" timeframe="120">
    <if_matched_sid>100001</if_matched_sid>
    <same_srcip />
    <description>MyApp brute force: 8 failures from one IP in 2 minutes</description>
    <mitre>
      <id>T1110.001</id>
      <tactic>Credential Access</tactic>
      <technique>Password Guessing</technique>
    </mitre>
  </rule>
</group>
```

Test and reload:

```bash
# Validate the rule syntax before reloading
sudo /var/ossec/bin/wazuh-logtest
# Paste a sample log line, check the decoded fields and matched rule, Ctrl-C to exit

sudo systemctl reload wazuh-manager
```

Map rules to MITRE in the `<mitre>` block so the dashboard shows
technique coverage.

## 5. Security configuration assessment

SCA runs CIS benchmark checks against hosts and reports failures:

```bash
# SCA policies live on the manager; check which are enabled
ls /var/ossec/etc/sca/

# Review a host's failing checks in the dashboard under
# Security configuration assessment, or via API
curl -k -u wazuh:wazuhpass \
  "https://manager.internal:55000/sca/001?pretty" | head -60
```

Workflow: enable the CIS policy matching each OS, review failures in
the pilot group, fix the real misconfigurations, and document accepted
risks for the rest. Do not alert on every SCA failure; track the trend
(failing checks going down) as the metric.

## 6. Vulnerability detection

Wazuh builds a software inventory per agent and matches it against
vulnerability feeds:

```bash
# Trigger an immediate vulnerability scan on one agent (lab)
sudo /var/ossec/bin/agent_control -r 001 -u 001
```

Tune before you alert: the first scan always has false positives
(backported patches on RHEL/Debian report the base version). Verify a
sample of critical findings against the vendor advisory, then build
allow rules or adjust severity. Feed confirmed vulnerabilities into
your patching process, not into the SOC paging queue.

## 7. Active response

Active response runs a script on the agent when a rule fires. Use it
sparingly and only for reversible actions:

```xml
<!-- Block an IP at the firewall after SSH brute force (rule 5760 level 10+) -->
<command>
  <name>firewall-drop</name>
  <executable>firewall-drop.sh</executable>
  <timeout_allowed>yes</timeout_allowed>
</command>
<active-response>
  <command>firewall-drop</command>
  <location>local</location>
  <level>10</level>
  <timeout>600</timeout>
</active-response>
```

Rules for safe active response:

- Only trigger on high-confidence, high-level rules you have tuned.
- Always set a timeout so blocks expire automatically.
- Never auto-isolate production servers without a tested unblock path.
- Log every active response action and alert the SOC when one fires.
- Test in the lab by simulating the trigger and confirming both the
  block and the expiry.

## 8. Agent health and fleet operations

A blind agent is a blind spot. Monitor the fleet:

```bash
# Agents not reporting in the last hour
sudo /var/ossec/bin/agent_control -l | grep -B2 "Never connected\|disconnected"

# Manager load: queue sizes and event rates
tail -50 /var/ossec/logs/ossec.log | grep -i "warn\|error"
```

Operational habits:

- Alert when any production agent is disconnected for more than 1 hour.
- Version agent configs in git and push via centralized configuration.
- Upgrade agents in waves: canary group first, then 25 percent, then
  the rest, watching for enrollment or performance regressions.
- Track coverage: percentage of in-scope hosts with a reporting agent,
  reported weekly.

## Edge cases

- Agents behind NAT: use `any` as the agent IP at enrollment and rely
  on the agent key, not the source IP, for identity.
- Clock skew breaks vulnerability matching and SCA scheduling. Sync
  all hosts with NTP and alert on drift.
- FIM on busy directories (log folders, database data dirs) floods the
  manager. Monitor config and data separately; FIM is for binaries
  and configuration.
- Windows agents need the audit policy enabled to produce useful logs.
  Deploy the audit baseline via GPO alongside the agent.
- The manager disk fills with archives: set log rotation and
  retention, and monitor disk space as a first-class alert.
- Custom rules with `frequency` need the events to arrive in order;
  delayed logs can break the count. Prefer SIEM-side correlation for
  precise thresholds.

## Escalation

- Manager will not start: check `/var/ossec/logs/ossec.log`, validate
  XML configs with `wazuh-logtest` and `xmllint`, restore the last
  known-good config from git.
- Agents enroll but never send logs: check firewall port 1514/udp and
  1515/tcp, verify the manager address in `ossec.conf`, and look for
  TLS errors in the agent log.
- Rule changes have no effect: confirm you edited the manager's live
  config (not a backup copy), reloaded the manager, and that the rule
  ID does not collide with a built-in one.
- Active response fired wrongly: check the timeout expiry, review the
  triggering rule's precision, and demote or disable the response
  until retuned.
- You suspect manager compromise: agents keep local logs; collect them
  directly from hosts, rebuild the manager from known-good config,
  and re-enroll agents with fresh keys.

## Detection and defender view

Wazuh is the defender's sensor grid, so think about how attackers
defeat host telemetry:

- Attackers kill or uninstall the agent. Alert on agent disconnection
  and on the agent service stopping (Windows Event 7036/7040, Linux
  service stop), and treat unexpected gaps as incidents.
- Attackers modify FIM-monitored files and then restore them. Use
  `realtime` monitoring plus `check_all` hashes, and keep an offline
  copy of critical hashes for comparison.
- Attackers use fileless techniques that FIM never sees. Pair FIM
  with Sysmon process telemetry on the same hosts.
- Attackers exploit the delay between vulnerability scan and patch.
  Shrink the window: scan daily, patch criticals on SLA, and track
  mean time to patch.
- Tune so analysts trust the console: every false positive you leave
  in place teaches the team to ignore the next true positive.

## Key references

- MITRE ATT&CK T1110.001 (Password Guessing), T1070 (Indicator
  Removal), T1562.001 (Disable or Modify Tools), T1486 (Data Encrypted
  for Impact).
- Wazuh 4.x documentation: https://documentation.wazuh.com/
- CIS benchmarks (SCA policies): https://www.cisecurity.org/cis-benchmarks
- Wazuh ruleset reference: https://documentation.wazuh.com/current/user-manual/ruleset/ruleset.html
