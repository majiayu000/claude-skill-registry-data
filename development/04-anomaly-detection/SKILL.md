---
name: anomaly-detection
description: Schema-level anomaly detection for Databricks Unity Catalog using the Data Quality API (Public Preview). Automatically monitors table freshness and completeness using ML models. Use when setting up schema-wide data reliability monitoring, detecting stale or incomplete tables, configuring anomaly detection alerts, or querying the system results table. **Auto-triggered by Silver and Gold layer setup workflows** to ensure every new schema has baseline freshness/completeness monitoring from day one.
clients: [ide_cli, genie_code]
bundle_resource: monitors
deploy_verb: bundle_deploy
deploy_note: "Schema-level anomaly detection (Data Quality API) on the per-user prefixed schema; deployed via `bundle deploy --target dev` (runDatabricksCli on Genie Code)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.1"
  domain: monitoring
  role: worker
  pipeline_stage: 7
  pipeline_stage_name: observability
  triggers:
    - anomaly detection
    - freshness
    - completeness
    - stale tables
    - unhealthy tables
    - schema monitoring
    - silver setup
    - gold setup
    - silver layer
    - gold layer
    - schema setup
  called_by:
    - observability-setup
    - silver-layer-setup
    - gold-layer-setup
  standalone: true
  last_verified: "2026-08-30"
  volatility: medium
  verification_sources:
    - url: "https://databricks-sdk-py.readthedocs.io/en/latest/workspace/dataquality/data_quality.html"
      check_for: "DataQualityAPI method signatures: create_monitor(monitor), delete_monitor(object_type, object_id), get_monitor(object_type, object_id), update_monitor(object_type, object_id, monitor, update_mask), list_monitor"
    - url: "https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/dataquality.html"
      check_for: "Monitor, AnomalyDetectionConfig field names (excluded_table_full_names), object_type/object_id semantics"
    - url: "https://learn.microsoft.com/en-us/azure/databricks/data-quality-monitoring/anomaly-detection/"
      check_for: "Anomaly detection overview, freshness/completeness concepts, enable/disable workflow"
    - url: "https://learn.microsoft.com/en-us/azure/databricks/data-quality-monitoring/anomaly-detection/results"
      check_for: "system.data_quality_monitoring.table_results schema, nested struct fields (freshness, completeness, downstream_impact)"
  upstream_sources:
    - name: "databricks-sdk-py"
      repo: "databricks/databricks-sdk-py"
      paths:
        - "databricks/sdk/service/dataquality.py"
      relationship: "reference"
      last_synced: "2026-08-30"
      sync_commit: "latest"
---

## Overview

Anomaly Detection is a **schema-level** monitoring capability that automatically assesses data quality by evaluating **freshness** (is the table up-to-date?) and **completeness** (did we get the expected number of rows?). It uses ML models built from historical patterns — no custom metric definitions needed.

**API Status:** Public Preview (`POST /api/data-quality/v1/monitors`)

**SDK Module:** `databricks.sdk.service.dataquality`

### When to Use This Skill vs. Lakehouse Monitoring

| Question | Use This Skill | Use Lakehouse Monitoring |
|----------|---------------|------------------------|
| "Did my pipeline break?" | **Yes** — detects stale/incomplete tables | No |
| "Is my revenue trending correctly?" | No | **Yes** — custom AGGREGATE/DERIVED/DRIFT metrics |
| "Which tables are unhealthy?" | **Yes** — schema-wide scan | No (per-table only) |
| "What's the average transaction value?" | No | **Yes** — custom business KPIs |
| "How quickly can I set up monitoring?" | **Yes** — minutes (enable on schema) | 2+ hours (custom metrics per table) |
| "Do I need ML model monitoring?" | No | **Yes** — `InferenceLogConfig` support |

**Use both together** for comprehensive monitoring: anomaly detection for baseline reliability + custom metrics for business KPIs.

## Core Concepts

### Freshness
Analyzes commit history to build a per-table model predicting next commit time. If a commit is unusually late, the table is marked **stale**.

### Completeness
Analyzes historical row counts to predict expected rows in the last 24 hours. If actual rows fall below the lower bound, the table is marked **incomplete**.

### Intelligent Scanning
Automatically aligns scan frequency with table update cadence. High-impact tables (by popularity and downstream usage) are prioritized; less critical tables are scanned less frequently.

### Results Storage
All results are stored in the system table:
```
system.data_quality_monitoring.table_results
```
**Access:** Only account admins by default. Grant access to others as needed.

## Quick Start

### Enable via UI (Simplest)
1. Navigate to schema in Catalog Explorer
2. Click **Details** tab
3. Click **Enable** under Data Quality Monitoring
4. Click **Save**

### Enable via SDK
```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dataquality import Monitor, AnomalyDetectionConfig

w = WorkspaceClient()

# Get schema UUID (required — NOT the three-level name)
schema_info = w.schemas.get(full_name=f"{catalog}.{schema}")
schema_id = schema_info.schema_id

# Enable anomaly detection
monitor = w.data_quality.create_monitor(
    monitor=Monitor(
        object_type="schema",
        object_id=schema_id,
        anomaly_detection_config=AnomalyDetectionConfig(
            excluded_table_full_names=[
                f"{catalog}.{schema}.staging_table",  # Optional: tables to skip
            ]
        )
    )
)
```

### Disable via SDK
```python
w.data_quality.delete_monitor(
    object_type="schema",
    object_id=schema_id
)
```
**Warning:** Disabling deletes ALL anomaly detection tables and information. This cannot be undone.

## Critical Rules

### Rule 1: create_monitor() Takes a Monitor Object with UUID
```python
# ✅ CORRECT: Wrap in Monitor object, use schema UUID
schema_info = w.schemas.get(full_name=f"{catalog}.{schema}")
w.data_quality.create_monitor(
    monitor=Monitor(object_type="schema", object_id=schema_info.schema_id, ...)
)

# ❌ WRONG: Three-level name, keyword args instead of Monitor object
w.data_quality.create_monitor(object_id=f"{catalog}.{schema}", ...)
```

### Rule 2: Permissions Required
To create/manage a **schema** monitor (anomaly detection), the caller must have **either** of these sets (per the Data Quality Monitoring API):
- **(a)** `MANAGE` **and** `USE_CATALOG` on the schema's parent catalog, **or**
- **(b)** `USE_CATALOG` on the parent catalog **plus** `MANAGE` **and** `USE_SCHEMA` on the schema.

(The Catalog Explorer UI states it more simply: `MANAGE` on the schema or its parent catalog.)
- To view table health indicators: `SELECT` or `BROWSE` on the tables.
- To query results: **SELECT** on `system.data_quality_monitoring.table_results`

### Rule 3: System Table Access Is Restricted
The results table contains data from ALL catalogs in the metastore. **Use caution when granting access** — it includes sample values from every monitored table.

### Rule 4: Anomaly Detection Does NOT Monitor Views
Only tables are scanned. Views are silently skipped.

### Rule 5: Completeness Only Checks Row Counts
Completeness does NOT evaluate null fractions, zero values, or NaN. For column-level quality monitoring, use the `lakehouse-monitoring-comprehensive` skill with custom metrics.

## Configuration Options

### Exclude Specific Tables
```python
AnomalyDetectionConfig(
    excluded_table_full_names=[
        f"{catalog}.{schema}.staging_raw",
        f"{catalog}.{schema}.temp_processing",
    ]
)
```

### Advanced Configuration (via REST API)
For freshness/completeness threshold overrides and table-specific settings, see `references/configuration-guide.md`.

## Querying Results

```sql
-- Find all unhealthy tables in a schema
SELECT
  table_name,
  status,
  freshness.status as freshness_status,
  completeness.status as completeness_status,
  downstream_impact.impact_level,
  downstream_impact.num_downstream_tables
FROM system.data_quality_monitoring.table_results
WHERE catalog_name = '{catalog}'
  AND schema_name = '{schema}'
  AND status = 'Unhealthy'
ORDER BY event_time DESC;
```

For the complete results schema and query patterns, see `references/results-schema.md`.

## Setting Up Alerts

```sql
-- Alert on unhealthy tables with downstream impact
SELECT
  CONCAT(catalog_name, '.', schema_name, '.', table_name) AS full_table_name,
  status,
  downstream_impact.num_queries_on_affected_tables AS impacted_queries
FROM system.data_quality_monitoring.table_results
WHERE event_time >= current_timestamp() - INTERVAL 6 HOURS
  AND status = 'Unhealthy'
  AND downstream_impact.num_queries_on_affected_tables > :min_tables_affected;
```

For complete alert templates including custom email notifications, see `references/alert-patterns.md`.

## Integration with Silver & Gold Layer Setup

**This skill is automatically invoked by `silver-layer-setup` and `gold-layer-setup` orchestrators.** Every new Silver or Gold schema should have anomaly detection enabled to provide baseline freshness/completeness monitoring from day one.

### Reusable Enable Function

Use this pattern in setup scripts to enable anomaly detection as part of schema creation:

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dataquality import Monitor, AnomalyDetectionConfig


def enable_anomaly_detection_on_schema(
    w: WorkspaceClient,
    catalog: str,
    schema: str,
    excluded_tables: list = None,
):
    """
    Enable anomaly detection on a schema. Safe to call if already enabled.

    Called by Silver and Gold layer setup workflows to ensure every schema
    has baseline freshness/completeness monitoring.

    Args:
        w: WorkspaceClient
        catalog: Catalog name
        schema: Schema name
        excluded_tables: Optional list of table names to exclude
                         (e.g., staging, quarantine, temp tables)
    """
    schema_info = w.schemas.get(full_name=f"{catalog}.{schema}")
    schema_id = schema_info.schema_id

    excluded_full_names = None
    if excluded_tables:
        excluded_full_names = [
            f"{catalog}.{schema}.{t}" for t in excluded_tables
        ]

    try:
        monitor = w.data_quality.create_monitor(
            monitor=Monitor(
                object_type="schema",
                object_id=schema_id,
                anomaly_detection_config=AnomalyDetectionConfig(
                    excluded_table_full_names=excluded_full_names
                )
            )
        )
        print(f"✓ Anomaly detection enabled on {catalog}.{schema}")
        return monitor
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✓ Anomaly detection already enabled on {catalog}.{schema} (skipping)")
        else:
            print(f"⚠️ Could not enable anomaly detection on {catalog}.{schema}: {e}")
            print("  (Non-blocking — schema setup continues)")
```

### When Invoked by Silver Layer Setup

```python
# After Silver schema creation and DLT pipeline deployment
enable_anomaly_detection_on_schema(
    w, catalog, silver_schema,
    excluded_tables=["dq_rules"]  # Exclude metadata tables
)
```

### When Invoked by Gold Layer Setup

```python
# After Gold tables are created via setup_tables.py
enable_anomaly_detection_on_schema(
    w, catalog, gold_schema,
    excluded_tables=None  # Monitor all Gold tables
)
```

### Why Enable at Schema Setup Time?

1. **Freshness baselines start building immediately** — ML models need historical commit patterns
2. **Completeness models train earlier** — more scan cycles = more accurate predictions
3. **Zero cost to enable** — no custom metrics needed, runs automatically
4. **Catches pipeline breaks early** — stale/incomplete tables detected before anyone queries them
5. **Complements custom metrics** — anomaly detection for reliability, Lakehouse Monitoring for business KPIs

## Workflow

| Phase | Duration | Activities |
|-------|----------|------------|
| Phase 1: Enable | 5 min | Enable anomaly detection on schema via UI or SDK |
| Phase 2: Wait | 15-30 min | First scan runs automatically |
| Phase 3: Review | 10 min | Check results in Catalog Explorer or system table |
| Phase 4: Alerts | 15 min | Set up SQL alerts on system table |

## Reference Files

### [configuration-guide.md](references/configuration-guide.md)
Complete configuration reference including:
- REST API endpoint and request schema
- SDK-based enable/disable patterns
- `excluded_table_full_names` configuration
- Advanced threshold overrides (freshness, completeness)
- Table skip/scan lists
- Event timestamp column configuration

### [results-schema.md](references/results-schema.md)
System results table documentation including:
- Full schema of `system.data_quality_monitoring.table_results`
- Nested struct documentation (freshness, completeness, downstream_impact, root_cause_analysis)
- Query patterns for common scenarios
- Metastore-level dashboard template reference

### [alert-patterns.md](references/alert-patterns.md)
SQL alert configuration including:
- Alert query template with downstream impact filtering
- Custom email notification template
- Alert configuration steps
- Integration with Databricks SQL Alerts

## Scripts

### [enable_anomaly_detection.py](scripts/enable_anomaly_detection.py)
SDK-based anomaly detection management including:
- Enable on schema with optional table exclusions
- Disable (with warning about data deletion)
- List monitored schemas
- Check monitor status

### [query_results.py](scripts/query_results.py)
Results querying utilities including:
- Query unhealthy tables
- Extract root cause analysis
- Filter by freshness/completeness status
- Generate summary reports

## Assets

### [alert-query-template.sql](assets/templates/alert-query-template.sql)
Ready-to-use SQL query for Databricks SQL Alerts with configurable thresholds and custom email template.

## Limitations

- Does NOT support views (only tables)
- Completeness does not evaluate null fractions, zero values, or NaN
- System table access is restricted to account admins by default
- Disabling deletes all monitoring data (irreversible)
- Event freshness (based on event time columns) is not supported in the current version

## Troubleshooting

### Monitor Not Detecting Anomalies
- **Check permissions:** Ensure MANAGE SCHEMA or MANAGE CATALOG
- **Wait for scan:** First scan may take 15-30 minutes
- **Check table activity:** Tables that rarely change may be classified as "static"

### Cannot Access Results Table
- **Default access:** Only account admins can read `system.data_quality_monitoring.table_results`
- **Grant access:** Account admin must grant SELECT on the system table

### Tables Showing as "Training"
- **Normal behavior:** New tables need historical data to build ML models
- **Wait:** Models improve after several scan cycles

## References

- [Anomaly Detection Overview](https://learn.microsoft.com/en-us/azure/databricks/data-quality-monitoring/anomaly-detection/)
- [Results Schema](https://learn.microsoft.com/en-us/azure/databricks/data-quality-monitoring/anomaly-detection/results)
- [Alert Setup](https://learn.microsoft.com/en-us/azure/databricks/data-quality-monitoring/anomaly-detection/alerts)
- [REST API](https://docs.databricks.com/api/azure/workspace/dataquality/createmonitor)
- [Python SDK Dataclasses](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/dataquality.html)

## Summary

Anomaly Detection provides automated, schema-level monitoring for table freshness and completeness. It complements the `lakehouse-monitoring-comprehensive` skill's custom business metrics with baseline data reliability monitoring. Enable it in minutes via UI or SDK, query results from the system table, and set up SQL alerts for proactive notification.

## Version History

- **2026-08-30** — Aligned Rule 2 permission wording to the live Data Quality Monitoring API: a schema monitor requires either `MANAGE` + `USE_CATALOG` on the parent catalog, or `USE_CATALOG` on the catalog + `MANAGE` + `USE_SCHEMA` on the schema; added the `SELECT`/`BROWSE` requirement for health indicators. Bumped `last_verified` and upstream `last_synced`.
