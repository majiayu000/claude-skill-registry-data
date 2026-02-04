---
name: monitoring-skill
description: Monitoring and observability with Prometheus, Grafana, ELK Stack, and distributed tracing.
sasmp_version: "1.3.0"
bonded_agent: 06-monitoring-observability
bond_type: PRIMARY_BOND

parameters:
  - name: pillar
    type: string
    required: false
    enum: ["metrics", "logs", "traces", "all"]
    default: "all"
  - name: tool
    type: string
    required: false
    enum: ["prometheus", "grafana", "elk", "jaeger"]
    default: "prometheus"

retry_config:
  strategy: exponential_backoff
  initial_delay_ms: 1000
  max_retries: 3

observability:
  logging: structured
  metrics: enabled
---

# Monitoring & Observability Skill

## Overview
Master the three pillars of observability: metrics, logs, and traces.

## Parameters
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pillar | string | No | all | Observability pillar |
| tool | string | No | prometheus | Tool focus |

## Core Topics

### MANDATORY
- Prometheus metrics and PromQL
- Grafana dashboards
- ELK Stack basics
- SLIs, SLOs, error budgets
- Alerting rules

### OPTIONAL
- Distributed tracing
- OpenTelemetry
- Custom exporters
- Log correlation

### ADVANCED
- High cardinality handling
- Recording rules
- Federation
- Continuous profiling

## Quick Reference

```bash
# PromQL
sum(rate(http_requests_total[5m])) by (service)
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
100 * sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Prometheus API
curl http://localhost:9090/api/v1/targets
curl 'http://localhost:9090/api/v1/query?query=up'
curl -X POST http://localhost:9090/-/reload

# Alertmanager
amtool silence add alertname="HighLatency" --duration=2h
amtool alert
```

## SRE Golden Signals
| Signal | Metric |
|--------|--------|
| Latency | `histogram_quantile(0.99, ...)` |
| Traffic | `sum(rate(requests_total[5m]))` |
| Errors | `rate(errors_total[5m])` |
| Saturation | `node_memory_MemAvailable_bytes` |

## Troubleshooting

### Common Failures
| Symptom | Root Cause | Solution |
|---------|------------|----------|
| No data | Scrape failing | Check targets page |
| Alert not firing | PromQL error | Test in UI |
| High cardinality | Too many labels | Reduce labels |
| Slow queries | Too much data | Add aggregation |

### Debug Checklist
1. Check targets: `/targets`
2. Test query in UI
3. Check logs: `journalctl -u prometheus`
4. Verify time sync (NTP)

### Recovery Procedures

#### Prometheus OOM
1. Check cardinality
2. Reduce retention
3. Add federation

## Resources
- [Prometheus Docs](https://prometheus.io/docs)
- [Grafana Docs](https://grafana.com/docs)
