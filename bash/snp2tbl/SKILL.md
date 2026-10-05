---
name: snp2tbl
description: Use when converting NCBI dbSNP docsum XML into flat tabular rows through the bundled `snp2hgvs | hgvs2spdi | spdi2tbl` pipeline.
disable-model-invocation: true
user-invocable: true
---

# snp2tbl

Thin bash pipeline wrapper. It does not parse SNP XML directly by itself; instead it sends dbSNP docsum XML through `snp2hgvs`, forwards any CLI arguments to `hgvs2spdi`, and then flattens the result with `spdi2tbl`.

## Quick Start

- **Command:** `efetch -db snp -id <rsid> -format docsum | snp2tbl`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/snp2tbl`
- **Internal pipeline:** `snp2hgvs | hgvs2spdi "$@" | spdi2tbl`

## When To Use This Tool

- Turning dbSNP docsum XML into one tabular row per reported variant representation
- Flattening rsID-derived HGVS/SPDI information for downstream filtering or spreadsheets
- Staying inside the Entrez Direct shell-tool ecosystem instead of writing custom XML transforms
- Passing conversion-related flags onward to `hgvs2spdi` while keeping a one-command wrapper

## Common Patterns

```bash
# Convert one rsID into tabular rows
efetch -db snp -id 104894914 -format docsum | snp2tbl
```

```bash
# Convert multiple rsIDs in one stream
efetch -db snp -id 104894914,104894915 -format docsum | snp2tbl
```

```bash
# Forward additional arguments to hgvs2spdi
efetch -db snp -id 104894914 -format docsum | snp2tbl <hgvs2spdi-args>
```

## Recommended Workflow

1. Fetch dbSNP records in `-format docsum`.
2. Pipe them into `snp2tbl` and inspect the emitted tabular rows.
3. If needed, pass only arguments that `hgvs2spdi` understands, because this wrapper forwards its own argv there.
4. Capture the resulting table for downstream joins, filtering, or export.

## Guardrails

- `-h` is not a safe help path. In local testing it was forwarded downstream and triggered `cat: invalid option -- 'h'` plus an `xtract` no-input error.
- `--version` is also not implemented as wrapper metadata; with no input it fell through to the same no-data failure class.
- The wrapper depends on `snp2hgvs`, `hgvs2spdi`, and `spdi2tbl` all being available on `PATH`.
- In live testing on rs104894914, the output contained rows shaped like `rs104894914  NC_000023.11  154191715  T  C  Genomic  Substitution  OPN1MW`.
- Because the first stage is `snp2hgvs`, this wrapper expects the same dbSNP docsum XML input that `snp2hgvs` expects; it is not a generic tabularizer for arbitrary SNP XML.
