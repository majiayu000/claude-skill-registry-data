---
name: ml-stack-tracking
description: Track and diagnose ML runs when a user asks for run identity, metrics, artifacts, dashboards, structured events, NaN or divergence alerts, stalls, privacy, or retrieval; use ledger semantics without claiming an unavailable provider integration.
---

# Run tracking and diagnostics

Require run ID, project, config, immutable input revisions, metric schema, artifact locations, privacy boundary, alert thresholds, and retention policy.

## Workflow

1. Create a provider-neutral run record and append config, metric, artifact, status, and error events using repository ledger semantics where available.
2. Emit live-dashboard expectations and structured JSON that can be replayed; keep tracking private by default.
3. Alert on NaN, divergence, stalls, threshold regressions, missing heartbeats, and budget violations with evidence and severity.
4. Bound autonomous loops: no unapproved retries, parameter changes, promotion, publication, or destructive cleanup.
5. Hand a retrieval-ready metric summary to `ml-stack-experiment`, `ml-stack-evaluation`, or `ml-stack-audit`; use `ml_stack.events` to replay available ledger history.

## Boundary and outputs

Do not claim Trackio or another adapter exists without a matching runtime operation. Abstain when event identity, timestamps, revisions, or artifact provenance cannot be reconstructed. Return run schema, event paths, alert diagnosis, operator action, and unknowns. Next owner: `ml-stack-experiment` for comparison, `ml-stack-evaluation` for quality, or `ml-stack-audit` for release evidence.

See [run schema](references/run-schema.md), [alerts and diagnostics](references/alerts-and-diagnostics.md), [tracking privacy](references/tracking-privacy.md), and [metric handoff](references/metric-handoff.md).
