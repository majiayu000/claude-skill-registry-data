---
name: building-config-extractors
description: 'Builds reusable malware configuration extractors by applying a declarative JSON spec
  (offsets, decode layers, field definitions) to a sample to produce structured, defanged config.
  Activates for requests to build a config extractor, write a reusable family config parser, or run
  a spec-driven configuration extraction.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - config-extraction
  - automation
  - tooling
  - c2
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1140
  - T1027
  - T1071
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'MITRE ATT&CK T1140 Deobfuscate/Decode Files or Information — https://attack.mitre.org/techniques/T1140/'
  - 'MWCP / config-extractor framework concepts — https://github.com/Defense-Cyber-Crime-Center/DC3-MWCP'
---

# Building Config Extractors

## When to Use

- You have reversed a family's config format and want a reusable, declarative extractor instead of
  one-off scripts.
- You need to apply a spec (offset, XOR/base64 layers, field map) to many samples and emit
  structured, defanged config.

**Do not use** a spec built for one variant blindly on another — re-verify offsets/keys per
variant. This skill reads samples statically and executes nothing.

## Prerequisites

- A reversed understanding of the config (location, decode layers, fields) expressed as a JSON
  spec.

## Safety & Handling

- Read bytes statically; defang recovered endpoints in output.

## Workflow

### Step 1: Write the extraction spec

Define a JSON spec: blob `offset`/`length` (or a `marker` to search), ordered `decode` layers
(`xor` with key, `base64`), and `fields` (name, offset, length, type: `str`/`u16`/`u32`/`ipv4`).

### Step 2: Run the extractor

```bash
python scripts/analyst.py extract sample.bin --spec family.json
```

Locates the blob, applies decode layers, parses fields, and defangs URL/IP fields.

### Step 3: Validate output

Confirm fields are plausible (valid hosts, ports, IDs); adjust the spec as needed.

### Step 4: Reuse

Store the spec per family and apply across the corpus.

## Validation

- The spec round-trips on a known sample to the expected config.
- Decode layers are applied in order and produce readable output.
- URL/IP fields are defanged in the emitted config.

## Pitfalls

- Hardcoding a variant-specific offset that shifts in other builds — prefer markers.
- Wrong field endianness (`u16`/`u32` little vs big) producing garbage ports.
- Forgetting a decode layer (base64 over XOR) and parsing ciphertext as fields.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the extractor engine.
- ATT&CK T1140 and config-extractor framework concepts (linked in frontmatter).
