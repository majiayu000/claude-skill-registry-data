---
name: spec-fixture
description: "Author a completed-spec fixture — a seeded intent graph plus a believable four-phase interview transcript — for a brunch feature, so it can feed any downstream tooling that consumes a completed spec or dogfood the UI. Use when you need a real completed specification in .brunch/brunch.db for testing or demo: pick a feature from memory/SPEC.md (or a free description), choose a stress profile (coverage|clean), and produce a registered scenario seed + an interview-questions doc that match exactly."
argument-hint: "[feature: SPEC.md req # or description] [profile: coverage|clean]"
---

# Spec Fixture

Turn one brunch feature into a **completed-spec fixture**: a seeded intent graph
(requirements, criteria, supporting knowledge, typed edges) with all four
interview phases closed, plus a believable interview transcript. The fixture is a
real `specification` row in `.brunch/brunch.db`, usable as input to any downstream
tooling that consumes a completed spec, or for dogfooding the workspace UI.

## Input

`$ARGUMENTS` = a feature + optional profile.

- **Feature**: a `memory/SPEC.md` capability-requirement number (e.g. "req 34–36")
  or a free-form description.
- **Profile**: `coverage` (default — maximize graph coverage / stress downstream
  consumers) or `clean` (tidy demo fixture). Either way, always produce a
  believable transcript.

## Use when

- You need a real completed spec to exercise downstream tooling that consumes one
  (plan generation, the orchestrator) end-to-end.
- You want a self-referential demo spec (brunch speccing a brunch feature).
- You want to dogfood the interview/graph UI against realistic data.

Not for: editing the product schema, building the downstream tooling itself, or
one-off throwaway graphs that don't need to persist.

## Why this works (read before designing)

- **Downstream tooling reads the graph snapshot, not the transcript.** It consumes
  `knowledge_item` + `knowledge_edge`; turn prose is irrelevant to it. So **graph
  fidelity is for the consumer; the transcript is for the UI/demo**. Get the graph
  exactly right; make the transcript believable.
- **Execution order is not spec truth.** The observer captures *epistemic* deps
  (assumptions/decisions/constraints point *at* requirements), never req→req
  execution order. Any downstream ordering is *synthesized* from requirement
  content. So a faithful fixture seeds **zero req→req `depends_on`** and lets the
  content imply the order.
- **Two unrelated "impact"s.** Turn `impact` (`high|medium|low`, read from
  `turn.impact`, defaults to `low`) is the interviewer's consequence hint. The
  edit-impact tier (`none|soft|hard`) is a separate edit-time cascade signal. This
  skill sets the *turn* impact; it does not touch the cascade tier.

## Method

### Defining the content (optional `ln-*` aids)
The fixture *is* an elicitation artifact, so the repo's `ln-*` elicitation skills
can shape its content during steps 1–3. Use each skill's **output** to populate the
fixture graph — do **not** let them write `memory/SPEC.md` / `PLAN.md`, which are
dev-layer planning, not this product-layer fixture data.
- **ln-grill** — pressure-test the feature into goals, constraints, and a thorough
  requirement set (the grounding/design content + supporting nodes).
- **ln-disambiguate** — turn vague criteria into concrete behavioral acceptance
  criteria (sharper `criterion` nodes).
- **ln-oracles** — design which criteria verify which requirements (the `verifies`
  edges) and the "expected downstream behavior" assertions.
- **ln-scope** — frame each buildable requirement as a slice with target behavior
  and acceptance criteria, mirroring requirement → `verifies` → criterion.

### 1. Frame the feature
Name it `snake_case`. Decide `mode` (greenfield | brownfield) and delivery posture
(incremental feature | end-to-end build). Brownfield + incremental is typical for
a feature on existing code, and routes cook output to `<dir>/.brunch/cook/plan.yaml`.

### 2. Design the intent graph
Enumerate nodes and edges before writing code. Nodes: `requirement` and
`criterion` (the buildable spine) plus supporting `goal` / `term` / `context` /
`constraint` / `decision` / `assumption`. Edges are typed and **must satisfy the
relationship policy** — see [references/seed-pattern.md](references/seed-pattern.md)
for the canonical direction table and the guard.

Apply the profile:

- **`coverage`** — bake in deliberate stressors so a downstream consumer's full
  behavior gets exercised (graph read, order synthesis, validation):
  - Full `verifies` coverage of every *buildable* requirement.
  - ≥1 criterion that verifies **two** requirements.
  - ≥1 requirement verified by **multiple** criteria.
  - ≥1 **non-buildable, constraint-phrased requirement** (typed `requirement`,
    phrased as a "must not" / invariant) with **no** `verifies` edge — reproduces
    the real data-quality case a validation pass must catch.
  - **Zero req→req `depends_on`** — force downstream ordering to be synthesized
    from content; make the content imply a clear order.
  - ≥1 adversarial epistemic edge (e.g. `refines` req→req, or
    assumption/decision/constraint → requirement) that a graph read must **ignore**
    for ordering.
- **`clean`** — well-ordered, every buildable requirement verified, no
  non-buildables, no adversarial edges. Optimized for a smooth demo run.

### 3. Write the interview-questions doc
`docs/fixtures/<name>-interview.md`. It is the source-of-truth and the capture map
for the seed. Include:
- A "Fixture fidelity" note (transcript reproduced verbatim from the seed).
- The four-phase transcript (grounding → design → requirements → criteria) as
  believable Q&A, each grounding/design question tagged with its `impact`.
- The **capture map**: node inventory (ref, kind, content) + edge inventory
  (canonical for the seed).
- **Expected downstream behavior**: assertions for how a consumer reads, orders,
  and validates the graph, so the end-to-end test has a target.

Assign `impact` by the rubric *"how much the answer shapes downstream choices"*
(`src/server/prompts/interviewer-grounding.md`): strategic forks, the core goal,
and binding constraints are `high`; localized design choices are `medium`;
assumptions-to-validate are `low`. Don't make everything `high` — the spread is
the signal.

### 4. Author the seed
Put `seedAccepted<Feature>Spec(db, projectId)` in its **own file**
`src/server/fixtures/scenarios/<name>.ts` (one fixture per file — keeps the
`scenarios.ts` registry lean), then import it into `src/server/fixtures/scenarios.ts`
and register a `<name>-all-phases-closed` scenario there. Mirror any existing
all-phases-closed scenario seed. The seed must: build real grounding/design Q&A
turns (set turn-level `impact`), capture each supporting item at the turn that
elicits it, accept the requirements + criteria reviews, confirm all four phase
outcomes, then add the policy-guarded edges. Full code skeleton and the
relation-policy table: [references/seed-pattern.md](references/seed-pattern.md).

### 5. Load + verify
- `npm run fix` then `npm run check` — must be green.
- Verify the graph against a fresh in-memory DB (counts by kind, edges by
  relation, four phases confirmed, and the profile's stressors). Use the
  verification script template in the reference file; delete it after.
- Load into the real DB. Re-seeding is **additive**, so to avoid duplicate specs,
  **delete-then-reseed** (FK-off across spec-scoped tables — snippet in the
  reference) before `npm run seed -- <name>-all-phases-closed`.

### 6. Reconcile
The doc transcript must match the seed **verbatim** — questions, answers, impacts,
and captures. If you simplify the seed (e.g. plain Q&A instead of preface cards),
update the doc to match, and vice versa. Note any folding (e.g. edge-styling intent
folded into a requirement) in the doc's fidelity note.

## Verification checklist
- [ ] `npm run check` green.
- [ ] In-memory seed asserts expected node/edge counts and the profile's stressors.
- [ ] All four phase outcomes confirmed.
- [ ] Every buildable requirement has ≥1 `verifies`; non-buildables have none.
- [ ] Every edge passes `supportsKnowledgeRelationship`.
- [ ] Doc transcript matches the seeded turns verbatim (incl. per-turn impact).
- [ ] Real DB has exactly one spec for this feature (no stale duplicates).
