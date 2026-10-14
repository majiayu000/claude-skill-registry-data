---
name: 05-schema-validation
description: Runtime schema validation patterns for Gold layer merge scripts. Use when creating merge scripts to ensure DataFrame columns match target DDL schemas, validate column mappings before MERGE operations, and catch schema issues before deployment. Includes the DDL-first workflow, validate_merge_schema() helper, explicit column mapping, DDL schema reader, and pre-deployment validation script. Addresses the "three sources of truth" problem by enforcing DDL as runtime truth.
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

# Merge Schema Validation (Runtime)

## Overview

Gold layer merge scripts must align perfectly with DDL-defined schemas. Mismatches between source DataFrame columns and target table schemas cause **59% of Gold layer bugs**. This skill provides runtime validation patterns to catch schema issues before deployment.

**Key Principle:** DDL (setup script) is the **runtime source of truth**, not YAML design specifications.

**Companion skill:** For design-time cross-validation of YAML ↔ ERD ↔ Lineage, see `design-workers/07-design-validation/SKILL.md`.

## When to Use This Skill

- Creating Gold layer merge scripts (Silver → Gold)
- Ensuring DataFrame columns match target table schemas
- Validating column mappings before MERGE operations
- Debugging `UNRESOLVED_COLUMN` errors in merge operations
- Running pre-deployment schema validation

## Core Problem: Three Sources of Truth

Gold layer development involves three schema definitions:

1. **YAML Design** (`gold_layer_design/yaml/*.yaml`) - Human-readable specifications
2. **DDL Scripts** (`src/gold/setup/*.py`) - CREATE TABLE statements
3. **Merge Scripts** (`src/gold/merge/*.py`) - DataFrame transformations

**Problem:** Manual transcription between these creates mismatches.

### Common Failure Pattern

```python
# YAML Design: user_email
# DDL Script: email (renamed during implementation)
# Merge Script: .select("user_email")  # ❌ Still references old name!
# Runtime Error: [UNRESOLVED_COLUMN]
```

**Root Cause:** DDL was updated, but merge script wasn't.

## Critical Rules

### Rule 1: DDL is Runtime Source of Truth

Always develop merge scripts against **actual created tables**, not YAML designs.

**Workflow:**
```
1. YAML Design (Planning)
   ↓
2. DDL Creation (Reality) ← SOURCE OF TRUTH
   ↓
3. Run Setup Job (Create Tables)
   ↓
4. Validate Schema (Read actual table)
   ↓
5. Write Merge Script (Against actual schema)
   ↓
6. Pre-Deployment Validation (Compare DataFrame vs DDL)
```

### Rule 2: Always Validate Before Merge

Use schema validation helper before every merge operation:

```python
from helpers import validate_merge_schema

updates_df = prepare_transformations(silver_df)

validate_merge_schema(
    spark, updates_df, catalog, gold_schema, "dim_user",
    raise_on_mismatch=True
)

delta_gold.merge(updates_df, ...)
```

### Rule 3: Explicit Column Mapping

Never assume Silver column names match Gold DDL. Always use explicit mapping:

```python
updates_df = (
    silver_df
    .withColumn("store_id", col("store_number"))
    .withColumn("product_id", col("upc_code"))
    .select("store_id", "product_id", ...)
)
```

## Quick Reference

### Schema Validation Helper

```python
validate_merge_schema(
    spark: SparkSession,
    updates_df: DataFrame,
    catalog: str,
    schema: str,
    table_name: str,
    raise_on_mismatch: bool = True
) -> dict
```

Returns validation result with:
- `valid`: Boolean indicating if schemas match
- `missing_in_df`: Columns in DDL but not in DataFrame
- `extra_in_df`: Columns in DataFrame but not in DDL
- `type_mismatches`: Columns with type differences

See `references/validation-patterns.md` for complete implementation with full code examples.

### Pre-Merge Validation Checklist

Before writing any Gold merge script:

**Pre-Development:**
- [ ] Read YAML design to understand intent
- [ ] Run setup job to create actual tables
- [ ] Read DDL schema from actual table (`DESCRIBE table`)
- [ ] Document column mappings (Silver → Gold)
- [ ] Identify any renamed columns

**During Development:**
- [ ] Use explicit `.withColumn()` for all renames
- [ ] Use `.select()` with explicit column list (no `*`)
- [ ] Add comments documenting mappings
- [ ] Cast data types explicitly if DDL differs from source
- [ ] Include all DDL columns in final DataFrame

**Pre-Deployment:**
- [ ] Run schema validation helper
- [ ] Verify no extra columns in DataFrame
- [ ] Verify no missing columns from DDL
- [ ] Verify data types match DDL
- [ ] Test merge with small sample data

## Core Patterns

### Pattern 1: Schema Inspector Helper

Validate DataFrame against target table schema before merge:

```python
from helpers import validate_merge_schema

validate_merge_schema(spark, updates_df, catalog, schema, table_name)
```

**Benefits:**
- Catches mismatches before Delta merge attempt
- Clear error messages with exact column differences
- Prevents cryptic Delta errors
- Validates data types, not just column names

### Pattern 2: Explicit Column Mapping

Document and implement explicit Silver → Gold column mappings:

```python
def merge_dim_store(spark, catalog, silver_schema, gold_schema):
    """
    Column Mapping (Silver → Gold):
    - store_number → store_number (same)
    - company_rcn → company_retail_control_number (renamed)
    - processed_timestamp → record_updated_timestamp (renamed)
    """
    updates_df = (
        silver_df
        .withColumn("company_retail_control_number", col("company_rcn"))
        .withColumn("record_updated_timestamp", col("processed_timestamp"))
        .select("store_number", "company_retail_control_number", ...)
    )
```

### Pattern 3: DDL Schema Reader

Read actual table schema before writing merge script:

```python
schema = spark.table(f"{catalog}.{gold_schema}.dim_user").schema
print([field.name for field in schema.fields])

updates_df = df.select("email")  # Matches DDL, not YAML
```

## Common Mistakes to Avoid

### Mistake 1: Trusting YAML Over DDL

```python
# ❌ BAD: Using YAML-defined column name
updates_df = df.select("user_email")  # Doesn't match DDL!
```

**Fix:** Always verify against actual DDL:
```python
# ✅ GOOD: Check actual table schema first
schema = spark.table("catalog.schema.dim_user").schema
updates_df = df.select("email")
```

### Mistake 2: Implicit Column Selection

```python
# ❌ BAD: Selecting with *
updates_df = silver_df.select("*")  # Includes all Silver columns
```

**Fix:** Explicit selection:
```python
# ✅ GOOD: Only select columns that exist in Gold DDL
updates_df = silver_df.select("column1", "column2", "column3")
```

### Mistake 3: No Pre-Merge Validation

```python
# ❌ BAD: Merge without validation
delta_gold.merge(updates_df, ...)  # Fails at runtime with cryptic error
```

**Fix:** Validate first:
```python
# ✅ GOOD: Validate before merge
validate_merge_schema(spark, updates_df, catalog, schema, table_name)
delta_gold.merge(updates_df, ...)
```

## Reference Files

- **[Validation Patterns](references/validation-patterns.md)** — Complete `validate_merge_schema()` implementation, DDL schema reader, column mapping patterns, pre-merge validation workflows, error handling, and testing patterns
- **[Validation Rules](references/validation-rules.md)** — Complete schema inspector implementation with error handling
- **[Validate Schema Script](scripts/validate_schema.py)** — Pre-deployment validation script for comparing all merge DataFrames against DDL schemas

## Scripts

### validate_schema.py

Pre-deployment validation script that compares all merge DataFrames against DDL schemas. Run before `databricks bundle deploy` to catch schema mismatches.

**Usage:**
```bash
python scripts/validate_schema.py \
  jane_doe_catalog \
  dev_jane_doe_system_gold
```

See `scripts/validate_schema.py` for complete implementation.

## Related Skills

- **Design Consistency Validation (Design):** `design-workers/07-design-validation/SKILL.md` — YAML↔ERD↔Lineage cross-validation during design
- **Grain Validation:** `pipeline-workers/04-grain-validation/SKILL.md` — Pre-merge grain validation for fact tables
- **Gold Merge Deduplication:** `pipeline-workers/03-deduplication/SKILL.md` — Deduplication patterns before MERGE

## References

- [Delta Lake Merge](https://docs.delta.io/latest/delta-update.html#upsert-into-a-table-using-merge) - Official documentation
- [Rule Improvement Case Study](../../docs/reference/rule-improvement-gold-layer-debugging.md) - Complete Gold layer debugging methodology

---

**Pattern Origin:** 88 bugs across 7 Gold domains, 26% schema mismatch errors
**Key Lesson:** DDL is runtime truth, not YAML. Always validate DataFrame against actual table schema before merge.
**Impact:** Prevents 48% of schema-related bugs through pre-merge validation

---

## Inputs

- Validated DataFrame (from `pipeline-workers/04-grain-validation` or directly after deduplication for dimensions)
- Target Gold table DDL schema (read via `spark.table(gold_table).schema`)
- Gold table name from YAML (`meta["table_name"]`)

## Outputs

- Schema validation report: valid/invalid, missing columns, extra columns, type mismatches
- If valid: DataFrame is safe to MERGE
- If invalid: detailed error report with exact column differences

## Pipeline Notes to Carry Forward

- DDL is runtime source of truth — not YAML design specifications
- Missing columns in DataFrame = likely a Silver-to-Gold mapping issue
- Extra columns in DataFrame = likely forgot to `.select()` only Gold columns
- Type mismatches = may need explicit `.cast()` in column mapping

## Next Step

If schema validation passes, execute the MERGE operation. If it fails, fix column mappings and re-validate before merging.
