---
name: hisat2
description: Use when aligning RNA-seq reads to a reference genome using graph-based indexing for fast and sensitive spliced alignment.
disable-model-invocation: true
user-invocable: true
---

# hisat2

## Quick Start
- **Command:** `hisat2 [options]* -x <ht2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hisat2`
- **Version:** 2.2.2
- **Full reference:** See [`references/help.md`](references/help.md) for complete options and usage details

## When To Use This Tool

- Splice-aware RNA-seq alignment against a HISAT2 index.
- Graph-aware alignment when splice sites, SNPs, or haplotypes are built into the index.
- A common choice for transcript assembly-oriented RNA workflows.
- Pair with `hisat2-build` when you need to create or rebuild the index.

## Common Patterns

```bash
# 1) Standard paired-end RNA-seq alignment
hisat2 \
  -x ref_index \
  -1 sample_R1.fastq.gz \
  -2 sample_R2.fastq.gz \
  -p 16 \
  -S sample.sam
```

```bash
# 2) Transcript-assembly friendly output
hisat2 \
  -x ref_index \
  -1 sample_R1.fastq.gz \
  -2 sample_R2.fastq.gz \
  --dta \
  --summary-file sample.hisat2.summary.txt \
  -S sample.sam
```

```bash
# 3) Supply known splice sites
hisat2 \
  -x ref_index \
  --known-splicesite-infile splicesites.txt \
  -U sample.fastq.gz \
  -S sample.sam
```

## Recommended Workflow

1. Build the index first, optionally including splice and exon annotation.
2. Align reads with explicit thread count and summary capture.
3. Use `--dta` when the output is headed into transcript assembly workflows.
4. Review summary statistics and splice-aware behavior before counting or assembly.

## Guardrails
- The `-x` value is the index basename, not a literal `.ht2` filename.
- `--no-spliced-alignment` is for DNA-like use cases, not ordinary RNA-seq.
- Large `-k` or `--max-seeds` values can slow alignment dramatically on repetitive genomes.
- Set `--rna-strandness` deliberately when the library is stranded; do not guess after the fact.
