---
name: dqx-patterns
description: Databricks DQX framework patterns for advanced data quality validation with detailed failure insights and flexible quarantine strategies. Use when implementing Silver/Gold layer validation, needing richer diagnostics than DLT expectations, or requiring pre-merge validation with detailed failure tracking. Supports YAML configuration, Delta table storage, and serverless compute compatibility.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "DQX validation runs as a serverless job/pipeline step; deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  dqx_version: ">=0.16.0"
  domain: silver
  role: worker
  pipeline_stage: 2
  pipeline_stage_name: silver
  called_by:
    - silver-layer-setup
  standalone: true
  dependencies:
    - databricks-python-imports
    - databricks-asset-bundles
  last_verified: "2026-08-30"
  volatility: medium
  upstream_sources: []  # DQX is from databrickslabs (databrickslabs/dqx), not the databricks-agent-skills registry
---
# DQX Data Quality Framework Patterns

## Overview

DQX is a Python-based data quality framework from Databricks Labs that validates PySpark DataFrames with richer diagnostics than standard DLT expectations. This skill provides production-grade patterns for integrating DQX into medallion architecture pipelines.

**Recommended Version:** `>=0.16.0` (float support, outlier detection, JSON validation, AI-assisted rules, plus the newer checks and behavior changes shipped in 0.13–0.16 — see "Breaking Changes Since 0.12.0" below)

**Key Benefits:**
- Detailed diagnostic information (`_error`, `_warning` columns)
- Flexible quarantine strategies (drop, mark, split)
- Dataset-level checks (uniqueness, foreign keys, outliers, aggregations)
- YAML/JSON/Delta/Lakebase check storage with governance
- Auto-profiling and AI-assisted rule generation (0.10.0+)
- Summary metrics for quality tracking over time (0.10.0+)

## Quick Start (3-4 hours for pilot)

**Goal:** Add DQX diagnostics to one Silver table without disrupting existing DLT expectations.

**What You'll Create:**
1. Quality rules YAML file
2. DQX-enhanced Silver DLT pipeline (valid + quarantine tables)
3. Diagnostic queries for failure analysis

**Fast Track:**

```python
# 1. Install DQX in notebook
%pip install databricks-labs-dqx>=0.16.0
dbutils.library.restartPython()

# 2. Define checks as dicts
checks = [
    {"name": "id_not_null", "criticality": "error",
     "check": {"function": "is_not_null", "arguments": {"column": "id"}}},
    {"name": "non_negative_amount", "criticality": "error",
     "check": {"function": "is_not_less_than", "arguments": {"column": "amount", "limit": 0}}},
]

# 3. Apply and split
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient

dq_engine = DQEngine(WorkspaceClient())
valid_df, invalid_df = dq_engine.apply_checks_by_metadata_and_split(input_df, checks)

# 4. Write results
valid_df.write.saveAsTable("catalog.schema.silver_valid")
invalid_df.write.saveAsTable("catalog.schema.silver_quarantine")
```

**See:** `references/implementation-roadmap.md` for full phased rollout guide.

## When to Use This Skill

### Use DQX When:
- Need detailed diagnostic information on why checks fail
- Want auto-profiling to suggest quality rules (`DQXProfiler`)
- Need flexible quarantine strategies (drop, mark, split)
- Require dataset-level checks (unique, foreign key, outlier, aggregation)
- Want centralized quality check storage (Delta, Lakebase, UC Volume)
- Need quality metrics tracking over time (summary metrics)

### Continue with Standard DLT Expectations When:
- Current DLT expectations + Lakehouse Monitoring are sufficient
- Don't need granular failure diagnostics
- Want to minimize external dependencies
- Simple pass/fail validation is adequate

## Quick Reference

### Installation

**Serverless Jobs:** Environment-level dependencies
```yaml
environments:
  - environment_key: default
    spec:
      dependencies:
        - "databricks-labs-dqx>=0.16.0"
```

**DLT Pipelines:** Pipeline-level library
```yaml
libraries:
  - pypi:
      package: databricks-labs-dqx>=0.16.0
```

### API Method Selection

**For dict/YAML checks (metadata):**
```python
valid_df, invalid_df = dq_engine.apply_checks_by_metadata_and_split(df, checks)
```

**For DQRowRule/DQDatasetRule objects (code):**
```python
valid_df, invalid_df = dq_engine.apply_checks_and_split(df, checks)
```

**For DLT/Lakeflow (view + get_valid/get_invalid):**
```python
@dlt.view
def dq_check():
    return dq_engine.apply_checks_by_metadata(dlt.read_stream("bronze"), checks)

@dlt.table
def silver():
    return dq_engine.get_valid(dlt.read_stream("dq_check"))

@dlt.table
def quarantine():
    return dq_engine.get_invalid(dlt.read_stream("dq_check"))
```

## Critical Rules

### 1. Function Names (Verified against 0.16.0 API)

**Reference:** [DQX Check Functions API](https://databrickslabs.github.io/dqx/docs/reference/api/check_funcs/)

| Use Case | Correct Function | Parameter | Wrong Names |
|----------|-----------------|-----------|-------------|
| Column >= value | `is_not_less_than` | `limit` | ~~is_greater_than_or_equal_to~~ |
| Column <= value | `is_not_greater_than` | `limit` | ~~is_less_than_or_equal_to~~ |
| Column == value | `is_equal_to` | **`value`** | (uses `value`, NOT `limit`) |
| Column != value | `is_not_equal_to` | **`value`** | |
| min <= col <= max | `is_in_range` | `min_limit`, `max_limit` | ~~is_between~~ |
| Column in list | `is_in_list` | `allowed` | ~~is_in~~, ~~is_in_values~~ |
| Column NOT in list | `is_not_in_list` | `forbidden` | |

> **⚠️ 0.16.0 breaking change — `is_in_list` / `is_not_in_list` values are column expressions.**
> Since 0.16.0 the `allowed` / `forbidden` entries resolve as **column expressions**, not bare literals. A bare string is treated as a **column reference**; string *literals* must be single-quoted (`"'ACTIVE'"`) or wrapped with `F.lit("ACTIVE")`. Numeric and ISO-date strings are parsed as numbers/dates. Example: `allowed=["'ACTIVE'", "'CLOSED'"]` (not `allowed=["ACTIVE", "CLOSED"]`, which now looks for columns named `ACTIVE`/`CLOSED`).
| Unique values | `is_unique` | `columns` (list) | ~~has_unique_key~~, ~~has_no_duplicate_values~~ |
| Strict > or < | `sql_expression` | `expression` | ~~is_greater_than~~, ~~is_less_than~~ |

**There is no `is_greater_than` or `is_less_than` function.** Use `sql_expression` for strict comparisons.

### 2. Parameter Names (Strict - wrong names cause errors)

| Function Type | Correct Parameter | Wrong Names |
|--------------|------------------|-------------|
| Comparison | `limit` | `value`, `threshold` |
| Equality | `value` | `limit` |
| Range | `min_limit` / `max_limit` | `min_value` / `max_value` |
| List | `allowed` | `values` |
| Not-in-list | `forbidden` | `values` |
| Regex | `regex` | `pattern` |

### 3. Data Types

- **Float support (since 0.12.0):** `limit`, `min_limit`, `max_limit` accept floats. The old integer-only restriction was a pre-0.12.0 constraint and is now historical.
- **Recommendation:** Use integers for clarity; floats when precision needed

### 4. Spark Connect Compatibility (Serverless)

```python
# WRONG - Fails on serverless
current_user = spark.sparkContext.sparkUser()

# CORRECT
current_user = spark.sql("SELECT current_user() as user").collect()[0]["user"]
```

### 5. Check Storage (use official save_checks/load_checks)

```python
from databricks.labs.dqx.config import TableChecksStorageConfig

# Save checks to Delta table
dq_engine.save_checks(checks, config=TableChecksStorageConfig(
    location="catalog.schema.dqx_checks",
    run_config_name="silver_transactions",
    mode="overwrite"  # be explicit: the default changed to "append" (with rule versioning) in newer DQX
))
```

> **Note (save-mode default changed):** newer DQX releases default the Delta/Lakebase checks-storage save mode to **`append`** (with rule versioning) rather than `overwrite`. Always set `mode=` explicitly so a re-run doesn't silently accumulate duplicate rule rows.

## Core Patterns

### Pattern 1: DLT/Lakeflow Integration

```python
import dlt
dq_engine = DQEngine(WorkspaceClient())

@dlt.view
def dq_check():
    return dq_engine.apply_checks_by_metadata(dlt.read_stream("bronze"), checks)

@dlt.table(name="silver_valid", ...)
def silver_valid():
    return dq_engine.get_valid(dlt.read_stream("dq_check"))

@dlt.table(name="silver_quarantine", ...)
def silver_quarantine():
    return dq_engine.get_invalid(dlt.read_stream("dq_check"))
```

**See:** `references/integration-guide.md` for all 6 integration patterns

### Pattern 2: Gold Layer Pre-Merge Validation

```python
from dqx_gold_checks import apply_dqx_validation

daily_sales = transactions.groupBy(...).agg(...)

valid_sales, invalid_sales, stats = apply_dqx_validation(
    spark=spark, df=daily_sales, catalog=catalog,
    schema=gold_schema, entity="fact_sales_daily"
)

if stats["invalid"] > 0:
    invalid_sales.write.saveAsTable(quarantine_table)

delta_gold.alias("target").merge(valid_sales.alias("source"), ...).execute()
```

**See:** `references/integration-guide.md` Pattern 3 for complete implementation

### Pattern 3: YAML Configuration

```yaml
- name: non_negative_revenue
  criticality: error
  check:
    function: is_not_less_than
    arguments:
      column: net_revenue
      limit: 0
  metadata:
    business_rule: "Revenue cannot be negative"
    failure_impact: "Critical - Invalid financial reporting"
```

**See:** `references/rule-patterns.md` for all rule definition patterns

## Requirements Template

Before integrating DQX, fill in the requirements template to define scope, strategy, and team readiness.

**See:** `references/requirements-template.md`

## Phased Implementation

DQX integration follows a 3-phase approach:
1. **Phase 1:** Silver layer pilot (3-4 hours)
2. **Phase 2:** Delta table check storage (1-2 hours)
3. **Phase 3:** Gold layer pre-merge validation (2-3 hours)

**See:** `references/implementation-roadmap.md` for detailed steps, success metrics, and rollback plans.

## Reference Files

### Configuration and API
- **`references/dqx-configuration.md`** - Complete 0.16.0 API reference: all check functions, parameter names, DQEngine methods, version compatibility, common errors

### Rule Definition Patterns
- **`references/rule-patterns.md`** - YAML declarative, Python programmatic, dataset-level (FK, outlier, aggregation), Delta storage, rich metadata, custom functions

### Integration Patterns
- **`references/integration-guide.md`** - DLT/Lakeflow, hybrid DLT+DQX, Gold pre-merge, foreachBatch streaming, multi-table, end-to-end, DQX vs DLT comparison

### Implementation Guide
- **`references/implementation-roadmap.md`** - 3-phase rollout (Silver pilot → Delta storage → Gold validation), architecture diagrams, success metrics, rollback plans, best practices

### Requirements
- **`references/requirements-template.md`** - Fill-in-the-blank requirements, integration strategy selection, team readiness checklist, version decision matrix

## Scripts

- **`scripts/setup_dqx.py`** - Creates DQX quality checks Delta table and loads initial checks using `DQEngine.save_checks()`.

```bash
python scripts/setup_dqx.py --catalog <catalog> --schema <schema>
python scripts/setup_dqx.py --catalog <catalog> --schema <schema> \
    --checks-yaml path/to/checks.yml --run-config-name silver_transactions
```

## Templates

- **`assets/templates/dqx-rules.yaml`** - Template YAML with examples for every check category: null, comparison, range, equality, list, SQL expression, regex, freshness, date, uniqueness, foreign key, aggregation.

## Validation Checklist

### Check Definitions
- [ ] All function names match [DQX API docs](https://databrickslabs.github.io/dqx/docs/reference/api/check_funcs/)
- [ ] Parameter names correct per function (`limit` vs `value` vs `allowed` vs `forbidden`)
- [ ] No `is_greater_than` or `is_less_than` (use `sql_expression` for strict comparisons)
- [ ] Metadata includes business context (`business_rule`, `failure_impact`)
- [ ] Critical checks use `criticality: error`; warnings use `criticality: warn`

### Code Implementation
- [ ] Using `apply_checks_by_metadata*` for dict/YAML checks
- [ ] Using `apply_checks*` for DQRowRule/DQDatasetRule objects
- [ ] DLT pattern uses `get_valid()`/`get_invalid()` helper methods
- [ ] Spark Connect-compatible APIs (no `sparkContext`)
- [ ] Check storage uses `dq_engine.save_checks()` / `load_checks()`
- [ ] Quarantine tables created for invalid records
- [ ] Only valid records are merged into Gold
- [ ] Shared code is pure Python (no `# Databricks notebook source` header)

### Workflow Configuration
- [ ] DQX library at environment level for serverless jobs
- [ ] DQX library in `libraries:` block for DLT pipelines
- [ ] Proper task dependencies configured
- [ ] Version pinned appropriately (production: `==0.16.0`, dev: `>=0.16.0`)
- [ ] `is_in_list` / `is_not_in_list` literals quoted as column expressions (`"'ACTIVE'"`, not `"ACTIVE"`) — 0.16.0 breaking change
- [ ] `save_checks` `mode=` set explicitly (default changed to `append`)

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `function 'is_greater_than' is not defined` | Function doesn't exist | Use `is_not_less_than` (>=) or `sql_expression` (>) |
| `Unexpected argument 'value'` | Wrong parameter name | Use `limit` (not `value`) for comparison functions |
| `Use 'apply_checks_by_metadata_and_split'` | Wrong API method for dict checks | Use `*_by_metadata*` methods |
| `Libraries field is not supported for serverless` | Task-level library | Move to `environments[].spec.dependencies` |
| `sparkContext is not supported in Spark Connect` | JVM API on serverless | Use SQL queries |
| `ModuleNotFoundError` | Notebook header in shared code | Remove `# Databricks notebook source` |
| `Argument 'limit' should be of type 'int'` | Float on DQX < 0.12.0 (historical) | Use integers or upgrade to >= 0.16.0 (floats supported since 0.12.0) |
| `is_in_list`/`is_not_in_list` matches a column instead of a literal | 0.16.0 resolves `allowed`/`forbidden` as column expressions | Quote literals: `"'ACTIVE'"` or `F.lit("ACTIVE")` |

**See:** `references/dqx-configuration.md` for detailed error solutions

## Breaking Changes Since 0.12.0

The skill was last pinned to 0.12.0; 0.13–0.16 shipped since. When bumping to `>=0.16.0`, review:

1. **`is_in_list` / `is_not_in_list` value resolution (breaking).** `allowed` / `forbidden` entries are now **column expressions**. Bare strings resolve as column references; string literals must be single-quoted (`"'ACTIVE'"`) or `F.lit(...)`; numeric/ISO-date strings parse as numbers/dates.
2. **Default checks-storage save mode → `append` (with rule versioning).** Previously `overwrite`. Set `mode=` explicitly on `save_checks(...)`.
3. **New checks available (0.13–0.16, optional):** `is_valid_email`, `is_valid_uuid`, ISO code checks, `has_no_gaps_per_time_window`, `aggr_matches_dataset`, `has_no_outliers`, and the ML-assisted `has_no_row_anomalies`.

**Authoritative source:** [DQX CHANGELOG](https://github.com/databrickslabs/dqx/blob/main/CHANGELOG.md).

## References

### Official Documentation
- [DQX GitHub Repository](https://github.com/databrickslabs/dqx)
- [DQX Check Functions API](https://databrickslabs.github.io/dqx/docs/reference/api/check_funcs/)
- [DQX User Guide](https://databrickslabs.github.io/dqx/docs/guide/)
- [DQX Applying Checks Guide](https://databrickslabs.github.io/dqx/docs/guide/quality_checks_apply/)
- [DQX Installation Guide](https://databrickslabs.github.io/dqx/docs/installation/)
- [DQX CHANGELOG](https://github.com/databrickslabs/dqx/blob/main/CHANGELOG.md)

### Related Skills
- `dlt-expectations-patterns` - DLT expectations patterns (complementary)
- `databricks-python-imports` - Pure Python module patterns (critical for DQX file structure)
- `databricks-asset-bundles` - Serverless configuration patterns

## Version History

- **2026-08-30** — Bumped recommended DQX version from `>=0.12.0` to `>=0.16.0` across the skill and reference files. Documented the 0.16.0 breaking change where `is_in_list`/`is_not_in_list` `allowed`/`forbidden` values resolve as column expressions (string literals must be quoted) and the checks-storage default save mode change to `append`. Quoted literals in `is_in_list` examples; added a "Breaking Changes Since 0.12.0" section and 0.13–0.16 check inventory. Bumped `last_verified`.
