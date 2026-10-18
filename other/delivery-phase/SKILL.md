---
name: delivery-phase
description: Human-invoked router for a scoped delivery goal using current artifacts and evidence.
disable-model-invocation: true
---

# Delivery Phase

## Quick Start

`delivery-phase` is a reusable phase router.

1. Read [phases/router.md](phases/router.md).
2. Inspect only enough issue, architecture, spec, plan, notes, diff, retained review, durable
   handoff, validation, and docs state to choose the current gate.
3. If approved artifact links or UI Evidence links are present, carry them as routing evidence.
4. Load exactly one phase file from `phases/`.
5. Complete that phase and write its outcome. Full delivery re-enters routing immediately; other modes stop at their selected boundary.

Within accepted bounds, full delivery grants its selected inner steps the authority needed to reach closeout. Progressive loading still exposes one phase at a time.

## Entry Modes

- **Full delivery:** user asks to deliver a bounded goal end to end.
- **Resume:** user returns after manual spec, plan, implementation, review, debugging, or docs work.
- **HITL checkpoint:** user explicitly wants one phase handled, then a manual stop.
- **Closeout:** user asks to finish evidence, docs, stack, tracker, or PR state after the work is already done.

## Phase Files

- [phases/router.md](phases/router.md): choose the next phase from artifacts and evidence.
- [phases/spec.md](phases/spec.md): route missing or stale Architecture/SPEC or backlog projection proof to Requirements Phase.
- [phases/plan.md](phases/plan.md): create or repair the execution-ready plan.
- [phases/implement.md](phases/implement.md): execute the accepted plan.
- [phases/review.md](phases/review.md): prepare the explicit review handoff or
  classify findings from a retained report.
- [phases/debug.md](phases/debug.md): investigate runtime-evidence failures.
- [phases/human-steering.md](phases/human-steering.md): return a scope or authority boundary for human steering.
- [phases/docs-ingest.md](phases/docs-ingest.md): ingest docs-affecting changes or record a no-op.
- [phases/closeout.md](phases/closeout.md): finish tracker, PR, validation, and final report state.

## Router Rules

- Read `router.md` and its continuity contract before selecting exactly one phase.
- Require the [Architecture/SPEC pair](references/artifact-state.md#architecturespec-pair-complete)
  before dependent dispatch in every entry mode, including local and resumed
  delivery. Reuse fresh matching authority; activate child skills only from
  their selected phase.
- One delivery run ships exactly one pull request. Every phase, including
  implementation, repair, review fixes, and docs, commits to that run's branch
  and PR. Split or stack PRs only when the user explicitly asks.
- Design-Owned UI Code from a `design-phase` promote commit is accepted input.
  Delivery adds logic, data, and the rest of the requirement to it. A change to a
  design-owned file is a defect fix only, recorded in the Phase Result.
- Full Delivery continues within accepted bounds. Other modes emit one common
  Phase Result and stop at their requested boundary.
- [references/context-continuity.md](references/context-continuity.md) owns
  Context Pointers, disposable packets, common Phase Results and legacy recovery.
- [references/phase-handoff.md](references/phase-handoff.md) owns durable delivery
  state and compact Delivery Handoff; [phases/review.md](phases/review.md) alone
  owns delivery review transitions and the two-completed-pass policy.
- Failed-task and repair evidence selects
  [references/failure-continuity.md](references/failure-continuity.md).

## Stop Conditions

- User explicitly requested a HITL checkpoint or one-phase mode and its resumable state was written.
- Router reaches closeout and final evidence is reported.
- Scope is ambiguous, stale, contradictory, or blocked by missing access.
- `human_steering_required` remains durable while its required decision is unresolved.
