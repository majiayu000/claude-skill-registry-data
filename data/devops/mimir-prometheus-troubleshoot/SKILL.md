---
name: mimir-prometheus-troubleshoot
description: "Help craft efficient Mimir/Prometheus queries, troubleshoot metric issues, avoid high-cardinality problems, and recommend best practices for aggregation, recording rules, and performance."
---

# Mimir + Prometheus Troubleshooting & Query-Builder Skill

## What this Skill does

Use this skill whenever a user needs help with:

- PromQL queries
- Metric debugging
- Missing data / gaps
- Cardinality optimization
- Aggregation strategy
- Recording rules

## Best Practices

### Low-cardinality label selection

Use labels such as:

- `job`, `instance`, `service`, `cluster`, `namespace`, `env`

Avoid:

- `user_id`, `session_id`, `request_id`, raw UUIDs

### Always narrow time ranges

Prefer `"5m"`, `"15m"`, `"1h"`.

### Use correct aggregations

- `rate()` for counters
- `sum by (...)` for grouping
- `histogram_quantile()` for latency

### Suggest recording rules if query is heavy

## Example Queries

| User Request                       | PromQL                                                                                                        |
|------------------------------------|---------------------------------------------------------------------------------------------------------------|
| "Error rate for payments in prod"  | `sum by (job) (rate(http_requests_total{job="payments", env="prod", status=~"5.."}[5m]))`                  |
| "Latency p95 for frontend"         | `histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{app="frontend"}[5m])))` |

## When to Suggest Loki or Tempo

For:

- request IDs
- root-cause event-level debugging  
- full request paths  

→ Recommend Tempo + Loki correlations.

## Limitations

- Skill does not run PromQL  
