---
name: analyzing-position-independent-code
description: 'Analyzes position-independent code and shellcode by identifying GetPC/PEB-walk
  techniques, API-hash resolution loops, and relocation-free addressing so the payload can be
  disassembled at the right base. Activates for requests to analyze position-independent code,
  identify PIC techniques, or understand how shellcode resolves APIs without imports.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - position-independent-code
  - shellcode
  - peb-walk
  - api-hashing
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1027.007
  - T1620
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'PEB / LDR structures (Windows internals) — https://learn.microsoft.com/windows/win32/api/winternl/'
  - 'MITRE ATT&CK T1027.007 Dynamic API Resolution — https://attack.mitre.org/techniques/T1027/007/'
---

# Analyzing Position-Independent Code

## When to Use

- You have a PIC blob/shellcode that resolves its own addresses and APIs without imports, and you
  need to understand its technique before disassembly.
- You want to identify the base-resolution (GetPC), PEB-walk, and API-hashing mechanics.

**Do not use** this to execute the code — analyze it statically (and emulate separately if needed).
Treat the blob as malicious.

## Prerequisites

- The PIC/shellcode blob (read inertly).

## Safety & Handling

- Read bytes statically; store the blob password-protected and never execute it.

## Workflow

### Step 1: Identify PIC techniques

```bash
python scripts/analyst.py analyze shellcode.bin
```

Detects GetPC stubs (`call $+5`/`fnstenv`), PEB access (`fs:[30]`/`gs:[60]`), API-hash loops
(`lodsb` + `ror`), and stack-string construction.

### Step 2: Determine architecture and base behavior

Confirm 32- vs 64-bit PEB access and how the code computes its own base for relative addressing.

### Step 3: Map API resolution

Note the hashing algorithm and that resolved APIs are obtained by walking the PEB→LDR→export tables
(pair with the API-hash resolver skill).

### Step 4: Disassemble at the right base

Load the blob at the inferred base/entry in a disassembler/emulator and proceed.

## Validation

- PIC technique hits reference real patterns (GetPC/PEB/API-hash), not arbitrary bytes.
- Architecture is consistent with the PEB-access form detected.
- The analysis points to a concrete entry/base for disassembly.

## Pitfalls

- Encoded/staged shellcode where the PIC patterns appear only after decoding.
- Mixed 32/64-bit (WoW64) transitions.
- Custom GetPC variants not matching common signatures.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the analyzer.
- PEB/LDR and ATT&CK T1027.007 references (linked in frontmatter).
