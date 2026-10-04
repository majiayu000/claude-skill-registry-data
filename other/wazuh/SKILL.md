---
name: wazuh
description: "Expert agent for Wazuh open-source EDR/SIEM platform. Covers agent deployment, ossec.conf configuration, FIM, SCA, active response, custom rules and decoders, vulnerability detection, compliance (PCI DSS, HIPAA, GDPR), cluster deployment, and Wazuh indexer/dashboard setup. WHEN: \"Wazuh\", \"OSSEC\", \"open-source EDR\", \"FIM\", \"SCA\", \"Wazuh manager\", \"Wazuh agent\", \"ossec.conf\", \"active response\", \"Wazuh indexer\"."
license: MIT
---

# Wazuh

This skill covers Wazuh, the open-source security monitoring platform. It has deep expertise in Wazuh architecture (manager, agents, indexer, dashboard), ossec.conf configuration, File Integrity Monitoring (FIM), Security Configuration Assessment (SCA), active response, custom rule and decoder development, vulnerability detection, and regulatory compliance automation (PCI DSS, HIPAA, GDPR).

## How to Approach Tasks

When you receive a request:

1. **Identify the deployment model** — Single-node (all-in-one) vs. distributed cluster. Large environments (>100 agents) should use distributed deployment for scalability.

2. **Determine the version** — Wazuh 4.x is current (4.7.x as of 2024). Significant architecture changes between versions; confirm version before providing specific configuration guidance.

3. **Classify the request type:**
   - **Deployment / installation** — Load `references/architecture.md`
   - **ossec.conf configuration** — Agent or manager configuration
   - **Rule development** — Custom XML rules and decoders
   - **FIM configuration** — File integrity monitoring scope
   - **SCA** — Security configuration assessment policies
   - **Active response** — Automated response to alerts
   - **Compliance** — PCI DSS, HIPAA, GDPR mapping
   - **Vulnerability detection** — CVE scanning configuration

4. **Analyze** — Apply Wazuh-specific reasoning. Wazuh is highly configurable but requires more manual tuning than commercial EDR products. The quality of detections depends heavily on rule and decoder quality.

## Architecture Overview

See `references/architecture.md` for full architecture details.

**Core components:**
- **Wazuh Manager** — Receives agent data, runs detection rules, generates alerts
- **Wazuh Agent** — Lightweight agent on monitored endpoints (Linux, Windows, macOS)
- **Wazuh Indexer** — OpenSearch-based event storage and search (replaces Elasticsearch in older versions)
- **Wazuh Dashboard** — Kibana-based web console for analysis and management
- **Filebeat** — Forwards manager output to Wazuh Indexer (in distributed setups)

## Agent Deployment

Agents are installed via native packages (RPM, APT, MSI, PKG) for Linux, Windows, and macOS and pointed at the manager address. See `references/agent-deployment.md` for full install commands per platform.

## ossec.conf Configuration

The primary configuration file for both agents (`/var/ossec/etc/ossec.conf`) and the manager.

### Agent ossec.conf Structure

```xml
<ossec_config>
  <!-- Manager connection -->
  <client>
    <server>
      <address>wazuh-manager.corp.com</address>
      <port>1514</port>
      <protocol>tcp</protocol>
    </server>
    <enrollment>
      <enabled>yes</enabled>
    </enrollment>
  </client>

  <!-- Logging configuration -->
  <logging>
    <log_format>plain</log_format>
  </logging>

  <!-- File Integrity Monitoring -->
  <syscheck>
    <frequency>43200</frequency>  <!-- 12 hours -->
    <scan_on_start>yes</scan_on_start>
    
    <!-- Directories to monitor -->
    <directories realtime="yes" check_all="yes" report_changes="yes">
      /etc
    </directories>
    <directories check_all="yes">/usr/bin</directories>
    <directories check_all="yes">/usr/sbin</directories>
    <directories check_all="yes">/bin</directories>
    <directories check_all="yes">/sbin</directories>
    
    <!-- Windows specific -->
    <directories realtime="yes">%WINDIR%/System32</directories>
    <directories realtime="yes">%PROGRAMFILES%</directories>
    
    <!-- Ignore patterns -->
    <ignore>/etc/mtab</ignore>
    <ignore>/etc/hosts.deny</ignore>
    <ignore>/etc/mail/statistics</ignore>
    <ignore type="sregex">.log$|.tmp$|.swp$</ignore>
    
    <!-- Windows registry monitoring -->
    <windows_registry>HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run</windows_registry>
    <windows_registry>HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services</windows_registry>
  </syscheck>

  <!-- Log collection -->
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/auth.log</location>
  </localfile>
  
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/syslog</location>
  </localfile>
  
  <!-- Windows Event Log -->
  <localfile>
    <log_format>eventchannel</log_format>
    <location>Security</location>
    <query>Event/System[EventID != 4688]</query>  <!-- Exclude process creation if noisy -->
  </localfile>
  
  <localfile>
    <log_format>eventchannel</log_format>
    <location>System</location>
  </localfile>
  
  <localfile>
    <log_format>eventchannel</log_format>
    <location>Microsoft-Windows-Sysmon/Operational</location>
  </localfile>

  <!-- Active response (allow manager to run scripts on agent) -->
  <active-response>
    <disabled>no</disabled>
  </active-response>
</ossec_config>
```

### Manager ossec.conf Key Sections

```xml
<ossec_config>
  <!-- Global settings -->
  <global>
    <jsonout_output>yes</jsonout_output>
    <alerts_log>yes</alerts_log>
    <logall>no</logall>
    <logall_json>no</logall_json>
    <email_notification>yes</email_notification>
    <smtp_server>smtp.corp.com</smtp_server>
    <email_from>wazuh@corp.com</email_from>
    <email_to>soc@corp.com</email_to>
    <email_maxperhour>12</email_maxperhour>
    <email_log_source>alerts.log</email_log_source>
  </global>

  <!-- Alert levels -->
  <alerts>
    <log_alert_level>3</log_alert_level>    <!-- Minimum level to log -->
    <email_alert_level>10</email_alert_level> <!-- Minimum level to email -->
  </alerts>

  <!-- Remote (agent communication) -->
  <remote>
    <connection>secure</connection>
    <port>1514</port>
    <protocol>tcp</protocol>
    <allowed-ips>10.0.0.0/8</allowed-ips>
  </remote>

  <!-- Vulnerability detection -->
  <vulnerability-detection>
    <enabled>yes</enabled>
    <index-status>yes</index-status>
    <feed-update-interval>60m</feed-update-interval>
  </vulnerability-detection>
</ossec_config>
```

## Custom Rules

Wazuh rules are XML-based and stored in `/var/ossec/etc/rules/` (custom) or `/var/ossec/ruleset/rules/` (default, do not edit).

### Rule Anatomy

```xml
<group name="custom_rules,">
  <!-- Rule structure -->
  <rule id="100001" level="10">
    <!-- Match criteria -->
    <if_sid>5501</if_sid>                        <!-- Match if parent rule 5501 fires -->
    <match>sshd</match>                          <!-- String match in log -->
    <regex>Failed password for root</regex>      <!-- Regex match -->
    <field name="srcip">192\.168\.0\.\d+</field> <!-- Match specific field -->
    
    <!-- Alert metadata -->
    <description>SSH brute force: Multiple failed logins for root</description>
    <group>authentication_failed,pci_dss_10.2.4,gpg13_7.1,gdpr_IV_35.7.d,</group>
    <mitre>
      <id>T1110</id>  <!-- Brute Force -->
    </mitre>
    <options>no_full_log</options>  <!-- Don't include full raw log in alert -->
  </rule>

  <!-- Frequency-based rule (trigger after N events in T seconds) -->
  <rule id="100002" level="12">
    <if_matched_sid>100001</if_matched_sid>     <!-- Based on rule 100001 firing -->
    <same_source_ip />                           <!-- Same IP must trigger repeatedly -->
    <description>SSH brute force: Source IP with multiple root login failures</description>
    <mitre>
      <id>T1110.001</id>
    </mitre>
    <options>no_full_log</options>
    <frequency>8</frequency>                     <!-- 8 occurrences -->
    <timeframe>120</timeframe>                   <!-- Within 120 seconds -->
  </rule>
</group>
```

### Rule Severity Levels

| Level | Meaning | Examples |
|---|---|---|
| 0-2 | Ignore / system noise | Agent start/stop |
| 3-4 | Low: Notable activity | User logins |
| 5-7 | Low-Medium: Uncommon activity | Unusual process |
| 8-9 | Medium: Error / anomaly | Authentication failure |
| 10-12 | High: Attack behavior | Brute force, rootkit |
| 13-15 | Critical: Confirmed attack | Successful exploit |

### Custom Rule Examples

See `references/rule-examples.md` for full example rules: PowerShell encoded-command detection, Office apps spawning scripting engines, and shadow-copy deletion (ransomware pre-step).

### Rule Testing

```bash
# Test rule against a sample log line
/var/ossec/bin/wazuh-logtest

# Paste a log line to see which rules fire:
# Input:
Oct 18 11:30:00 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2

# Output: Rule IDs that matched, decoded fields, alert level
```

## Custom Decoders

Decoders parse raw log lines into named fields used by rules.

```xml
<!-- Decoder for custom application log format: -->
<!-- Example log: 2024-01-15 14:30:00 AUTH FAILED user=jsmith src=192.168.1.100 -->

<decoder name="custom_auth_app">
  <prematch>^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} AUTH</prematch>
</decoder>

<decoder name="custom_auth_app_fields">
  <parent>custom_auth_app</parent>
  <regex>(\w{4}-\w{2}-\w{2} \w{2}:\w{2}:\w{2}) AUTH (\w+) user=(\w+) src=(\d+\.\d+\.\d+\.\d+)</regex>
  <order>timestamp, action, user, srcip</order>
</decoder>

<!-- Then reference in rule: -->
<rule id="100300" level="8">
  <decoded_as>custom_auth_app</decoded_as>
  <field name="action">FAILED</field>
  <description>Custom app authentication failure for $(user) from $(srcip)</description>
</rule>
```

## File Integrity Monitoring (FIM)

### FIM Configuration Best Practices

**Directories to monitor on Linux:**
```xml
<syscheck>
  <!-- Critical system binaries (hash + permissions check) -->
  <directories check_all="yes" report_changes="yes">/etc</directories>
  <directories check_all="yes">/usr/bin,/usr/sbin,/bin,/sbin</directories>
  
  <!-- Web server document root (realtime for web shells) -->
  <directories realtime="yes" check_all="yes" report_changes="yes">
    /var/www/html
  </directories>
  
  <!-- SSH keys -->
  <directories check_all="yes" report_changes="yes">/root/.ssh</directories>
  
  <!-- Cron jobs -->
  <directories check_all="yes">/etc/cron.d,/etc/cron.daily,/var/spool/cron</directories>
  
  <!-- Ignore noisy files -->
  <ignore>/etc/mtab</ignore>
  <ignore>/etc/mnttab</ignore>
  <ignore>/etc/hosts.deny</ignore>
  <ignore type="sregex">.log$|.swp$|.bak$</ignore>
</syscheck>
```

**Windows critical paths:**
```xml
<syscheck>
  <!-- System binaries -->
  <directories check_all="yes">%WINDIR%\System32</directories>
  
  <!-- Startup locations -->
  <directories realtime="yes" check_all="yes">
    %PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup
  </directories>
  
  <!-- Hosts file tampering -->
  <directories realtime="yes" check_all="yes" report_changes="yes">
    %WINDIR%\System32\drivers\etc
  </directories>
  
  <!-- Registry (Windows only) -->
  <windows_registry check_all="yes">
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
  </windows_registry>
  <windows_registry check_all="yes">
    HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services
  </windows_registry>
</syscheck>
```

## Security Configuration Assessment (SCA)

SCA checks endpoints against security benchmarks (CIS, PCI DSS, etc.) automatically.

### Built-in SCA Policies

Wazuh includes SCA policies for:
- CIS benchmarks (Windows 10, Windows Server, RHEL, Ubuntu, macOS)
- PCI DSS
- HIPAA
- GDPR

### Custom SCA Policy

```yaml
# Custom SCA policy example: /var/ossec/etc/shared/custom_sca.yml
policy:
  id: custom_policy
  file: custom_sca.yml
  name: Custom Security Policy
  description: Internal security standards
  references:
    - https://internal.corp.com/security-standards

requirements:
  title: Custom Requirements
  description: Internal security baseline

checks:
  - id: 10001
    title: "Ensure SSH root login is disabled"
    description: "Root login via SSH should be disabled"
    remediation: "Set PermitRootLogin no in /etc/ssh/sshd_config"
    compliance:
      - pci_dss: "2.2.4"
    rules:
      - 'f:/etc/sshd_config -> r:PermitRootLogin\s*no'
    condition: all

  - id: 10002
    title: "Ensure password maximum age is 90 days or less"
    compliance:
      - pci_dss: "8.3.1"
    rules:
      - 'f:/etc/login.defs -> n:PASS_MAX_DAYS\s*(\d+) compare <= 90'
    condition: all
```

## Active Response

Active response allows Wazuh to automatically execute scripts on agents when specific rules fire.

See `references/active-response.md` for the built-in active response script table, manager ossec.conf binding syntax, and a custom active response script example.

## Vulnerability Detection

Wazuh's vulnerability detection module compares installed packages against CVE databases.

### Configuration

```xml
<!-- Manager ossec.conf -->
<vulnerability-detection>
  <enabled>yes</enabled>
  <index-status>yes</index-status>
  <feed-update-interval>60m</feed-update-interval>
</vulnerability-detection>
```

**Supported OS vulnerability databases:**
- OVAL (RedHat, Debian, Ubuntu, Canonical, SUSE, Arch, Fedora)
- NVD (National Vulnerability Database) — for Windows and macOS
- MSU (Microsoft Security Updates)
- Canonical USN

### Vulnerability Alerts

Vulnerability detection generates alerts with:
- CVE ID
- CVSS score
- Package name and version
- Fixed version (if available)
- Severity (Critical/High/Medium/Low)

View in Dashboard: Vulnerability Detection > Agents overview

## Compliance Mapping

Wazuh rules include compliance tags for automated compliance reporting.

### Rule Compliance Tags

```xml
<rule id="100001" level="10">
  ...
  <group>
    authentication_failed,
    pci_dss_10.2.4,           <!-- PCI DSS requirement -->
    hipaa_164.312.b,           <!-- HIPAA requirement -->
    gdpr_IV_35.7.d,            <!-- GDPR requirement -->
    nist_800_53_AU.14,         <!-- NIST 800-53 control -->
    tsc_CC6.1,                 <!-- SOC2 TSC control -->
  </group>
</rule>
```

### Compliance Dashboards

Navigate to: Wazuh Dashboard > Compliance > select framework (PCI DSS, HIPAA, GDPR, NIST, TSC)

Each compliance dashboard shows:
- Control coverage (which controls have matching events)
- Top failing requirements (most rule triggers per control)
- Per-agent compliance posture
- Trend over time

## Reference Files

Load for deep knowledge:

- `references/architecture.md` — Wazuh manager/agent/indexer/dashboard architecture, cluster deployment, agent groups, enrollment methods, Filebeat configuration, API reference
- `references/agent-deployment.md` — Full agent install commands for Linux (RPM/APT), Windows (MSI), and macOS (PKG).
- `references/rule-examples.md` — Example custom XML rules for PowerShell encoded commands, Office macro execution, and ransomware shadow-copy deletion.
- `references/active-response.md` — Built-in active response scripts, manager configuration binding, and a custom active response script.
