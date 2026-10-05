---
name: nhmmscan
description: Use when scanning DNA or RNA sequences against a nucleotide profile HMM database such as Dfam to identify annotated families or repeated elements.
disable-model-invocation: true
user-invocable: true
---

# nhmmscan

## Quick Start
- **Command:** `nhmmscan [options] <hmmdb> <seqfile>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/nhmmscan`
- **Version:** HMMER 3.4
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Annotate DNA or RNA sequences against a database of nucleotide profile HMMs.
- Run Dfam-style repetitive element or family annotation against genome fragments or contigs.
- Prefer `nhmmer` when you have one query and a plain nucleotide database instead of an HMM database.
- Save Dfam-style tables when you plan to feed results into repeat annotation workflows.

## Common Patterns

```bash
# 1) Scan sequences against a nucleotide HMM database
nhmmscan \
  --tblout hits.tbl \
  --cpu 8 \
  Dfam.hmm \
  genome.fa
```

```bash
# 2) Save Dfam-style output for downstream repeat annotation
nhmmscan \
  --dfamtblout dfam.tbl \
  Dfam.hmm \
  genome.fa
```

```bash
# 3) Use curated thresholds from the HMM database
nhmmscan \
  --cut_ga \
  --tblout hits.tbl \
  Dfam.hmm \
  genome.fa
```

## Recommended Workflow

1. Prepare a nucleotide HMM database, ideally pressed if you will reuse it heavily.
2. Scan the target sequence file and save a parseable output table from the start.
3. Use curated thresholds only when the source models actually provide them.
4. Interpret hits in terms of family architecture and biological context, not just best-scoring labels.

## Guardrails

- Positional argument order matters: HMM database first, sequence file second.
- Use `-h` for help; `--help` and `--version` are not valid here.
- `--dfamtblout` is only useful if your downstream tooling expects Dfam-style tabular output.
- This is a nucleotide scanner; do not point it at protein sequences or protein HMM libraries.
