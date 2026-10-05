---
name: map-bed
description: Use when you need to apply aggregation functions (sum, mean, count, etc.) to values from overlapping intervals in one file and map them onto intervals from another file.
disable-model-invocation: true
user-invocable: true
---

# map-bed

## Quick Start
- **Command:** `mapBed -a A.bed -b B.bed -c <B_col> -o <op> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/mapBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Aggregate values from overlapping B intervals onto each A interval.
- Summarize signal tracks, counts, names, or scores across target intervals.
- Attach mean, sum, min, max, count, or distinct summaries to an interval set.
- Constrain which overlaps contribute with strand or reciprocal-overlap rules.

## Common Patterns

```bash
# 1) Mean signal from B column 5 over each A interval
mapBed \
  -a exons.bed \
  -b signal.bed \
  -c 5 \
  -o mean
```

```bash
# 2) Count distinct overlapping labels
mapBed \
  -a peaks.bed \
  -b annotations.bed \
  -c 4 \
  -o count_distinct
```

```bash
# 3) Map multiple B columns with matching operations
mapBed \
  -a peaks.bed \
  -b signal.bed \
  -c 4,5 \
  -o distinct,mean
```

## Recommended Workflow

1. Sort both files by chromosome and start coordinate before running `mapBed`.
2. Decide which B columns carry the statistic you actually want to summarize.
3. Choose aggregation operators that match the column type: numeric ops for numeric columns, `collapse` / `distinct` for labels.
4. Add `-s`, `-S`, `-f`, `-F`, `-r`, or `-e` only if overlap eligibility needs to be biologically constrained.

## Guardrails

- Both inputs must be sorted by chromosome then start.
- `-c` refers to columns in B, not A.
- If you provide multiple `-c` columns and multiple `-o` operators, the counts must align unless you intentionally rely on the single-column / single-op broadcast behavior.
- `collapse` keeps duplicates whereas `distinct` removes them.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.
