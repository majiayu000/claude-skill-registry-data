---
name: observability
description: Add structured logging, metrics, and distributed tracing to any service or monolith
triggers: [observability, logging, metrics, tracing, monitoring, alerting, structured logs, distributed tracing, telemetry]
audience: engineer, manager
---

# Observability

## Context
Observability is the ability to understand the internal state of a system from its external outputs. The three pillars are **logs**, **metrics**, and **traces**. A system without observability is a black box — you cannot debug production issues, validate deployments, or understand user-facing behavior.

Works in monoliths (single service, shared log/metrics output) and distributed systems (requires correlation IDs and distributed tracing).

Use this skill when:
- Instrumenting a new service or feature
- Diagnosing a production issue with poor visibility
- Reviewing observability coverage before a major release
- Setting up alerting for a system that lacks it

## Instructions

### Pillar 1 — Structured Logging

**Rules:**
1. **Log in structured format (JSON).** Never use unstructured string concatenation. Structured logs are queryable.
2. **Every log line must have:** timestamp, log level, service name, correlation/trace ID, and message.
3. **Log at the right level:**
   - `ERROR` — unexpected failure requiring investigation
   - `WARN` — unexpected but handled, or degraded behavior
   - `INFO` — significant business events (order placed, user logged in)
   - `DEBUG` — developer diagnostics (do not enable in production by default)
4. **Never log sensitive data:** passwords, tokens, PII, payment data.
5. **Include context, not just messages.** Bad: `"payment failed"`. Good: `{"event": "payment_failed", "order_id": "abc", "reason": "gateway_timeout", "attempt": 2}`.

**Minimum fields on every log entry:**
```json
{
  "timestamp": "2025-03-15T21:00:00Z",
  "level": "ERROR",
  "service": "checkout-service",
  "trace_id": "abc123",
  "span_id": "def456",
  "message": "Payment gateway timeout",
  "order_id": "ord_789",
  "duration_ms": 5023
}
```

### Pillar 2 — Metrics

**Key metric types:**
| Type | Use for | Example |
|------|---------|---------|
| **Counter** | Things that accumulate | `http_requests_total` |
| **Gauge** | Current values | `active_connections`, `queue_depth` |
| **Histogram** | Latency and size distributions | `http_request_duration_seconds` |

**The Four Golden Signals (Google SRE):** Instrument these for every service:
1. **Latency** — time to serve a request (separate success vs. error latency)
2. **Traffic** — requests per second
3. **Errors** — error rate (4xx, 5xx, application errors)
4. **Saturation** — how "full" the service is (CPU, memory, queue depth)

**USE Method (for infrastructure):**
- **Utilization** — % time resource is busy
- **Saturation** — amount of queued/waiting work
- **Errors** — error count

### Pillar 3 — Distributed Tracing

**For monoliths:** Add trace IDs to log lines to correlate events within a single request lifecycle.

**For distributed systems:**
1. Generate a `trace_id` at the entry point (API gateway or first service to receive the request).
2. Propagate `trace_id` and `span_id` in HTTP headers (`traceparent` in W3C Trace Context format).
3. Every service creates a child span with its own `span_id` and the parent's ID.
4. Instrument slow or critical operations as explicit spans.

**OpenTelemetry** is the standard instrumentation library — use it over vendor-specific SDKs where possible.

### Alerting Principles
- **Alert on symptoms, not causes.** Alert when users are affected (high error rate, high latency), not when an internal metric crosses a threshold.
- **Every alert must be actionable.** If you don't know what to do when an alert fires, it should not be an alert.
- **Link every alert to a runbook.** The alert body should include a direct link to the relevant runbook.
- **Avoid alert fatigue.** A team that ignores alerts is more dangerous than a team with no alerts.

### Observability Readiness Checklist
- [ ] All services emit structured JSON logs
- [ ] Logs include trace ID and service name
- [ ] Four golden signals are instrumented and dashboarded
- [ ] Alerts exist for error rate and latency SLOs
- [ ] Distributed traces propagate across all service calls
- [ ] No sensitive data in logs
- [ ] Runbooks exist for all active alerts

## Principles
- Source: [Observability — Martin Fowler](https://martinfowler.com/articles/domain-oriented-observability.html)
- Source: [Google SRE Book — Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/)
- Key idea: *"Observability is not about collecting more data. It is about having the right data to answer arbitrary questions about your system's behavior in production without deploying new code."*

## Output Format
When applying this skill, the agent should:
- Audit existing observability coverage against the checklist
- Add structured log statements at key entry/exit points
- Instrument the four golden signals for any new service
- Generate the trace propagation boilerplate for the relevant language/framework
- Produce a prioritized list of observability gaps to address
