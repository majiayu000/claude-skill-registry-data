---
name: ln-scope
description: "Define one thin vertical slice with target behavior, risks, and acceptance criteria. Use when scoping the next piece of work before building, or when a slice from `memory/PLAN.md` needs precise definition."
argument-hint: "[behavior to deliver in this slice]"
---

# Ln Scope

Define **one** buildable scope card. The card always describes one slice, but it can carry one of two weights:

- a **full scope card** for structural work
- a **light scope card** for bounded feature or hardening work inside settled seams

If the target behavior needs "and", split it.

Apply the repo's pre-release posture while scoping: prefer correcting the model and regenerating fixtures over preserving accidental compatibility, unless live docs or the user require migration support. Include deletion/retirement work in the slice when obsolete code, data, or terminology would otherwise linger.

## Input

The behavior to deliver: $ARGUMENTS

Orient before weighting.

If `memory/SPEC.md` exists, use its lexicon and respect its live invariants.

If `memory/PLAN.md` exists, check whether the named work is already represented as a frontier item in `Sequencing` (`Active`, `Next`, `Parallel / Low-conflict`, or `Horizon`) and `Frontier Definitions`.

Treat the containing `memory/PLAN.md` frontier item as the Linear-issue / branch boundary. Here, a frontier item means the canonical plan item, preferably keyed by a stable frontier id in `Frontier Definitions`, not the scope card you are about to write. Your scope card may narrow that frontier item into the next buildable slice, but scope-card granularity alone does **not** imply a new issue or branch. Only route to `ln-plan` for new frontier items when the frontier itself must be split or reordered.

If this is a fresh thread or an unfamiliar area, also read `HANDOFF.md` if present. Read `docs/archive/PLAN_HISTORY.md` only if the frontier rationale or touched area is still unclear.

Write a 2-4 bullet orientation note naming the containing seam, the relevant frontier item, volatile handoff state, and the main open risk.

Do not create new planning documents or scratch scope files without explicit permission. The canonical planning state remains `memory/SPEC.md` and `memory/PLAN.md`. The sanctioned derivative exception is `memory/CARDS.md`, which may hold several prepared scope cards for one frontier item while that execution queue is still live.

If scoping reveals that one frontier item needs multiple sequential slices, keep them nested under that same frontier item unless the plan-level frontier must change. Do not silently turn slices into separate tracker / branch work items.

## Prepared card queue

When the containing seam is already settled and several next commit-sized steps are obvious, `ln-scope` may prepare a short queue of consecutive scope cards in `memory/CARDS.md` instead of stopping after exactly one card.

Use this queue only when all of these are true:

- the work stays inside one existing frontier item
- each queued card is still small enough to verify and commit independently
- no queued card is expected to change requirements, assumptions, decisions, or invariants
- the next few cards are sequentially obvious enough that pre-scoping them reduces churn rather than hiding uncertainty
- later queued cards are **not expected to change shape based on the implementation findings of earlier cards**

A short serial queue is for already-legible follow-through, not for guessing ahead. If card B or C depends on what you learn while building card A, stop after scoping card A (or at most the last card whose validity is still implementation-independent).

Queue discipline:

- keep the queue short — usually 2-5 cards
- keep each card in full or light scope-card format
- mark status clearly (`next`, `in progress`, `done`, `dropped`)
- do **not** pre-scope speculative downstream cards just because the work is serial; only queue cards whose scope would still be valid if you paused before building the earlier one
- overwrite or delete `memory/CARDS.md` when the queue is exhausted or superseded
- if any queued card trips the promotion checklist, reveals a frontier split, or turns out to depend on unknown results from an earlier card, stop the queue and route back through `ln-spec` or `ln-plan` as appropriate

## Scope-weight decision

Choose one before writing the scope card.

### Full scope card

Use this when the work:

- establishes or changes a seam / boundary
- changes a requirement, assumption, decision, or invariant
- crosses more than two major boundaries
- would alter future planning if it landed differently
- is the first touch in an unfamiliar seam from a fresh thread

### Light scope card

Use this when the work is a bounded feature, hardening task, or bugfix inside settled seams you can already name.

If a light scope card later trips the promotion checklist below, stop and explicitly promote it to a full scope card.

If you cannot name the containing seam, the governing decision, or the live invariant family that contains the work, it is not settled enough for light mode.

## Full scope card

### Target Behavior

What is true when this slice is done? Single declarative sentence — observable, testable, no conjunctions.

### Boundary Crossings

Every boundary the slice passes through, entry to exit:

```
→ [entry point]
→ [layer / boundary]
→ [exit point]
```

### Risks and Assumptions

```
- RISK: [what might not work] → MITIGATION: [how to handle it]
- ASSUMPTION: [what we're assuming] → VALIDATE: [how we'll know] → [→ memory/SPEC.md §Assumptions]
```

High-risk unvalidated assumption → suggest `ln-spike` before `ln-build`.

### Acceptance Criteria

```
✓ [test name] — [observable assertion]
✓ [test name] — [observable assertion]
```

### Verification Approach

Name the oracle strategy for this slice.

```
- Inner: [oracle family] — [what it proves]
- Middle: [oracle family] — [what it proves] (if applicable)
- Outer: [oracle family] — [what it proves] (if applicable)
```

## Light scope card

### Objective

Single sentence: what this work changes for the user, operator, or codebase.

### Acceptance Criteria

```
✓ [observable result]
✓ [observable result]
```

### Verification Approach

```
- Inner: [command / test family]
- Middle: [if needed]
- Outer: [if needed]
```

### Promotion checklist

If any answer is yes, stop treating the work as light and promote it to a full scope card before routing to `ln-build`. Do not quietly carry durable change under a light card.

- [ ] Does this change a requirement?
- [ ] Does this create, retire, or invalidate an assumption?
- [ ] Does this make or reverse a non-trivial design decision?
- [ ] Does this establish a new seam-level invariant?
- [ ] Does it cross more than two major seams?
- [ ] Is this the first touch in an unfamiliar seam from a fresh thread?
- [ ] Can you not name the containing seam or current rationale from the live docs?

## Traceability

Canonical reconciliation is **mandatory**; durable updates are **conditional**.

- Full scope card: update `memory/SPEC.md` / `memory/PLAN.md` as needed during or after scoping.
- Light scope card: run the promotion checklist explicitly. If it stays light, canonical reconciliation may be a no-op; if it promotes, reconcile the durable change before build.
- Multi-card queue: keep the queue itself in `memory/CARDS.md`, but do not mirror those queued slice cards into `memory/PLAN.md` unless the frontier item itself changes. At most, add a lightweight `Current execution pointer` in the frontier definition.

When adding or updating an assumption, apply the same-item test first:

- **Same assumption** = same boundary/component + same unresolved claim

## Routing

After the scope card is complete, present these options to the user (use `tool-ask-question`):

| #   | Label          | Target       | Why |
| --- | -------------- | ------------ | --- |
| 1   | Build it       | `ln-build`   | The scope card is defined and verified enough to implement |
| 2   | Design oracles | `ln-oracles` | The verification strategy still needs explicit design |
| 3   | Spike first    | `ln-spike`   | Technical uncertainty should be retired before coding |
| 4   | Revise spec    | `ln-spec`    | Scoping revealed a durable architectural change |
| 5   | Revise plan    | `ln-plan`    | The work no longer fits the current frontier |
| 6   | Back to triage | `ln-consult` | Scope revealed unclear state |

Recommended: **1** unless the promotion checklist fires or the verification approach is still unclear. If a short prepared queue is warranted, write it to `memory/CARDS.md` and let `ln-build` consume the next ready card from there.
