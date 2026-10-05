---
name: gff2gff
description: Use when a GFF file needs bcftools/csq-compatible gene and transcript attributes before consequence annotation.
disable-model-invocation: true
user-invocable: true
---

# gff2gff

## Quick Start

- **Command:** `zcat in.gff.gz | /home/vimalinx/miniforge3/envs/bio/bin/gff2gff | gzip -c > out.gff.gz`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gff2gff`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Fix GFF attributes so `bcftools csq` can recognize genes and transcripts more reliably.
- Add missing `ID`, `biotype`, and `Name` fields when equivalent source attributes such as `gene_id`, `gene_type`, `gene_name`, `transcript_id`, or `transcript_type` are present.
- Keep an otherwise-streaming bcftools workflow by reading from stdin and writing normalized GFF to stdout.

## Common Patterns

```bash
# 1) Normalize a compressed GFF before bcftools/csq
zcat in.gff.gz | \
  /home/vimalinx/miniforge3/envs/bio/bin/gff2gff | \
  gzip -c > out.gff.gz
```

```bash
# 2) Run verbosely to inspect warnings while capturing fixed output
cat input.gff | \
  /home/vimalinx/miniforge3/envs/bio/bin/gff2gff -v \
  > fixed.gff \
  2> gff2gff.log
```

## Recommended Workflow

1. Start from the same GFF you plan to feed into `bcftools csq`, not from an already manually edited copy.
2. Run `gff2gff` in a pipe and capture stdout explicitly into a new file.
3. Check stderr for the final "Fixed N records" summary and any warnings about records it could not repair.
4. Test the normalized file with a small `bcftools csq` run before using it across a whole cohort.

## Guardrails

- This is a stdin-to-stdout filter; it does not accept positional input or output filenames.
- `-h`, `-?`, and `--help` work, but `--version` is treated as an unknown parameter.
- Even successful runs print a repair summary to stderr; capture logs separately from the normalized GFF stream.
- The script is narrowly aimed at `bcftools csq` compatibility, not broad GFF3 validation or arbitrary format conversion.
