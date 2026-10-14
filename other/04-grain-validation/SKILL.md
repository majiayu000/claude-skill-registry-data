---
name: 04-grain-validation
description: Pre-merge grain validation patterns for Gold layer fact tables. Use when creating fact table merge scripts to validate that DataFrame grain matches DDL PRIMARY KEY, prevent transaction vs aggregated confusion, and catch grain mismatches before MERGE. Includes grain inference functions, pre-merge validation, validation SQL, and common grain mismatch errors.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Pattern consumed by the Gold merge jobs (notebook_task); deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: gold
  role: worker
  pipeline_stage: 4
  pipeline_stage_name: gold-implementation
  called_by:
    - gold-layer-setup
  standalone: true
  last_verified: "2026-02-19"
  volatility: low
  upstream_sources: []
---

# Fact Table Grain Validation (Pre-Merge)

## Overview

Gold layer merge scripts must produce DataFrames whose grain matches the DDL PRIMARY KEY. This skill provides **runtime validation patterns** to catch grain mismatches before MERGE execution, preventing costly errors and table rewrites.

**Key Principle:** DDL PRIMARY KEY reveals the grain. Merge script must match that grain.

**Companion skill:** For grain type selection during design, see `design-workers/01-grain-definition/SKILL.md`.

## When to Use This Skill

- Creating fact table merge scripts (Silver → Gold)
- Validating that DataFrame grain matches DDL PRIMARY KEY before MERGE
- Debugging `DELTA_MERGE_UNRESOLVED_EXPRESSION` or duplicate row errors
- Adding pre-merge grain validation to existing merge scripts

## Common Failure Pattern

```python
# DDL (Aggregated Grain)
CREATE TABLE fact_model_serving_inference (
  date_key INT NOT NULL,
  endpoint_key STRING NOT NULL,
  model_key STRING NOT NULL,
  request_count BIGINT,        -- ✅ Aggregated measure
  avg_latency_ms DOUBLE,       -- ✅ Aggregated measure
  error_count BIGINT,          -- ✅ Aggregated measure
  PRIMARY KEY (date_key, endpoint_key, model_key) NOT ENFORCED
)

# Merge Script (Transaction Grain - WRONG!)
def merge_fact_model_serving_inference(...):
    updates_df = (
        endpoint_usage_df
        .withColumn("request_id", col("databricks_request_id"))  # ❌ Transaction ID
        .withColumn("latency_ms", col("execution_duration_ms"))  # ❌ Single request
        .select(
            "request_id",      # ❌ Not in DDL!
            "date_key",
            "endpoint_key",
            "model_key",
            "latency_ms"       # ❌ Not aggregated
        )
    )
    
    # Merge with wrong primary key
    merge_fact_table(spark, updates_df, catalog, schema, 
                     "fact_model_serving_inference",
                     ["request_id"])  # ❌ DDL says (date_key, endpoint_key, model_key)!

# Error at Runtime:
# [DELTA_MERGE_UNRESOLVED_EXPRESSION] Cannot resolve target.request_id
```

**Root Cause:** Merge script treats aggregated fact as transaction-level fact.

## Pre-Merge Validation Pattern

Always validate grain BEFORE merge:

```python
def merge_fact_sales_daily(spark, catalog, silver_schema, gold_schema):
    """Merge daily sales with grain validation."""
    
    # Aggregate to daily grain
    daily_sales_df = transactions_df.groupBy(...).agg(...)
    
    # ✅ Validate grain BEFORE merge
    validate_fact_grain(
        spark, daily_sales_df, catalog, gold_schema,
        "fact_sales_daily",
        ["date_key", "store_key", "product_key"]
    )
    
    # Proceed with merge
    merge_fact_table(...)
```

## Common Mistakes

### ❌ Mistake 1: Aggregated DDL, Transaction Script

```python
# DDL (Aggregated)
PRIMARY KEY (date_key, endpoint_key, model_key)

# Script (Transaction - WRONG!)
updates_df = df.select("request_id", ...)  # ❌ Transaction ID
merge_fact_table(..., ["request_id"])      # ❌ Wrong grain!
```

**Fix:** Aggregate to match DDL grain:
```python
# ✅ CORRECT: Aggregate to match DDL
updates_df = (
    df
    .withColumn("date_key", date_format(col("timestamp"), "yyyyMMdd").cast("int"))
    .groupBy("date_key", "endpoint_key", "model_key")
    .agg(
        count("*").alias("request_count"),
        avg("latency_ms").alias("avg_latency_ms"),
        sum("error_count").alias("error_count")
    )
)
merge_fact_table(..., ["date_key", "endpoint_key", "model_key"])
```

### ❌ Mistake 2: Transaction DDL, Aggregated Script

```python
# DDL (Transaction)
PRIMARY KEY (query_key)

# Script (Aggregated - WRONG!)
updates_df = df.groupBy("query_key").agg(count("*"))  # ❌ Why aggregate?
merge_fact_table(..., ["query_key"])
```

**Fix:** Pass through individual records:
```python
# ✅ CORRECT: No aggregation for transaction grain
updates_df = df.select(
    "query_key",
    "execution_duration_ms",
    "rows_returned",
    "query_timestamp"
)
merge_fact_table(..., ["query_key"])
```

## Validation Checklists

### During Development
- [ ] If composite PK: use `.groupBy()` on PK columns
- [ ] If single PK: pass through individual records (no aggregation)
- [ ] Verify measures match grain (aggregated vs individual)
- [ ] Use `validate_fact_grain()` function before merge

### Pre-Deployment
- [ ] Validate PRIMARY KEY matches merge script PK
- [ ] Check for duplicate rows at grain level
- [ ] Verify measures are correctly aggregated (if needed)
- [ ] Test with sample data

### Post-Deployment
- [ ] Verify row counts match expected grain
- [ ] Check for NULL values in PRIMARY KEY columns
- [ ] Validate measures are within expected ranges
- [ ] Monitor for merge conflicts

## Reference Files

- **[Grain Validation Patterns](references/grain-validation-patterns.md)** — Complete merge script examples for transaction, aggregated, and snapshot grains with validation SQL
- **[Validate Grain Script](scripts/validate_grain.py)** — `infer_grain_from_ddl()` and `validate_fact_grain()` utilities

## Related Skills

- **Grain Definition (Design):** `design-workers/01-grain-definition/SKILL.md` — PK-grain decision tree for choosing grain during design
- **Merge Schema Validation:** `pipeline-workers/05-schema-validation/SKILL.md` — DataFrame-to-DDL column validation
- **Gold Merge Deduplication:** `pipeline-workers/03-deduplication/SKILL.md` — Deduplication patterns before MERGE

## References

- [Delta Lake Merge](https://docs.delta.io/latest/delta-update.html#upsert-into-a-table-using-merge) - Merge semantics
- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/) - Grain definition

---

**Pattern Origin:** Bug #84 (wrong fact table grain), 2% of Gold bugs but high impact
**Key Lesson:** DDL PRIMARY KEY reveals grain. Composite PK = aggregated, single PK = transaction.
**Impact:** Prevents costly table rewrites by catching grain mismatches before deployment

---

## Inputs

- Deduplicated DataFrame (from `pipeline-workers/03-deduplication`)
- PK columns from YAML (`meta["pk_columns"]`)
- Grain type from YAML (`meta["grain"]`) — transaction, aggregated, periodic snapshot, accumulating snapshot

## Outputs

- Validated DataFrame confirmed at correct grain (one row per PK combination)
- Grain validation report: duplicate count, sample duplicates if any

## Pipeline Notes to Carry Forward

- Composite PK = aggregated grain (requires `.groupBy(pk_columns).agg(...)`)
- Single PK = transaction grain (no aggregation needed)
- If grain validation fails, fix aggregation logic before proceeding to schema validation
- Grain type determines which merge pattern template to use

## Next Step

Proceed to `pipeline-workers/05-schema-validation` to validate DataFrame columns against Gold DDL before executing MERGE.
