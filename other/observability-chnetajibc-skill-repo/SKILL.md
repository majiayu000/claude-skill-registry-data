---
name: observability
description: "Observe systems: logging, metrics, tracing, health checks, graceful shutdown. Measure before optimizing."
---

# observability

If you can't see it, you can't run it: structured logs, RED/USE metrics, traces, and honest health checks.

## Activate when

- Operating, debugging, or shipping any deployed service; adding alerts, dashboards, or probes.

## Do NOT activate for

- One-off local debugging (use a debugger/log); frontend-only analytics (see product/mvp-discovery, startup/launch-ops).

## Inspection

Inventory existing signals: log format/levels, emitted metrics, trace coverage, health endpoints, alert rules, dashboards. Find the gaps against the failure modes below.

## Decision rules

- Logs: structured (JSON) with trace/request IDs; levels meaningful (ERROR = page someone); no PII/secrets; correlation across service hops.
- Metrics: RED (rate/errors/duration) per endpoint, USE (utilization/saturation/errors) per resource; business metrics only where they drive alerts.
- Tracing: OpenTelemetry spans across service/queue boundaries; sample head- or tail-based deliberately.
- Health: liveness (restart me) vs readiness (send traffic) as separate probes hitting real checks; graceful shutdown drains first.
- Alerts: symptom-based, runbook-linked, with halt/escalation criteria — never alert on what nobody will act on.

## Procedure

1. Close the highest-risk gap first (usually: request IDs, error-rate alert, readiness probe).
2. Wire one dashboard per service (RED + saturation + deploys marked) and one runbook per alert.
3. Prove each alert fires (trigger on purpose in staging) and each probe reflects reality (kill a dependency, watch readiness drop).
4. Verify: incident drill passes using only these signals; no secret/PII in log samples.

## Failure modes

- Unstructured logs without IDs; metrics nobody alerts on; liveness==readiness single probe; alert fatigue from symptomless thresholds; traces unsampled at cost.

## Escalation

Vendor specifics via registry (opentelemetry, prometheus, grafana, sentry) + research/documentation-search; incident process itself is out of scope — hand to on-call with the runbook.

## References

- Registry: `../../research/documentation-search/references/framework-registry.yaml` (opentelemetry, prometheus, grafana, sentry).
- Related: `../../backend/production-readiness/`, `../../cloud/foundations/`.
