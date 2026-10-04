---
name: hunting-lateral-movement-over-smb-and-wmi
description: 'Hunts for lateral movement via remote service creation, admin share writes, and
  remote WMI process creation by correlating Windows logon, service install, and process-creation
  events. Activates for requests to hunt lateral movement, detect PsExec/WMIexec activity, or find
  remote execution over SMB and WMI.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - lateral-movement
  - smb
  - wmi
  - remote-execution
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1021.002
  - T1021.003
  - T1570
d3fend:
  - D3-NTA
  - D3-PSA
car:
  - CAR-2014-11-007
references:
  - 'MITRE ATT&CK T1021.002 SMB/Windows Admin Shares — https://attack.mitre.org/techniques/T1021/002/'
  - 'Windows Security Event 4624/4697 — https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4624'
---

# Hunting Lateral Movement Over SMB and WMI

## When to Use

- You have Windows logon (4624), service install (7045/4697), and process-creation telemetry and
  want to detect remote execution tools (PsExec, WMIexec, SMBexec) moving between hosts.
- You are reconstructing an attacker's east-west movement.

**Do not use** this to alert on all Type 3 logons — network logons are normal. Hunt the
service-creation, admin-share, and remote-WMI patterns that accompany them.

## Prerequisites

- Logon (4624 Type 3), service install (7045/4697), and process-creation events.

## Workflow

### Step 1: Correlate remote-execution indicators

```bash
python scripts/analyst.py hunt events.csv
```

Flags PsExec-style service installs (`PSEXESVC`, randomly named services running from `ADMIN$`),
remote WMI parents (`wmiprvse.exe` spawning `cmd`/`powershell`), and named-pipe service binaries.

### Step 2: Build a movement graph

Group by source account and target host to see fan-out across systems.

### Step 3: Confirm

Distinguish admin tooling from intrusion by account, timing, and target breadth.

### Step 4: Operationalize

Write Sigma rules for PsExec service creation and `wmiprvse.exe` child shells.

## Validation

- Remote service installs are flagged by image path/name patterns, not service installs broadly.
- `wmiprvse.exe`-parented shells are correlated with the originating account where possible.
- Findings map to ATT&CK T1021.002/.003.

## Pitfalls

- Legitimate admin/management software using PsExec or remote WMI.
- Renamed PsExec service binaries evading name checks.
- Missing the logon-to-execution correlation across separate event sources.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1021.002 and Event 4624/4697 docs (linked in frontmatter).
