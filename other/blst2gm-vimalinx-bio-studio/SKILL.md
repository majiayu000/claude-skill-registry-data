---
name: blst2gm
description: Use when converting compatible BLAST annotation XML/ASN streams into a compact gene-markup-style table for downstream EDirect interval helpers.
disable-model-invocation: true
user-invocable: true
---

# blst2gm

## Quick Start

- **Command:** `cat blast_input.asn | blst2gm`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/blst2gm`
- **I/O shape:** reads BLAST annotation data on stdin and writes a compact tab-delimited summary

## When To Use This Tool

- Collapse compatible BLAST annotation records into a small tabular representation.
- Prepare BLAST-derived intervals for downstream helpers such as `gm2ranges` or `gm2segs`.
- Stay inside an EDirect / `xtract` pipeline instead of manually traversing `annot_E` structures.
- Filter specifically for the `BLASTN - mrna` annotation class used by this wrapper.

## Common Patterns

```bash
# 1) Convert a compatible BLAST annotation stream
cat smear.asn | blst2gm > smear.tsv
```

```bash
# 2) Feed the result into range-oriented downstream helpers
cat smear.asn | blst2gm | gm2ranges
```

```bash
# 3) Inspect the compact columns directly
cat smear.asn | blst2gm | column -ts $'\t'
```

## Recommended Workflow

1. Start from BLAST annotation data in the structure expected by the wrapper's `xtract` recipe.
2. Pipe that stream into `blst2gm` and inspect the emitted accession, score, starts, lengths, and strand fields.
3. Continue into `gm2ranges` or `gm2segs` if you need interval normalization or segment reporting.
4. Keep the original BLAST annotation source around if you may need richer metadata later.

## Guardrails

- The wrapper has no option parsing or built-in help path.
- Empty stdin fails with the underlying `xtract` error `No data supplied to xtract from stdin or file`.
- The source recipe explicitly filters for annotations labeled `BLASTN - mrna`; other BLAST types are ignored.
- Output fields are condensed with pipe-separated multi-value columns rather than expanded row-per-segment tables.
- The wrapper depends on `xtract` being on `PATH`.
