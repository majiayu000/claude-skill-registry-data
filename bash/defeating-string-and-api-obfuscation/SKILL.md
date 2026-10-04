---
name: defeating-string-and-api-obfuscation
description: 'Recovers obfuscated strings and resolves dynamically loaded APIs in malware:
  reversing XOR/stack-string/encoding schemes and mapping API-hash lookups back to function
  names. Activates for requests to deobfuscate strings, decode stack strings, or resolve
  API hashing in a binary.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - obfuscation
  - strings
  - api-hashing
  - xor
  - deobfuscation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1140
  - T1106
d3fend:
  - D3-FCR
  - D3-FA
references:
  - 'FLOSS (FLARE Obfuscated String Solver) — https://github.com/mandiant/flare-floss'
  - 'API hashing techniques (ROR13 / djb2) — https://learn.microsoft.com/windows/win32/api/'
---

# Defeating String and API Obfuscation

## When to Use

- A binary has few readable strings because they are XOR/stack-encoded or built at runtime.
- The import table is sparse because APIs are resolved by hash at runtime.
- You need to recover C2 URLs, paths, and the real API set to understand behavior.

**Do not use** plain `strings` and conclude "no indicators" — modern malware hides strings;
absence of readable strings is itself a sign of obfuscation.

## Prerequisites

- A disassembler/decompiler to read the decode routine, plus the bundled XOR/hash tooling.
- Optionally FLOSS for automated stack/decoded-string recovery.

## Workflow

### Step 1: Recognize the obfuscation type

```text
Stack strings  : bytes mov'd to the stack one/few at a time, then used
Single-byte XOR: a loop XORing a buffer with a constant
Multi-byte/RC4 : a keyed stream over a blob
API hashing    : a hash compared against export-name hashes to resolve functions
```

### Step 2: Recover XOR-encoded strings

If you find the key and ciphertext, decode directly. The script brute-forces single-byte XOR
and surfaces readable results:

```bash
python scripts/analyst.py xor-strings sample.bin
```

### Step 3: Reconstruct stack strings

Read the decompiler to collect the byte sequence assembled on the stack and reassemble it. For
volume, FLOSS emulates and extracts these automatically.

### Step 4: Resolve API hashing

Identify the hash algorithm (often ROR13/ROR7 additive, or djb2). Precompute hashes for known
export names and match the constants in the binary back to functions:

```bash
python scripts/analyst.py api-hash --algo ror13 --hash 0x726774C
```

### Step 5: Reannotate and extract IOCs

Apply recovered strings and API names back in the disassembler and extract the now-visible
URLs, paths, and behavior.

## Validation

- Decoded strings are meaningful (URLs, DLL/API names, paths), not random bytes.
- Resolved API names match the calls' usage in the surrounding code.
- The recovered API set explains behavior seen dynamically.

## Pitfalls

- Assuming single-byte XOR when it is keyed/RC4; check key length and the decode loop.
- Using the wrong hash algorithm/seed and getting no matches — verify against a known function.
- Recovering strings but not feeding them back into the analysis.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the XOR and API-hash
  tools.
- FLOSS and API-hashing references (linked in frontmatter).
