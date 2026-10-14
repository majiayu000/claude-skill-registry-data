---
name: 03-deduplication
description: Delta MERGE deduplication pattern for Gold layer to prevent duplicate source key errors. Use when merging from Silver to Gold tables where Silver may contain duplicate business keys due to incremental DLT streaming, CDC patterns, SCD Type 2 tracking, or multiple batch loads. Prevents DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE errors by deduplicating before merge.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Pattern consumed by the Gold merge jobs (notebook_task); deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0"
  domain: gold
  role: worker
  pipeline_stage: 4
  pipeline_stage_name: gold-implementation
  called_by:
    - gold-layer-setup
  standalone: true
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Stable deduplication patterns
---

# Gold Layer Delta MERGE Deduplication Pattern

## Overview

Gold layer merge operations read from Silver and write to Gold using Delta MERGE. This skill standardizes the deduplication pattern required to prevent `[DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE]` errors.

## When to Use This Skill

Use this skill when:
- Merging from Silver to Gold tables
- Silver may contain duplicate business keys due to:
  - Incremental DLT streaming ingestion
  - Change Data Capture (CDC) patterns
  - Historical SCD Type 2 tracking
  - Test data generation creating duplicates
  - Multiple batch loads
- Encountering `DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE` errors

## Critical Rule: Always Deduplicate Before MERGE

**Delta MERGE operations REQUIRE unique source keys.** Multiple source rows matching the same target row causes ambiguity and fails the merge.

**Without deduplication:** MERGE fails with error:
```
[DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE] Cannot perform Merge as multiple source rows matched and attempted to modify the same target row in the Delta table in possibly conflicting ways.
```

## Standard Deduplication Pattern

### ✅ CORRECT: Deduplicate Before MERGE

```python
def merge_dim_store(spark: SparkSession, catalog: str, silver_schema: str, gold_schema: str):
    """Merge dim_store from Silver to Gold (SCD Type 2)."""
    print("Merging dim_store...")
    
    silver_table = f"{catalog}.{silver_schema}.silver_store_dim"
    gold_table = f"{catalog}.{gold_schema}.dim_store"
    
    # CRITICAL: Deduplicate Silver source before merging
    silver_raw = spark.table(silver_table)
    original_count = silver_raw.count()
    
    silver_df = (
        silver_raw
        .orderBy(col("processed_timestamp").desc())  # Order by timestamp first (latest first)
        .dropDuplicates(["store_number"])  # Keep only first occurrence per business key
    )
    
    dedupe_count = silver_df.count()
    print(f"  Deduplicated: {original_count} → {dedupe_count} records ({original_count - dedupe_count} duplicates removed)")
    
    # Prepare Gold updates
    updates_df = (
        silver_df
        .withColumn("store_key", md5(concat_ws("||", col("store_id"), col("processed_timestamp"))))
        # ... other transformations
    )
    
    # MERGE into Gold
    delta_gold = DeltaTable.forName(spark, gold_table)
    
    delta_gold.alias("target").merge(
        updates_df.alias("source"),
        "target.store_number = source.store_number AND target.is_current = true"
    ).whenMatchedUpdate(set={
        "record_updated_timestamp": "source.record_updated_timestamp"
    }).whenNotMatchedInsertAll(
    ).execute()
    
    record_count = updates_df.count()
    print(f"✓ Merged {record_count} records into dim_store")
```

### ❌ WRONG: No Deduplication

```python
# ❌ BAD: No deduplication - reads ALL Silver records including duplicates
silver_df = spark.table(silver_table)

# ❌ MERGE will fail if multiple rows have same store_number
delta_gold.alias("target").merge(
    updates_df.alias("source"),
    "target.store_number = source.store_number"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

## Key Requirements

### 1. Order by Timestamp Descending

**Always order by `processed_timestamp DESC`** before deduplication to keep the LATEST record:

```python
.orderBy(col("processed_timestamp").desc())  # Latest first
```

**Why important:**
- Ensures most recent data is kept
- Older versions are dropped
- Consistent with SCD Type 2 patterns

### 2. Match Deduplication Key to Merge Key

**CRITICAL:** The column used in `.dropDuplicates()` MUST match the column in the MERGE condition.

#### ✅ CORRECT: Keys Match

```python
# Deduplicate on product_code
silver_df = (
    silver_raw
    .orderBy(col("processed_timestamp").desc())
    .dropDuplicates(["product_code"])
)

# Merge on product_code (SAME KEY)
delta_gold.alias("target").merge(
    updates_df.alias("source"),
    "target.product_code = source.product_code"
).execute()
```

#### ❌ WRONG: Keys Don't Match

```python
# Deduplicate on upc_code
.dropDuplicates(["upc_code"])  # ❌ WRONG KEY

# Merge on product_code (DIFFERENT KEY!)
"target.product_code = source.product_code"  # Still has duplicates!
```

**Result:** MERGE still fails because multiple `upc_code` records can have the same `product_code`.

### 3. Use dropDuplicates() Not Window Functions

**Preferred approach:** `.dropDuplicates()` with ordering

```python
# ✅ SIMPLE and RELIABLE
silver_df = (
    spark.table(silver_table)
    .orderBy(col("processed_timestamp").desc())
    .dropDuplicates(["store_number"])
)
```

**Avoid:** Window functions with `row_number()` - more complex with no benefit.

### 4. Add Debug Logging

**Always log deduplication metrics** for visibility:

```python
original_count = silver_raw.count()
dedupe_count = silver_df.count()
print(f"  Deduplicated: {original_count} → {dedupe_count} records ({original_count - dedupe_count} duplicates removed)")
```

**Benefits:**
- Proves deduplication is working
- Shows magnitude of duplicate problem
- Helps troubleshoot merge failures
- Provides data quality insights

## Quick Reference

### Standard Pattern Template

```python
silver_raw = spark.table(silver_table)
original_count = silver_raw.count()

silver_df = (
    silver_raw
    .orderBy(col("processed_timestamp").desc())  # Latest first
    .dropDuplicates([business_key])  # Keep first (latest) per business key
)

dedupe_count = silver_df.count()
print(f"  Deduplicated: {original_count} → {dedupe_count} records")

# Then proceed with merge
delta_gold.alias("target").merge(
    updates_df.alias("source"),
    f"target.{business_key} = source.{business_key}"  # MUST MATCH deduplication key
).execute()
```

## Core Patterns

### Pattern 1: Simple SCD Type 1 (Overwrite)

```python
# Deduplicate on product_code (business key)
silver_df = (
    silver_raw
    .orderBy(col("processed_timestamp").desc())
    .dropDuplicates(["product_code"])
)

delta_gold.alias("target").merge(
    updates_df.alias("source"),
    "target.product_code = source.product_code"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

### Pattern 2: SCD Type 2 (Historical Tracking)

```python
# Deduplicate on store_number (business key)
silver_df = (
    silver_raw
    .orderBy(col("processed_timestamp").desc())
    .dropDuplicates(["store_number"])
)

delta_gold.alias("target").merge(
    updates_df.alias("source"),
    "target.store_number = source.store_number AND target.is_current = true"
).whenMatchedUpdate(set={
    "record_updated_timestamp": "source.record_updated_timestamp"
}).whenNotMatchedInsertAll().execute()
```

### Pattern 3: Fact Table with Aggregation

```python
# Aggregation handles deduplication, but MERGE key must be composite
daily_sales = (
    transactions
    .groupBy("store_number", "upc_code", "transaction_date")
    .agg(
        spark_sum(col("final_sales_price")).alias("net_revenue"),
        spark_sum(col("quantity_sold")).alias("net_units")
    )
)

delta_gold.alias("target").merge(
    daily_sales.alias("source"),
    """target.store_number = source.store_number 
       AND target.upc_code = source.upc_code 
       AND target.transaction_date = source.transaction_date"""
).execute()
```

See `references/dedup-patterns.md` for complete pattern examples.

## Validation Checklist

Before deploying Gold MERGE operations:

- [ ] Source data is deduplicated with `.dropDuplicates()`
- [ ] Deduplication key matches MERGE condition key
- [ ] Ordered by `processed_timestamp DESC`
- [ ] Debug logging shows deduplication metrics
- [ ] Error handling with try/except
- [ ] Success/failure messages printed
- [ ] Tested with actual Silver data containing duplicates
- [ ] MERGE condition uses correct business key

## Common Mistakes to Avoid

### ❌ Mistake 1: No Deduplication
```python
# BAD
silver_df = spark.table(silver_table)
```

### ❌ Mistake 2: Wrong Deduplication Key
```python
# BAD - Deduplicate on upc_code but merge on product_code
.dropDuplicates(["upc_code"])
# ... later ...
"target.product_code = source.product_code"
```

### ❌ Mistake 3: No Ordering
```python
# BAD - Which duplicate to keep is non-deterministic
.dropDuplicates(["store_number"])  # No orderBy!
```

### ✅ CORRECT: Simple and Reliable
```python
# GOOD
silver_df = (
    spark.table(silver_table)
    .orderBy(col("processed_timestamp").desc())
    .dropDuplicates(["store_number"])
)
```

## Performance Considerations

### 1. Deduplicate Before Transformations

Deduplicate BEFORE applying transformations to reduce compute:

```python
# ✅ GOOD - Deduplicate first, then transform
silver_df = (
    spark.table(silver_table)
    .orderBy(col("processed_timestamp").desc())
    .dropDuplicates(["store_number"])  # Reduces data size
)
updates_df = apply_transformations(silver_df)  # Works on smaller dataset
```

### 2. Partition Pruning

If Silver tables are partitioned, leverage partition pruning:

```python
silver_df = (
    spark.table(silver_table)
    .filter(col("transaction_date") >= "2025-01-01")  # Partition pruning
    .orderBy(col("processed_timestamp").desc())
    .dropDuplicates(["store_number"])
)
```

## Reference Files

- **`references/dedup-patterns.md`** - Detailed deduplication SQL patterns, generic reusable functions, complete scenario examples, and troubleshooting patterns

## Related Patterns

- **Merge Schema Validation** - See `gold/pipeline-workers/05-schema-validation` skill
- **Gold Layer Merge Patterns** - See `gold/pipeline-workers/02-merge-patterns` skill

## References

- [Delta Lake MERGE](https://docs.delta.io/latest/delta-update.html#upsert-into-a-table-using-merge) - Official documentation
- [PySpark dropDuplicates](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.dropDuplicates.html)

---

## Key Takeaway

> **Delta MERGE operations require unique source keys. ALWAYS deduplicate Silver data before merging to Gold using `.orderBy(col("processed_timestamp").desc()).dropDuplicates([business_key])` to prevent `[DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE]` errors.**

This pattern is mandatory for all Gold layer MERGE operations.

---

## Inputs

- Silver DataFrame with potential duplicates (from `spark.table(silver_table)`)
- Business key columns from YAML (`meta["business_key"]`)
- Ordering column for recency (typically `processed_timestamp`)

## Outputs

- Deduplicated DataFrame ready for MERGE (one row per business key)
- Deduplication statistics: original count, deduplicated count, duplicates removed

## Pipeline Notes to Carry Forward

- Deduplication key MUST match MERGE condition key (both from YAML `business_key`)
- Always order by `processed_timestamp` descending to keep latest record
- Run deduplication BEFORE grain validation and schema validation
- If deduplication removes 0 rows, Silver source is already clean (still run for safety)

## Next Step

Pass deduplicated DataFrame to `pipeline-workers/04-grain-validation` (for fact tables) or directly to MERGE (for dimensions).
