---
name: project-flow-ops
description: Use when projects or tasks need explicit state, WIP control, ownership, definitions of done, blocker handling, and verified closure.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "stateful"
  assumes: "Project state can be persisted and each active task can have one accountable owner."
  conflicts_with: "Hidden WIP, status by intuition, or marking work complete without a fresh verification receipt."
---

# Project Flow Ops

<skill_contract>
  <input>Project objective, tasks, owners, dependencies, budgets, artifacts, current states, and definitions of done.</input>
  <output>A WIP-limited project state with ranked work, explicit blockers, bounded actions, and verified closure receipts.</output>
  <done>Every active item has one owner and observable artifact, and completion is backed by its named fresh verification.</done>
  <non_goals>Hidden WIP, duplicate ownership, status by intuition, backlog accumulation, or completion without evidence.</non_goals>

Maintain a small, inspectable project state machine: `BACKLOG -> ACTIVE -> BLOCKED | COMPLETED`. Optimize flow and verified outcomes, not task volume.

## Usage Template

Provide: project objective, current tasks, owners, dependencies, time budget, artifacts, and definition of done. Optional: prior review receipts.

## Workflow

<intake>

Normalize each item into `{id, objective, owner, state, artifact, definition_of_done, budget, dependencies}`. Reject duplicate ownership and distinguish waiting from active execution.

</intake>

<unknowns_gate>

If an active item lacks an owner, artifact, or observable definition of done, return `NEEDS_INPUT`. Probe the ambiguity with the largest impact on scheduling; do not guess priority from wording alone.

</unknowns_gate>

<execute>

1. Rank work by objective impact, urgency, dependency leverage, and cost of delay.
2. Limit `ACTIVE` to one or two items per owner.
3. Decompose the selected item until one bounded action can produce a reviewable artifact.
4. For a blocker, record owner, missing condition, evidence, next probe, and review time; move independent work forward.
5. Run the verification named in the definition of done.
6. Move to `COMPLETED` only with a fresh receipt; otherwise keep `ACTIVE` or `BLOCKED`.
7. At review, remove stale backlog items and state the next constraint.

</execute>

<evaluate>

Check state-transition legality, WIP limits, ownership, artifact existence, and completion evidence. Use an independent check for consequential deliverables. If verification fails, reopen the item with the failure evidence and smallest corrective action.

</evaluate>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus project objective, task ledger, dependency map, WIP count, transition history, and receipts. Transitions are append-only events; current state is derived from the latest valid event.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: ownership, priority boundary, or definition of done is missing.
- `BLOCKED_DEPENDENCY`: execution cannot continue; preserve the blocker contract and review time.
- `VERIFY_FAILED`: the artifact fails its named check; reopen rather than relabel completion.
- `NO_PROGRESS`: two reviews produce no new evidence; reduce scope, change strategy, or escalate.
- `BUDGET_STOP`: stop active work, persist state, and report the highest-value next action.

## Output Contract

Return `status`, `result` (project board and transition decisions), `evidence` (artifacts and receipts), `unknowns`, and `next_action` with owner and review time.

## Edge Cases

- Everything is marked urgent: use cost of delay and dependency leverage, then force one explicit tradeoff.
- A task is 90% complete but verification is unavailable: keep it active or blocked; never infer the final 10%.

## Success Metrics

- Active WIP remains within the declared limit.
- Every completed task has an artifact and fresh verification receipt.
- Blocked work names an owner, next probe, and review time.

## Quality Gates

- [ ] Every active task has one owner and bounded budget.
- [ ] State transitions are legal and traceable.
- [ ] Completion evidence is fresh and objective.
- [ ] The next constraint is explicit after each review.

</skill_contract>
