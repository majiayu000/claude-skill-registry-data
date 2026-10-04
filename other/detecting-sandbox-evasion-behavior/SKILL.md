---
name: detecting-sandbox-evasion-behavior
description: 'Detects sandbox and analysis evasion techniques in a sample by scanning static
  strings, imports, and API traces for VM artifact checks, timing/sleep stalls, anti-debug calls,
  and environment fingerprinting. Activates for requests to detect sandbox evasion, find anti-VM
  or anti-debug checks, or explain why a sample did not detonate.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - evasion
  - anti-vm
  - anti-debug
  - sandbox
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1497
  - T1497.001
  - T1622
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'MITRE ATT&CK T1497 Virtualization/Sandbox Evasion — https://attack.mitre.org/techniques/T1497/'
  - 'MITRE ATT&CK T1622 Debugger Evasion — https://attack.mitre.org/techniques/T1622/'
---

# Detecting Sandbox Evasion Behavior

## When to Use

- A sample ran inertly in a sandbox and you suspect evasion.
- You want to enumerate anti-VM, anti-debug, timing, and environment-fingerprinting checks from
  static strings/imports and/or an API trace.

**Do not use** this to conclude a sample is benign — evasion is itself a malicious signal, and
absence of detected checks does not prove there are none.

## Prerequisites

- The sample (read inertly) and optionally a JSON API trace.

## Safety & Handling

- Read bytes statically; never execute the sample to "see if it evades."

## Workflow

### Step 1: Scan for evasion indicators

```bash
python scripts/analyst.py scan sample.bin
```

Searches for VM/sandbox artifact strings (`VMware`, `VBOX`, `vmtoolsd`, `sbiedll`, common
sandbox usernames/hostnames), anti-debug APIs (`IsDebuggerPresent`, `CheckRemoteDebuggerPresent`,
`NtQueryInformationProcess`), timing stalls (`Sleep`, `GetTickCount`, `rdtsc`), and CPUID checks.

### Step 2: Categorize techniques

Group hits into anti-VM, anti-debug, anti-sandbox, and timing/stalling categories.

### Step 3: Recommend bypass and report

Suggest analysis adjustments (patch sleeps, hardened VM, hooking) and map findings to ATT&CK.

## Validation

- Detected indicators are grouped by evasion category.
- Findings distinguish static-string evidence from API-trace evidence when both are provided.
- Each category maps to an ATT&CK technique/subtechnique.

## Pitfalls

- False positives from benign software that also queries the environment — corroborate.
- Strings can be obfuscated; absence of plaintext artifacts is not absence of evasion.
- Confusing a hung sample with deliberate stalling without timing evidence.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the scanner.
- ATT&CK T1497 and T1622 (linked in frontmatter).
