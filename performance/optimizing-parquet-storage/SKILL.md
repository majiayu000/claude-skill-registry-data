---
name: optimizing-parquet-storage
description: Optimize columnar Parquet storage for analytics — file and row-group sizing, compression codecs (Snappy/ZSTD), partitioning and file layout, column pruning and predicate pushdown, dictionary encoding, and fixing the small-files problem. Use when Parquet reads are slow or costly, files are too small/large, choosing compression or partitioning, or improving scan pruning on a data lake.
---

# Optimizing Parquet Storage

## When to use

- Parquet/lake reads are slow or scan too much data.
- Files are too small (many tiny files) or too large (poor parallelism).
- Choosing compression, row-group size, or partition layout.
- Do NOT use for warehouse-native storage tuning (use the warehouse skills).

## Workflow

```
- [ ] Target ~128MB-1GB files and ~128MB row groups
- [ ] Partition by common filter columns (low/medium cardinality)
- [ ] Sort within files by a filter column to tighten min/max pruning
- [ ] Pick compression: Snappy (speed) or ZSTD (ratio)
- [ ] Compact small files; select only needed columns
```

1. **Right-size files and row groups.** Aim for ~128MB–1GB files and ~128MB row
   groups so engines get efficient parallelism and pruning. Tiny files kill
   performance via per-file overhead.
2. **Partition on filter columns** of low/medium cardinality (date, region). Avoid
   high-cardinality partitioning (user_id) — it creates millions of tiny files.
3. **Sort within files** by a frequently filtered column so Parquet's per-row-group
   min/max stats enable predicate pushdown (data skipping).
4. **Compression:** Snappy for hot, latency-sensitive data; ZSTD for better ratio
   and cheaper storage at similar read speed.
5. **Read fewer columns** — the biggest columnar win is column pruning.

## Patterns

**Write well-sized, sorted Parquet (Spark):**

```python
(df.sort("ordered_at")                       # tighten row-group min/max for pushdown
   .repartition(1, "region")                 # control file count per partition
   .write.partitionBy("region")
   .option("compression", "zstd")
   .parquet("s3://lake/orders/"))
```

**Predicate pushdown** — filtering on the sorted/partition column lets the reader
skip row groups and partitions entirely, reading far fewer bytes.

**Compact small files** — periodically read a partition and rewrite it into a few
large files (or use a table format's compaction) to fix the small-files problem
from streaming/frequent appends.

## Common pitfalls

- **Small-files problem** — frequent small appends create thousands of tiny files;
  compact on a schedule.
- **High-cardinality partitioning** — partitioning by id/timestamp-to-the-second
  explodes file count; partition coarsely, sort finely.
- **No sorting** — unsorted files have wide row-group min/max, so pushdown skips
  nothing.
- **`SELECT *` on wide tables** — reads every column's bytes; project only needed
  columns.
- **Row groups too small/large** — too small loses compression/pushdown efficiency,
  too large hurts parallelism and memory.
- **Gzip for analytics** — slow to decode; prefer Snappy or ZSTD.
