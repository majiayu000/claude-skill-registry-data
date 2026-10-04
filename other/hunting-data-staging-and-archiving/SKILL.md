---
name: hunting-data-staging-and-archiving
description: 'Hunts for pre-exfiltration data staging and archiving by detecting archive-tool
  execution (rar, 7z, zip, tar), large compressed files written to staging directories, and
  collection into a single location before transfer. Activates for requests to hunt data staging,
  detect pre-exfil archiving, or find collection and compression before exfiltration.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - data-staging
  - archiving
  - exfiltration
  - collection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1074.001
  - T1560.001
  - T1560
d3fend:
  - D3-FA
  - D3-PSA
references:
  - 'MITRE ATT&CK T1074 Data Staged — https://attack.mitre.org/techniques/T1074/'
  - 'MITRE ATT&CK T1560 Archive Collected Data — https://attack.mitre.org/techniques/T1560/'
---

# Hunting Data Staging and Archiving

## When to Use

- You have process-creation and file telemetry and want to detect an actor collecting and
  compressing data into a staging location before exfiltration.
- You are looking for the step between collection and exfil.

**Do not use** this to alert on all archive usage — backups and legitimate compression are common.
Hunt the staging context (temp paths, password-protected archives, unusual parents).

## Prerequisites

- Process-creation events (with command line) and/or file-write telemetry.

## Workflow

### Step 1: Detect archive-tool execution

```bash
python scripts/analyst.py hunt events.csv
```

Flags `rar`/`7z`/`zip`/`tar`/`winrar` execution with compression + password flags
(`a -hp`, `-p`, `-r`), and archives written to staging paths (`%TEMP%`, `%APPDATA%`,
`ProgramData`, `C:\Users\Public`).

### Step 2: Surface large/odd archives

Highlight large archive writes and archives created by unusual parents (Office, script hosts,
remote-exec services).

### Step 3: Confirm

Correlate with subsequent outbound transfer of the archive (pair with the unusual-outbound hunt).

### Step 4: Operationalize

Write a detection for password-protected archiving into staging directories.

## Validation

- Archive execution is flagged with the compression/password flags, not tool presence alone.
- Staging-path writes are surfaced with the file path.
- Findings map to ATT&CK T1074 / T1560.

## Pitfalls

- Legitimate backup/IT archiving — corroborate with path, parent, and password use.
- Built-in `tar`/`Compress-Archive` blending into normal admin activity.
- Split archives (`.r00`, `.z01`) that evade single-file size thresholds.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1074 and T1560 (linked in frontmatter).
