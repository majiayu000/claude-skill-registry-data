---
name: author-epics
description: Draft /grill's epic cut for one REALIZED slice — the user-testable delivery increments the delivery pipeline picks up. Reads the slice's hub from the spine (its functionalities' grounding docs `functionality.md` + the spine profile) AND all SEVEN lens grounding docs (quality, ux, agentic, marketing, architecture, run, measure — the solved design), then cuts epics by the user-testability grain — when an epic is delivered, a user can open the product, do something, and see it work. For EACH epic it drafts a spine `epics` index entry PLUS a rich `epic.md` grounding doc, referencing the slice's functionalities by spine id, never copying functionality or lens content. Orders the cut (explicit acyclic dependencies; the first epic stands alone) and records explicit deferrals for any slice functionality not cut this run. Also applies revision directives from /grill's grilling rounds to the existing cut. Under direct-model-write (ADR 026) it writes ONLY the per-node docs (each `epic.md`, and the slice's `deferrals.yaml`) straight to the live model, and emits the epics-index delta (the spine `epics` entries) as structured data in the epics-manifest — it NEVER writes `_spine.yaml`, `profile.yaml`, or `decisions`. The generative work for the /grill play.
version: 0.3.0
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, Glob
---

# author-epics

Turns one **realized** slice into its **epic cut** — the ordered set of user-testable
delivery increments that `/start` will pick up one at a time. A slice is a vertical product
increment whose design the seven realize lenses have already solved; its **hub** is the
union of its functionalities' grounding docs (`functionality.md`) plus the product profile
(read from the spine). The epic is the delivery grain below the slice, and its rule is
single: **when this epic is delivered, a user can open the product, do something, and see
it work.**

An epic may thread one or several of the slice's functionalities; a big functionality may
yield several epics. What an epic may NOT be is internal-only — plumbing, schema setup, an
API with no surface — unless that work rides inside an epic that ends at something a user
can exercise. Cut vertically, not horizontally.

Each epic is **two artifacts**: a structured **spine `epics` entry** (the machine index the
delivery pipeline reads) and a rich **`epic.md` grounding doc** (the human-readable cut a
builder picks up). This skill writes the `epic.md` docs straight to the live model and emits
the spine `epics` entries as structured manifest data; it never writes the spine itself.
/grill grills the cut (cited push-back, tension rounds), the human approves, and /grill's
keyed persist script turns the manifest's epics-index delta into the spine `epics` writes.

## Write discipline — direct-model-write containment split (ADR 026)

This skill is the LLM worker in a direct-model-write play. Per
`standards/rules/direct-model-write.md` it obeys the **containment split**, and this is
mandatory:

- It writes ONLY the per-node grounding docs — each epic's `epic.md`, and the slice's
  `deferrals.yaml` — **straight to the live model** under the slice's `epics/` home. There
  is no `draft/` tree.
- It **NEVER** writes any shared model file: not `_spine.yaml`, not `profile.yaml`, not
  `decisions/`. The spine `epics`-index mutation is the job of /grill's deterministic keyed
  persist script, which reads this skill's manifest.
- The spine `epics` entries it used to write into a draft `_spine.yaml` are now emitted as
  **structured data in `epics-manifest.yaml`** (a non-model STM artifact). The keyed persist
  script merges those entries into the live spine `epics` index in place, keyed to the slice.

Because the LLM only ever writes separate doc files, /grill's file-level scoped guard is
sufficient for this skill's blast radius, and node-level containment inside the shared spine
(only the `epics` index changes; an epic delivery already owns is untouched) is preserved by
the keyed script.

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| `slice_ref` | yes | The slice, `{domain}/{slice-id}`. |
| `slice_file` | yes | The slice record path (read-only) — its `functionalities` are the set to cover. |
| `functionality_groundings` | yes | The resolved `functionality.md` grounding-doc paths for the slice's functionalities (the hub), from the readiness gate, each with its spine `functionality_ref`. Their intent/rules/acceptance shape each epic's context and acceptance. |
| `lens_dir` | yes | The slice's lens folder (read-only) — all SEVEN lens grounding docs (`quality.md`, `ux.md`, `agentic.md`, `marketing.md`, `architecture.md`, `run.md`, `measure.md`). The solved design the cut must honor. |
| `spine` | yes | The live `_spine.yaml` (read-only) — the profile (the bars acceptance must respect) and the functionality entries the `functionality_ref`s resolve against. Read only; never written here. |
| `product_base` | yes | The product model root. Read the spine + lenses, and WRITE each epic's `epic.md` and the slice's `deferrals.yaml` in place under the slice's `epics/` home at `{product_base}product-os/{domain}/slices/{slice-id}/epics/`. Only the epic docs — never a shared file, never another slice's docs. |
| `manifest_path` | yes | Where to write `epics-manifest.yaml` (STM, non-model) — carries the epics-index delta (the spine `epics` entries) + deferrals as structured data for the keyed persist script. |
| `directives` | no | Path to a revision-directives file from a grilling round. When present, revise the existing cut (the live `epic.md` docs + the manifest) per the directives instead of cutting fresh. |

## Procedure

1. **Read the hub + the seven lenses.** Load the slice record (its functionalities and
   outcome), every functionality's `functionality.md` (what it does, rules & behavior,
   acceptance criteria), the spine profile (its bars), and all seven lens `.md` docs. /grill
   is the reconciliation point — unlike a realize lens, this skill reads everything the slice
   declared.

2. **Cut by user-testability.** Walk the slice outcome and the functionalities and ask: what
   is the smallest increment that ends at something a user can open, do, and verify? Each
   such increment is an epic. Thread whatever functionalities it needs (by spine
   `functionality_ref`); pull the necessary internal work (migrations from `run.md`,
   components from `architecture.md`, gates from `quality.md`, the surface from `ux.md`) INTO
   the epic that surfaces it — never out as a standalone internal epic.

3. **Write each epic's `epic.md` grounding doc, in place.** Write it straight to the live
   model under the slice's `epics/` home
   (`{product_base}product-os/{domain}/slices/{slice-id}/epics/{epic-slug}.md`). Conform to
   the epic template
   (`standards/schemas/product-os/grounding/epic.md`) — H1 `# Epic: <title>` and the sections
   `Intent (goals)`, `Constraints`, `Failures`, `Expectations / success`, `Context (persona /
   systems / scope)`, `Outcome`, `User check` (the one-line open/do/verify, concrete and
   distinct per epic), `Surface`, `Delivers — functionalities (linked)` (the slice
   functionalities this epic delivers, by spine id), and `Acceptance criteria` (each a
   Given/When/Then observable behavior; quality-lens gates and profile bars surface here as
   the bar the behavior must meet). Self-explaining prose per the content standard — the play
   runs the linter and the judge over every `epic.md`.

4. **Record each epic's spine entry in the MANIFEST.** In `epics-manifest.yaml`'s `epics`
   list — NOT in `_spine.yaml` — record each entry: `id`
   (`e-<n>-<slug>` or a stable id), `slug`, `slice_ref`, `status: ready`, `order` (unique
   1..n), `depends_on` (the ids of other epics in this cut it depends on — acyclic; the first
   epic has none), `functionality_refs` (the spine functionality ids it delivers),
   `user_check` (the concrete one-line open/do/verify, distinct per epic — the validator
   requires it on every entry), a `surface` block (`{type, human_run_target, must_open[]}` per
   surface-contract.md — `type` from web_dashboard | server_api | cli | library |
   service_read_model), `surface_verified: false`, `issue_ref: null`, and `doc` (the pointer
   to its `epic.md`, relative to `product-os/`). These are manifest fields the keyed persist
   script merges into the live spine `epics` index; you never write them to `_spine.yaml`
   yourself.

5. **Reference, never copy.** `functionality_refs` and `Delivers` point at the slice's
   functionalities by spine id; the functionality and lens content stay where they live. No
   functionality body, ICE, or lens content is pasted into an epic.

6. **Order the cut.** Explicit `depends_on` between epics (within this slice only), acyclic,
   `order` 1..n unique, and the first epic stands alone — independently deliverable.

7. **Defer explicitly.** Any slice functionality not threaded by any epic this run is written
   to the slice's `epics/deferrals.yaml` (in place, in the live model) with a recorded reason,
   AND its id is recorded in the manifest's `deferrals` list. Nothing is silently dropped.

8. **On revision rounds** (`directives` present): apply each directive to the existing cut —
   split, merge, re-scope, re-order, rewrite acceptance — rewriting the affected live
   `epic.md` docs in place and updating the manifest's `epics`/`deferrals`, keeping every rule
   above intact and leaving the rest of the cut untouched.

## Output — live docs + the manifest

Written straight to the live model (no draft tree):

```
{product_base}product-os/
  {domain}/slices/{slice-id}/epics/
    {epic-slug}.md                                # rich epic grounding doc (epic template), one per epic
    deferrals.yaml                                # always written, even when empty (deferrals: [])
```

Plus the manifest (STM, non-model) at `manifest_path`:

```yaml
epics:                                            # epics-index DELTA — persist merges into _spine.yaml `epics`
  - id: e-1-open-dashboard
    slug: open-dashboard
    slice_ref: dom/slice-x
    status: ready
    order: 1
    depends_on: []                                # first epic stands alone; acyclic within this slice
    functionality_refs: [func-a]
    user_check: A user opens the dashboard and sees their data render   # concrete, distinct per epic
    surface: { type: web_dashboard, human_run_target: open the dashboard, must_open: [the app] }
    surface_verified: false
    issue_ref: null
    doc: dom/slices/slice-x/epics/e-1-open-dashboard.md
deferrals: [func-z]                               # functionality ids deferred this run (reasons live in deferrals.yaml)
coverage: { func-a: [e-1-open-dashboard] }        # functionality -> epics that deliver it
grounded_in: "the slice hub + seven lenses"       # the design material honored
```

Return the live doc paths + the `epics-manifest.yaml` path — paths, never inline content.

## Boundaries

### NEVER
- Write `_spine.yaml`, `profile.yaml`, or `decisions/` — emit their delta as manifest data;
  write only the `epic.md` docs and `deferrals.yaml` to the live model, under the slice's
  `epics/` home. Never touch the slice record, a lens, a functionality's grounding, another
  slice's docs, or any shared file.
- Cut an internal-only epic — every epic ends at a `User check` a user can actually perform.
- Copy functionality or lens content into an epic — reference functionalities by spine id.
- Leave a slice functionality unmapped — every one is delivered by an epic or deferred with a
  reason.
- Mint a dependency on an epic outside this slice, a cycle, or a first epic that depends on
  anything.
- Set any status but `ready`, or any `issue_ref` — delivery owns the lifecycle.

### ALWAYS
- Ground each epic's context and acceptance in the functionality groundings, the seven
  lenses, and the profile — the cut honors the solved design; it does not redesign.
- Give every epic a concrete, distinct `User check`.
- Make every `epic.md` clear the content standard (it is linted and judged).
- Write `deferrals.yaml` to the live model, even when empty, and record its ids in the manifest.
- Return the live doc paths + the `epics-manifest.yaml` path, not the contents.
