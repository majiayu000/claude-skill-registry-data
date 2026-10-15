---
name: special-education-support
description: "Draft special-education support materials for K-12: accommodation plans, modification plans, IEP goal drafts and present-levels language, and progress-monitoring tools. Use whenever a special-education teacher, case manager, or general-ed teacher needs help with IEPs, 504 plans, accommodations, modifications, specially-designed instruction, or tracking progress toward goals — e.g. 'draft an IEP goal for…', 'what accommodations for a student who…', 'modify this assignment for…', or 'a progress monitoring sheet for…'. It distinguishes accommodations (how a student accesses learning) from modifications (what they're expected to learn), grounds supports in the accommodations catalog, and flags everything for team/legal review. CRITICAL: never use real student data — placeholders only — and treat all output as a draft for the IEP/504 team, not a final or legal determination. Do NOT use it to write general lessons (lesson-planner) or tiered intervention plans (intervention-mtss)."
---

# special-education-support

Drafts individualized support materials — always as **decision support for the IEP/504 team**, never
as a final or legal determination.

> **Read first — boundaries (SECURITY_AND_SAFETY.md).** Every output here is a *draft for a
> qualified team* and must be validated against the student's **actual** IEP/504 plan and local/state
> law and policy. **Never request, infer, or include real student data — use placeholders only.**
> Eligibility and legal determinations are out of scope; if a request needs a specific student's
> plan details, **escalate** (`references/assumptions-protocol.md`) rather than assume.

## 1. Follow the pipeline (`references/method.md`)
Within Generation: `Analysis → Standards Alignment → Differentiation → Generation`.

1. **Analysis** — identify the artifact (`references/artifact-types.md`), the area of need, grade
   band, and the general-ed context. Do not invent disability/eligibility facts — log assumptions or
   escalate.
2. **Standards Alignment** — where goals connect to academic standards, cite real, verified standards
   (`shared/standards/`); IEP goals may also be functional/behavioral. For students with significant
   cognitive disabilities, pull the matching **Access Points** from the offline index (zero-token,
   verbatim — it cannot fabricate a code): `tools/offline_index.py --standards "<topic>" --grade <g>
   --subject <s>` returns AP codes (`.AP.`, `.In./.Su./.Pa.`) alongside the parent benchmark, so the
   alternate-standard alignment is grounded, not recalled.
3. **Differentiation core** — ground supports in `shared/differentiation/accommodations-catalog.md`.
   **Accommodation** = changes *how* a student accesses/shows learning (expectation unchanged).
   **Modification** = changes *what* is expected (significant team decision — flag it, don't assume).
4. **Generation** — draft from the templates, in clear team-ready language, with the legal-boundary
   note attached.

## 2. Validate, then gate
Run the universal + SpEd checks (`references/verification-checklists.md`); the Safety gate is
prominent here (PII, legal boundary, human review). Self-score against `references/quality-gates.md`,
then hand to **quality-review**.

## 3. Always emit the metadata block
Per `references/metadata-schema.md`, with `human_review_required: true` and an explicit "validate
against the student's actual plan" note. Placeholders only.

Artifact types: `references/artifact-types.md`. Templates: `assets/templates/`. Example:
`examples/example-accommodations.md`.
