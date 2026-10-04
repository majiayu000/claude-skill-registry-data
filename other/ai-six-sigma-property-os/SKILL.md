---
name: ai-six-sigma-property-os
description: Use when property-service operations need an AI plus ontology plus DMAIC design for work orders, dispatch, quotes, evidence, CTQ metrics, and control dashboards.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "high-risk"
  assumes: "A real or planned service workflow has identifiable customers, work orders, workers, quotes, evidence, and accountable operators."
  conflicts_with: "Automating undefined processes, hiding safety or pricing decisions, or expanding into a full ERP before the core quality loop works."
---

# AI Six Sigma Property OS

<skill_contract>
  <input>Named property-service workflow, actors, evidence, CTQs, approval boundaries, and MVP constraints.</input>
  <output>A bounded ontology, DMAIC control plan, agent roles, gates, metrics, and rollback-ready MVP design.</output>
  <done>Every proposed state transition and CTQ has an owner, evidence source, verifier, approval gate, and control receipt.</done>
  <non_goals>Full ERP replacement, autonomous safety or pricing decisions, and automation of undefined processes.</non_goals>

Ontology defines the operating world; bounded agents execute and audit; DMAIC improves rules from work-order evidence. Design the management system before software scope. Load `references/property-control-model.md` for the baseline ontology, CTQs, and state machine.

## Usage Template

Provide: business type, stage, first workflow, current process/data, service standards, approval boundaries, failure history, and MVP budget. Optional: table schemas and sample work orders.

## Workflow

<intake>

Verify the operating objective and select one first workflow: classification, dispatch recommendation, quote draft, evidence audit, or quality dashboard. Map actors, current states, systems of record, customer/safety impact, and data maturity.

</intake>

<unknowns_gate>

If service standard, accountable owner, safety boundary, or system of record is missing, return `NEEDS_INPUT`. Treat absent baseline data as a Measure-phase task; never invent CTQ thresholds or automation accuracy.

</unknowns_gate>

<execute>

1. **Define:** set customer pain, process boundary, work-order type, SLA, CTQs, and excluded scope.
2. **Measure:** map each CTQ to formula, source field, owner, baseline, target, and data-quality check.
3. **Analyze:** for red metrics, use process bottlenecks, fishbone categories, and 5 Why until the cause can change a rule, field, SOP, training item, or threshold.
4. **Improve:** propose one bounded change with hypothesis, owner, rollout cohort, budget, success/guardrail metrics, and rollback trigger.
5. **Control:** define dashboard, alert, approval, exception, audit sample, and review cadence.
6. Define ontology objects and legal work-order transitions before assigning agent roles.
7. Give each agent a bounded input, action, output, confidence, evidence, and human gate.
8. Keep customer-facing quotes, pricing/policy changes, low-confidence dispatch, safety, compliance, privacy, payment, case closure, and disciplinary action under human approval.

Use an independent quality reviewer for closure and abnormal cases. Rollback must restore the prior rule/SOP/version without deleting work-order evidence.

</execute>

<evaluate>

Trace every agent action and dashboard metric to a field, state transition, CTQ, owner, and gate. Simulate normal, missing-data, exception, rework, and cancellation paths. Reject modules with no objective metric or safe manual fallback.

</evaluate>

<retry_policy>

`max_attempts: 2`. Retry design only after changing scope, data definition, rule, or control. Stop on repeated missing baseline, unsafe transition, or `NO_PROGRESS`; escalate the decision to the accountable operator.

</retry_policy>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus process version, ontology, state machine, CTQ dictionary, agent contracts, approval matrix, experiment cohort, exceptions, independent review, and rollback receipt.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: owner, service standard, safety boundary, or data source is unclear.
- `INSUFFICIENT_EVIDENCE`: baseline cannot support threshold or automation decisions.
- `BLOCKED_PERMISSION`: required approval/system access is absent; remain in manual mode.
- `VERIFY_FAILED`: state, metric, or agent action is not traceable; block rollout.
- `NO_PROGRESS`: two changed designs fail the same control. `max_attempts: 2`.
- `BUDGET_STOP`: preserve the manual workflow and return the smallest measurable MVP.

## Output Contract

Return `status`, `result` (DMAIC memo, ontology, states, CTQs, agent/gate matrix, dashboard, MVP), `evidence`, `unknowns`, and `next_action` with approval and rollback condition.

## Edge Cases

- Quote automation has no reliable material-cost feed: generate an internal draft with uncertainty and require human pricing approval; do not send it.
- Worker recommendation is high-confidence but violates access/safety rules: rules override score and the case moves to exception review.

## Success Metrics

- One bounded workflow is measurable end to end.
- Every automated action maps to state, evidence, CTQ, owner, and human gate.
- Red metrics produce controlled countermeasures rather than commentary.

## Quality Gates

- [ ] MVP excludes unrelated ERP/marketplace/payroll scope.
- [ ] CTQs have formulas, source fields, baselines, and owners.
- [ ] Independent review, approval, manual fallback, and rollback are explicit.
- [ ] Exception and rework paths were simulated.

</skill_contract>
