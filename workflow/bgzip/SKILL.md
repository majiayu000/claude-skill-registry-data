---
name: bgzip
description: Use when you need to compress or decompress files using BGZF (Blocked GNU Zip Format), create BGZF indexes for random access, or prepare bioinformatics files for tabix indexing.
disable-model-invocation: true
user-invocable: true
---

# bgzip

Block compression utility from htslib that creates BGZF-compressed files suitable for random access and indexing.

## Quick Start

- **Command:** `bgzip [OPTIONS] [FILE]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bgzip`
- **Version:** 1.22.1
- **Full reference:** See [references/help.md](references/help.md) for complete options and usage

## When To Use This Tool

- Compress tabular genomics files into BGZF rather than ordinary gzip.
- Prepare files for random access and indexing in the HTS ecosystem.
- Reindex or integrity-check an existing BGZF file.
- Use it before `tabix` or other tools that require BGZF-aware random access.

## Common Patterns

```bash
# 1) Compress and create a BGZF index
bgzip -i variants.vcf
```

```bash
# 2) Write compressed output while preserving the original file
bgzip -c variants.vcf > variants.vcf.gz
```

```bash
# 3) Reindex an existing BGZF file
bgzip -r variants.vcf.gz
```

```bash
# 4) Test file integrity
bgzip -t variants.vcf.gz
```

## Recommended Workflow

1. Use BGZF, not generic gzip, for files that must support random access.
2. Create or refresh `.gzi` indexes when the compressed file changes.
3. Test integrity before feeding compressed files into downstream indexing or querying steps.
4. Keep compression and indexing steps explicit in pipelines.

## Guardrails

- BGZF is gzip-compatible for decompression but not interchangeable with ordinary gzip for random-access workflows.
- `-i` creates a `.gzi` during compression; `-r` rebuilds the index later.
- `-c` writes to stdout and keeps the input file unchanged.
- Threading with `-@` is useful for bigger files, but remember that downstream tools still need the final `.gzi` or tabix index.
