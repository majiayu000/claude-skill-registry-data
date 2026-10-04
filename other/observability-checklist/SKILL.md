---
name: observability-checklist
description: What good observability looks like — structured logs, trace spans, metrics, correlation ids, and the instrumentation rules that turn logs into answers. Use when adding a feature, reviewing a service, or debugging a prod issue.
---

# Observability checklist

The goal isn't logs — it's answering "what happened" in under five minutes at 2am. Design backward from the question.

## Logs

### Structured or nothing
- JSON (or logfmt), not free text.
- Every log has: `ts`, `level`, `service`, `request_id`, `msg`, and relevant fields.
- Fields are snake_case or camelCase — pick one per service. No mixing.
- Durations in milliseconds as numbers, not "took 2s" strings.

### Levels are a contract
- `error`: something failed the user can't recover from. Alert-worthy.
- `warn`: something unexpected but handled. Review-worthy.
- `info`: the shape of normal traffic. Sampling OK.
- `debug`: developer-only. Off in prod.
- Don't invent new levels.

### What to log
- Request entry (method, path, user, request_id).
- Outcome (status, duration).
- Branch decisions that matter (authz check, cache hit/miss, retry).
- Errors with the full context you need to reproduce.

### What NOT to log
- Secrets, tokens, passwords, PII — scrub before logging.
- The full request body by default. Specific fields, yes. Everything, no.
- Stack traces as separate lines — include as a `stack` field so they stay with the event.

## Traces

### Span per unit of work
- HTTP request handler = 1 span.
- Outbound call = child span.
- DB query = child span (with `db.statement` truncated / hashed, not raw if PII risk).
- Background job step = 1 span.

### Mandatory attributes
- `service.name`, `service.version`.
- For HTTP: `http.method`, `http.route`, `http.status_code`.
- For DB: `db.system`, `db.operation`.
- For errors: `exception.type`, `exception.message`.

### Propagation
- Every outbound request carries trace context headers.
- Every background job enqueues with trace context.
- A trace that ends at the HTTP edge and restarts at the worker is useless.

## Metrics

### RED for services
- **Rate** — requests per second, per endpoint.
- **Errors** — error rate, per endpoint.
- **Duration** — p50/p95/p99, per endpoint.

### USE for resources
- **Utilization** — % of capacity in use.
- **Saturation** — queue depth / wait time.
- **Errors** — failed operations.

### Cardinality discipline
- No unbounded tags (user_id, tenant_id, url with params). They explode your TSDB bill.
- Pre-aggregate cardinal dimensions; keep labels coarse.
- `http.route` (the template), not `http.url` (the instance).

## Correlation

- `request_id` in: logs, traces (as `request.id` attr), response headers, error payloads.
- `trace_id` in: logs (auto-injected by SDK), response headers for user bug reports.
- A user reporting "I got a 500" should give you enough to find the request — the `request_id` is visible and searchable.

## Per-language

### Node
- Pino or Winston with JSON transport.
- OpenTelemetry SDK (`@opentelemetry/sdk-node`).
- Prom-client for metrics.

### Python
- `structlog` with `ProcessorFormatter`.
- `opentelemetry-sdk` + `opentelemetry-instrumentation-*`.
- `prometheus_client`.

### Go
- `slog` (stdlib, Go 1.21+) with JSON handler.
- `go.opentelemetry.io/otel` + auto-instrumentation.
- `prometheus/client_golang`.

### Rust
- `tracing` + `tracing-subscriber` with JSON formatter.
- `opentelemetry-otlp`.
- `prometheus` crate.

## Anti-patterns

- "Log everything, we'll figure it out later" — the noise hides the signal you need.
- Traces without sampling — you'll drown; sample intelligently (head-based at edges, tail-based for errors).
- Metrics where logs would do — counting "user clicked button" 1M times/day is cheaper as a metric than a log.
- Logs where metrics would do — "latency: 247ms" as a log line is wasting money; it's a histogram.
- Alerts on everything — page only on symptoms that hurt users, not causes.

## Smells

- A single log line has more than ~10 fields — probably two events glued together.
- You use `grep` to find things — you should have a field + dashboard.
- Error messages are generic ("an error occurred") — they cost you the 2am minutes.
- `console.log` in prod code — belongs in a logger, tagged and leveled.
