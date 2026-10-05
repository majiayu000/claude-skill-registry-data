---
name: seqtk
description: Use when doing lightweight FASTA/FASTQ transformations such as conversion, subsampling, subsequence extraction, trimming, or quick QC with seqtk.
disable-model-invocation: true
user-invocable: true
---

# seqtk

## Quick Start
- **Command:** `seqtk <subcommand> ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/seqtk`
- **Version:** 1.5-r133
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert FASTQ to FASTA or normalize sequence formatting quickly.
- Subsample reads, extract named intervals or records, and perform quick read trimming.
- Run lightweight QC summaries without pulling in a larger workflow engine.
- Prefer `seqtk` for small, surgical sequence manipulations rather than full-blown alignment or variant tooling.

## Common Patterns

```bash
# 1) Convert FASTQ to FASTA
seqtk seq -A reads.fq.gz > reads.fa
```

```bash
# 2) Subsample reads reproducibly
seqtk sample -s100 reads.fq.gz 100000 > reads.subset.fq
```

```bash
# 3) Extract named regions or sequences
seqtk subseq genome.fa regions.bed > subset.fa
```

```bash
# 4) Trim low-quality FASTQ ends
seqtk trimfq reads.fq.gz > reads.trimmed.fq
```

## Recommended Workflow

1. Pick the exact subcommand first: `seq` for format conversion, `sample` for downsampling, `subseq` for extraction, `trimfq` for simple trimming, or `fqchk` for quick QC.
2. Treat `seqtk` as a stream-oriented filter and redirect output explicitly.
3. Use a fixed sampling seed when you need reproducible subsets.
4. Validate output record counts or names before feeding the result into heavier downstream tools.

## Guardrails

- `seqtk` does not use global `--help` or `--version` flags; run it without arguments or use the specific subcommand help patterns instead.
- Most subcommands write to stdout by default, so forgetting redirection can make pipelines look like they succeeded without leaving files behind.
- `subseq` is convenient, but if you only need a few genomic intervals from a large indexed FASTA, `samtools faidx` may be a better fit.
- For paired-end subsampling, keep mate handling and random seed strategy consistent across both files.
