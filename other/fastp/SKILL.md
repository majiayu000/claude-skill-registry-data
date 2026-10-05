---
name: fastp
description: Use when processing raw FASTQ files for quality control, adapter trimming, length or complexity filtering, polyG tail trimming, or generating QC reports before downstream analysis.
disable-model-invocation: true
user-invocable: true
---

# fastp

## Quick Start
- **Command:** `fastp`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/fastp`
- **Version:** 1.1.0
- **Full options:** see [references/help.md](references/help.md)

## When To Use This Tool

- One-stop FASTQ preprocessing before alignment or quantification.
- Adapter trimming, quality filtering, polyG/polyX trimming, and QC reporting in one run.
- Best default choice when you want both cleaned FASTQ and an HTML/JSON report.
- Prefer `cutadapt` when trimming logic needs very explicit adapter semantics or more surgical control.

## Common Patterns

```bash
# 1) Single-end QC + trimming
fastp \
  -i sample.fastq.gz \
  -o sample.clean.fastq.gz \
  -h sample.fastp.html \
  -j sample.fastp.json \
  -w 8
```

```bash
# 2) Paired-end preprocessing
fastp \
  -i sample_R1.fastq.gz \
  -I sample_R2.fastq.gz \
  -o sample_R1.clean.fastq.gz \
  -O sample_R2.clean.fastq.gz \
  -h sample.fastp.html \
  -j sample.fastp.json \
  -w 8
```

```bash
# 3) Stricter length/quality filtering
fastp \
  -i sample_R1.fastq.gz \
  -I sample_R2.fastq.gz \
  -o sample_R1.clean.fastq.gz \
  -O sample_R2.clean.fastq.gz \
  -q 20 -u 20 -n 3 -l 50 \
  -h sample.fastp.html \
  -j sample.fastp.json
```

## Recommended Workflow

1. Decide single-end vs paired-end first, because output wiring differs.
2. Run one conservative preprocessing pass that emits both cleaned reads and QC reports.
3. Review the HTML or JSON summary before aligning, especially read retention, adapter content, and quality trimming extent.
4. Keep the chosen thresholds stable across the cohort unless there is a documented reason to split processing.

## Guardrails

- Always set explicit outputs for both mates in paired-end mode.
- `--disable_adapter_trimming` is rarely what you want unless reads are known to be pre-trimmed.
- PolyG trimming is useful for some Illumina platforms; do not disable it blindly if you see artificial G tails.
- Use `--dont_overwrite` in production runs to avoid clobbering previous preprocessing outputs.
