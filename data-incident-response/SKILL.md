---
name: Data Incident Response
description: Procedures and playbooks for responding to data quality incidents, data loss, corruption, and pipeline failures.
---

# Data Incident Response

## Overview

Data Incident Response is the process of detecting, triaging, and resolving issues related to data quality, availability, or integrity. Unlike application incidents, data incidents can have long-lasting impacts on analytics, ML models, and business decisions.

**Core Principle**: "Bad data is worse than no data. Detect fast, respond faster, prevent recurrence."

---

## 1. Types of Data Incidents

| Type | Description | Example | Severity |
|------|-------------|---------|----------|
| **Data Loss** | Data deleted or not captured | Accidental DROP TABLE | P0 |
| **Data Corruption** | Data modified incorrectly | ETL bug multiplies prices by 100 | P0-P1 |
| **Data Breach** | Unauthorized data access | PII exposed in logs | P0 |
| **Pipeline Failure** | ETL/ELT pipeline stops | Airflow DAG fails | P1-P2 |
| **Schema Breaking Change** | Upstream schema change breaks pipeline | Column renamed without notice | P1 |
| **Data Quality Degradation** | Increasing nulls, duplicates, anomalies | 20% of orders have null customer_id | P2 |
| **Freshness Violation** | Data not updated within SLA | Dashboard showing yesterday's data | P2-P3 |

---

## 2. Data Incident Severity Levels

### P0 (Critical)
- **Definition**: Data breach, major data loss, or corruption affecting production decisions
- **Examples**:
  - PII exposed publicly
  - Financial data deleted
  - ML model making wrong predictions due to corrupt training data
- **Response Time**: Immediate (< 15 minutes)
- **Notification**: Page on-call + executives
- **Postmortem**: Required within 48 hours

### P1 (High)
- **Definition**: Pipeline down, critical data corrupt, major quality degradation
- **Examples**:
  - Daily ETL failed, no fresh data
  - Revenue reporting showing incorrect numbers
  - Customer-facing dashboard broken
- **Response Time**: < 1 hour
- **Notification**: Page on-call data team
- **Postmortem**: Required within 1 week

### P2 (Medium)
- **Definition**: Data quality issue affecting internal reports
- **Examples**:
  - 10% of records have validation errors
  - Non-critical dashboard stale
  - Schema drift detected but not breaking
- **Response Time**: < 4 hours
- **Notification**: Slack alert to data team
- **Postmortem**: Optional

### P3 (Low)
- **Definition**: Minor data inconsistency, no immediate impact
- **Examples**:
  - Duplicate records in non-critical table
  - Formatting inconsistency
  - Deprecated field still populated
- **Response Time**: < 1 business day
- **Notification**: Ticket created
- **Postmortem**: Not required

---

## 3. Incident Detection

### Automated Detection
```python
# Data quality monitoring
def monitor_data_quality():
    """Continuously monitor data quality metrics"""
    
    checks = {
        'null_rate': check_null_rate('orders', 'customer_id', threshold=0.05),
        'duplicate_rate': check_duplicates('orders', 'order_id', threshold=0.01),
        'freshness': check_freshness('orders', 'created_at', max_age_minutes=60),
        'row_count': check_row_count_anomaly('orders', expected_range=(1000, 10000))
    }
    
    for check_name, result in checks.items():
        if not result['passed']:
            trigger_incident(
                severity=result['severity'],
                title=f"Data quality check failed: {check_name}",
                details=result
            )
```

### Pipeline Failure Alerts
```python
# Airflow callback
from airflow.operators.python import PythonOperator

def on_failure_callback(context):
    """Trigger incident on DAG failure"""
    trigger_incident(
        severity='P1',
        title=f"Pipeline failed: {context['dag'].dag_id}",
        details={
            'task': context['task'].task_id,
            'execution_date': context['execution_date'],
            'error': str(context['exception'])
        }
    )

task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    on_failure_callback=on_failure_callback
)
```

### User Reports
```
User report channels:
- Support tickets
- Slack #data-issues channel
- Email to data-team@company.com
- Dashboard "Report Issue" button
```

---

## 4. Incident Triage

### Initial Assessment Questions
1. **What data is affected?** (table, time range, row count)
2. **Who is impacted?** (internal teams, customers, ML models)
3. **When did it start?** (timestamp, duration)
4. **Is it still happening?** (ongoing vs. resolved)
5. **What's the business impact?** (revenue, compliance, reputation)

### Triage Decision Tree
```
Is data breach or PII exposed?
  YES → P0, page security team immediately
  NO → Continue

Is production decision-making affected?
  YES → P0/P1, page data team
  NO → Continue

Is critical pipeline down?
  YES → P1, page data team
  NO → Continue

Is data quality degraded?
  YES → P2, alert data team
  NO → P3, create ticket
```

---

## 5. Response Procedures

### Step 1: Stop the Bleeding
```python
def stop_the_bleeding(incident_type: str):
    """Immediate actions to prevent further damage"""
    
    if incident_type == 'pipeline_failure':
        # Pause downstream pipelines
        pause_dependent_dags()
        
    elif incident_type == 'data_corruption':
        # Stop writes to affected table
        revoke_write_permissions('corrupted_table')
        
    elif incident_type == 'data_breach':
        # Immediately restrict access
        revoke_all_access('sensitive_table')
        notify_security_team()
```

### Step 2: Assess Damage
```sql
-- Assess extent of data corruption
SELECT 
    COUNT(*) as total_rows,
    COUNT(*) FILTER (WHERE price < 0) as corrupt_rows,
    MIN(created_at) as first_corrupt_timestamp,
    MAX(created_at) as last_corrupt_timestamp
FROM orders
WHERE created_at > '2024-01-15 10:00:00';
```

### Step 3: Restore from Backup (if needed)
```bash
# PostgreSQL point-in-time recovery
pg_restore \
  --dbname=production \
  --table=orders \
  --data-only \
  --clean \
  backup_before_corruption.dump

# Verify restoration
psql -c "SELECT COUNT(*) FROM orders WHERE created_at > '2024-01-15 09:00:00';"
```

### Step 4: Fix Root Cause
```python
# Example: Fix ETL bug that caused corruption
def fixed_transform(df):
    """Corrected transformation logic"""
    # OLD (buggy): df['price'] = df['price'] * 100
    # NEW (fixed): df['price'] = df['price']  # Already in cents
    return df

# Reprocess affected data
reprocess_date_range(
    start_date='2024-01-15',
    end_date='2024-01-16',
    transform_fn=fixed_transform
)
```

### Step 5: Validate Fix
```python
def validate_fix():
    """Verify data is correct after fix"""
    
    # Check row counts match
    assert get_row_count('orders') == expected_count
    
    # Check no corrupt data remains
    corrupt_count = db.execute("""
        SELECT COUNT(*) FROM orders WHERE price < 0
    """).fetchone()[0]
    assert corrupt_count == 0
    
    # Check data quality metrics
    quality_score = run_data_quality_checks('orders')
    assert quality_score > 95
```

### Step 6: Resume Operations
```python
def resume_operations():
    """Resume normal operations"""
    
    # Restore write permissions
    grant_write_permissions('orders')
    
    # Resume downstream pipelines
    resume_dependent_dags()
    
    # Monitor closely for 24 hours
    enable_enhanced_monitoring('orders', duration_hours=24)
```

---

## 6. Data Recovery Strategies

### Point-in-Time Recovery (PITR)
```sql
-- PostgreSQL: Restore to specific timestamp
SELECT pg_restore_point('before_corruption');

-- Restore database to point before corruption
pg_basebackup --pgdata=/var/lib/postgresql/restore \
  --target-time='2024-01-15 09:55:00'
```

### Replay from Source
```python
def replay_from_kafka(topic: str, start_offset: int, end_offset: int):
    """Replay events from Kafka to rebuild state"""
    
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest'
    )
    
    # Seek to start offset
    partition = TopicPartition(topic, 0)
    consumer.assign([partition])
    consumer.seek(partition, start_offset)
    
    for message in consumer:
        if message.offset > end_offset:
            break
        
        # Reprocess event
        process_event(message.value)
```

### Manual Correction
```sql
-- Identify and fix corrupt records
UPDATE orders
SET price = price / 100  -- Undo the bug that multiplied by 100
WHERE created_at BETWEEN '2024-01-15 10:00:00' AND '2024-01-15 12:00:00'
  AND price > 1000000;  -- Only fix obviously wrong prices
```

### Reprocessing Pipelines
```python
# Airflow: Backfill specific date range
airflow dags backfill \
  --start-date 2024-01-15 \
  --end-date 2024-01-16 \
  --reset-dagruns \
  daily_etl_dag
```

---

## 7. Communication During Data Incidents

### Internal Communication Template
```markdown
🚨 **DATA INCIDENT** - P1

**Affected Data**: orders table
**Impact**: Revenue dashboard showing incorrect numbers
**Started**: 2024-01-15 10:13 UTC
**Status**: Investigating

**What we know**:
- ETL bug multiplied all prices by 100
- Affects orders from 10:00-12:00 UTC (2 hours)
- ~5,000 orders impacted

**What we're doing**:
- Stopped downstream pipelines
- Restoring from backup
- Fixing ETL bug

**Next update**: 30 minutes

**Incident Commander**: @alice
**War Room**: #incident-data-001
```

### Stakeholder Notification
```python
def notify_stakeholders(incident):
    """Notify affected teams"""
    
    affected_teams = identify_affected_teams(incident['table'])
    
    for team in affected_teams:
        send_notification(
            channel=team['slack_channel'],
            message=f"""
            ⚠️ Data incident affecting {incident['table']}
            
            Impact: {incident['impact']}
            ETA for resolution: {incident['eta']}
            
            Please avoid using this data until resolved.
            Updates in #incident-{incident['id']}
            """
        )
```

---

## 8. Common Data Incident Scenarios

### Scenario 1: Accidental DELETE
```sql
-- Incident: Developer ran DELETE without WHERE clause
DELETE FROM users;  -- ❌ Deleted all users!

-- Response:
-- 1. Immediately stop application writes
-- 2. Restore from most recent backup
-- 3. Replay transactions from WAL (Write-Ahead Log)
-- 4. Implement safeguards (require WHERE clause, read-only by default)
```

### Scenario 2: Bad Data from Upstream
```python
# Incident: Upstream API started sending null customer_ids

# Detection
if df['customer_id'].isna().sum() > len(df) * 0.01:  # > 1% nulls
    raise DataQualityError("Too many null customer_ids")

# Response
# 1. Reject the batch
# 2. Alert upstream team
# 3. Use previous day's data as fallback
# 4. Implement validation before ingestion
```

### Scenario 3: Pipeline Bug Corrupting Data
```python
# Incident: ETL bug converted all timestamps to UTC incorrectly

# Detection
anomaly_count = db.execute("""
    SELECT COUNT(*) FROM events
    WHERE event_time > NOW()  -- Future timestamps = bug
""").fetchone()[0]

# Response
# 1. Identify affected date range
# 2. Pause pipeline
# 3. Fix transformation logic
# 4. Reprocess affected dates
# 5. Add validation for timestamp sanity
```

### Scenario 4: Schema Change Breaking Pipeline
```python
# Incident: Upstream renamed 'user_id' to 'customer_id'

# Detection
try:
    df = spark.read.parquet("s3://data/users/")
    df.select("user_id")  # KeyError
except KeyError:
    trigger_incident("Schema drift detected")

# Response
# 1. Update pipeline to handle both column names
# 2. Coordinate with upstream for future changes
# 3. Implement schema validation before processing
```

---

## 9. Prevention Strategies

### Immutable Data Lakes
```python
# Never modify data in place; always append new versions
# S3 versioning enabled
s3.put_bucket_versioning(
    Bucket='data-lake',
    VersioningConfiguration={'Status': 'Enabled'}
)

# Write new partition instead of overwriting
df.write.partitionBy('date').mode('append').parquet('s3://data-lake/orders/')
```

### Strong Data Validation
```python
# Validate before loading
@validate_schema(expected_schema)
@validate_quality(min_quality_score=95)
def load_to_warehouse(df):
    df.write.jdbc(url, table, mode='append')
```

### Backup and Restore Testing
```bash
# Monthly backup restore drill
# 1. Restore backup to test environment
pg_restore --dbname=test_db production_backup.dump

# 2. Verify data integrity
python verify_data_integrity.py --db test_db

# 3. Measure restore time
# 4. Document any issues
```

### Schema Change Management
```yaml
# Data contract with upstream
contract:
  table: users
  schema_changes_require:
    - 2 weeks notice
    - Backward compatibility
    - Coordination meeting
  breaking_changes_forbidden:
    - Column removal
    - Column rename
    - Type change
```

---

## 10. Data Incident Playbooks

### Playbook: Data Loss
```markdown
## Data Loss Incident Response

### Immediate Actions (0-15 min)
- [ ] Confirm scope of data loss (tables, time range, row count)
- [ ] Stop any processes that might overwrite backups
- [ ] Page on-call data engineer + DBA
- [ ] Create war room (#incident-XXX)

### Assessment (15-30 min)
- [ ] Identify last known good backup
- [ ] Estimate recovery time
- [ ] Identify affected downstream systems
- [ ] Notify stakeholders

### Recovery (30 min - X hours)
- [ ] Restore from backup to staging environment
- [ ] Validate restored data
- [ ] Restore to production
- [ ] Verify row counts and data quality
- [ ] Resume dependent pipelines

### Prevention
- [ ] Implement soft deletes
- [ ] Add confirmation prompts for destructive operations
- [ ] Enable database audit logging
- [ ] Schedule backup restore drills
```

### Playbook: Data Corruption
```markdown
## Data Corruption Incident Response

### Immediate Actions
- [ ] Identify extent of corruption (affected rows, columns, time range)
- [ ] Pause downstream pipelines to prevent propagation
- [ ] Quarantine corrupt data

### Root Cause Analysis
- [ ] Review recent code changes
- [ ] Check for upstream data issues
- [ ] Examine pipeline logs for errors

### Remediation
- [ ] Fix root cause (code bug, config error)
- [ ] Choose recovery method:
  - [ ] Restore from backup
  - [ ] Replay from source
  - [ ] Manual correction
  - [ ] Reprocess pipeline
- [ ] Validate fix with data quality checks

### Prevention
- [ ] Add data quality checks before and after transformation
- [ ] Implement idempotency in pipelines
- [ ] Add integration tests for edge cases
```

---

## 11. Incident Response Checklist

- [ ] **Detection**: Do we have automated monitoring for data quality?
- [ ] **Alerting**: Are alerts routed to the right people?
- [ ] **Runbooks**: Do we have playbooks for common scenarios?
- [ ] **Backups**: Are backups tested and restore time known?
- [ ] **Communication**: Do we have templates for stakeholder updates?
- [ ] **War Room**: Is there a dedicated channel for incidents?
- [ ] **Postmortem**: Do we conduct blameless postmortems?
- [ ] **Prevention**: Are action items from postmortems tracked?

---

## Related Skills
- `41-incident-management/incident-triage`
- `41-incident-management/incident-retrospective`
- `43-data-reliability/data-quality-checks`
- `43-data-reliability/schema-drift`
- `40-system-resilience/disaster-recovery`
