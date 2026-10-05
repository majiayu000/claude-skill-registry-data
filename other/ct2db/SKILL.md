---
name: ct2db
description: Use when converting RNA connectivity-table (`.ct`) files into extended FASTA with dot-bracket structures, optionally removing pseudoknots or modified bases.
disable-model-invocation: true
user-invocable: true
---

# ct2db

## Quick Start

- **Command:** `ct2db [options] input.ct ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/ct2db`
- **Version observed locally:** `1.0`
- **Help:** `ct2db -h`

## When To Use This Tool

- Convert Zuker-style `.ct` connectivity tables into dot-bracket notation.
- Turn RNA structure files into an extended FASTA representation for downstream tools.
- Remove pseudoknots or normalize modified bases during conversion.
- Batch-convert one or more `.ct` files with a single command.

## Common Patterns

```bash
# 1) Basic conversion
ct2db structure.ct > structure.db.fa
```

```bash
# 2) Remove pseudoknots during conversion
ct2db --no-pk structure.ct > structure_no_pk.db.fa
```

```bash
# 3) Override the FASTA header
ct2db --fasta-header sample_01 structure.ct > sample_01.db.fa
```

## Recommended Workflow

1. Confirm the input really is a `.ct` connectivity-table file.
2. Decide whether you need pseudoknot removal or replacement of modified bases before export.
3. Convert to extended FASTA and inspect both the sequence and dot-bracket lines.
4. Keep the original `.ct` file if you will need richer connectivity information later.

## Guardrails

- `ct2db` writes converted sequences to stdout.
- Help and version are available as `-h` / `--help` and `-V` / `--version`.
- `--filename-suffix` defaults to removing `.ct` when deriving FASTA headers from filenames.
- `--no-pk` removes pseudoknots, which can change structure interpretation for downstream analyses.
- `--no-modified` replaces non-canonical nucleotides with `N`.
