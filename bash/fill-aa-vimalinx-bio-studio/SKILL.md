---
name: fill-aa
description: Use when filling ancestral alleles into the INFO column of VCF files using ancestral alignment data from 1000 Genomes or similar sources.
disable-model-invocation: true
user-invocable: true
---

# fill-aa

## Quick Start

- **Command**: `fill-aa [OPTIONS] < in.vcf > out.vcf`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/fill-aa`
- **Full reference**: See [references/help.md](references/help.md) for complete options and examples.

## When To Use This Tool

- Add `AA` ancestral-allele annotations to a VCF INFO column.
- Fill ancestral bases from 1000 Genomes-style ancestral FASTA files for SNPs, indels, or reference sites.
- Prepare variant datasets for analyses that need ancestral-state-aware annotations.

## Common Patterns

```bash
# 1) Annotate a sorted VCF with ancestral alleles
fill-aa -a human_ancestor_ < sorted.vcf > aa.vcf
```

```bash
# 2) Restrict filling to selected event types
fill-aa -a human_ancestor_ -t snp,indel < sorted.vcf > aa_subset.vcf
```

## Recommended Workflow

1. Prepare ancestral allele FASTA files: decompress, rename sequence headers to match chromosome names, compress with gzip (not bgzip), and index with `samtools faidx`.
2. Ensure input VCF is sorted using `vcf-sort` to avoid severe performance degradation.
3. Run `fill-aa -a <ancestral_prefix> [-t <types>] < in.vcf > out.vcf`.
4. Verify output VCF contains AA annotations in the INFO column.

## Guardrails

- Input VCF must be sorted; unsorted files cause serious performance issues.
- Ancestral allele FASTA must be gzip-compressed and indexed with `samtools faidx`.
- Sequence headers in ancestral files must use simple chromosome names (e.g., `1` or `chr1`).
- `--help` works, but `--version` is not implemented and errors as an unknown parameter.
- If the exact `-a` path does not exist, the script falls back to `<prefix><chrom>.fa.gz`, so record your naming convention carefully.
