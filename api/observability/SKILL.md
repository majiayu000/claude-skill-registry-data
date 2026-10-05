---
name: observability
description: Use when instrumenting a system or when an incident cannot be diagnosed from existing telemetry. Covers structured logging, metrics, distributed tracing, SLOs, and alerts that are worth waking someone for.
metadata:
  category: devops
  version: 1.0.0
  tags: [observability, monitoring, tracing, metrics, slo]
---

# Observability

## Purpose

Instrument a system so that a question you did not anticipate can still be answered from its telemetry. Monitoring tells you *that* something is wrong; observability lets you find out *why* without shipping new code.

## When to Use

- Instrumenting a new service.
- An incident where the data needed to diagnose it did not exist.
- Defining SLOs and the alerts that derive from them.
- Reducing alert noise that the team has learned to ignore.

## Capabilities

- Structured logging with consistent, queryable fields.
- Metrics: RED (rate, errors, duration) for services, USE (utilization, saturation, errors) for resources.
- Distributed tracing with OpenTelemetry and context propagation.
- SLO and error-budget definition.
- Alert design: symptom-based, actionable, and rare.

## Inputs

- The service, its dependencies, and its user-facing operations.
- The questions you have needed to answer in past incidents.
- Existing telemetry and its gaps.

## Outputs

- Structured logs with a trace ID on every line.
- RED metrics per endpoint and USE metrics per resource.
- SLOs with error budgets, and alerts that fire on symptoms.

## Workflow

1. **Instrument the user-visible path first** — Rate, errors, and duration per endpoint. This answers "is it broken and for whom", which is the first question in every incident.
2. **Log structurally** — JSON with consistent field names, including a trace ID. A log line that must be parsed with a regex is a log line nobody will query at 3am.
3. **Propagate context** — OpenTelemetry, with the trace ID flowing through every hop, including the message queue. A trace that stops at a queue boundary is half a trace.
4. **Define SLOs from the user's perspective** — "99.9% of checkout requests succeed within 500ms." Not "CPU stays below 80%", which no user has ever cared about.
5. **Alert on symptoms, not causes** — Page on "error budget burning fast", not on "CPU high". High CPU with a healthy service is not an incident.
6. **Delete the alerts nobody acts on** — An alert that has fired forty times and been acknowledged forty times without action is training the team to ignore alerts.

## Best Practices

- Every alert that pages a human must be urgent, actionable, and real. If it is not all three, it belongs on a dashboard, not on a pager.
- High-cardinality fields (user ID, request ID) belong in traces and logs, not in metric labels. A metric label with a million values will take down your metrics backend.
- The trace ID must appear in the log line, the error report, and the response header. That is what turns three tools into one investigation.
- Log at the boundaries: request in, request out, and the decision points between. Logging every function entry produces volume, not insight.
- Sample traces, but always keep the errors and the slow ones. Head-based sampling that drops the 1% of requests that failed has thrown away the only useful data.
- An SLO with no error budget policy is a number on a dashboard. Decide in advance what happens when the budget is exhausted.

## Examples

**A structured log line that is actually useful:**

```json
{
  "timestamp": "2026-03-04T09:14:22.481Z",
  "level": "error",
  "message": "payment authorization failed",
  "service": "checkout-api",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "order_id": "ord_01HXKZ",
  "tenant_id": "tnt_9f2",
  "gateway": "stripe",
  "gateway_error_code": "card_declined",
  "duration_ms": 842,
  "attempt": 2
}
```

Every field is queryable. "Show me declines for tenant tnt_9f2 in the last hour, grouped by gateway error code" is one query, not a grep.

**A symptom-based alert with a burn rate:**

```yaml
# Pages only when the error budget is being consumed fast enough to matter.
- alert: CheckoutErrorBudgetBurn
  expr: |
    (
      sum(rate(http_requests_total{route="/checkout", status=~"5.."}[5m]))
      / sum(rate(http_requests_total{route="/checkout"}[5m]))
    ) > (14.4 * 0.001)                     # 14.4x burn against a 99.9% SLO
  for: 2m
  labels: { severity: page }
  annotations:
    summary: "Checkout is burning its error budget 14x faster than sustainable"
    runbook: "https://runbooks.example.com/checkout-errors"
    dashboard: "https://grafana.example.com/d/checkout"
```

A 14.4x burn rate over 5 minutes exhausts a 30-day budget in about two days. That is worth waking someone for. A 2x burn is not.

## Notes

- Multi-window, multi-burn-rate alerting (a fast window for severe burns, a slow window for gradual ones) is the standard way to get both fast detection and low noise. A single threshold gives you one or the other.
- OpenTelemetry is now the vendor-neutral standard for traces and metrics. Instrumenting with a vendor SDK locks the instrumentation to the vendor; instrumenting with OTel does not.
- Logs are the most expensive telemetry per byte and the least structured. If a question can be answered by a metric or a trace, do not answer it with a log search.
