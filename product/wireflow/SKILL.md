---
name: wireflow
description: >
  Create OR review a wireflow — the artifact BETWEEN user journeys and wireframes. It maps whole
  journeys into swimlane flows with high-level navigation (screens, decisions, system/agent steps)
  while keeping Jobs-To-Be-Done at the core, WITHOUT deep UI. Use whenever the user wants to "map
  the flows", "make/build a wireflow", turn journeys / JTBDs / a spec / a live prototype into flows,
  or put every journey on one board against shared owner lanes — even if they never say "wireflow".
  ALSO use it to REVIEW or critique an existing wireflow (image, FigJam, or description). In the
  A-Team pipeline this is a definition-phase skill: output lands in docs/features/<slug>/briefs/wireflow/
  with jobs consumed by id from docs/product/jtbd/; pipeline mode derives the method decisions and
  highlights the riskiest at the gate, standalone mode runs the full grill. CREATE generates verified
  SVG/HTML (self-checked by rendering and Reading its output) in a horizontal per-journey OR
  shared-matrix layout, and can rebuild in FigJam. Do NOT use for high-fidelity wireframes, UI design,
  customer journey maps, architecture/data-flow diagrams, or a sitemap.
metadata:
  version: 1.2.0
  owner: Alvaro Bezerra
  provenance: ported 2026-07-24 from product-craft wireflow v1.1.0 (github.com/ABZerra/product-craft) and adapted to the A-Team contract — briefs/ output home, JTBD-by-id anchoring, derive-mode for the definition phase.
---

# Wireflow

A **wireflow** is the deliverable that sits *between* user journeys and wireframes. It maps
whole journeys into flows with high-level navigation (pages/screens, decisions, system steps,
external stubs, agent nodes) **without** deep UI, keeping the **JTBDs at the core**. The term
is NN/g's (Page Laubheimer, 2016): a wireflow combines wireframe-style page nodes with a
simplified flowchart. It is the *right* tool for apps with **few pages that change dynamically**
(agent-first SPAs, task-heavy tools) and the *wrong* tool for many static pages — if the product
is mostly static content, say so and suggest a sitemap or plain user-flow instead.

This skill is **context-agnostic**: it carries the *method* and the *build engine*, and learns
the project specifics per run — by grilling the human (standalone) or by deriving them from the
context layer (pipeline).

## Place in the A-Team pipeline

Definition-phase skill. Output home: **`<target>/docs/features/<slug>/briefs/wireflow/`** —
`board.json` (the spec — source of truth and breadcrumb; the render is regenerable from it),
`wireflow.html` + SVG(s) (the deliverable), PNGs (verification copies, kept so gate reviewers
see what you saw). Per-feature artifact: overwrite cleanly on revision. Commit per run:
`docs(<slug>): wireflow`.

- **Jobs by id.** JTBDs come from `docs/product/jtbd/` — cite `[[NN-<slug>]]` with verbatim
  headlines in journey headers and the JTBD × Journey matrix. Never mint or reword a job; a
  journey that serves no existing job is evidence a job is missing → `TBD`, route to
  `jobs-to-be-done`.
- **Two interaction modes, one method:**
  - **Standalone (human present)** — run the full Movement-1 grill below, one decision at a time.
  - **Pipeline (definition phase — draft + review, no interrogation)** — lock the method
    decisions yourself from `prd.md`, the jobs, and `context.md`, using the recommended defaults
    in `references/method-decisions.md`. Then make the gate do the grill's work: the delivery
    explicitly surfaces the two riskiest calls — **journey set** and **spine** — as headlined
    items for correction via the revise loop. Never block waiting for answers mid-phase.
- Consumes `prd.md` (scope, stories by job) when definition ran first; can also run
  journeys-first from jobs + context alone.

## Mode 0 — Create or Review? (decide first)

- **CREATE** (default) — build a new wireflow from journeys / JTBDs / a spec / a live prototype.
- **REVIEW** — critique an *existing* wireflow (an image, a FigJam board, a description, or a
  spec) against the method, and hand back a verdict + concrete fixes.

If the user's intent is ambiguous ("look at my wireflow"), ask which they want. Artifact + "what's
wrong" = REVIEW; raw material + "make flows" = CREATE.

---

## Creating a wireflow

Work in two movements: **(1) lock context + method decisions — grilled or derived per the mode
above; (2) run the generate → rasterize → Read → iterate pipeline** until every journey renders
cleanly, then deliver.

### Movement 0 — Ground yourself first
Skim whatever sources exist so your decisions (or grill questions) are sharp: the context layer
(`context.md`, jobs, `ateam-plan.md`/`research-plan.md`), `prd.md` + stories, a **live prototype** and
its real routes, existing user journeys. Reading real screens/routes is what lets own-screen
nodes link to live routes instead of screenshots (which go stale).

### Movement 1 — The decisions (grilled standalone; derived in pipeline)
The full checklist with the reasoning behind each locked decision is in
**`references/method-decisions.md`** — read it before starting and follow its order. Briefly:

1. **Journey set** — the unit is a *cross-cutting, actor-anchored journey* (not
   one-flow-per-epic). JTBDs are **many-to-many** with journeys. Propose a small set that covers
   the whole product (every job and every scoped item embodied somewhere).
2. **The spine** — which single journey carries the core JTBD and goes *deeper* than the rest.
3. **Node taxonomy** — own screen · external-site stub · external-product stub · system/engine
   (no UI) · decision · agent · start/outcome · stop. Granularity: **one node = one page, one
   page-state, or one system step** — never below page-block level.
4. **Lanes** — swimlanes where **lane = owner**; shape/colour = node type. Cross-lane arrows tint
   with the landing lane's colour; lane labels carry a matching tick.
5. **Branches** — only branches that change the page path or encode a locked decision/edge case.
   **Locked cuts become visible Stop nodes.** Omit cosmetic/deferred branches.
6. **Coverage without labels** — every requirement embodied by a node/branch; initiatives never
   labelled on the board; no MoSCoW/roadmap metadata. Coverage, not clutter.
7. **JTBD anchoring** — per-journey header (actor + job id served) with **Start = the struggle**
   and **Outcome = the job done**, plus a board-level JTBD × Journey matrix (ids + headlines).
8. **Deepen inline, never split** — fold detail into the *same* journey band; no separate "L2".
9. **Orientation** (see `references/orientation.md`) — **horizontal** (default; the working
   deliverable, room for a deep spine) vs **matrix** (stakeholder overview; owner rows × journey
   columns). Recommended: build horizontal, offer matrix as a companion.
10. **Output target** — SVG + combined HTML always; **offer** the native editable **FigJam**
    rebuild as an add-on (`references/figjam-rebuild.md`).

Keep a running written summary of the locked decisions; in pipeline mode this summary ships with
the gate presentation (the breadcrumb of what was derived and why).

### Movement 2 — The build pipeline (the reliability core)
Do **not** build straight onto a FigJam board via the API first — a real board is too large for
the design tool to render back, so you'd be building blind. Instead:

1. **Write a compact board spec** (`board.json`) from the locked decisions — schema and worked
   examples: **`references/spec-schema.md`**.
2. **Generate** with the bundled engine:
   `python scripts/wireflow.py board.json --out docs/features/<slug>/briefs/wireflow --layout horizontal --rasterize`
   (or `--layout matrix`). It emits the SVG(s), a combined `wireflow.html` (deliverable + legend +
   JTBD × Journey matrix), and PNGs.
3. **Read the PNGs.** You *see your own output* and catch overlaps, out-of-lane nodes, and glyph
   problems **before anyone else does**. Verify **every** journey — never skip; this loop is what
   makes wireflows reliable.
4. **Iterate** on the spec (rarely the engine) until clean — `references/layout-engine.md`.
5. **Deliver** the combined HTML + SVG(s). Own-screen nodes carry `href` to live routes.
6. **If requested, rebuild natively in FigJam** (`references/figjam-rebuild.md`).
7. **Hand off to `page-brief`.** The wireflow owns the page set, the journey↔page linkage, and
   **where each job enters a screen** — that entry-point detail is flow-level, so it lives here
   and the page-brief no longer carries it. Make sure journey steps actually say where a job
   picks up, not just that the page is traversed. Offer: *"Wireflow's done — want to spec each
   page's requirements next?"*

---

## Reviewing a wireflow

Critique against the method — don't redraw unless asked. Be a sharp, specific reviewer.

1. **Take in the artifact.** Image/rasterized board → Read it; FigJam → screenshot/export;
   description or spec → read it. Note what you can and can't see.
2. **Score against `references/review-criteria.md`**: is it actually a wireflow (vs a flowchart
   or wireframes)? Journeys actor-anchored and cross-cutting? Clear spine? Node taxonomy
   consistent, system boundary legible? Lanes = owners? Locked cuts as Stop nodes? Coverage
   embodied without labels? JTBDs anchored (struggle → job done)? Depth inline? Orientation fits?
3. **Return a structured verdict**: **Verdict** (one line + the single biggest issue) ·
   **Strengths** · **Findings** (each tied to a method point, ordered by impact, with the fix) ·
   **Fastest wins** (2–3).
4. **Offer to apply the fixes** by switching to CREATE and regenerating (grill only the gaps).

---

## Guardrails to hold throughout
- **Never label initiatives; embody them.**
- **Deepen inline, never split** into a separate L2 diagram.
- **Always verify by rasterize → Read before showing anyone.** No blind delivery.
- **Draw locked cuts as Stop nodes** — the deliberate non-path is documentation.
- **Own-screen nodes link to live routes**, not screenshots.
- **Keep the spine the human screen-journey.** Backend enters as system nodes and decision
  diamonds between screens — full coverage without becoming a data-flow diagram.
- **Jobs are consumed, never minted** — ids + verbatim headlines from `docs/product/jtbd/`.

## What ships in this skill
- `scripts/wireflow.py` — the spec-driven layout engine (horizontal + matrix, auto-sized lanes,
  geometry routers, wrapping edge labels, glyph sanitising, combined-HTML + JTBD×Journey matrix,
  optional PNG).
- `references/method-decisions.md` — the decision checklist: each decision + *why* it's locked.
- `references/orientation.md` — horizontal vs matrix: when each wins.
- `references/spec-schema.md` — the board JSON schema + worked examples.
- `references/layout-engine.md` — layout rules and how to debug a bad render.
- `references/pipeline.md` — the end-to-end build pipeline checklist.
- `references/review-criteria.md` — the REVIEW rubric.
- `references/figjam-rebuild.md` — native FigJam mechanics (load only for an editable board).

## Strict versus draft rendering

Rendering defaults to strict validation. Use `--validate-only` for a source-only
check and explicit `--permissive` for incomplete drafts with visible warnings.
Unknown edge/job/page references must be fixed before phase completion. Keep
canonical job IDs, stable node/edge IDs, and screen `pageId` values in board.json.
See `<harness>/runner/ARTIFACTS.md` for the cross-file gate. The validator requires
the full harness checkout and Node 20+; set `ATEAM_NODE` if needed.
