---
name: assessment-designer
description: "Create standards-aligned K-12 assessments and scoring tools. Use this whenever a teacher or coach wants a quiz, test, formative check, performance task, item bank, or a rubric / scoring guide — including phrasings like 'write a quiz on…', 'make a rubric for…', 'I need a unit test for…', 'create a performance task…', or 'how should I grade this project?'. It aligns every item to a real, cited standard (CCSS/NGSS/state), balances difficulty and cognitive level, supplies an answer key or scoring guide, and builds in accessibility + accommodations, then self-checks against the Quality Gates and hands to quality-review. Make sure to use this whenever the user wants to measure or grade learning. Do NOT use it to build a full lesson (use lesson-planner) or slides (use presentation-builder), though an assessment may accompany a lesson."
---

# assessment-designer

Produces standards-aligned assessments and rubrics that actually measure the intended learning.

## 1. Follow the pipeline (`references/method.md`)
Within Generation: `Analysis → Standards Alignment → Differentiation → Generation`.

1. **Analysis** — determine the artifact (`references/artifact-types.md`), the **objective/standard
   to measure**, grade band, and purpose (formative vs. summative). Log assumptions
   (`references/assumptions-protocol.md`).
2. **Standards Alignment** — every item maps to a real, cited, **verified** standard
   (`shared/standards/`, `references/standards-verification.md`). Alignment is the point of an
   assessment — items must measure the objective, not merely the topic (QG §26).
3. **Differentiation & accessibility** — apply UDL (multiple ways to demonstrate learning), readable
   language for the band (`shared/quality/readability-age.md`), and accommodations
   (`shared/differentiation/accommodations-catalog.md`); assess **content, not language**, for ELs.
4. **Generation** — build items + an **answer key or scoring guide** from the templates in
   `assets/templates/`, following `references/assessment-design.md` (validity, cognitive balance,
   bias-free items).

## 2. Validate, then gate
Run the universal + assessment checks (`references/verification-checklists.md`), self-score
against `references/quality-gates.md`, then hand to **quality-review**.

## 3. Always emit the metadata block
Per `references/metadata-schema.md`, including standards cited, the objective measured, and
`human_review_required: true`. Placeholders only — never real student data.

Artifact types: `references/artifact-types.md`. Templates: `assets/templates/`. Worked example:
`examples/grade3-fractions-rubric.md`.
