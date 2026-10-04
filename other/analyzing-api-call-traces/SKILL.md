---
name: analyzing-api-call-traces
description: 'Analyzes API call traces from a sandbox or API monitor (JSON) to group calls by
  category, reconstruct high-level behaviors (process injection, file drops, network, crypto), and
  flag suspicious call sequences. Activates for requests to analyze an API trace, interpret sandbox
  API logs, or identify behavior from Win32/Native API calls.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - dynamic-analysis
  - api-trace
  - winapi
  - sandbox
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1106
  - T1055
  - T1027
d3fend:
  - D3-PSA
  - D3-SDA
references:
  - 'MITRE ATT&CK T1106 Native API — https://attack.mitre.org/techniques/T1106/'
  - 'Windows API Index — https://learn.microsoft.com/windows/win32/apiindex/windows-api-list'
---

# Analyzing API Call Traces

## When to Use

- You have a JSON API trace (CAPE/Cuckoo "apistats"/calls, API Monitor export) from a detonation.
- You need to translate raw API calls into high-level behaviors and flag suspicious sequences
  (e.g., `VirtualAllocEx` → `WriteProcessMemory` → `CreateRemoteThread`).

**Do not use** this as a substitute for detonation — it consumes an existing trace produced in an
isolated sandbox.

## Prerequisites

- A JSON API trace with at least an API name per call (and optionally arguments).

## Safety & Handling

- Consume traces only; never execute the sample to generate one outside a sandbox.

## Workflow

### Step 1: Group calls by category

```bash
python scripts/analyst.py classify trace.json
```

Buckets calls into process, memory, file, registry, network, crypto, and synchronization.

### Step 2: Detect behavior signatures

Matches ordered API sequences that indicate techniques — remote injection, hollowing,
self-deletion, dynamic API resolution (`LoadLibrary`/`GetProcAddress` bursts).

### Step 3: Prioritize and report

Rank detected behaviors by severity and map each to ATT&CK.

## Validation

- Each API call is categorized; unknown APIs are reported, not dropped silently.
- Injection-style sequences are detected only when the ordered prerequisites are present.
- Detected behaviors map to ATT&CK techniques.

## Pitfalls

- Flagging individual benign APIs out of context — the sequence matters.
- Assuming call order in the JSON equals execution order without a timestamp/index.
- Ignoring failed calls (non-zero error) that never actually executed the behavior.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the classifier.
- ATT&CK T1106 and the Windows API Index (linked in frontmatter).
