---
name: prometheus-query-patterns
description: "rate(http_requests_total[5m])"
---

# Prometheus Query Patterns (Verbose)

## Fundamental Operators

### rate() - Per-Second Rate
```promql
# HTTP requests per second (over 5-minute window)
rate(http_requests_total[5m])

# Only successful requests
rate(http_requests_total{status="200"}[5m])

# Error rate (errors per second)
rate(http_requests_total{status=~"5.."}[5m])
```

### histogram_quantile() - Percentiles
```promql
# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 99th percentile
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

### sum() - Aggregation
```promql
# Total requests across all services
sum(rate(http_requests_total[5m]))

# By service
sum by (service) (rate(http_requests_total[5m]))

# By service and method
sum by (service, method) (rate(http_requests_total[5m]))
```

## RED Method Implementation

**Rate:** requests per second
```promql
# Total RPS
sum(rate(http_requests_total[5m]))

# RPS by endpoint
sum by (path) (rate(http_requests_total[5m]))

# Alert if rate anomaly
rate(http_requests_total[5m]) > 10000  # >10K req/sec
```

**Errors:** Error rate percentage
```promql
# Error rate (0-1)
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m]))

# Alert if >1% error rate
(...) > 0.01
```

**Duration:** Latency percentiles
```promql
# P95, P99 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Alert if p95 > 500ms
(...) > 0.5
```

## Advanced Queries

**Availability (Uptime %):**
```promql
# Monthly availability
sum(rate(http_requests_total{status="200"}[30d])) /
sum(rate(http_requests_total[30d]))
* 100
```

**SLO Tracking:**
```promql
# Are we burning error budget?
(1 - availability_actual) / (1 - slo_target)
# >1 means we're burning budget faster than planned
```

**Comparing Services:**
```promql
# Latency across services
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[5m])
) by (service)
```

## Alert Examples

```yaml
groups:
  - name: api
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        annotations:
          summary: "Error rate > 1%"
      
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            rate(http_request_duration_seconds_bucket[5m])
          ) > 0.5
        for: 10m
        annotations:
          summary: "P95 latency > 500ms"
```

## Common Mistakes

❌ Using raw counter values (not per-second rate)  
✅ Always use rate() for counters

❌ Not specifying time window [5m], [1h], [1d]  
✅ Match window to alerting needs

❌ Over-aggregating, losing context  
✅ Keep dimensions (service, region, etc.)
