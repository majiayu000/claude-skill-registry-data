---
name: unity-catalog-constraints
description: Unity Catalog Primary Key and Foreign Key constraint patterns for proper relational modeling in Databricks. Use when implementing star schema dimensional models with PK/FK relationships in Gold layer tables. Covers surrogate keys as PRIMARY KEYS (not business keys), facts referencing surrogate PKs via FOREIGN KEY constraints, NOT NULL requirements for PK columns, proper dimensional modeling patterns (SCD Type 1/2, date dimensions), production deployment error prevention (never define FK inline in CREATE TABLE, DATE type casting from DATE_TRUNC, avoid module imports, widget parameter naming consistency), and validation checklists. Critical for ensuring proper relational modeling and preventing constraint application errors during Gold layer deployment.
metadata:
  author: prashanth subrahmanyam
  version: "2.1"
  domain: infrastructure
  role: shared
  used_by_stages: [3, 4]
  last_verified: "2026-06-02"
  volatility: medium
  clients: [ide_cli, genie_code]   # deploy via databricks-asset-bundles (the spine); Genie detail via genie-code-environment
  deploy_verb: "bundle deploy --target dev"
  deploy_note: "PK/FK constraint DDL are deploy-time bundle-resource bodies (RULE_10: run during bundle deploy, retained)"
  coverage: gold
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-unity-catalog/SKILL.md"
      relationship: "derived"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Unity Catalog Primary Key and Foreign Key Constraints

## Overview

Unity Catalog supports informational constraints (NOT ENFORCED) that enrich metadata, improve query optimization, and enable BI tool relationship discovery. This skill standardizes PK/FK implementation for star schema dimensional models following Kimball dimensional modeling best practices.

**Core Principle:** Surrogate keys are PRIMARY KEYS. Facts reference surrogate PKs via FOREIGN KEY constraints. Business keys have UNIQUE constraints for alternate lookups.

## When to Use This Skill

Use this skill when:
- Creating Gold layer tables with star schema dimensional models
- Implementing PRIMARY KEY and FOREIGN KEY constraints in Unity Catalog
- Setting up SCD Type 1 or Type 2 dimension tables
- Creating fact tables that reference dimension tables
- Troubleshooting constraint application errors
- Preventing common production deployment failures

## Most Common Failure

> **FK constraints referencing business keys instead of surrogate PK columns.**
>
> This is the single highest-impact failure observed in production.
> The Gold design YAML may generate `references: dim_user(user_id)` but the PK
> is `user_key`. Unity Catalog will reject the FK with:
> `foreign key parent columns do not match the referenced primary key.`
>
> **Before applying ANY FK constraint, verify the target column is a PRIMARY KEY.**
> See the [Pre-Apply Checklist](#pre-apply-checklist) below.

## Critical Rules

### 1. Surrogate Keys as Primary Keys

**❌ WRONG:** Business keys as PKs, facts reference business keys

**✅ CORRECT:** Surrogate keys as PKs, facts reference surrogate keys

```sql
CREATE TABLE dim_store (
    store_key STRING NOT NULL,  -- ✅ Surrogate PK
    store_number STRING NOT NULL,  -- Business key (UNIQUE)
    CONSTRAINT pk_dim_store PRIMARY KEY (store_key) NOT ENFORCED,
    CONSTRAINT uk_store_number UNIQUE (store_number) NOT ENFORCED
)

CREATE TABLE fact_sales (
    store_key STRING NOT NULL,  -- ✅ Surrogate FK
    CONSTRAINT fk_sales_store FOREIGN KEY (store_key) 
        REFERENCES dim_store(store_key) NOT ENFORCED
)
```

### 2. NOT NULL Requirement for Primary Keys

**All surrogate key columns used in PKs MUST be NOT NULL.**

Error: `Cannot create the primary key because its child column(s) is nullable.`

### 3. Foreign Keys Must Reference Primary Keys

**Foreign keys MUST reference PRIMARY KEY columns, even when NOT ENFORCED.**

- FKs can only reference PK columns (not any column)
- FKs must reference exact column(s) in PK definition

### 4. Never Define FK Constraints Inline in CREATE TABLE

**❌ WRONG:** FK constraints inline during table creation

**✅ CORRECT:** Define PKs inline, apply FKs later via ALTER TABLE

```sql
-- Step 1: CREATE TABLE with PK only
CREATE TABLE fact_sales (
    CONSTRAINT pk_fact_sales PRIMARY KEY (...) NOT ENFORCED  -- ✅ OK
)

-- Step 2: Apply FKs after all tables exist (separate script)
ALTER TABLE fact_sales
    ADD CONSTRAINT fk_sales_store 
    FOREIGN KEY (store_key) 
    REFERENCES dim_store(store_key) NOT ENFORCED  -- ✅ Safe
```

**Key Principles:**
- ✅ Inline PKs are safe - Define PRIMARY KEY constraints directly in CREATE TABLE
- ❌ Inline FKs fail - Never define FOREIGN KEY constraints in CREATE TABLE
- ✅ Separate constraint script - Create dedicated `constraints.py` to apply all FKs after tables exist
- ✅ Dependency order matters - Reference tables (dims) before fact tables, constraints last

### 5. Never Use `DEFAULT` Column Clauses in DDL

**❌ FORBIDDEN:** a `DEFAULT <expr>` clause on any column in `CREATE TABLE` (Delta / serverless).

```sql
-- ❌ WRONG — fails with "...requires table feature allowColumnDefaults..." by default
is_active BOOLEAN NOT NULL DEFAULT true

-- ✅ CORRECT — declare the column, set the default at INSERT time
is_active BOOLEAN NOT NULL          -- in CREATE TABLE
... INSERT ... SELECT ..., true AS is_active, ...   -- default supplied on write
```

Column `DEFAULT` expressions require the `delta.feature.allowColumnDefaults` table feature, which is **off by default** — DDL using `DEFAULT` fails on a standard table. Do NOT enable the feature flag to make `DEFAULT` work; **set defaults at INSERT time instead** (and do not add columns the design/template did not call for — this rule exists because an agent invented an `is_active BOOLEAN NOT NULL DEFAULT true` column that was never in the template). This applies to every layer's DDL (Bronze, Silver `dq_rules`, Gold), not just constraints.

## Quick Reference

### Dimension Table (SCD Type 1)
- Surrogate key (`*_key`) is PRIMARY KEY
- Business key has UNIQUE constraint
- All PK columns are NOT NULL
- PK defined inline in CREATE TABLE

### Dimension Table (SCD Type 2)
- Surrogate key (`*_key`) is PRIMARY KEY
- Business key does NOT have UNIQUE (multiple versions allowed)
- `is_current` flag indicates current version
- Facts join to surrogate key, filter `WHERE is_current = TRUE`

### Fact Table
- Composite PK on surrogate FKs (defines grain)
- Surrogate FKs reference dimension PKs
- Business keys included for readability
- NO inline FK constraints (apply separately via ALTER TABLE)

### Date Type Casting
**Rule:** Always `CAST(DATE_TRUNC(...) AS DATE)` when populating DATE columns.

### Constraint Naming Conventions

| Constraint Type | Pattern | Example |
|----------------|---------|---------|
| Primary Key | `pk_<table_name>` | `pk_dim_store` |
| Foreign Key | `fk_<fact_table>_<dimension>` | `fk_sales_store` |
| Unique (Business Key) | `uk_<table>_<column>` | `uk_store_number` |

## Quick Reference Checklist

### Table Creation Phase
- [ ] All dimension tables define PRIMARY KEY inline in CREATE TABLE
- [ ] **NO** fact tables define FOREIGN KEY inline in CREATE TABLE
- [ ] **NO** `DEFAULT` column clauses anywhere in DDL (set defaults at INSERT time)
- [ ] Date columns use explicit `CAST(DATE_TRUNC(...) AS DATE)`
- [ ] All surrogate key columns are `NOT NULL`
- [ ] Reference dimension (dim_date) created before facts that reference it

### Constraint Application Phase
- [ ] Separate `constraints.py` script applies ALL FKs via ALTER TABLE
- [ ] Constraint script runs AFTER all table creation tasks
- [ ] Primary keys applied to dimensions before foreign keys applied to facts
- [ ] Each FK references an existing PK column
- [ ] Constraint names are descriptive (e.g., `pk_dim_date`, `fk_sales_date`)

### Validation Phase
- [ ] All surrogate key columns are `NOT NULL`
- [ ] PKs defined on surrogate keys (proper dimensional modeling)
- [ ] FKs reference surrogate PK columns exactly
- [ ] Facts have surrogate FK columns (store_key, product_key, date_key)
- [ ] Business keys have UNIQUE constraints (where applicable)
- [ ] All constraints include `NOT ENFORCED`

## Common Mistakes to Avoid

1. **PK on business key** - Use surrogate keys as PKs
2. **Nullable surrogate key** - All PK columns must be NOT NULL
3. **FK references non-PK column** - FKs must reference PK columns
4. **Inline FK constraints** - Never define FKs in CREATE TABLE
5. **DATE_TRUNC without casting** - Always CAST to DATE
6. **Module imports in notebooks** - Inline helper functions or use pure Python
7. **Widget parameter name mismatch** - YAML parameters must match `dbutils.widgets.get()`

## Serverless Limitations

UNIQUE constraints require `spark.databricks.sql.dsv2.unique.enabled = true`.
This config **cannot be set in serverless compute** (Spark config is read-only).

**Impact:** `spark.conf.set(...)` will crash the job in serverless.

**Workarounds:**
- Use classic (non-serverless) compute for the constraint application job
- Skip UNIQUE constraints on serverless; rely on surrogate PK + FK only
- Use a DAB job definition that targets a classic job cluster for constraint tasks

## Pre-Apply Checklist

Before executing any FK ALTER TABLE statement:

1. **Verify target column is a PK** -- run `SHOW CONSTRAINTS IN <schema>` or `DESCRIBE EXTENDED <dim_table>` to confirm the referenced column has a PRIMARY KEY constraint
2. **Verify PK constraint exists** -- if the dimension table was just created but PK not yet applied, the FK will fail
3. **Verify serverless compatibility** -- if running on serverless, skip UNIQUE constraints (see Serverless Limitations above)
4. **Verify YAML FK format** -- the `references:` field must use surrogate key columns (e.g., `dim_store(store_key)`), NOT business keys (e.g., `dim_store(store_number)`)

## Cross-Skill Dependencies

- **Gold Design skill** (`gold/00-gold-layer-design`): The YAML schema generator may produce FK references to business keys. During Gold implementation, validate that all `references:` fields in YAML point to surrogate PK columns before applying constraints.
- **Gold Setup skill** (`gold/01-gold-layer-setup`): The `fk-constraint-patterns.md` reference defers to this skill for PK/FK rules. Ensure the FK application script verifies PK existence first.

## Reference Files

### [constraint-patterns.md](references/constraint-patterns.md)
Detailed SQL patterns including:
- Standard dimensional model patterns (SCD Type 1/2, date dimensions, fact tables)
- Correct vs incorrect pattern examples
- Common mistakes and solutions
- Production error prevention patterns
- Benefits of NOT ENFORCED constraints
- Design philosophy

### [validation-guide.md](references/validation-guide.md)
Validation patterns and troubleshooting:
- NOT NULL requirement for primary keys
- Databricks FK constraint requirements
- Validation checklists (pre-deployment, post-deployment)
- Common error patterns and solutions
- Production deployment checklist
- Benefits of NOT ENFORCED constraints

## Scripts

### [apply_constraints.py](scripts/apply_constraints.py)
Python utility for applying constraints:
- `verify_pk_exists()` - Verify PK constraint exists before applying FK (pre-flight check)
- `add_primary_key()` - Add PRIMARY KEY constraint
- `add_foreign_key()` - Add FOREIGN KEY constraint (with optional PK verification)
- `add_unique_constraint()` - Add UNIQUE constraint (for business keys)
- `drop_constraint()` - Drop constraint (for idempotency)
- `apply_all_constraints()` - Example function applying all constraints

**Usage:**
```python
from scripts.apply_constraints import add_primary_key, add_foreign_key

add_primary_key(spark, catalog, schema, "dim_store", ["store_key"])
add_foreign_key(spark, catalog, schema, "fact_sales", ["store_key"], 
                "dim_store", ["store_key"])
```

## Assets

### [constraints-template.sql](assets/templates/constraints-template.sql)
SQL template for creating Gold layer tables with constraints:
- Dimension table templates (SCD Type 1 and Type 2)
- Date dimension template
- Fact table template (PK only, no inline FKs)
- Foreign key application examples (ALTER TABLE statements)

**Usage:** Copy template, replace placeholders (`<dimension_name>`, `<business_key>`, etc.), customize for your schema.

## References

- [Unity Catalog Constraints](https://docs.databricks.com/data-governance/unity-catalog/constraints.html)
- [Primary and Foreign Keys](https://docs.databricks.com/tables/constraints.html#declare-primary-key-and-foreign-key-relationships)
- [Dimensional Modeling Best Practices](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [Star Schema Design](https://docs.databricks.com/lakehouse-architecture/medallion.html)
