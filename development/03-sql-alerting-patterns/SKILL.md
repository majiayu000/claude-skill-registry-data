---
name: sql-alerting-patterns
description: Comprehensive guide for Databricks SQL Alerts V2 - config-driven alerting framework with SDK deployment, hierarchical job architecture (5 atomic + 1 composite), proactive EXPLAIN-based query validation, and partial success patterns. Use when setting up SQL alerts, creating alert configuration tables, deploying alerts via Databricks SDK (V2 dict-based or typed classes), or troubleshooting alert failures. Includes config-driven patterns, fully qualified table names (no parameters), severity-based routing, alert ID conventions, SQL query patterns (threshold, percentage change, anomaly detection), DataFrame-based config seeding, DAB job configuration, custom notification templates, Quartz cron schedules, and troubleshooting patterns.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "SQL Alerts V2 config-driven; alert-deployment jobs (5 atomic + 1 composite) deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code); alert config tables live in the per-user prefixed schema."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  domain: monitoring
  role: worker
  pipeline_stage: 7
  pipeline_stage_name: observability
  called_by:
    - observability-setup
  standalone: true
  last_verified: "2026-08-30"
  volatility: medium
  upstream_sources: []  # Internal alerting patterns
---

# SQL Alerting: Config-Driven Framework for Databricks

## Overview

This skill provides a comprehensive config-driven framework for setting up Databricks SQL Alerts using the V2 API, a Delta configuration table, and SDK deployment. It covers alert rule design, SQL query patterns, SDK integration (both V2 dict-based and typed classes), hierarchical job architecture, proactive query validation, partial success deployment, and troubleshooting workflows.

## When to Use This Skill

- Setting up SQL alerts for Gold layer tables
- Creating alert configuration tables
- Deploying alerts via Databricks SDK (V2 or typed classes)
- Troubleshooting alert failures
- Implementing config-driven alerting (runtime updates without code changes)
- Creating severity-based notification routing
- Setting up hierarchical job architecture for alerting pipelines
- Validating alert queries before deployment

## Core Principles

### Principle 1: Config-Driven Alerting

Alert rules are stored in a Delta configuration table, not hardcoded. This enables:
- Runtime updates without code changes
- Centralized alert management
- Version history via Delta time travel
- Easy enable/disable without deployment

### Principle 2: Hierarchical Job Architecture

**⚠️ CRITICAL:** Use atomic + composite jobs pattern for production alerting:

```
Layer 1 (Atomic - single notebook per job):
├── alerting_tables_setup_job.yml    → setup_alerting_tables.py
├── seed_all_alerts_job.yml          → seed_all_alerts.py
├── alert_query_validation_job.yml   → validate_alert_queries.py
├── notification_destinations_sync_job.yml → sync_notification_destinations.py
└── sql_alert_deployment_job.yml     → sync_sql_alerts.py

Layer 2 (Composite - orchestrates via run_job_task):
└── alerting_layer_setup_job.yml     → References all atomic jobs
```

**Composite Job Pattern:**

```yaml
tasks:
  - task_key: setup_alerting_tables
    run_job_task:  # ✅ NOT notebook_task!
      job_id: ${resources.jobs.alerting_tables_setup_job.id}

  - task_key: deploy_sql_alerts
    depends_on:
      - task_key: validate_alert_queries
    run_job_task:
      job_id: ${resources.jobs.sql_alert_deployment_job.id}
```

**Benefits:** Test atomic jobs independently, debug failures at specific step, run subsets of pipeline.

#### Minimal Alternative: Two-Job Pattern

For simpler setups, a two-job separation still works:

1. **Setup Job** (`alert_rules_setup_job`): Creates/updates the `alert_rules` config table
2. **Deploy Job** (`alert_deploy_job`): Reads config table and creates/updates SQL Alerts via SDK

**Why This Matters:**
- Rules can be modified in Delta without redeploying alerts
- Dry-run capability for validation
- Clear separation between configuration and deployment

### Principle 3: Fully Qualified Table Names

**⚠️ CRITICAL:** Databricks SQL Alerts (Public Preview) do NOT support parameters in queries.

```sql
-- ❌ WRONG: Parameterized query (NOT SUPPORTED)
SELECT * FROM ${catalog}.${schema}.fact_booking_daily

-- ✅ CORRECT: Fully qualified table names embedded in query
SELECT * FROM wanderbricks_dev.gold.fact_booking_daily
```

**Pattern:** Use f-strings at rule creation time to embed catalog/schema:

```python
rev_001_query = f"""
SELECT ...
FROM {catalog}.{gold_schema}.fact_booking_daily
WHERE ...
"""
```

### Principle 4: Severity-Based Notification Routing

Alerts are categorized by severity with different notification strategies:

| Severity | Icon | Action Required | Notification Speed |
|----------|------|-----------------|-------------------|
| CRITICAL | 🔴 | Immediate | Real-time (email + Slack) |
| WARNING | 🟡 | Investigate soon | Batched (email) |
| INFO | 🟢 | Informational | Daily digest |

### Principle 5: Proactive Query Validation

**⚠️ CRITICAL:** Run EXPLAIN on all alert queries before deployment to catch column/table errors early.

```python
def validate_alert_query(spark, alert_id: str, query: str) -> tuple:
    """Validate query using EXPLAIN."""
    try:
        spark.sql(f"EXPLAIN {query}")
        return (alert_id, True, None)
    except Exception as e:
        if "UNRESOLVED_COLUMN" in str(e):
            return (alert_id, False, "Column not found")
        elif "TABLE_OR_VIEW_NOT_FOUND" in str(e):
            return (alert_id, False, "Table not found")
        return (alert_id, False, f"Error: {str(e)[:100]}")
```

Create a dedicated validation job (`alert_query_validation_job`) that tests all alert queries before deployment. This catches:
- Missing tables (renamed/dropped)
- Missing columns (schema evolution)
- SQL syntax errors
- Permission issues

### Principle 6: Partial Success Tolerance

**⚠️ CRITICAL:** Allow deployment to succeed if ≥90% of alerts deploy successfully. Don't fail the entire deployment for a single alert issue.

```python
# Allow job to succeed if ≥90% of alerts deploy successfully
if success_rate >= 90:
    print(f"⚠️ Partial success: {success_rate:.0f}% ({success_count}/{total})")
else:
    raise RuntimeError(f"Too many failures: {len(errors)} errors")
```

### Principle 7: DataFrame-Based Config Seeding

**⚠️ CRITICAL:** Never use SQL INSERT for seeding alert configurations. Use DataFrame instead.

**Problem:** SQL INSERT with `replace("'", "''")` breaks LIKE patterns:

```sql
-- Original: WHERE sku_name LIKE '%ALL_PURPOSE%'
-- After INSERT escaping: WHERE sku_name LIKE %ALL_PURPOSE% (quotes lost!)
```

**Solution:** Use DataFrame with explicit schema:

```python
# ✅ CORRECT: DataFrame handles escaping automatically
rows = [(alert_id, alert_name, alert_query, ...)]
df = spark.createDataFrame(rows, schema)
df.write.mode("append").saveAsTable(cfg_table)
```

## Quick Reference

### Alert ID Convention

**Format:** `<DOMAIN>-<NUMBER>-<SEVERITY>`

**Components:**
- `DOMAIN`: Business domain (3-4 chars): REV, ENG, PROP, HOST, CUST, COST, SECURITY, PERF
- `NUMBER`: Sequential within domain (3 digits, zero-padded)
- `SEVERITY`: CRIT, WARN, or INFO

**Examples:**
- `REV-001-CRIT` → Revenue domain, alert #1, critical severity
- `ENG-003-WARN` → Engagement domain, alert #3, warning severity
- `PROP-004-INFO` → Property domain, alert #4, informational
- `COST-001-CRIT` → Cost domain, alert #1, critical severity
- `SECURITY-003-WARN` → Security domain, alert #3, warning
- `PERF-005-INFO` → Performance domain, alert #5, informational

### Alert Rules Configuration Table Schema

**Required Columns for SDK Deployment:**

| Column | SDK Field | Required | Notes |
|--------|-----------|----------|-------|
| `alert_query` | `query_text` | ✅ | Full SQL query |
| `condition_column` | `AlertOperandColumn.name` | ✅ | Column to check |
| `condition_operator` | `AlertConditionOperator` | ✅ | >, <, =, etc. |
| `condition_threshold` | `AlertOperandValue.string_value` | ✅ | Threshold value |
| `schedule_cron` | `cron_schedule` | ✅ | Quartz format |
| `schedule_timezone` | `cron_timezone` | ✅ | IANA timezone |

See [alert-patterns.md](references/alert-patterns.md) for complete schema definition.

### SQL Query Patterns

1. **Threshold Comparison** - Alert when metric crosses threshold
2. **Percentage Change from Baseline** - Alert when metric deviates from historical average
3. **Statistical Anomaly Detection (Z-Score)** - Alert when metric is statistically unusual
4. **Count-Based Alert** - Alert when count is below threshold
5. **Informational Summary** - Always triggers for daily/weekly summaries

See [alert-patterns.md](references/alert-patterns.md) for detailed SQL examples.

### SDK Setup (Critical!)

**⚠️ This is the #1 operational gotcha.** The SDK must be upgraded at runtime for V2 API support:

```python
# Databricks notebook source
# MAGIC %pip install --upgrade databricks-sdk>=0.40.0 --quiet

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import AlertV2
```

### V2 API Payload Structure

```python
alert_dict = {
    "display_name": "[CRITICAL] Alert Name",
    "query_text": "SELECT column FROM catalog.schema.table WHERE condition",
    "warehouse_id": "warehouse-id",
    "schedule": {
        "quartz_cron_schedule": "0 0 * * * ?",  # Every hour
        "timezone_id": "America/Los_Angeles",
        "pause_status": "UNPAUSED"
    },
    "evaluation": {
        "source": {"name": "column_name", "aggregation": "SUM"},
        "comparison_operator": "GREATER_THAN",
        "threshold": {"value": {"double_value": 1000}},
        "empty_result_state": "OK",
        "notification": {
            "notify_on_ok": False,
            "subscriptions": [{"user_email": "user@company.com"}]
        }
    }
}

alert_v2 = AlertV2.from_dict(alert_dict)
ws.alerts_v2.create_alert(alert_v2)
```

See [sdk-api-reference.md](references/sdk-api-reference.md) for complete V2 API details.

### Comparison Operators

| Operator | API Value |
|----------|-----------|
| `>` | `GREATER_THAN` |
| `>=` | `GREATER_THAN_OR_EQUAL` |
| `<` | `LESS_THAN` |
| `<=` | `LESS_THAN_OR_EQUAL` |
| `=` | `EQUAL` |
| `!=` | `NOT_EQUAL` |
| `IS NULL` | `IS_NULL` |

### Aggregation Types

`SUM`, `COUNT`, `COUNT_DISTINCT`, `AVG`, `MEDIAN`, `MIN`, `MAX`, `STDDEV`, `FIRST` (null in API)

## Critical Rules

### Rule 1: Fully Qualified Table Names Only

**❌ WRONG:** Parameterized queries (NOT SUPPORTED)

```sql
SELECT * FROM ${catalog}.${schema}.fact_booking_daily
```

**✅ CORRECT:** Fully qualified names embedded at rule creation

```python
alert_query = f"""
SELECT * FROM {catalog}.{gold_schema}.fact_booking_daily
WHERE check_in_date = DATE_ADD(CURRENT_DATE(), -1)
"""
```

### Rule 2: Query Must Return Rows Only When Condition Met

**❌ WRONG:** Returns rows always

```sql
SELECT rate FROM ... WHERE rate IS NOT NULL
```

**✅ CORRECT:** Only returns rows when threshold crossed

```sql
SELECT rate FROM ... HAVING rate > 15
```

### Rule 3: Always Include alert_message Column

**✅ CORRECT:** Human-readable notification content

```sql
SELECT
    cancellation_rate,
    'CRITICAL: Cancellation rate at ' || cancellation_rate || '%' as alert_message
FROM ...
HAVING cancellation_rate > 15
```

### Rule 4: Use NULLIF for Division

**✅ CORRECT:** Prevent division by zero errors

```sql
ROUND(SUM(cancellation_count) / NULLIF(SUM(booking_count), 0) * 100, 1) as cancellation_rate
```

### Rule 5: Use DataFrame for Config Seeding (Never SQL INSERT)

**⚠️ CRITICAL:** SQL INSERT with string escaping breaks LIKE patterns in alert queries. See Principle 7.

```python
# ❌ WRONG: SQL INSERT loses quotes in LIKE patterns
spark.sql(f"INSERT INTO {table} VALUES ('{alert_query.replace(chr(39), chr(39)+chr(39))}')")

# ✅ CORRECT: DataFrame handles escaping automatically
rows = [(alert_id, alert_name, alert_query, ...)]
df = spark.createDataFrame(rows, schema)
df.write.mode("append").saveAsTable(cfg_table)
```

### Rule 6: No CHECK Constraints or DEFAULT Values in DDL

**⚠️ Unity Catalog limitation:** CHECK constraints and DEFAULT values are not supported in DDL. Validate in code instead.

```python
# ❌ WRONG: CHECK constraints in DDL (not supported)
# severity STRING NOT NULL CHECK (severity IN ('CRITICAL', 'WARNING', 'INFO'))

# ✅ CORRECT: Validate in code
assert rule["severity"] in ("CRITICAL", "WARNING", "INFO"), f"Invalid severity: {rule['severity']}"
```

### Rule 7: Validate Queries with EXPLAIN Before Deployment

**⚠️ CRITICAL:** Run EXPLAIN on all alert queries before deployment. See Principle 5.

```python
# ✅ CORRECT: Validate before deploying
for rule in alert_rules:
    alert_id, is_valid, error = validate_alert_query(spark, rule["alert_id"], rule["alert_query"])
    if not is_valid:
        print(f"❌ {alert_id}: {error}")
```

## Core Patterns

### Pattern 1: Alert Rules Configuration Table

```sql
CREATE TABLE IF NOT EXISTS {catalog}.{gold_schema}.alert_rules (
    alert_id STRING NOT NULL,
    alert_name STRING NOT NULL,
    domain STRING NOT NULL,
    severity STRING NOT NULL,
    alert_description STRING NOT NULL,
    alert_query STRING NOT NULL,
    condition_column STRING NOT NULL,
    condition_operator STRING NOT NULL,
    condition_threshold STRING NOT NULL,
    aggregation_type STRING,
    schedule_cron STRING NOT NULL,
    schedule_timezone STRING NOT NULL,
    notification_emails STRING,
    notification_slack_channel STRING,
    custom_subject_template STRING,
    custom_body_template STRING,
    notify_on_ok BOOLEAN NOT NULL,
    rearm_seconds INT,
    is_enabled BOOLEAN NOT NULL,
    tags STRING,
    owner STRING NOT NULL,
    record_created_timestamp TIMESTAMP NOT NULL,
    record_updated_timestamp TIMESTAMP NOT NULL,
    CONSTRAINT pk_alert_rules PRIMARY KEY (alert_id) NOT ENFORCED
)
USING DELTA
CLUSTER BY AUTO
```

### Pattern 2a: SDK Alert Creation (Typed Classes)

**Note:** Works with `databricks-sdk>=0.28.0`. See Pattern 2b for the newer V2 dict-based approach.

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import (
    AlertCondition,
    AlertConditionOperand,
    AlertConditionThreshold,
    AlertOperandColumn,
    AlertOperandValue,
    AlertConditionOperator,
)

def create_alert(ws: WorkspaceClient, rule: dict, warehouse_id: str):
    """Create a SQL Alert from a rule configuration."""

    # Build condition
    condition = AlertCondition(
        op=get_operator_enum(rule["condition_operator"]),
        operand=AlertConditionOperand(
            column=AlertOperandColumn(name=rule["condition_column"])
        ),
        threshold=AlertConditionThreshold(
            value=AlertOperandValue(
                string_value=str(rule["condition_threshold"])
            )
        )
    )

    # Create alert
    new_alert = ws.alerts.create(
        display_name=f"[{rule['severity']}] {rule['alert_name']}",
        query_text=rule["alert_query"],
        warehouse_id=warehouse_id,
        condition=condition,
        cron_schedule=rule["schedule_cron"],
        cron_timezone=rule["schedule_timezone"],
        notify_on_ok=rule.get("notify_on_ok", False),
        custom_subject=rule.get("custom_subject_template"),
        custom_body=rule.get("custom_body_template"),
    )

    return new_alert
```

### Pattern 2b: SDK Alert Creation (V2 Dict-Based)

**Note:** Requires `databricks-sdk>=0.40.0`. This is the newer, recommended approach.

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import AlertV2

def create_alert_v2(ws: WorkspaceClient, rule: dict, warehouse_id: str):
    """Create a SQL Alert using V2 dict-based API."""

    alert_dict = {
        "display_name": f"[{rule['severity']}] {rule['alert_name']}",
        "query_text": rule["alert_query"],
        "warehouse_id": warehouse_id,
        "schedule": {
            "quartz_cron_schedule": rule["schedule_cron"],
            "timezone_id": rule["schedule_timezone"],
            "pause_status": "UNPAUSED" if rule["is_enabled"] else "PAUSED"
        },
        "evaluation": {
            "source": {
                "name": rule["condition_column"],
                "aggregation": rule.get("aggregation_type", "FIRST")
            },
            "comparison_operator": rule["condition_operator"],
            "threshold": {
                "value": {"double_value": float(rule["condition_threshold"])}
            },
            "empty_result_state": "OK",
            "notification": {
                "notify_on_ok": rule.get("notify_on_ok", False),
                "subscriptions": [
                    {"user_email": email.strip()}
                    for email in rule.get("notification_emails", "").split(",")
                    if email.strip()
                ]
            }
        }
    }

    alert_v2 = AlertV2.from_dict(alert_dict)
    return ws.alerts_v2.create_alert(alert_v2)
```

See [sdk-api-reference.md](references/sdk-api-reference.md) for complete V2 API reference including comparison operators, aggregation types, and API gotchas.

### Pattern 3: Idempotent Deployment

```python
def deploy_alert(ws: WorkspaceClient, rule: dict, warehouse_id: str,
                 existing_alerts: dict, dry_run: bool = False):
    """Deploy alert with idempotency check."""

    alert_name = f"[{rule['severity']}] {rule['alert_name']}"
    existing = existing_alerts.get(alert_name)

    if dry_run:
        if existing:
            print(f"[DRY RUN] Would update: {existing.id}")
        else:
            print(f"[DRY RUN] Would create new alert")
        return {"status": "dry_run"}

    if existing:
        print(f"Alert exists: {existing.id} - skipping")
        return {"status": "skipped", "id": existing.id}

    # Create new alert
    new_alert = create_alert(ws, rule, warehouse_id)
    return {"status": "created", "id": new_alert.id}
```

#### Handling RESOURCE_ALREADY_EXISTS

When creating alerts, you may encounter `RESOURCE_ALREADY_EXISTS` errors. Handle by refreshing the alert list and updating instead:

```python
try:
    new_alert = ws.alerts_v2.create_alert(alert_v2)
except Exception as e:
    if "RESOURCE_ALREADY_EXISTS" in str(e):
        # Refresh alert list and update instead
        existing_alerts = {a.display_name: a for a in ws.alerts_v2.list_alerts().alerts}
        existing = existing_alerts.get(alert_name)
        if existing:
            ws.alerts_v2.update_alert(
                id=existing.id,  # ⚠️ param is `id`, NOT `alert_id`
                alert=alert_v2,
                update_mask="query_text,evaluation,schedule"  # ⚠️ Required!
            )
    else:
        raise
```

**Key:** PATCH requests require the `update_mask` parameter specifying which fields to update. The SDK signature is `update_alert(id, alert, update_mask)` — pass the alert UUID as `id` (not `alert_id`).

### Pattern 4: DAB Job Configuration

#### Minimal (2-Job) Configuration

**Setup Job:**

```yaml
resources:
  jobs:
    alert_rules_setup_job:
      name: "[${bundle.target} ${var.user_prefix}] Alert Rules - Setup"
      description: "Creates alert_rules configuration table"
      environments:
        - environment_key: default
          spec:
            environment_version: "4"
      tasks:
        - task_key: setup_alert_rules
          environment_key: default
          notebook_task:
            notebook_path: ../../src/alerting/setup_alert_rules.py
            base_parameters:
              catalog: ${var.catalog}
              gold_schema: ${var.gold_schema}
```

**Deploy Job:**

```yaml
resources:
  jobs:
    alert_deploy_job:
      name: "[${bundle.target} ${var.user_prefix}] Alert - Deploy"
      description: "Deploys SQL alerts from alert_rules configuration table"
      environments:
        - environment_key: default
          spec:
            environment_version: "4"
            dependencies:
              - "databricks-sdk>=0.40.0"  # Required for V2 alerts API
      tasks:
        - task_key: deploy_alerts
          environment_key: default
          notebook_task:
            notebook_path: ../../src/alerting/deploy_alerts.py
            base_parameters:
              catalog: ${var.catalog}
              gold_schema: ${var.gold_schema}
              warehouse_id: ${var.warehouse_id}
              dry_run: "false"
```

#### Production (5+1 Hierarchical) Configuration

**Composite Orchestrator Job:**

```yaml
resources:
  jobs:
    alerting_layer_setup_job:
      name: "[${bundle.target} ${var.user_prefix}] Alerting Layer - Full Setup"
      description: "Orchestrates all alerting setup jobs"
      tasks:
        - task_key: setup_alerting_tables
          run_job_task:
            job_id: ${resources.jobs.alerting_tables_setup_job.id}

        - task_key: seed_all_alerts
          depends_on:
            - task_key: setup_alerting_tables
          run_job_task:
            job_id: ${resources.jobs.seed_all_alerts_job.id}

        - task_key: validate_alert_queries
          depends_on:
            - task_key: seed_all_alerts
          run_job_task:
            job_id: ${resources.jobs.alert_query_validation_job.id}

        - task_key: sync_notification_destinations
          depends_on:
            - task_key: setup_alerting_tables
          run_job_task:
            job_id: ${resources.jobs.notification_destinations_sync_job.id}

        - task_key: deploy_sql_alerts
          depends_on:
            - task_key: validate_alert_queries
            - task_key: sync_notification_destinations
          run_job_task:
            job_id: ${resources.jobs.sql_alert_deployment_job.id}
```

### Pattern 5: Proactive Query Validation

```python
def validate_alert_query(spark, alert_id: str, query: str) -> tuple:
    """Validate query using EXPLAIN."""
    try:
        spark.sql(f"EXPLAIN {query}")
        return (alert_id, True, None)
    except Exception as e:
        if "UNRESOLVED_COLUMN" in str(e):
            return (alert_id, False, "Column not found")
        elif "TABLE_OR_VIEW_NOT_FOUND" in str(e):
            return (alert_id, False, "Table not found")
        return (alert_id, False, f"Error: {str(e)[:100]}")


# Usage: validate all rules before deployment
def validate_all_rules(spark, rules: list) -> tuple:
    """Validate all alert queries and return results."""
    results = [validate_alert_query(spark, r["alert_id"], r["alert_query"]) for r in rules]
    valid = [r for r in results if r[1]]
    invalid = [r for r in results if not r[1]]

    for alert_id, _, error in invalid:
        print(f"❌ {alert_id}: {error}")

    print(f"✅ {len(valid)}/{len(results)} queries valid")
    return valid, invalid
```

### Pattern 6: Partial Success Deployment

```python
def deploy_all_alerts(ws, rules, warehouse_id, dry_run=False):
    """Deploy all alerts with partial success tolerance."""
    existing_alerts = {a.display_name: a for a in ws.alerts_v2.list_alerts().alerts}

    results = []
    errors = []

    for rule in rules:
        try:
            result = deploy_alert(ws, rule, warehouse_id, existing_alerts, dry_run)
            results.append(result)
        except Exception as e:
            errors.append({"alert_id": rule["alert_id"], "error": str(e)})

    success_count = len(results)
    total = success_count + len(errors)
    success_rate = (success_count / total * 100) if total > 0 else 100

    # Allow job to succeed if ≥90% of alerts deploy successfully
    if success_rate >= 90:
        print(f"⚠️ Partial success: {success_rate:.0f}% ({success_count}/{total})")
    else:
        raise RuntimeError(f"Too many failures: {len(errors)} errors")

    return results, errors
```

## File Structure

```
src/alerting/
├── alerting_config.py              # Config helpers, dataclasses
├── alerting_metrics.py             # Metrics collection
├── setup_alerting_tables.py        # Creates Delta config tables
├── seed_all_alerts.py              # Seeds alert configs (DataFrame-based)
├── validate_alert_queries.py       # EXPLAIN-based query validation
├── sync_notification_destinations.py # Syncs notification channels
└── sync_sql_alerts.py              # SDK-based sync engine

resources/alerting/
├── alerting_layer_setup_job.yml          # Layer 2: Composite orchestrator
├── alerting_tables_setup_job.yml         # Layer 1: Atomic
├── seed_all_alerts_job.yml               # Layer 1: Atomic
├── alert_query_validation_job.yml        # Layer 1: Atomic
├── notification_destinations_sync_job.yml # Layer 1: Atomic
└── sql_alert_deployment_job.yml          # Layer 1: Atomic
```

## Reference Files

### [alert-patterns.md](references/alert-patterns.md)

Comprehensive SQL alert patterns including:
- SQL query patterns (threshold, percentage change, anomaly detection, count-based, informational)
- Complete alert examples (CRITICAL, WARNING, INFO)
- Custom notification templates
- Schedule patterns (Quartz cron)
- Query design rules

### [sdk-api-reference.md](references/sdk-api-reference.md)

Complete SDK and V2 API reference including:
- V2 API payload structure with field descriptions
- Comparison operators table
- Aggregation types reference
- API gotchas and common pitfalls
- SDK version requirements
- SDK setup ceremony for notebooks

## Assets

### [alert-config.yaml](assets/templates/alert-config.yaml)

Template configuration file for alert rules with example structure.

## Troubleshooting

### Problem: Alert Not Triggering

**Symptoms:** Alert is enabled but never sends notifications

**Diagnosis Steps:**
1. Run the alert query manually - does it return rows?
2. Check condition: does returned value satisfy operator + threshold?
3. Verify warehouse is running when schedule fires
4. Check notification destination configuration

**Fix:** Add HAVING clause to filter results:

```sql
-- ✅ CORRECT: Only returns rows when threshold crossed
SELECT rate FROM ... HAVING rate > 15
```

### Problem: Alert Always Triggering

**Symptoms:** Getting notifications even when condition shouldn't be met

**Fix:** Query returns rows even when condition isn't met - missing HAVING clause

### Problem: "Query Failed" Error Status

**Common Causes:**
1. Table doesn't exist (wrong catalog/schema)
2. Column doesn't exist
3. SQL syntax error
4. Warehouse unavailable

**Debug:** Test query in notebook first:

```python
spark.sql(f"""
    {alert_query}
""").display()
```

### Problem: SDK Permission Error

**Fix:** Ensure service principal or user has:
- `CAN_MANAGE` permission on SQL Warehouse
- `CAN_CREATE` permission for SQL Alerts
- `CAN_USE` on catalog and schema

### Problem: RESOURCE_ALREADY_EXISTS on Create

**Symptoms:** `RESOURCE_ALREADY_EXISTS` error when creating an alert that was previously deleted or has the same display name.

**Fix:** Refresh the alert list and update instead of creating:

```python
# Refresh alert list
existing_alerts = {a.display_name: a for a in ws.alerts_v2.list_alerts().alerts}
existing = existing_alerts.get(alert_name)
if existing:
    ws.alerts_v2.update_alert(
        id=existing.id,  # ⚠️ param is `id`, NOT `alert_id`
        alert=alert_v2,
        update_mask="query_text,evaluation,schedule"  # ⚠️ Required!
    )
```

### Problem: LIKE Pattern Quotes Lost in Config Table

**Symptoms:** Alert queries with LIKE patterns (`'%ALL_PURPOSE%'`) lose their quotes after being inserted into the config table via SQL INSERT.

**Root Cause:** `replace("'", "''")` breaks LIKE patterns during SQL INSERT escaping.

**Fix:** Use DataFrame-based seeding instead of SQL INSERT:

```python
# ✅ CORRECT: DataFrame handles escaping automatically
rows = [(alert_id, alert_name, alert_query, ...)]
df = spark.createDataFrame(rows, schema)
df.write.mode("append").saveAsTable(cfg_table)
```

### Problem: SDK ImportError for AlertV2

**Symptoms:** `ImportError: cannot import name 'AlertV2' from 'databricks.sdk.service.sql'`

**Root Cause:** SDK version is too old. AlertV2 requires `databricks-sdk>=0.40.0`.

**Fix:** Upgrade SDK at runtime:

```python
# MAGIC %pip install --upgrade databricks-sdk>=0.40.0 --quiet
# COMMAND ----------
# MAGIC %restart_python
```

### Problem: PATCH Update Fails

**Symptoms:** Alert update via PATCH returns an error or silently fails.

**Root Cause:** Missing `update_mask` parameter. PATCH requests require specifying which fields to update.

**Fix:** Include `update_mask` in update calls (and pass the UUID as `id`, not `alert_id`):

```python
ws.alerts_v2.update_alert(
    id=existing.id,  # ⚠️ param is `id`, NOT `alert_id`
    alert=alert_v2,
    update_mask="query_text,evaluation,schedule"  # ⚠️ Required!
)
```

## Best Practices

### ✅ DO

1. **Use config table for all rules** - Never hardcode alert configurations
2. **Include `alert_message` column** - Human-readable notification content
3. **Test queries manually first** - Verify in notebook before adding to config
4. **Use NULLIF for division** - Prevent division by zero errors
5. **Set appropriate rearm periods** - Prevent alert fatigue (1800-3600 seconds)
6. **Enable notify_on_ok for critical** - Know when issues are resolved
7. **Use dry_run for validation** - Test deployment without creating alerts
8. **Run EXPLAIN on all alert queries before deployment** - Catch errors early (see Principle 5)
9. **Use DataFrame (not SQL INSERT) for config seeding** - Prevent escaping bugs (see Principle 7)
10. **Allow partial success (≥90%) for deployment jobs** - Don't fail all for one (see Principle 6)

### ❌ DON'T

1. **Don't use parameters in queries** - SQL Alerts don't support `${param}` syntax
2. **Don't skip the HAVING clause** - Queries should only return rows when alerting
3. **Don't set rearm too low** - Causes notification spam
4. **Don't hardcode credentials** - Use WorkspaceClient() for auto-auth
5. **Don't skip schema validation** - Verify alert_rules table exists before deploying
6. **Don't use SQL INSERT for queries with LIKE patterns** - Quotes get lost (see Rule 5)
7. **Don't use CHECK or DEFAULT in config table DDL** - Not supported in Unity Catalog (see Rule 6)

## Workflow Summary

### Initial Setup (Hierarchical)

> **Client note:** IDE runs these in a terminal; Genie Code runs the `databricks bundle …` commands via `runDatabricksCli` (be on the bundle's page). See `skills/genie-code-environment`.

```bash
# 1. Deploy all alerting infrastructure (composite orchestrator)
databricks bundle run alerting_layer_setup_job -t dev

# Or run individual atomic jobs (see below)
```

### Initial Setup (Minimal 2-Job)

```bash
# 1. Deploy alert rules table
databricks bundle run alert_rules_setup_job -t dev

# 2. Verify rules
# SELECT * FROM {catalog}.{gold_schema}.alert_rules

# 3. Deploy alerts (dry run first)
# Edit dry_run: "true" in job config
databricks bundle run alert_deploy_job -t dev

# 4. Deploy alerts (for real)
# Edit dry_run: "false" in job config
databricks bundle run alert_deploy_job -t dev
```

### Running Individual Jobs

Run atomic jobs independently for debugging or partial updates:

```bash
# Just set up tables
databricks bundle run alerting_tables_setup_job -t dev

# Just seed alert configurations
databricks bundle run seed_all_alerts_job -t dev

# Just validate queries (after config changes)
databricks bundle run alert_query_validation_job -t dev

# Just sync notification destinations
databricks bundle run notification_destinations_sync_job -t dev

# Just deploy alerts (after validation passes)
databricks bundle run sql_alert_deployment_job -t dev
```

### Adding New Alerts

1. Add rule to `get_alert_rules()` function in `seed_all_alerts.py` (or `setup_alert_rules.py` for 2-job pattern)
2. Run seed job: `databricks bundle run seed_all_alerts_job -t dev`
3. Run validation: `databricks bundle run alert_query_validation_job -t dev`
4. Run deploy job: `databricks bundle run sql_alert_deployment_job -t dev`

### Modifying Existing Alerts

1. Update rule in config table or seed script
2. Run seed job to update config table
3. Delete existing alert in Databricks UI
4. Run deploy job to recreate with new configuration

## Key Learnings

Hard-won operational lessons from production deployment:

1. **API Endpoint**: Use `/api/2.0/alerts` (NOT `/api/2.0/sql/alerts-v2`)
2. **SDK Version**: Requires `%pip install --upgrade databricks-sdk>=0.40.0` + `%restart_python`
3. **List Response**: V2 API returns `alerts` key (NOT `results`)
4. **Update Mask**: PATCH requests require `update_mask` parameter
5. **RESOURCE_ALREADY_EXISTS**: Handle by refreshing alert list and updating instead
6. **Fully Qualified Names**: Alerts don't support query parameters
7. **⚠️ SQL Escaping**: Use DataFrame (not SQL INSERT) for inserting queries - LIKE patterns lose quotes otherwise
8. **Proactive Validation**: Run EXPLAIN on all queries before deployment to catch column/table errors
9. **Hierarchical Jobs**: Atomic jobs (single notebook) + Composite jobs (`run_job_task`) for production
10. **Partial Success**: Allow ≥90% success rate - don't fail entire deployment for single alert issues
11. **Unity Catalog**: No CHECK constraints, no DEFAULT values in DDL - validate in code

## References

- [Databricks SQL Alerts Documentation](https://docs.databricks.com/sql/user/alerts/)
- [Alert Notifications](https://docs.databricks.com/sql/user/alerts/index.html#notifications)
- [Databricks SDK - Alerts API](https://databricks-sdk-py.readthedocs.io/en/latest/)
- [Databricks SDK - Alerts V2 API](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/sql/alerts_v2.html)
- [V2 API Documentation](https://docs.databricks.com/api/workspace/alertsv2/createalert)
- [Quartz Cron Expression Format](http://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html)

## Summary

**Key Takeaways:**
- Use config-driven approach with Delta table for runtime updates
- Hierarchical 5+1 job architecture for production (or minimal 2-job for simple setups)
- Fully qualified table names only (no parameters)
- Queries must return rows ONLY when condition is met (HAVING clause)
- Always include `alert_message` column for notifications
- Use NULLIF for division to prevent errors
- Validate all queries with EXPLAIN before deployment
- Use DataFrame-based config seeding (never SQL INSERT)
- Allow partial success (≥90%) for deployment resilience
- Use V2 dict-based SDK pattern (>=0.40.0) for newest API features

**Next Steps:**
1. Review [alert-patterns.md](references/alert-patterns.md) for SQL query examples
2. Review [sdk-api-reference.md](references/sdk-api-reference.md) for V2 API details
3. Set up alert_rules configuration table
4. Create hierarchical job architecture
5. Test with dry_run before production deployment

## Version History

- **2026-08-30** — Fixed `alerts_v2.update_alert` keyword from `alert_id=` to `id=` (the SDK signature is `update_alert(id, alert, update_mask)`); corrected deletion verb from the non-existent `delete_alert` to `trash_alert(id, purge)`; noted `get_alert(id)` as the V2 read verb. Bumped `last_verified`.
