---
name: performing-dynamic-analysis-in-a-sandbox
description: 'Runs a sample in an instrumented sandbox to observe behavior: process tree, file
  and registry changes, network activity, and persistence, then summarizes the behavioral
  report into capabilities and IOCs. Activates for requests to detonate a sample, do dynamic
  or behavioral analysis, or interpret sandbox output.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - dynamic-analysis
  - sandbox
  - behavioral
  - procmon
  - detonation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1055
  - T1071
  - T1547
  - T1497
d3fend:
  - D3-DA
  - D3-PSA
references:
  - 'CAPE Sandbox — https://github.com/kevoreilly/CAPEv2'
  - 'Sysinternals Process Monitor — https://learn.microsoft.com/sysinternals/downloads/procmon'
---

# Performing Dynamic Analysis in a Sandbox

## When to Use

- Static analysis is blocked by packing/obfuscation and you need to observe runtime behavior.
- You want a behavioral picture: spawned processes, dropped files, registry edits, and C2.
- You are confirming capabilities hypothesized from static analysis.

**Do not use** dynamic analysis as the only method — evasive samples may sleep, detect the
sandbox, or require arguments. Pair it with static/RE work.

## Prerequisites

- An isolated lab with a victim VM and simulated internet (see the lab-setup skill).
- A sandbox stack (CAPE/Cuckoo) or manual instrumentation: Process Monitor, Process Explorer,
  Regshot, and a packet capture on the services guest.
- A clean base snapshot to revert to.

## Safety & Handling

- Detonate only inside the isolated victim VM; revert the snapshot after each run.
- Route all network through the simulated-internet guest; never allow live egress.
- Defang any captured URLs/IPs before they leave the lab.

## Workflow

### Step 1: Prepare instrumentation

Start Process Monitor (filtered to the target), Regshot baseline, and packet capture on the
services guest. Snapshot the victim as clean.

### Step 2: Detonate with the right context

Many samples need a parent (Office, rundll32), an export (`rundll32 dll,Export`), or arguments.
Match the original delivery context or the sample stalls.

### Step 3: Observe for the full behavior window

Watch process creation, file drops, registry Run keys/services, scheduled tasks, and network
beacons. Give it several minutes; some samples sleep first.

### Step 4: Summarize the report

Feed the sandbox JSON (or your collected logs) to the summarizer to group events into
capabilities and IOCs:

```bash
python scripts/analyst.py summarize report.json
```

### Step 5: Diff the system state

Compare Regshot/file baselines pre- and post-run to capture persistence and dropped artifacts.

## Validation

- The observed process tree and network match the static-analysis hypothesis.
- Persistence mechanisms found dynamically are confirmed in registry/task artifacts.
- Re-running from the clean snapshot reproduces the core behavior.

## Pitfalls

- Detonating without the required parent/args, so the sample exits early ("sandbox evasion"
  that is really a context problem).
- Too-short observation windows that miss sleeping or staged payloads.
- Trusting a single sandbox verdict; tune and corroborate.
- Allowing real network egress and contaminating live infrastructure.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the report summarizer.
- CAPE Sandbox and Process Monitor (linked in frontmatter).
