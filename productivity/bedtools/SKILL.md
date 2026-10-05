---
name: bedtools
description: Use when performing genome arithmetic on interval files (BED, BAM, BEDGRAPH), including intersection, merging, coverage, format conversion, or sequence extraction.
disable-model-invocation: true
user-invocable: true
---

# bedtools

## Quick Start
- **Command:** `bedtools <subcommand> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bedtools`
- **Version:** 2.31.1
- **Full reference:** See [`references/help.md`](references/help.md) for complete subcommand list and options

## When To Use This Tool

- Perform interval arithmetic on BED/BAM/BEDGRAPH/GFF-like genomic coordinates.
- This is the default tool for overlap, merge, coverage, complement, and FASTA extraction tasks.
- Use it whenever the job is fundamentally about genomic intervals rather than alignments or variants.
- Choose the subcommand first; `bedtools` is a toolbox, not one operation.

## Common Patterns

```bash
# 1) Intersect peaks with genes
bedtools intersect -a peaks.bed -b genes.bed > peaks_in_genes.bed
```

```bash
# 2) Merge overlapping intervals
bedtools merge -i intervals.sorted.bed > intervals.merged.bed
```

```bash
# 3) Compute coverage of intervals by alignments
bedtools coverage -a targets.bed -b sample.sorted.bam > targets.coverage.tsv
```

```bash
# 4) Extract sequences from a reference FASTA
bedtools getfasta -fi genome.fa -bed regions.bed -fo regions.fa
```

## Recommended Workflow

1. Make sure coordinate systems, chromosome names, and genome assembly all match.
2. Sort interval inputs whenever the subcommand expects sorted data.
3. Pick the specific subcommand that matches the biological question.
4. Validate output shape and coordinate sanity before chaining into another tool.

## Guardrails

- BEDTools assumes interval semantics are correct; mixed assemblies or `chr` naming mismatches will silently distort results.
- Many operations behave best or only correctly with sorted input.
- Some interval-manipulation subcommands need a genome file for chromosome lengths.
- Always check subcommand-specific help, because required flags differ substantially across subcommands.
