---
name: right-size
description: Grade an epic's work items and output a dispatch plan — how much process each item deserves, and the concrete workflow/skill to run it with.
disable-model-invocation: true
---

# Right-size

Match process weight to the work — in either direction. Heavy workflow on a mechanical dedup is ceremony; a bare agent on a pattern-establishing auth change is negligence. Both are right-sizing failures, and the second is costlier.

You are grading, not executing. No edits, no dispatched implementation agents, no oracle planning. The deliverable is the dispatch plan; the user decides what runs.

## 1. Ingest

Read the epic and every child work item — GitHub issue with sub-issues (`gh`), a plan file, or a loose ticket list; treat them uniformly as *items*.

Done when every item has its goal and acceptance criteria captured, and the dependency edges between items are noted.

## 2. Grade on spec text

Score every item against every heuristic in the rubric below, from spec text alone. Assign each item a provisional verdict tier and mark it **confident** or **uncertain**. A verdict is uncertain when it hinges on a codebase fact the spec doesn't settle — how subtle the auth layer is, whether a "simple" module hides coupling, whether tests already cover the seam. Any verdict or brief that leans on a spec-stated **inventory** — counts, file lists, getter or module names — is automatically uncertain: specs go stale against the codebase, and a probe that verifies the inventory upgrades every downstream brief.

### Rubric

- **Decision density vs. line count** — process weight follows decisions, not diff size. A large item that stamps out a settled pattern is light; a small item full of judgement calls is heavy. Tell: count the choices the implementer must make that the spec doesn't already make.
- **Pattern-establishing vs. pattern-following** — an item whose output later items copy compounds its mistakes; grade it one tier heavier than its size suggests. A follower item inherits its pattern's correctness and mainly risks drift — its need is a consistency check, not decomposition.
- **Blast radius** — auth/security semantics, shared layouts, public seams, data migrations: wrong here breaks things far from the diff. Tell: who else touches what this touches.
- **TDD fit** — "no behavioral change" refactors and rendering-only work gain little from test-first; loader, validation, and state logic gain a lot. Feeds the suggested-skill column, not the tier.
- **Tracer bullet** — identify which item establishes the patterns and should run first; sequencing is part of the plan.

### Verdict tiers

- **inline** — do it in the current session; mechanical, one seam, criteria checkable at a glance.
- **single agent** — one dispatched agent, no review loop; the plan already makes the path obvious.
- **agent + review** — one agent plus a cold review pass; the judgement calls are real but contained in the item itself.
- **orchestrate** — full orchestration workflow; multiple coupled items, or an item where the implementer makes decisions the spec doesn't make *and* those decisions are copied downstream.

### Tier → dispatch mapping

Each tier resolves to one of the four installed implementation modes, so a verdict row reads "run this", not just a label — substitute the closest installed equivalent if a name has moved.

- **inline** → do it in this session now, no preparation.
- **single agent** → one of two modes, chosen by the TDD-fit heuristic: the **Builder Mode** workflow (`build.md` — orientation, `context_builder` plan, implement, oracle on gaps) when the item's value is plan quality and context; the `tdd` skill (red→green loop at a pre-agreed seam) when the item has a nameable seam and gains from test-first. Name the seam in the row when recommending `tdd`.
- **agent + review** → the same mode choice as single agent, plus a cold review pass (`aa-second-opinion`, or a fresh `design` agent with the Review workflow) triaged warm via `apply-review`.
- **orchestrate** → the **Orchestrate (TDD)** workflow, seeded with the epic reference; when step 4 fired, one orchestrate run over the whole set replaces per-item runs.
- Prefacing any tier: recommend `tidy-first` when the item needs its landing zone prepared, and **Deep Plan (TDD)** when an item's spec is too thin to dispatch from.

## 3. Probe

Dispatch explore subagents **only for uncertain verdicts** — confident verdicts never touch the codebase. One narrow, self-contained question per probe, dispatched in parallel (`detach: true`, then `wait` on the batch). Budget: `min(6, uncertain items + 1)` probes total — the budget grows with the uncertainty the grading step produced, so the inventory rule never starves it; if uncertain verdicts still exceed the budget, probe the ones whose tier would swing furthest.

Done when every uncertain verdict is resolved to confident, or the budget is spent — items still uncertain keep the *heavier* of their candidate tiers and the plan says so.

## 4. Detect double-orchestration

If the epic already is the decomposition — items with goals, criteria, and dependency edges — then running the full orchestration workflow per item re-plans a plan that exists. Recommend the alternative shape, decided by coupling: **one orchestration run over the whole set** (one item ≈ one dispatch) when items build on each other and need mid-flight verification between dispatches — a tracer-bullet chain where each item copies the last one's pattern qualifies; **sequential dispatches with one closing review** when items are independent stamps that only need a consistency check at the end. Pick one and say why — offering both is a coin-flip the user has to call. This changes the plan's headline, not just a row.

When the headline is one orchestration run over the set, per-item tiers re-scope to **dispatch weight inside that run**: `inline` items are pulled out of the run and done in this session before it starts; `single agent` = a dispatch with no checkpoint; `agent + review` = a dispatch followed by a checkpoint review before dependent items start; and no item is tiered `orchestrate` — the run *is* the orchestration. The epic itself is never a table row.

## 5. Deliver

Present the dispatch plan:

1. **Headline** — the overall shape (per step 4), and the single most load-bearing caution first: the item the user is most likely to mis-weight, named with why.
2. **Table** — one row per item: item → verdict tier → one-line reason → concrete invocation (per the tier → dispatch mapping) → sequencing note (blocked-by / establishes-pattern-for).
3. **Spec corrections** — every spec-vs-codebase discrepancy the probes surfaced (wrong counts, false acceptance criteria, contradicted prior art), each with the file evidence and which item's brief must carry the correction. A process weight asserted in metadata that the item doesn't earn counts too — a label like `ready-for-agent` on a spec that leaves real decisions unmade is a discrepancy, quoted like any other. These are the probes' yield — a discrepancy left out of the plan gets re-discovered mid-implementation by an agent without the context to judge it.

Done when every item has a verdict, a reason, and a suggestion, and every probe-found discrepancy is listed with its owning item.

On request only: post the table as a comment on the epic.
