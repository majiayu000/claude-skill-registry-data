---
name: analyzing-loaders-and-droppers
description: 'Analyzes loader and dropper samples by identifying staging behavior — embedded or
  downloaded next-stage payloads, decode/decrypt routines, and the execution mechanism used to run
  the next stage. Activates for requests to analyze a loader or dropper, find a staged payload, or
  map multi-stage delivery behavior.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - loader
  - dropper
  - multi-stage
  - delivery
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1105
  - T1140
  - T1574
d3fend:
  - D3-DA
  - D3-FCR
references:
  - 'MITRE ATT&CK T1105 Ingress Tool Transfer — https://attack.mitre.org/techniques/T1105/'
  - 'MITRE ATT&CK T1140 Deobfuscate/Decode Files or Information — https://attack.mitre.org/techniques/T1140/'
---

# Analyzing Loaders and Droppers

## When to Use

- You have a first-stage loader/dropper and need to find the next stage: an embedded resource, an
  appended overlay, or a download URL.
- You need to identify the decode/decrypt routine and the execution mechanism (process creation,
  injection, scheduled task, DLL side-loading).

**Do not use** this to run the loader and fetch live stages — characterize staging statically and
retrieve next stages only in an isolated sandbox.

## Prerequisites

- The loader/dropper sample (read inertly).

## Safety & Handling

- Read bytes statically; defang download URLs; never execute to pull live payloads.

## Workflow

### Step 1: Locate staged payloads

```bash
python scripts/analyst.py stage sample.bin
```

Detects embedded PE/archive signatures, an appended overlay beyond the PE's mapped size, large
high-entropy blobs, and download URLs.

### Step 2: Identify decode/execution mechanism

Scan imports/strings for decode APIs (`CryptDecrypt`, base64), download APIs (`URLDownloadToFile`,
`WinHttp`, `InternetReadFile`), and execution (`CreateProcess`, `ShellExecute`, `WinExec`,
side-loading hints).

### Step 3: Map the delivery chain

Document stage-1 → decode → stage-2 → execution and map each step to ATT&CK.

### Step 4: Defang and report

Defang URLs and produce IOCs for the staging infrastructure.

## Validation

- Embedded/overlay stages are confirmed by signature or entropy, with offsets recorded.
- Download URLs and execution mechanism are identified from imports/strings.
- The multi-stage chain maps cleanly to ATT&CK techniques.

## Pitfalls

- Treating a benign overlay (installer data, signature) as a payload without corroboration.
- Missing stages fetched at runtime when no URL is in plaintext (obfuscated/encoded).
- Confusing the decode routine for the payload itself.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the stager.
- ATT&CK T1105 and T1140 (linked in frontmatter).
