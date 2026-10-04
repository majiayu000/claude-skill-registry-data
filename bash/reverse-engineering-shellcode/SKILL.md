---
name: reverse-engineering-shellcode
description: 'Analyzes position-independent shellcode: disassembling raw bytes at the right
  architecture, recognizing PEB-walk API resolution and egg hunters, and emulating execution
  to recover behavior and payloads. Activates for requests to analyze shellcode, disassemble
  raw position-independent code, or emulate a shellcode blob.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - shellcode
  - emulation
  - position-independent
  - peb-walk
  - disassembly
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1055
  - T1106
  - T1027
d3fend:
  - D3-PSA
  - D3-FCR
references:
  - 'Capstone disassembly framework — https://www.capstone-engine.org/'
  - 'Unicorn CPU emulator — https://www.unicorn-engine.org/'
---

# Reverse Engineering Shellcode

## When to Use

- You extracted a raw code blob (from a document, exploit, injected memory region, or beacon)
  with no PE/ELF headers.
- You need to determine the architecture, recover the API-resolution method, and understand
  what the shellcode does.
- You want to emulate the shellcode safely to recover staged payloads or C2.

**Do not use** a file-format parser on shellcode — there is no header. Treat it as a flat byte
stream at a known base and disassemble/emulate.

## Prerequisites

- Capstone (`pip install capstone`) for disassembly; Unicorn (`pip install unicorn`) for
  emulation.
- Knowledge of the likely architecture/bitness (x86 vs x64) and calling context.

## Workflow

### Step 1: Determine architecture and entry

Try disassembling as x86 and x64; the one that yields coherent instructions (and a sane
prologue) is correct. Shellcode usually starts executing at offset 0.

```bash
python scripts/analyst.py disasm shellcode.bin --arch x64
```

### Step 2: Recognize API resolution

Windows shellcode typically walks the PEB to find `kernel32`, then resolves exports by hash:

```text
mov rax, gs:[60h]        ; PEB (x64)   / mov eax, fs:[30h] (x86)
... traverse Ldr -> InMemoryOrderModuleList
... hash export names, compare to embedded constants
```

Recovered hash constants feed the API-hash resolver (see the obfuscation skill).

### Step 3: Identify the technique

Look for egg hunters (searching memory for a tag), socket setup (reverse/bind shell), or a
download-and-exec stager (`WinINet`/`WinHTTP` resolution then a URL).

### Step 4: Emulate to recover behavior

Emulate with Unicorn, hooking memory and (optionally) faking API calls, to observe the
control flow and extract strings/URLs the static view hides:

```bash
python scripts/analyst.py emulate shellcode.bin --arch x64 --base 0x140000000
```

### Step 5: Extract IOCs and payload

Recover C2 URLs/hosts, embedded second stages, and the resolved API set for the report.

## Validation

- The chosen architecture yields a coherent prologue and no garbage instruction stream.
- Recovered API hashes resolve to a sensible function set (LoadLibrary/GetProcAddress, network
  APIs).
- Emulation reaches the network/exec stage consistent with the static read.

## Pitfalls

- Disassembling at the wrong bitness and chasing nonsense.
- Emulating without bounding execution, looping forever on unresolved calls.
- Ignoring self-modifying decoders — emulate through the decode stub to reach real code.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the disassembler and
  emulator wrapper.
- Capstone and Unicorn (linked in frontmatter).
