---
name: observability
description: >-
  Design metrics, logs, traces, alerts, and SLOs alongside a feature or
  service. Use when adding observability, defining SLIs/SLOs, designing
  dashboards or alerts, or when a feature is about to ship with no way to tell
  if it works in production. Do not use for handling a live outage (use
  incident-response).
---

# Observability

If you can't tell within minutes that it broke in production, it isn't done. Design the signals with the feature, not after the incident.

## Workflow

1. **Define "healthy" for this feature** — 1–3 user-observable outcomes (request succeeds within X ms, job completes, message processed exactly once). These become your SLIs.
2. **Metrics** — instrument the RED set per service/endpoint (Rate, Errors, Duration) and the USE set per resource (Utilization, Saturation, Errors) where relevant. Name metrics per the project's existing convention; add labels for the dimensions you'll actually filter by — not unbounded ones (no user-ids as labels).
3. **Logs** — structured (key=value/JSON), one event per line, at boundaries and failures. Every error log answers: what operation, on what input (id, not payload), failed how, correlation id. No PII/secrets. Log levels mean something: `error` pages someone, `warn` is actionable later, `info` narrates state changes.
4. **Traces** — propagate the correlation/trace id across service and queue boundaries the feature touches. Span the operations you'll want to see in a slow-request investigation.
5. **Alerts** — alert on symptoms (SLO burn, error rate, latency) not causes (CPU). Every alert has: threshold with rationale, runbook link, and an owner. If it can't wake someone with a next action, it's a dashboard panel, not an alert.
6. **SLOs** — for services with consumers: target (e.g. 99.9% success over 30d), measurement query, and the error budget policy (what stops when the budget burns).
7. **Verify the signals** — trigger a failure in a test environment and confirm the metric moves, the log line appears, and the alert fires. Unverified observability is decoration.

## Constraints

- Reuse the project's existing observability stack and conventions; don't introduce a second metrics system for one feature.
- Cardinality is a cost: review label sets before shipping.
- Dashboards answer questions ("is checkout healthy?"), not display everything collected.

## Verification

- [ ] SLIs defined from user-observable outcomes
- [ ] RED/USE instrumentation added where applicable
- [ ] Structured logs at boundaries/failures, no PII
- [ ] Correlation id propagates across the feature's boundaries
- [ ] Alerts have thresholds, owners, runbook links
- [ ] Signals verified by triggering a failure
