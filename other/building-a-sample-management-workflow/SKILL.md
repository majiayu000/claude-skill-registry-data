---
name: building-a-sample-management-workflow
description: 'Establishes a disciplined malware sample repository: content-addressed storage by
  hash, encrypted/password-protected archiving, consistent metadata records, and chain-of-custody
  tracking so samples are reproducible and safe to handle. Activates for requests to organize a
  malware repository, manage samples, or track sample metadata and provenance.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - sample-management
  - storage
  - metadata
  - chain-of-custody
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1587
d3fend:
  - D3-FH
references:
  - 'NIST SP 800-86 Guide to Integrating Forensic Techniques into Incident Response — https://csrc.nist.gov/pubs/sp/800/86/final'
  - 'MalwareBazaar sample conventions — https://bazaar.abuse.ch/'
---

# Building a Sample Management Workflow

## When to Use

- You are accumulating malware samples and need a repeatable, safe way to store and find them.
- You need metadata and provenance (source, date, case) attached to every sample.
- You want content-addressed storage so the same sample is never duplicated or misnamed.

**Do not use** original filenames or loose folders as the organizing principle — names are
attacker-controlled and collide; address samples by hash.

## Prerequisites

- The hashing skill for content addressing; encrypted/password-protected archive tooling.
- A defined storage location inside the isolated lab.

## Safety & Handling

- Store every sample inside a password-protected archive (commonly `infected`) so it cannot
  auto-execute or be scanned/quarantined by host AV.
- Strip the executable bit / neutralize the extension at rest; restore only inside the lab.

## Workflow

### Step 1: Content-address on intake

On receipt, compute SHA-256 and store the sample under a path derived from its hash
(e.g., `samples/ab/cd/<sha256>`), preventing duplicates and name collisions.

```bash
python scripts/analyst.py intake sample.bin --source "phishing-case-42" --store ./samples
```

### Step 2: Record metadata

Write a metadata record per sample: hashes, original name, source, intake date, case ID,
file type, and analyst — kept next to the sample or in an index.

### Step 3: Archive safely

Wrap the sample in a password-protected archive; keep the inert copy out of host AV's reach and
the metadata in plaintext for searchability.

### Step 4: Maintain chain of custody

Append-only log each access/action (who, when, what) so the sample's handling is auditable.

### Step 5: Index and search

Build a searchable index over metadata so samples can be found by hash, family, source, or case
without touching the raw bytes.

## Validation

- The same sample always lands at the same hash-derived path (idempotent intake).
- Every sample has a complete metadata record and an access log entry.
- Samples are stored password-protected; metadata is searchable in plaintext.

## Pitfalls

- Organizing by attacker-supplied filename, causing collisions and confusion.
- Storing live samples unarchived where host AV deletes them mid-analysis.
- Losing provenance, so an indicator cannot be traced back to its case.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the intake/indexer.
- NIST SP 800-86 and MalwareBazaar conventions (linked in frontmatter).
