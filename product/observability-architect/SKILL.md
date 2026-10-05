---
name: observability-architect
version: 1.0.0
description: Application-side observability — structured logs, Prometheus metrics, OTel traces, signal correlation, head sampling, PII discipline, RED+USE. Use when instrumenting code, naming metrics, or auditing what a service emits.
---

# Observability Architecture — Signal Production

What an application emits about itself: **logs**, **metrics**, **traces**. Pairs with [grafana-architect](../grafana-architect/SKILL.md) which owns the consumption side (dashboards, alerts). This skill enforces what gets emitted, how it's named, and how the three pillars correlate. Wiring code in [RECIPES.md](RECIPES.md); pinned libraries in [STACK.md](STACK.md).

## 1. Three pillars + correlation

Each pillar answers a different question:

| Pillar | Question | Cardinality | Cost |
|---|---|---|---|
| **Logs** | "What happened on *this* request?" | High (per event) | High storage |
| **Metrics** | "What is the *rate* / *aggregate*?" | Low (aggregated) | Low storage |
| **Traces** | "What was the *path*?" | One per request | Medium |

The *design goal* is **correlation**: from any signal you can pivot to the others. A trace shows a slow request → click → see the logs from that request → see the metric spike around the same time. This is what makes observability worth the cost.

**Correlation mechanism: trace_id everywhere.**

- Every log line carries the current `trace_id` and `span_id`.
- Every metric exposes the current `trace_id` as an exemplar (Prometheus exemplars).
- Every trace span carries the operation name, attributes, and status.

If you skip the correlation, you have three independent data lakes — useful in isolation, painful to cross-reference. Concrete wiring in [RECIPES §1](RECIPES.md#1-correlation-trace_id-in-log-lines).

## 2. Metrics: Prometheus

**Why Prometheus over OTel metrics in 2026:** Prom client libs are mature in every language, the exposition format is universal, ops engineers already know `rate()` / `histogram_quantile()`. OTel metrics are catching up but not yet at parity for ergonomics.

### Naming

Follow the [Prometheus / OpenMetrics convention](https://prometheus.io/docs/practices/naming/):

- **Pattern:** `<namespace>_<subsystem>_<name>_<unit>_<type>`
- `<namespace>` = application name (`orders`, `payments`).
- `<unit>` is **always present** for sample values: `_seconds`, `_bytes`, `_total`, `_ratio`, `_celsius`. Never `_ms`, never bare units.
- `<type>` suffix for cumulative counters: `_total`. Gauges and histograms don't take a type suffix.

```
orders_http_requests_total{method="POST", route="/v1/orders", status="201"}
orders_http_request_duration_seconds_bucket{le="0.5", route="/v1/orders"}
orders_db_connections_active        # gauge, no suffix
```

### Types

- **Counter** — monotonically increasing; `_total` suffix; reset on process restart. Query with `rate()`.
- **Gauge** — point-in-time value, up or down. Active connections, queue depth, in-flight requests.
- **Histogram** — distribution of values; choose buckets explicitly. Default latency buckets in [RECIPES §4](RECIPES.md#4-default-histogram-buckets).
- **Summary** — pre-computed quantiles; avoid unless you can't aggregate across instances (you usually can — use histogram).

### Cardinality

The single most expensive observability mistake: high-cardinality labels.

- **Bad:** `user_id`, `email`, `request_id`, `correlation_id`, anything unique per request. One time series per unique value — millions of series, ruined retention.
- **Good:** `method`, `route` (templatized, not the raw path), `status_class` (`2xx`, `4xx`, `5xx`), `tenant`, `region`. Bounded sets.
- **Templatize routes** to bounded patterns: `/v1/users/{id}` not `/v1/users/01J9X...`.
- **`< 100` distinct values per label** as a soft cap; review labels with more.

## 3. Logging: structured, leveled, correlated

- **Structured JSON** to stderr (per [cli-tool-architect §6](../../tooling/cli-tool-architect/SKILL.md#6-output-discipline--stdout-for-data-stderr-for-logs)). One log line = one JSON object.
- **Stdlib first:**
  - Go: `log/slog` per [go-architect §5](../../languages/go-architect/SKILL.md#5-stdlib-defaults). `slog.JSONHandler` in production.
  - Python: `structlog` configured to emit JSON.
- **Mandatory fields:** `timestamp` (RFC 3339 UTC), `level`, `msg` (fixed string), `trace_id`/`span_id` (when in a traced request), `service`.
- **Don't log full payloads.** A request body field can be PII; the bytes are dead weight even when it isn't. Log the **shape**: `request_size_bytes`, `field_count`, `customer_id`.
- **`msg` is a fixed string** for grep-ability: `msg="user created"` with `user_id` and `email_domain` as separate fields, not `msg=f"created user {email}"`.
- **One level per environment:** prod `info`, staging `info`/`debug`, dev `debug`.
- **Errors include the operation that failed + the inputs that mattered**. No stack traces in `msg`; stack traces are a separate `error.stack` field.

## 4. Tracing: OpenTelemetry

OTel for traces is unambiguously the right choice — vendor-neutral, well-instrumented per language, supports all major backends (Jaeger, Tempo, Honeycomb, Datadog).

- **Auto-instrumentation first.** OTel libs for net/http, gin, FastAPI, requests, psycopg, grpc cover 80% of useful spans for free. Add manual spans only where business boundaries deserve them.
- **Span naming:** verb + resource. `POST /v1/orders`, `db.query`, `kafka.publish`. **Templatized**, low cardinality.
- **Attribute keys follow [OTel semantic conventions](https://opentelemetry.io/docs/specs/semconv/):** `http.method`, `http.status_code`, `db.system`, `messaging.system`. Don't invent your own.
- **Set span status on errors:** `span.SetStatus(codes.Error, msg)` — backends colorize error spans.
- **Don't trace everything.** Per-call spans for hot loops kill performance. Trace the request boundary, major sub-operations (DB call, external API call, queue publish), and failure paths.

## 5. Correlation rules

Three rules to make signals jump between each other:

1. **`trace_id` in every log line.** Pull from the OTel SDK's current context — every modern logging integration supports this.
2. **Prometheus exemplars** on histograms (especially latency). When a slow bucket increments, the exemplar records the `trace_id`. Grafana lets you click from a histogram bucket directly to the trace.
3. **`service.name` and `service.version`** as resource attributes on traces + as labels on metrics + as fields on logs. Ties signals across deploys and versions.

Wiring snippets in [RECIPES §1](RECIPES.md#1-correlation-trace_id-in-log-lines).

## 6. Sampling

- **Head sampling at 10%** in production. Deterministic per `trace_id` so a request is either fully sampled or fully dropped — no half-traces.
- **100% sampling on errors** — always keep the trace when span status is error. Cheap, decisive ROI.
- **100% sampling in non-prod** (dev, staging) — volume is low; you want full visibility.
- **Tail sampling via the OTel Collector** is the upgrade when 10% head misses interesting low-volume endpoints. Adds Collector infrastructure. Defer until needed.
- **Configure via env vars** — see [RECIPES §5](RECIPES.md#5-sampling--env-var-configuration).

## 7. What NOT to emit

**PII and secrets** never appear in any signal:

- No email addresses, names, addresses, phone numbers in attributes or fields. Use `email_domain` (`acme.com`) to slice by tenant.
- No passwords, tokens, API keys, session cookies — not in headers, not in payloads. Use redaction filters at the SDK level — defense in depth, since one careless `log.Info("creating user", user)` can leak it all.
- No full payloads. Log size and shape, never contents.
- No internal IDs that could be re-identified. UUID v7 IDs are fine in metric labels (they don't leak meaning per [sql-architect §1](../../databases/sql-architect/SKILL.md#1-schema-design)); raw `auth_token_id` is not.

Configure your SDK redaction list at startup; review it on every deploy.

## 8. SLOs and golden signals

What to measure for *every* service.

### RED — for request-driven services

| Signal | Question | Metric |
|---|---|---|
| **R**ate | How many requests/sec? | `<svc>_http_requests_total` over time |
| **E**rrors | How many fail? | `<svc>_http_requests_total{status=~"5.."}` |
| **D**uration | How long do they take? | `<svc>_http_request_duration_seconds` histogram |

### USE — for resource-driven services

| Signal | Question | Metric |
|---|---|---|
| **U**tilization | What % of capacity is used? | CPU%, memory%, queue%, connection pool% |
| **S**aturation | How queued / blocked is it? | Run queue, GC pause, lock waits |
| **E**rrors | What's failing at this layer? | Resource-specific error counters |

### SLOs

- **One SLO per critical user journey.** Not per endpoint — per *journey*. "User can place an order in < 500ms 99% of the time."
- **Error budget** = `1 - SLO`. Track burn rate; alert on fast burn.
- **Don't write more than 3–5 SLOs per service.** More and no one watches any of them.
- **Multi-window, multi-burn-rate alerts** (Google SRE handbook): 2% in 1h + 5% in 6h = page. Avoids both alert noise and slow detection.

## 9. Language wiring

Full instrumentation stacks (metrics + tracing + logging together) in [RECIPES](RECIPES.md):

- Go: [RECIPES §2](RECIPES.md#2-full-instrumentation-stack--go)
- Python: [RECIPES §3](RECIPES.md#3-full-instrumentation-stack--python)

## 10. Cross-skill ties

- [grafana-architect](../grafana-architect/SKILL.md) — consumes everything this skill produces. Dashboards query Prometheus metrics; explorations follow trace_id from logs to traces.
- [go-architect §5](../../languages/go-architect/SKILL.md#5-stdlib-defaults) — `log/slog` as the logging default.
- [python-architect](../../languages/python-architect/SKILL.md) — `structlog` for structured logging.
- [fastapi-architect](../../frameworks/fastapi-architect/SKILL.md) / [gin-architect](../../frameworks/gin-architect/SKILL.md) / [nethttp-architect](../../frameworks/nethttp-architect/SKILL.md) — OTel auto-instrumentation libs cover the framework HTTP boundary.
- [rest-api-architect §10](../../protocols/rest-api-architect/SKILL.md#10-auth--security-headers) — `correlation_id` ties to `trace_id`; expose it in error responses for support workflows.
- [docker-architect §7](../docker-architect/SKILL.md#7-runtime-defaults) — logging driver routes structured logs to stderr → aggregator.
