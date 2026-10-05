---
name: blastp
description: Use when comparing protein sequences against protein databases for similarity searches, homology detection, or functional annotation.
disable-model-invocation: true
user-invocable: true
---

# blastp

## Quick Start
- **Command:** `blastp`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/blastp`
- **Version:** 2.17.0+
- **Reference:** [references/help.md](references/help.md)

## When To Use This Tool

- Search protein queries against protein databases for close or moderate-distance homologs.
- Quick functional annotation or sanity-checking of predicted proteins.
- Use `blastp-short` for short peptides.
- Prefer `psiblast` when ordinary `blastp` is not sensitive enough for distant homologs.

## Common Patterns

```bash
# 1) Standard protein homology search
blastp \
  -query proteins.fa \
  -db prot_db \
  -outfmt "6 qaccver saccver pident length evalue bitscore qcovhsp" \
  -evalue 1e-5 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) Search short peptides
blastp \
  -task blastp-short \
  -query peptides.fa \
  -db prot_db \
  -outfmt 6
```

```bash
# 3) Use a custom scoring matrix when the biology justifies it
blastp \
  -query proteins.fa \
  -db prot_db \
  -matrix BLOSUM80 \
  -outfmt 7
```

## Recommended Workflow

1. Make sure the query FASTA is truly protein and the target database is `prot`.
2. Start with a standard `blastp` run and inspect top hits before tuning matrices or thresholds.
3. Use tabular output for pipelines and pairwise text only for manual review.
4. Escalate to `psiblast` if you need iterative profile-based sensitivity.

## Guardrails
- Query input must be amino-acid sequence, not nucleotide sequence.
- `-db` and `-subject` are mutually exclusive here too.
- Composition-based statistics are on by default; do not change `-comp_based_stats` casually.
- For reproducible filtering, set `-evalue`, `-max_target_seqs`, and `-outfmt` explicitly.
