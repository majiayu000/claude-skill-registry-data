---
name: hmmscan
description: Use when searching protein sequences against profile hidden Markov models (HMMs) such as Pfam or other HMM databases.
disable-model-invocation: true
user-invocable: true
---

# hmmscan

## Quick Start
- **Command:** `hmmscan [-options] <hmmdb> <seqfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmscan`
- **Version:** HMMER 3.4
- **Full reference:** See [references/help.md](references/help.md) for detailed options

## When To Use This Tool

- Annotate protein sequences against an HMM database such as Pfam.
- Find domains or families for many query proteins at once.
- Prefer `hmmscan` when the query is sequence and the target is the HMM database.
- Press the HMM database first with `hmmpress` for faster repeated scans.

## Common Patterns

```bash
# 1) Scan proteins against a pressed HMM database
hmmscan \
  --tblout hits.tbl \
  --domtblout domains.tbl \
  --cpu 8 \
  Pfam-A.hmm \
  proteins.fa
```

```bash
# 2) Use curated gathering thresholds from the database
hmmscan \
  --cut_ga \
  --domtblout domains.tbl \
  Pfam-A.hmm \
  proteins.fa
```

```bash
# 3) Produce smaller text output while keeping parseable tables
hmmscan \
  --noali \
  --tblout hits.tbl \
  --domtblout domains.tbl \
  Pfam-A.hmm \
  proteins.fa
```

## Recommended Workflow

1. Press the HMM database once with `hmmpress` if you will reuse it.
2. Scan the sequence FASTA and save both sequence-level and domain-level tables.
3. Use curated thresholds when available; otherwise set E-value thresholds explicitly.
4. Review domain architecture, not just best-hit name, before functional labeling.

## Guardrails

- Positional argument order matters: HMM database first, query sequence file second.
- Use `-h` for help; `--help` and `--version` are not valid here.
- `--cut_ga`, `--cut_tc`, and `--cut_nc` only make sense if the HMMs actually carry curated thresholds.
- Use `--domtblout` when domain boundaries matter; `--tblout` alone is not enough.
