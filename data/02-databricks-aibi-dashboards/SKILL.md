---
name: databricks-aibi-dashboards
description: Production-grade patterns for Databricks AI/BI (Lakeview) dashboards. Prevents visualization errors, deployment failures, and maintenance issues through widget-query alignment, number formatting, parameter configuration, monitoring table patterns, chart scale properties, and automated deployment workflows. Includes pivot tables with hierarchy drill-down and ratio metrics, point/choropleth maps, sankey diagrams, waterfall and histogram charts, cross-filtering and drill-through patterns, filter defaultSelection/disallowAll configuration, disaggregated vs aggregated query modes, and complete JSON templates for all widget types.
clients: [ide_cli, genie_code]
bundle_resource: dashboards
deploy_verb: bundle_deploy
deploy_note: "AI/BI (Lakeview) dashboards deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code); .lvdash.json content MUST be base64(ascii) on import (B6) and every widget fieldName must match a SQL alias. On Genie Code, write the generated .lvdash.json under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`, e.g. `resources/`), not a bare relative path \u2014 relative paths resolve against the page CWD (see `skills/genie-code-environment` \u00a78)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "4.2"
  domain: monitoring
  role: worker
  pipeline_stage: 7
  pipeline_stage_name: observability
  called_by:
    - observability-setup
  standalone: true
  keywords:
    - databricks
    - ai/bi
    - lakeview
    - dashboards
    - monitoring
    - visualization
    - deployment
    - widget configuration
    - sql validation
    - automation
    - production-grade
  last_verified: "2026-04-16"
  volatility: medium
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-aibi-dashboards/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Databricks AI/BI Dashboards

## Overview

This skill provides comprehensive patterns for building production-grade Databricks AI/BI (Lakeview) dashboards. These patterns were developed from 100+ production deployments and prevent common visualization errors, deployment failures, and maintenance issues.

**Core Philosophy: Self-Service Analytics**

AI/BI Lakeview dashboards provide **visual analytics for business users** with **no SQL required**. This skill emphasizes:

- ✅ **Visual insights** for non-technical users
- ✅ **Consistent metrics** across the organization
- ✅ **Self-service analytics** without coding knowledge
- ✅ **Professional, branded** appearance
- ✅ **Automated deployment** with validation
- ✅ **Error prevention** through pre-deployment checks

**Key Capabilities:**

- Widget-query column alignment validation
- Number formatting rules (percentages, currency, plain numbers)
- Parameter configuration (time ranges, multi-select, text input)
- Monitoring table query patterns (window structs, CASE pivots, custom drift metrics)
- Chart configuration (pie, bar, line, area, table, pivot, point map, choropleth, sankey)
- **Pivot tables** with hierarchy expand/collapse and non-additive ratio metric support
- **Map visualizations** (point maps with lat/lng, choropleth by region)
- **disaggregated vs aggregated** query mode patterns for correct metric rollups
- Pre-deployment SQL validation (90% reduction in dev loop time)
- UPDATE-or-CREATE deployment pattern (preserves URLs and permissions)
- Variable substitution (no hardcoded schemas)
- Complete JSON templates for all widget types
- Phase-by-phase implementation guide
- **Production example** - Complete Jobs System Tables Dashboard demonstrating all patterns

## When to Use This Skill

Use this skill when:

- **Building AI/BI dashboards** - Creating new dashboards with proper widget configurations
- **Troubleshooting visualization errors** - Fixing "no fields to visualize", empty charts, or formatting issues
- **Deploying dashboards via API** - Automating dashboard deployment with UPDATE-or-CREATE pattern
- **Validating dashboard queries** - Pre-deployment SQL validation to catch errors before deployment
- **Querying monitoring tables** - Accessing Lakehouse Monitoring profile and drift metrics
- **Configuring parameters** - Setting up time ranges, filters, and multi-select parameters
- **Planning dashboard projects** - Using templates to gather requirements and plan implementation
- **Onboarding new developers** - Teaching AI/BI dashboard best practices with working examples

## Mandatory Skill Dependencies

**Before building dashboard datasets, determine which query pattern the task requires:**

| Query Pattern | Required Pre-Read | Trigger |
|---|---|---|
| `MEASURE()` against Metric Views | **MUST READ** `semantic-layer/01-metric-views-patterns/SKILL.md` + [references/metric-view-dashboard-queries.md](references/metric-view-dashboard-queries.md) | User mentions "MEASURE()", "Metric View", or semantic layer queries |
| Direct Gold table SQL | No additional skill needed | Querying fact/dimension tables directly |
| Monitoring / system table queries | **MUST READ** `monitoring/01-lakehouse-monitoring-comprehensive/SKILL.md` | Dashboard includes monitoring widgets |

**Always load these common skills first (per AGENTS.md):**
- `skills/databricks-expert-agent/SKILL.md` — "Extract Don't Generate" principle, core SA behavior
- `common/naming-tagging-standards/SKILL.md` — naming conventions for dashboards and datasets

> **Plan addendum filename:** Dashboards are always planned in `plans/phase1-addendum-1.5-aibi-dashboards.md`. See [`planning/00-project-planning/assets/addendum-numbering.md`](../../planning/00-project-planning/assets/addendum-numbering.md) for the canonical numbering table. The legacy name `phase1-addendum-1.1-dashboards.md` is forbidden — if you see it anywhere, replace it with `1.5-aibi-dashboards.md`.

**Complementary installed skills** (check `available_skills` list):
- `databricks-lakeview-dashboard` — comprehensive widget JSON patterns for 16+ chart types, **mandatory "TEST EVERY QUERY" validation workflow**
- `databricks-lakeview-dashboard-analyzer` — analyzing existing dashboards for patterns

## 🚀 Quick Start (2 Hours)

**Goal:** Create visual dashboards with AI-powered insights for business users

**What You'll Create:**
1. SQL queries from Metric Views or Gold tables
2. AI/BI Dashboard via UI (drag-and-drop layout)
3. Auto-refresh schedule

**Fast Track (UI-Based):**
```
1. Navigate to: Databricks Workspace → Dashboards → Create AI/BI Dashboard
2. Add Data → Query Metric View or Gold table
3. Add Visualizations:
   - Counter tiles for KPIs (Total Revenue, Units, Transactions)
   - Bar charts for comparisons (Revenue by Store)
   - Line charts for trends (Daily Revenue Trend)
   - Tables for drill-down (Top Products Detail)
4. Add Filters (Date Range, Store, Category)
5. Configure Layout (Canvas: 1280px wide, tiles sized to fit)
6. Enable Auto-refresh (Hourly/Daily)
7. Share with business users
```

**Query Pattern (Metric Views):**
```sql
-- Use MEASURE() function for semantic metrics
SELECT 
  store_name,
  MEASURE(`Total Revenue`) as revenue,
  MEASURE(`Total Units`) as units,
  MEASURE(`Transaction Count`) as transactions
FROM sales_performance_metrics
WHERE transaction_date BETWEEN :start_date AND :end_date
ORDER BY revenue DESC
LIMIT 10
```

**Best Practices:**
- ✅ **Use Metric Views** (not raw tables) for consistent metrics
- ✅ **Add filters** for date range, key dimensions
- ✅ **Counter tiles** for top KPIs (large, prominent)
- ✅ **Charts** for trends and comparisons
- ✅ **Auto-refresh** for near real-time dashboards

**Output:** Professional dashboard with AI-powered insights

**Time Estimate:** 2-4 hours for complete dashboard

**Production Example:** See `references/Jobs System Tables Dashboard.lvdash.json` for a complete working example demonstrating all patterns from this skill.

---

## 📋 Project Planning Template

**Use this template to gather requirements before building your dashboard.**

### Dashboard Purpose

- **Dashboard Name:** _________________ (e.g., "Sales Performance Dashboard", "Patient Outcomes Dashboard")
- **Audience:** _________________ (e.g., "Sales Managers", "Hospital Administrators", "Finance Team")
- **Update Frequency:** [ ] Real-time [ ] Hourly [ ] Daily [ ] Weekly
- **Primary Goal:** _________________ (e.g., "Track daily KPIs", "Monitor data quality", "Analyze trends")

### Data Sources

- **Catalog:** _________________ (e.g., my_catalog)
- **Schema:** _________________ (e.g., my_project_gold)
- **Primary Data Source:** [ ] Metric View [ ] Gold Fact Table [ ] System Tables
- **Table/View Name:** _________________ (e.g., sales_performance_metrics, fact_sales_daily)

### KPIs to Display (3-6 key metrics)

| # | KPI Name | Source Field | Format |
|---|----------|--------------|--------|
| 1 | Total Revenue | SUM(net_revenue) | Currency (USD) |
| 2 | _____________ | ______________ | _____________ |
| 3 | _____________ | ______________ | _____________ |
| 4 | _____________ | ______________ | _____________ |

**Example - Retail:**
- Total Revenue (Currency), Total Units (Number), Transaction Count (Number)

**Example - Healthcare:**
- Patient Count (Number), Readmission Rate (Percentage), Avg Length of Stay (Number)

**Example - Finance:**
- Transaction Volume (Number), Total Amount (Currency), Fraud Rate (Percentage)

### Filters Required

| Filter Name | Type | Values Source |
|------------|------|---------------|
| Date Range | Date Range | start_date, end_date |
| __________ | Single Select | Dimension table |
| __________ | Multi Select | Dimension table |

**Common Filters:**
- Date Range (always include)
- Location/Store/Facility (dimension)
- Category/Type (dimension)
- Status/State (dimension)

### Charts to Include (3-5 visualizations)

| # | Chart Type | Purpose | Data |
|---|-----------|---------|------|
| 1 | Line Chart | Revenue Trend | Daily revenue over time |
| 2 | Bar Chart | Top 10 by metric | Category comparison |
| 3 | _________ | ______________ | __________________ |
| 4 | _________ | ______________ | __________________ |

**Chart Types Available:**
- Line Chart (trends over time)
- Bar Chart (category comparisons)
- Pie Chart (distribution)
- Pivot Table (hierarchical drill-down with expand/collapse)
- Table (detailed flat data)
- Point Map (lat/lng store-level data)
- Choropleth Map (geographic aggregations by region)
- Sankey (flow/relationship diagrams)
- Counter/KPI (single metric)

### Dashboard Pages

| Page Name | Purpose | Widgets |
|-----------|---------|---------|
| Overview | High-level KPIs | 6 KPIs + 2 charts |
| Details | Detailed analysis | 1 table + 2 charts |
| Global Filters | Cross-page filters | Date, dimensions |

### Input Required Summary

- Gold layer tables or Metric Views
- KPI requirements (metrics to display)
- Filter requirements (date range, dimensions)
- Visualization preferences (charts, tables)

---

## Quick Reference

### Top 10 Critical Rules

| Rank | Issue | Prevention |
|------|-------|------------|
| 1 | **Lakeview JSON Format** | Datasets MUST use `queryLines` (array) + `catalog` + `schema` — NOT `query` (string). Textboxes MUST use `multilineTextboxSpec.lines` — NOT `textbox_spec`. Violating this causes ALL visuals to error. |
| 2 | **Dataset `columns` for Hierarchy Pivots** | Deep hierarchy pivots with `cubeGroupingSets` MUST use dataset `columns` array for ratio calculations + `MEASURE()` references in widget query + `cell` encodings (Pattern A). Do NOT use `values` encoding with `cubeGroupingSets`. |
| 3 | Widget-Query Column Mismatch | Always use explicit SQL aliases matching widget `fieldName` |
| 4 | Incorrect Number Formatting | Return raw numbers, not formatted strings |
| 5 | Missing Parameter Definitions | Define ALL parameters in dataset's `parameters` array |
| 6 | Ratio Metrics in Pivots | Use `disaggregated: false`. **Always prefer Pattern A** (dataset `columns` + `MEASURE()` + `cell` encoding) — it works in both the UI editor/draft mode and published view. Pattern B (inline expressions + `values` encoding) only renders when published and is invisible in the UI draft editor. Neither pattern uses `transform`. |
| 7 | Monitoring Table Schema | Use `CASE` pivots on `column_name`, access `window.start` |
| 8 | Map Coordinates Must Be Numeric | CAST lat/lng to DOUBLE upstream; STRING coordinates render blank maps |
| 9 | Metric View Column References | Use bare dimension `name` in queries — not `source.col` or `dim.col` prefixes |
| 10 | Bundle Deploy vs UI Draft | Bundle deploy updates published version; use API PATCH + publish to overwrite UI draft state |

### Widget-Query Alignment

**Rule:** Widget `fieldName` MUST exactly match query output column alias.

```sql
-- ✅ CORRECT
SELECT COUNT(*) AS total_queries FROM ...
-- Widget: "fieldName": "total_queries"

-- ❌ WRONG
SELECT COUNT(*) AS query_count FROM ...
-- Widget: "fieldName": "total_queries"  -- MISMATCH!
```

### Number Formatting

| Format Type | Expects | Example |
|-------------|---------|---------|
| `number-plain` | Raw number | `1234` → `1,234` |
| `number-percent` | 0-1 decimal (×100) | `0.85` → `85%` |
| `number-currency` | Raw number | `1234.56` → `$1,234.56` |

**Never use:** `FORMAT_NUMBER()`, `CONCAT('$', ...)`, or `CONCAT(..., '%')` in queries.

### Monitoring Table Patterns

```sql
-- ✅ CORRECT - Access window struct
SELECT window.start AS window_start FROM monitoring_table
WHERE window.start BETWEEN :time_range.min AND :time_range.max

-- ✅ CORRECT - CASE pivot for generic metrics
SELECT 
  window.start AS window_start,
  MAX(CASE WHEN column_name = 'success_rate' THEN avg END) AS success_rate_pct
FROM fact_job_run_timeline_profile_metrics
WHERE window.start BETWEEN :time_range.min AND :time_range.max
GROUP BY window.start

-- ✅ CORRECT - Custom drift metrics are direct columns
SELECT 
  window.start AS window_start,
  success_rate_drift,  -- Direct column!
  cost_drift_pct       -- Direct column!
FROM fact_job_run_timeline_drift_metrics
WHERE column_name = ':table' AND drift_type = 'CONSECUTIVE'
```

### Chart Scale Requirements

**Pie Charts:**
```json
{
  "encodings": {
    "color": { "fieldName": "category", "scale": { "type": "categorical" } },
    "angle": { "fieldName": "value", "scale": { "type": "quantitative" } }
  }
}
```

**Bar Charts:**
```json
{
  "encodings": {
    "x": { "fieldName": "category", "scale": { "type": "categorical" } },
    "y": { "fieldName": "value", "scale": { "type": "quantitative" } }
  }
}
```

---

## Critical Rules (Production-Grade)

### ⚠️ CRITICAL PRINCIPLES

**These are non-negotiable for production dashboards:**

- ✅ **12-Column Grid:** Widths are 1–12; each row should fill width=12 with no gaps. Add `"layoutVersion": "GRID_V1"` to every page.
- ✅ **Version Specs:** KPIs use v2, Charts use v3, Tables use v2, Pivots use v3, Choropleth Map (`choropleth-map`) uses v1, Symbol Map (`symbol-map`) uses v2
- ✅ **Global Filters:** Cross-dashboard filtering on a dedicated page
- ✅ **DATE Parameters:** Static dates, not DATETIME with dynamic expressions
- ✅ **Proper JOINs:** Include workspace_id AND entity ID
- ❌ **No gaps in a row:** Widget widths in a row must sum to 12, never leave a partial row
- ❌ **No Assumed Field Names:** Verify system table schemas

**Why This Matters:**
- Visual insights for non-technical users
- Consistent metrics across the organization
- Self-service analytics (no SQL required)
- Professional, branded appearance

---

### 1. Grid System (12-Column)

#### ⚠️ AI/BI uses a 12-Column Grid

AI/BI dashboards use a flexible **12-column grid** (`layoutVersion: "GRID_V1"`). You subdivide it into
3, 4, or 6 visual columns depending on density — but the underlying width unit is always out of **12**.
The #1 cause of widget snapping issues is rows that don't sum to 12 (gaps) or that assume a 6-unit grid.

```json
{
  "position": {
    "x": 0,      // Column position: 0-11 (12-column grid)
    "y": 0,      // Row position: any positive integer
    "width": 6,  // Width: 1-12 (widths in a row must sum to 12, no gaps)
    "height": 6  // Height: row units (KPIs 3-4, charts 5-6, tables 5-8)
  }
}
```

> **"6-column" is a subdivision choice, not the grid.** A dense technical dashboard divides the 12-grid
> into six 2-wide columns; an executive dashboard uses three 4-wide columns. Either way `width` is out of 12.

#### Grid Layout Patterns

```json
// Two widgets side-by-side (each 6 = half of 12)
{"x": 0, "y": 0, "width": 6, "height": 6}  // Left
{"x": 6, "y": 0, "width": 6, "height": 6}  // Right

// Three widgets across (each 4 = a third)
{"x": 0, "y": 0, "width": 4, "height": 6}  // Left
{"x": 4, "y": 0, "width": 4, "height": 6}  // Center
{"x": 8, "y": 0, "width": 4, "height": 6}  // Right

// KPI row (6 counters, width 2 each = 12)
{"x": 0,  "y": 0, "width": 2, "height": 3}
{"x": 2,  "y": 0, "width": 2, "height": 3}
{"x": 4,  "y": 0, "width": 2, "height": 3}
{"x": 6,  "y": 0, "width": 2, "height": 3}
{"x": 8,  "y": 0, "width": 2, "height": 3}
{"x": 10, "y": 0, "width": 2, "height": 3}

// Full-width chart / table
{"x": 0, "y": 0, "width": 12, "height": 6}
```

#### Common Height Values

| Widget Type | Height |
|------------|--------|
| Filters | 1-2 |
| KPI Counters | 2 |
| Charts (standard) | 6 |
| Charts (large) | 9 |
| Tables | 6+ |

---

### 2. Widget-Query Column Alignment

**MUST:** Widget `fieldName` exactly matches query output alias.

**Common Mismatches:**
- Widget expects `total_queries`, query returns `query_count` → Alias as `total_queries`
- Widget expects `warehouse_name`, query returns `compute_type` → Alias as `warehouse_name`
- Widget expects `unique_users`, query returns `distinct_users` → Alias as `unique_users`

**Validation:** Use `validate_widget_encodings.py` script before deployment.

---

### 3. Number Formatting

**MUST:** Return raw numbers, let widgets format them.

**Rules:**
- Percentages: Return 0-1 decimal (e.g., `0.85` for 85%)
- Currency: Return raw numeric (e.g., `1234.56` for $1,234.56)
- Never use `FORMAT_NUMBER()` or string concatenation in queries

**Example:**
```sql
-- ✅ CORRECT - Return raw decimal
SELECT 
  COUNT(CASE WHEN status = 'success' THEN 1 END) * 1.0 / COUNT(*) AS success_rate
FROM job_runs
-- Returns: 0.85 → Widget displays as "85%"

-- ❌ WRONG - Formatted string
SELECT 
  CONCAT(ROUND(success_count * 100.0 / total_count, 2), '%') AS success_rate
FROM job_runs
-- Returns: "85.00%" → Widget cannot parse
```

---

### 4. Parameter Configuration

**MUST:** Define ALL parameters in dataset's `parameters` array.

#### Time Range Pattern

```json
{
  "keyword": "time_range",
  "dataType": "DATETIME_RANGE",
  "defaultSelection": {
    "range": {
      "min": { "dataType": "DATETIME", "value": "now-30d/d" },
      "max": { "dataType": "DATETIME", "value": "now/d" }
    }
  }
}
```

**SQL Access:**
```sql
WHERE date BETWEEN :time_range.min AND :time_range.max
```

#### Date Parameters (Static Dates)

##### ✅ Correct: DATE with Static Values

```json
{
  "displayName": "Start Date",
  "keyword": "start_date",
  "dataType": "DATE",
  "defaultSelection": {
    "values": {
      "dataType": "DATE",
      "values": [{"value": "2024-01-01"}]
    }
  }
}
```

##### ❌ Wrong: DATETIME with Dynamic Expressions

```json
// This will NOT work
{
  "dataType": "DATETIME",
  "values": [{"value": "now-12M/M"}]
}
```

---

### 5. Monitoring Table Schema

**MUST:** Use correct access patterns for monitoring tables.

#### Window Struct

- Use `window.start` not `window_start`
- Access as `window.start AS window_start`

#### Generic Metrics

- Use `CASE` pivot on `column_name` field
- Pattern: `MAX(CASE WHEN column_name = 'metric_name' THEN avg END) AS metric_name`

#### Custom Drift Metrics

- Stored as **direct columns** (not in `avg_delta`)
- Filter: `WHERE column_name = ':table' AND drift_type = 'CONSECUTIVE'`

**Complete Example:**
```sql
-- Generic metrics from profile table
SELECT 
  window.start AS window_start,
  MAX(CASE WHEN column_name = 'row_count' THEN avg END) AS avg_row_count,
  MAX(CASE WHEN column_name = 'null_count' THEN avg END) AS avg_null_count
FROM ${catalog}.${gold_schema}_monitoring.fact_usage_profile_metrics
WHERE window.start BETWEEN :time_range.min AND :time_range.max
  AND slice_key IS NULL
GROUP BY window.start
ORDER BY window.start

-- Custom drift metrics (direct columns)
SELECT 
  window.start AS window_start,
  success_rate_drift,
  cost_per_dbu_drift
FROM ${catalog}.${gold_schema}_monitoring.fact_usage_drift_metrics
WHERE column_name = ':table' 
  AND drift_type = 'CONSECUTIVE'
  AND window.start BETWEEN :time_range.min AND :time_range.max
ORDER BY window.start
```

---

### 6. Chart Scale Properties

**MUST:** Add explicit `scale` to chart encodings.

#### Required Scales

**Pie Charts:**
- `color.scale: categorical`
- `angle.scale: quantitative`

**Bar Charts:**
- `x.scale: categorical`
- `y.scale: quantitative`

**Line Charts:**
- `x.scale: temporal`
- `y.scale: quantitative`
- `color.scale: categorical` (for multi-series)

**Area Charts:**
- `x.scale: temporal`
- `y.scale: quantitative`
- `color.scale: categorical` (for multi-series)

---

## Complete Widget Specifications

### KPI Counter (Version 2)

```json
{
  "widget": {
    "name": "kpi_total_revenue",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "kpi_totals",
          "fields": [
            {"name": "total_revenue", "expression": "`total_revenue`"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 2,
      "widgetType": "counter",
      "encodings": {
        "value": {
          "fieldName": "total_revenue",
          "displayName": "Total Revenue",
          "booleanValues": ["False", "True"]
        }
      },
      "frame": {
        "showTitle": true,
        "title": "Total Revenue",
        "showDescription": true,
        "description": "Total sales revenue for selected period"
      }
    }
  },
  "position": {"x": 0, "y": 2, "width": 4, "height": 3}
}
```

**⚠️ Note:** KPIs use version 2. Do NOT include `period` in encodings.

**Widget version summary:** KPIs=v2, Charts (bar/line/pie/area/scatter)=v3, Pivots=v3, Tables=v2, Sankey=v1, Filters=v2, **Choropleth Map=v1** (`choropleth-map`), **Symbol/Point Map=v2** (`symbol-map`).

---

### Bar Chart (Version 3)

```json
{
  "widget": {
    "name": "chart_revenue_by_category",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "revenue_by_category",
          "fields": [
            {"name": "category", "expression": "`category`"},
            {"name": "revenue", "expression": "`revenue`"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "bar",
      "encodings": {
        "x": {
          "fieldName": "category",
          "displayName": "Category",
          "scale": {"type": "categorical"}
        },
        "y": {
          "fieldName": "revenue",
          "displayName": "Revenue",
          "scale": {"type": "quantitative"}
        }
      },
      "frame": {
        "showTitle": true,
        "title": "Revenue by Category",
        "showDescription": true,
        "description": "Sales revenue breakdown by product category"
      }
    }
  },
  "position": {"x": 6, "y": 4, "width": 6, "height": 6}
}
```

---

### Line Chart (Version 3)

```json
{
  "widget": {
    "name": "chart_revenue_trend",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "revenue_trend",
          "fields": [
            {"name": "transaction_date", "expression": "`transaction_date`"},
            {"name": "revenue", "expression": "`revenue`"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "line",
      "encodings": {
        "x": {
          "fieldName": "transaction_date",
          "displayName": "Date",
          "scale": {"type": "temporal"}
        },
        "y": {
          "fieldName": "revenue",
          "displayName": "Revenue",
          "scale": {"type": "quantitative"}
        }
      },
      "frame": {
        "showTitle": true,
        "title": "Revenue Trend",
        "showDescription": true,
        "description": "Daily revenue over time"
      }
    }
  },
  "position": {"x": 0, "y": 4, "width": 6, "height": 6}
}
```

---

### Pie Chart (Version 3)

```json
{
  "widget": {
    "name": "chart_revenue_distribution",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "revenue_by_category",
          "fields": [
            {"name": "category", "expression": "`category`"},
            {"name": "revenue", "expression": "`revenue`"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "pie",
      "encodings": {
        "angle": {
          "fieldName": "revenue",
          "displayName": "Revenue",
          "scale": {"type": "quantitative"}
        },
        "color": {
          "fieldName": "category",
          "displayName": "Category",
          "scale": {"type": "categorical"}
        }
      },
      "frame": {
        "showTitle": true,
        "title": "Revenue Distribution",
        "showDescription": true,
        "description": "Revenue share by category"
      }
    }
  },
  "position": {"x": 0, "y": 10, "width": 6, "height": 6}
}
```

---

### Table Widget (Version 2)

```json
{
  "widget": {
    "name": "table_sales_detail",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "sales_detail",
          "fields": [
            {"name": "store_name", "expression": "`store_name`"},
            {"name": "product", "expression": "`product`"},
            {"name": "revenue", "expression": "`revenue`"},
            {"name": "units", "expression": "`units`"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 2,
      "widgetType": "table",
      "encodings": {
        "columns": [
          {"fieldName": "store_name", "title": "Store"},
          {"fieldName": "product", "title": "Product"},
          {
            "fieldName": "revenue", 
            "title": "Revenue",
            "type": "number"
          },
          {"fieldName": "units", "title": "Units"}
        ]
      },
      "frame": {
        "showTitle": true,
        "title": "Sales Detail",
        "showDescription": true,
        "description": "Detailed sales by store and product"
      }
    }
  },
  "position": {"x": 0, "y": 16, "width": 12, "height": 6}
}
```

---

### Pivot Table (Version 3)

Pivot tables display hierarchical data with expand/collapse drill-down (released Feb 2026). Use for Power BI matrix visual equivalents.

**Two query modes** — the choice of `disaggregated` determines how aggregation works:

- `disaggregated: true` — Raw rows flow to the pivot; the pivot applies `transform` (SUM, AVG, etc.) at each hierarchy level. Use for **additive measures only** (totals, counts).
- `disaggregated: false` — Widget query fields contain aggregate expressions (SUM, computed ratios); the visualization controls the GROUP BY. Use when you need **ratio metrics** (averages, percentages) that must recompute at each hierarchy level.

#### Pivot with Additive Measures Only (disaggregated: true)

```json
{
  "widget": {
    "name": "pivot_hierarchy_additive",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_hierarchy",
          "fields": [
            {"name": "region", "expression": "`region`"},
            {"name": "market", "expression": "`market`"},
            {"name": "store", "expression": "`store`"},
            {"name": "revenue", "expression": "`revenue`"},
            {"name": "stores", "expression": "`stores`"}
          ],
          "disaggregated": true
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "pivot",
      "encodings": {
        "rows": [
          {"fieldName": "region", "displayName": "Region"},
          {"fieldName": "market", "displayName": "Market"},
          {"fieldName": "store", "displayName": "Store"}
        ],
        "values": [
          {"fieldName": "stores", "displayName": "Store#", "transform": "SUM"},
          {"fieldName": "revenue", "displayName": "Revenue", "transform": "SUM"}
        ]
      },
      "frame": {
        "showTitle": true,
        "title": "Hierarchy Drill-Down"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 12, "height": 8}
}
```

#### Pivot with Ratio Metrics — Two Patterns

Non-additive ratio metrics (e.g., avg_revenue = total_revenue / store_count) must recompute at each hierarchy level. Two working patterns exist:

##### Pattern A: Dataset `columns` + `MEASURE()` (for deep hierarchy drill-down)

Use when you need `cubeGroupingSets` for expand/collapse. Define custom calculations on the **dataset** via a `columns` array, then reference via `MEASURE()` in the widget query:

**Dataset** (note the `columns` array):
```json
{
  "name": "ds_hierarchy",
  "displayName": "Store Hierarchy",
  "queryLines": ["SELECT region, market, store_id,\n", "  MEASURE(store_count) AS stores,\n", "  MEASURE(total_revenue) AS revenue,\n", "  MEASURE(store_day_count) AS store_days\n", "FROM catalog.schema.mv_store_metrics\n", "GROUP BY ALL"],
  "columns": [
    {"displayName": "Store#", "description": "Count of stores", "expression": "SUM(`stores`)"},
    {"displayName": "Avg Revenue", "description": "Average revenue per store-day", "expression": "SUM(`revenue`) / NULLIF(SUM(`store_days`), 0)"}
  ],
  "catalog": "my_catalog",
  "schema": "my_schema"
}
```

**Widget**:
```json
{
  "widget": {
    "name": "pivot_hierarchy_ratios_a",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_hierarchy",
          "fields": [
            {"name": "region", "expression": "`region`"},
            {"name": "market", "expression": "`market`"},
            {"name": "store_id", "expression": "`store_id`"},
            {"name": "measure(Store#)", "expression": "MEASURE(`Store#`)"},
            {"name": "measure(Avg Revenue)", "expression": "MEASURE(`Avg Revenue`)"}
          ],
          "cubeGroupingSets": {"sets": [{"fieldNames": ["region", "market", "store_id"]}, {}]},
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "pivot",
      "encodings": {
        "rows": [
          {"fieldName": "region", "displayName": "Region"},
          {"fieldName": "market", "displayName": "Market"},
          {"fieldName": "store_id", "displayName": "Store"}
        ],
        "cell": {
          "type": "multi-cell",
          "fields": [
            {"fieldName": "measure(Store#)", "cellType": "text"},
            {"fieldName": "measure(Avg Revenue)", "cellType": "text"}
          ],
          "displayAs": "columns"
        }
      },
      "frame": {"showTitle": true, "title": "Hierarchy with Ratio Metrics"}
    }
  },
  "position": {"x": 0, "y": 0, "width": 12, "height": 8}
}
```

##### Pattern B: Inline Widget Query Expressions (for flat/shallow groupings)

Use when you don't need `cubeGroupingSets`. Define aggregate expressions directly in widget query `fields`:

```json
{
  "widget": {
    "name": "pivot_hierarchy_ratios_b",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_hierarchy_detail",
          "fields": [
            {"name": "region", "expression": "`region`"},
            {"name": "sum_stores", "expression": "SUM(`stores`)"},
            {"name": "avg_revenue", "expression": "SUM(`revenue`) / NULLIF(SUM(`store_days`), 0)"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "pivot",
      "encodings": {
        "rows": [
          {"fieldName": "region", "displayName": "Region"}
        ],
        "values": [
          {"fieldName": "sum_stores", "displayName": "Store#"},
          {"fieldName": "avg_revenue", "displayName": "Avg Revenue"}
        ]
      },
      "frame": {"showTitle": true, "title": "Flat Grouping with Ratios"}
    }
  },
  "position": {"x": 0, "y": 0, "width": 12, "height": 8}
}
```

##### Pattern Comparison

| Feature | Pattern A: Dataset `columns` | Pattern B: Inline Expressions |
|---|---|---|
| Hierarchy drill-down | Yes (`cubeGroupingSets`) | No |
| Custom calculations | Dataset `columns` array | Widget query `fields` |
| Widget references | `MEASURE(\`Display Name\`)` | Direct field names |
| Encoding type | `cell` (multi-cell) | `values` array |
| `transform` property | Not used | Not used |
| **Visible in UI draft mode** | **Yes** — calculations appear in Values panel | **No** — panel is empty in draft, only renders when published |
| Best for | Deep hierarchies (3+ levels) | Flat/shallow groupings (1-2 levels) |
| **Recommendation** | **Always prefer this pattern** | Avoid unless you never need to edit in UI |

**When sourcing from Metric Views**, the additive components come from `MEASURE()` calls:
```sql
SELECT
  region, market, store_id,
  MEASURE(total_revenue) AS revenue,
  MEASURE(store_day_count) AS store_days,
  MEASURE(store_count) AS stores
FROM catalog.schema.mv_store_metrics
GROUP BY region, market, store_id
```

---

### Point Map / Symbol Map (Version 2)

Requires **numeric** latitude/longitude columns (DOUBLE, not STRING). If upstream tables store coordinates as STRING, cast them to DOUBLE in the materialized view layer.

**CRITICAL:** The widget type is `"symbol-map"` (NOT `"point"`), version is `2` (NOT `3`), and coordinates use a nested `coordinates` object.

```json
{
  "widget": {
    "name": "map_store_locations",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_store_points",
          "fields": [
            {"name": "latitude", "expression": "`latitude`"},
            {"name": "longitude", "expression": "`longitude`"},
            {"name": "region", "expression": "`region`"},
            {"name": "revenue", "expression": "`revenue`"}
          ],
          "disaggregated": true
        }
      }
    ],
    "spec": {
      "version": 2,
      "widgetType": "symbol-map",
      "encodings": {
        "coordinates": {
          "latitude": {"fieldName": "latitude"},
          "longitude": {"fieldName": "longitude"}
        },
        "color": {"fieldName": "region", "scale": {"type": "categorical"}},
        "size": {"fieldName": "revenue", "scale": {"type": "quantitative"}},
        "extra": [{"fieldName": "region"}]
      },
      "frame": {
        "showTitle": true,
        "title": "Store Locations"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 8}
}
```

---

### Choropleth Map (Version 1)

**CRITICAL:** The widget type is `"choropleth-map"` (NOT `"choropleth"`), version is `1` (NOT `3`), and the geographic encoding uses a `region` object with `regionType` and `admin0`/`admin1` sub-objects. Queries MUST use `disaggregated: false` with aggregate expressions.

Geographic role values:
- Country by name: `geographicRole: "admin0-name"`
- Country by 2-letter code: `geographicRole: "admin0-unit-code"`
- State/Province by name: use `admin1` with `geographicRole: "admin1-name"`

**State/Province (admin1) choropleths:** When mapping at the state/province level, you MUST include BOTH `admin0` (country) AND `admin1` (state) in the `region` encoding. The `admin0` field provides the country context required for Mapbox to resolve state names. State names must be **full names** (e.g., "California", "Ontario"), not abbreviations ("CA", "ON"). If your source data uses abbreviations, apply a CASE expression in the dataset query to convert them.

**Country-level (admin0) example:**

```json
{
  "widget": {
    "name": "map_choropleth",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_country_sales",
          "fields": [
            {"name": "country_name", "expression": "`country_name`"},
            {"name": "sum(total_sales)", "expression": "SUM(`total_sales`)"}
          ],
          "disaggregated": false
        }
      }
    ],
    "spec": {
      "version": 1,
      "widgetType": "choropleth-map",
      "encodings": {
        "region": {
          "regionType": "mapbox-v4-admin",
          "admin0": {
            "fieldName": "country_name",
            "type": "field",
            "geographicRole": "admin0-name"
          }
        },
        "color": {
          "fieldName": "sum(total_sales)",
          "scale": {"type": "quantitative"}
        },
        "extra": [{"fieldName": "country_name"}]
      },
      "frame": {
        "showTitle": true,
        "title": "Sales by Country"
      }
    }
  },
  "position": {"x": 6, "y": 0, "width": 6, "height": 8}
}
```

**State/Province-level (admin1) example — requires admin0 context:**

```json
{
  "spec": {
    "version": 1,
    "widgetType": "choropleth-map",
    "encodings": {
      "region": {
        "regionType": "mapbox-v4-admin",
        "admin0": {
          "fieldName": "country_name",
          "type": "field",
          "geographicRole": "admin0-name"
        },
        "admin1": {
          "fieldName": "state_full_name",
          "type": "field",
          "geographicRole": "admin1-name"
        }
      },
      "color": {
        "fieldName": "total_sales",
        "scale": {"type": "quantitative"}
      }
    }
  }
}
```

State name CASE pattern for abbreviation-to-full-name conversion in dataset SQL:
```sql
CASE state_abbr
  WHEN 'CA' THEN 'California'
  WHEN 'TX' THEN 'Texas'
  WHEN 'NY' THEN 'New York'
  -- ... all states
END AS state_full_name
```

---

### Filter Widget (Single Select)

```json
{
  "widget": {
    "name": "filter_store",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "store_filter_values",
          "fields": [
            {"name": "store_name", "expression": "`store_name`"}
          ],
          "disaggregated": true
        }
      }
    ],
    "spec": {
      "version": 2,
      "widgetType": "filter-single-select",
      "encodings": {
        "fields": [
          {
            "displayName": "Store",
            "fieldName": "store_name",
            "queryName": "main_query"
          }
        ]
      },
      "frame": {
        "showTitle": true,
        "title": "Store Filter"
      }
    }
  },
  "position": {"x": 0, "y": 0, "width": 3, "height": 2}
}
```

#### Default Selection and `disallowAll`

To set a default value on a single-select filter (e.g., defaulting to "Day" instead of "All"), use the `selection` and `disallowAll` properties. The `defaultSelection` format requires a typed value structure — a bare string array will silently fall back to "All".

**Correct `defaultSelection` format:**
```json
{
  "spec": {
    "version": 2,
    "widgetType": "filter-single-select",
    "selection": {
      "defaultSelection": {
        "values": {
          "dataType": "STRING",
          "values": [{"value": "Day"}]
        }
      }
    },
    "disallowAll": true
  }
}
```

- `disallowAll: true` removes the "All" option, forcing the user to pick one value. Without this, even with a `defaultSelection`, users can revert to "All" and see unfiltered results — which causes double-counting when multiple period rows exist.
- `dataType` must match the column type (`"STRING"`, `"NUMBER"`, etc.).
- Each value is an object: `{"value": "Day"}`, not a bare string.

### Filter Widget (Multi Select)

```json
{
  "widget": {
    "name": "filter_region",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_region_data",
          "fields": [
            {"name": "region", "expression": "`region`"}
          ],
          "disaggregated": true
        }
      }
    ],
    "spec": {
      "version": 2,
      "widgetType": "filter-multi-select",
      "encodings": {
        "fields": [
          {
            "displayName": "Region",
            "fieldName": "region",
            "queryName": "main_query"
          }
        ]
      },
      "frame": {
        "showTitle": true,
        "title": "Filter by Region"
      }
    }
  }
}
```

### Waterfall Chart (Version 3)

Waterfall charts show additive/subtractive contributions to a total — ideal for decomposing "who helped and who hurt?" (e.g., region contribution to total metric change).

```json
{
  "widget": {
    "name": "region_contribution_waterfall",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_region_performance",
          "fields": [
            {"name": "region", "expression": "`region`"},
            {"name": "metric_change", "expression": "`metric_change`"}
          ],
          "disaggregated": true
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "waterfall",
      "encodings": {
        "x": {
          "fieldName": "region",
          "displayName": "Region",
          "scale": {"type": "categorical"}
        },
        "y": {
          "fieldName": "metric_change",
          "displayName": "$ Change",
          "scale": {"type": "quantitative"}
        }
      },
      "frame": {
        "showTitle": true,
        "title": "Region Contribution to Total Change"
      }
    }
  }
}
```

### Histogram (Version 3)

Histograms show distribution of a continuous variable — useful for identifying outliers or skewed metric distributions.

```json
{
  "widget": {
    "name": "revenue_distribution",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ds_store_detail",
          "fields": [
            {"name": "avg_revenue", "expression": "`avg_revenue`"}
          ],
          "disaggregated": true
        }
      }
    ],
    "spec": {
      "version": 3,
      "widgetType": "histogram",
      "encodings": {
        "x": {
          "fieldName": "avg_revenue",
          "displayName": "Avg Revenue per Store",
          "scale": {"type": "quantitative"}
        }
      },
      "frame": {
        "showTitle": true,
        "title": "Revenue Distribution Across Stores"
      }
    }
  }
}
```

---

## Cross-Filtering and Drill-Through Patterns

### Cross-Filtering (Same Page, Automatic)

**Golden Rule:** Charts on the same page sharing the **same `datasetName`** automatically cross-filter when a user clicks a data point. Field-name matching alone is NOT sufficient — the charts must reference the identical dataset.

**How it works:** When a user clicks a bar (region "EAST") on a bar chart using `ds_region_pulse`, every other chart on the same page that also uses `ds_region_pulse` filters to rows where the clicked value matches. No additional configuration is required.

**Shared dataset pattern for maps:** A single store-level dataset can power both a choropleth map and a point/symbol map. The choropleth uses `disaggregated: false` (aggregates to state level) while the symbol map uses `disaggregated: true` (shows individual stores). Clicking a state on the choropleth filters the point map to only that state's stores.

**UNION ALL multi-metric dataset:** To enable cross-filtering between a bar chart and a heatmap showing different metrics, pivot N metrics into rows using UNION ALL:

```sql
SELECT region, 'Revenue %Chg' AS metric, pct_chg_revenue AS metric_value FROM ...
UNION ALL
SELECT region, 'Customer %Chg' AS metric, pct_chg_customers AS metric_value FROM ...
UNION ALL
SELECT region, 'Avg Txn %Chg' AS metric, pct_chg_avg_txn AS metric_value FROM ...
```

### Drill-Through (Cross-Page Navigation)

**How it works:** Right-clicking a data point on a supported chart (bar, pie, scatter, heatmap, histogram, point map, box plot) shows a context menu: "Drill to → [Page Name]". The target page opens with filters auto-populated from the clicked data point.

**Configuration requirement:** The target page MUST have filter widgets whose `datasetName` matches the source chart's dataset AND whose `fieldName` matches the clicked dimension. Matching field names across **different** datasets does NOT enable drill-through.

**Design for both simultaneously:** Cross-filtering happens automatically within a page (same dataset). Drill-through navigates between pages (shared dataset + field on target filter). Plan your dataset topology to support both:
1. Charts that should cross-filter on the same page → share one dataset.
2. Charts that should drill to a target page → the target page needs a filter widget on the same dataset.

### `COUNT(DISTINCT pk_column)` for Store Counts

In dashboard calculated columns (`columns[]`), prefer `COUNT(DISTINCT location_id)` over `SUM(stores)` for store counts. When a filter defaults to "All" and multiple period rows exist per store, `SUM(stores)` double-counts. `COUNT(DISTINCT pk)` remains correct regardless of filter state.

```json
{"displayName": "Store#", "description": "Count of stores", "expression": "COUNT(DISTINCT `location_id`)"}
```

---

## Dashboard Structure Patterns

### Standard Dashboard Layout

```
Page 1: Overview
├── Row 0: Filters (height: 2)
│   ├── Date Range Filter (width: 4)
│   ├── Store Filter (width: 4)
│   └── Product Filter (width: 4)
│
├── Row 2: KPIs (height: 3)
│   ├── Total Revenue (width: 4)
│   ├── Total Units (width: 4)
│   └── Transaction Count (width: 4)
│
├── Row 5: Main Charts (height: 6)
│   ├── Revenue Trend (line, width: 6)
│   └── Revenue by Category (bar, width: 6)
│
└── Row 11: Detail Table (height: 6)
    └── Transaction Details (width: 12)

Page: Global Filters
└── Cross-dashboard filters
```

---

### Complete Dashboard Template

```json
{
  "datasets": [
    {
      "name": "kpi_totals",
      "displayName": "KPI Totals",
      "queryLines": ["SELECT SUM(net_revenue) as total_revenue, SUM(net_units) as total_units, SUM(transaction_count) as total_transactions FROM ${catalog}.${schema}.fact_sales_daily WHERE transaction_date BETWEEN :start_date AND :end_date"],
      "catalog": "${catalog}",
      "schema": "${schema}"
    },
    {
      "name": "revenue_trend",
      "displayName": "Revenue Trend",
      "queryLines": ["SELECT transaction_date, SUM(net_revenue) as revenue FROM ${catalog}.${schema}.fact_sales_daily WHERE transaction_date BETWEEN :start_date AND :end_date GROUP BY transaction_date ORDER BY transaction_date"],
      "catalog": "${catalog}",
      "schema": "${schema}"
    },
    {
      "name": "revenue_by_category",
      "displayName": "Revenue by Category",
      "queryLines": ["SELECT p.category, SUM(f.net_revenue) as revenue FROM ${catalog}.${schema}.fact_sales_daily f JOIN ${catalog}.${schema}.dim_product p ON f.upc_code = p.upc_code WHERE f.transaction_date BETWEEN :start_date AND :end_date GROUP BY p.category ORDER BY revenue DESC"],
      "catalog": "${catalog}",
      "schema": "${schema}"
    },
    {
      "name": "store_filter_values",
      "displayName": "Store Filter Values",
      "queryLines": ["SELECT 'All' as store_name UNION ALL SELECT DISTINCT store_name FROM ${catalog}.${schema}.dim_store WHERE is_current = true ORDER BY store_name"],
      "catalog": "${catalog}",
      "schema": "${schema}"
    }
  ],
  
  "pages": [
    {
      "name": "page_overview",
      "displayName": "Overview",
      "pageType": "PAGE_TYPE_CANVAS",
      "layoutVersion": "GRID_V1",
      "layout": [
      ]
    },
    {
      "name": "page_global_filters",
      "displayName": "Global Filters",
      "pageType": "PAGE_TYPE_GLOBAL_FILTERS",
      "layoutVersion": "GRID_V1",
      "layout": [
      ]
    }
  ],
  
  "parameters": [
    {
      "displayName": "Start Date",
      "keyword": "start_date",
      "dataType": "DATE",
      "defaultSelection": {
        "values": {
          "dataType": "DATE",
          "values": [{"value": "2024-01-01"}]
        }
      }
    },
    {
      "displayName": "End Date",
      "keyword": "end_date",
      "dataType": "DATE",
      "defaultSelection": {
        "values": {
          "dataType": "DATE",
          "values": [{"value": "2024-12-31"}]
        }
      }
    }
  ],
  
  "uiSettings": {
    "theme": {
      "canvasBackgroundColor": {"light": "#F7F9FA", "dark": "#0B0E11"},
      "widgetBackgroundColor": {"light": "#FFFFFF", "dark": "#1A1D21"},
      "widgetBorderColor": {"light": "#E0E4E8", "dark": "#2A2E33"},
      "fontColor": {"light": "#11171C", "dark": "#E8ECF0"},
      "selectionColor": {"light": "#077A9D", "dark": "#8ACAE7"},
      "visualizationColors": [
        "#077A9D", "#00A972", "#FFAB00", "#FF3621",
        "#8BCAE7", "#99DDB4", "#FCA4A1", "#AB4057",
        "#6B4FBB", "#BF7080"
      ],
      "widgetHeaderAlignment": "LEFT"
    },
    "genieSpace": {"isEnabled": false}
  }
}
```

**⚠️ CRITICAL:** Note that datasets use `queryLines` (array) + `catalog` + `schema` — NOT `query` (string). Using `query` instead of `queryLines` will cause ALL widgets to error silently.

---

### Global Filters Page

Always include a Global Filters page for cross-dashboard filtering:

```json
{
  "name": "page_global_filters",
  "displayName": "Global Filters",
  "pageType": "PAGE_TYPE_GLOBAL_FILTERS",
  "layoutVersion": "GRID_V1",
  "layout": [
    {
      "widget": {
        "name": "global_date_range",
        "spec": {
          "version": 2,
          "widgetType": "filter-date-range",
          "frame": {
            "showTitle": true,
            "title": "Date Range"
          }
        }
      },
      "position": {"x": 0, "y": 0, "width": 3, "height": 2}
    },
    {
      "widget": {
        "name": "global_store_filter",
        "spec": {
          "version": 2,
          "widgetType": "filter-single-select",
          "frame": {
            "showTitle": true,
            "title": "Store"
          }
        }
      },
      "position": {"x": 3, "y": 0, "width": 3, "height": 2}
    }
  ]
}
```

---

## Query Patterns & Best Practices

### Pattern: "All" Option for Filters

```sql
SELECT 'All' AS filter_value
UNION ALL
SELECT DISTINCT actual_value AS filter_value
FROM source_table
ORDER BY filter_value
```

### Pattern: Dynamic Filtering

```sql
WHERE (:store_filter = 'All' OR store_name = :store_filter)
  AND transaction_date BETWEEN :start_date AND :end_date
```

### Pattern: Handle NULL Values

```sql
COALESCE(store_name, 'Unknown')
COALESCE(category, 'Uncategorized')
```

### Pattern: Date Range

```sql
WHERE DATE(timestamp_field) >= :start_date 
  AND DATE(timestamp_field) <= :end_date
```

### Pattern: SCD2 Latest Records

```sql
WITH latest AS (
  SELECT *,
    ROW_NUMBER() OVER(PARTITION BY entity_id ORDER BY change_time DESC) as rn
  FROM source_table
  WHERE delete_time IS NULL
  QUALIFY rn = 1
)
SELECT * FROM latest
```

### Pattern: Multi-Series Charts

Use `UNION ALL` to combine series:

```sql
SELECT date, 'Average' AS metric, AVG(value) AS value FROM table GROUP BY date
UNION ALL
SELECT date, 'P95' AS metric, PERCENTILE_APPROX(value, 0.95) AS value FROM table GROUP BY date
ORDER BY date, metric
```

**Widget Encoding:**
```json
{
  "x": { "fieldName": "date", "scale": { "type": "temporal" } },
  "y": { "fieldName": "value", "scale": { "type": "quantitative" } },
  "color": { "fieldName": "metric", "scale": { "type": "categorical" } }
}
```

### Pattern: Stacked Area Charts

Use `stack: "zero"` in y encoding:

```json
{
  "y": {
    "fieldName": "run_count",
    "scale": { "type": "quantitative" },
    "stack": "zero"
  }
}
```

### Pattern: Metric View Queries Using MEASURE()

When dashboards query Metric Views, use `MEASURE()` for aggregate datasets (KPIs, trends, breakdowns) and direct Gold SQL for detail tables and filter values. See [Metric View Dashboard Queries](references/metric-view-dashboard-queries.md) for complete syntax, SQL templates, rules, and anti-patterns.

---

## System Tables Reference

### ⚠️ Always Verify Field Names!

When using system tables, verify schema against [official docs](https://docs.databricks.com/aws/en/admin/system-tables/).

### `system.lakeflow.jobs` (SCD2)

```sql
-- Note: Column is 'name', NOT 'job_name'
SELECT workspace_id, job_id, name, description, run_as
FROM system.lakeflow.jobs
WHERE delete_time IS NULL
```

### `system.lakeflow.job_task_run_timeline`

```sql
-- Note: NO job_name column! JOIN with jobs table
SELECT jtr.*, 
  COALESCE(j.name, 'Job ' || jtr.job_id) AS job_name
FROM system.lakeflow.job_task_run_timeline jtr
LEFT JOIN (
  SELECT workspace_id, job_id, name,
    ROW_NUMBER() OVER(PARTITION BY workspace_id, job_id 
                      ORDER BY change_time DESC) as rn
  FROM system.lakeflow.jobs
  WHERE delete_time IS NULL
  QUALIFY rn = 1
) j ON jtr.workspace_id = j.workspace_id AND jtr.job_id = j.job_id
```

### `system.compute.clusters`

```sql
SELECT workspace_id, cluster_id, 
       MAX_BY(dbr_version, change_time) AS dbr_version
FROM system.compute.clusters
WHERE delete_time IS NULL
GROUP BY workspace_id, cluster_id
```

---

## Core Patterns (Deployment-Ready)

### Variable Substitution

**NEVER hardcode schemas.** Always use variables:

```sql
-- ✅ CORRECT
FROM ${catalog}.${gold_schema}.fact_usage
FROM ${catalog}.${gold_schema}_monitoring.fact_usage_profile_metrics

-- ❌ WRONG
FROM jane_catalog.gold.fact_usage
```

**Substitution in Python:**
```python
json_str = json_str.replace('${catalog}', catalog)
json_str = json_str.replace('${gold_schema}', gold_schema)
```

---

### UPDATE-or-CREATE Deployment

**Pattern:** Use Workspace Import API with `overwrite: true`

**Benefits:**
- Preserves dashboard URLs and permissions
- Single code path for CREATE and UPDATE
- No manual dashboard creation required

**Implementation:** See `scripts/deploy_dashboard.py`

#### ⚠️ CRITICAL: Content MUST be base64-encoded (not raw UTF-8 bytes)

The Workspace Import API (`ws.workspace.import_` / `POST /api/2.0/workspace/import`) expects the `content` field to be a **base64-encoded ASCII string**. Passing raw UTF-8 bytes silently produces a corrupt `.lvdash.json` that appears in the workspace tree but fails to open in the AI/BI editor with a generic parse error — the most frustrating failure mode because there is no import-time exception.

```python
import base64

# ❌ WRONG — uploads the wrong bytes; the file is corrupt on arrival.
ws.workspace.import_(
    path=target_path,
    content=rendered.encode("utf-8"),
    format=ImportFormat.AUTO,
    overwrite=True,
)

# ✅ CORRECT — base64-encode the UTF-8 bytes then decode to ASCII str.
b64_content = base64.b64encode(rendered.encode("utf-8")).decode("ascii")
ws.workspace.import_(
    path=target_path,
    content=b64_content,
    format=ImportFormat.AUTO,
    overwrite=True,
)
```

Reference: https://docs.databricks.com/api/workspace/workspace/import

#### ⚠️ CRITICAL: Pre-loop variable enumeration

Before entering the per-dashboard deploy loop, scan **every** `.lvdash.json` file for `${...}` placeholders and fail loud if the caller's `variables` dict does not cover every placeholder. This prevents the partial-deploy failure mode where dashboards N+1…K never get deployed because dashboard N referenced an unsupplied variable mid-loop.

```python
import re
_VAR_RE = re.compile(r"(?<!\$)\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

required = {}
for df in dashboard_files:
    for name in _VAR_RE.findall(df.read_text()):
        required.setdefault(name, []).append(df)

missing = {n: fs for n, fs in required.items() if variables.get(n) in (None, "")}
if missing:
    raise RuntimeError(
        "Dashboard deploy pre-flight FAILED — missing variable values:\n"
        + "\n".join(f"  - ${{{n}}} required by {fs}" for n, fs in sorted(missing.items()))
    )
```

The canonical implementation of both guards lives in `scripts/deploy_dashboard.py` (`enumerate_required_variables`, `assert_all_variables_provided`, base64-encoded `deploy_dashboard`). The Phase 0.5 pre-flight in `semantic-layer/00-semantic-layer-setup/SKILL.md` calls `enumerate_required_variables` directly so the failure surfaces BEFORE `bundle validate`.

---

### Pre-Deployment Validation

**Strategy:** Validate queries with `SELECT LIMIT 1` before deployment

**Benefits:**
- 90% reduction in dev loop time
- Catches ALL errors at once (not one-by-one)
- Validates runtime errors (not just syntax)

**Scripts:**
- `validate_dashboard_queries.py` - SQL validation
- `validate_widget_encodings.py` - Widget-query alignment

---

## Implementation Guide

### Phase-by-Phase Checklist

#### Phase 0: Input Validation (5 min) — MANDATORY

- [ ] **Verify all user-referenced files exist** (plan files, manifests, schemas)
  - If a referenced file is missing: STOP and ask the user for the correct path or alternative
  - NEVER silently reconstruct requirements from other sources
- [ ] **Read observability manifest** (`plans/manifests/observability-manifest.yaml`) if it exists
  - Check `dashboards:` section for pre-planned dashboard specs
- [ ] **Load prerequisite skills** (see "Mandatory Skill Dependencies" above)

#### Phase 1: Planning (30 min)

- [ ] Identify KPIs to display
- [ ] List required filters (date, dimensions)
- [ ] Plan page structure and layout
- [ ] Sketch widget placement (grid positions)

#### Phase 2: Datasets (30 min)

- [ ] Create dataset for each unique query
- [ ] Use `queryLines` array format (NOT `query` string)
- [ ] Add "All" option to filter datasets
- [ ] Handle NULL values with COALESCE
- [ ] Test queries in SQL editor first

#### Phase 3: Widgets (1-2 hours)

- [ ] Create KPI counters (version 2)
- [ ] Create charts (version 3)
- [ ] Create tables (version 2)
- [ ] Create filter widgets (version 2)
- [ ] Position using 12-column grid (rows sum to 12, `layoutVersion: "GRID_V1"` on every page)

#### Phase 4: Parameters (15 min)

- [ ] Add date parameters (DATE type, static defaults)
- [ ] Link parameters to dataset queries
- [ ] Test parameter binding

#### Phase 5: Styling (15 min)

- [ ] Apply Databricks theme colors
- [ ] Add titles and descriptions to all widgets
- [ ] Verify consistent formatting

#### Phase 6: Testing (30 min)

- [ ] Import dashboard JSON
- [ ] Test all filters
- [ ] Verify widget snapping (12-column grid, rows sum to 12)
- [ ] Check data accuracy

---

### Verification Checklist

#### Pre-Deployment

- [ ] SQL Validation passed - All queries return results without error
- [ ] Widget Encoding Validation passed - All fieldNames match query aliases
- [ ] Git diff reviewed - No accidental deletions or regressions
- [ ] Local testing done - Validated in dev environment

#### Widget-Query Alignment

- [ ] Widget `fieldName` matches query output alias exactly
- [ ] Format type matches expected value type (raw numbers for percent/currency)
- [ ] All parameters are defined in dataset's `parameters` array
- [ ] Time range uses correct access pattern (`:time_range.min`, `:time_range.max`)

#### Monitoring Query Validation

- [ ] Uses `window.start` not `window_start`
- [ ] Custom AGGREGATE/DERIVED metrics selected as direct columns
- [ ] Schema is `${catalog}.${gold_schema}_monitoring`
- [ ] Includes `WHERE column_name = ':table' AND slice_key IS NULL`

#### Chart Validation

- [ ] Pie charts: `color.scale: categorical`, `angle.scale: quantitative`
- [ ] Bar charts: `x.scale: categorical`, `y.scale: quantitative`
- [ ] Pivot tables: Ratio metrics use `disaggregated: false`. **Always use Pattern A** (dataset `columns` + `MEASURE()` + `cell` encoding) — it is the only pattern visible in the UI editor. Pattern B (inline expressions) is invisible in draft mode. Neither uses `transform`.
- [ ] Point maps: Use `widgetType: "symbol-map"` (v2) with nested `coordinates` encoding; `latitude`/`longitude` fields are DOUBLE type (not STRING)
- [ ] Choropleth maps: Use `widgetType: "choropleth-map"` (v1) with `region` encoding including `geographicRole`
- [ ] Table widgets: Uses `version: 2`, no invalid properties

#### Before Deploying Dashboard

- [ ] All widget positions use 12-column grid (widths: 1-12; each row sums to 12)
- [ ] KPIs use version 2 (not version 3)
- [ ] Charts use version 3 (bar, line, pie, area, scatter, point, choropleth, pivot)
- [ ] Tables use version 2
- [ ] Sankey uses version 1
- [ ] Date parameters use DATE type (not DATETIME)
- [ ] Global Filters page included
- [ ] All filters have "All" option
- [ ] NULL values handled with COALESCE
- [ ] System table fields verified against docs
- [ ] SCD2 tables handled with QUALIFY pattern
- [ ] JOINs include both workspace_id AND entity ID

---

## Scripts & Automation

### update_dashboard.py — Lakeview Dashboard JSON Utility

A Python utility for robust, programmatic manipulation of `.lvdash.json` files. Copy to your project's `scripts/` folder when needed.

**Location:** [scripts/update_dashboard.py](scripts/update_dashboard.py)

**Key functions:** `load_dashboard`, `save_dashboard`, `find_dataset`, `find_widget`, `add_dataset_columns`, `update_widget_query_fields`, `add_widget_query_fields`, `rename_widget_query_field`, `set_widget_encoding_rows`, `set_widget_encoding_values`, `rename_encoding_field`, `reorder_widget_query_fields`, `reorder_cube_grouping_sets`, `replace_in_dataset_query`, `validate_dashboard`.

**CLI usage:**
```bash
python scripts/update_dashboard.py input.lvdash.json output.lvdash.json \
  --validate
```

**Common operations:**
```python
from update_dashboard import *
data = load_dashboard("dashboard.lvdash.json")

# Fix hierarchy order
data = reorder_widget_query_fields(data, "my-pivot", ["region", "market", "store_id"])
data = reorder_widget_encoding_rows(data, "my-pivot", ["region", "market", "store_id"])

# Add dataset custom calculations (Pattern A)
data = add_dataset_columns(data, "ds_hierarchy", [
    {"displayName": "Avg Revenue", "description": "Revenue per store-day", "expression": "SUM(`revenue`) / NULLIF(SUM(`store_days`), 0)"}
])

warnings = validate_dashboard(data)
save_dashboard("dashboard.lvdash.json", data)
```

### deploy_dashboard.py

UPDATE-or-CREATE deployment with variable substitution:

```python
from scripts.deploy_dashboard import deploy_dashboards
deploy_dashboards(workspace_client, dashboard_dir, catalog, gold_schema, warehouse_id)
```

### validate_dashboard_queries.py

Pre-deployment SQL validation:

```bash
python scripts/validate_dashboard_queries.py
```

Catches: `UNRESOLVED_COLUMN`, `TABLE_OR_VIEW_NOT_FOUND`, `UNBOUND_SQL_PARAMETER`, `DATATYPE_MISMATCH`

### validate_widget_encodings.py

Widget-query alignment validation:

```bash
python scripts/validate_widget_encodings.py
```

Catches: Column alias mismatches, missing columns

---

## Assets & Templates

### dashboard-template.json

Starter dashboard JSON with dataset, time range parameter, KPI widget, and page layout. Copy and modify for new dashboards.

Location: `assets/templates/dashboard-template.json`

### Jobs System Tables Dashboard (Production Example)

**Complete, production-ready dashboard** demonstrating best practices for Databricks System Tables monitoring. This real-world example showcases:

- ✅ **System Tables Integration** - Queries `system.lakeflow.jobs`, `system.lakeflow.job_task_run_timeline`, `system.compute.clusters`
- ✅ **Proper JOIN Patterns** - Demonstrates correct workspace_id + entity_id JOIN requirements
- ✅ **SCD2 Handling** - Shows QUALIFY pattern for latest records from SCD2 tables
- ✅ **Widget Configuration** - All widget types properly configured (counters, bar charts, line charts, tables)
- ✅ **12-Column Grid Layout** - Correct positioning with the 12-column grid system (rows sum to 12)
- ✅ **Parameter Configuration** - Time range parameters with proper DATE type
- ✅ **Variable Substitution** - Uses ${catalog} and ${schema} patterns
- ✅ **Multi-Page Dashboard** - Overview + Global Filters pages
- ✅ **Number Formatting** - Raw numbers for proper widget formatting
- ✅ **Field Name Verification** - Uses actual system table column names (not assumptions)

**Use this as a reference for:**
- Building system tables dashboards
- Understanding complete dashboard JSON structure
- Seeing all patterns from this skill in action
- Learning proper widget-query alignment
- Implementing multi-page layouts

Location: `references/Jobs System Tables Dashboard.lvdash.json`

**Dashboard Includes:**
- Job success rate and failure tracking
- Task execution timeline and durations
- Cluster utilization and DBR version distribution
- Job run history with filters by workspace and date range
- Detailed tables for job configuration and task details

---

## Common Mistakes & Error Messages

### Common Mistakes to Avoid

#### ❌ Mistake 1: Rows that don't sum to 12 (gaps)

```json
// Wrong - leaves a gap, widget won't snap correctly
{"x": 0, "width": 4}  // ...and the row stops here, columns 4-11 left empty

// Right - the row fills all 12 columns
{"x": 0, "width": 6}   // half
{"x": 6, "width": 6}   // half → 6 + 6 = 12
```

#### ❌ Mistake 2: Wrong Widget Version

```json
// Wrong - KPIs must use version 2
"version": 3,
"widgetType": "counter"
```

#### ❌ Mistake 3: DATETIME Parameters

```json
// Wrong - use DATE type
"dataType": "DATETIME"
```

#### ❌ Mistake 4: Missing "All" Option

```sql
-- Wrong - no way to clear filter
SELECT DISTINCT store_name FROM stores
```

#### ❌ Mistake 5: Assuming Field Names

```sql
-- Wrong - job_name doesn't exist in this table!
SELECT job_name FROM system.lakeflow.job_task_run_timeline
```

#### ❌ Mistake 6: SUM on Ratio Metrics in Pivots

```json
// Wrong - SUM of pre-computed averages is mathematically incorrect at rolled-up levels
"values": [{"fieldName": "precomputed_avg", "transform": "SUM"}]
```

```json
// Correct (Pattern A — deep hierarchies) - use dataset columns + MEASURE()
// Dataset: "columns": [{"displayName": "Avg Rev", "expression": "SUM(`revenue`) / NULLIF(SUM(`store_days`), 0)"}]
// Widget: "fields": [{"name": "measure(Avg Rev)", "expression": "MEASURE(`Avg Rev`)"}]
// Encodings: "cell": {"fields": [{"fieldName": "measure(Avg Rev)", "cellType": "text"}], "displayAs": "columns"}
```

#### ❌ Mistake 7: Using `query` Instead of `queryLines` in Datasets

```json
// Wrong - Lakeview editor will not parse the dataset and ALL widgets will error
{"name": "ds_example", "query": "SELECT * FROM table"}
```

```json
// Correct - use queryLines array + catalog + schema
{"name": "ds_example", "queryLines": ["SELECT * FROM table"], "catalog": "my_catalog", "schema": "my_schema"}
```

#### ❌ Mistake 8: Using `textbox_spec` Instead of `multilineTextboxSpec`

```json
// Wrong - Lakeview editor will not render the textbox
{"textbox_spec": "### Title"}
```

```json
// Correct
{"multilineTextboxSpec": {"lines": ["### Title"]}}
```

#### ❌ Mistake 9: Using `values` Encoding with `cubeGroupingSets` for Ratio Metrics

```json
// Wrong - values with cubeGroupingSets causes ratio metrics to appear as extra rows
"cubeGroupingSets": {"sets": [{"fieldNames": ["region", "market"]}, {}]},
"encodings": {"values": [{"fieldName": "avg_revenue", "displayName": "Avg Revenue"}]}
```

```json
// Correct - use dataset columns + MEASURE() + cell encoding (Pattern A)
"cubeGroupingSets": {"sets": [{"fieldNames": ["region", "market"]}, {}]},
"encodings": {"cell": {"type": "multi-cell", "fields": [{"fieldName": "measure(Avg Revenue)", "cellType": "text"}], "displayAs": "columns"}}
```

#### ❌ Mistake 10: STRING Coordinates for Maps

```sql
-- Wrong - point map will render blank
SELECT latitude, longitude FROM dim_location  -- STRING type
```

```sql
-- Correct - cast in upstream MV
SELECT CAST(latitude AS DOUBLE) AS latitude, CAST(longitude AS DOUBLE) AS longitude
```

#### ❌ Mistake 11: Using Source Table Prefix in Metric View Queries

```sql
-- Wrong - metric views flatten dimensions into a single namespace
WHERE dim_location.is_same_store = 1

-- Correct - use bare dimension name
WHERE is_same_store = 1
```

---

### Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "no fields to visualize" | Widget `fieldName` doesn't match query alias | Align column aliases |
| "UNRESOLVED_COLUMN" | Column doesn't exist | Check schema, use correct column |
| "UNRESOLVED_COLUMN" with metric view | Using source table alias (e.g., `dim_location.col`) instead of dimension name | Drop table prefix — use bare dimension `name` from metric view YAML |
| "UNBOUND_SQL_PARAMETER" | Parameter not defined | Add to `parameters` array |
| "Unable to render visualization" | Pie chart missing scale | Add `scale` to encodings |
| Blank point map | lat/lng are STRING type | CAST to DOUBLE in upstream MV |
| Incorrect pivot rollup totals | Ratio metric summed incorrectly | Use `disaggregated: false` with aggregate expressions. For hierarchies with `cubeGroupingSets`, use Pattern A (dataset `columns` + `MEASURE()` + `cell` encoding). |
| Empty chart with data | Wrong number format | Return raw numbers, not strings |
| 0% or 0 in counter | Formatted string or wrong percentage | Return 0-1 decimal for percent |
| "Visualization has no fields selected" on counter | Invalid encoding key (e.g., `comparison`) in counter spec | Counter widgets (v2) ONLY support `"value"` in encodings. Do NOT add `"comparison"`, `"extra"`, or any other key — it silently breaks the entire widget. |

---

## Lessons Learned (Production)

These patterns were discovered through production deployments and iterative dashboard refinement.

### L1: Non-Additive Ratio Metrics in Pivot Hierarchies

**Problem:** Ratio metrics (e.g., avg_revenue = total_revenue / store_count) produce incorrect results when simply summed. The sum of ratios at leaf nodes does not equal the ratio at the rolled-up parent level.

**Solution:** Two patterns exist depending on whether you need hierarchy expand/collapse:

- **Pattern A (Dataset `columns` + `MEASURE()`) — ALWAYS PREFERRED**: Define custom calculated measures in the dataset `columns` array, reference via `MEASURE(\`Display Name\`)` in widget query, use `cell` encodings with `displayAs: "columns"`. Works in both the Lakeview UI editor/draft mode and published view.
- **Pattern B (Inline widget expressions) — AVOID**: Define aggregate expressions directly in widget query `fields`, use `values` encodings. **Only renders in published view** — the UI editor/draft mode shows an empty Values panel and "No data".

Both patterns use `disaggregated: false`. Neither uses the `transform` property.

### L2: Map Widget Types Use Different Names and Versions Than Standard Charts

**Problem:** Map visualizations show "Visualization has no fields selected" when using `widgetType: "choropleth"` / `"point"` with `version: 3`.

**Fix:**
- Choropleth: `widgetType: "choropleth-map"`, `version: 1`, use `encodings.region` with `regionType: "mapbox-v4-admin"` and `admin0`/`admin1` sub-objects
- Point/Symbol Map: `widgetType: "symbol-map"`, `version: 2`, use `encodings.coordinates` with nested `latitude`/`longitude` objects

### L3: Querying Metric Views in Dashboard Datasets

**Problem:** `UNRESOLVED_COLUMN` errors when dashboard SQL references dimensions with source table prefixes.

**Fix:** Reference dimensions by their metric view `name` (not the source table alias):
```sql
-- ❌ WRONG: WHERE dim_location.is_same_store = 1
-- ✅ CORRECT: WHERE is_same_store = 1
```

### L4: Dashboard vs Metric View Measure Reusability

**Architecture:** The metric view remains the single source of truth for reusable, context-aware measures (Genie, ad-hoc SQL, KPI counters). Dashboard pivot widget aggregate expressions are a **presentation layer** adaptation specific to the interactive hierarchy, consuming additive components from the metric view.

- **Genie/ad-hoc SQL:** `SELECT MEASURE(avg_revenue) ...` — context-aware, works natively
- **Dashboard KPIs:** Same as above — single-value counters work with MEASURE() directly
- **Dashboard pivots:** Must use additive components + aggregate expressions for correct hierarchy rollups

### L5: Bundle Deployment State Management

**Problem:** Repeated `lineage mismatch`, `Node already exists`, or stale resource errors when iterating on dashboards via Databricks Asset Bundles.

**Fix:** Systematic cleanup before redeployment:
1. Delete local `.databricks/bundle/dev/terraform/terraform.tfstate`
2. Delete remote bundle workspace directory
3. Clean orphaned resources (pipelines, jobs, dashboards) by ID if needed
4. Redeploy: `databricks bundle deploy -t dev --profile <profile>`

### L6: Dataset `columns` for Custom Calculated Measures

**Problem:** Hierarchy pivots with `cubeGroupingSets` cannot use inline widget query aggregate expressions for ratio metrics — the values appear as additional rows instead of columns.

**Solution:** Use the dataset `columns` array to define custom calculated measures that the Lakeview engine evaluates at each hierarchy level. The widget query references these via `MEASURE(\`Display Name\`)` and the encoding uses `cell` with `displayAs: "columns"`.

### L7: Cross-Filtering Is Dataset-Scoped, Not Field-Scoped

**Problem:** Two charts on the same page with the same field name but pointing to different datasets did not cross-filter when clicked.

**Fix:** Consolidate charts that should cross-filter onto a single shared dataset.

### L8: `disallowAll` Prevents Silent Double-Counting

**Problem:** Aggregated metrics showed incorrect values because the period filter silently defaulted to "All", including both Day and MTD rows.

**Fix:** Use the correct `defaultSelection` format with `disallowAll: true` on single-select filters where "All" is not meaningful. Additionally, use `COUNT(DISTINCT pk_column)` instead of `SUM(count_column)` for robustness.

### L9: Choropleth admin1 (State) Maps Require Explicit admin0 (Country) Context

**Problem:** A state-level choropleth map rendered blank even though state names were correctly provided.

**Fix:** Always include both `admin0` and `admin1` in the `region` encoding for state/province choropleths. Convert abbreviations to full names via CASE expressions in the dataset SQL.

### L10: Silent Recovery from Missing Input Files

**Problem:** When a user-referenced file (plan, manifest, schema) is not found, the agent silently reconstructs requirements from secondary sources. The user has no visibility into the gap, and the dashboard may miss specific KPIs, charts, or layout preferences.

**Fix:** Always surface missing files to the user before proceeding. Search for similar filenames and nearby directories, then ask: "The file at [path] was not found. I found [alternatives]. Should I proceed with those, or is the file at a different path?"

### L11: Substituting "Safer" Query Patterns for User-Requested Patterns

**Problem:** When uncertain about MEASURE() syntax, the agent fell back to direct Gold table SQL — contradicting the user's explicit request. The dashboard bypassed the semantic layer entirely.

**Fix:** When uncertain about a query pattern, load the owning skill (e.g., `semantic-layer/01-metric-views-patterns/SKILL.md` for MEASURE()). If the tradeoff involves contradicting a user instruction, surface it to the user — never resolve it unilaterally.

### L12: Producing All Referenced Scripts

**Problem:** The skill references three companion scripts (`validate_dashboard_queries.py`, `validate_widget_encodings.py`, `deploy_dashboard.py`). Agents sometimes create only the "most important" one and skip the others, leaving the dev loop with no live SQL validation or no deployment path.

**Fix:** Treat the "Scripts & Automation" section as a checklist. All three scripts should be created (or copied from the skill's `scripts/` templates) during dashboard builds. If a script is intentionally skipped, state which one and why — do not silently produce a partial deliverable.

### L13: Reading Large Dashboard JSON Examples

**Problem:** Production `.lvdash.json` files can exceed 100K characters. Reading from line 1 returns dataset SQL but misses the widget/page structure — usually the more valuable reference for layout patterns, grid positions, and encodings.

**Fix:** Read strategically instead of from the top:
1. Grep for `"pages"` to locate where page/widget definitions begin
2. Read from that line to see widget patterns, grid positions, encodings, and parameter bindings
3. Read datasets separately only when you need query patterns (usually the SKILL.md and reference files already cover these)
4. If the file exceeds read limits, prioritize the pages section — it has higher value per token than dataset SQL

---

## Dashboard File Management

### File Location

```
project/
├── docs/
│   └── dashboards/
│       └── {project}_dashboard.lvdash.json
```

### Naming Convention

```
{project}_{purpose}_dashboard.lvdash.json

Examples:
- lakehouse_monitoring_dashboard.lvdash.json
- sales_analytics_dashboard.lvdash.json
- executive_kpi_dashboard.lvdash.json
```

### Version Control

- Track dashboard JSON in git
- Use meaningful commit messages
- Document changes in comments

---

## Key Principles Summary

### 1. 12-Column Grid

```json
// ✅ Correct — widths in a row sum to 12
{"width": 6}   // Half width
{"width": 12}  // Full width

// ❌ Wrong — leaves a gap (row must total 12)
{"width": 3}  // A quarter — pair with widths that complete the row to 12
```

### 2. Version Numbers

| Widget | Version |
|--------|---------|
| KPI Counter | 2 |
| Bar Chart | 3 |
| Line Chart | 3 |
| Pie Chart | 3 |
| Area Chart | 3 |
| Scatter Chart | 3 |
| Pivot Table | 3 |
| Symbol/Point Map (`symbol-map`) | 2 |
| Choropleth Map (`choropleth-map`) | 1 |
| Table | 2 |
| Sankey | 1 |
| Waterfall | 3 |
| Histogram | 3 |
| Filter (single/multi) | 2 |
| Filter (date-range) | 2 |

### 3. DATE, Not DATETIME

```json
// ✅ Correct
"dataType": "DATE"

// ❌ Wrong
"dataType": "DATETIME"
```

### 4. Always Include Global Filters

```json
"pageType": "PAGE_TYPE_GLOBAL_FILTERS"
```

### 5. Handle NULL Values

```sql
COALESCE(field, 'Default Value')
```

---

## Reference Documentation

Detailed patterns and examples are organized in reference files:

- **[Dashboard JSON Reference](references/dashboard-json-reference.md)** - JSON structure, page layouts, dataset configuration, variable substitution, widget versions, naming conventions
- **[Widget Patterns](references/widget-patterns.md)** - Widget-query alignment, number formatting, parameters, chart configurations, multi-series charts, error fixes
- **[Deployment Guide](references/deployment-guide.md)** - UPDATE-or-CREATE pattern, variable substitution, SQL validation, monitoring queries, best practices, checklists
- **[Jobs System Tables Dashboard](references/Jobs%20System%20Tables%20Dashboard.lvdash.json)** - Complete production example demonstrating all patterns from this skill with System Tables integration

---

## References

### Official Documentation

- [AI/BI Lakeview Dashboards](https://docs.databricks.com/dashboards/lakeview/)
- [Pivot Table Configuration](https://docs.databricks.com/aws/en/dashboards/manage/visualizations/tables#pivot-table-configuration)
- [Map Visualizations](https://docs.databricks.com/aws/en/dashboards/manage/visualizations/maps)
- [Visualization Types](https://docs.databricks.com/aws/en/dashboards/manage/visualizations/types)
- [Custom Calculations / LOD Expressions](https://docs.databricks.com/aws/en/dashboards/manage/data-modeling/custom-calculations/level-of-detail)
- [Dashboard Filters](https://docs.databricks.com/aws/en/dashboards/manage/filters/)
- [System Tables Overview](https://docs.databricks.com/aws/en/admin/system-tables/)
- [Jobs System Tables](https://docs.databricks.com/aws/en/admin/system-tables/jobs)
- [Compute System Tables](https://docs.databricks.com/aws/en/admin/system-tables/compute)
- [Lakehouse Monitoring](https://docs.databricks.com/lakehouse-monitoring/)
- [Workspace Dashboard API](https://learn.microsoft.com/en-us/azure/databricks/dashboards/tutorials/workspace-dashboard-api)

### Related Skills

- `lakehouse-monitoring-comprehensive` - Monitoring setup patterns
- `sql-alerting-patterns` - SQL alert configuration
- `metric-views-patterns` - Semantic layer metric views

---

## Summary

### What to Create

1. Dashboard JSON file with proper structure
2. Datasets (queries for each widget)
3. Pages with widget layouts
4. Parameters (date filters)
5. Global Filters page

### Critical Rules

- 12-column grid (`layoutVersion: "GRID_V1"`; rows sum to 12, no gaps)
- KPIs: v2, Charts/Pivots: v3, Tables: v2, Sankey: v1, Choropleth: v1, Symbol Map: v2, Waterfall: v3, Histogram: v3
- DATE type for parameters (not DATETIME)
- Include Global Filters page
- Verify system table field names
- Return raw numbers for formatting
- Match widget fieldNames to query aliases
- Ratio metrics in pivots: use `disaggregated: false` with aggregate expressions
- Map widgets: ensure lat/lng are DOUBLE (not STRING)
- Metric view queries: reference dimensions by `name`, not by source table alias
- Cross-filtering: charts must share the same `datasetName` on the same page
- Drill-through: target page filter widgets must share source chart's dataset AND field
- Choropleth admin1 (state): always include admin0 (country) field; use full state names
- Filter `defaultSelection`: use typed value format `{"dataType":"STRING","values":[{"value":"..."}]}`
- Use `disallowAll: true` on single-select filters where "All" is not meaningful
- Store counts: prefer `COUNT(DISTINCT pk)` over `SUM(pre_aggregated_count)`
- Datasets must use `queryLines` (array) — NOT `query` (string)
- Textboxes must use `multilineTextboxSpec` — NOT `textbox_spec`

### Time Estimate

2-4 hours for complete dashboard

### Next Action

1. Fill out Project Planning Template
2. Create datasets with validated queries
3. Build widgets with correct specifications
4. Test in Databricks
5. Deploy via API with validation
