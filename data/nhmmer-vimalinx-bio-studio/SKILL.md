---
name: nhmmer
description: Use when searching DNA or RNA queries against nucleotide sequence databases with HMMER's nucleotide homology search engine.
disable-model-invocation: true
user-invocable: true
---

# nhmmer

## Quick Start
- **Command:** `nhmmer`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/nhmmer`
- **Version:** HMMER 3.4
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Search DNA or RNA queries against nucleotide sequence databases with HMMER sensitivity.
- Look for more remote nucleotide homologs than simple pairwise nucleotide aligners tend to recover.
- Restrict searches to the Watson or Crick strand when the biology justifies it.
- Prefer `nhmmscan` when the target is a nucleotide HMM database rather than a plain sequence database.

## Common Patterns

```bash
# 1) Search a nucleotide query against a genomic FASTA database
nhmmer \
  --tblout hits.tbl \
  --cpu 8 \
  query.fa \
  genome.fa
```

```bash
# 2) Search only one strand
nhmmer \
  --watson \
  --tblout watson_hits.tbl \
  query.fa \
  genome.fa
```

```bash
# 3) Use curated model thresholds and save Dfam-style output
nhmmer \
  --cut_ga \
  --dfamtblout dfam.tbl \
  query.fa \
  genome.fa
```

## Recommended Workflow

1. Start from a nucleotide query and a nucleotide target database in FASTA or another supported sequence format.
2. Save parseable output with `--tblout`, and use `--dfamtblout` if you are working in a Dfam-like annotation workflow.
3. Apply strand restriction or curated thresholds only when the underlying assay or model supports those assumptions.
4. Review significant hits before deciding whether to promote the query into a reusable profile model.

## Guardrails

- In this workspace the binary currently fails to start because `libopenblas.so.0` is missing.
- `nhmmer` expects DNA or RNA queries and DNA/RNA targets; it is not the protein HMMER engine.
- If the query comes from stdin, the local binary expects `--qformat` to be set explicitly.
- Use `--watson` or `--crick` deliberately; do not silently halve the search space unless strand specificity is real.
