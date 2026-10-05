---
name: gbf2tbl
description: Use when converting GenBank format files to table format as part of the Entrez Direct toolkit from bioconda.
disable-model-invocation: true
user-invocable: true
---

# gbf2tbl

## Quick Start

- **Command:** `gbf2tbl`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gbf2tbl`
- **Full reference:** See `references/help.md` for detailed usage and options

## When To Use This Tool

- Convert GenBank flatfiles into a feature-table view.
- Flatten GenBank annotations into the `>Feature` / interval / qualifier layout used by table-oriented downstream tools.
- Reuse the existing `gbf2xml | xml2tbl` pipeline without reconstructing it by hand.

## Common Patterns

```bash
# 1) Convert a GenBank flatfile into a feature table
gbf2tbl < records.gbf > records.tbl
```

```bash
# 2) Stream GenBank output directly into a feature-table dump
efetch -db nuccore -id TEST0001 -format gb | gbf2tbl
```

## Recommended Workflow

1. Prepare your GenBank format input file
2. Run `gbf2tbl` through stdin redirection or a pipe.
3. Inspect the first `>Feature` block and qualifier rows on a small sample.
4. Integrate results into downstream analysis or reporting

## Guardrails

- Verify input files are valid GenBank format before processing
- This wrapper is just `gbf2xml | xml2tbl`, so `transmute`, `xtract`, and the companion wrappers must be on `PATH`.
- The wrapper does not provide meaningful `--help` / `--version` output.
- Output follows the `xml2tbl` feature-table layout, beginning with `>Feature <accession>` and then interval/qualifier rows.
