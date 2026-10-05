---
name: star
description: Use when aligning spliced RNA-seq reads to a reference genome, generating genome indices, or performing splice-aware alignment for transcriptome analysis.
disable-model-invocation: true
user-invocable: true
---

# star

## Quick Start
- **Command:** `STAR`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/STAR`
- **Version:** 2.7.11b
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Bulk RNA-seq or other splice-aware alignment against a genome index.
- One-time genome index generation before repeated RNA-seq alignments.
- Recovering splice junction evidence from `SJ.out.tab` and alignment QC from `Log.final.out`.
- Prefer `STAR` over `subread-align` when intron-spanning alignment is the main job.

## Common Patterns

```bash
# 1) Build a STAR genome index once per reference/annotation pair
STAR \
  --runMode genomeGenerate \
  --runThreadN 16 \
  --genomeDir star_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --sjdbOverhang 149
```

```bash
# 2) Align paired-end gzipped RNA-seq reads and emit sorted BAM
STAR \
  --runThreadN 16 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --outFileNamePrefix sample.
```

```bash
# 3) Add simple gene-level quantification during alignment
STAR \
  --runThreadN 16 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --quantMode GeneCounts \
  --outFileNamePrefix sample.
```

## Recommended Workflow
1. Build the index once with the exact genome FASTA and annotation you plan to quantify against.
2. Align reads with `--genomeDir`, `--readFilesIn`, and `--readFilesCommand zcat` for gzipped FASTQ.
3. Inspect `Log.final.out`, `SJ.out.tab`, and BAM size before moving into counting.
4. Count with `featureCounts` or another quantifier using the same annotation build.

## Guardrails
- `--genomeFastaFiles` for genome generation must be plain-text FASTA, not gzipped FASTA.
- Set `--sjdbOverhang` to read length minus 1 for the library you are aligning.
- For small genomes, scale down `--genomeSAindexNbases` as documented in `references/help.md`.
- Keep chromosome naming consistent across FASTA, GTF, and downstream BAM-aware tools.
