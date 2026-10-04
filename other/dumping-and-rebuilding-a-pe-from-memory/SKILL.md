---
name: dumping-and-rebuilding-a-pe-from-memory
description: 'Rebuilds a usable PE file from a memory dump by fixing the section alignment
  (virtual-to-raw), correcting the entry point, and preparing for import table reconstruction.
  Activates for requests to rebuild a dumped PE, fix a memory-dumped executable, or convert a
  process dump into an analyzable file.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - unpacking
  - pe-rebuild
  - memory
  - imports
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027.002
  - T1620
  - T1055.012
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'PE Format — https://learn.microsoft.com/windows/win32/debug/pe-format'
  - 'MITRE ATT&CK T1620 Reflective Code Loading — https://attack.mitre.org/techniques/T1620/'
---

# Dumping and Rebuilding a PE From Memory

## When to Use

- You have a process/region dump of an unpacked or injected PE and need a file that loads in a
  disassembler.
- You need to convert virtual (loaded) layout back toward raw layout and fix the entry point.

**Do not use** this on a still-packed image — unpack to OEP first. This skill operates on an
already-captured dump; it does not execute the sample.

## Prerequisites

- A raw PE dump (e.g., from x64dbg Scylla, vaddump) and the OEP if known.

## Safety & Handling

- The dump is live malicious code; store password-protected and never execute it.

## Workflow

### Step 1: Inspect the dumped headers

```bash
python scripts/analyst.py inspect dump.bin
```

Reports whether section RawAddress/RawSize match VirtualAddress/VirtualSize (memory-aligned dumps
have raw==virtual) and the current AddressOfEntryPoint.

### Step 2: Realign sections to raw layout

```bash
python scripts/analyst.py fix dump.bin --oep 0x1234 -o rebuilt.bin
```

Rewrites each section's PointerToRawData/SizeOfRawData to its virtual layout (the on-disk-from-
memory convention) and sets the entry point to the supplied OEP.

### Step 3: Reconstruct imports

The dumped image usually has a destroyed IAT; rebuild it with an import reconstructor (Scylla/
ImpRec) using the OEP, then re-inspect.

### Step 4: Verify

Confirm the rebuilt file parses, has a valid entry point, and disassembles.

## Validation

- Section table is internally consistent (no overlaps, within file size).
- AddressOfEntryPoint points inside an executable section.
- The rebuilt file is accepted by a PE parser/disassembler.

## Pitfalls

- Forgetting that memory dumps use virtual alignment — raw offsets must be rewritten.
- Setting an OEP RVA that lies outside any section.
- Skipping IAT reconstruction, leaving call targets pointing at null/garbage.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the rebuilder.
- PE format spec and ATT&CK T1620 (linked in frontmatter).
