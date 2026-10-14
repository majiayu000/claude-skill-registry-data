---
name: metric-views-patterns
description: Standard patterns for creating Databricks Metric Views with semantic metadata for Genie and AI/BI. Use when creating metric views, troubleshooting metric view creation errors, validating schema references before deployment, implementing joins (including snowflake schema patterns), or optimizing metric views for Genie natural language queries.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Metric Views are created by a notebook_task in the semantic-layer job; deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code)."
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
  last_verified: "2026-06-06"
  volatility: high
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-metric-views/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
    - name: "databricks-docs-overview"
      url: "https://docs.databricks.com/aws/en/business-semantics/metric-views/"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-yaml-reference"
      url: "https://docs.databricks.com/aws/en/business-semantics/metric-views/yaml-reference"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-basic-modeling"
      url: "https://docs.databricks.com/aws/en/business-semantics/metric-views/basic-modeling"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-advanced-techniques"
      url: "https://docs.databricks.com/aws/en/business-semantics/metric-views/advanced-techniques"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-create-sql"
      url: "https://docs.databricks.com/aws/en/metric-views/create/sql"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-manage"
      url: "https://docs.databricks.com/aws/en/business-semantics/metric-views/manage"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-agent-metadata"
      url: "https://docs.databricks.com/aws/en/business-semantics/agent-metadata"
      relationship: "upstream"
      last_synced: "2026-06-05"
---

> **End-to-end semantic layer?** If you are creating Metric Views as part of a larger deployment that also includes TVFs and Genie Spaces, read `semantic-layer/00-semantic-layer-setup/SKILL.md` first — it orchestrates this skill with the others and mandates Gold schema validation before artifact creation.

# Metric Views Patterns for Genie & AI/BI

## Overview

Metric Views provide a semantic layer for natural language queries via Genie and AI/BI dashboards. This skill standardizes the YAML structure for comprehensive, LLM-friendly metric definitions following Databricks Metric View Specification v1.1.

**Predecessor:** Gold tables must exist before creating metric views. Use `gold-layer-design` + `gold-layer-setup` skills first.

**Key Capabilities:**
- Create metric views with proper SQL syntax (`WITH METRICS LANGUAGE YAML`)
- Validate schemas before deployment to prevent 100% of common errors
- Structure joins (direct and snowflake schema patterns)
- Optimize comments for Genie natural language queries
- Handle SCD2 dimensions with proper `is_current` filtering

## When to Use This Skill

Use this skill when:
- Creating new metric views for Genie Spaces
- Troubleshooting metric view creation errors
- Validating schema references before deployment
- Implementing joins (including transitive relationships)
- Optimizing metric views for Genie natural language queries
- Ensuring compliance with v1.1 specification
- Following the requirements gathering template to design metric views

## Prerequisites

⚠️ **MANDATORY:** Complete these before creating metric views:
- [ ] Gold layer tables exist in Unity Catalog (use `gold-layer-design` + `gold-layer-setup` skills) — required for **production deployment**.
- [ ] Gold layer YAML schemas exist in `gold_layer_design/yaml/` (for validation script). When invoked from a workshop-draft plan with `selected_layer = gold_design`, YAML alone is acceptable as the source of truth and the validation script's live-catalog probe is advisory.
- [ ] Serverless SQL warehouse available (for metric view creation and querying)
- [ ] SQL warehouse or compute resource on Databricks Runtime 17.3+ (current docs requirement for `CAN USE` permission to create or edit a metric view). YAML v1.1 features were introduced in DBR 17.2; some experimental features (snowflake schema joins, agent metadata, materialization) require DBR 17.3+.

> **Layer-aware deployment (workshop mode):** The patterns in this skill (YAML, dimensions, measures, joins) are layer-neutral. The orchestrator (`semantic-layer/00-semantic-layer-setup`) decides which schema to deploy against based on `planning_source.selected_layer`:
>
> - `deployed_gold` / `gold_design` → reference Gold tables (production path).
> - `deployed_silver` / `deployed_bronze` (workshop deployments) → reference Silver or Bronze tables directly. Metric View YAML is identical in shape; the `source` field points at the workshop layer's schema. The orchestrator prints a quality advisory because raw layers typically lack curated COMMENTs and dimensional joins.
> - `source_csv` → not reached; the orchestrator stops because no live tables exist.
>
> Production Metric Views always reference Gold; workshop builds may reference Silver/Bronze and should be promoted to Gold for production hardening.

## MCP Tools (from upstream databricks-metric-views)

The `manage_metric_views` MCP tool supports all metric view operations:

| Action | Description |
|--------|-------------|
| `create` | Create a metric view with dimensions and measures |
| `alter` | Update a metric view's YAML definition |
| `describe` | Get the full definition and metadata |
| `query` | Query measures grouped by dimensions |
| `drop` | Drop a metric view |
| `grant` | Grant SELECT privileges to users/groups |

## Quick Start (2 hours)

**What You'll Create:**
1. `metric_views/{view_name}.yaml` — Semantic definitions (dimensions, measures, joins, formats)
2. `create_metric_views.py` — Script reads YAML, creates views with `WITH METRICS LANGUAGE YAML`
3. `metric_views_job.yml` — Asset Bundle job for deployment

**Deploy:** `databricks bundle deploy -t dev && databricks bundle run metric_views_job -t dev`

## Critical Rules

### ⚠️ CRITICAL: Correct SQL Syntax

**Metric views MUST be created using `WITH METRICS LANGUAGE YAML` syntax:**

```python
create_sql = f"""
CREATE OR REPLACE VIEW {fully_qualified_name}
WITH METRICS
LANGUAGE YAML
COMMENT '{view_comment_escaped}'
AS $$
{yaml_str}
$$
"""
```

**Key Requirements:**
1. `WITH METRICS` — Identifies the view as a metric view
2. `LANGUAGE YAML` — Specifies YAML format
3. `AS $$ ... $$` — YAML content wrapped in dollar-quote delimiters
4. No SELECT statement — The YAML definition IS the view definition
5. `version` field — Must be included in each metric view YAML

**❌ WRONG:** Regular view with TBLPROPERTIES (creates regular VIEW, not METRIC_VIEW)

### ⚠️ Modifying: prefer `ALTER VIEW` over `CREATE OR REPLACE`

When **updating** an existing metric view, prefer `ALTER VIEW` — it preserves the view's Unity Catalog permissions (grants) and cascading metadata:

```sql
ALTER VIEW ${catalog}.${gold_schema}.<view_name>
AS $$
{updated_yaml}
$$
```

`CREATE OR REPLACE` (and the drop+create the deploy script uses by default) **deletes the view and therefore its grants and cascading metadata**. Only use replace/drop+create when a CI/CD step re-applies permissions on every deploy (e.g. via the `grant` action). For incremental edits to a live, governed view, always `ALTER`.

### ⚠️ CRITICAL: v1.1 Unsupported Fields

**These fields will cause errors and MUST NOT be used:**

| Field | Error | Action |
|-------|-------|--------|
| `name` | `Unrecognized field "name"` | ❌ NEVER include — name is in CREATE VIEW statement |
| `time_dimension` | `Unrecognized field "time_dimension"` | ❌ Remove entirely |
| `window_measures` | `Unrecognized field "window_measures"` | ❌ Remove the top-level `window_measures:` array. The per-measure `window:` property IS supported in v1.1 (Experimental status; `offset` requires DBR 18.1+). See `references/composability-patterns.md`. |
| `join_type` | Unsupported | ❌ Remove — defaults to LEFT OUTER JOIN |
| `table` (in joins) | `Missing required creator property 'source'` | ✅ Use `source` instead |

### ⚠️ MANDATORY: Pre-Creation Schema Validation

**ALWAYS validate schemas BEFORE creating metric view YAML. 100% of deployment failures are preventable schema issues.**

**Schema Validation Checklist:**
- [ ] Verified source table schema (ran DESCRIBE TABLE or checked YAML)
- [ ] Verified all joined table schemas
- [ ] Created column reference checklist for all tables
- [ ] Validated every dimension `expr` column exists
- [ ] Validated every measure `expr` column exists
- [ ] Validated join key columns exist in both tables
- [ ] Verified no transitive joins (all joins are source → table)
- [ ] For COUNT measures, verified primary key column exists
- [ ] For SCD2 joins, verified `is_current` column exists

See `references/validation-checklist.md` for detailed validation steps.

### ⚠️ CRITICAL: Source Table Selection

**Rule:** Revenue/bookings/transactions → FACT table. Property/host counts → DIMENSION table.

**❌ WRONG:** Revenue from dimension table (under-reports by 4x)
```yaml
source: ${catalog}.${schema}.dim_property  # ❌ Wrong for revenue!
```

**✅ CORRECT:** Revenue from fact table
```yaml
source: ${catalog}.${schema}.fact_booking_daily  # ✅ Correct for revenue!
```

### ⚠️ CRITICAL: Transitive Join Limitations

**Metric Views DO NOT support transitive/chained joins** (where join B's `on` clause references join A instead of `source`).

**How to detect:** If ANY join's `on` clause references a join alias (not `source`), it is transitive and will fail.

**❌ WRONG:** Transitive join (join B references join A)
```yaml
joins:
  - name: dim_property                              # Join A
    source: catalog.schema.dim_property
    'on': source.property_id = dim_property.property_id
  - name: dim_destination                            # Join B
    source: catalog.schema.dim_destination
    'on': dim_property.destination_id = dim_destination.destination_id  # ❌ References dim_property!
```

This fails at plan-time with `UNRESOLVED_COLUMN` because `dim_property` is not visible in `dim_destination`'s `on` scope.

**✅ FIX 1 (Preferred — simplest): Use denormalized columns from existing dimension**

If `dim_property` already has `destination_name` and `destination_country`, reference them directly — no second join needed:
```yaml
# `fields:` is an alias for `dimensions:` introduced in DBR 18.1+; preserve whichever key the YAML already uses.
fields:
  - name: destination_name
    expr: dim_property.destination_name  # ✅ Already in dim_property
  - name: destination_country
    expr: dim_property.destination_country
```

**✅ FIX 2: Snowflake schema (nested joins) — requires DBR 17.1+**
```yaml
joins:
  - name: dim_property
    source: catalog.schema.dim_property
    'on': source.property_id = dim_property.property_id
    joins:  # ✅ Nested under dim_property — snowflake schema
      - name: dim_destination
        source: catalog.schema.dim_destination
        'on': dim_property.destination_id = dim_destination.destination_id
```

**Validation gate:** Before generating YAML, inspect all join `on` clauses. If the left side of any `on` references a join name (not `source`), restructure as nested joins or use denormalized columns.

**Pre-check for Fix 2 (nested joins):** Verify the workspace runtime supports nested joins:

```python
dbr = spark.sql("SELECT current_version()").first()[0]
assert float('.'.join(dbr.split('.')[:2])) >= 17.1, \
    f"Nested joins require DBR 17.1+, got {dbr}. Use Fix 1 or restructure."
```

**If Fix 1 is not feasible** (the intermediate dimension lacks the needed column, e.g., `dim_property` does not have `destination_name`), do NOT silently use Fix 2. Flag the constraint to the user and offer:
- (a) Add the column to the intermediate dimension in the Gold layer design
- (b) Confirm DBR 17.1+ and use nested joins
- (c) Omit the dimension from the Metric View and handle it via TVFs instead

See `references/advanced-patterns.md` for additional snowflake schema examples.

### ⚠️ CRITICAL: Multi-Hop / Snowflake Joins (subquery-source pattern)

Transitive joins aren't the only multi-hop trap. Two other shapes silently produce **wrong numbers** instead of a clean planner error — and both are indistinguishable from valid Metric Views on casual inspection. Treat this section as the canonical reference for any join that must traverse more than one dimension hop.

**Failure mode A (silent row-drop — DBR < 17.1):** Nested joins emitted under `joins:` are ignored by older runtimes. Aggregations run against the un-joined base, so dimensions from the nested table quietly disappear from the GROUP BY. No error surfaces — the Metric View just returns the wrong grain.

**Failure mode B (fan-out cartesian):** Nested joins work on DBR 17.1+ but the join key on the intermediate table (`dim_property.destination_id`) is **not unique**. Every row from `source` fans out over every matching `dim_destination` row, inflating measures. Again: no error — just a wrong total.

#### ❌ Anti-pattern 1 — flat "sibling" join relying on an earlier join's alias

```yaml
# Wrong: dim_destination is a sibling, not nested — and references dim_property.
joins:
  - name: dim_property
    source: catalog.schema.dim_property
    'on': source.property_id = dim_property.property_id
  - name: dim_destination
    source: catalog.schema.dim_destination
    'on': dim_property.destination_id = dim_destination.destination_id  # ❌ transitive
```

Planner behaviour:
- DBR ≥ 17.1: raises `UNRESOLVED_COLUMN` at creation time.
- DBR < 17.1: may silently accept and produce wrong results. **Never rely on the error.**

#### ❌ Anti-pattern 2 — nested join without verifying intermediate uniqueness

```yaml
joins:
  - name: dim_property
    source: catalog.schema.dim_property
    'on': source.property_id = dim_property.property_id
    joins:
      - name: dim_destination
        source: catalog.schema.dim_destination
        'on': dim_property.destination_id = dim_destination.destination_id
# ❌ Wrong if dim_property rows can share a destination_id with dim_destination M:1 ambiguity,
#    OR if dim_destination has multiple rows per destination_id (e.g. SCD2 without is_current filter).
```

Always verify uniqueness before shipping a nested join:

```sql
-- Intermediate table must be 1:1 on the OUTER-facing key:
SELECT property_id, COUNT(*) AS c
FROM catalog.schema.dim_property
GROUP BY property_id HAVING c > 1;  -- must return 0 rows

-- Inner dimension must be 1:1 on the join key (or filtered to is_current):
SELECT destination_id, COUNT(*) AS c
FROM catalog.schema.dim_destination
WHERE is_current = true              -- if SCD2
GROUP BY destination_id HAVING c > 1;  -- must return 0 rows
```

#### ✅ Correct pattern — subquery `source` (pre-join, then treat as one dim)

When nested joins are not available (DBR < 17.1) OR the intermediate table is not uniquely keyed, fold the multi-hop into a **subquery source** that pre-resolves the join off-Metric-View. The Metric View then joins `source` to a single, clean, uniquely-keyed dimension.

```yaml
source: catalog.schema.fact_booking_daily
joins:
  - name: dim_property_enriched
    # Subquery as source — pre-joins dim_property → dim_destination and enforces uniqueness.
    source: |
      (
        SELECT
          p.property_key,
          p.property_id,
          p.property_name,
          d.destination_id,
          d.destination_name,
          d.country
        FROM catalog.schema.dim_property p
        LEFT JOIN catalog.schema.dim_destination d
          ON p.destination_id = d.destination_id
         AND d.is_current = true        -- SCD2 guard
        WHERE p.is_current = true
      )
    'on': source.property_key = dim_property_enriched.property_key
fields:
  - name: property_name
    expr: dim_property_enriched.property_name
  - name: destination_name
    expr: dim_property_enriched.destination_name
  - name: country
    expr: dim_property_enriched.country
```

**Why this is the robust FALLBACK (use only when nested joins are unavailable — DBR < 17.1 — or the intermediate key is not unique):**
- Works on **every** DBR version (no 17.1 dependency).
- The subquery makes uniqueness guarantees explicit — reviewers can see and test them.
- Re-usable: wrap the subquery in a **Gold-layer VIEW** (`dim_property_enriched_v`) and reference it in every Metric View that needs the same enrichment — this also anchors the Gold dependency manifest (see `planning/00-project-planning/SKILL.md`).

> **Default preference (do not over-engineer):** on the workshop runtime (serverless, DBR ≥ 17.1) with 1:1 intermediate keys, **nested joins (Fix 2) are the PREFERRED multi-hop solution** — simpler, no extra Gold view, native to the Metric View. Reach for the subquery-source pattern only as the fallback. Do NOT spend planning cycles designing a subquery workaround when nested joins resolve the path directly.

**Decision ladder for any multi-hop requirement:**
1. Can the intermediate dimension carry the needed attribute directly (denormalize)? → Use Fix 1 (flat join, no second hop).
2. **PREFERRED on the workshop runtime.** Is every intermediate key uniquely 1:1 and is DBR ≥ 17.1? → Use nested joins (Fix 2) and document the uniqueness check in a comment.
3. Only if DBR < 17.1 OR an intermediate key is non-unique → use the **subquery-source fallback above**. Do NOT ship a transitive join and hope for an error.

**Anti-pattern detector — run before deploy:**

```python
import yaml, re
bad = []
for yf in Path("src/semantic/metric_views").rglob("*.yaml"):
    mv = yaml.safe_load(yf.read_text())
    joins = (mv.get("joins") or []) if isinstance(mv, dict) else []
    alias_names = {j["name"] for j in joins}
    for j in joins:
        on_clause = j.get("on", "")
        # Left side of `=` must start with `source.` or be a nested-join alias.
        m = re.match(r"\s*([A-Za-z_][\w.]*)", on_clause)
        left_head = (m.group(1).split(".", 1)[0] if m else "")
        if left_head in alias_names:
            bad.append((str(yf), j["name"], on_clause))
if bad:
    for f, n, o in bad:
        print(f"TRANSITIVE JOIN in {f} :: join '{n}' -> {o}")
    raise RuntimeError(
        "Transitive/flat-sibling joins detected. Restructure as nested "
        "joins (DBR 17.1+) or as subquery-source (preferred)."
    )
```

## Implementation Workflow

### Phase 1: Design (30 min)

**Read:** `references/requirements-template.md`

- [ ] Identify fact table as primary source
- [ ] List dimensions to join (2-5 dimension tables)
- [ ] Define key measures (5-10 measures with aggregation type)
- [ ] List common user questions (guides synonym creation)
- [ ] Map synonyms for each dimension and measure (3-5 each)

### Phase 2: YAML Creation (1 hour)

**Read:** `references/yaml-reference.md` and `references/advanced-patterns.md`

- [ ] Create one YAML file per metric view (filename = view name)
- [ ] Define `source` table (fully qualified with `${catalog}` and `${gold_schema}` placeholders)
- [ ] Add `joins` with `name`, `source`, `'on'` (include `is_current = true` for SCD2)
- [ ] Define dimensions with correct prefix (`source.` or `{join_name}.`)
  - [ ] Business-friendly comments and display names
  - [ ] 3-10 synonyms each (max 10 per field, max 255 chars each)
- [ ] Define measures with correct aggregation (SUM, AVG, COUNT)
  - [ ] Proper formatting (currency, number, percentage)
  - [ ] Comprehensive comments for Genie
  - [ ] 3-10 synonyms each (max 10 per field, max 255 chars each)

### Phase 3: Script & Bundle (30 min)

**Read:** `references/implementation-workflow.md`

- [ ] Validate YAML with `scripts/validate_metric_view.py`
- [ ] Use `scripts/create_metric_views.py` for deployment
- [ ] Configure Asset Bundle job (see `assets/templates/metric-views-job-template.yml`)
- [ ] Add YAML file sync to `databricks.yml`

### Phase 4: Deploy & Test (30 min)

**Read:** `references/validation-queries.md`

- [ ] Deploy: `databricks bundle deploy -t dev`
- [ ] Run: `databricks bundle run metric_views_job -t dev`
- [ ] Verify: `DESCRIBE EXTENDED` shows Type: METRIC_VIEW
- [ ] Test: `SELECT ... MEASURE(\`Total Revenue\`) ... GROUP BY ...`
- [ ] Test with Genie: Ask natural language questions

## Quick Reference

### YAML Structure (v1.1)

```yaml
version: "1.1"
comment: >
  PURPOSE: [One-line description]
  BEST FOR: [Question 1] | [Question 2] | [Question 3]
  NOT FOR: [What to avoid] (use [correct_asset] instead)
  DIMENSIONS: [dim1], [dim2], [dim3]
  MEASURES: [measure1], [measure2], [measure3]
  SOURCE: [fact_table] ([domain] domain)
  JOINS: [dim_table1] ([description])
  NOTE: [Critical caveats]

source: ${catalog}.${gold_schema}.<fact_table>
filter: <sql_boolean_expression>  # Optional: WHERE clause applied to all queries

joins:
  - name: <dim_table_alias>
    source: ${catalog}.${gold_schema}.<dim_table>
    'on': source.<fk> = <dim_table_alias>.<pk> AND <dim_table_alias>.is_current = true
    rely:
      at_most_one_match: true   # Optional. Many-to-one joins only — declares the join does not fan out, so the
                                # analyzer plans more efficiently. NOT validated at runtime: if it fans out,
                                # SUM/COUNT measures return wrong results. Omit if unsure.

# `fields:` is an alias for `dimensions:` (DBR 18.1+); preserve whichever key the YAML already uses.
# A metric view is valid with only dimensions, only measures, or both — measures are NOT mandatory.
# NOTE: the `materialization` block below still requires the `dimensions:` keyword.
fields:
  - name: <dimension_name>
    expr: source.<column>
    comment: <Business description>
    display_name: <User-Friendly Name>
    synonyms: [<alt1>, <alt2>]

measures:
  - name: <measure_name>
    expr: SUM(source.<column>)
    comment: <Business description>
    display_name: <User-Friendly Name>
    format:
      type: currency|number|percentage
      currency_code: USD
      decimal_places:
        type: exact|all
        places: 2
    synonyms: [<alt1>, <alt2>]
```

**Valid format types (exhaustive):**

| Type | Use For | Common Mistake |
|------|---------|----------------|
| `byte` | Data sizes (storage, memory) | — |
| `currency` | Monetary values (revenue, cost) | — |
| `date` | Date-only values | — |
| `date_time` | Timestamp values | — |
| `number` | Counts, averages, decimals, integers | ❌ `decimal`, ❌ `integer` |
| `percentage` | Ratios, rates, percentages | ❌ `percent` |

**⚠️ `percent` is NOT valid** (use `percentage`). **`decimal` is NOT valid** (use `number`).

### Column References

- **Main table columns:** Use `source.` prefix in all `expr` fields
- **Joined table columns:** Use join `name` as prefix (e.g., `dim_store.column_name`)
- **Never reference table names directly:** Use `source.` or `{join_name}.`

### Join Semantics

- Metric view joins use **LEFT OUTER JOIN** semantics by default — `source` (the fact) is the left side, joined dimension tables are the right side.
- Joins are **many-to-one by design**. If a join is actually many-to-many, the engine selects the **first matching row** from the dimension — silently wrong for aggregations. Keep joins many-to-one.
- The engine only joins tables **needed for the query** (based on the selected dimensions/measures), so unused joins add no cost.
- The optional `rely.at_most_one_match: true` hint lets the analyzer optimize filter pushdown for genuine many-to-one joins. It is **NOT validated at runtime** — if the join fans out, SUM/COUNT inflate. Verify cardinality before setting it (below).

**Cardinality verification (gate for `rely.at_most_one_match: true` and any join):**

```sql
-- The join key MUST be unique in the dimension table (0 rows = safe many-to-one).
SELECT <join_key>, COUNT(*) AS c
FROM ${catalog}.${gold_schema}.<dim_table>
WHERE is_current = true            -- include for SCD2 dimensions
GROUP BY <join_key>
HAVING c > 1;                       -- must return 0 rows
```

If this returns rows, the join can fan out: do not set `at_most_one_match`, filter to `is_current`, or pre-aggregate the dimension. A quick `COUNT(*)` before/after adding a join is the fastest fan-out smoke test — if the row count changes, you have a fan-out.

### Join Requirements

- Each join **MUST have** `name`, `source`, and either `'on'` or `using`
- `ON` clause: boolean expression using `source.` for main table, join name for joined table (quote the key: `'on'`). If a reference in an `on` clause has no prefix, it defaults to the joined table.
- `USING` clause: array of column names — use only when both tables share **identical** column names; use `on` for all other cases
- Each first-level join must reference `source` (NOT another join alias — that's transitive)
- For transitive relationships, use nested `joins:` (snowflake schema, DBR 17.1+) or denormalized columns; reference nested columns as `parent_join.child_join.column`
- SCD2 joins must include `AND {dim_table}.is_current = true`
- **MAP type columns are NOT supported** in joined tables

## Core Patterns

### Composability (MEASURE Function)

Metric views support **composability** — building complex metrics by referencing simpler measures via the `MEASURE()` function. Define atomic measures first, then compose derived KPIs:

```yaml
measures:
  - name: total_revenue
    expr: SUM(source.net_revenue)
  - name: order_count
    expr: COUNT(source.order_id)
  - name: avg_order_value
    expr: MEASURE(total_revenue) / MEASURE(order_count)  # ✅ Composed measure
```

**Measure-level filtering** with `FILTER` clause:
```yaml
  - name: fulfilled_orders
    expr: COUNT(1) FILTER (WHERE source.order_status = 'F')
  - name: fulfillment_rate
    expr: MEASURE(fulfilled_orders) / MEASURE(order_count)
    format:
      type: percentage
```

**Best practices:** Define atomic measures (SUM, COUNT, AVG) first; always use `MEASURE()` to reference other measures (never repeat the aggregation logic).

See `references/composability-patterns.md` for full guide including conditional logic, window measures (Experimental, supported in v1.1), and complete examples.

### Level of Detail (Percent-of-Total, Cohorts, Peer Averages)

Some metrics need an aggregate at a **different grain** than the query `GROUP BY` — percent-of-total, percent-of-category, cohort assignment, peer-average comparisons. A plain measure cannot do this because it always resolves at the query grain. Use a **Fixed LOD** (a dimension with `OVER (PARTITION BY ...)`, read with `ANY_VALUE()`) or an **Exclude LOD** (a window measure with `range: all`).

> ⚠️ **Do NOT compute percent-of-total with `MEASURE() / MEASURE()`** — both sides resolve at the query grain, so the ratio is always `1.0`. Use a Fixed LOD + `ANY_VALUE()`:

```yaml
# ❌ WRONG — always 1.0 (both operands at the query GROUP BY level)
- name: pct_wrong
  expr: MEASURE(`revenue`) / MEASURE(`total_revenue`)

# ✅ RIGHT — Fixed LOD dimension (global) + ANY_VALUE() in the measure
fields:
  - name: global_revenue
    expr: SUM(source.net_revenue) OVER ()      # ignores query GROUP BY
measures:
  - name: revenue
    expr: SUM(source.net_revenue)
  - name: pct_of_total
    expr: MEASURE(`revenue`) / ANY_VALUE(`global_revenue`)
    format: { type: percentage, decimal_places: { type: exact, places: 1 } }
```

See `references/level-of-detail.md` for Fixed vs Exclude LOD, percent-of-category, cohort analysis, and constraints.

### Standardized Comment Format (v3.0)

Use structured format for Genie optimization:

```yaml
comment: >
  PURPOSE: Comprehensive cost analytics for Databricks billing and usage analysis.
  
  BEST FOR: Total spend by workspace | Cost trend over time | SKU cost breakdown
  
  NOT FOR: Commit/contract tracking (use commit_tracking) | Real-time cost alerts
  
  DIMENSIONS: usage_date, workspace_name, sku_name, owner, tag_team
  
  MEASURES: total_cost, total_dbus, cost_7d, cost_30d
  
  SOURCE: fact_usage (billing domain)
  
  JOINS: dim_workspace (workspace details), dim_sku (SKU details)
  
  NOTE: Cost values are list prices. Actual billed amounts may differ.
```

### Dimension & Measure Patterns

See `references/advanced-patterns.md` for complete dimension patterns (geographic, product, time), measure patterns (revenue, count, percentage), and a full worked retail example.

## Common Mistakes to Avoid

Top 5 mistakes (with paired wrong/correct examples): wrong syntax (TBLPROPERTIES), unsupported fields (`time_dimension`, `window_measures`), wrong column references, including `name` in YAML, transitive joins.

See `references/advanced-patterns.md` for detailed wrong/correct code examples for each mistake.

## Python Script Error Handling

Key rules: strip `name` before `yaml.dump()`, drop existing VIEW/TABLE before CREATE, track failures and raise `RuntimeError`, verify METRIC_VIEW type via `DESCRIBE EXTENDED`.

See `scripts/create_metric_views.py` for the full working script and `references/implementation-workflow.md` for the detailed error handling patterns.

## Time Estimates

| Metric Views | Design | YAML Creation | Deploy & Test | Total |
|---|---|---|---|---|
| 1 view | 20 min | 30 min | 20 min | ~1 hour |
| 2-3 views | 30 min | 1 hour | 30 min | ~2 hours |
| 5+ views | 1 hour | 2 hours | 30 min | ~3.5 hours |

## Reference Files

- **`references/yaml-reference.md`** — Complete YAML fields, syntax, format options
- **`references/advanced-patterns.md`** — Dimension/measure patterns, joins, snowflake schema, worked examples
- **`references/composability-patterns.md`** — MEASURE() function, FILTER clause, window measures (Experimental, v1.1)
- **`references/level-of-detail.md`** — Fixed/Exclude LOD: percent-of-total, percent-of-category, cohort, peer-average
- **`references/querying-metric-views.md`** — Query syntax: GROUP BY ALL, MEASURE(), HAVING-on-alias, Top-K, casting, agg()
- **`references/validation-checklist.md`** — Pre-creation validation steps
- **`references/requirements-template.md`** — Design template for dimensions, measures, joins
- **`references/implementation-workflow.md`** — Step-by-step creation workflow
- **`references/validation-queries.md`** — SQL queries for deployment verification
- **`references/import-bi-to-metric-view.md`** — BYO lane: Genie Code `/importBI` (Tableau/Power BI) → promote local → governed UC Metric View (formats, 100 MB/volume limit, "Export to a Unity Catalog metric view", aliases→synonyms)
- **`references/analytical-patterns.md`** — advanced measure/dimension cookbook: ranking (dynamic/static/partitioned), semi-additive balances (opening/closing/growth), currency conversion (query-time parameter + FX join), static segmentation (price bands, per-category, config table). Distilled from `uc-semantics-patterns` with TPC-H/TPC-DS fit notes

## External sources (authoritative pattern lookups)

- **[databricks-solutions/uc-semantics-patterns](https://github.com/databricks-solutions/uc-semantics-patterns)** — Databricks' curated Metric View YAML pattern library (Time Intelligence, Semi-additive, Ranking, Currency conversion, Static segmentation), each with a **verified test query + expected output** on TPC-H/TPC-DS. Use as the source-of-truth lookup when a request needs a pattern beyond this skill's shipped set; the distilled highlights live in `references/analytical-patterns.md`.

## Scripts & Assets

- **`scripts/validate_metric_view.py`** — Pre-deployment column reference validation
- **`scripts/create_metric_views.py`** — YAML loading, parameter substitution, METRIC_VIEW verification
- **`assets/templates/metric-view-template.yaml`** — Starter YAML template
- **`assets/templates/metric-views-job-template.yml`** — Asset Bundle job template

## Materialization (Experimental)

Metric views support optional materialization for pre-computed aggregations. Lakeflow Spark Declarative Pipelines orchestrates materialized views, and the query optimizer automatically routes queries to the best materialized view using aggregate-aware query rewriting.

```yaml
materialization:
  schedule: every 6 hours
  mode: relaxed
  materialized_views:
    - name: baseline
      type: unaggregated
    - name: revenue_breakdown
      type: aggregated
      dimensions: [category, color]
      measures: [total_revenue]
```

**Materialized view types:** `unaggregated` (full data) and `aggregated` (pre-computed for specific dimension/measure combinations). Check refresh status with `DESCRIBE TABLE EXTENDED`.

Requires serverless compute enabled. Currently experimental — use for high-query-volume metric views where pre-computation reduces latency.

## Common Issues

| Issue | Solution |
|-------|----------|
| `SELECT *` not supported | Must explicitly list dimensions and use `MEASURE()` for measures |
| "Cannot resolve column" | Dimension/measure names with spaces need backtick quoting |
| JOIN at query time fails | Joins must be in the YAML definition, not in the SELECT query |
| `MEASURE()` required | All measure references must be wrapped: `MEASURE(\`name\`)` (or `agg()` on DBR 18.1+) |
| `HAVING` on a measure fails | Filter on the measure **alias**, not the `MEASURE()` expression |
| Redeploy dropped UC grants | `CREATE OR REPLACE`/drop+create deletes permissions — use `ALTER VIEW` to preserve them (see Critical Rules) |
| DBR version error | Compute must be on DBR 17.3+ to create or edit metric views (current docs requirement); YAML v1.1 features need 17.2+; legacy v0.1 needs 16.4+ |
| Materialization not working | Requires serverless compute enabled; currently experimental |

See `references/querying-metric-views.md` for the full query syntax guide (`GROUP BY ALL`, HAVING-on-alias, Top-K, casting, `agg()`).

## External References

### Official Documentation
- [Metric Views Overview](https://docs.databricks.com/aws/en/business-semantics/metric-views/)
- [Create and Edit Metric Views](https://docs.databricks.com/aws/en/metric-views/create/sql)
- [Metric View YAML Syntax Reference](https://docs.databricks.com/aws/en/business-semantics/metric-views/yaml-reference)
- [Basic Modeling (sources, dimensions, measures, joins)](https://docs.databricks.com/aws/en/business-semantics/metric-views/basic-modeling)
- [Advanced Techniques (composability, window measures, materialization)](https://docs.databricks.com/aws/en/business-semantics/metric-views/advanced-techniques)
- [Tutorial: Build a complete metric view with joins](https://docs.databricks.com/aws/en/business-semantics/metric-views/tpch-example)
- [Manage Metric Views](https://docs.databricks.com/aws/en/business-semantics/metric-views/manage)
- [Query Metric Views](https://docs.databricks.com/aws/en/business-semantics/metric-views/query)
- [Agent Metadata in Metric Views](https://docs.databricks.com/aws/en/business-semantics/agent-metadata)

### Related Skills
- `databricks-table-valued-functions` — TVF patterns for Genie
- `genie-space-patterns` — Genie Space setup
- `databricks-aibi-dashboards` — AI/BI dashboard patterns

## Version History

- **v5.2** (Jun 6, 2026) — Reconciled against the authoritative Databricks `using-metric-views` skill. Corrected window measures: they are supported in **v1.1** (Experimental), not "v0.1 only" — added `inclusive`/`exclusive` anchor modifiers and MTD example. Added `references/level-of-detail.md` (Fixed/Exclude LOD, percent-of-total via `ANY_VALUE()`, cohort) and `references/querying-metric-views.md` (`GROUP BY ALL`, HAVING-on-alias, Top-K, casting, `agg()` alias). Added join semantics (LEFT OUTER, many-to-one, first-matching-row), cardinality-verification query, and `ALTER VIEW` vs `CREATE OR REPLACE` governance (grant-preserving ALTER path in `create_metric_views.py`). Clarified `fields` is a DBR 18.1+ alias for `dimensions` and that measures are optional.
- **v5.1** (Apr 27, 2026) — Refreshed prerequisites and Common Issues for the current docs requirement (DBR 17.3+ for `CAN USE` on metric view creation/edit). Migrated External Documentation links and `upstream_sources` URLs to the current `/business-semantics/metric-views/...` paths (overview, yaml-reference, basic-modeling, advanced-techniques, manage, agent-metadata).
- **v5.0** (Feb 2026) — Expanded transitive joins with inline fixes; exhaustive format type table (6 types); composability (MEASURE function) patterns; FILTER clause; USING join clause; filter top-level field; window measures clarification (Experimental v0.1); materialization expansion; progressive disclosure restructure (Notes to Carry Forward + Next Step); 7 upstream_sources from official docs; new composability-patterns.md reference
- **v4.0** (Feb 2026) — Merged prompt content: Quick Start, implementation workflow, requirements template, creation script, validation queries, worked examples, common mistakes with paired examples
- **v3.0** (Dec 19, 2025) — Standardized structured comment format
- **v2.0** (Dec 16, 2025) — Genie optimization patterns from production post-mortem
- **v1.0** (Oct 2025) — Initial rule based on metric view deployment learnings

## Metric Views Notes to Carry Forward

After completing metric view creation, carry these notes to the next worker:
- **Metric View names and paths:** List of all created MVs with YAML file paths
- **Grain per view:** Which fact table sources each MV
- **Measure counts:** Number of dimensions and measures per MV
- **Validation status:** Which MVs passed schema validation, any unresolved issues
- **Composability notes:** Any composed measures using MEASURE() that downstream workers should know about

## Next Step

After metric views are deployed and validated, proceed to:
**`semantic-layer/02-databricks-table-valued-functions/SKILL.md`** — Create TVFs for Genie Spaces using the Gold tables referenced by your metric views.
