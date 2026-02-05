---
name: observability-standards
description: Prometheus metrics and observability standards. Use when writing, generating, or reviewing code with metrics or instrumentation.
---

# Observability Standards

## Prometheus Naming Conventions

Format: `namespace_subsystem_name_unit`

| Suffix | Meaning | Example |
|--------|---------|---------|
| `_total` | Counter (cumulative) | `http_requests_total` |
| `_seconds` | Duration | `http_request_duration_seconds` |
| `_bytes` | Size | `response_size_bytes` |
| `_info` | Metadata gauge (always 1) | `build_info` |

## Metric Types

| Type | Use For | Example |
|------|---------|---------|
| **Counter** | Cumulative totals (only increases) | Requests, errors, events |
| **Gauge** | Current value (can go up/down) | Queue depth, active connections |
| **Histogram** | Distribution of values | Latency, response sizes |
| **Summary** | Quantiles (prefer histogram) | Legacy latency metrics |

## Instrumentation by Operation Type

| Operation | Metrics to Add |
|-----------|---------------|
| **API endpoint** | `http_requests_total{method,path,status}`, `http_request_duration_seconds` |
| **Database query** | `db_queries_total{operation,table}`, `db_query_duration_seconds` |
| **Background job** | `jobs_processed_total{type,status}`, `jobs_in_queue` (gauge) |
| **External API** | `external_api_requests_total{service,status}`, `external_api_duration_seconds` |
| **Cache** | `cache_hits_total`, `cache_misses_total` |
| **Business event** | `orders_created_total`, `graduations_completed_total` |

## Labels

Use labels for dimensions that are:
- Low cardinality (bounded set of values)
- Useful for aggregation/filtering

```go
// Good - bounded cardinality
httpRequests.WithLabelValues(method, statusCode, handler).Inc()

// Bad - unbounded cardinality (user IDs, timestamps)
httpRequests.WithLabelValues(userID).Inc()  // Creates millions of series
```

## Standard Labels

| Label | Values | Use |
|-------|--------|-----|
| `method` | GET, POST, PUT, DELETE | HTTP method |
| `status` | 2xx, 4xx, 5xx or exact codes | Response status |
| `operation` | create, read, update, delete | CRUD operation |
| `success` | true, false | Operation outcome |

## What to Instrument

### Always Instrument
- Request/operation counters (total, success, failure)
- Latency for user-facing operations
- Error rates by type
- Queue depths and processing times

### Consider Instrumenting
- Cache hit/miss rates
- Connection pool utilization
- Retry counts
- Business metrics (orders, graduations, deposits)

## Tracing Context

For multi-service operations:
- Propagate `trace_id` and `span_id` through headers
- Include correlation IDs in logs
- Use OpenTelemetry for distributed tracing

## Alerting Considerations

When adding metrics, consider:
- Can failures trigger alerts?
- What are the SLI/SLO implications?
- What thresholds indicate problems?

## Review Checklist

- [ ] Critical paths have latency histograms
- [ ] Operations have success/failure counters
- [ ] Metric names follow `namespace_subsystem_name_unit` convention
- [ ] Labels are low cardinality
- [ ] Business events are tracked
- [ ] Error types are distinguishable via labels
- [ ] Gauges used for current-state values
