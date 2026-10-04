---
name: resolving-dynamic-api-hashing
description: 'Resolves dynamically hashed Windows API names by brute-forcing observed hash constants
  against a wordlist of API/DLL names using common malware hashing algorithms (ROR13, djb2, FNV,
  CRC32). Activates for requests to resolve API hashes, identify hashed imports, or reverse an API
  hashing routine.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - api-hashing
  - obfuscation
  - imports
  - deobfuscation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027.007
  - T1106
  - T1140
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'MITRE ATT&CK T1027.007 Dynamic API Resolution — https://attack.mitre.org/techniques/T1027/007/'
  - 'Windows API Index — https://learn.microsoft.com/windows/win32/apiindex/windows-api-list'
---

# Resolving Dynamic API Hashing

## When to Use

- A sample resolves APIs by hash (no plaintext import names) and you have the hash constants from
  disassembly.
- You need to map each hash back to an API/DLL name to understand functionality.

**Do not use** this to execute the resolver — it computes hashes over a name wordlist statically
and matches them to your observed constants.

## Prerequisites

- The hash constants observed in the binary and (optionally) a names wordlist.

## Workflow

### Step 1: Identify the algorithm

```bash
python scripts/analyst.py id 0x6A4ABC5B
```

Computes the constant under each supported algorithm against a built-in seed list to suggest which
algorithm/seed reproduces known API hashes.

### Step 2: Resolve hashes against a wordlist

```bash
python scripts/analyst.py resolve hashes.txt --algo ror13 --wordlist names.txt
```

Brute-forces the provided hashes against the wordlist using the chosen algorithm and reports
matches.

### Step 3: Annotate the disassembly

Label resolved call sites with their API names to recover behavior.

### Step 4: Document the routine

Record the algorithm, seed/initial value, and any key so the routine is reusable.

## Validation

- The chosen algorithm reproduces at least one known API hash (sanity anchor).
- Resolved names are real exported symbols of plausible DLLs.
- Unresolved hashes are reported, not silently dropped.

## Pitfalls

- Wrong endianness/rotation direction producing no matches — try variants.
- Algorithms seeded with a per-sample key; without the key, matches fail.
- Case sensitivity: some routines hash uppercased names, others as-is.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the resolver.
- ATT&CK T1027.007 and the Windows API Index (linked in frontmatter).
