---
name: sprint-planner
owner: baseline
description: Propose the next dependency-ready sprint from the ALREADY-DECOMPOSED roadmap — standup's active sibling. Reads docs/roadmap-execution-plan.md + the memory backlog, computes per-task readiness from the roadmap's machine-readable status, orders with roadmap-planner's graph engine, and emits a proposed task-set (sprint-plan manifest shape) with per-feature done-criteria, excluding unready tasks and naming their unmet prerequisite. PROPOSES ONLY — the human confirms/edits before /triage routes it (typically to the `power` track). Distinct from `sprint-plan`, which decomposes a fresh vision.
disable-model-invocation: true
---

# sprint-planner — select the next ready sprint from the roadmap

`sprint-plan` **decomposes a fresh vision** into features. `sprint-planner` **selects from an
already-decomposed roadmap** — it does not invent features, it picks the ready, cohesive subset of
roadmap tasks and proposes them as a sprint. Same manifest schema, same `sprint-oracle` completeness
gate; different input (existing roadmap graph) and different verb (select, not decompose).

This is standup's **active sibling**: standup recaps "where are we + next single pickup"; sprint-planner
proposes "the next coherent sprint (3–4 dependency-ready tickets)" to feed the `power` batch-sprint track.

## Step 1 — gather (reuse standup's readers)

```bash
node .claude/skills/standup/gather.mjs --root .
```

Use the public `gatherSync({rootDir})` recap: `roadmap` (epics + per-task emoji status) and `backlog`.
Do **not** reach into standup's module-private readers.

## Step 2 — build the task graph + status

Assemble a `tasks.json` (roadmap-planner's shape: `{tasks:[{id, epic, bucket, category, title, deps[],
order?}]}`) from the roadmap in main context — the same model step roadmap-planner documents. Roadmap
dependencies are usually prose in the roadmap text; read them from the roadmap and the derived artifact
under `docs/roadmap/derived-*.md` when present. (A project that records structured `deps:` in its tracker
can feed them directly instead of re-deriving from prose.)

Order + cycle-check with the existing engine (CLI subprocess; it has no exports):

```bash
node .claude/skills/roadmap-planner/scripts/graph.mjs order  <tasks.json>
node .claude/skills/roadmap-planner/scripts/graph.mjs analyze <tasks.json>
```

## Step 3 — compute readiness + select (helper)

Readiness is computed **in-planner** from the roadmap's machine-readable status (a task is ready iff every
`dep` is `done`), NOT pushed into `graph.mjs`:

```bash
node .claude/skills/sprint-planner/planner.mjs select <input.json> [--capacity N] --json   # wraps planner.mjs -> selectSprint
```

`selectSprint({tasks, statusById, capacity})` → `{features, excluded}`:
- `features` — the ready, cohesive (same-epic-preferred) subset up to `capacity`, each carrying
  `{id, done_record, edge_tests, wiring_test}` (the `sprint-plan` manifest feature shape).
- `excluded` — unready tasks as `{id, blockedBy:[unmet prerequisite ids]}`.

## Step 4 — emit the proposal + self-check

Render the selected features into a `sprint-plan` manifest (`{sprint, features:[…]}`). Validate the shape
with `sprint-plan`'s `validateManifest`, and self-check completeness with `sprint-oracle`'s `runOracle`
(done-record + edge/wiring tags) once the tickets have tagged tests. Write the proposal to
`.claude/state/sprint/<name>/proposal.json`.

## Step 5 — propose only; the human confirms

Present the proposed sprint (features + excluded-with-blockers). **Do not start work, stage, or commit
anything** (AC-005). The human confirms or edits the task-set; then `/triage` routes it (usually to the
`power` track). Decisions stay in main context (Article II).

## Constraints

- **Read-only.** The only write is the proposal artifact. No source, no git.
- **No autonomous selection into a build.** Proposing ≠ starting. The human is the gate before `/triage`.
- **Reuse, don't rebuild.** `gatherSync`, `graph.mjs`, `validateManifest`, `runOracle`, `planner.mjs` —
  compose them; do not reimplement roadmap parsing, graph ordering, or the oracle.
