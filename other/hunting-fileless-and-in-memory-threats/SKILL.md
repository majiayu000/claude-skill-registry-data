---
name: hunting-fileless-and-in-memory-threats
description: 'Hunts for fileless and in-memory threats by correlating PowerShell script-block logs,
  encoded-command usage, in-memory loading patterns, and registry-resident payloads from Windows
  telemetry. Activates for requests to hunt fileless malware, detect in-memory execution, or find
  registry-resident and reflective-loading activity.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - fileless
  - in-memory
  - powershell
  - defense-evasion
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059.001
  - T1620
  - T1112
d3fend:
  - D3-PSA
  - D3-SDA
car:
  - CAR-2014-04-003
references:
  - 'MITRE ATT&CK T1620 Reflective Code Loading — https://attack.mitre.org/techniques/T1620/'
  - 'PowerShell Script Block Logging (4104) — https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_logging_windows'
---

# Hunting Fileless and In-Memory Threats

## When to Use

- You have PowerShell script-block logs (4104), process telemetry, and registry-write events and
  want to detect fileless execution that leaves little on disk.
- You are hunting reflective loading, in-memory .NET execution, and registry-resident payloads.

**Do not use** this to alert on all PowerShell use — hunt the in-memory loading and encoded-payload
patterns specifically.

## Prerequisites

- 4104 script-block logs and/or process and registry telemetry (CSV/JSON).

## Workflow

### Step 1: Hunt in-memory loading patterns

```bash
python scripts/analyst.py hunt events.csv
```

Flags `[Reflection.Assembly]::Load`, `VirtualAlloc`/`WriteProcessMemory` via PowerShell,
`Invoke-Expression` of decoded blobs, `DownloadString`+`IEX`, and large base64 in script blocks.

### Step 2: Detect registry-resident payloads

Surface writes of large encoded blobs to `HKCU\Software\...` Run-adjacent or custom keys (fileless
storage).

### Step 3: Confirm

Correlate script-block content with the parent process and subsequent network/child activity.

### Step 4: Operationalize

Write detections for reflective loading and base64-heavy script blocks.

## Validation

- Flags are based on in-memory loading/encoded-payload patterns, not PowerShell presence.
- Registry-resident payload detection keys on large encoded values.
- Findings map to ATT&CK T1620/T1059.001/T1112.

## Pitfalls

- Legitimate admin scripts using `Invoke-Expression` — corroborate with content/parent.
- Obfuscated script blocks splitting indicators across logs.
- Constrained Language Mode evasions changing the observable API surface.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1620 and script-block logging docs (linked in frontmatter).
