---
name: grafana-dashboard-design
description: "**Level 1: Executive Dashboard**"
---

# Grafana Dashboard Design (Verbose)

## Dashboard Hierarchy

**Level 1: Executive Dashboard**
- Single status (green/red)
- Key business metrics (users, revenue, SLO %)
- No drilling down

**Level 2: Service Overview**
- Health at a glance (status, uptime)
- RED metrics (rate, errors, duration)
- Resource usage (CPU, memory)

**Level 3: Deep Dive**
- Detailed metrics by component
- Error logs and patterns
- Time-series breakdown

## Panel Selection

```
├─ Status/Gauge (single number)
│  └─ "Availability: 99.95%"
│  └─ "Requests/sec: 1,234"
│
├─ Time-series (trend over time)
│  └─ Request rate (5 min graph)
│  └─ Latency (p95 over 1 hour)
│
├─ Heatmap (distribution)
│  └─ Latency distribution (0ms-5s)
│  └─ Error rate by percentile
│
├─ Table (list data)
│  └─ Top 10 errors
│  └─ Slowest endpoints
│
└─ Logs (debugging)
   └─ ERROR level logs
   └─ Exception traces
```

## Annotation & Alerting

```yaml
# Annotate deploys
- time: 2026-04-10T14:30:00Z
  text: "Deployed v1.2.3"
  tags: ["deployment"]

# Show alert thresholds
- threshold: 0.01  # 1% error rate
  fill: red
  line: solid
```

## Dashboard Template

```
┌─────────────────────────────────────────────────┐
│ API Service Dashboard                           │
│ [Time Range: Last 24h] [Refresh: 30s] [Fullscreen]
├─────────────────────────────────────────────────┤
│
│ Status: ✓ HEALTHY   Uptime: 99.95%  Since: 3d
│
├──────────────────┬──────────────────────────────┤
│ Requests/sec: 1,234      │ Latency p95: 145ms │
│ Error rate: 0.08%        │ CPU: 65%           │
├──────────────────┴──────────────────────────────┤
│
│ [Request Rate Graph]     [Error Rate Graph]    │
│ [Latency Graph]          [CPU Usage Graph]     │
│
├──────────────────────────────────────────────────┤
│ Top Errors           │ Top Slow Endpoints      │
│ [ERROR TABLE]        │ [LATENCY TABLE]         │
│
└──────────────────────────────────────────────────┘
```

## Best Practices

✅ **DO:**
- Use consistent colors (green=good, red=bad)
- Include units in axis labels (ms, %, req/sec)
- Add thresholds/alert bands
- Keep related panels together
- Show time range
- Auto-refresh (30s-5m)

❌ **DON'T:**
- Too many panels (>12 causes cognitive overload)
- Low-level metrics (use aggregates)
- Without context (what's "normal"?)
- Without titles (what am I looking at?)
- Hardcoded values (use variables)

## Advanced: Templated Dashboards

```yaml
# Parameterize for reuse
variables:
  - name: service
    type: query
    datasource: Prometheus
    query: 'label_values(http_requests_total, job)'
  
  - name: region
    type: query
    query: 'label_values(http_requests_total, region)'

# Use in panels
expr: 'rate(http_requests_total{job="$service", region="$region"}[5m])'
```

This creates reusable dashboards for different services/regions.
