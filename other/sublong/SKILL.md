---
name: sublong
description: Use when aligning long FASTQ reads to a reference genome with Subread's long-read aligner, optionally in RNA-seq mode.
disable-model-invocation: true
user-invocable: true
---

# sublong

## Quick Start

- **Command:** `sublong -i <index_name> -r <input.fastq> -o <output.bam>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/sublong`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Aligning long reads (e.g., PacBio, Oxford Nanopore) to a reference genome
- Mapping reads against a full Subread index with a single block
- Producing BAM or SAM output for downstream analysis
- RNA-seq mode alignment via the `-X` flag

## Common Patterns

```bash
# Align long genomic reads and write BAM output
sublong -i long_index -r long_reads.fastq.gz -o long_reads.bam -T 8
```

```bash
# Run in long-read RNA-seq mode
sublong -i transcriptome_index -r isoform_reads.fastq.gz -o isoform_reads.bam -X -T 8
```

```bash
# Emit SAM instead of BAM
sublong -i long_index -r long_reads.fastq.gz -o long_reads.sam --SAMoutput
```

## Recommended Workflow

1. Build a full one-block Subread index first, usually via `subread-buildindex -F -B`.
2. Prepare long reads in FASTQ or gzipped FASTQ format.
3. Decide whether you want standard genomic alignment or RNA-seq mode with `-X`.
4. Run `sublong` with an explicit output file and thread count.
5. Validate the BAM or SAM output before downstream quantification, QC, or variant analysis.

## Guardrails

- The index must be a full index with exactly one block; multi-block indexes are not supported
- Input must be FASTQ or gzipped FASTQ; other formats are not accepted
- Default output is BAM; use `--SAMoutput` explicitly if SAM format is required
- `-h` is not a true help switch here. Local testing shows `--help` and `--version` both print usage text and then complain about the unrecognized option; `-v` is the real version flag.
- `-o` is mandatory for `sublong`; unlike some other Subread tools, output is not optional.
- `-X` switches on RNA-seq mode but does not replace the need for an index compatible with the same reference build you expect downstream.
