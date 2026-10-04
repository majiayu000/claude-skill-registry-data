---
name: hunting-cobalt-strike-traffic
description: 'Hunts for Cobalt Strike beacon traffic by detecting default stager URI checksum8
  values, default Malleable C2 profile artifacts, and default ports/named pipes in HTTP and process
  telemetry. Activates for requests to hunt Cobalt Strike, detect beacon stager URIs, or find
  default Malleable C2 indicators.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - cobalt-strike
  - c2
  - beacon
  - network-detection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071.001
  - T1573
  - T1090
d3fend:
  - D3-NTA
  - D3-NTPM
references:
  - 'MITRE ATT&CK Software S0154 Cobalt Strike — https://attack.mitre.org/software/S0154/'
  - 'Cobalt Strike checksum8 stager URI behavior (public research) — https://attack.mitre.org/techniques/T1071/001/'
---

# Hunting Cobalt Strike Traffic

## When to Use

- You have HTTP request logs (proxy/Zeek http.log) and/or process telemetry and want to detect
  default-configuration Cobalt Strike beacons.
- You are triaging suspected C2 using known default artifacts before deeper analysis.

**Do not use** default-indicator detection as proof — operators customize Malleable C2 profiles.
Absence of defaults does not mean no Cobalt Strike. This skill parses telemetry and executes nothing.

## Prerequisites

- HTTP request URIs and/or process/pipe telemetry.

## Workflow

### Step 1: Detect default stager URIs

```bash
python scripts/analyst.py hunt http.csv
```

Flags request URIs whose path matches the Cobalt Strike default stager checksum8 algorithm (sum of
the path characters mod 256 equals 92 for x86 or 93 for x64 stagers).

### Step 2: Match default profile artifacts

Flag default user-agents, default URIs (`/__utm.gif`, `/submit.php`, `/pixel`), and default named
pipes (`\\.\pipe\msagent_*`, `\\.\pipe\status_*`) when present in telemetry.

### Step 3: Confirm

Corroborate with beaconing periodicity and destination reputation; pivot to memory/config analysis.

### Step 4: Operationalize

Write detections for checksum8 URIs and known default artifacts, accepting they catch defaults only.

## Validation

- checksum8 detection correctly computes the path-character sum mod 256.
- Default profile artifacts are matched exactly, not by loose substrings.
- Findings are presented as default-indicator hits, not definitive attribution.

## Pitfalls

- Customized Malleable C2 profiles defeating all default-artifact checks.
- checksum8 false positives on unrelated short URIs — corroborate with other signals.
- Treating a single default hit as confirmation without behavioral corroboration.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK S0154 Cobalt Strike (linked in frontmatter).
