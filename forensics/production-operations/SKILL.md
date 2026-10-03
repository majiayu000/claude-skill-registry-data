---
name: production-operations
description: Route release readiness, observability and runbook design, and incident postmortems for production systems.
---

# Production Operations

Choose one primary mode and read only its workflow. Add modes only when the request crosses preparation, live diagnostics, and retrospective analysis.

| Mode | Use when | Workflow |
| --- | --- | --- |
| `release-readiness` | Check build, migration, configuration, rollout, rollback, support, or go/no-go evidence. | [Release readiness](references/workflows/release-readiness.md) |
| `observability-runbooks` | Design logs, metrics, traces, alerts, dashboards, SLOs, triage, or recovery steps. | [Observability runbooks](references/workflows/observability-runbooks.md) |
| `incident-postmortems` | Reconstruct impact, timeline, detection, contributing factors, and corrective actions. | [Incident postmortems](references/workflows/incident-postmortems.md) |

Do not load sibling workflows or artifacts prospectively. Keep live mutations and go/no-go decisions behind explicit authority; distinguish facts, hypotheses, and unverified gates.
