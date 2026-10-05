---
name: tabix
description: Use when you need to index or query tab-delimited genomic files for fast region-based retrieval.
disable-model-invocation: true
user-invocable: true
---

# tabix

## Quick Start
- **Command**: `tabix [OPTIONS] [FILE] [REGION [...]]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/tabix`
- **Version:** 1.22.1
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Index a sorted BGZF-compressed BED, GFF, VCF, GAF, or similar interval file for random access.
- Query one or more genomic regions without scanning the entire file.
- List contigs or print headers from an indexed genomics file.
- Use CSI instead of TBI when coordinates or contigs exceed classic tabix limits.

## Common Patterns

```bash
# 1) Index a compressed VCF with the built-in preset
tabix -p vcf variants.vcf.gz
```

```bash
# 2) Query a region and keep the header
tabix -h variants.vcf.gz chr1:100000-110000
```

```bash
# 3) Pull many regions from a BED-like list
tabix -R regions.bed variants.vcf.gz > subset.vcf
```

```bash
# 4) Build a CSI index for large references or long coordinates
tabix -C -p bed intervals.bed.gz
```

## Recommended Workflow

1. Sort the file by sequence and start coordinate, then compress it with `bgzip`.
2. Index with a preset like `-p vcf` whenever possible; fall back to explicit column settings only for custom tabular layouts.
3. Query exact regions, a regions file with `-R`, or a streaming targets file with `-T` depending on workload shape.
4. Keep the `.tbi` or `.csi` beside the data file so downstream tools can reuse the index.

## Guardrails

- Input must be BGZF-compressed, not plain gzip-compressed.
- TBI is the default, but CSI is safer for large genomes, long contigs, or coordinates beyond the classic TBI range.
- `-R` uses indexed jumps, while `-T` streams through the file; pick the right mode for the number and distribution of intervals.
- Reindex after changing the file contents; stale indexes are a common silent failure mode.
