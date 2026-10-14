---
name: 01-yaml-table-setup
description: Patterns for creating Gold layer tables dynamically from YAML schema definitions at runtime. Use when managing 10+ Gold layer tables across multiple domains, when schema evolves frequently, or when you want to avoid embedded SQL DDL strings in Python. Includes YAML schema structure, setup script implementation, Asset Bundle configuration, and workflow patterns for schema changes.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Pattern consumed by the Gold table-setup/merge jobs (notebook_task); deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code)."
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
  upstream_sources: []  # Internal YAML-driven approach
---

# YAML-Driven Gold Layer Table Setup

## Overview

Use YAML schema files as the **single source of truth** for Gold layer table definitions. A single Python script reads YAMLs at runtime and creates tables dynamically - no code generation or embedded DDL required.

**Key Principle:** Schema definitions live in YAML files. Python code is generic and reusable.

## When to Use This Pattern

✅ **Use when:**
- Managing 10+ Gold layer tables across multiple domains
- Schema evolves frequently and needs easy updates
- Want to avoid embedded SQL DDL strings in Python
- Need consistent table properties across all tables
- Want YAML files to be reviewable/diffable

❌ **Don't use when:**
- Only 1-2 simple tables to create
- Complex transformation logic required during table creation
- Tables have highly custom DDL not expressible in YAML

## Architecture

```
┌─────────────────────────────┐
│  YAML Schema Files          │  ← Source of Truth
│  gold_layer_design/         │
│  yaml/{domain}/*.yaml       │
└──────────┬──────────────────┘
           │
           │ (read at runtime)
           ▼
┌─────────────────────────────┐
│  setup_tables.py            │  ← Single Generic Script
│  - find_yaml_base()         │
│  - load_yaml()              │
│  - build_create_table_ddl() │
│  - create_table()           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Gold Layer Tables          │
│  (with PKs, comments, etc.) │
└─────────────────────────────┘
```

## YAML Schema Structure Summary

### Standard YAML Schema File

```yaml
# gold_layer_design/yaml/{domain}/{table_name}.yaml

table_name: dim_cluster
domain: compute
description: >
  Gold layer compute cluster dimension with configuration attributes.

primary_key:
  columns: ['workspace_id', 'cluster_id']
  composite: true

columns:
  - name: workspace_id
    type: STRING
    nullable: false
    description: "Workspace identifier..."
  
  - name: cluster_id
    type: STRING
    nullable: false
    description: "Cluster identifier..."
```

### Column Definition Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Column name |
| `type` | Yes | SQL data type (STRING, INT, BIGINT, TIMESTAMP, etc.) |
| `nullable` | No | Default: `true`. Set `false` for NOT NULL |
| `description` | No | Column comment (LLM-friendly description) |

### Supported Data Types

```yaml
# Standard types
type: STRING
type: INT
type: BIGINT
type: DOUBLE
type: BOOLEAN
type: DATE
type: TIMESTAMP
type: DECIMAL(38,10)

# Complex types
type: ARRAY<STRING>
type: MAP<STRING,STRING>
```

See `assets/templates/gold-table-template.yaml` for complete YAML template.

## Setup Script Implementation

### Core Functions

```python
# src/gold/setup_tables.py

import yaml
from pathlib import Path
from pyspark.sql import SparkSession

STANDARD_PROPERTIES = {
    "delta.enableChangeDataFeed": "true",
    "delta.enableRowTracking": "true",
    "delta.autoOptimize.autoCompact": "true",
    "delta.autoOptimize.autoCompact": "true",
    "layer": "gold",
}

def find_yaml_base() -> Path:
    """Find YAML directory - works in Databricks and locally."""
    possible_paths = [
        Path("../../gold_layer_design/yaml"),
        Path("gold_layer_design/yaml"),
    ]
    for path in possible_paths:
        if path.exists():
            return path
    raise FileNotFoundError("YAML directory not found")

def load_yaml(path: Path) -> dict:
    """Load and parse YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def build_create_table_ddl(catalog: str, schema: str, config: dict) -> str:
    """Build CREATE TABLE DDL from YAML config."""
    table_name = config['table_name']
    columns = config.get('columns', [])
    description = config.get('description', '')
    domain = config.get('domain', 'unknown')
    
    # Build column DDL
    col_ddls = []
    for col in columns:
        null_str = "" if col.get('nullable', True) else " NOT NULL"
        desc = escape_sql_string(col.get('description', ''))
        comment = f"\n    COMMENT '{desc}'" if desc else ""
        col_ddls.append(f"  {col['name']} {col['type']}{null_str}{comment}")
    
    columns_str = ",\n".join(col_ddls)
    
    # Build properties
    props = STANDARD_PROPERTIES.copy()
    props['domain'] = domain
    props['entity_type'] = "dimension" if table_name.startswith("dim_") else "fact"
    props_str = ",\n    ".join([f"'{k}' = '{v}'" for k, v in props.items()])
    
    return f"""CREATE OR REPLACE TABLE {catalog}.{schema}.{table_name} (
{columns_str}
)
USING DELTA
CLUSTER BY AUTO
TBLPROPERTIES (
    {props_str}
)
COMMENT '{escape_sql_string(description)}'"""

def create_table(spark: SparkSession, catalog: str, schema: str, yaml_path: Path) -> dict:
    """Create a single table from YAML file."""
    config = load_yaml(yaml_path)
    table_name = config.get('table_name', yaml_path.stem)
    
    # Create table
    ddl = build_create_table_ddl(catalog, schema, config)
    spark.sql(ddl)
    
    # Add primary key
    pk_config = config.get('primary_key', {})
    if pk_config and pk_config.get('columns'):
        pk_cols = ", ".join(pk_config['columns'])
        spark.sql(f"""
            ALTER TABLE {catalog}.{schema}.{table_name}
            ADD CONSTRAINT pk_{table_name}
            PRIMARY KEY ({pk_cols})
            NOT ENFORCED
        """)
    
    return {"table": table_name, "status": "success"}
```

### Main Entry Point

```python
def get_parameters():
    """Get job parameters from dbutils widgets."""
    catalog = dbutils.widgets.get("catalog")
    gold_schema = dbutils.widgets.get("gold_schema")
    domain = dbutils.widgets.get("domain")  # 'all' or specific domain
    return catalog, gold_schema, domain

def main():
    catalog, gold_schema, domain = get_parameters()
    spark = SparkSession.builder.getOrCreate()
    
    yaml_base = find_yaml_base()
    
    # Process all domains or specific domain
    if domain.lower() == "all":
        domains = [d.name for d in yaml_base.iterdir() if d.is_dir()]
    else:
        domains = [domain]
    
    for d in domains:
        yaml_files = sorted((yaml_base / d).glob("*.yaml"))
        for yaml_file in yaml_files:
            result = create_table(spark, catalog, gold_schema, yaml_file)
            print(f"✓ {result['table']}")

if __name__ == "__main__":
    main()
```

## Asset Bundle Configuration

### Sync YAML Files to Workspace

```yaml
# databricks.yml

sync:
  include:
    - src/**/*.py
    - sql/**/*.sql
    - gold_layer_design/yaml/**/*.yaml  # ← CRITICAL: Sync YAMLs
```

### Simplified Job Definition

```yaml
# resources/gold/gold_setup_job.yml

resources:
  jobs:
    gold_setup_job:
      name: "[${bundle.target} ${var.user_prefix}] Health Monitor - Gold Layer Setup"
      
      # PyYAML dependency required
      environments:
        - environment_key: default
          spec:
            environment_version: "4"
            dependencies:
              - "pyyaml>=6.0"
      
      tasks:
        # Single task creates ALL tables from YAMLs
        - task_key: setup_all_tables
          environment_key: default
          notebook_task:
            notebook_path: ../../src/gold/setup_tables.py
            base_parameters:
              catalog: ${var.catalog}
              gold_schema: ${var.gold_schema}
              domain: all  # or specific domain name
          timeout_seconds: 1800
        
        # FK constraints after all PKs exist
        - task_key: add_fk_constraints
          depends_on:
            - task_key: setup_all_tables
          environment_key: default
          notebook_task:
            notebook_path: ../../src/gold/add_all_fk_constraints.py
            base_parameters:
              catalog: ${var.catalog}
              gold_schema: ${var.gold_schema}
```

## Directory Structure

```
project_root/
├── databricks.yml                          # Bundle config (sync YAMLs!)
├── gold_layer_design/
│   └── yaml/                               # YAML Schema Files
│       ├── billing/
│       │   ├── dim_sku.yaml
│       │   ├── fact_usage.yaml
│       │   └── ...
│       ├── compute/
│       │   ├── dim_cluster.yaml
│       │   └── ...
│       └── ... (other domains)
├── src/
│   └── gold/
│       ├── setup_tables.py                 # Single setup script
│       └── add_all_fk_constraints.py       # FK constraints script
└── resources/
    └── gold/
        └── gold_setup_job.yml              # Job definition
```

## Workflow

### Making Schema Changes

1. **Edit YAML** - Modify the schema in `gold_layer_design/yaml/{domain}/{table}.yaml`
2. **Deploy** - `databricks bundle deploy -t dev` (YAMLs are synced)
3. **Run** - `databricks bundle run -t dev gold_setup_job`

**No code generation step!** Changes are picked up at runtime.

### Adding a New Table

1. Create new YAML file in appropriate domain folder
2. Deploy and run job
3. Table is created automatically

### Adding a New Domain

1. Create new folder under `gold_layer_design/yaml/`
2. Add YAML files for tables
3. Deploy and run job with `domain: all`

## Comparison: Before vs After

### ❌ Before: Embedded DDL Strings

```python
# 14 separate setup scripts with embedded SQL
DDL = """
CREATE OR REPLACE TABLE ${catalog}.${schema}.dim_sku (
  sku_name STRING NOT NULL COMMENT '...',
  ...
)
"""
```

**Problems:**
- SQL embedded as strings (escaping issues)
- 14 separate files to maintain
- Schema changes require editing Python code
- Hard to diff/review schema changes

### ✅ After: YAML-Driven

```yaml
# dim_sku.yaml
table_name: dim_sku
columns:
  - name: sku_name
    type: STRING
    nullable: false
    description: "SKU identifier..."
```

**Benefits:**
- YAML is single source of truth
- One generic Python script for all domains
- Schema changes are pure YAML edits
- Easy to review schema changes in PRs

## Validation Checklist

When using YAML-driven setup:

- [ ] YAML files synced in `databricks.yml` (`gold_layer_design/**/*.yaml`)
- [ ] PyYAML dependency in job environment
- [ ] All required columns have `name` and `type`
- [ ] Primary key columns marked `nullable: false`
- [ ] Column descriptions are LLM-friendly
- [ ] FK constraints handled in separate script (not in YAML)
- [ ] Domain parameter supports 'all' or specific domain
- [ ] Error handling for missing YAMLs/columns

## Common Issues

### Issue 1: YAML Files Not Found

**Error:** `FileNotFoundError: YAML directory not found`

**Solution:** Add YAMLs to sync in `databricks.yml`:
```yaml
sync:
  include:
    - gold_layer_design/yaml/**/*.yaml
```

### Issue 2: PyYAML Not Available

**Error:** `ModuleNotFoundError: No module named 'yaml'`

**Solution:** Add dependency to job environment:
```yaml
environments:
  - environment_key: default
    spec:
      dependencies:
        - "pyyaml>=6.0"
```

### Issue 3: PK Column Mismatch

**Error:** `Column 'xyz' not found in table`

**Solution:** Ensure PK columns in YAML match actual column names:
```yaml
# CORRECT  
primary_key:
  columns: ['table_catalog']  # ← Match column definition
```

## Assets

### gold-table-template.yaml

Starter YAML template for new Gold layer tables. Copy and customize for your table.

See `assets/templates/gold-table-template.yaml` for the complete template.

## Related Patterns

- **Databricks Asset Bundles** - See `skills/databricks-asset-bundles` skill
- **Unity Catalog Constraints** - See `common/unity-catalog-constraints` skill
- **Gold Layer Documentation** - See `gold/design-workers/06-table-documentation` skill

## References

- [Databricks Asset Bundles Sync](https://docs.databricks.com/dev-tools/bundles/settings.html#sync)
- [Unity Catalog Constraints](https://docs.databricks.com/tables/constraints.html)
- [Delta Lake Table Properties](https://docs.delta.io/latest/table-properties.html)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)

---

**Pattern Origin:** December 2025  
**Trigger:** Refactoring 14 domain-specific setup scripts with embedded DDL into single YAML-driven approach  
**Impact:** Reduced code from ~5000 lines across 14 files to ~300 lines in 1 file + 39 YAML schemas

---

## Inputs

- Gold YAML schema files from design phase (`gold_layer_design/yaml/{domain}/*.yaml`)
- Catalog and schema names (from job parameters or dbutils widgets)
- Common skill patterns: `databricks-table-properties`, `unity-catalog-constraints`, `schema-management-patterns`

## Outputs

- Created Gold tables with PKs, standard TBLPROPERTIES, CLUSTER BY AUTO
- Schema created with `CREATE SCHEMA IF NOT EXISTS`
- Predictive Optimization enabled on Gold schema
- FK constraints applied (via separate `add_fk_constraints.py`)

## Pipeline Notes to Carry Forward

- Table inventory dict from `build_inventory()` — reuse in merge scripts (Phase 2)
- YAML base path from `find_yaml_base()` — same path used by merge scripts
- Any FK constraint failures — may indicate missing PK tables that need creation first

## Next Step

Proceed to `pipeline-workers/02-merge-patterns` to implement Silver-to-Gold MERGE operations using the tables created in this phase.
