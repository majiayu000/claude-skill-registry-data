---
name: monitoring-process-and-file-behavior
description: 'Summarizes runtime behavior of a sample from Procmon-style operation logs — process
  and thread creation, file and registry writes, and network-related operations — to build a
  behavioral profile. Activates for requests to analyze Procmon output, summarize sample behavior,
  or profile process/file/registry activity from a sandbox run.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - dynamic-analysis
  - procmon
  - behavioral
  - sandbox
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1106
  - T1112
  - T1059
d3fend:
  - D3-PSA
  - D3-FAPA
car:
  - CAR-2013-05-002
references:
  - 'MITRE ATT&CK T1106 Native API — https://attack.mitre.org/techniques/T1106/'
  - 'Sysinternals Process Monitor — https://learn.microsoft.com/sysinternals/downloads/procmon'
---

# Monitoring Process and File Behavior

## When to Use

- You have a Procmon CSV/XML export (or equivalent sandbox operation log) from detonating a sample.
- You need a concise behavioral profile: child processes, file writes, registry persistence,
  and network-related calls.
- You are correlating dynamic behavior with static indicators.

**Do not use** this to detonate the sample yourself — it consumes already-captured logs. Run the
sample only inside an isolated, instrumented sandbox you own.

## Prerequisites

- A Procmon CSV export (or comparable operation log) from an isolated detonation.

## Safety & Handling

- Only consume logs; never execute the sample on an analyst workstation.
- Defang any captured URLs/hosts before sharing.

## Workflow

### Step 1: Summarize operations by category

```bash
python scripts/analyst.py summarize procmon.csv
```

Counts operations by class (Process/Thread, File, Registry, Network) and lists the busiest paths.

### Step 2: Identify process tree

Extract `Process Create` events to reconstruct parent/child relationships and command lines —
LOLBins (`powershell`, `rundll32`, `mshta`) spawned from the sample are high-signal.

### Step 3: Identify persistence and drops

Registry writes under `Run`/`RunOnce`/services, and file writes to `%APPDATA%`/`%TEMP%`/startup,
indicate persistence and staged payloads.

### Step 4: Build the behavioral profile

Map observed operations to ATT&CK techniques and defang any network endpoints.

## Validation

- The process tree reconstructs from `Process Create` events.
- File and registry writes are categorized with their target paths.
- Observed behaviors map to specific ATT&CK techniques.

## Pitfalls

- Treating noisy read operations as significant — writes and creates carry the signal.
- Missing short-lived child processes that exited before capture stopped.
- Ignoring path normalization (`%TEMP%` vs absolute) when deduplicating.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the summarizer.
- ATT&CK T1106 and Process Monitor docs (linked in frontmatter).
