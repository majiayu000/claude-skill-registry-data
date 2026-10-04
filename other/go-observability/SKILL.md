---
name: go-observability
description: "Golang observability patterns — logs, metrics, and traces. Covers structured logging (slog), Prometheus metrics, and OpenTelemetry tracing."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:05:00 GMT
---

## The Three Pillars

1. **Logs**: What happened? Use structured logging with `log/slog`.
2. **Metrics**: How much/how fast? Use Prometheus client for aggregated measurements.
3. **Traces**: Where did time go? Use OpenTelemetry (OTel) for distributed tracing.

## Best Practices

1. **Structured Logging (JSON)** — Production services MUST emit structured logs (JSON), not freeform strings.
2. **Log with Context** — Use `slog.InfoContext(ctx, ...)` to correlate logs with traces.
3. **Histogram over Summary** — For latency metrics, prefer Histograms as they support server-side aggregation.
4. **Low Cardinality Labels** — NEVER use unbounded values (user IDs, full URLs) as Prometheus label values.
5. **Propagate Context** — Context is the vehicle that carries `trace_id` and `span_id` across service boundaries.
6. **Golden Signals** — Always monitor Latency, Traffic, Errors, and Saturation.
7. **Single Handling Rule** — Errors MUST be either logged OR returned, NEVER both.

## Code Examples

### Structured Logging (slog)
```go
slog.Info("order processed",
    "order_id", order.ID,
    "user_id", user.ID,
    "amount", order.Amount,
)
```

### Prometheus Metrics
```go
var (
    httpRequests = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "http_requests_total",
        Help: "Total number of HTTP requests.",
    }, []string{"method", "route", "status"})
)

func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        next.ServeHTTP(w, r)
        httpRequests.WithLabelValues(r.Method, r.URL.Path, "200").Inc()
    })
}
```

### OpenTelemetry Tracing
```go
func (s *Service) DoWork(ctx context.Context) error {
    ctx, span := otel.Tracer("my-service").Start(ctx, "DoWork")
    defer span.End()
    
    // Perform work, span context is propagated via ctx
    return s.repo.Save(ctx, data)
}
```

## Anti-patterns

- ❌ **High cardinality labels** — e.g., using UserID in Prometheus labels (crashes Prometheus).
- ❌ **Log and Return** — Causes duplicate logs and noise.
- ❌ **Not passing context** — Breaks the trace chain and makes debugging across services impossible.
- ❌ **Using `fmt.Printf` or `log.Printf`** for production logs (non-structured).
- ❌ **Missing error recording in spans** — Use `span.RecordError(err)` to see failures in your tracing tool.
