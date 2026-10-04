---
name: coval-eval-audit
description: Audit an existing Coval evaluation setup for coverage, misleading scores, missing evidence, judge validation and execution risk. Read-only; use when inheriting an eval or deciding whether its results support a release decision.
---

# Audit a Coval evaluation

Inspect what the customer actually ran and what decision those results support.
Stay read-only unless they separately request a concrete repair or test.

## Collect the smallest useful evidence

Confirm organization, workspace, API environment, agent, time window and decision.
Use explicit resource IDs where available. Start with a recent relevant run,
its agent, persona, cases and metrics; sample completed, failed and unscored
conversations. Don't download the whole account or launch a run to fill a gap.

Discover installed commands with `coval --agent agent manifest` and resource
`context`. Common reads:

```bash
coval --agent runs get <run-id>
coval --agent agents get <agent-id>
coval --agent personas get <persona-id>
coval --agent test-sets get <test-set-id>
coval --agent test-cases list --test-set-id <test-set-id> --page-size 100
coval --agent simulated-conversations list --run-id <run-id> --page-size 100
coval --agent simulated-conversations get <simulation-id>
coval --agent simulated-conversations metrics <simulation-id>
coval --agent metrics get <metric-id>
```

Check `ok`, errors and pagination. Some CLI versions return only the first page
without its token. For complete coverage, use the published `/v1/openapi` schemas
and public API pagination (`page_token` from `next_page_token`), retaining the
original filter and workspace header. Never infer missing resources from a
failed read, a truncated page or an unsearched workspace. If evidence is bounded,
state the inspected sample and leave completeness unknown.

## Inspect six decision risks

| Area | Inspect | Consequence / next step |
|---|---|---|
| Evaluation objective | Requirement, pass rule and origin of each key criterion | Generic sentiment/tone alone cannot establish task success. Use `configure-metrics` for a concrete criterion. |
| Scenario coverage | Actual inputs/expectations, known incidents, source distribution, duplicate cases, language and persona choices | A generated happy-path suite may miss observed failures. Use `coval-discover-failures` or `build-test-suite`. |
| Execution validity | Requested vs observed conversations; individual statuses; both transcript speakers; recording availability; test scenario actually exercised | A completed run can contain unusable calls. Separate connection, simulator, provider and agent failures; do not count unknowns as passes. |
| Measurement validity | Metric output status, value, units, polarity, criteria subvalues, evidence source, metric version | Null/skipped/failed is not zero or pass. A composite average can hide one mandatory failed criterion. Transcript claims don't prove a tool side effect. |
| Human calibration | Human label provenance, disagreements, both classes, prompt examples, dev/test separation and version matching | Agreement on tuned examples is development evidence. Use `coval-calibrate-metric`; missing labels means unvalidated, not a bad judge by assertion. |
| Comparison and cost | Exact case IDs/versions, persona/config/model changes, repeats, missing pairs, runtime/spend and rerun authorization | Confounded deltas and small samples cannot establish improvement. Use `coval-compare-runs`; propose a bounded test, never an automatic hill-climb. |

Read actual transcript excerpts and metric explanations for consequential
findings. For audio claims, listen to the relevant recording segments. For tool
or retrieval claims, inspect correlated traces and returned evidence; missing
instrumentation is an observability gap, not proof a tool never ran.

Numerical latency, counts and calibrated categorical metrics are legitimate.
Do not force everything into binary judging. Prefer deterministic checks for
exact constraints; require an explicit decision threshold when the result is
used as a release gate. Safety-critical requirements can justify tests before
any naturally occurring failure is observed.

## Report

For each material finding, provide severity relative to the customer's decision,
observed evidence and resource IDs, impact, smallest fix, and how to verify it.
Mark each inspected area **supported**, **problem observed**, or **unknown**.
Keep hypotheses separate from confirmed findings. Do not invent a numeric
readiness score.

Finish with:
- What was inspected (counts, scope, window, versions and missing evidence).
- Whether the evidence supports the stated decision, and why.
- At most three next actions, ordered by expected learning per cost.

Use app URLs verified from the user's org/workspace context or returned by Coval.
Do not expose credentials, signed recording URLs, private metadata or full
customer transcripts in a shareable report. No resource mutations, notifications,
scheduled monitoring or paid evaluations are part of this audit.
