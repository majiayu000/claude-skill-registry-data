---
name: multiqc
description: Use when you need to aggregate quality control reports from multiple bioinformatics tools into a single HTML report
disable-model-invocation: true
user-invocable: true
---

# multiqc

## Quick Start
- **Command:** `multiqc [OPTIONS] [ANALYSIS DIRECTORY]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/multiqc`
- **Version:** 1.33
- **Full reference:** See `references/help.md` for complete options and usage

## When To Use This Tool

- Aggregate many per-sample QC or analysis reports into one HTML dashboard.
- Summarize outputs from FastQC, cutadapt, aligners, quantifiers, and many other tools.
- Use it after per-sample processing is done, not as a first-pass QC tool.
- Best for cohort-level review and sample-to-sample comparison.

## Common Patterns

```bash
# 1) Scan the current analysis directory
multiqc .
```

```bash
# 2) Write report into a dedicated output directory
multiqc results -o multiqc_out -n project_multiqc.html
```

```bash
# 3) Limit or exclude modules
multiqc results -m fastqc -m cutadapt -e star
```

```bash
# 4) Prefix sample names with directory names to reduce collisions
multiqc results -d
```

## Recommended Workflow

1. Run per-sample QC and analysis tools first.
2. Point MultiQC at the project results tree or a curated file list.
3. Review sample naming, module detection, and missing-module warnings before trusting the report.
4. Archive the HTML plus parsed data directory if the summary will be cited or shared.

## Guardrails

- MultiQC only summarizes logs it recognizes; if upstream tools did not emit report files, there is nothing to aggregate.
- Re-running in the same output location often needs `-f/--force`.
- Sample name collisions can silently confuse interpretation; use `-d`, `-s`, or renaming options when needed.
- If the report looks suspiciously sparse, check whether modules were excluded or whether files were ignored by glob patterns.
