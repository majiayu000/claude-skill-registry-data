---
name: xml2tbl
description: Use when extracting INSDSeq XML feature tables into tab-delimited text for downstream parsing or annotation review.
disable-model-invocation: true
user-invocable: true
---

# xml2tbl

## Quick Start

- Command: `cat records.xml | xml2tbl > features.tbl`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/xml2tbl`
- Reference: [references/help.md](references/help.md)

## When To Use This Tool

- Flatten INSDSeq XML feature annotations into a compact tabular view.
- Review feature intervals and qualifiers from NCBI sequence XML without writing a custom `xtract` command.
- Export a quick human-readable feature table from `efetch` XML output.

## Common Patterns

```bash
# 1) Convert INSDSeq XML into a feature table
cat records.xml | xml2tbl > features.tbl
```

```bash
# 2) Pipe efetch-style XML straight into a tabular annotation dump
efetch -db nuccore -id ABC123.1 -format gbc | xml2tbl
```

## Recommended Workflow
1. Start from INSDSeq-style XML, usually from `efetch` or a previously saved XML stream.
2. Pipe the XML into `xml2tbl`; the wrapper itself is stdin-driven.
3. Inspect the first `>Feature` block and a few qualifier lines to confirm the layout.
4. Use the resulting table for review, lightweight filtering, or export into downstream annotation tooling.

## Guardrails
- This is a fixed `xtract` recipe for `INSDSeq`, not a general XML-to-table converter.
- It does not pass through positional filenames, so stdin / pipes are the reliable invocation path.
- `xtract` must be available on `PATH`, and `--help` / `--version` just fall through to xtract-style input errors.
- Output is a feature-centric table beginning with `>Feature <accession>` lines, followed by interval and qualifier rows; downstream code should expect that layout.
