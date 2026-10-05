---
name: roh-viz
description: Use when turning `bcftools roh` output plus a VCF/BCF into an interactive HTML visualization of ROH segments and homozygosity rates.
disable-model-invocation: true
user-invocable: true
---

# roh-viz

Perl HTML report generator for ROH review. It parses `RG` segments from `bcftools roh` output, queries alt-genotype calls from the supplied VCF/BCF with `bcftools query`, then renders an HTML/JavaScript report with optional embedded D3/Pako assets.

## Quick Start

- **Command:** `roh-viz -i roh.txt -v cohort.bcf -o output.html`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/roh-viz`
- **Required companions:** `bcftools`, `bash`, `zless`

## When To Use This Tool

- Reviewing runs of homozygosity from `bcftools roh` in a browser instead of raw text
- Combining ROH segments with homozygosity-rate traces derived from the source VCF/BCF
- Filtering the visualization by samples, regions, or minimum ROH length
- Generating a self-contained offline HTML report with embedded JavaScript assets

## Common Patterns

```bash
# Basic ROH visualization
bcftools roh --AF-dflt 0.5 -G 30 -Or -o roh.txt cohort.bcf
roh-viz -i roh.txt -v cohort.bcf -o roh.html
```

```bash
# Embed JavaScript for offline viewing
roh-viz -i roh.txt -v cohort.bcf -e 1 -o roh_offline.html
```

```bash
# Restrict to selected samples and regions
roh-viz -i roh.txt -v cohort.bcf -s sample1,sample2 -r chr1,chr2 -l 500000 -o subset.html
```

## Recommended Workflow

1. Generate `bcftools roh` output first, then keep the original VCF/BCF available for genotype-rate calculation.
2. Feed the ROH text through `-i` and the variant file through `-v`.
3. Tune `-l`, `-s`, and `-r` to reduce clutter before sharing the report.
4. Use `-e 1` whenever the final HTML must work without internet access.

## Guardrails

- The real ROH-input flag is `-i`, not `-r`. Source inspection shows `-r` means genomic regions, but the built-in error message and example text incorrectly say `Missing the -r option` / `roh-viz -r roh.txt ...`.
- Both `-i` and `-v` are required by the parser.
- The script shells out to `bcftools query` and `zless`, so those tools must be available on `PATH`.
- Only `RG` lines from the ROH file are plotted as ROH segments; other record types are ignored.
- If `-o` is omitted, the script writes HTML to stdout.
- By default it links D3/Pako from remote URLs; use `-e 1` to embed those assets for offline viewing.
