---
name: bwa
description: Use when aligning low-divergence DNA sequence reads to a reference genome
disable-model-invocation: true
user-invocable: true
---

# bwa

## Quick Start
- **Command:** `bwa`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bwa`
- **Version:** 0.7.19-r1273
- **Reference:** See [references/help.md](references/help.md) for detailed usage

## When To Use This Tool

- Align low-divergence DNA sequencing reads to a reference genome.
- Use `bwa index` to build the reference index and `bwa mem` for modern short-read alignment.
- Good default for WGS, targeted DNA-seq, and many standard Illumina DNA workflows.
- If unsure which BWA algorithm to use, `bwa mem` is the normal starting point.

## Common Patterns

```bash
# 1) Build the BWA index
bwa index reference.fa
```

```bash
# 2) Paired-end alignment with read group
bwa mem \
  -t 16 \
  -R '@RG\tID:sample1\tSM:sample1\tPL:ILLUMINA' \
  reference.fa \
  sample_R1.fastq.gz sample_R2.fastq.gz \
  > sample.sam
```

```bash
# 3) Single-end alignment
bwa mem \
  -t 8 \
  reference.fa \
  sample.fastq.gz \
  > sample.sam
```

## Recommended Workflow

1. Build the BWA index from the exact reference FASTA used for the project.
2. Align with `bwa mem`, usually with explicit `-t` and a correct read-group line.
3. Convert, sort, and index the SAM/BAM output with `samtools`.
4. Check mapping rate and duplicate behavior before variant calling or coverage analysis.

## Guardrails

- `bwa` is a dispatcher; `bwa --help` is not the interface you want, while `bwa`, `bwa mem`, and `bwa index` are.
- `bwa mem` expects an indexed reference; forgetting `bwa index` is a common failure mode.
- Add an `@RG` line for any workflow that will later merge BAMs or call variants.
- The usual output is SAM to stdout; redirect it explicitly or pipe it into downstream tools.
