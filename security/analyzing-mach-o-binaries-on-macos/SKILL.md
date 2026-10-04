---
name: analyzing-mach-o-binaries-on-macos
description: 'Statically analyzes macOS Mach-O malware: parsing the header and load commands,
  handling fat/universal binaries, reading linked dylibs and entitlements, and checking code
  signatures to infer capability and trust. Activates for requests to analyze a Mach-O binary,
  inspect macOS malware, or parse load commands and entitlements.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - mach-o
  - macos
  - static-analysis
  - code-signing
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1059.002
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'Apple Mach-O file format reference — https://github.com/apple-oss-distributions/xnu/blob/main/EXTERNAL_HEADERS/mach-o/loader.h'
  - 'macOS code signing overview — https://developer.apple.com/documentation/security/code_signing_services'
---

# Analyzing Mach-O Binaries on macOS

## When to Use

- You have a macOS sample (Mach-O) and need a static capability and trust read.
- You must handle a fat/universal binary containing multiple architecture slices.
- You need to inspect linked dylibs, entitlements, and code-signing status.

**Do not use** Windows PE tooling on Mach-O — the formats differ entirely; use Mach-O-aware
parsers.

## Prerequisites

- A Mach-O parser (Python stdlib `struct`, or `macholib`/LIEF); the sample handled inertly.
- For signing/entitlements on macOS, `codesign`/`otool` are authoritative.

## Safety & Handling

- Parse statically; never execute the sample, especially on a real macOS host.
- Keep the sample password-protected at rest and reference it by hash.

## Workflow

### Step 1: Detect fat vs. thin and architecture

Check the magic: `0xCAFEBABE` (fat/universal) vs. `0xFEEDFACE`/`0xFEEDFACF` (Mach-O 32/64). For
fat binaries, enumerate and analyze each slice.

```bash
python scripts/analyst.py header sample.macho
```

### Step 2: Parse load commands

Read load commands for linked dylibs (`LC_LOAD_DYLIB`), entry point (`LC_MAIN`), and signing
(`LC_CODE_SIGNATURE`). The dylib list hints at capability (networking, crypto).

### Step 3: Inspect entitlements and signing

On macOS, use `codesign`/`otool` to read entitlements and verify the signature. Ad-hoc or absent
signatures and suspicious entitlements are risk indicators.

### Step 4: Infer capability and route

Map linked frameworks/symbols to behaviors and route to disassembly/RE for deeper analysis.

## Validation

- Fat binaries are decomposed and each slice is analyzed, not just the first.
- Load commands, dylibs, and signing status are enumerated correctly.
- Capability inferences are corroborated by linked frameworks/symbols.

## Pitfalls

- Analyzing only one slice of a universal binary.
- Trusting a present signature without verifying it (ad-hoc signatures verify but aren't trusted).
- Applying PE assumptions (sections/imports) to Mach-O structures.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the Mach-O header parser.
- Apple Mach-O loader.h and code signing docs (linked in frontmatter).
