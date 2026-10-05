---
name: fill-fs
description: Use when annotating VCF files with flanking sequence information (INFO/FS tag) or masking regions/variants in flanking sequences.
disable-model-invocation: true
user-invocable: true
---

# fill-fs

## Quick Start

- **Command**: `fill-fs [OPTIONS] file.vcf`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/fill-fs`
- **Full reference**: See [references/help.md](references/help.md) for complete options and examples

## When To Use This Tool

- Annotate VCF records with flanking sequence in `INFO/FS`.
- Mask known variants or BED regions out of the flanks before downstream primer/probe design.
- Lowercase or replace masked sequence context to make nearby-conflict regions obvious.
- Self-mask clustered nearby variants with `-c` when local variant density matters.

## Common Patterns

```bash
# 1) Add 100-bp flanking sequence around each variant
fill-fs -r ref.fa.gz variants.vcf > variants.fs.vcf
```

```bash
# 2) Mask known variants and BED regions, lowercasing the BED masks
fill-fs \
  -r ref.fa.gz \
  -v known.vcf.gz \
  -m lc -b mask.bed.gz \
  variants.vcf > masked.fs.vcf
```

```bash
# 3) Self-mask clustered nearby variants within 20 bp
fill-fs -r ref.fa.gz -c 20 variants.vcf > clustered.fs.vcf
```

## Recommended Workflow

1. Prepare a tabix-indexed reference sequence file (required for flanking sequence extraction)
2. Optionally prepare tabix-indexed VCF or BED files for masking known variants or regions
3. Run `fill-fs` with appropriate masking options (`-v`, `-b`, `-c`) and flanking length (`-l`)
4. Validate the output VCF contains the expected INFO/FS annotations

## Guardrails

- Requires a reference sequence file (`-r`) to extract flanking sequences
- Masking files (VCF/BED) must be tabix-indexed before use
- `-m` only affects the next `-b`, `-v`, or `-c` target and must appear before that argument to take effect.
- Multiallelic sites are reduced to the first ALT allele when constructing the `FS` annotation.
- `--help` works, but `--version` is not implemented and errors as an unknown parameter.
