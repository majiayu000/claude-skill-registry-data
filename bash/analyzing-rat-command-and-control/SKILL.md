---
name: analyzing-rat-command-and-control
description: 'Analyzes remote access trojan command-and-control by mapping the RAT command set,
  identifying the C2 transport and beacon parameters, and cataloging operator capabilities from
  static strings and config. Activates for requests to analyze RAT C2, map a trojan command
  handler, or identify remote-access capabilities and C2 transport.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - rat
  - command-and-control
  - c2
  - capability-mapping
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1219
  - T1071
  - T1105
d3fend:
  - D3-NTA
  - D3-SDA
references:
  - 'MITRE ATT&CK T1219 Remote Access Software — https://attack.mitre.org/techniques/T1219/'
  - 'MITRE ATT&CK T1071 Application Layer Protocol — https://attack.mitre.org/techniques/T1071/'
---

# Analyzing RAT Command and Control

## When to Use

- You have a RAT sample and need to map its command set (shell, file ops, screenshot, keylog,
  webcam, proxy), C2 transport, and beacon parameters.
- You are cataloging operator capabilities for detection and impact assessment.

**Do not use** this to operate the RAT or connect to its C2 — characterize capabilities from inert
static analysis.

## Prerequisites

- The RAT sample (read inertly), optionally with an extracted config.

## Safety & Handling

- Read bytes statically; defang C2 endpoints; never connect to the C2.

## Workflow

### Step 1: Map command handlers and capabilities

```bash
python scripts/analyst.py profile sample.bin
```

Matches command-keyword and API patterns for capability classes: remote shell, file transfer,
screenshot/keylog/webcam, persistence, proxy/relay, and self-update.

### Step 2: Identify the C2 transport

Detect HTTP(S), raw TCP, TLS, DNS, or messaging-platform transport from imports/strings, plus
beacon intervals/user-agents where present.

### Step 3: Build the capability matrix

Summarize capabilities and transport, mapping to ATT&CK.

### Step 4: Defang and report

Defang endpoints and produce IOCs.

## Validation

- Capabilities are grouped into classes with the matched evidence.
- The C2 transport is identified from concrete imports/strings.
- Findings map to ATT&CK T1219/T1071.

## Pitfalls

- Generic API presence (e.g., `gdi32`) misread as screenshot capability — corroborate with command
  handlers.
- Commodity RAT builders sharing strings across families — avoid over-attribution.
- Encrypted command sets requiring config decryption first.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the profiler.
- ATT&CK T1219 and T1071 (linked in frontmatter).
