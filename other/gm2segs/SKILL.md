---
name: gm2segs
description: Use when converting BLASTN mRNA alignment XML into segmented interval reports and strand-overlap summaries in EDirect pipelines.
disable-model-invocation: true
user-invocable: true
---

# gm2segs

CLI tool from the Entrez Direct (EDirect) suite that processes genomic map data and converts it to segment intervals. Reports counts for raw (RAW), plus strand (PLS), minus strand (MNS), and combined (CMB) intervals, detecting overlaps where both strands share coordinates.

## Quick Start

- **Command:** `PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/gm2segs -1-based < alignments.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gm2segs`
- **Full reference:** See `references/help.md` for detailed documentation

## When To Use This Tool

- Converting genomic map input to segmented interval output
- Detecting overlapping intervals between plus and minus strands
- Summarizing interval counts by strand orientation
- Piping output from other EDirect tools like `xtract`

## Common Patterns

```bash
# 1) Generate the default 1-based segment report
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/gm2segs -1-based \
  < alignments.xml
```

```bash
# 2) Emit UCSC-style coordinates instead
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/gm2segs -ucsc-based \
  < alignments.xml
```

## Recommended Workflow

1. Prepare input data from prior EDirect pipeline steps (e.g., via `xtract`)
2. Pipe data to `gm2segs` through stdin
3. Review the output interval counts for each category (RAW, PLS, MNS, CMB)
4. Use reported overlap information to identify strand conflicts or features

## Guardrails

- The script depends on several sibling EDirect helpers: `xtract`, `print-columns`, `sort-table`, and `fuse-segments` must all be on `PATH`.
- It specifically filters for alignments whose label string equals `BLASTN - mrna`.
- Output is a multi-section report (`RAW`, `PLS`, `MNS`, `CMB`), not one flat table.
- Because it reuses `fuse-segments`, empty strand partitions can still produce the bogus sentinel row `0\t0\t1`; interpret `MNS` / `PLS` sections cautiously when one strand is absent.
