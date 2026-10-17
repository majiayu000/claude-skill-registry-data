---
name: etl-runbook
description: >
  Write an ETL operational runbook. Use when the user says "ETL runbook", "pipeline runbook",
  "data job runbook", "how to operate this ETL", "on-call guide for data pipelines",
  "what to do when the data job fails", "pipeline troubleshooting guide",
  "data ops runbook", or needs to document how to operate, monitor, and recover a
  data pipeline or ETL job - even if they don't explicitly say "runbook".
---

## Overview

Based on **Data Pipelines Pocket Reference** (Densmore) and **Fundamentals of Data Engineering** (Reis & Housley). An ETL runbook is the operational contract for a data job: how to monitor it, diagnose when it breaks, and recover data integrity. Densmore's standard: data pipelines fail in subtle ways - not always with an error, sometimes with silent data loss or incorrect rows. A good runbook covers job failures AND data quality failures.

The test: can an on-call engineer who didn't build this pipeline detect a problem, isolate the cause, and restore data integrity at 3am?

## Workflow

### Step 1: Write the job overview

```
Job: [job name]
Pipeline: [parent pipeline name]
Owner: [team]
Purpose: [what this job does and what breaks downstream if it doesn't run]
Schedule: [cron expression or trigger condition]
SLA: [data must be available by X time or downstream is impacted]
Typical runtime: [expected duration, e.g. 15-25 minutes]
Max runtime before alert: [e.g. 45 minutes]
Orchestrator: [Airflow / Prefect / dbt Cloud / etc.]
Job link: [direct link to job in orchestration UI]
Dashboard: [link to data quality/freshness monitoring]
```

### Step 2: Define what "healthy" looks like

Data quality thresholds, not just job status:

```
Healthy signals:
- Job status: SUCCESS
- Row count: [expected range, e.g. 50,000–200,000 rows]
- Null rate on critical fields: < 0.1%
- Duplicate rate: 0% (on primary key)
- Freshness: data timestamp within [N hours] of run time
- Downstream table last_updated: matches run date

Alert on these metrics: [link to monitoring tool]
```

### Step 3: Diagnose a failed job

Use this decision tree when a job fails or an alert fires:

**1. Check job status:**
```
[Orchestration UI link] → find the failed run → check error message
Common errors:
  - "Connection refused" → source database is unavailable (see Step 4a)
  - "Schema mismatch" → source schema changed (see Step 4b)
  - "Out of memory" → data volume spike (see Step 4c)
  - "Timeout" → source query is slow (see Step 4d)
```

**2. Check if data arrived:**
```sql
-- Did the source data land in the raw layer?
SELECT COUNT(*), MAX(extracted_at)
FROM raw.[source_table]
WHERE DATE(extracted_at) = CURRENT_DATE;
-- Expected: > 0 rows, extracted_at within last [N] hours
```

**3. Check data quality:**
```sql
-- Are there unexpected nulls?
SELECT COUNT(*) as nulls
FROM [target_table]
WHERE [critical_field] IS NULL AND DATE(created_at) = CURRENT_DATE;
-- Expected: 0

-- Are there duplicates?
SELECT [primary_key], COUNT(*) as cnt
FROM [target_table]
WHERE DATE(created_at) = CURRENT_DATE
GROUP BY [primary_key] HAVING cnt > 1;
-- Expected: 0 rows
```

### Step 4: Resolve common failures

**4a. Source database unavailable**
```
Check: ping source system or check their status page
If transient (< 30 min): wait and trigger a manual rerun after source recovers
If prolonged: escalate to source team via [contact method]
Rerun command: [airflow trigger_dag / dbt run / etc.]
```

**4b. Source schema changed**
```
Symptom: column not found / type mismatch error in job logs
Diagnose: compare current source schema against schema spec [link]
Fix:
  1. Identify which column changed
  2. Update schema spec
  3. Update pipeline transformation logic
  4. Backfill affected date range (see backfill section)
Escalate: notify [data platform team] if schema change was unannounced
```

**4c. Out of memory / volume spike**
```
Symptom: job killed due to OOM, or runtime > [max runtime threshold]
Diagnose:
  SELECT COUNT(*) FROM [source_table] WHERE DATE(created_at) = CURRENT_DATE;
  Compare to normal range in Step 2.
Fix:
  - If volume is legitimately large: rerun with increased memory allocation
    [specific command or config change]
  - If volume is abnormal (data duplication upstream): do NOT load. Escalate.
```

**4d. Source query timeout**
```
Diagnose: check source query runtime vs. normal
Fix:
  1. Check if source DB has an active incident
  2. If query plan degraded: add EXPLAIN to identify missing index
  3. Short-term: increase job timeout in [config file]
  4. Long-term: file ticket to optimize source query or add index
```

### Step 5: Backfill procedure

When data needs to be reloaded for a historical date range:

```
When to backfill: source was late, schema changed mid-run, data quality failure detected

Backfill command:
[exact command with date range parameters]

Idempotency: [yes/no]
  If yes: safe to rerun, uses MERGE/UPSERT on [primary key]
  If no: must truncate target partition first:
    DELETE FROM [table] WHERE DATE(partition_date) BETWEEN [start] AND [end];

Backfill duration estimate: [N rows/minute, use to estimate runtime]

After backfill, verify:
  SELECT COUNT(*), MIN(created_at), MAX(created_at)
  FROM [target_table]
  WHERE DATE(created_at) BETWEEN [start] AND [end];
```

### Step 6: Escalation path

| Situation | Contact | Channel |
|-----------|---------|---------|
| Source system down > 30 min | [Source team on-call] | [PagerDuty / Slack] |
| Unannounced schema change | [Source team lead] | [channel] |
| Data quality failure affecting downstream reports | [Data platform lead] | [channel] |
| Cannot determine root cause within 30 min | [Senior DE on-call] | [PagerDuty] |

## Anti-Patterns

**1. Job success ≠ data success**
Bad: "If the job shows SUCCESS, we're done."
Good: Check row counts, null rates, and freshness even on successful runs. Silent data quality failures are more dangerous than job failures because they go undetected longer.

**2. No backfill procedure**
Bad: "Rerun the job."
Good: Specify whether reruns are idempotent, what to truncate if not, and the exact command with date range parameters.

**3. Diagnose without data context**
Bad: "Check the logs."
Good: Provide specific SQL queries to confirm whether data arrived, check for nulls, and detect duplicates.

**4. Escalate immediately**
Bad: On-call escalates after every failure without attempting diagnosis.
Good: Runbook gives the on-call engineer 30 minutes of self-service steps before escalation is appropriate.

## Quality Checklist

- [ ] Job overview includes schedule, SLA, expected runtime, and direct links
- [ ] "Healthy" state defined with row count ranges, null rates, and freshness thresholds
- [ ] Diagnosis flow covers job failure AND data quality failure (they are different)
- [ ] Top 4 failure modes documented with exact diagnostic steps and SQL queries
- [ ] Backfill procedure specifies idempotency, truncation if needed, and verification query
- [ ] Escalation path names specific people or teams and contact channels
- [ ] All commands and queries are copy-pasteable (no "run the relevant command")
