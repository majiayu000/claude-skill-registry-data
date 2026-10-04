---
name: recovering-injected-code-and-shellcode
description: 'Carves injected PE images and position-independent shellcode from a memory dump or
  carved region, identifies the payload type, and prepares it for disassembly or emulation.
  Activates for requests to recover injected code, carve shellcode from memory, or reconstruct a
  dumped payload for analysis.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - shellcode
  - memory-forensics
  - carving
  - dynamic-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1055
  - T1620
  - T1027
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'MITRE ATT&CK T1620 Reflective Code Loading — https://attack.mitre.org/techniques/T1620/'
  - 'MITRE ATT&CK T1055 Process Injection — https://attack.mitre.org/techniques/T1055/'
---

# Recovering Injected Code and Shellcode

## When to Use

- You have a carved memory region (from malfind/vaddump) and need to identify and extract the
  payload — an injected PE or raw shellcode.
- You need to locate likely shellcode entry points (egg hunters, GetPC stubs) before disassembly.

**Do not use** this to execute the payload — it prepares code for static disassembly/emulation in
a controlled tool, not for running.

## Prerequisites

- A carved binary region (raw bytes) from a memory image.

## Safety & Handling

- The carved region is live malicious code; store it password-protected and never execute it.

## Workflow

### Step 1: Identify payload type

```bash
python scripts/analyst.py identify region.bin
```

Detects an embedded `MZ`/PE (with offset) versus raw shellcode, and reports the PE's architecture
if present.

### Step 2: Locate shellcode entry hints

Finds common position-independent code markers: GetPC stubs (`call $+5`/`fldz/fnstenv`), PEB
access (`fs:[30]`/`gs:[60]`), and API-hashing loops.

### Step 3: Extract for analysis

Carve the PE at its offset (or keep the raw shellcode) and hand it to a disassembler/emulator at
the detected base/entry.

### Step 4: Document

Record offsets, architecture, and entry hints for the downstream RE workflow.

## Validation

- An embedded PE is confirmed by `MZ` + valid `e_lfanew` → `PE\0\0`.
- Shellcode entry hints reference real PIC patterns, not arbitrary bytes.
- Architecture detection matches the PE Machine field (or PIC heuristics for raw shellcode).

## Pitfalls

- Assuming everything carved is a PE; much injected code is headerless shellcode.
- Wrong base address breaking relocations when loading a dumped PE — note it for rebuilding.
- Treating compressed/encrypted stages as final shellcode without a decode pass.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the identifier.
- ATT&CK T1620 and T1055 (linked in frontmatter).
