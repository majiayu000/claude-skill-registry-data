---
name: unpacking-upx-and-common-packers
description: 'Identifies and unpacks packed binaries: detecting packers from section names and
  entropy, automatically unpacking UPX, and manually unpacking custom packers by finding the
  OEP and dumping. Activates for requests to unpack a packed sample, detect a packer, or
  recover the original binary from UPX or a custom packer.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - unpacking
  - upx
  - packers
  - entropy
  - oep
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027.002
  - T1140
  - T1480
d3fend:
  - D3-FCR
  - D3-PSA
references:
  - 'UPX — https://upx.github.io/'
  - 'Detect It Easy (DIE) — https://github.com/horsicq/Detect-It-Easy'
---

# Unpacking UPX and Common Packers

## When to Use

- A sample shows high entropy, few imports, or packer section names, and you need the original
  code for static analysis or RE.
- You want to unpack UPX automatically or manually unpack a custom/modified packer.
- You are preparing a sample for Ghidra/IDA (decompiling packed code is pointless).

**Do not use** generic unpackers as a guarantee — modified UPX and custom packers defeat
`upx -d`. Fall back to debugger-based manual unpacking.

## Prerequisites

- Packer detection (Detect It Easy, or the bundled section/entropy heuristics).
- `upx` for standard UPX; x64dbg + Scylla for manual unpacking (see the x64dbg skill).
- Isolated lab.

## Workflow

### Step 1: Detect the packer

```bash
python scripts/analyst.py detect sample.bin
```

Signals: section names (`UPX0`/`UPX1`, `.aspack`, `.themida`), high section entropy, a tiny
import table, and a small `.text` with a large high-entropy section.

### Step 2: Try automated UPX unpacking

If standard UPX:

```bash
upx -d -o sample_unpacked.bin sample.bin
```

If `upx -d` fails on a UPX-like sample, the header was likely tampered (e.g. `UPX!` magic or
version bytes altered) — repair the marker or unpack manually.

### Step 3: Manual unpacking for custom packers

In x64dbg: break on `VirtualAlloc`/`VirtualProtect`, run until the unpacked region is written
and made executable, find the **tail jump** to the original entry point (OEP), and dump there.

### Step 4: Dump and rebuild imports

Use Scylla to dump the process and reconstruct the Import Address Table (IAT) so the dumped PE
loads in a disassembler.

### Step 5: Verify the unpacked result

Confirm the dump is a clean PE with a populated import table and readable strings/code.

## Validation

- The unpacked file has restored imports and meaningful strings absent from the packed sample.
- Entropy of the unpacked `.text` drops to normal code levels.
- The disassembler resolves API calls (IAT rebuilt correctly).

## Pitfalls

- Running `upx -d` on tampered UPX and concluding it is not UPX; check for renamed/edited
  markers.
- Dumping before reaching the OEP, capturing still-encrypted code.
- Forgetting IAT reconstruction, leaving the dump unusable in Ghidra/IDA.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the packer detector.
- UPX and Detect It Easy (linked in frontmatter).
