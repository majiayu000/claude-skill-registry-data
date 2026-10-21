---
name: observability
description: Instrument service behavior and verify operators can diagnose it. Triggers on "add logging", "加日志".
---

# Observability and Instrumentation

## When to use

- Instrument service behavior and verify operators can diagnose it.

**Not for:** incident-response for active incidents.

## Steps

1. Identify operational questions, critical flows and service objectives.

2. Add redacted structured logs, bounded metric labels and meaningful correlated spans using existing tooling.

3. Configure actionable symptom alerts with measured or requirement-based thresholds and a runbook: meaning, first query, recovery and escalation.

4. Generate controlled traffic and failures, confirm actual signals and alert behavior and restore temporary settings.

## Verify

- Telemetry traces real success and failure without secrets; unavailable signal or delivery checks are explicit.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/observability-checklist.md](references/observability-checklist.md) — at-a-glance instrumentation checklist + pre-launch gate
- [references/slo-methodology.md](references/slo-methodology.md) — SLI definition, error budgets, burn-rate alerting, SLO-based release gating
- [references/cost-observability.md](references/cost-observability.md) — FinOps: cost attribution, per-request cost, anomaly detection, optimization levers
- [runbook-template.md](../incident-response/references/runbook-template.md) — runbook authoring structure (write when you create the alert, not during the incident)
- [references/slo-implementation.md](references/slo-implementation.md) — Prometheus recording/alerting rules, multi-window burn-rate alerts, error-budget queries, dashboards, review cadence
