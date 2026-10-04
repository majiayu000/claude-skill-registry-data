---
name: aws-rds-deep
description: |
  Use when working with Aws Rds Deep — aWS RDS deep analysis covering
  Performance Insights, event subscriptions, proxy management, and global
  database status. Covers PI counter metrics, wait event analysis, top SQL
  queries, read replica lag, storage autoscaling, and Aurora-specific
  diagnostics.
connection_type: aws
preload: false
---

# AWS RDS Deep Skill

Deep analysis of AWS RDS instances with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-rds-deep/` → RDS deep-dive analysis (Performance Insights, proxies, global DBs)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)
- `aws-rightsizing/` → RDS rightsizing recommendations

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for db in $databases; do
  get_db_performance "$db" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List RDS instances with Performance Insights status
list_rds_instances() {
  aws rds describe-db-instances \
    --output text \
    --query 'DBInstances[].[DBInstanceIdentifier,Engine,EngineVersion,DBInstanceClass,DBInstanceStatus,PerformanceInsightsEnabled,MultiAZ,StorageType,AllocatedStorage]'
}

# Get Performance Insights resource metrics
get_pi_metrics() {
  local resource_arn=$1 hours=${2:-1}
  local end_time start_time
  end_time=$(date +%s)
  start_time=$((end_time - hours * 3600))
  aws pi get-resource-metrics \
    --service-type RDS \
    --identifier "$resource_arn" \
    --metric-queries '[{"Metric":"db.load.avg"}]' \
    --start-time "$start_time" --end-time "$end_time" \
    --period-in-seconds 300 \
    --output text \
    --query 'MetricList[0].DataPoints[*].[Timestamp,Value]' | tail -10
}

# Get top wait events from PI
get_pi_wait_events() {
  local resource_arn=$1 hours=${2:-1}
  local end_time start_time
  end_time=$(date +%s)
  start_time=$((end_time - hours * 3600))
  aws pi get-resource-metrics \
    --service-type RDS \
    --identifier "$resource_arn" \
    --metric-queries '[{"Metric":"db.load.avg","GroupBy":{"Group":"db.wait_event","Limit":10}}]' \
    --start-time "$start_time" --end-time "$end_time" \
    --period-in-seconds $((hours * 3600)) \
    --output text \
    --query 'MetricList[0].DataPoints[0].Value'
}

# List RDS event subscriptions
list_event_subscriptions() {
  aws rds describe-event-subscriptions \
    --output text \
    --query 'EventSubscriptionsList[].[CustSubscriptionId,Status,SnsTopicArn,SourceType,Enabled]'
}

# List RDS proxies
list_proxies() {
  aws rds describe-db-proxies \
    --output text \
    --query 'DBProxies[].[DBProxyName,Status,EngineFamily,VpcId,IdleClientTimeout,RequireTLS]' 2>/dev/null
}

# Get read replica lag
get_replica_lag() {
  local instance_id=$1
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1H +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS --metric-name ReplicaLag \
    --dimensions Name=DBInstanceIdentifier,Value="$instance_id" \
    --start-time "$start_time" --end-time "$end_time" \
    --period 300 --statistics Average Maximum \
    --output text --query 'Datapoints[*].[Timestamp,Average,Maximum]' | sort -k1 | tail -5
}
```

## Common Operations

### 1. Instance Inventory with PI Status

```bash
#!/bin/bash
export AWS_PAGER=""
aws rds describe-db-instances \
  --output text \
  --query 'DBInstances[].[DBInstanceIdentifier,Engine,DBInstanceClass,DBInstanceStatus,PerformanceInsightsEnabled,MultiAZ,ReadReplicaDBInstanceIdentifiers[0]]' | sort -k2
```

### 2. Performance Insights DB Load Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
PI_INSTANCES=$(aws rds describe-db-instances \
  --output text \
  --query 'DBInstances[?PerformanceInsightsEnabled==`true`].[DbiResourceId,DBInstanceIdentifier]')
END=$(date +%s)
START=$((END - 3600))
echo "$PI_INSTANCES" | while read resource_id db_name; do
  {
    load=$(aws pi get-resource-metrics \
      --service-type RDS --identifier "db-$resource_id" \
      --metric-queries '[{"Metric":"db.load.avg"}]' \
      --start-time "$START" --end-time "$END" \
      --period-in-seconds 3600 \
      --output text \
      --query 'MetricList[0].DataPoints[0].Value')
    printf "%s\tDBLoad:%s\n" "$db_name" "${load:-N/A}"
  } &
done
wait
```

### 3. Read Replica Lag Monitoring

```bash
#!/bin/bash
export AWS_PAGER=""
REPLICAS=$(aws rds describe-db-instances \
  --output text \
  --query 'DBInstances[?ReadReplicaSourceDBInstanceIdentifier!=null].DBInstanceIdentifier')
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1H +"%Y-%m-%dT%H:%M:%S")
for replica in $REPLICAS; do
  aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS --metric-name ReplicaLag \
    --dimensions Name=DBInstanceIdentifier,Value="$replica" \
    --start-time "$START" --end-time "$END" \
    --period 300 --statistics Average Maximum \
    --output text --query "Datapoints[-1].[\"$replica\",Average,Maximum]" &
done
wait
```

### 4. RDS Proxy Health

```bash
#!/bin/bash
export AWS_PAGER=""
PROXIES=$(aws rds describe-db-proxies --output text --query 'DBProxies[].DBProxyName' 2>/dev/null)
for proxy in $PROXIES; do
  {
    info=$(aws rds describe-db-proxies --db-proxy-name "$proxy" \
      --output text --query 'DBProxies[].[DBProxyName,Status,EngineFamily,IdleClientTimeout,RequireTLS]')
    targets=$(aws rds describe-db-proxy-targets --db-proxy-name "$proxy" \
      --output text --query 'Targets[].[RdsResourceId,TargetHealth.State,TargetHealth.Description,Type]' 2>/dev/null)
    printf "%s\nTargets:\n%s\n" "$info" "$targets"
  } &
done
wait
```

### 5. Event Subscription and Recent Events

```bash
#!/bin/bash
export AWS_PAGER=""
aws rds describe-event-subscriptions \
  --output text \
  --query 'EventSubscriptionsList[].[CustSubscriptionId,Status,SourceType,Enabled]' &

aws rds describe-events --duration 1440 \
  --output text \
  --query 'Events[].[Date,SourceIdentifier,SourceType,Message]' | tail -20 &
wait
```

## Anti-Hallucination Rules

1. **Performance Insights identifier format** - PI uses DbiResourceId (e.g., `db-ABCDEFGHIJKLMN`), NOT DBInstanceIdentifier. Get it from `describe-db-instances`.
2. **PI must be enabled** - Performance Insights is not enabled by default on all instance types. Check `PerformanceInsightsEnabled` before querying PI APIs.
3. **ReplicaLag units vary by engine** - MySQL/MariaDB ReplicaLag is in seconds. Aurora replica lag is in milliseconds. PostgreSQL uses different replication metrics.
4. **Storage autoscaling** - `MaxAllocatedStorage` being set does not mean autoscaling is active. Check if `MaxAllocatedStorage > AllocatedStorage`.
5. **Aurora vs RDS** - Aurora instances appear in `describe-db-instances` but are managed differently. Aurora uses clusters (describe-db-clusters), reader/writer endpoints, and shared storage.

## Output Format

Present results as a structured report:
```
Aws Rds Deep Report
═══════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **PI data retention**: Free tier retains PI data for 7 days. Paid tier (long-term retention) stores up to 2 years.
- **Global databases**: Aurora global databases span regions. The primary cluster is read-write; secondary clusters are read-only. Use `describe-global-clusters`.
- **RDS Proxy connection limits**: Proxy manages connection pooling but has its own limits. Check `MaxConnectionsPercent` and `MaxIdleConnectionsPercent`.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Multi-AZ failover**: During failover, the CNAME endpoint switches to the standby. This causes a brief outage (usually 60-120 seconds).
