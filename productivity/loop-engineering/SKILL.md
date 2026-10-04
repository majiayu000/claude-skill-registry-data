---
name: loop-engineering
description: Use when a repeatable task must become a bounded Trigger -> Execute -> Verify -> State loop, scheduled automation, goal agent, or metric-driven research cycle.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "loop"
  assumes: "The task has inspectable state, a finite budget, and at least one verifier independent of the builder's opinion."
  conflicts_with: "Unbounded retries, self-certification, silent external mutation, or loops whose state cannot be recovered."
---

# Loop Engineering

<skill_contract>
  <input>A repeatable task with inspectable state, finite budgets, permissions, and an independent verifier.</input>
  <output>A validated Trigger -> Execute -> Verify -> State contract plus resumable run receipts.</output>
  <done>The declared metric or stop condition is supported by fresh validator and verifier evidence.</done>
  <non_goals>Dependency-graph orchestration, unbounded autonomy, or self-certified completion.</non_goals>

Build loops only when repeated execution creates evidence. Every loop needs admission, a validated contract, durable state, independent evaluation, bounded retries, stop/recovery rules, and a final receipt.

## Usage Template

Provide: objective, trigger, scope/non-goals, inputs, state/artifact paths, metric, verifier, permissions, budgets, stop condition, recovery, and write-back. See `references/ci-repair-loop-example.md` for a worked contract.

## Workflow

<intake>

Select one mode:

- **Goal:** run until a defined end state or cap.
- **Loop:** poll/iterate while eligible work exists.
- **Automation:** start from an external schedule/event; the trigger is not execution evidence.
- **AutoResearch:** vary experiments against an objective metric in a sandbox.

Admit only if work is repeatable, outputs are inspectable, a verifier exists, failures are recoverable, and autonomy is worth the orchestration/review cost. Otherwise use a one-shot workflow.

Use `graph-engineering` instead when explicit data dependencies, independent
branches, typed joins, or node-local recovery create measurable value. A Graph
node may use this Loop contract for local repetition; Graph width does not
replace finite Loop depth.

</intake>

<unknowns_gate>

Classify unknowns as known, probeable, testable, or blocked. Missing objective, verifier, permission boundary, budget, or recovery is `NEEDS_INPUT`; do not infer these controls from intent. Unknown implementation details may be resolved inside the loop only when the probe is bounded and reversible.

</unknowns_gate>

<execute>

Write this contract before acting:

```text
Objective:                 Mode: Goal | Loop | Automation | AutoResearch
Trigger:                   Scope:                 Non-goals:
Owner:                     Inputs:
Artifacts path:            State path:            Work clock:
Success metric:            Evidence:              Verifier:
Topology: single-agent | maker-checker | manager-workers
Max iterations:            Time limit:            Budget:
Review budget:             Stop condition:
Write-back:                Permission boundary:   Recovery:
```

Validate it with `scripts/validate_loop_contract.py --strict`. Then iterate:

1. **Observe:** load durable state, fresh environment evidence, budgets, and last error.
2. **Orient:** update one hypothesis; choose the smallest action that can change the metric.
3. **Decide:** check scope, permissions, expected evidence, and rollback.
4. **Act:** execute one bounded action and capture artifact/diff/receipt.
5. **Verify:** use a deterministic check or independent checker; compare metric and guardrails.
6. **State:** append diagnosis, action, evidence, delta, budget, and next decision atomically.
7. **Stop/continue:** stop on success, cap, permission boundary, regression, repeated signature, or no useful work.

Normalize the model/runtime termination signal after every action. `complete`
still requires the declared verifier; `tool_request` returns proposed arguments
to the host permission gate; `checkpoint/truncation` persists state before any
continuation; refusal, error, or unknown escalates. Never infer completion from
fluent prose or from the word "stop" alone.

For maintenance and queue loops, declare an allowed `NO_OP` outcome and its
eligibility query. A quiet iteration is successful only when the query proves
there was no eligible work, output count is within policy, and no side effect
occurred.

Use `single-agent` by default, `maker-checker` for ambiguous/high-risk evaluation, and `manager-workers` only for genuinely independent work with an explicit integration gate.

If a validated Graph owns the dependency topology, this skill owns only the
bounded retry behavior inside its declared `loop` nodes.

</execute>

<evaluate>

The verifier must test the declared result rather than reward activity. Check evidence freshness, metric movement, guardrails, scope, and state replay. For external or consequential actions, require approval and verified rollback before crossing the boundary.

</evaluate>

<retry_policy>

`max_attempts` equals the contract's finite max iterations. Retry only after a named diagnosis and a changed input, tool, scope, or strategy. Stop on the same failure signature twice, metric regression, exhausted review budget, or `NO_PROGRESS`.

</retry_policy>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus contract version, trigger receipt, hypothesis, action, normalized termination reason, artifact/diff, metric/guardrail delta, permissions, output count, no-op receipt, work clock, and recovery point. Append iterations; write current state atomically.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: a mandatory contract field is absent; do not start.
- `BLOCKED_PERMISSION`: the next action crosses authority; checkpoint and request approval.
- `VERIFY_FAILED`: result or guardrail fails; rollback/regroup before another attempt.
- `NO_PROGRESS`: the same signature repeats or the metric is unchanged after a changed attempt.
- `BUDGET_STOP`: any iteration, time, tool, cost, or review cap fires. `max_attempts` is always finite.

## Output Contract

Return `status`, `result` (metric/end-state decision), `evidence` (validator and iteration receipts), `unknowns`, and `next_action` (stop, retry, approval, recovery, or handoff).

## Edge Cases

- A scheduled job fired but produced no run receipt: status is triggered, not completed; inspect executor state.
- The model ends because its context or token budget is exhausted: checkpoint
  and return `BUDGET_STOP` or resume from state; do not label truncation success.
- A queue poll returns zero items: accept `NO_OP` only after the declared query
  and side-effect check pass.
- The metric improves while a safety guardrail regresses: rollback and return `VERIFY_FAILED`; never optimize the headline metric alone.

## Success Metrics

- The strict validator passes before execution.
- Every iteration changes evidence, state, or diagnosis within finite budgets.
- A fresh verifier supports the final status and residual risk.

## Quality Gates

- [ ] Trigger, owner, topology, budgets, stop, recovery, and write-back are explicit.
- [ ] Builder opinion is not the only verifier.
- [ ] Termination classes and any legal no-op have host-owned routing and evidence.
- [ ] State replay recovers the next decision losslessly.
- [ ] External mutation requires approval and rollback.

</skill_contract>
