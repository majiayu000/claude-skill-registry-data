---
name: extracting-and-classifying-strings
description: 'Extracts ASCII and Unicode strings from a binary and classifies them into
  investigative categories: URLs, IPs, file paths, registry keys, mutexes, commands, and API
  names, prioritizing the analyst''s attention. Activates for requests to extract strings,
  classify strings output, or pull human-readable artifacts from a sample.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - strings
  - static-analysis
  - triage
  - ioc
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'GNU binutils strings — https://www.gnu.org/software/binutils/'
  - 'FLOSS (FLARE Obfuscated String Solver) — https://github.com/mandiant/flare-floss'
---

# Extracting and Classifying Strings

## When to Use

- You are triaging a sample and want quick investigative leads from its readable strings.
- You need both ASCII and UTF-16LE (Unicode) strings, which many tools miss by default.
- You want strings grouped by meaning (URLs, paths, registry, commands) rather than a flat dump.

**Do not use** plaintext strings as the whole story for packed/obfuscated samples — the useful
strings may be encrypted; pair with entropy checks and deobfuscation (FLOSS) when the dump is
sparse.

## Prerequisites

- Python (stdlib) or `strings`/FLOSS; the sample handled inertly in the lab.

## Safety & Handling

- Extract strings from the inert file; never execute the sample.
- Defang any URLs/IPs before putting them in a report or ticket.

## Workflow

### Step 1: Extract ASCII and Unicode strings

Pull printable runs at a minimum length (default 4–5) for both ASCII and UTF-16LE encodings to
avoid missing Windows wide strings.

```bash
python scripts/analyst.py strings sample.bin --min-len 5
```

### Step 2: Classify by category

Bucket strings into URLs, IPs, domains, file paths, registry keys, mutex/event names, suspicious
commands, and API names so leads surface immediately.

### Step 3: Prioritize leads

Promote network indicators, command lines, and suspicious API references to the top; defang
network artifacts for safe handling.

### Step 4: Recognize obfuscation

A near-empty or junk-only dump signals packing/string obfuscation; route to entropy analysis and
FLOSS/manual deobfuscation.

## Validation

- Both ASCII and Unicode strings are extracted (Windows wide strings are not missed).
- Strings are grouped into useful categories, not a flat list.
- A sparse/garbage dump is correctly read as an obfuscation signal, not "clean".

## Pitfalls

- Extracting ASCII only and missing UTF-16LE strings.
- Treating a packed sample's empty dump as benign.
- Reporting live URLs/IPs without defanging.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the string extractor.
- binutils strings and FLOSS (linked in frontmatter).
