---
name: curriculum-mapping
description: "Build long-range curriculum planning artifacts for K-12: curriculum maps, pacing guides, and scope & sequence documents. Use this whenever a teacher, curriculum specialist, or administrator is planning across a quarter, semester, or year — phrasings like 'a pacing guide for…', 'map out my year for…', 'scope and sequence for…', 'how should I order these units?', or 'spread these standards across the semester'. It organizes standards into a coherent sequence with realistic pacing, ensures full standards coverage with no gaps or redundancy, and aligns units vertically and horizontally. Make sure to use this whenever the request spans multiple units/weeks/months rather than a single lesson. Do NOT use it to write an individual lesson (lesson-planner) or a single assessment (assessment-designer) — it plans the arc those fit into."
---

# curriculum-mapping

Builds the long-range plan — maps, pacing, and scope & sequence — that individual lessons and
assessments fit inside.

## 1. Follow the pipeline (`references/method.md`)
Within Generation: `Analysis → Standards Alignment → Differentiation → Generation`.

1. **Analysis** — identify the artifact (`references/artifact-types.md`), subject, grade band, the
   time span (year / semester / quarter), and instructional days available. Log assumptions
   (calendar, period length) where not given.
2. **Standards Alignment** — gather the full set of standards for the span and **verify** them
   (`shared/standards/`, `references/standards-verification.md`); the goal is **complete coverage**
   with no gaps or unnecessary duplication. Pull standards AND the **FL course code** from the offline
   index (zero-token, verbatim — `tools/offline_index.py --standards "<topic>" --grade <g> --subject
   <s>` and `--course "<title>"`, e.g. `Grade Three Mathematics → 5012050`) so the map anchors to the
   real FL Course Code Directory entry, not a recalled one.
3. **Coherence & differentiation** — sequence so prerequisites precede dependents (vertical
   coherence) and connections across subjects are noted (horizontal); flag where differentiation
   will be needed at the unit level.
4. **Generation** — produce the map/pacing/scope from the template: units in order, standards per
   unit, a realistic time allocation, and assessment checkpoints.

## 2. Validate, then gate
Run the universal + mapping checks (`references/verification-checklists.md`) — especially
**coverage** (every required standard placed once) and **pacing realism**. Self-score against
`references/quality-gates.md`, then hand to **quality-review**.

## 3. Always emit the metadata block
Per `references/metadata-schema.md`, with `human_review_required: true` and the standards-coverage
summary. Placeholders only.

Artifact types: `references/artifact-types.md`. Template: `assets/templates/pacing-guide-template.md`.
