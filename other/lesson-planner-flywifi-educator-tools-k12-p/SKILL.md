---
name: lesson-planner
description: "Create standards-aligned, differentiated K-12 instructional materials. Use this whenever a teacher or coach wants a lesson plan, unit plan, guided notes, exit ticket, learning centers/stations, or a project/performance task — including phrasings like 'plan a lesson on…', 'I need a 5-day unit for…', 'make an exit ticket for…', 'activities to teach…', or 'something to use tomorrow for my 3rd graders on fractions'. It selects + cites real standards (CCSS/NGSS/state), builds in UDL plus tiering / EL / IEP supports, and self-checks against the Quality Gates before handing to quality-review. Make sure to use this skill whenever the user wants teaching materials for a specific topic, grade, or standard, even if they don't say the words 'lesson plan'. Do NOT use it to build standalone tests/rubrics (use assessment-designer) or slide decks (use presentation-builder), though it will include an aligned check-for-understanding."
---

# lesson-planner

Produces classroom-ready, standards-aligned, differentiated instructional artifacts. This is the
reference implementation of a TOS capability skill — it follows the shared pipeline exactly.

## 1. Follow the pipeline (`references/method.md`)
`Request → Routing → Protocol Enforcement → Generation → Validation → Quality Gates → Release`.
Within **Generation**, work `Analysis → Standards Alignment → Differentiation → Generation`:

1. **Analysis** — determine artifact type (`references/artifact-types.md`), subject, **grade band**,
   topic, and time available. Missing facts → assume the safest default and log it
   (`references/assumptions-protocol.md`); ask only if a choice is high-stakes.
2. **Standards Alignment** — select the most specific aligned standard(s) and cite with
   framework + version (`shared/standards/`). **Verify** every code
   (`references/standards-verification.md`); never invent a code. Use the offline index for a
   zero-token, verbatim lookup — `tools/offline_index.py --standards "<topic>" --grade <g> --subject
   <s>` (returns benchmarks + ESE access points), and `--resource <code>` to surface vetted **CPALMS
   lesson/resource links** already mapped to that standard from the FL instructional toolkits.
3. **Differentiation** — apply **UDL by default** (`shared/differentiation/udl.md`), then add
   tiering, EL supports, and IEP accommodations as relevant. Keep cognitive demand at grade level.
4. **Generation** — fill the matching template in `assets/templates/`, following the design
   principles in `references/lesson-design.md` (measurable objective, gradual release, checks for
   understanding, aligned closure).

## 2. Validate, then gate
Run the universal + lesson checks (`references/verification-checklists.md`), self-score against
`references/quality-gates.md`, then hand to **quality-review** for the authoritative decision.
Nothing is "Final" below 4.0 or with a critical failure.

## 3. Always emit the metadata block
End every artifact with the metadata block (`references/metadata-schema.md`): artifact type, persona,
grade band, subject, standards set + cited codes, differentiation applied, assumptions, the quality
decision, and `human_review_required: true`. Use placeholder student names only — never real data.

## 4. Gold example
`examples/grade3-fractions-lesson.md` is a complete, Approved reference output — match its depth,
structure, and metadata.

Artifact types + required elements: `references/artifact-types.md`. Templates: `assets/templates/`.
