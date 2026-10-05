---
name: fastqc
description: Use when you need to perform quality control analysis on high-throughput sequencing data (fastq, bam, sam, or fast5 files) to identify potential problems before downstream analysis.
disable-model-invocation: true
user-invocable: true
---

# fastqc

## Quick Start
- **Command:** `fastqc [options] seqfile1 seqfile2 .. seqfileN`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/fastqc`
- **Version:** 0.12.1
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Inspect raw or cleaned sequencing reads before downstream analysis.
- Generate per-sample QC reports for FASTQ, BAM, SAM, or FAST5 inputs.
- Use it before trimming and again after trimming if you want a before/after QC comparison.
- Pair it with `multiqc` when handling many samples.

## Common Patterns

```bash
# 1) QC two FASTQ files
fastqc -o fastqc_out sample_R1.fastq.gz sample_R2.fastq.gz
```

```bash
# 2) Run several files with multiple threads
fastqc -t 8 -o fastqc_out *.fastq.gz
```

```bash
# 3) Keep only zipped output package
fastqc --noextract -o fastqc_out sample.fastq.gz
```

## Recommended Workflow

1. Run FastQC on representative raw reads before trimming.
2. Inspect the HTML report for adapter content, per-base quality, sequence duplication, and overrepresented sequences.
3. If trimming or filtering is applied, rerun FastQC on cleaned reads.
4. Aggregate all sample reports with `multiqc` for cohort-level review.

## Guardrails

- The output directory must already exist; FastQC does not create it for you.
- Each thread needs roughly a few hundred MB of RAM; oversubscribing threads is counterproductive.
- `--nogroup` can produce huge plots and unstable behavior on long reads.
- A warning flag in FastQC is not automatically a fatal problem; interpret modules in context of assay type and library prep.
