---
name: writing-yara-rules-from-reversed-code
description: 'Turns reverse-engineering findings into durable YARA detections: selecting stable
  code constructs and constants over volatile strings, extracting opcode/byte patterns with
  wildcards, and validating rules for low false positives. Activates for requests to write a
  YARA rule from reversed code, create a detection signature, or convert RE findings into
  hunting rules.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - yara
  - detection
  - signatures
  - threat-hunting
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027.001
  - T1587.001
d3fend:
  - D3-FCR
  - D3-FA
references:
  - 'YARA documentation — https://yara.readthedocs.io/'
  - 'YARA writing-better-rules guidance — https://github.com/Neo23x0/YARA-Style-Guide'
---

# Writing YARA Rules from Reversed Code

## When to Use

- You finished reversing a sample/family and want a detection that survives recompilation and
  cosmetic changes.
- You need byte-pattern signatures from decryptors, API-hash constants, or unique algorithms
  rather than fragile strings.
- You are converting RE notes into hunting/scanning rules for a corpus.

**Do not use** volatile artifacts (file paths, mutex names that change per build, packer stubs
shared across unrelated families) as your primary anchor — they cause drift and false hits.

## Prerequisites

- The `yara` engine (and ideally `yara-python`) for testing.
- A small corpus: target samples (true positives) and clean/unrelated files (false-positive
  control).

## Workflow

### Step 1: Choose stable anchors

Prefer, in order: a unique algorithm's opcode sequence (decryptor, hashing loop), embedded
magic constants (API hashes, XOR keys, S-box), then distinctive strings only if intrinsic.

### Step 2: Extract byte patterns with wildcards

Pull the relevant opcodes and wildcard volatile operands (addresses, immediates) so the rule
survives relocation/recompilation:

```text
$dec = { 8A 04 ?? 34 ?? 88 04 ?? 41 3B ?? 7? ?? }   ; xor-decrypt loop, regs/disp wildcarded
```

### Step 3: Assemble the rule

Combine 2–3 independent anchors with a `condition` requiring enough of them, plus a cheap
prefilter (file size, PE magic) to keep scanning fast:

```bash
python scripts/analyst.py scaffold --name family_xyz --hash 0xABCDEF12
```

### Step 4: Validate against the corpus

Run the rule across true positives and the clean control set; require all TPs match and zero
FPs on the control.

```bash
yara -r rules/family_xyz.yar ./corpus
```

### Step 5: Tune and document

Adjust thresholds, add `meta` (author, date, reference, hash), and record which construct each
string anchors so future analysts can maintain it.

## Validation

- Rule matches all intended samples and produces zero hits on the clean control set.
- Anchors map to intrinsic code/constants, not build-specific noise.
- `meta` documents source samples and the reasoning for each pattern.

## Pitfalls

- Wildcarding too little (brittle) or too much (false positives); wildcard only volatile bytes.
- Anchoring on shared library/packer code present in unrelated binaries.
- Skipping the clean-corpus test, shipping a noisy rule.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the rule scaffolder.
- YARA documentation and style guide (linked in frontmatter).
