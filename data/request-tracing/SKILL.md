---
name: request-tracing
description: "Instrument HTTP/gRPC endpoints with distributed tracing and RED metrics"
triggers:
  - "trace HTTP requests"
  - "instrument endpoints"
  - "distributed tracing"
  - "trace context propagation"
  - "gRPC tracing"
priority: 1
---

# Request Tracing

Every request needs: a span, RED metrics, and trace context propagation.

## Required Attributes

| Attribute | Example | Note |
|-----------|---------|------|
| `http.method` | GET, POST | Required |
| `http.route` | /api/orders/:id | **Template, not actual path!** |
| `http.status_code` | 200, 500 | Required |
| `user.tier` | premium | Recommended (not user_id!) |

## RED Metrics

```
Rate:     http.requests.count{method, route, status}
Errors:   http.requests.errors{method, route, error_type}
Duration: http.request.duration{method, route} (histogram p50/p95/p99)
```

## Middleware Flow

```
Request → Extract trace context (W3C traceparent)
        → Start span (method + route)
        → Start timer
        → Call handler
        → Set status_code
        → Record duration histogram
        → If 4xx/5xx: increment error counter
        → End span
        → Inject trace context into response
```

## Context Propagation

**Critical:** Always propagate to downstream services:
```
// Outgoing request
propagator.inject(ctx, headers)
```

## Common Mistakes

1. **Using actual path** → `/api/orders/12345` creates millions of unique values
2. **Missing propagation** → Traces break at service boundaries
3. **Only tracking success** → Must track errors with `error_type`

## References

- `references/methodology/red-methodology.md`
- `references/platforms/{platform}/http.md`
