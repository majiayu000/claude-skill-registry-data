---
name: detecting-process-injection-in-memory
description: 'Detects process injection in a memory image by identifying private executable regions
  with no file backing, RWX protections, and modified entry points using Volatility 3 malfind-style
  analysis. Activates for requests to detect process injection, find injected code in memory, or
  triage suspicious executable regions in a memory image.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - memory-forensics
  - process-injection
  - volatility
  - malfind
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1055
  - T1055.001
  - T1055.012
d3fend:
  - D3-PSA
  - D3-SDA
car:
  - CAR-2014-04-003
references:
  - 'MITRE ATT&CK T1055 Process Injection — https://attack.mitre.org/techniques/T1055/'
  - 'Volatility 3 windows.malfind — https://volatility3.readthedocs.io/'
---

# Detecting Process Injection in Memory

## When to Use

- You have a Windows memory image and want to find injected/hollowed code.
- You are triaging private RWX regions, unbacked executable memory, and PE headers in private
  allocations (classic injection/hollowing signs).

**Do not use** this on a live production host without authorization — work from an acquired image.
This skill interprets analysis output; run Volatility separately on the image.

## Prerequisites

- A memory image and Volatility 3 (`windows.malfind`, `windows.vadinfo`) installed.

## Safety & Handling

- Treat carved injected regions as live malicious code; store them password-protected.

## Workflow

### Step 1: Run malfind and capture output

```bash
vol -f memory.raw windows.malfind > malfind.txt
```

### Step 2: Score injection candidates

```bash
python scripts/analyst.py score malfind.txt
```

Flags regions with `PAGE_EXECUTE_READWRITE`, MZ/PE headers in private memory, and shellcode-like
disassembly hints, ranking processes by suspicion.

### Step 3: Corroborate

Cross-check flagged PIDs with `windows.vadinfo` (private, executable, no mapped file) and the
process tree for anomalous parents.

### Step 4: Carve and route

Carve the injected region for follow-on shellcode/PE recovery and analysis.

## Validation

- Flagged regions are private + executable, not legitimate mapped images.
- PE-in-private-memory findings are confirmed by an MZ/`This program` signature.
- High-scoring PIDs corroborate with VAD protections and process-tree anomalies.

## Pitfalls

- JIT engines (.NET, Java, browsers) legitimately create RWX regions — corroborate before alerting.
- Relying on malfind alone; pair with vadinfo and ldrmodules.
- Missing hollowing where the region is RX (not RWX) after protection change.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the scorer.
- ATT&CK T1055 and Volatility 3 docs (linked in frontmatter).
