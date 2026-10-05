---
name: subjunc
description: Use when aligning RNA-seq reads to a reference genome with junction detection, including exon-exon junctions and gene fusions.
disable-model-invocation: true
user-invocable: true
---

# subjunc

## Quick Start

- **Command:** `subjunc -i <index> -r <reads> -o <output.bam>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/subjunc`
- **Version:** 2.1.1
- **Full options:** See [references/help.md](references/help.md) for complete argument reference

## When To Use This Tool

- Align RNA-seq reads when exon-exon junction detection matters.
- Prefer `subjunc` over `subread-align` for splice-aware RNA workflows.
- Detect canonical and non-canonical junctions, and optionally broader junction/fusion events.
- Produce BAM output that can go straight into `featureCounts` or visual inspection.

## Common Patterns

```bash
# 1) Standard paired-end RNA-seq alignment
subjunc \
  -i ref_index \
  -r sample_R1.fastq.gz \
  -R sample_R2.fastq.gz \
  -o sample.bam \
  -T 8
```

```bash
# 2) Coordinate-sorted BAM for downstream browsing/counting
subjunc \
  -i ref_index \
  -r sample_R1.fastq.gz \
  -R sample_R2.fastq.gz \
  -o sample.bam \
  -T 8 \
  --sortReadsByCoordinates
```

```bash
# 3) Broader junction discovery, including non-canonical events
subjunc \
  -i ref_index \
  -r sample_R1.fastq.gz \
  -R sample_R2.fastq.gz \
  -o sample.bam \
  -T 8 \
  --allJunctions
```

## Recommended Workflow

1. Build a Subread index once and reuse it across the cohort.
2. Run `subjunc` on RNA-seq FASTQ with paired-end information if available.
3. Sort output if downstream tools or browsers expect coordinate order.
4. Count with `featureCounts` and inspect suspicious junction-rich loci separately.

## Guardrails

- `-i` expects the pre-built index basename, not the original FASTA file.
- `subjunc` is RNA-oriented; use `subread-align -t 1` for ordinary genomic DNA alignment.
- The default `-m 1` is permissive; tighten thresholds if false junctions become a problem.
- The default maximum indel length is 5 bp; raise `-I` when longer indels are biologically expected.
- `--allJunctions` expands reporting scope and can increase noisy findings, so use it deliberately.
