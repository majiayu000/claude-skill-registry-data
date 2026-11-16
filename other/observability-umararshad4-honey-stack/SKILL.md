---
name: observability
description: "Instrument a service for production: structured logs, metrics (RED/USE), distributed tracing, error tracking, SLOs and alerting. OpenTelemetry-first."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (OpenTelemetry spec status, Prometheus, Sentry, Google SRE SLOs/burn-rate alerts). Details in references/."
---

# observability

Make a running system legible: what happened (logs), is it healthy (metrics), where did time go (traces). Default to **OpenTelemetry** — instrument once, export anywhere.

## The three pillars (reach for the right one)
- **Logs** — one event: "what exactly happened in this request?" Detail-rich, expensive at volume.
- **Metrics** — aggregates and trends: "is the system healthy?" Cheap, numeric; not for high-cardinality per-entity questions.
- **Traces** — causality across services: "where did time go for this request?"
Prefer **one wide, structured event per unit of work** (a span carrying user/route/version/timing/outcome) over scattered thin log lines — it's queryable after the fact.

## Structured logging
JSON, one object per line, with `timestamp`, `level`, `service`, `trace_id`/`span_id` and a propagated request/correlation ID. **Never log** secrets, tokens, passwords, auth headers, or PII beyond what's lawful — redact at the logger. Sample INFO/DEBUG at volume; keep all errors. Libraries: pino (Node), zap/zerolog/slog (Go), structlog (Python). `references/logging.md`.

## Metrics
Counter (monotonic), gauge (point-in-time), **histogram** (distributions — use for latency, not averages). **RED** per service, **USE** per resource. Prometheus + Grafana, Alertmanager. **The #1 mistake is a cardinality explosion**: never put unbounded values (user id, email, request id, raw URL, trace id) in metric labels — series count is the product of all label cardinalities. Keep labels bounded (route *template*, status class, method, region); put high-cardinality context in traces/wide events. `references/metrics.md`.

## Tracing
Spans form a tree per request sharing a `trace_id`; propagate context across services with **W3C Trace Context** (`traceparent`). Pipeline: app → OTel SDK → **Collector** (batch, redact, sample, fan-out) → backend (Jaeger/Tempo/Honeycomb/Datadog). Sampling: head (cheap, may drop the rare error) vs **tail** (decide after the trace completes — keep all errors + slow traces; preferred). `references/tracing.md`.

## Error tracking
Sentry (or GlitchTip/Rollbar, or errors-as-spans). Upload source maps per release so stack traces are readable; tag events with release/commit + environment for "regressed in release X". Tune fingerprints so one bug isn't thousands of issues. Alert on *new/regressed/spiking* issues, not every occurrence.

## SLOs & alerting
**SLI** = measured indicator (e.g. % requests < 300ms); **SLO** = target over a window (99.9%/30d); **error budget** = 1 − SLO, which governs release risk. **Alert on symptoms (user-facing SLO burn), not causes** — page on error-rate/latency, not "CPU 90%". Use **multi-window multi-burn-rate** alerts (fast-burn → page, slow-burn → ticket). Every page must be actionable; demote the rest to tickets/dashboards or alert fatigue hides real incidents. `references/slos.md`.

## Instrumenting a service
Auto-instrumentation first (OTel agents capture HTTP/DB/queues with near-zero code), then manual spans on meaningful business operations with domain attributes (`order.id`, `tenant`), recording exceptions and span status. Set `service.name`, `service.version`, `deployment.environment` everywhere — they correlate all three pillars. `references/instrumenting.md`.

## Confirm before (never on your own)
- Turning on high-overhead/high-volume instrumentation in prod (full sampling, verbose spans, heap profiling) — it adds latency and cost.
- Exporting telemetry to a third-party backend before PII/secret redaction is in the Collector.

Done when: the service emits correlated logs/metrics/traces with `service.name`/`version`/`environment` set, secrets are redacted, and alerts fire on SLO burn rather than raw resource metrics.
