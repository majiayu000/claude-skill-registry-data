---
name: bypassing-anti-vm-and-sandbox-checks
description: 'Bypasses anti-VM and sandbox checks during analysis by locating the specific detection
  routines (artifact strings, timing, CPUID/hypervisor bit) and planning patches or environment
  hardening so the sample detonates. Activates for requests to bypass anti-VM checks, defeat sandbox
  detection, or make an evasive sample run for analysis.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - anti-vm
  - evasion
  - patching
  - sandbox
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1497
  - T1497.001
  - T1497.003
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'MITRE ATT&CK T1497 Virtualization/Sandbox Evasion — https://attack.mitre.org/techniques/T1497/'
  - 'Intel SDM CPUID hypervisor-present bit — https://www.intel.com/sdm'
---

# Bypassing Anti-VM and Sandbox Checks

## When to Use

- An evasive sample refuses to detonate under analysis and you need to locate and neutralize its
  anti-VM/sandbox checks (artifact strings, timing stalls, CPUID hypervisor bit, MAC/registry
  checks).
- You are planning patches or environment hardening to force execution.

**Do not use** patching as a shortcut that changes malicious logic — patch only the evasion gate.
Run only in an isolated, instrumented VM with snapshots.

## Prerequisites

- The sample and a debugger/disassembler on an isolated VM.

## Safety & Handling

- The sample executes during bypass work; use a disposable, snapshotted, network-controlled VM.

## Workflow

### Step 1: Locate the evasion checks

```bash
python scripts/analyst.py locate sample.bin
```

Reports offsets of anti-VM artifact strings, timing APIs (`GetTickCount`, `rdtsc`), CPUID usage,
and environment-fingerprint APIs to point you at the detection routines.

### Step 2: Plan the bypass

For each check decide the approach: patch the conditional jump after the check, hook/stub the API
to return benign values, or harden the VM (rename adapters, patch registry, add fake processes).

### Step 3: Apply and verify

Patch the gate (e.g., force the "not detected" branch) and confirm the sample proceeds past the
check.

### Step 4: Document

Record each check, its offset, and the bypass applied for reproducibility.

## Validation

- Each located check maps to a real detection primitive (string/timing/CPUID/API).
- The patched/hooked gate provably lets execution continue.
- Only the evasion gate is altered, not the payload logic.

## Pitfalls

- Multiple layered checks — bypassing one is not enough.
- Timing checks needing instruction-accurate handling (`rdtsc` deltas).
- Anti-tamper detecting the patch; prefer hooking returns over byte patches when fragile.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the locator.
- ATT&CK T1497 and the CPUID hypervisor bit reference (linked in frontmatter).
