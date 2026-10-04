---
name: hunting-credential-dumping-activity
description: 'Hunts for credential dumping by detecting LSASS process access with suspicious access
  masks, known dumping tool signatures, and comsvcs.exe MiniDump abuse in Sysmon Event ID 10 and
  process-creation telemetry. Activates for requests to hunt credential dumping, detect LSASS
  access, or find Mimikatz/comsvcs MiniDump activity.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - credential-access
  - lsass
  - sysmon
  - mimikatz
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1003.001
  - T1003
  - T1003.002
d3fend:
  - D3-PSA
  - D3-PAN
car:
  - CAR-2019-04-004
references:
  - 'MITRE ATT&CK T1003.001 LSASS Memory — https://attack.mitre.org/techniques/T1003/001/'
  - 'Sysmon Event ID 10 ProcessAccess — https://learn.microsoft.com/sysinternals/downloads/sysmon'
---

# Hunting Credential Dumping Activity

## When to Use

- You have Sysmon ProcessAccess (Event ID 10) and/or process-creation telemetry and want to detect
  attempts to read LSASS memory or dump credentials.
- You are investigating post-exploitation credential theft.

**Do not use** this to dump credentials yourself — it analyzes telemetry of such activity. Legit
security tools also touch LSASS; corroborate before alerting.

## Prerequisites

- Sysmon EID 10 events (with TargetImage, GrantedAccess, SourceImage) and/or EID 1 process events.

## Workflow

### Step 1: Hunt LSASS access and dumping patterns

```bash
python scripts/analyst.py hunt events.csv
```

Flags EID 10 events where `TargetImage` is `lsass.exe` with high-risk `GrantedAccess` masks
(`0x1010`, `0x1410`, `0x143a`, `0x1438`), and process events showing `comsvcs.dll,MiniDump`,
`procdump ... lsass`, `rundll32 ... MiniDump`, or known tool names.

### Step 2: Reduce false positives

De-prioritize known security agents (EDR, AV) as the `SourceImage`; weight unsigned or unusual
source processes.

### Step 3: Confirm

Correlate with file writes of `.dmp` files and subsequent off-host transfer.

### Step 4: Operationalize

Write a Sigma rule for LSASS access masks and comsvcs MiniDump.

## Validation

- LSASS access flags are based on access mask, not mere access by trusted tools.
- comsvcs/procdump/rundll32 MiniDump patterns are detected from command lines.
- Findings map to ATT&CK T1003.001/.002.

## Pitfalls

- Many legitimate tools open LSASS — access mask + source-image context is essential.
- Attackers renaming tools; rely on behavior (mask, MiniDump export) not just names.
- Direct-syscall dumpers that avoid the usual API and reduce telemetry.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1003.001 and Sysmon EID 10 (linked in frontmatter).
