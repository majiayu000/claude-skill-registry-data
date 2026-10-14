---
name: adhoc-exploration-notebooks
description: Create dual-format ad-hoc exploration notebooks for Databricks workspace (.py) and local Jupyter (.ipynb) with Databricks Connect. Use when building data exploration tools, debugging data quality issues, or creating interactive analysis notebooks. Supports widget fallback patterns, helper functions for table discovery, and proper Spark session initialization for both environments.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "The local-Jupyter path (Databricks Connect + profile-based CLI auth) is the IDE/local branch only. On Genie Code there is no local toolchain: explore directly in the workspace on serverless compute (pre-authenticated — no profile setup, no local Connect session), and deploy the exploration job via `bundle deploy --target dev` + `bundle run` through runDatabricksCli (see `skills/genie-code-environment`). On Genie Code, write generated notebooks under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`), not a bare relative path — relative paths resolve against the page CWD (§8)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  domain: exploration
  role: utility
  standalone: true
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Internal notebook patterns
---
# Ad-Hoc Exploration Notebook Patterns

## Overview

Every data product should include exploration notebooks in **two formats** to support different development workflows: Databricks workspace format (`.py`) for interactive use in Databricks UI, and Jupyter format (`.ipynb`) for local development with Databricks Connect. Magic commands (`%pip`, `%sql`, `dbutils.library.restartPython()`) only work in Databricks workspace, not with Databricks Connect or local execution.

## Quick Start (30 minutes)

**Goal:** Create interactive notebooks for data exploration (works both in Databricks and locally).

**What You'll Create:**
1. `adhoc_exploration.py` — Databricks workspace version (with magic commands)
2. `adhoc_exploration.ipynb` — Local Jupyter version (Databricks Connect)
3. Standard helper functions (list tables, explore, check quality, compare, show properties)

**Before You Begin:** Fill in the [Requirements Template](assets/templates/requirements-template.md) with your catalog, schemas, and key tables.

### Fast Track: Databricks Workspace

```python
# 1. Upload adhoc_exploration.py to Databricks workspace
# 2. Run setup cells (installs databricks-sdk)
# 3. Use helper functions:

list_tables(catalog, "my_schema")
explore_table(catalog, "my_schema", "fact_sales_daily")
check_data_quality(catalog, "my_schema", "fact_sales_daily")
compare_tables(catalog, "silver_schema", "silver_transactions",
               catalog, "gold_schema", "fact_sales_daily")
```

### Fast Track: Local Jupyter

```bash
# 1. Install requirements
pip install -r requirements.txt

# 2. Configure Databricks Connect — authenticate per PRE-REQUISITES §11 (IDE/CLI only; Genie Code skips this path — see callout below)

# 3. Launch Jupyter and open adhoc_exploration.ipynb
jupyter lab
```

> **Genie Code:** there is no local toolchain — skip the Jupyter / Databricks Connect path and explore directly in the workspace on serverless compute (pre-authenticated). Write generated notebooks under the cloned repo root (`{REPO_ROOT}`), never `/tmp`. See `skills/genie-code-environment` §8–§9.

**Key Differences:**
- **Databricks (.py):** Uses magic commands (`%pip`, `%sql`), `dbutils.widgets.text()` for params
- **Local (.ipynb):** Pure Python, direct variable assignment, requires Databricks Connect

## When to Use This Skill

- Building data exploration tools for Bronze/Silver/Gold layers
- Debugging data quality issues
- Creating interactive analysis notebooks
- Validating schema changes
- Testing query patterns before production
- Testing Metric Views and monitoring tables
- Cross-layer data flow validation (Bronze → Silver → Gold)

## Critical Rules

### 1. Dual-Format Requirement

**CRITICAL:** Create both `.py` (Databricks workspace) and `.ipynb` (local Jupyter) formats.

**Why:** Magic commands (`%pip`, `%sql`, `dbutils.library.restartPython()`) only work in Databricks workspace, not with Databricks Connect.

### 2. Spark Session Initialization

**CRITICAL:** Must specify either `.serverless()` or `.clusterId()` — default will fail:

```python
# ✅ CORRECT
spark = DatabricksSession.builder.serverless().profile("profile").getOrCreate()
# OR
spark = DatabricksSession.builder.clusterId("cluster-id").getOrCreate()

# ❌ WRONG
spark = DatabricksSession.builder.getOrCreate()  # Exception: Cluster id or serverless required
```

### 3. Widget Fallback Pattern

Always use widget fallback pattern for cross-environment compatibility:

```python
# Default values
catalog = "default_catalog"

# Try widgets (Databricks workspace), fall back to defaults
try:
    dbutils.widgets.text("catalog", catalog, "Catalog")
    catalog = dbutils.widgets.get("catalog")
except Exception:
    # Widgets not available (Databricks Connect)
    pass
```

## Quick Reference

### File Structure

```
src/exploration/
├── adhoc_exploration.py              # Databricks workspace format
├── adhoc_exploration.ipynb           # Local Jupyter format
├── requirements.txt                  # Python dependencies
├── README.md                         # Full documentation
└── QUICKSTART.md                     # 5-minute setup guide
```

### Standard Helper Functions

Every exploration notebook should include:

1. **Table Discovery:** `list_tables(catalog_name, schema_name)` — List all tables with metadata
2. **Table Exploration:** `explore_table(catalog_name, schema_name, table_name, limit)` — Schema + sample data + row count
3. **Data Quality:** `check_data_quality(catalog_name, schema_name, table_name)` — Null counts, duplicates
4. **Comparison:** `compare_tables(catalog1, schema1, table1, catalog2, schema2, table2)` — Compare across layers
5. **Governance:** `show_table_properties(catalog_name, schema_name, table_name)` — View metadata, tags, TBLPROPERTIES

See [Notebook Patterns](references/notebook-patterns.md) for complete implementations.

## Core Patterns

### Databricks Workspace Format (.py)

**Key Features:**
- `# Databricks notebook source` header
- `# COMMAND ----------` cell separators
- `# MAGIC %md` for markdown cells
- Widget support with fallback pattern
- Magic commands work (`%pip`, `%sql`)

See [Notebook Patterns](references/notebook-patterns.md) for complete template.

### Local Jupyter Format (.ipynb)

**Key Features:**
- Standard Jupyter notebook format
- No Databricks-specific headers
- No magic commands
- Direct variable assignment (no widgets)
- Setup instructions in markdown cell

**Requirements:**
```txt
databricks-sdk[notebook]>=0.28.0
pyspark>=3.5.0
```

### Multiple Execution Options

#### Option 1: Run via Databricks UI
1. Open the notebook in Databricks workspace
2. Attach to a cluster
3. Adjust widget parameters if needed
4. Run cells interactively

#### Option 2: Run via Asset Bundle

**Critical:** Include `.py` extension in notebook path:

```yaml
notebook_task:
  notebook_path: ../src/exploration/adhoc_exploration.py  # ✅ Include .py extension
  base_parameters:
    catalog: ${var.catalog}
```

> **Client note:** IDE runs these in a terminal; Genie Code runs the `databricks bundle …` commands via `runDatabricksCli` (be on the bundle's page; generated files anchor to `{REPO_ROOT}`). See `skills/genie-code-environment`.

```bash
# Deploy and run
databricks bundle deploy -t dev
databricks bundle run -t dev adhoc_exploration_job
```

See [Notebook Patterns](references/notebook-patterns.md) for complete YAML example.

#### Option 3: Direct Execution via %run

```python
# In any Databricks notebook, import and use the functions:
%run ./exploration/adhoc_exploration

# Then use the helper functions
list_tables(catalog, bronze_schema)
df = explore_table(catalog, gold_schema, "fact_sales_daily")
```

## Common Mistakes to Avoid

### ❌ Mistake 1: Missing .serverless() or .clusterId()
```python
# ❌ DON'T: Use default builder
spark = DatabricksSession.builder.getOrCreate()
# Exception: Cluster id or serverless are required
```

### ✅ Correct: Specify execution environment
```python
spark = DatabricksSession.builder.serverless().profile("profile").getOrCreate()
```

### ❌ Mistake 2: Forgetting File Extension in Bundle
```yaml
# ❌ DON'T: Omit .py extension
notebook_path: ../src/exploration/adhoc_exploration
# Error: notebook not found
```

### ✅ Correct: Include .py extension
```yaml
notebook_path: ../src/exploration/adhoc_exploration.py
```

### ❌ Mistake 3: Using Magic Commands Locally
```python
# ❌ DON'T: Use magic commands
%pip install 'databricks-sdk[notebook]'
# SyntaxError: invalid syntax
```

### ✅ Correct: Install packages before running
```bash
pip install -r requirements.txt
```

## Validation Checklist

### File Structure
- [ ] Both `.py` and `.ipynb` formats created
- [ ] `requirements.txt` with dependencies
- [ ] README.md with full documentation
- [ ] QUICKSTART.md with 5-minute setup

### .py File (Databricks Workspace)
- [ ] Has `# Databricks notebook source` header
- [ ] Uses `# COMMAND ----------` cell separators
- [ ] Markdown cells use `# MAGIC %md`
- [ ] Initializes Spark with `.serverless()` or `.clusterId()`
- [ ] Uses widget fallback pattern
- [ ] All helper functions defined

### .ipynb File (Local Jupyter)
- [ ] Standard Jupyter notebook format
- [ ] No Databricks-specific headers
- [ ] No magic commands
- [ ] Direct variable assignment (no widgets)
- [ ] Setup instructions in markdown cell
- [ ] Same helper functions as .py

### Helper Functions
- [ ] `list_tables()` — Table discovery
- [ ] `explore_table()` — Schema + samples
- [ ] `check_data_quality()` — DQ checks
- [ ] `compare_tables()` — Layer comparison
- [ ] `show_table_properties()` — Governance metadata

## Reference Files

### Notebook Patterns
[references/notebook-patterns.md](references/notebook-patterns.md) — Complete code patterns for both `.py` and `.ipynb` formats, helper function implementations, widget fallback patterns, Spark session initialization, dev/prod configuration, `%run` import patterns, and Asset Bundle integration.

### Analysis Workflows
[references/analysis-workflows.md](references/analysis-workflows.md) — Step-by-step analysis workflows for data discovery, data quality investigation, schema validation, Metric View testing, monitoring metrics review, and cross-layer comparison.

### Tips & Troubleshooting
[references/tips-and-troubleshooting.md](references/tips-and-troubleshooting.md) — Visualization tips, summary statistics, performance analysis, extending notebooks with custom functions and matplotlib/plotly, troubleshooting common errors (table not found, permission denied, slow queries, connection issues), and best practices.

## Assets

### Exploration Notebook Template
[assets/templates/exploration-notebook.py](assets/templates/exploration-notebook.py) — Starter notebook template with all standard helper functions and widget fallback patterns.

### Requirements Template
[assets/templates/requirements-template.md](assets/templates/requirements-template.md) — Fill-in-the-blank planning template for catalog configuration, environment settings, tables to explore, DQ focus areas, and cross-layer comparisons.

## References

### Official Databricks Documentation
- [Databricks Connect](https://docs.databricks.com/dev-tools/databricks-connect.html)
- [Databricks Notebooks](https://docs.databricks.com/notebooks/)
- [Databricks SDK for Python](https://databricks-sdk-py.readthedocs.io/)

### Related Patterns
- [Databricks Asset Bundles](skills/databricks-asset-bundles/SKILL.md) — Deployment patterns
- [Python File Imports](../common/databricks-python-imports/SKILL.md) — Sharing code between notebooks
- [DLT Expectations](../silver/dlt-expectations-patterns/SKILL.md) — DQ rules and validation
- [Metric Views](../semantic-layer/metric-views-patterns/SKILL.md) — Metric View testing patterns
- [Observability Setup](../monitoring/00-observability-setup/SKILL.md) — Monitoring table patterns
