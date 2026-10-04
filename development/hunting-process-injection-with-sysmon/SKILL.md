---
name: hunting-process-injection-with-sysmon
description: 'Hunts for process injection using Sysmon telemetry: correlating CreateRemoteThread
  (EID 8), suspicious cross-process access (EID 10), and RWX image-less memory to surface
  hollowing, shellcode injection, and APC abuse. Activates for requests to hunt process
  injection, analyze Sysmon EID 8/10, or detect code injection on Windows.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - process-injection
  - sysmon
  - windows
  - edr
  - detection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1055
  - T1055.001
  - T1055.012
d3fend:
  - D3-PSA
  - D3-PCSV
car:
  - CAR-2019-04-001
references:
  - 'Sysmon documentation — https://learn.microsoft.com/sysinternals/downloads/sysmon'
  - 'MITRE ATT&CK T1055 Process Injection — https://attack.mitre.org/techniques/T1055/'
---

# Hunting Process Injection with Sysmon

## When to Use

- You have Sysmon (or equivalent EDR) telemetry and want to hunt code injection across hosts.
- You are testing a hypothesis that an implant injects into benign processes
  (`explorer.exe`, `svchost.exe`) to evade defenses.
- You need to triage EID 8/10 events into a prioritized list of injection candidates.

**Do not use** EID 8/10 in isolation as a verdict — legitimate software (security tools,
debuggers, injectors in dev tools) generates these; correlation and baselining are required.

## Prerequisites

- Sysmon configured to log Event ID 8 (CreateRemoteThread) and 10 (ProcessAccess) with useful
  access masks; a SIEM or log export to query.
- A baseline of normal cross-process access for your environment.

## Workflow

### Step 1: Pull the candidate events

Collect EID 8 (remote thread creation) and EID 10 (process access) with high-power access
masks (e.g., `0x1F0FFF`, `PROCESS_VM_WRITE | PROCESS_CREATE_THREAD`).

### Step 2: Filter known-good

Remove baseline noise: security agents, legitimate debuggers, and known injector pairs. Keep
unusual source→target pairs (e.g., a document app injecting into a browser).

```bash
python scripts/analyst.py triage sysmon.json
```

### Step 3: Correlate signals

Raise priority when multiple indicators stack: cross-process write + remote thread into the
same target, target with RWX private memory, or source process spawned from a macro/script.

### Step 4: Pivot per candidate

For top candidates, pull the source process tree, image path, signing status, and network
connections to confirm or clear.

### Step 5: Confirm and respond

Validate suspected hollowing/shellcode (memory analysis), then escalate confirmed injections
to IR and convert the logic into a detection rule.

## Validation

- Surfaced candidates show a coherent injection pattern (access + remote thread to same PID),
  not isolated single events.
- Known-good injectors are filtered, keeping the candidate list small and reviewable.
- Confirmed cases are corroborated by process lineage or memory evidence.

## Pitfalls

- Alerting on every EID 10 — the access mask matters; filter to write/inject rights.
- Ignoring source lineage; a script-spawned source is far more suspicious.
- No baseline, so security tooling buries real injection in noise.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the Sysmon triage helper.
- Sysmon docs and ATT&CK T1055 (linked in frontmatter).
