---
name: hunting-ransomware-precursor-behavior
description: 'Hunts for ransomware precursor behavior that precedes encryption — shadow-copy and
  backup deletion, recovery disabling, security-tool tampering, and mass file modification — so the
  attack can be stopped before payload detonation. Activates for requests to hunt ransomware
  precursors, detect shadow-copy deletion, or find pre-encryption recovery sabotage.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - ransomware
  - shadow-copy
  - impact
  - early-warning
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1490
  - T1489
  - T1486
d3fend:
  - D3-PSA
  - D3-FA
car:
  - CAR-2016-04-002
references:
  - 'MITRE ATT&CK T1490 Inhibit System Recovery — https://attack.mitre.org/techniques/T1490/'
  - 'MITRE ATT&CK T1486 Data Encrypted for Impact — https://attack.mitre.org/techniques/T1486/'
---

# Hunting Ransomware Precursor Behavior

## When to Use

- You have endpoint process/command telemetry and want to catch the steps ransomware takes
  *before* encrypting — deleting shadow copies, disabling recovery, killing security tools, and
  stopping backup/database services.
- You want early warning to intervene before payload detonation.

**Do not use** this as a substitute for blocking the encryption itself — it is an early-warning
hunt for the preparation phase, not a recovery procedure.

## Prerequisites

- Process-creation telemetry (with command line) and optionally service/file telemetry.

## Workflow

### Step 1: Hunt recovery-inhibition commands

```bash
python scripts/analyst.py hunt events.csv
```

Flags `vssadmin delete shadows`, `wmic shadowcopy delete`, `wbadmin delete catalog`,
`bcdedit /set recoveryenabled no` / `bootstatuspolicy ignoreallfailures`, and `wevtutil cl`.

### Step 2: Detect defense and service tampering

Surface stopping/killing of AV/EDR and backup/DB services (`net stop`, `taskkill`,
`sc stop`) targeting `veeam`, `sql`, `backup`, `sophos`, `defender`, etc.

### Step 3: Correlate and prioritize

A host showing recovery-inhibition + service-stop in a short window is a high-priority
pre-encryption signal — escalate immediately.

### Step 4: Operationalize

Write a high-severity detection for shadow-copy deletion and recovery disabling.

## Validation

- Recovery-inhibition commands are detected with their specific syntax.
- Security/backup service tampering is identified by target service names.
- Findings map to ATT&CK T1490 / T1489 (and precede T1486).

## Pitfalls

- Admins occasionally delete shadow copies legitimately — corroborate with co-occurring tampering.
- LOLBin variants (`wmic`, PowerShell `Get-WmiObject Win32_ShadowCopy | Remove`) evading
  `vssadmin`-only rules.
- Fast attacks where precursor and encryption are near-simultaneous — alert must be real-time.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1490 and T1486 (linked in frontmatter).
