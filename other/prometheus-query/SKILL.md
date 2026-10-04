---
name: prometheus-query
description: Query Prometheus metrics and alerts
activation_keywords: [prometheus, metrics, alert, promql, monitoring, scrape]
execution_mode: server
---

# Prometheus Query Skill

Provides read-only Prometheus operations:
- Execute PromQL queries for instant/vector results
- List available metrics
- Query alert rules and their status
- Check Prometheus targets health

Use `builtin_prometheus_query` tool with fields:
- `operation`: one of "query", "query_range", "alerts", "targets", "metrics"
- `query`: PromQL expression (required for query operations)
- `prometheus_url`: Prometheus base URL only, for example `https://prometheus.example.com` (optional, uses default if not set). Do not pass `/api/v1/query` or other API paths here.
- `start`, `end`, `step`: (optional) time range parameters for range queries

Notes:
- Pass raw PromQL in `query`; the tool handles URL encoding.
- All operations are read-only.
