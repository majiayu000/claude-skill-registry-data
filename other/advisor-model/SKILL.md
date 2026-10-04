---
name: advisor-model
description: 'Consult a separate model at a selected plan, fork, or completion decision while the current model retains execution ownership; use supplied context only, keep the consultation read-only, and never treat advice as a goal check.'
---

# Advisor Model

## Purpose

The advisor is a second model consulted at a selected decision point. The current model
remains the executor: it owns the task, edits, commands, goal ledger, and final decision.
Advice is evidence to consider, not an approval gate. The executor may reject it when the
repository, command output, or other supplied evidence contradicts the recommendation.

This skill is standalone. A goal file is useful context when one exists, but it is not
required.

When persisted with a goal, use an optional `## Advisor` section after the budget:

```markdown
## Advisor
enabled: true | false
required: false | true
backend: native | delegated | unavailable
model: host-default | <configured model>
consultations:
- id: <stable id>
  mode: plan-review | decision-fork | completion-check
  status: pending | accepted | rejected | opaque | declined | unavailable
  plan_revision: <revision or null>
  request: <why this consultation was selected>
  evidence_refs: <paths, outputs, or transcript references supplied>
  response: <recorded response or opaque>
  disposition: accepted | rejected | unresolved
  accounting: <host-reported cumulative usage or unavailable>
criterion_proposal: <pending tightening and evidence, or none>
```

Persist explicit advisor requests here, including whether the user requires a consultation.
An explicit `enabled: false` disables consultation. Honor the selected backend and model and
the host's existing configuration; do not silently override them. Record consultations here so
resume cannot dispatch the same decision twice.

## Consultation boundary

When no backend was selected, prefer an available native advisor, which may receive the full conversation according to its
host contract. Otherwise use an actual separate, read-only delegated model with the context
explicitly supplied by the executor. If neither exists, report that the advisor is unavailable
and continue the ordinary loop unless the user explicitly requires an advisor. Never present
same-model self-critique as a separate consultation.

Use one consultation when it can change the outcome materially: review a plan before work,
choose between a consequential fork, or check a result the executor believes is complete.
Do not consult for syntax, routine lookup, or every goal-loop tick.

The advisor receives only the context and artifacts the executor supplies when using the
delegated path. It must not imply that it saw private state, repository files, or tool output
unless those were included. It has no write authority and must never edit files, run the task,
set a goal status, or replace a check.

## Executor protocol and advisor response

1. The executor reads goal status, cumulative usage, finite token limit, and the latest
   consultation before invocation. With a goal, consult only while it is `active`; preserve
   other states and counters. At or above a finite token limit becomes `exhausted` before
   the call; missing finite accounting becomes `blocked`. Accounting must include the
   selected advisor's usage; an executor-only total is insufficient.
2. The executor selects exactly one configured backend and model, records the request as
   `pending` before dispatch, then sends the question and supplied context. A backend failure becomes
   `unavailable` or `declined` for that consultation; it must not silently invoke a second
   backend. Existing host settings are read-only: this skill writes no native settings.
3. A pending record found on resume is unresolved. Inspect an available recorded result or
   report it unresolved; do not assume completion and do not replay it automatically.
4. The executor asks for plan review, a decision fork, or a completion check. Routine
   questions stay with the executor and require no consultation.
5. The advisor reads the supplied artifacts and command output before judging. Name missing context and
   stop short of conclusions that depend on it.
6. For plan review, return `APPROVE` or `REVISE`, followed by ranked corrections and the
   concrete failure each correction prevents.
7. For a decision fork, select one option, give the deciding evidence, the strongest case
   for the alternative, and the evidence that would reverse the call.
8. For completion, return `PASS` or `FAIL` against the goal's declared external checks and
   review criteria, citing the evidence. If the advisor result is opaque, record it as opaque
   and do not invent a verdict.
9. Treat an opaque, declined, unavailable, or disabled result in any consultation mode as
   `OPAQUE`, `DECLINED`, `UNAVAILABLE`, or `SKIPPED`, preserving the actual response; never
   infer approval, revision, or completion from it. The executor records disposition and any
   changed plan or checks; the advisor does not mutate goal state.
10. If accepted advice changes the plan, the executor marks both the current Plan and its
   latest matching plan ledger entry `unsound` with the reason, preserves revision and
   `iterations_used`, and lets the next plan allocate the next iteration. For a proposed
   criterion tightening, preserve the current criteria and store `criterion_proposal` here.
   Before further implementation, run `verify-goal` against those unchanged criteria, then
   pass that verification ledger and the proposal to `refine-goal`. This also applies when
   verification marks the old criteria `met`: refinement may reopen that completed result.
   Clear the proposal only after refinement records its disposition. Recheck budgets between
   these operations; an interrupted handoff retains the proposal for resume. The end state
   must remain unchanged; a changed end state or widened non-goal requires a new goal contract
   and user authorization.
11. If accepted advice changes an executable artifact, the executor runs the affected checks
   again and preserves goal iteration and accounting state.

## Goal-loop accounting

Advisor usage belongs in the host's cumulative usage accounting exactly once. Do not add an
advisor total to a host total that already includes it. The executor records an in-flight
overshoot and marks `exhausted` at the next boundary.
Refresh usage after the response and before advancing the goal. If inclusive usage becomes
unavailable under a finite limit, set `blocked` and preserve the last known counters. When a
required advisor is unavailable, declines, or its pending result cannot be recovered, record that
blocker and stop the goal; resume only after resolving it or an explicit user policy change.

The goal loop does not require a consultation on every tick. A selected consultation may
inform the next plan or verification, but only the goal's declared external checks and reviews
can establish a criterion.

## Output format

```text
mode: plan-review | decision-fork | completion-check
availability: native | delegated | unavailable
verdict: APPROVE | REVISE | OPTION-A | OPTION-B | PASS | FAIL | OPAQUE | DECLINED | UNAVAILABLE | SKIPPED
evidence: <artifacts and command output actually read>
advice: <compact decision or ranked corrections>
reversal: <evidence that would change the advice>
executor-action: <what the current model should do next>
accounting: <host-reported cumulative usage, or unavailable>
```

## Source

The native advisor principle is documented at https://code.claude.com/docs/en/advisor.
