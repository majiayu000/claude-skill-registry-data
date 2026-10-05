---
name: phmmer
description: Use when searching one or more protein query sequences against a protein sequence database with HMMER's one-pass sequence-vs-sequence searcher.
disable-model-invocation: true
user-invocable: true
---

# phmmer

## Quick Start
- **Command:** `phmmer`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/phmmer`
- **Version:** HMMER 3.4
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Search protein queries against a protein FASTA database without building a reusable profile HMM first.
- Use HMMER-style statistics for one-pass homolog discovery.
- Prefer `jackhmmer` when you want iterative family expansion, and `hmmsearch` when you already have a profile HMM.
- Use `phmmer` as a protein-oriented counterpart to `nhmmer` for nucleotide work.

## Common Patterns

```bash
# 1) Standard protein-vs-protein search with parseable output tables
phmmer \
  --tblout hits.tbl \
  --domtblout domains.tbl \
  --cpu 8 \
  query.fa \
  proteome.fa
```

```bash
# 2) Save the accepted-hit alignment for later model building
phmmer \
  -A accepted_hits.sto \
  query.fa \
  proteome.fa
```

```bash
# 3) Emit Pfam-style table output when that downstream format is useful
phmmer \
  --pfamtblout pfam.tbl \
  query.fa \
  proteome.fa
```

## Recommended Workflow

1. Start from protein queries and a protein target database in FASTA or another supported sequence format.
2. Save `--tblout` and `--domtblout` outputs so sequence-level and domain-level significance can be inspected separately.
3. If the first-pass search is promising, keep `-A` output for downstream `hmmbuild` or manual curation.
4. Escalate to `jackhmmer` if you need iterative sensitivity rather than a one-shot scan.

## Guardrails

- In this workspace the binary currently fails to start because `libopenblas.so.0` is missing.
- `phmmer` is for protein queries against protein sequence databases, not nucleotide targets.
- Positional argument order matters: query sequence file first, target database second.
- If your input is nucleotide, the HMMER family itself suggests using `nhmmer` or `nhmmscan` instead.
