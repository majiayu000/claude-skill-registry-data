---
name: anthropic-os
description: Use when a personal or team operating system needs a bounded redesign using Four-C, closed-loop controls, 70/30 allocation, 3B creativity, experiments, and prediction-error learning.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "high-risk"
  assumes: "The operating system has a named owner, observable workflow, local metrics, and a review cadence."
  conflicts_with: "Copying extreme productivity claims, surveillance without governance, automatic policy evolution, or cadence before context and capability."
---

# Anthropic OS

<skill_contract>
  <input>One owned work system with its workflow, users, traces, permissions, metrics, constraints, and review horizon.</input>
  <output>A supervised operating-system redesign with one bounded experiment, control gates, cadence, and rollback.</output>
  <done>The selected practice has a baseline, hypothesis, owner, metric, guardrail, budget, stop rule, and review receipt.</done>
  <non_goals>Extreme productivity claims, surveillance, automatic policy evolution, or cadence without supporting context and capability.</non_goals>

Redesign one work system as a supervised learning loop. Plasticity means practices may change from evidence; competition means alternatives contend; constraint means attention, time, permissions, and review bandwidth shape the design. Load `references/operating-system-playbook.md` for diagnostics and artifacts.

## Usage Template

Provide: system boundary, owner, desired outcome, users, current workflow, local metrics, traces/data, permissions, failure history, review capacity, and horizon.

## Workflow

<intake>

Define one operating bottleneck and baseline. Run Four-C in order: **Context** (truth/history), **Connections** (systems/accounts), **Capabilities** (skills/SOPs/evals), **Cadence** (triggers/reviews). Do not add automation cadence until the first three can support and verify it.

</intake>

<unknowns_gate>

Treat productivity multipliers, culture narratives, maturity scores, and vendor case claims as hypotheses until local evidence exists. If outcome owner, trace consent, or approval authority is absent, return `NEEDS_INPUT`. Do not infer the expansion of local labels such as CASH when the system has not defined them.

</unknowns_gate>

<execute>

1. Audit the closed loop: trace substrate, DRI, custom taste/eval, review bandwidth, prediction, feedback latency, and quiet-success stop.
2. Choose one flywheel and its bottleneck; allocate roughly 70% to a validated big bet and 30% to business-as-usual/option preservation only when local constraints justify it.
3. Apply 3B: **Bending** adapts a practice to context, **Breaking** removes a limiting rule or metric through an approved experiment, **Blending** combines mechanisms across domains.
4. Generate alternatives, then select one two-week-or-shorter experiment with hypothesis, owner, cohort, metric, guardrail, budget, stop, and rollback.
5. Run dual prediction when useful: human and agent predict outcome independently; compare actual result, record prediction error, and update decision weights only after repeated calibrated evidence.
6. Add a success-disaster pre-mortem: what breaks if adoption or throughput exceeds expectations; define load, quality, permission, support, and rollback controls.
7. Escalate permission through observe -> co-drive -> scoped reversible action -> monitored routine -> audited autonomy. Keys and environment enforce boundaries.
8. Review evidence; keep, adapt, retire, or combine the practice. No automatic archival or policy installation: human approval and the promotion gate govern system changes.

Use independent evaluation for organizational, cultural, or high-impact recommendations. A rollback restores the prior practice/config while retaining evidence and decision history.

</execute>

<evaluate>

Compare baseline and outcome on the named metric and guardrails. Inspect operator comprehension, review load, false positives, prediction calibration, and unintended incentives. Reject “success” when throughput rises but quality, agency, privacy, or local understanding falls.

</evaluate>

<retry_policy>

`max_attempts: 2` per practice experiment. Retry only after changing the hypothesis, constraint, cohort, or mechanism. Stop on repeated signature, weak feedback, review overload, guardrail regression, or `NO_PROGRESS`.

</retry_policy>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus system boundary, Four-C audit, maturity evidence, flywheel/bottleneck, allocation, predictions, experiment version, metrics/guardrails, consent/approval, independent review, rollback point, and promotion decision.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: owner, consent, outcome, or approval authority is missing.
- `INSUFFICIENT_EVIDENCE`: a maturity/policy claim lacks local observations.
- `BLOCKED_PERMISSION`: trace or delegated action exceeds authorized access.
- `VERIFY_FAILED`: outcome, guardrail, comprehension, or calibration check fails.
- `NO_PROGRESS`: changed experiments repeat the failure. `max_attempts: 2`.
- `BUDGET_STOP`: preserve the prior operating system and return a supervised next test.

## Output Contract

Return `status`, `result` (diagnosis, one redesigned loop, experiment, and review decision), `evidence`, `unknowns`, and `next_action` including approval or rollback.

## Edge Cases

- Leadership requests autonomous cadence but source context is stale: improve Context and Capabilities first; do not schedule theater.
- A practice increases output while reviewers cannot explain changes: trigger quiet-success stop, reduce volume, and restore understanding before scaling.

## Success Metrics

- One owned bottleneck, experiment, feedback signal, and review date are explicit.
- Local evidence, not borrowed multipliers, drives maturity and allocation decisions.
- The operating system improves while agency, privacy, quality, and comprehension remain within guardrails.

## Quality Gates

- [ ] Four-C order, DRI, trace consent, eval, and review budget are explicit.
- [ ] 3B changes are experiments, not automatic policy mutations.
- [ ] Independent review, human approval, and rollback match impact.
- [ ] Prediction errors and superseded practices remain auditable.
- [ ] Promotion requires repeated support/local verification and a cheap check.

</skill_contract>
