---
name: databricks-table-valued-functions
description: End-to-end guide for planning, creating, deploying, and validating Table-Valued Functions (TVFs) in Databricks optimized for Genie Space natural language queries. Use when creating TVFs for Genie Spaces, planning TVF requirements from business questions, troubleshooting TVF compilation errors, or ensuring Genie compatibility. Includes requirements gathering templates, schema validation patterns, SQL requirements (STRING parameters, parameter ordering, LIMIT workarounds), v3.0 bullet-point comment format, null safety, SCD2 handling, cartesian product prevention, 5 complete domain-adaptable examples, Asset Bundle deployment patterns, and post-deployment validation queries.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "TVFs are created by a notebook_task in the semantic-layer job; deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code). TVF params are STRING for Genie compatibility."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  domain: semantic-layer
  role: worker
  pipeline_stage: 6
  pipeline_stage_name: semantic-layer
  called_by:
    - semantic-layer-setup
  standalone: true
  last_verified: "2026-02-07"
  volatility: medium
  upstream_sources: []  # Internal TVF patterns
---

> **End-to-end semantic layer?** If you are creating TVFs as part of a larger deployment that also includes Metric Views and Genie Spaces, read `semantic-layer/00-semantic-layer-setup/SKILL.md` first — it orchestrates this skill with the others and mandates Gold schema validation before artifact creation.

# Databricks Table-Valued Functions (TVFs) for Genie

## Overview

Table-Valued Functions (TVFs) provide **pre-built, parameterized queries** that Genie can invoke for natural language access to your data. This skill covers the entire TVF lifecycle: planning, creation, deployment, and validation.

**Why TVFs Matter:**
- **Pre-built queries** ensure consistent business logic across all consumers
- **LLM-friendly metadata** helps Genie understand when to use each function
- **Proper SQL patterns** prevent compile-time errors and data inflation bugs
- **Parameterized access** gives users instant answers to common questions

**Key Capabilities:**
- Plan TVFs from business questions using requirements gathering templates
- Create TVFs with Genie-compatible parameter types (STRING for dates)
- Validate schemas before writing SQL to prevent 100% of compilation errors
- Structure comments (v3.0 bullet-point format) for optimal Genie query matching
- Handle SCD2 dimensions with proper `is_current` filtering
- Prevent cartesian products in aggregation CTEs
- Use proper parameter ordering and LIMIT workarounds
- Deploy TVFs via Asset Bundle jobs
- Validate TVFs with post-deployment queries

**What TVFs Provide:**
- ✅ Parameterized queries with input parameters
- ✅ LLM-friendly metadata for Genie understanding
- ✅ Genie-compatible types (STRING for dates, not DATE)
- ✅ Top N patterns using WHERE rank <= param (not LIMIT param)
- ✅ Null safety with NULLIF for all divisions
- ❌ No DATE parameters (Genie doesn't support DATE type)
- ❌ No LIMIT with parameters (use ROW_NUMBER + WHERE instead)

## When to Use This Skill

Use this skill when:
- Planning which TVFs to create from business questions
- Creating TVFs for Genie Spaces
- Troubleshooting TVF compilation errors
- Ensuring Genie compatibility
- Validating schemas before writing SQL
- Deploying TVFs via Asset Bundles
- Preventing common SQL errors (parameter types, LIMIT clauses, cartesian products)

> **Layer-aware manifest fields:** TVF manifest entries carry one of two table lists:
>
> - `gold_tables_used` — canonical for Gold-based runs (acceleration; workshop on `deployed_gold` / `gold_design`). TVF DDL references `${catalog}.${gold_schema}.*`.
> - `source_assets_used` — canonical for workshop deployments on `deployed_silver` / `deployed_bronze`. TVF DDL references `${catalog}.${silver_schema}.*` or `${catalog}.${bronze_schema}.*` directly. The orchestrator prints a quality advisory; STRING parameter rules and Genie compatibility are unchanged.
>
> The orchestrator (`semantic-layer/00-semantic-layer-setup`) only stops before invoking this skill when `planning_source.selected_layer = source_csv` (no live tables exist). Production TVFs should ultimately reference Gold; promote workshop TVFs to Gold for production hardening.

## Quick Start (2-3 hours)

**Goal:** Create 10-15 pre-built, parameterized SQL queries for common business questions.

**What You'll Create:**
1. `table_valued_functions.sql` — SQL file with 10-15 TVF definitions using `${catalog}` and `${gold_schema}` template variables
2. `create_tvfs.py` — Python notebook that reads the SQL file, substitutes `${catalog}` / `${gold_schema}` variables, splits into individual statements, and executes each via `spark.sql()`. **Use the canonical template at `assets/templates/create_tvfs.py`** — it imports the shared `src/common/_notebook_paths.py` helper (see `common/databricks-python-imports/SKILL.md`) and fails loud with `RuntimeError` on any DDL error. Never call `sys.exit(0)` to report failure (exit 0 = "success" to Databricks Jobs).
3. `tvf_job.yml` — Asset Bundle job using `notebook_task` (NOT `sql_task` — see warning below)

**⚠️ Why `notebook_task` instead of `sql_task`?** TVF DDL uses `${catalog}.${gold_schema}` in identifiers (schema-qualified function names). `sql_task.parameters` are SQL bind parameters (`:param`) that cannot substitute identifiers — only values in `WHERE` clauses. A Python notebook performs string substitution before executing the SQL.

**Fast Track:**
```sql
CREATE OR REPLACE FUNCTION get_top_stores_by_revenue(
    start_date STRING COMMENT 'Start date (format: YYYY-MM-DD)',
    end_date STRING COMMENT 'End date (format: YYYY-MM-DD)',
    top_n INT DEFAULT 10 COMMENT 'Number of top stores to return'
)
RETURNS TABLE(
    rank INT COMMENT 'Store rank by revenue',
    store_name STRING COMMENT 'Store display name',
    total_revenue DECIMAL(18,2) COMMENT 'Total revenue for period'
)
COMMENT '
• PURPOSE: Returns top N stores ranked by revenue for a date range
• BEST FOR: "What are the top 10 stores by revenue?" | "Show me best performing stores"
• RETURNS: Individual store rows (rank, store_name, total_revenue)
• PARAMS: start_date, end_date, top_n (default: 10)
• SYNTAX: SELECT * FROM get_top_stores_by_revenue(''2024-01-01'', ''2024-12-31'', 10)
'
RETURN ...;
```

**Common Business Naming Patterns:**

| Pattern | Template | Example |
|---|---|---|
| **Top N** | `get_top_{entity}_by_{metric}(start_date, end_date, top_n)` | `get_top_stores_by_revenue(...)` |
| **Trending** | `get_{metric}_trend(start_date, end_date)` | `get_daily_sales_trend(...)` |
| **Comparison** | `get_{metric}_by_{dimension}(start_date, end_date)` | `get_sales_by_state(...)` |
| **Performance** | `get_{entity}_performance(entity_id, start_date, end_date)` | `get_store_performance(...)` |

**Critical SQL Rules:**
- STRING for date parameters (never DATE)
- Required parameters first, DEFAULT parameters last
- ROW_NUMBER + WHERE for Top N (never LIMIT with parameter)

**Output:** 10-15 TVFs callable by Genie and queryable via SQL

See `references/tvf-planning-guide.md` for question categorization and domain examples.
See `references/tvf-examples.md` for 5 complete, production-ready TVF implementations.
See `assets/templates/tvf-requirements-template.md` to plan your TVFs before coding.

## Critical Rules

### ⚠️ CRITICAL: Schema Validation BEFORE Writing SQL

**RULE #0: Always consult YAML schema definitions before writing any TVF SQL**

**100% of SQL compilation errors are caused by not consulting YAML schemas first.**

**Pre-Development Checklist:**
1. Read YAML schema files (5 minutes)
2. Create SCHEMA_MAPPING.md (2 minutes)
3. Write TVF SQL using documented schema
4. Run validation script (30 sec)
5. Deploy

**ROI:** 71% time reduction (45 min → 13 min)  
**First-Time Success Rate:** 0% → 95%+

See `references/tvf-patterns.md` for detailed schema validation workflow.

### ⚠️ Issue 1: Parameter Types for Genie Compatibility

**RULE: Use STRING for date parameters, not DATE**

Genie Spaces do not support DATE type parameters. Always use STRING with explicit format documentation.

**❌ DON'T:**
```sql
CREATE FUNCTION get_sales_by_date_range(
  start_date DATE COMMENT 'Start date',
  end_date DATE COMMENT 'End date'
)
```

**✅ DO:**
```sql
CREATE FUNCTION get_sales_by_date_range(
  start_date STRING COMMENT 'Start date (format: YYYY-MM-DD)',
  end_date STRING COMMENT 'End date (format: YYYY-MM-DD)'
)
...
WHERE transaction_date BETWEEN CAST(start_date AS DATE) AND CAST(end_date AS DATE)
```

### ⚠️ Issue 2: Parameter Ordering with DEFAULT Values

**RULE: Parameters with DEFAULT must come AFTER parameters without DEFAULT**

**❌ DON'T:**
```sql
CREATE FUNCTION get_top_stores(
  top_n INT DEFAULT 10,          -- ❌ DEFAULT parameter first
  start_date STRING,              -- ❌ Required parameter after DEFAULT
  end_date STRING
)
```

**✅ DO:**
```sql
CREATE FUNCTION get_top_stores(
  start_date STRING,              -- ✅ Required parameter first
  end_date STRING,                -- ✅ Required parameter
  top_n INT DEFAULT 10            -- ✅ Optional parameter last
)
```

### ⚠️ Issue 3: LIMIT Clauses Cannot Use Parameters

**RULE: Use WHERE rank <= parameter instead of LIMIT parameter**

LIMIT clauses require compile-time constants. Use WHERE with ROW_NUMBER() instead.

**❌ DON'T:**
```sql
SELECT * FROM store_metrics
ORDER BY total_revenue DESC
LIMIT top_n;  -- ❌ Cannot use parameter here
```

**✅ DO:**
```sql
WITH ranked_stores AS (
  SELECT ...,
    ROW_NUMBER() OVER (ORDER BY total_revenue DESC) as rank
  FROM store_metrics
)
SELECT * FROM ranked_stores
WHERE rank <= top_n  -- ✅ Can use parameter in WHERE
ORDER BY rank;
```

### ⚠️ CRITICAL: Cartesian Product Bug in Aggregation CTEs

**Never re-join a table that's already been aggregated in a CTE.**

**❌ BUGGY PATTERN:**
```sql
WITH period_data AS (
  SELECT SUM(revenue) as total_revenue
  FROM fact_table
  GROUP BY period
),
final AS (
  SELECT SUM(pd.total_revenue), SUM(ft.other_metric)  -- 🔥 CARTESIAN!
  FROM period_data pd
  LEFT JOIN fact_table ft ON ...  -- ❌ Re-joining source!
)
```

**✅ CORRECT PATTERN:**
```sql
SELECT 
  period,
  SUM(revenue) as total_revenue,
  SUM(other_metric) as other_metric
FROM fact_table
GROUP BY period;  -- ✅ Single aggregation pass
```

See `references/tvf-patterns.md` for detailed cartesian product prevention patterns.

## Quick Reference

### Standardized TVF Comment Format (v3.0)

Use bullet-point format for ALL TVF comments:

```sql
COMMENT '
• PURPOSE: [One-line description of what the TVF does]
• BEST FOR: [Example questions separated by |]
• NOT FOR: [What to avoid - redirect to correct TVF] (optional)
• RETURNS: [PRE-AGGREGATED rows or Individual rows] (exact column list)
• PARAMS: [Parameter names with defaults]
• SYNTAX: SELECT * FROM tvf_name(''param1'', ''param2'')
• NOTE: [Important caveats - DO NOT wrap in TABLE(), etc.] (optional)
'
```

### Complete TVF Pattern

```sql
CREATE OR REPLACE FUNCTION get_top_stores_by_revenue(
  -- Required parameters first (no DEFAULT)
  start_date STRING COMMENT 'Start date (format: YYYY-MM-DD)',
  end_date STRING COMMENT 'End date (format: YYYY-MM-DD)',
  -- Optional parameters last (with DEFAULT)
  top_n INT DEFAULT 10 COMMENT 'Number of top stores to return'
)
RETURNS TABLE(
  rank INT COMMENT 'Store rank by revenue',
  store_number STRING COMMENT 'Store identifier',
  store_name STRING COMMENT 'Store name',
  total_revenue DECIMAL(18,2) COMMENT 'Total revenue for period',
  total_units BIGINT COMMENT 'Total units sold'
)
COMMENT '
• PURPOSE: Returns the top N stores ranked by revenue for a date range
• BEST FOR: "What are the top 10 stores by revenue?" | "Show me best performing stores"
• RETURNS: Individual store rows (rank, store_number, store_name, total_revenue, total_units)
• PARAMS: start_date, end_date, top_n (default: 10)
• SYNTAX: SELECT * FROM get_top_stores_by_revenue(''2024-01-01'', ''2024-12-31'', 10)
• NOTE: Returns user_id for individual store analysis | Sorted by total_revenue DESC
'
RETURN
  WITH store_metrics AS (
    SELECT 
      store_number,
      store_name,
      SUM(net_revenue) as total_revenue,
      SUM(net_units) as total_units
    FROM fact_sales_daily
    WHERE transaction_date BETWEEN CAST(start_date AS DATE) AND CAST(end_date AS DATE)
    GROUP BY store_number, store_name
  ),
  ranked_stores AS (
    SELECT 
      ROW_NUMBER() OVER (ORDER BY total_revenue DESC) as rank,
      store_number,
      store_name,
      total_revenue,
      total_units
    FROM store_metrics
  )
  SELECT * FROM ranked_stores
  WHERE rank <= top_n  -- ✅ Use WHERE instead of LIMIT
  ORDER BY rank;
```

## Core Patterns

### Null Safety

**Always use NULLIF() for division to prevent divide-by-zero errors:**

```sql
-- ✅ DO: Null-safe division
total_revenue / NULLIF(transaction_count, 0) as avg_transaction_value
```

### SCD Type 2 Dimension Handling

**Always filter for current records when joining SCD2 dimensions:**

```sql
-- ✅ Correct: Filter for current version
LEFT JOIN dim_store ds 
  ON fsd.store_number = ds.store_number 
  AND ds.is_current = true
```

### Aggregate vs Individual Row TVFs

**Aggregate TVF (Returns Pre-Aggregated Rows):**
- Returns fixed number of rows (e.g., 5 segment rows)
- Data is PRE-AGGREGATED - no GROUP BY needed on top
- Do NOT use in JOINs (no user_id or other keys to join on)

**Individual Row TVF (Returns Detail Rows):**
- Returns variable number of rows based on data
- Each row represents one entity (customer, property, host)
- CAN be used in JOINs (has identifier columns)

See `references/genie-integration.md` for detailed examples.

## TVF Creation Checklist

### SQL Compliance
- [ ] All date parameters are STRING type (not DATE)
- [ ] Required parameters come before optional parameters
- [ ] No parameters used in LIMIT clauses (use WHERE rank <= param)
- [ ] All divisions use NULLIF to prevent divide-by-zero
- [ ] SCD2 joins include `is_current = true` filter
- [ ] **No cartesian products:** CTEs don't re-join tables already aggregated
- [ ] **Single aggregation pass:** Each source table read and aggregated only once

### Genie Optimization (Standardized Comment Format)
- [ ] Function COMMENT uses bullet-point format (• PURPOSE, • BEST FOR, etc.)
- [ ] **PURPOSE:** One-line description of what TVF does
- [ ] **BEST FOR:** 2+ example questions (pipe-separated)
- [ ] **NOT FOR / PREFERRED OVER:** Redirect to correct asset when applicable
- [ ] **RETURNS:** Specifies PRE-AGGREGATED or Individual rows + exact column list
- [ ] **PARAMS:** Parameter names with defaults
- [ ] **SYNTAX:** Exact copyable example with proper date format
- [ ] **NOTE:** Caveats (DO NOT wrap in TABLE(), DO NOT add GROUP BY, etc.)
- [ ] All parameters have descriptive COMMENT with format
- [ ] All returned columns have COMMENT
- [ ] Professional language (no "metric view is broken" phrases)

### Testing
- [ ] Function compiles without errors
- [ ] Function executes with valid parameters
- [ ] Function handles edge cases (empty results, null values)
- [ ] Function tested in Genie Space (if applicable)
- [ ] **Results validated against metric view** (ratio ≈ 1.0, not 254x)

## Implementation Workflow

### Phase 1: Planning (30 min)
- [ ] Fill out requirements template (`assets/templates/tvf-requirements-template.md`)
- [ ] List 10-15 common business questions from stakeholders
- [ ] Categorize questions (revenue, product, entity, trend)
- [ ] Map questions to TVF names and parameters using naming patterns
- [ ] Identify required vs optional parameters

See `references/tvf-planning-guide.md` for question categories and domain examples.

### Phase 2: SQL Development (1-2 hours)
- [ ] Consult YAML schemas FIRST (Rule #0 — see `references/tvf-patterns.md`)
- [ ] Create `table_valued_functions.sql` following file organization pattern
- [ ] Implement each TVF following the template (`assets/templates/tvf-template.sql`)
- [ ] Verify all date parameters are STRING type
- [ ] Verify parameter ordering (required first)
- [ ] Verify Top N uses ROW_NUMBER + WHERE (not LIMIT)
- [ ] Verify all divisions use NULLIF

See `references/tvf-examples.md` for 5 complete TVF examples covering different patterns.

### Phase 3: Metadata (30 min)
- [ ] Add function-level COMMENT using v3.0 bullet-point format
- [ ] Add 2+ example questions per function (BEST FOR)
- [ ] Add COMMENT to every parameter (include format for STRING dates)
- [ ] Add COMMENT to every returned column
- [ ] Add NOT FOR / PREFERRED OVER cross-references where applicable

See `references/genie-integration.md` for comment format details and Genie misuse prevention.

### Phase 4: Testing (30 min)
- [ ] Compile each function (no syntax errors)
- [ ] Execute with valid parameters
- [ ] Test edge cases (empty results, null values)
- [ ] Validate results against metric view (ratio ≈ 1.0)
- [ ] Verify results match expectations

See `scripts/validate_tvfs.sql` for ready-to-run validation queries.

### Phase 5: Deployment
- [ ] Add to Asset Bundle job (`notebook_task` — NOT `sql_task`, which cannot substitute identifiers in DDL)
- [ ] Deploy: `databricks bundle deploy -t dev`
- [ ] Run: `databricks bundle run gold_setup_job -t dev`
- [ ] Test in Genie Space (if applicable)

See `references/tvf-patterns.md` (Asset Bundle Deployment section) for job YAML patterns.

**Time Estimates:**

| Phase | Duration | Activities |
|---|---|---|
| Phase 1: Planning | 30 min | Requirements gathering, question mapping |
| Phase 2: SQL Development | 1-2 hours | Write 10-15 TVFs with schema validation |
| Phase 3: Metadata | 30 min | v3.0 comments, parameter/column documentation |
| Phase 4: Testing | 30 min | Compile, execute, validate against metric views |
| Phase 5: Deployment | 30 min | Asset Bundle deploy, Genie Space testing |
| **Total** | **2-3 hours** | For 10-15 TVFs |

## Common Mistakes to Avoid

❌ **Don't:**
- Use DATE parameters (use STRING with CAST)
- Mix DEFAULT and non-DEFAULT parameters
- Use parameters in LIMIT clauses
- Re-join tables after aggregation (cartesian product)
- Skip schema validation before writing SQL

✅ **Do:**
- Validate schemas from YAML before coding
- Use STRING for date parameters
- Put required parameters before optional ones
- Use WHERE rank <= param instead of LIMIT param
- Single aggregation pass, no self-joins

## Reference Files

- **`references/tvf-patterns.md`** — SQL patterns, parameter types, cartesian product prevention, schema validation, SQL file organization, Asset Bundle deployment
- **`references/genie-integration.md`** — Genie compatibility, v3.0 comment format, misuse prevention, professional language standards
- **`references/tvf-examples.md`** — 5 complete production-ready TVF examples (ranking, drilldown, product, geographic, temporal)
- **`references/tvf-planning-guide.md`** — Question categorization, TVF planning tables, domain-specific examples (Retail, Healthcare, Finance, Hospitality)

## Assets

- **`assets/templates/tvf-template.sql`** — Starter SQL template for new TVFs with v3.0 comment format
- **`assets/templates/tvf-requirements-template.md`** — Requirements gathering template (fill in before coding)
- **`assets/templates/tvf-creation-job-template.yml`** — Standalone Asset Bundle job for TVF deployment. **⚠️ Uses `notebook_task` (NOT `sql_task`)** because TVF DDL requires `${catalog}.${gold_schema}` identifier substitution which `sql_task` bind parameters cannot do. For combined deployment, use the orchestrator's `semantic-layer-job-template.yml`.

## Scripts

- **`scripts/validate_tvfs.sql`** — Post-deployment validation queries (list, describe, test, compare to metric views)

## References

### Official Documentation
- [Databricks Table-Valued Functions](https://docs.databricks.com/sql/language-manual/sql-ref-syntax-qry-select-tvf)
- [Genie Trusted Assets - Functions](https://docs.databricks.com/genie/trusted-assets#tips-for-writing-functions)
- [SQL UDF Best Practices](https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-sql-function)

### Related Skills
- `metric-views-patterns` - Metric view YAML structure
- `genie-space-patterns` - Genie Space setup

## TVF Notes to Carry Forward

After completing TVF creation, carry these notes to the next worker:
- **TVF names and paths:** List of all created TVFs with their SQL file paths
- **Parameter signatures:** For each TVF, list parameters (all STRING) with descriptions
- **Domain assignments:** Which Gold tables each TVF queries, grouped by domain
- **Genie-relevant TVFs:** Which TVFs are designed for Genie use (date-range filters, lookup queries)
- **Validation status:** Which TVFs passed test queries, any unresolved issues

## Next Step

After TVFs are deployed and validated, proceed to:
**`semantic-layer/03-genie-space-patterns/SKILL.md`** — Configure Genie Spaces using the Metric Views (from Phase 1) and TVFs (from this phase) as trusted assets.

## Version History

- **v2.1** (Feb 2026) — Corrected deployment from sql_task to notebook_task; added explanation of sql_task parameter limitation for DDL identifier substitution; added Notes to Carry Forward and Next Step for progressive disclosure
- **v2.0** (Feb 2026) - Merged comprehensive TVF creation workflow: Quick Start, requirements gathering template, 5 complete examples, planning guide with domain-specific examples, implementation workflow (5 phases), Asset Bundle deployment patterns, validation queries, common business naming patterns
- **v1.3** (Dec 16, 2025) - Standardized TVF comment format v3.0 for Genie optimization
- **v1.2** (Dec 15, 2025) - Critical bug prevention: Cartesian product in aggregations
- **v1.1** (Dec 2025) - Major enhancement: Schema-first development patterns
- **v1.0** (Oct 2025) - Initial rule based on 15 TVF deployment learnings
