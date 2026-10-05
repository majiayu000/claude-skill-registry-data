---
name: md5fa
description: Use when hashing FASTA records and comparing ordered versus order-insensitive sequence digests instead of taking a single whole-file MD5.
disable-model-invocation: true
user-invocable: true
---

# md5fa

md5fa is an HTSlib-based FASTA digester. It emits one MD5 per FASTA record plus two aggregate summaries, `>ordered` and `>unordered`, so it is materially different from `md5sum` on the raw file bytes.

## Quick Start

- **Command:** `md5fa <fasta>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/md5fa`
- **Live output shape:** `md5  fasta_path  record_label`

## When To Use This Tool

- Hash FASTA content at the record level instead of hashing the literal file bytes.
- Compare two FASTA files while distinguishing "same records, different order" from "different sequence content".
- Generate stable per-sequence digests for reference or manifest workflows.

## Common Patterns

```bash
# 1) Hash every FASTA record plus aggregate ordered/unordered summaries
md5fa sample.fa
```

```bash
# 2) Use the >unordered line when record order should not matter
md5fa a.fa
md5fa b.fa
# in local testing, swapping record order changed >ordered but kept >unordered identical
```

```bash
# 3) Capture the digest table for later comparison
md5fa sample.fa > sample.fa.md5fa.txt
```

## Recommended Workflow

1. Run `md5fa` on a valid FASTA file rather than on arbitrary text.
2. Compare the per-record lines first if you need to identify which sequence changed.
3. Compare `>ordered` when record order is meaningful and `>unordered` when you only care about the multiset of records.
4. Store the full output table, not just one line, because the aggregate summaries capture different invariants.

## Guardrails

- `md5fa -h` is not help; it is treated as a filename and errors with `md5fa: -h: No such file or directory`.
- This is not a whole-file checksum tool. A multi-record FASTA produces one digest per record plus `>ordered` and `>unordered`.
- In live testing, swapping the order of two FASTA records changed the `>ordered` digest but left `>unordered` unchanged.
- An empty FASTA emitted the normal empty MD5 for `>ordered` (`d41d8cd98f00b204e9800998ecf8427e`) and an all-zero digest for `>unordered`.
- Output includes three fields: digest, source FASTA path, and record label. Downstream parsers should not assume a plain two-column `md5sum` layout.
