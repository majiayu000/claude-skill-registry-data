---
name: optimizing-pyspark-jobs
description: Optimize slow or failing PySpark and Spark SQL jobs — partitioning and repartitioning, data skew, shuffles, broadcast joins, caching, Adaptive Query Execution, and avoiding driver collects and Python UDFs. Use when a Spark job is slow, spills, OOMs, has skewed tasks, runs a huge shuffle, or a stage hangs on a few straggler tasks.
---

# Optimizing PySpark Jobs

## When to use

- A Spark/PySpark job is slow, spills to disk, or OOMs (driver or executor).
- One or a few tasks straggle while the rest finish (skew).
- Huge shuffles, wide stages, or exploding output.
- Do NOT use for pure SQL warehouse tuning (use `optimizing-sql-queries`).

## Workflow

```
- [ ] Read the Spark UI: find the slow stage and its shuffle/skew
- [ ] Confirm the cause: skew, too many/few partitions, wide shuffle, or driver pull
- [ ] Fix joins (broadcast small side; salt skewed keys)
- [ ] Right-size partitions; enable AQE
- [ ] Re-run and compare stage time/shuffle bytes
```

1. **Read the Spark UI** (Stages/SQL tab). Find the stage dominating wall-clock;
   look at shuffle read/write and the task-duration distribution (a long tail =
   skew).
2. **Diagnose** the dominant cause before changing config.
3. **Fix joins first** — broadcast the small side; handle skewed keys.
4. **Right-size partitions** and let Adaptive Query Execution coalesce them.
5. **Re-measure** in the UI; confirm shuffle bytes / stage time dropped.

## Patterns

**Broadcast the small side** to avoid a shuffle join:

```python
from pyspark.sql.functions import broadcast
fact.join(broadcast(small_dim), "dim_id")
```

**Enable Adaptive Query Execution** (coalesces partitions, converts to broadcast,
handles skew automatically):

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

**Salt a skewed join key** when one key value dominates (AQE off or extreme skew):
add a random suffix to the hot key on both sides so it spreads across tasks.

**Right-size partitions** — aim for ~128MB per partition. Use `repartition(n)` to
increase parallelism before a wide operation; use `coalesce(n)` to reduce small
output files without a shuffle.

**Cache only reused DataFrames**, and unpersist when done:

```python
df.cache(); df.count()   # materialize once if used multiple times
...
df.unpersist()
```

## Common pitfalls

- **`collect()` / `toPandas()` on large data** — pulls everything to the driver
  and OOMs it. Aggregate first, or write to storage.
- **Python UDFs in hot paths** — serialize row-by-row; use built-in/SQL functions,
  or pandas/vectorized UDFs when unavoidable.
- **Default 200 shuffle partitions** on big or tiny data — too few causes spills,
  too many causes overhead; enable AQE or set
  `spark.sql.shuffle.partitions` to fit the data.
- **`repartition()` when `coalesce()` suffices** — `repartition` forces a full
  shuffle; use `coalesce` to only shrink partition count.
- **Ignoring skew** — a few straggler tasks dominate runtime; salt or use AQE
  skew join.
- **Caching everything** — wastes memory and forces eviction; cache only reused
  frames.
- **Many small output files** — `coalesce` before write or use adaptive
  file sizing.
