---
name: hunting-lolbin-abuse-on-windows
description: 'Hunts for living-off-the-land binary (LOLBin) abuse in Windows process-creation
  telemetry by flagging trusted system binaries used with download, execution-proxy, or
  encoded-command arguments. Activates for requests to hunt LOLBins, detect signed-binary proxy
  execution, or find suspicious certutil/mshta/regsvr32 usage.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - lolbin
  - process-creation
  - defense-evasion
  - sysmon
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1218
  - T1105
  - T1059
d3fend:
  - D3-PSA
  - D3-PA
car:
  - CAR-2021-01-009
references:
  - 'MITRE ATT&CK T1218 System Binary Proxy Execution — https://attack.mitre.org/techniques/T1218/'
  - 'LOLBAS project — https://lolbas-project.github.io/'
---

# Hunting LOLBin Abuse on Windows

## When to Use

- You have process-creation telemetry (Sysmon Event ID 1 or EDR process events as CSV/JSON) and
  want to surface trusted binaries used for malicious proxy execution or download.
- You are building a detection from known LOLBin argument patterns.

**Do not use** this as a blocklist of the binaries themselves — they are legitimate. Hunt on the
suspicious argument/parent context, not mere presence.

## Prerequisites

- Process-creation events with image path, command line, and (ideally) parent image.

## Workflow

### Step 1: Score LOLBin invocations

```bash
python scripts/analyst.py hunt events.csv
```

Flags known LOLBins (`certutil`, `mshta`, `regsvr32`, `rundll32`, `bitsadmin`, `msiexec`,
`installutil`, `wmic`) paired with suspicious arguments (`-urlcache`, `http`, `javascript:`,
`scrobj`, `-decode`, `DownloadString`).

### Step 2: Add context

Weight by anomalous parent (Office, browser, script host) and unusual execution path.

### Step 3: Triage and confirm

Investigate the top-scoring events; confirm whether the download/proxy behavior is legitimate
administration or malicious.

### Step 4: Operationalize

Convert confirmed patterns into a Sigma rule for ongoing detection.

## Validation

- Flags require a suspicious argument/parent, not just the binary name.
- Known-benign administrative patterns are distinguishable from abuse in the output.
- Each flagged technique maps to an ATT&CK ID (T1218.x / T1105).

## Pitfalls

- Alerting on `rundll32`/`regsvr32` presence alone — extremely noisy.
- Missing renamed LOLBins (hash/signature checks help, name checks do not).
- Encoded-command obfuscation hiding the true argument intent.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1218 and the LOLBAS project (linked in frontmatter).
