---
name: identifying-anti-debugging-techniques
description: 'Identifies and bypasses anti-debugging and anti-analysis checks in malware: PEB
  flags, debugger-detection APIs, timing checks, and exception tricks, then neutralizes them
  to continue analysis. Activates for requests to identify anti-debugging, bypass anti-debug
  checks, or analyze evasion that blocks a debugger.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - anti-debugging
  - evasion
  - peb
  - debugging
  - windows
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1622
  - T1497.001
  - T1027
d3fend:
  - D3-PSA
  - D3-FCR
references:
  - 'Microsoft debugging APIs (IsDebuggerPresent, CheckRemoteDebuggerPresent) — https://learn.microsoft.com/windows/win32/api/debugapi/'
  - 'PEB structure (BeingDebugged, NtGlobalFlag) — https://learn.microsoft.com/windows-hardware/drivers/'
---

# Identifying Anti-Debugging Techniques

## When to Use

- A sample behaves differently (or exits) under a debugger and you need to find the checks.
- You are stuck at a point where execution diverges when analysis tooling is present.
- You want to neutralize anti-debug logic to continue dynamic analysis.

**Do not use** brute removal of every check — some are tied to control flow or decryption keys;
faking the expected result is usually safer than deleting the check.

## Prerequisites

- x64dbg (with anti-debug plugins like ScyllaHide) inside the victim VM.
- A disassembler to locate checks statically.
- Familiarity with the Windows PEB and debug APIs.

## Workflow

### Step 1: Enumerate likely checks statically

Scan imports and code for common anti-debug primitives:

```bash
python scripts/analyst.py scan sample.bin
```

```text
API-based   : IsDebuggerPresent, CheckRemoteDebuggerPresent, NtQueryInformationProcess
PEB-based   : BeingDebugged (PEB+0x2), NtGlobalFlag (PEB+0xBC/0x68)
Timing      : rdtsc, GetTickCount/QueryPerformanceCounter deltas around code
Exceptions  : INT3/INT2D, SetUnhandledExceptionFilter, single-step traps
Self-checks : CRC of own code, breakpoint (0xCC) scanning
```

### Step 2: Confirm at runtime

Set breakpoints on the detection APIs and observe how the result is used (a conditional jump
that leads to exit vs. real code).

### Step 3: Neutralize

Prefer faking results over deletion: force `IsDebuggerPresent` to return 0, clear the PEB
`BeingDebugged` flag, or use ScyllaHide to hook the common checks automatically. For timing,
patch the comparison or reduce measured deltas.

### Step 4: Re-run and continue

With checks neutralized, proceed to unpacking/behavior analysis. Re-scan in case later stages
add more checks.

## Validation

- After neutralization, execution follows the same path as on a non-debugged run.
- Faked check results do not break decryption or control flow (no corrupted code paths).
- The sample reaches and reveals its real behavior.

## Pitfalls

- Patching a check that feeds a decryption key, corrupting later code. Understand the use
  before editing.
- Missing PEB-direct checks because you only looked at imported APIs.
- Stopping after one check; samples chain several across stages.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the anti-debug scanner.
- Microsoft debug APIs and PEB documentation (linked in frontmatter).
