---
name: lakehouse-monitoring-comprehensive
description: Comprehensive guide for Databricks Lakehouse Monitoring (Data Profiling) with quick-start workflow (2 hours), fill-in-the-blank requirements template, concrete fact/dimension monitor examples, and complete deployment patterns. Uses the new Data Quality API (`databricks.sdk.service.dataquality`). Use when setting up Lakehouse Monitoring for Gold layer tables, creating custom business metrics, designing monitoring strategy, querying monitoring tables for dashboards, or troubleshooting monitor initialization failures. Includes setup patterns with graceful degradation, custom metric syntax (AGGREGATE, DERIVED, DRIFT), table-level business KPIs with `input_columns=[":table"]`, query patterns for dashboards, async operations handling, monitor cleanup, Genie documentation integration, and production deployment workflow.
clients: [ide_cli, genie_code]
bundle_resource: monitors
deploy_verb: bundle_deploy
deploy_note: "Lakehouse monitors (Data Quality API) on Gold tables, deployed via `bundle deploy --target dev` (runDatabricksCli on Genie Code); monitors target the per-user prefixed schema."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0"
  domain: monitoring
  role: worker
  triggers:
    - monitoring
    - Lakehouse
    - data profiling
    - custom metrics
    - AGGREGATE
    - DERIVED
    - DRIFT
    - profile metrics
    - drift metrics
    - monitor setup
    - data quality
  dependencies:
    - databricks-asset-bundles
    - sql-alerting-patterns
    - anomaly-detection
  last_verified: "2026-08-30"
  volatility: medium
  verification_sources:
    - url: "https://databricks-sdk-py.readthedocs.io/en/latest/workspace/dataquality/data_quality.html"
      check_for: "DataQualityAPI method signatures: create_monitor(monitor), create_refresh(object_type, object_id, refresh), delete_monitor(object_type, object_id), get_monitor, list_refresh, cancel_refresh, update_monitor(object_type, object_id, monitor, update_mask)"
    - url: "https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/dataquality.html"
      check_for: "Monitor, DataProfilingConfig, DataProfilingCustomMetric, DataProfilingCustomMetricType, TimeSeriesConfig, SnapshotConfig, AggregationGranularity, RefreshState, Refresh field names and enum values"
    - url: "https://learn.microsoft.com/en-us/azure/databricks/lakehouse-monitoring/custom-metrics"
      check_for: "Custom metric syntax (AGGREGATE, DERIVED, DRIFT), output_data_type format, Jinja template rules"
    - url: "https://docs.databricks.com/api/azure/workspace/dataquality/createmonitor"
      check_for: "REST API request/response schema, monitor creation payload structure"
  upstream_sources:
    - name: "databricks-sdk-py"
      repo: "databricks/databricks-sdk-py"
      paths:
        - "databricks/sdk/service/dataquality.py"
      relationship: "reference"
      last_synced: "2026-08-30"
      sync_commit: "latest"
---

# Lakehouse Monitoring Comprehensive

## Overview

Data Profiling monitors provide **table-level custom business metrics** that track data quality, detect drift, and support business KPI monitoring on Gold layer tables. This is the **custom metrics** counterpart to Anomaly Detection's automated freshness/completeness checks.

**API Status:** Public Preview (`POST /api/data-quality/v1/monitors`)

**SDK Module:** `databricks.sdk.service.dataquality` (replaces legacy `databricks.sdk.service.catalog`)

### When to Use This Skill vs. Anomaly Detection

| Need | Use This Skill | Use Anomaly Detection |
|------|---------------|----------------------|
| Custom business KPIs (revenue, velocity) | **Yes** | No |
| Table freshness checks | No | **Yes** |
| Schema-wide row completeness | No | **Yes** |
| Period-over-period drift | **Yes** (DRIFT metrics) | No |
| Per-table deep profiling | **Yes** | No (schema-level only) |
| ML model monitoring | **Yes** (InferenceLog) | No |

**Use both together** for comprehensive monitoring: data profiling for business KPIs + anomaly detection for baseline reliability.

## Quick Start (2-Hour Workflow)

| Phase | Duration | Activities |
|-------|----------|------------|
| Phase 1: Design | 30 min | Define metrics per table using `references/metric-design-guide.md` |
| Phase 2: Setup | 30 min | Run setup script from `scripts/create_monitor.py` |
| Phase 3: Wait | 15-20 min | Monitor initialization (async) using `scripts/wait_for_initialization.py` |
| Phase 4: Validate | 15 min | Query `_profile_metrics` and `_drift_metrics` tables |

## Critical Rules

### Rule 0: Permissions Required to Create a Table Monitor
To create a data profiling monitor on a **table**, the caller (user or service principal) must have **all** of:
- `USE CATALOG` on the parent catalog **and** `USE SCHEMA` on the parent schema,
- `SELECT` on the table, **and**
- `MANAGE` on the catalog, schema, **or** table.

`MANAGE` alone does not grant data access — `SELECT` on the table is always required. Viewing the dashboard, computed metrics, or monitor config only needs `SELECT` (+ `USE_SCHEMA`/`USE_CATALOG`). (Grant the app/job service principal these before running the setup job.)

### Rule 1: SDK Module — Use `dataquality`, NOT `catalog`
```python
# ✅ CORRECT (new API)
from databricks.sdk.service.dataquality import (
    Monitor,
    DataProfilingConfig,
    DataProfilingCustomMetric,
    DataProfilingCustomMetricType,
    TimeSeriesConfig,
    SnapshotConfig,
    AggregationGranularity,
)

# ❌ WRONG (legacy API — deprecated)
from databricks.sdk.service.catalog import MonitorMetric, MonitorMetricType
```

### Rule 2: create_monitor() Takes a Monitor Object
```python
# ✅ CORRECT: Wrap in Monitor object
table_info = w.tables.get(full_name=f"{catalog}.{schema}.{table}")
w.data_quality.create_monitor(
    monitor=Monitor(
        object_type="table",
        object_id=table_info.table_id,
        data_profiling_config=config,
    )
)

# ❌ WRONG: Three-level name
w.quality_monitors.create(table_name=f"{catalog}.{schema}.{table}", ...)
```

### Rule 3: Use SDK Objects, NOT Dictionaries
```python
# ✅ CORRECT: DataProfilingCustomMetric objects
DataProfilingCustomMetric(
    type=DataProfilingCustomMetricType.DATA_PROFILING_CUSTOM_METRIC_TYPE_AGGREGATE,
    name="total_revenue",
    input_columns=[":table"],
    definition="SUM(net_revenue)",
    output_data_type=T.StructField("output", T.DoubleType()).json()
)

# ❌ WRONG: Plain dictionaries
{"name": "total_revenue", "type": "AGGREGATE", "definition": "SUM(net_revenue)"}
```

### Rule 4: output_data_type MUST Be StructField JSON
```python
# ✅ CORRECT: StructField JSON format
output_data_type=T.StructField("output", T.DoubleType()).json()

# ❌ WRONG: String will silently fail monitor initialization
output_data_type="double"
```

### Rule 5: DERIVED Syntax — Direct Reference, No Templates
```python
# ✅ CORRECT: Direct reference to aggregate metric name
definition="(total_cancellations / NULLIF(total_bookings, 0)) * 100"

# ❌ WRONG: Template syntax causes INVALID_DERIVED_METRIC error
definition="({{total_cancellations}} / NULLIF({{total_bookings}}, 0)) * 100"
```

### Rule 6: DRIFT Syntax — MUST Use Window Templates
```python
# ✅ CORRECT: Compare windows
definition="{{current_df}}.daily_revenue - {{base_df}}.daily_revenue"

# ❌ WRONG: Missing window comparison
definition="{{daily_revenue}}"
```

### Rule 7: Use Typed Granularity Enums
```python
# ✅ CORRECT: AggregationGranularity enum
from databricks.sdk.service.dataquality import AggregationGranularity
TimeSeriesConfig(
    timestamp_column="transaction_date",
    granularities=[AggregationGranularity.AGGREGATION_GRANULARITY_1_DAY]
)

# ❌ WRONG: String granularity (legacy API)
MonitorTimeSeries(timestamp_col="transaction_date", granularities=["1 day"])
```

### Rule 8: Use Output Schema UUID
```python
# ✅ CORRECT: Get monitoring schema UUID
monitoring_schema = w.schemas.get(full_name=f"{catalog}.{schema}_monitoring")
DataProfilingConfig(output_schema_id=monitoring_schema.schema_id, ...)

# ❌ WRONG: output_schema_name is legacy
create_monitor(output_schema_name=f"{catalog}.{schema}_monitoring")
```

### Rule 9: Monitor Initialization Is Async (15-20 Minutes)
After creating a monitor, the first profile computation runs automatically. Use the Refresh tracking pattern in `scripts/wait_for_initialization.py` to poll for completion.

### Rule 10: Delete Cleanup — Drop Output Tables Too
```python
# Delete monitor definition
w.data_quality.delete_monitor(object_type="table", object_id=table_id)

# Also drop the output tables
spark.sql(f"DROP TABLE IF EXISTS {catalog}.{monitoring_schema}.{table}_profile_metrics")
spark.sql(f"DROP TABLE IF EXISTS {catalog}.{monitoring_schema}.{table}_drift_metrics")
```

## SDK Migration Summary

| Legacy (`catalog` module) | New (`dataquality` module) |
|--------------------------|---------------------------|
| `MonitorMetric` | `DataProfilingCustomMetric` |
| `MonitorMetricType.CUSTOM_METRIC_TYPE_AGGREGATE` | `DataProfilingCustomMetricType.DATA_PROFILING_CUSTOM_METRIC_TYPE_AGGREGATE` |
| `MonitorMetricType.CUSTOM_METRIC_TYPE_DERIVED` | `DataProfilingCustomMetricType.DATA_PROFILING_CUSTOM_METRIC_TYPE_DERIVED` |
| `MonitorMetricType.CUSTOM_METRIC_TYPE_DRIFT` | `DataProfilingCustomMetricType.DATA_PROFILING_CUSTOM_METRIC_TYPE_DRIFT` |
| `MonitorTimeSeries(timestamp_col=..., granularities=["1 day"])` | `TimeSeriesConfig(timestamp_column=..., granularities=[AggregationGranularity.AGGREGATION_GRANULARITY_1_DAY])` |
| `MonitorSnapshot()` | `SnapshotConfig()` |
| `MonitorInfoStatus.MONITOR_STATUS_ACTIVE` | `DataProfilingStatus.DATA_PROFILING_STATUS_ACTIVE` |
| `w.quality_monitors.create(table_name=...)` | `w.data_quality.create_monitor(monitor=Monitor(object_type="table", object_id=uuid, data_profiling_config=...))` |
| `w.quality_monitors.get(table_name=...)` | `w.data_quality.get_monitor(object_type="table", object_id=uuid)` |
| `w.quality_monitors.delete(table_name=...)` | `w.data_quality.delete_monitor(object_type="table", object_id=uuid)` |
| Manual status polling | `Refresh` object with `RefreshState` enum |

## Reference Files

### [custom-metrics.md](references/custom-metrics.md)
Custom metric type reference including:
- Required imports (`DataProfilingCustomMetric`, `DataProfilingCustomMetricType`)
- AGGREGATE syntax (SQL on table columns)
- DERIVED syntax (direct reference, NO `{{ }}`)
- DRIFT syntax (`{{current_df}}.metric - {{base_df}}.metric`)
- Business-focused metric categories
- `output_data_type` format (`T.StructField().json()`)

### [monitor-configuration.md](references/monitor-configuration.md)
Monitor setup patterns including:
- UUID lookup helpers (table and schema)
- `DataProfilingConfig` construction
- TimeSeries vs Snapshot configuration with typed granularities
- Graceful degradation (try/except for SDK imports)
- Notification settings
- Schedule configuration

### [deployment-guide.md](references/deployment-guide.md)
Operational deployment including:
- Genie Space documentation patterns
- Query patterns for `_profile_metrics` and `_drift_metrics` tables
- Ad-hoc ratio calculations (alternative to DERIVED metrics)
- Asset Bundle job configuration

### [quick-start-guide.md](references/quick-start-guide.md)
Fast-track setup including:
- Phase-based implementation checklist
- Fast-track code (corrected patterns)
- Sample metric queries
- Critical validation steps

### [metric-design-guide.md](references/metric-design-guide.md)
Metric design and planning including:
- Fill-in-the-blank requirements template
- Monitor priority definitions (P1-P3)
- Custom metric templates by category
- Alert strategy table

### [example-monitor-definitions.md](references/example-monitor-definitions.md)
Concrete implementation examples including:
- `create_fact_sales_daily_monitor()` — 9 metrics (aggregate + derived + drift)
- `create_dim_store_monitor()` — 4 metrics (snapshot)

## Scripts

### [create_monitor.py](scripts/create_monitor.py)
Core monitor management functions:
- `get_table_id()` / `get_schema_id()` — UUID lookup helpers
- `create_table_monitor()` — Full monitor creation with `DataProfilingConfig`
- `delete_monitor_if_exists()` — Safe cleanup with output table drops
- `wait_with_progress()` — Timer-based fallback wait

### [setup_monitors_template.py](scripts/setup_monitors_template.py)
Complete notebook template:
- `argparse` parameter handling
- Monitor tracking with success/failure reporting
- Error handling with graceful degradation
- `create_monitor_with_custom_metrics()` — Full pipeline

### [wait_for_initialization.py](scripts/wait_for_initialization.py)
Async monitoring:
- `wait_for_monitor_refresh()` — Refresh-based tracking with `RefreshState`
- `wait_for_all_monitors()` — Multi-table status polling with timeout

## Assets

### [monitoring-requirements-template.md](assets/templates/monitoring-requirements-template.md)
Fill-in-the-blank markdown template for defining monitoring requirements.

### [monitoring-job-template.yml](assets/templates/monitoring-job-template.yml)
Databricks Asset Bundle job template for deploying monitors.

## Troubleshooting

### Monitor Shows No Data After 20+ Minutes
1. Check monitor status via `w.data_quality.get_monitor()`
2. Check latest refresh: `w.data_quality.list_refresh()`
3. Verify table has data: `SELECT COUNT(*) FROM table`
4. Verify `output_data_type` uses `T.StructField().json()` format

### INVALID_DERIVED_METRIC Error
Using `{{metric_name}}` template syntax instead of direct reference. Remove all `{{ }}` from DERIVED metric definitions.

### Profile Metrics Table Empty
The `_profile_metrics` table is created by the monitor. If empty, the first refresh hasn't completed yet. Wait 15-20 minutes.

### "Monitor Already Exists" Error
Delete the existing monitor first using `delete_monitor_if_exists()` from `scripts/create_monitor.py`.

## References

- [Data Quality API](https://docs.databricks.com/api/azure/workspace/dataquality/createmonitor)
- [Python SDK Dataclasses](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/dataquality.html)
- [Lakehouse Monitoring Overview](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-monitoring/)
- [Custom Metrics](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-monitoring/custom-metrics)
- [Create Monitor API](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-monitoring/create-monitor-api)

## Version History

- **2026-08-30** — Added Rule 0 documenting the permissions to create a table (data profiling) monitor: `USE CATALOG` + `USE SCHEMA` + `SELECT` on the table, plus `MANAGE` on the catalog/schema/table (`MANAGE` alone does not grant data access). Bumped `last_verified` and upstream `last_synced`.
