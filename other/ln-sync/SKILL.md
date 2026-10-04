---
name: ln-sync
description: "Refresh `memory/SPEC.md` and `memory/PLAN.md` in mature mode — restore canonical truth, archive retired plan history, delete stale derivative artifacts, and flag drift against code."
---

# Ln Sync

Audit and refresh the canonical documents so they stay lightweight enough for fast re-entry.

`ln-sync` is the family-wide ontology repair and garbage-collection pass. Merge equivalent facts, repair stale references, and delete exhausted derivative artifacts. Only `docs/archive/PLAN_HISTORY.md` acts as archive history.

Apply the repo's pre-release posture: optimize canonical memory for the model we now believe in, not compatibility with stale docs. Retire superseded claims, delete obsolete derivative artifacts, and tighten lexicon drift instead of preserving historical aliases in active truth.

## When to run

Prefer `ln-sync` at these moments:

- milestone boundaries
- before major refactors
- at handoff / context compaction
- when `memory/SPEC.md` or `memory/PLAN.md` feels overweight

## Document roles

| File | Authority | Keep live |
| --- | --- | --- |
| `memory/SPEC.md` | what and why | product contract, live architecture register, future direction pointers, lexicon, verification stance |
| `memory/PLAN.md` | what's next | sequencing, frontier definitions, near-horizon items, recent completions |
| `docs/archive/PLAN_HISTORY.md` | historical ledger | older completed phases and retired plan history |
| `HANDOFF.md` | derivative volatile transfer | only unfinished chat state not yet reconciled |
| `memory/CARDS.md` | derivative execution queue | only unfinished prepared scope cards inside one frontier item |
| `memory/REFACTOR.md` | derivative temporary execution plan | only unfinished refactor steps |

## Procedure

### 1. Read the current docs

If either `memory/SPEC.md` or `memory/PLAN.md` is missing, route to `ln-spec` or `ln-plan` first.

### 2. Weight check

Ask whether each file is still serving re-entry.

- If `memory/SPEC.md` is carrying embedded truths, old implementation detail, closed historical debates, or validated assumptions that no longer shape frontier work, prune it.
- If `memory/PLAN.md` is mostly completed history, collapse it to a rolling frontier and archive the rest.
- If `HANDOFF.md`, `memory/CARDS.md`, or `memory/REFACTOR.md` no longer carry live temporary state, delete them.

### 3. SPEC pass — keep only live architecture

Use the mature SPEC shape as the target unless the project has an explicit alternate shape:

- **Product Contract** — concept, constraints / non-goals, grouped capability requirements.
- **Live Architecture Register** — open assumptions, active decisions, critical invariants.
- **Future Direction Register** — directional bets with PLAN/design-doc pointers.
- Compact model / architecture sections only while they still serve as SPEC authority.
- Lexicon and Verification Design.

For each item in `memory/SPEC.md`, choose one:

- **keep live** — still unresolved or still constrains future work
- **update** — wording / evidence / scope changed
- **compress / merge** — overlaps another live row or carries too much rationale
- **retire embedded** — fully shipped and now protected by code/tests/design docs
- **move rationale** — valuable context, but too detailed for SPEC; keep a short guardrail and link to a design doc
- **future direction** — not current product contract; move under Future Direction Register or ensure PLAN owns it
- **remove** — moot, superseded, redundant, or implementation diary

#### Keep in SPEC

- stable product contract
- constraints and non-goals
- capability requirements
- open assumptions only
- current spine decisions and durable seam-defining decisions
- critical seam-level invariants only
- future direction pointers that shape sequencing
- lexicon
- verification stance / commands / blind spots

#### Remove from SPEC

- implementation diary entries
- historical completion notes already reflected in code or tests
- micro-variant decisions / invariants that are embedded in a larger seam
- validated assumptions that no longer change future work
- detailed design-doc prose, card styling minutiae, or exhaustive test inventories
- future acceptance criteria that PLAN should own until the work is active

Validated assumptions retire by default. Promote the durable residue only when it still constrains active work: product facts go to Product Contract, architectural authority goes to Active Decisions / Critical Invariants, vocabulary goes to Lexicon, and sequencing implications go to PLAN.

Do **not** remove durable seam rationale merely because code and tests now exist. Prune micro-decisions, not the architectural spine.

Merge equivalent assumptions, decisions, and invariants instead of carrying parallel rows for the same seam-level fact. When rows merge or move, repair the references that point at them.

When pruning, leave concise HTML comments naming removed IDs when useful. Do not renumber survivors.

### 4. PLAN pass — restore the rolling frontier

Prefer the conflict-resistant mature shape:

- `Context`
- `Sequencing`
  - `Active`
  - `Next`
  - `Parallel / Low-conflict`
  - `Horizon`
- `Frontier Definitions`
- `Recently Completed`
- `Dependencies`

Rules:

- treat **frontier items** as the canonical plan/Linear/branch units
- treat **slices** as scoped execution units from `ln-scope` / `ln-build`, usually inside one frontier item
- edit `Sequencing` for ordering/status churn; do not move or rewrite `Frontier Definitions` merely to reorder work
- keep detailed scope-card queues out of `memory/PLAN.md`; use `memory/CARDS.md` for temporary slice execution queues and at most a lightweight pointer from the frontier definition
- move older completed items to `docs/archive/PLAN_HISTORY.md`
- keep only the last 2-3 completed items live
- only active / next frontier definitions need detailed acceptance or traceability
- keep dependency diagrams limited to active / next frontier ids
- keep enough `Why now / unlocks` context that a fresh thread can understand frontier ordering without reading the full archive
- do not archive handoffs, refactor plans, or sync reports

### 5. Drift and ontology check

Scan recent code / commits for:

- new domain concepts not reflected in the lexicon
- durable decisions not reflected in `memory/SPEC.md`
- active work not represented in `memory/PLAN.md` sequencing or frontier definitions
- stale references between `memory/PLAN.md` and `memory/SPEC.md`, especially PLAN links to retired assumptions / decisions / invariants
- equivalent facts that should merge instead of coexisting
- prepared cards in `memory/CARDS.md` that should be retired, re-scoped, or reconciled into the next thread's live state
- stale derivative artifacts that should be deleted after reconciliation

### 6. Garbage-collect derivative artifacts

Delete exhausted temporary artifacts after their useful state has been reconciled:

- remove stale `HANDOFF.md` files instead of preserving them as archive breadcrumbs
- remove exhausted `memory/CARDS.md` queues instead of letting old prepared cards masquerade as live work
- remove completed `memory/REFACTOR.md` files instead of leaving completion notes or pointers
- if an ad hoc planning/status file was created with explicit permission and is now exhausted, reconcile any durable facts, then delete it unless the user asked to keep it

### 7. Report and update

Produce a concise sync report and make the edits.

```md
## Sync Report

### Pruned
- [items removed, merged, or moved and why]

### Archived
- [history moved to PLAN_HISTORY.md]

### Garbage-collected
- [temporary artifacts deleted and why]

### Drift fixed
- [concept / decision / frontier / traceability updates made]

### Retirement assessment
- [whether embedded items were sufficiently retired, or whether a stronger protocol / follow-up frontier is needed]

### Remaining live items
- [important assumptions or frontier work that still matter]
```

## Routing

After sync, present these options to the user (use `tool-ask-question`):

| #   | Label             | Target       | Why |
| --- | ----------------- | ------------ | --- |
| 1   | Scope next item   | `ln-scope`   | Docs are current and the next slice is ready |
| 2   | Revisit the plan  | `ln-plan`    | Sync changed priorities or exposed new frontier work |
| 3   | Back to triage    | `ln-consult` | Direction needs reassessment |

Recommended: **1** if the frontier is still sound, **2** if sync materially changed it.
