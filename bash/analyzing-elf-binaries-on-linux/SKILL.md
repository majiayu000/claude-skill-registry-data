---
name: analyzing-elf-binaries-on-linux
description: 'Statically analyzes Linux ELF malware: ELF header and sections, dynamic symbols
  and imports, segment permissions, embedded strings, and packing indicators to infer
  capability without execution. Activates for requests to analyze an ELF binary, Linux
  malware, or shared object.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - static-analysis
  - elf
  - linux
  - symbols
  - entropy
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1059.004
  - T1129
d3fend:
  - D3-FA
  - D3-FCR
references:
  - 'ELF specification (System V ABI) — https://refspecs.linuxfoundation.org/elf/elf.pdf'
  - 'pyelftools — https://github.com/eliben/pyelftools'
---

# Analyzing ELF Binaries on Linux

## When to Use

- You have a Linux executable or shared object and need to assess it statically.
- You want to read the ELF header, segments, dynamic symbols, and strings to infer behavior.
- You are checking for static linking, stripped symbols, or packing.

**Do not use** symbol absence as proof of nothing — stripped or statically linked Go/Rust
binaries hide structure; switch to disassembly when static metadata is thin.

## Prerequisites

- `readelf`/`nm`/`strings` (binutils) or `pyelftools` (`pip install pyelftools`).
- The sample in neutralized form inside the lab.

## Safety & Handling

- Static only: parse the file; do not set it executable or run it.

## Workflow

### Step 1: Read the ELF header

```bash
python scripts/analyst.py analyze sample.elf
```

Note class (ELF32/64), endianness, type (EXEC/DYN/REL), machine (x86-64, ARM, MIPS), and
whether it is stripped.

### Step 2: Examine segments and section permissions

Writable+executable segments, or a single large segment, suggest packing or self-modifying
code. Compare `PT_LOAD` permissions against expectations.

### Step 3: Inspect dynamic symbols and needed libraries

Imported functions hint at capability: `socket`/`connect` (network), `ptrace` (anti-debug or
injection), `fork`/`execve` (process control), `crypt`/`EVP_*` (encryption).

### Step 4: Detect static linking and packing

Static binaries lack a dynamic symbol table and `NEEDED` entries. High whole-file entropy and
a tiny section table suggest a packer (e.g. UPX leaves `UPX!` markers).

### Step 5: Skim strings and constructors

Check `.init_array`/constructors (code before `main`), and strings for paths, URLs, and shell
commands.

## Validation

- Header `type` and segment permissions are consistent with the inferred behavior.
- Imported symbols correspond to plausible capabilities.
- Packing call (entropy + missing sections) matches the strings observed.

## Pitfalls

- Assuming dynamic symbols are complete — they only cover imported/exported names, not
  internal functions.
- Treating a stripped Go binary as "empty"; its structure lives in runtime metadata, not the
  symbol table.
- Ignoring constructors/`.init_array`, which run before `main`.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the ELF analyzer.
- ELF/System V ABI spec and pyelftools (linked in frontmatter).
