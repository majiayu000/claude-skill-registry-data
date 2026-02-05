---
name: tempo-troubleshoot
description: "Help craft efficient Tempo trace queries, troubleshoot distributed traces, link logs and metrics (Loki/Mimir), and perform request-level root cause analysis."
---

# Tempo Distributed Tracing Troubleshooting Skill

## What this Skill does

Use for:

- TraceQL queries
- Distributed tracing debugging
- Correlating traces with logs & metrics
- Investigating latency, errors, bottlenecks

## Best Practices

### Always start with service + time range

Examples:

- `resource.service.name = "payments"`
- `span.status = "error"`
- `span.duration > 500ms"`

### Avoid high-cardinality attributes

UUIDs, user IDs → only secondary filters.

### Use TraceQL for structure

Preferring simple comparisons & attribute filters.

### Link with Loki / Mimir when relevant

- Loki: `|= "<trace_id>"`
- Prometheus: find metrics for same window

## Example Queries

### Slow frontend traces

```traceql
{ resource.service.name = "frontend" } | span.duration > 1s
```

### Payment errors

```traceql
{ resource.service.name = "payments", span.status = "error", start >= now() - 15m }
```

## Limitations

- Skill does not execute TraceQL  
