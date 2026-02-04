---
name: Prometheus Analysis
description: This skill should be used when the user asks to "query Prometheus", "analyze Prometheus metrics", "check Prometheus alerts", "write PromQL", "interpret Prometheus data", "fetch metrics", or mentions Prometheus querying, alerting, or metrics analysis. Provides guidance for querying and interpreting Prometheus metrics for root cause analysis.
version: 0.1.0
---

# Prometheus Analysis

## Overview

Prometheus is a time-series metrics collection and alerting system widely used for monitoring production systems. This skill provides guidance for querying Prometheus metrics, interpreting alert data, and using metrics for root cause analysis.

## When to Use This Skill

Apply this skill when:
- Analyzing Prometheus alerts that have fired
- Querying metrics to understand system behavior
- Investigating metric anomalies or spikes
- Correlating metrics with incidents
- Writing PromQL queries for specific metrics
- Interpreting time-series data patterns

## Prometheus Fundamentals

### Metric Types

**Counter**: Cumulative value that only increases (e.g., total requests, error count)
- Use `rate()` or `increase()` to get per-second rate or total increase
- Example: `http_requests_total`

**Gauge**: Value that can go up or down (e.g., CPU usage, memory usage, queue depth)
- Query directly or use functions like `avg_over_time()`
- Example: `node_memory_usage_bytes`

**Histogram**: Distribution of values in buckets (e.g., request durations)
- Provides `_sum`, `_count`, and `_bucket` metrics
- Use for percentile calculations
- Example: `http_request_duration_seconds`

**Summary**: Similar to histogram but with pre-calculated quantiles
- Example: `http_request_duration_seconds{quantile="0.95"}`

### Time Series Format

Metrics have format: `metric_name{label1="value1", label2="value2"}`

Example: `http_requests_total{method="POST", status="500", service="api"}`

## Querying Prometheus

### Basic Queries

**Instant query** (current value):
```promql
http_requests_total
```

**Range query** (over time):
```promql
http_requests_total[5m]
```

**Filter by labels**:
```promql
http_requests_total{status="500", service="api"}
```

**Rate of increase** (per-second rate):
```promql
rate(http_requests_total[5m])
```

### Common Aggregation Functions

**Sum** across dimensions:
```promql
sum(rate(http_requests_total[5m])) by (status)
```

**Average**:
```promql
avg(node_memory_usage_bytes) by (instance)
```

**Max/Min**:
```promql
max(http_request_duration_seconds) by (endpoint)
```

**Count**:
```promql
count(up == 0)  # Count instances that are down
```

### Useful RCA Queries

**Error rate percentage**:
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m])) * 100
```

**95th percentile latency**:
```promql
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket[5m])
)
```

**Request rate by endpoint**:
```promql
sum(rate(http_requests_total[5m])) by (endpoint)
```

**Memory usage percentage**:
```promql
(node_memory_usage_bytes / node_memory_total_bytes) * 100
```

**Database connection pool usage**:
```promql
sum(db_connection_pool_active) / sum(db_connection_pool_max) * 100
```

## Working with Alerts

### Alert Structure

Prometheus alerts contain:
- **Alert name**: Identifier for the alert rule
- **Labels**: Dimensions and metadata (service, severity, etc.)
- **Annotations**: Human-readable descriptions
- **State**: pending, firing, resolved
- **Active since**: When alert started firing
- **Value**: Current metric value that triggered alert

### Fetching Alert Details

Use Prometheus API to fetch alerts:

**List active alerts**:
```
GET /api/v1/alerts
```

**Query alert rule**:
```
GET /api/v1/rules
```

### Analyzing Alert Context

When investigating an alert:

1. **Check alert expression**: What PromQL query triggered the alert?
2. **Review threshold**: What value caused the alert to fire?
3. **Check alert duration**: How long has condition been true?
4. **Review labels**: What services/instances are affected?
5. **Query related metrics**: Get broader context around the alert

### Example Alert Investigation

Alert: `HighErrorRate`
Expression: `rate(http_requests_total{status=~"5.."}[5m]) > 0.05`

**Investigation queries**:

Query error rate breakdown:
```promql
rate(http_requests_total{status=~"5.."}[5m]) by (endpoint)
```

Query total request rate:
```promql
rate(http_requests_total[5m])
```

Query error rate percentage:
```promql
(sum(rate(http_requests_total{status=~"5.."}[5m])) /
 sum(rate(http_requests_total[5m]))) * 100
```

Check for correlated latency increase:
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

## Metrics Patterns for RCA

### Pattern 1: Sudden Spike

**Signature**: Metric jumps sharply at specific time

**Possible causes**:
- Code deployment
- Configuration change
- Traffic surge
- Dependency failure

**Investigation**:
- Correlate spike time with deployments
- Check for sudden traffic increase
- Query dependency health metrics
- Review recent configuration changes

### Pattern 2: Gradual Increase

**Signature**: Metric grows steadily over hours/days

**Possible causes**:
- Memory leak
- Resource exhaustion
- Unbounded data growth
- Missing cleanup job

**Investigation**:
- Check memory/disk usage trends
- Review data volume growth
- Query for resource leaks
- Check scheduled job execution

### Pattern 3: Periodic Pattern

**Signature**: Metric spikes at regular intervals

**Possible causes**:
- Scheduled job or cron
- Batch processing
- Cache expiration
- Garbage collection

**Investigation**:
- Identify period (hourly, daily, etc.)
- Check for scheduled tasks at that interval
- Review batch job schedules
- Query job execution metrics

### Pattern 4: Drop to Zero

**Signature**: Metric suddenly drops to zero or very low value

**Possible causes**:
- Service crash
- Instance termination
- Network partition
- Monitoring failure

**Investigation**:
- Check service health (`up` metric)
- Review instance count
- Query service availability
- Check for infrastructure changes

### Pattern 5: High Variability

**Signature**: Metric fluctuates wildly

**Possible causes**:
- Intermittent errors
- Race condition
- Resource contention
- Unhealthy load balancing

**Investigation**:
- Check error logs for patterns
- Review load distribution across instances
- Query resource utilization
- Check for concurrency issues

## Time Range Selection

Choose appropriate time ranges for investigation:

**Incident detection** (5-15 minutes):
```promql
rate(metric[5m])
```

**Trend analysis** (1-6 hours):
```promql
rate(metric[1h])
```

**Long-term patterns** (1-7 days):
```promql
avg_over_time(metric[1d])
```

**Comparison with past**:
```promql
# Current value
metric

# Value 1 week ago
metric offset 1w
```

## Correlating Metrics

### Multiple Metric Analysis

Query related metrics together to understand full context:

```promql
# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Request rate
rate(http_requests_total[5m])

# CPU usage
rate(process_cpu_seconds_total[5m])

# Memory usage
process_resident_memory_bytes
```

### Identifying Correlations

Look for metrics that change together:
- Error rate ↑ + Latency ↑ → Performance degradation
- Error rate ↑ + CPU ↑ → Resource exhaustion
- Error rate ↑ + Request rate ↑ → Traffic surge
- Error rate ↑ + Dependency metric ↓ → Dependency failure

## Best Practices

### Query Writing

- Use appropriate time ranges (5m for recent, 1h for trends)
- Filter by relevant labels to reduce cardinality
- Use `rate()` for counters, not raw values
- Aggregate when dealing with multiple instances
- Use recording rules for expensive queries

### Alert Investigation

- Start with alert expression to understand trigger
- Query wider time range to see pattern before/after
- Break down aggregated metrics to find specific instances/endpoints
- Check for correlated metric changes
- Compare current values with historical baseline

### Metric Interpretation

- Consider metric type (counter, gauge, histogram)
- Look for patterns over time, not just current values
- Compare across instances to find outliers
- Correlate with other metrics for complete picture
- Validate hypotheses with multiple metrics

## Integration with Thufir

This skill works with:
- **Prometheus MCP server**: Fetches alerts and queries metrics via API
- **root-cause-analysis skill**: Metrics provide evidence for RCA
- **RCA agent**: Agent queries Prometheus to gather metric data

### Using Prometheus MCP

The Thufir plugin includes Prometheus MCP server for querying:

**Query instant value**:
```
Use MCP tool: prometheus_query
Query: rate(http_requests_total[5m])
```

**Query time range**:
```
Use MCP tool: prometheus_query_range
Query: rate(http_requests_total[5m])
Start: 2025-12-19T14:00:00Z
End: 2025-12-19T15:00:00Z
Step: 15s
```

**Fetch active alerts**:
```
Use MCP tool: prometheus_alerts
```

## Additional Resources

### Reference Files

For detailed PromQL patterns and advanced queries:
- **`references/promql-cookbook.md`** - Common PromQL queries for RCA scenarios

## Quick Reference

**Error rate**: `rate(http_requests_total{status=~"5.."}[5m])`
**Latency p95**: `histogram_quantile(0.95, rate(duration_bucket[5m]))`
**CPU usage**: `rate(process_cpu_seconds_total[5m])`
**Memory**: `process_resident_memory_bytes`
**Request rate**: `rate(http_requests_total[5m])`

**Time ranges**: 5m (instant), 1h (trend), 1d (baseline)
**Aggregations**: `sum`, `avg`, `max`, `min`, `count`
**Filters**: `{label="value"}`, `{label=~"regex"}`

---

Use Prometheus metrics to provide objective, time-series evidence for root cause analysis. Correlate metrics with code changes and system events to identify precise incident causes.
