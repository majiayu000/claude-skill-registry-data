---
name: receive-brief
description: Use this skill when the user receives an externally-authored, multi-feature product brief -- a PRD, a solution handoff, a requirements packet -- and needs to turn it into shippable specs. Triggers on "receive a brief", "decompose this PRD", "we got a product brief", "break this handoff into specs". Elicits the load-bearing fields without mandating a schema, decomposes by shippability, and executes each slice through new-spec then work-loop. Do NOT use to author a single feature from scratch (use new-spec) or to record a decision (use new-adr).
---

# Skill: receive-brief

Receive a product brief — a PRD, a solution handoff, a packet of work product
handed from someone else — and route it into delivery. A brief spans several
features and carries the *what/why*; a spec is one feature and carries the
*how*. `new-spec` authors one feature; this skill is the inbox a level above
it: **elicit** what the brief is missing, **decompose** it into
independently-shippable slices, and **execute** each slice through the normal
`new-spec` → `work-loop` pipeline. The brief becomes a live tracker whose
coverage rolls up from the specs it spawned.

## When to invoke

Invoke when the unit of work that arrives is **bigger than one feature** and
authored by someone other than the implementer — product hands engineering a
brief. If the user is authoring a single feature themselves, that's `new-spec`,
not this skill. If they want to record a decision already made, that's
`new-adr`. The tell is multiplicity: one outcome, several features, no home.

A brief lives at `docs/product/briefs/<slug>.md`. Copy the bundled template
(your installer places a `_template.md` in that directory) and fill what you
have. The shape is a guide, not a gate — see the Elicit stage.

## Two shapes, one toggle

The only structural choice is whether the brief carries **user stories**:

- **Shape A — no stories.** You derive spec boundaries from the Outcome and
  Scope, and surface the cut for confirmation. Coverage is **spec-granular**
  ("is `password-reset` shipped?"). Stories still exist — they're written as
  each spec's acceptance criteria when the spec is authored.
- **Shape B — story list.** The brief lists stories with ids (`US-1`, `US-2`,
  …). Decomposition is *grouping stories into specs*. Each satisfying
  acceptance criterion carries a `Satisfies: US-n` marker, so coverage is
  **story-granular** ("US-2 → `password-reset` AC3 → shipped"). A story too
  big to fit one feature-sized spec is an epic — flag it for splitting.

Both shapes run the same three stages below. The toggle changes traceability
granularity, not the pipeline.

## Procedure

### 1. Elicit — meet the brief where it is

Ingest whatever the user has: a pasted document, a file, a link, or a verbal
sketch. Then fill the brief template by **conversation**, not by rejection.

- **Insist on only the load-bearing fields: Outcome and Scope.** Without the
  outcome you can't tell whether a slice serves the brief; without scope (and
  non-goals) the decomposition sprawls. Ask for these until you have them.
- **Offer the rest; never require it.** Success metrics, appetite, and stories
  improve the cut but are not gates. Suggest a default ("no metrics given — I'll
  propose p95 latency and ticket volume; correct me") rather than blocking.
- **Surface gaps; never invent.** If the brief is silent on something
  load-bearing, say so and ask. Do not fabricate an outcome or quietly drop a
  requirement to make the brief parse.
- **Never mandate a schema.** A half-formed brief is normal input. The template
  is a prompt sheet, not a form to be rejected for missing sections.

Record the result in `docs/product/briefs/<slug>.md`. Carry the optional
`Epic:` pointer if this repo's work is one slice of a larger cross-repo effort
— that pointer is the *only* nod to the wider epic; you own this repo's slice
and nothing above it. Likewise carry the optional `parent-intent:` pointer if
the brief arrived as a per-component slice of a larger product intent — an
upward provenance pointer you carry but never interpret, exactly like `Epic:`.

### 2. Decompose — cut by shippability, then surface the cut

Cut the brief into slices, each of which is **independently shippable and
independently testable** — a feature `work-loop` can carry end to end. This is
the shippability test, **not** a component or layer split: "auth service" and
"auth UI" are not two slices unless each ships and tests on its own.

- In **Shape A**, derive slice boundaries from Outcome + Scope.
- In **Shape B**, group the stories into slices; each slice becomes one spec.
- **Flag any epic-sized story** — one that can't fit a single feature-sized
  spec — for splitting before you scaffold. Ask before treating it as one spec.
- **Flag any outcome no slice covers** as a gap, and surface it. Don't silently
  drop an outcome to make the decomposition tidy.

**Surface the proposed cut and wait for confirmation before scaffolding any
spec.** Present the slices, what each delivers, and (Shape B) which stories
each carries. The decomposition is judgment; the human signs off on it.

### 3. Execute — scaffold, back-link, hand off

For each confirmed slice, in dependency order:

1. **Chain `new-spec`** to scaffold the slice's `spec.md` + `plan.md`. Pass the
   slice's outcome and scope so `new-spec`'s assumption-surfacing starts from
   the brief, not a blank page. `new-spec`'s **shape/stack-derivation step**
   runs as part of that chain — it sets each slice's `Shape:` (the brief's
   framing usually decides it) and derives the stack the plan's `## Design (LLD)`
   names; pass the brief's stack context so it conforms rather than re-elicits.
2. **Stamp the `Brief:` back-link** on the derived spec — set it to this
   brief's slug. In **Shape B**, also stamp `Satisfies: US-n` on each
   acceptance criterion that satisfies a story, so the trace is bidirectional.
3. **Add a row to the brief's Spec map** for the new slice (the Status column
   is auto-derived — leave it to the lint; do not hand-write it).
4. **Hand off to `work-loop`** to build the slice. The brief is thus
   *executable*: brief → (spec, plan) × N → work-loop.

You don't have to scaffold every slice at once — a brief can grow its Spec map
over time as slices are picked up. A spec may even predate its brief; the
`Brief:` back-link is what ties them together, not directory nesting.

## Coverage — auto-rolled-up, never hand-maintained

The brief's **Spec map** answers "is this brief delivered?" and stays current
on its own. The bundled coverage lint at `scripts/lint-brief-coverage.py`
reads every spec's `Status:` field, follows the `Brief:` back-links, and rolls
each brief's map up from its children:

- A brief whose every mapped spec is `Shipped` reports **delivered**.
- A brief whose map has no mapped specs reports **not delivered** — an empty
  map is never vacuously delivered.
- A spec that back-links a brief but isn't in that brief's map is reported
  **untracked** (informational) — add the row; it's not an error.

Run it after a slice's status changes; wire it into your gate if you want it
enforced. **Never hand-edit the Status column** — a status written by hand
drifts the moment a spec ships, which is the exact failure this rollup avoids.

See `examples/` for two worked briefs — a no-stories outcome brief (Shape A)
and a story-list brief (Shape B), each with a populated Spec map.

## Anti-patterns to refuse

- **Mandating a schema / rejecting a half-formed brief.** The shape is a guide.
  Elicit the load-bearing fields; offer the rest. A brief that arrives missing
  metrics is normal, not invalid.
- **Decomposing by component or layer instead of shippability.** "Backend,
  then frontend" is not two slices; "the slice that lets a user reset their
  password, end to end" is. If a slice can't ship and test on its own, it's not
  a slice yet.
- **Scaffolding before the cut is confirmed.** The decomposition is the
  judgment call the human most needs to see. Surface it; don't present N specs
  as a fait accompli.
- **Building a cross-repo coordination hub.** You own this repo's slice. Point
  upward with the optional `Epic:` pointer; do not reimplement a tracker.
- **Hand-maintaining the coverage map.** The Status column is derived. Editing
  it by hand reintroduces the drift the lint exists to prevent.
- **Cramming a multi-feature brief into one oversized spec.** That breaks the
  one-feature sizing rule and the per-spec `work-loop`. If it's several
  features, it's several specs.
