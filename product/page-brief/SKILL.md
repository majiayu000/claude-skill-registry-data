---
name: page-brief
description: >
  Create OR review a page-brief — the artifact BETWEEN a wireflow and the full PRD. It turns each
  unique page/screen of a product into documented requirements TIED TO JOBS: a self-contained board
  card per page (what the page is accountable for, the job-tagged checklist of what it must let you
  do, the journeys it appears in, what it connects to, and the acceptance criteria that say how you'd
  know it's right). It is the "PRD per page", not a sitemap — and it stops ABOVE the screen: no
  components, no layout, no hierarchy. Use whenever the user wants to "spec the pages", "document each
  screen", turn a wireflow + live design into per-page requirements, or asks "what does this page need
  to do / which jobs pass through it" — even if they never say "page-brief". Natural NEXT STEP after
  the wireflow skill. ALSO use it to REVIEW an existing page-brief / screen catalog. In the A-Team
  pipeline this is a definition-phase skill: output lands in docs/features/<slug>/briefs/pages/, job
  codes are the durable [[NN]] ids from docs/product/jtbd/, and pipeline mode derives all cards with
  flags headlined at the gate while standalone runs the per-page grill. CREATE gates on JTBD quality
  first, then generates verified SVG/HTML cards (self-checked by rendering and Reading the output) and
  can rebuild in FigJam. Do NOT use for a full PRD (that consumes this), wireframes / UI design /
  component specs, a wireflow (use the wireflow skill), or a sitemap.
metadata:
  version: 2.1.0
  owner: Alvaro Bezerra
  provenance: ported 2026-07-24 from product-craft page-brief v2.0.0 (github.com/ABZerra/product-craft) and adapted to the A-Team contract — briefs/pages/ home, durable job ids, derive-mode for the definition phase.
---

# Page-brief

A **page-brief** is the layer *between the wireflow and the full PRD*. It turns each **unique
page/screen** into documented **requirements tied to jobs** — the "PRD per page", not a sitemap. It
makes the implicit decisions baked into an existing design **explicit and documentable**: what the
page is accountable for, what it must let a user do (and which job each of those rolls up to), where
it sits in the product's journeys and graph, and how you would know the page is actually right.

Pipeline position: **JTBDs → journeys → wireflow → `page-brief` → PRD → wireframes/build.** (In an
A-Team feature run the PRD may exist first — then the cards check against its scope and roll up
into its revision rather than being consumed by a later PRD.)

It is **bounded on both sides**, and both boundaries are load-bearing:

- It stops **below the PRD** — no business goals, metrics, or scope/phasing.
- It stops **above the screen** — no components, no layout, no hierarchy, no information design.
  That's design's work, and the live design is its source of truth.

The success metric to hold onto: **the output must be digestible by a human, not just the AI.** A
cold reader should be able to pick up one card and understand the page.

## Place in the A-Team pipeline

Definition-phase skill. Output home: **`<target>/docs/features/<slug>/briefs/pages/`** —
`board.json` (spec — breadcrumbed source of truth), combined HTML + SVG (deliverable), PNG
(verification copy for gate reviewers). Per-feature artifact: overwrite cleanly on revision.
Commit per run: `docs(<slug>): page briefs`.

- **Job codes are the durable ids.** Board-wide job codes ARE `[[NN-<slug>]]` from
  `docs/product/jtbd/`, headlines quoted verbatim. Never invent a job label on a card — an
  "unlisted job?" flag routes to `jobs-to-be-done`.
- **The wireflow is machine-readable input**: read `briefs/wireflow/board.json` for the page set,
  the journey↔page linkage, and where each job enters a screen — that entry-point detail is
  flow-level and lives there, not here.
- **Two interaction modes, one method:**
  - **Standalone (human present)** — full draft-then-grill per page (Movement 1 below).
  - **Pipeline (definition phase — draft + review, no interrogation)** — **derive all cards** from
    wireflow + PRD + jobs + the live design. Every guess and every "serves an unlisted job?"
    signal is flagged **on the card**; qualitative acceptance criteria are marked
    **"not yet run with a human"** (never self-certified); the gate reviews the full catalog with
    the flags headlined, and the revise loop fixes what's wrong.

## Acceptance lineage in board metadata

Read `acceptance.json` when the feature PRD exists. The canonical schema is in
`../prd-writer/SKILL.md` under **Acceptance obligation ledger**. Preserve the
stable requirement ID/version and obligation IDs behind every page criterion.
In `board.json`, add a top-level `acceptanceObligations` array containing exact
canonical definition snapshots for the page obligations; a Markdown page brief
uses one `acceptance-obligations` JSON fence instead. This is board metadata,
not an extra visible card field. Register every actual board/Markdown page brief
and its applicable obligation IDs in the canonical artifact inventory through
the PRD owner; do not independently rewrite that ledger.

Qualitative criteria remain `human-study` obligations marked pending in the
ledger until a person runs the study and records evidence. A rendering check
supports a separate `rendered-review` obligation; it does not satisfy the cotton
test or a comparative usability study. Preserve benchmark definitions and
acceptance stages without weakening them. If briefs precede the PRD, hand all
factual and qualitative criteria to prd-writer for canonical IDs and return to
attach those IDs before the issues-phase coverage gate.

## The card (7 fields, 3 blocks)

```
Header        P{n} · Page name · route · design-ref
Purpose       1. Responsibilities    — 1–3 lines translating the JTBD into page accountability
              2. Checklist           — TASKS, each tagged to the JTBD it rolls up to
Connections   3. Appears in journeys — inbound journey·step chips
              4. Connects to         — outbound, cross-page AND cross-job
Validation    5. Acceptance criteria — factual + qualitative (the cotton test)
Footer        6. Reading key
```

That's the whole card. **Do not add fields.** Everything that used to be here and isn't was removed
deliberately — the reasoning is in `references/method-decisions.md` Q3/Q14. Read it before you
re-add anything.

## Mode 0 — Create or Review? (decide first)

- **CREATE** (default) — build page-briefs from JTBDs / journeys / wireflow / live design.
- **REVIEW** — critique an *existing* page-brief or screen catalog against the method.

Ambiguous intent → ask. Artifact + "what's wrong" → REVIEW. Raw material + "spec the pages" →
CREATE.

---

## Creating page-briefs

Three movements: **(0) gate on the upstream jobs, (1) draft each card — grilled per page
standalone, derived-with-flags in pipeline, (2) run the generate → rasterize → Read pipeline**
until every card renders cleanly, then deliver.

The method is **draft-then-confirm, per page**: the **design/prototype is the WHAT** (the page's
capabilities are readable off the live screen), the **human is the WHY and the whether-it's-good**
(responsibilities, which jobs truly pass through, ambiguous mappings, the acceptance criteria).
Drafting first grounds the conversation so the human *reacts* rather than authors from scratch.

### Movement 0 — Gather inputs, and GATE on the jobs

**A page-brief cannot be better than the JTBDs feeding it.** Thin cards trace back to
feature-shaped jobs, every time. Check the jobs *before* drafting.

**1. Assemble the inputs:**

| Input | Supplies | If missing |
|---|---|---|
| **The JTBD set** (`docs/product/jtbd/`, active) | the jobs every card tags against | **Stop — gate below.** |
| **The journeys / wireflow** (`briefs/wireflow/board.json`) | page set + "Appears in journeys" linkage | Degraded mode (below). |
| **`prd.md`** | scope the cards must live within | Proceed; cards feed the PRD later. |
| **The live design/prototype** | what each page actually does; the design-ref link | Draft from the wireflow alone, flag heavily. |

**2. Run the job gate.** Even A-Team jobs that passed `jobs-to-be-done`'s gates get rechecked —
defense in depth, and standalone runs may bring outside jobs:

- **Progress-shaped, not feature-shaped?** A job is macro, about progress or feeling — never a
  feature or a screen. ("One place to work my leads" → reject; "Have fluid control over my leads
  and any opportunity that comes" → accept.)
- **Template followed?** `When [situation], I want [motivation], so I can [desired outcome]` —
  motivation ≠ outcome.
- **Attached to an actor-in-situation?** Jobs belong to people in situations, never to "the
  platform". The same product serves two people at the same company with **different jobs**; one
  flat product-owned job list is a smell. (Not personas — the A-Team works situations and
  struggles, not demographics; the job's Context section carries the who/when.)
- **Names a feature at all?** Then it isn't a job yet.

**3. Act on the gate.** If the jobs fail: say so plainly, quote the offending job, show the
progress-shaped version beside it, and route to `jobs-to-be-done`. Explain the downstream cost —
every checklist item and criterion inherits the weakness. Proceed on insistence, but say once,
clearly, that the cards will be limited by it. Never silently draft on bad jobs.

**Degraded mode (no wireflow):** run from design + JTBDs alone; leave **"Appears in journeys" as
an explicit TODO** per card — that field is the one thing only a wireflow can supply.

### Movement 1 — Draft each card, then confirm it (the core loop)

Work **one unique page at a time**. The unit is the **unique page**, deduplicated into a catalog —
one card per page, not one per journey-occurrence. Materially different behavior by context is a
**variant inside the one card**, never a second card.

For each page: **draft the card** from the live screen + wireflow + jobs — responsibility,
job-tagged checklist, connections, acceptance criteria — flagging every gap and guess. Then:
**standalone**, grill the human on that card one thing at a time (confirm the responsibility,
validate each job mapping, resolve every "unlisted job?" flag, land the criteria — especially the
qualitative ones, which you cannot write alone); **pipeline**, keep the flags on the card and move
on — the gate is the confirmation pass.

Rules to enforce while drafting (full reasoning in **`references/method-decisions.md`**):

- **Responsibilities translate the job.** 1–3 lines of page accountability; variants noted here.
- **Checklist items are TASKS, not jobs.** Each a concrete thing the user must be able to do or
  see **on this page**, tagged `task ——▷ [[NN]]`. *Test:* an item that could appear unchanged on
  three pages is a job — rewrite until it's true of *this* page only.
- **The checklist is a job-alignment audit — a gap-finder.** An item mapping to **no** listed job
  branches two ways: **drop it**, or **flag "serves an unlisted job?"** — that flag is a signal
  the upstream job set is missing something. Surface it prominently (gate headline in pipeline
  mode); route to `jobs-to-be-done`.
- **Connects to = outbound, and it's what makes this a graph.** Cross-page (`→ P2`) *and*
  cross-job, including non-navigational connections (open WhatsApp, notify someone, open an
  external form) — exactly what a sitemap would miss.
- **Acceptance criteria have two layers, both required.**
  1. **Factual** — present and true, binary, checkable by anyone.
  2. **Qualitative — the cotton test**: hand a person **only the criterion and the screen** and
     ask *"can you do this?"* **Never self-certify this layer.** Draft the criteria, then state
     plainly they need to be run with a person — in pipeline mode, every qualitative criterion
     ships marked "not yet run with a human", and running them lands on the research plan as an
     activity.
- **Every reference declares its kind: JOB or JOURNEY.** Job pills are `[[NN]]` ids — stable
  board-wide, never invented on a card. Journey chips come from the wireflow. No field mixes the
  namespaces.
- **ID-based page↔journey linkage.** Pages carry stable IDs (`P1`, `P2`, …); link by ID, not
  drawn connectors.
- **Say nothing about the surface.** No components, layout, hierarchy. If you catch yourself
  describing the screen you would draw — stop; that's design's step.
- **Open questions live on the board, not on the card.** Raise in the grill (standalone) or as a
  pinned note beside the card (pipeline); once answered they become a checklist item or a
  criterion. Genuinely open ones mirror into the context ledger.

### Movement 2 — The build pipeline (the reliability core)

Do **not** build straight onto a FigJam board via the API first — you'd be building blind.

1. **Write the board spec** (`board.json`) — `title`, `jtbds` (ids + verbatim headlines + the
   actor-in-situation each belongs to), `pages`. Schema + worked example:
   **`references/spec-schema.md`**.
2. **Generate**:
   `python scripts/page-brief.py board.json --out docs/features/<slug>/briefs/pages --rasterize`
   (add `--columns N` for the card grid). Emits the SVG, combined HTML, PNG — including the JTBD
   definitions page and the job → pages reverse index.
3. **Read the PNG.** See your own output; catch overflow, glyph problems, cramped columns before
   anyone else does. Verify **every** card — never skip.
4. **Iterate** on the spec until clean — `references/card-layout.md`.
5. **Deliver** the combined HTML + SVG. Header design-refs point to live routes, not screenshots.
6. **If requested, rebuild natively in FigJam** (`references/figjam-rebuild.md`).
7. **Hand off.** Upward: `prd-writer` consumes (or re-scopes against) the catalog — pass the
   job-tagged checklists, acceptance criteria, and "unlisted job?" flags. Sideways to design: the
   acceptance criteria are the brief a designer works against, and the cotton tests validate
   their output. Cotton-test runs land as research-plan activities.

---

## Reviewing page-briefs

Critique against the method — don't redraw unless asked.

1. **Take in the artifact** (Read images; screenshot FigJam; read specs). Note what you can't see.
2. **Score against `references/review-criteria.md`.** Headline checks: unit = unique page,
   deduplicated? Checklist = tasks-not-jobs, each `[[NN]]`-tagged? Acceptance criteria present
   with a qualitative layer, not self-certified? Connects-to a real graph (cross-page and
   cross-job)? Job vs journey explicit, codes stable board-wide? Below the PRD and above the
   screen? Upstream jobs progress-shaped and actor-attached? Digestible to a cold reader?
3. **Check upstream too.** Weak cards usually trace to weak jobs — say which it is; fixing cards
   without fixing jobs is wasted work.
4. **Structured verdict**: Verdict (one line + biggest issue) · Strengths · Findings (ordered by
   impact, each with the fix) · Fastest wins (2–3).
5. **Offer to apply the fixes** via CREATE (grill only the gaps).

---

## Guardrails to hold throughout
- **Unit = the unique page.** Variants within one card, never new cards.
- **7 fields, no more.** What you want to add was removed on purpose — check Q3.
- **Checklist = tasks tagged to jobs.** The card's only concrete layer.
- **Qualitative criteria are human-run. Never self-certify a cotton test.**
- **Job vs journey always explicit; job codes are the durable `[[NN]]` ids.** Never invented.
- **Below the PRD, above the screen.**
- **Gate on the jobs before drafting.** Feature-shaped jobs produce thin cards, every time.
- **Always verify by rasterize → Read before showing anyone.** No blind delivery.

## What ships in this skill
- `scripts/page-brief.py` — the spec-driven card engine (3-block layout, job pills with explicit
  kind, JTBD definitions page, job → pages reverse index, N-up grid, combined HTML, optional PNG).
- `references/method-decisions.md` — the method: each locked decision (Q1–Q14) + why, including
  what v2 removed and the reasoning.
- `references/spec-schema.md` — the board JSON schema + worked example.
- `references/card-layout.md` — card layout rules and debugging.
- `references/pipeline.md` — the end-to-end build checklist (incl. rasterizer fallbacks).
- `references/review-criteria.md` — the REVIEW rubric.
- `references/figjam-rebuild.md` — native FigJam mechanics (load only for an editable board).
- `references/examples/` — a worked example spec (illustration only, not method).

## Strict versus draft rendering

Rendering defaults to strict validation. Use explicit `--permissive` for partial
cards; missing criteria and unknown jobs remain warnings on that draft and block
phase advancement. `--validate-only` checks without rendering. For a handoff,
each page needs both acceptance layers, a nonempty job-tagged checklist, and
canonical requirement/obligation IDs. Internal links use exact `targetId`;
`appears_in.step` is the actual screen node ID, not its display label. Follow
`<harness>/runner/ARTIFACTS.md` for the full cross-file gate and Node prerequisite.

## Risk-triggered interaction comparison

When research declares an `interaction-comparison` probe, carry the shared active
job, scenario, constraints, criteria and token conventions into each option’s
brief. Compare task sequence, information architecture or user control; palette
and scale alone do not answer the uncertainty. Link the exact comparison and
selected flow from `runner/INTERACTION-ALTERNATIVES.md`, with benefits, costs and
unrun usability obligations. Routine corrections keep the settled interaction
with a reason; do not generate variants just to fill this section.
