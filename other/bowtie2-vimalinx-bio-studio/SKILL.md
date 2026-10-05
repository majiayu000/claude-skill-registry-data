---
name: bowtie2
description: Use when aligning short reads to a reference genome or indexed sequence database. Suitable for mapping FASTQ/FASTA reads in paired-end or single-end mode to produce SAM output.
disable-model-invocation: true
user-invocable: true
---

# bowtie2

## Quick Start
- **Command:** `bowtie2 -x <bt2-idx> -1 <m1> -2 <m2> -S <sam>` or `bowtie2 -x <bt2-idx> -U <r> -S <sam>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2`
- **Version:** 2.5.5
- **Full reference:** See [references/help.md](references/help.md) for complete options and flags

## When To Use This Tool

- Align short reads to a Bowtie2 index.
- Use for DNA or transcriptome-like short-read mapping where Bowtie2 behavior is already established in the workflow.
- Prefer Bowtie2 presets over micromanaging seed parameters on the first pass.
- Pair with `bowtie2-build` when the reference index still needs to be created.

## Common Patterns

```bash
# 1) Paired-end end-to-end alignment
bowtie2 \
  -x ref_index \
  -1 sample_R1.fastq.gz \
  -2 sample_R2.fastq.gz \
  -p 16 \
  -S sample.sam
```

```bash
# 2) More sensitive local alignment
bowtie2 \
  --very-sensitive-local \
  -x ref_index \
  -U sample.fastq.gz \
  -p 8 \
  -S sample.sam
```

```bash
# 3) Interleaved input
bowtie2 \
  -x ref_index \
  --interleaved sample.interleaved.fastq.gz \
  -S sample.sam
```

## Recommended Workflow

1. Build the index once with `bowtie2-build`.
2. Choose single-end, paired-end, interleaved, or BAM input mode explicitly.
3. Start with preset sensitivity options and only tune lower-level parameters if needed.
4. Convert and sort downstream with `samtools`, then review alignment summaries from stderr.

## Guardrails

- Bowtie 1 and Bowtie 2 indexes are not compatible.
- `-k` and especially `-a` change reporting semantics; MAPQ becomes less interpretable in multi-hit reporting modes.
- `--local` allows soft clipping; use it intentionally rather than by habit.
- SAM output defaults to stdout, so `-S` or shell redirection should be explicit.
