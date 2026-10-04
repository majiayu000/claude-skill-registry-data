---
name: hashing-and-fingerprinting-files
description: 'Computes cryptographic and fuzzy fingerprints for malware samples: MD5/SHA-1/SHA-256
  for exact identity, plus import hashing (imphash), section hashing, and fuzzy hashes (ssdeep,
  TLSH) to cluster related variants. Activates for requests to hash a sample, compute imphash,
  or fingerprint files for similarity clustering.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - hashing
  - fingerprinting
  - imphash
  - fuzzy-hashing
  - clustering
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
d3fend:
  - D3-FH
references:
  - 'ssdeep fuzzy hashing — https://ssdeep-project.github.io/ssdeep/'
  - 'TLSH locality-sensitive hashing — https://github.com/trendmicro/tlsh'
---

# Hashing and Fingerprinting Files

## When to Use

- You need a stable identity for a sample to look up, deduplicate, or share as an IOC.
- You want to cluster related variants that differ slightly using fuzzy/similarity hashes.
- You are computing imphash or section hashes to pivot across a malware family.

**Do not use** cryptographic hashes alone to judge similarity — a single byte change yields a
completely different SHA-256; use fuzzy/import hashing for relatedness.

## Prerequisites

- Python with `hashlib` (stdlib); optionally `ssdeep`/`python-tlsh` for fuzzy hashes and
  `pefile` for imphash.
- Samples handled in the isolated lab per the safe-handling skill.

## Safety & Handling

- Treat every sample as live: never execute it during hashing; operate on the inert file only.
- Store samples encrypted/password-protected and reference them by hash, not by original name.

## Workflow

### Step 1: Compute cryptographic hashes

Generate MD5, SHA-1, and SHA-256. SHA-256 is the canonical identity for sharing; MD5/SHA-1 aid
lookups in legacy feeds.

```bash
python scripts/analyst.py hash sample.bin
```

### Step 2: Compute structural hashes (PE)

For PE files, compute imphash (hash of the import table) and per-section hashes to pivot across
samples built from the same toolchain.

### Step 3: Compute fuzzy/similarity hashes

Generate ssdeep and/or TLSH digests so near-duplicates can be matched even when bytes differ.

### Step 4: Record and cross-reference

Store all digests with the sample metadata; query threat-intel feeds by SHA-256 and cluster by
imphash/fuzzy hash.

## Validation

- The same input always yields identical cryptographic hashes (deterministic).
- Imphash matches across known-related samples; fuzzy hashes score high similarity for variants.
- Digests are recorded alongside sample metadata for later pivoting.

## Pitfalls

- Treating MD5 collisions as identity proof; use SHA-256 as canonical.
- Assuming different cryptographic hashes mean unrelated files; check fuzzy/import hashes.
- Computing imphash on packed samples (imports are stubbed) and over-trusting the result.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hashing helper.
- ssdeep and TLSH (linked in frontmatter).
