---
name: intervention-mtss
description: "Build Multi-Tiered System of Supports (MTSS/RTI) materials for K-12: Tier 1/2/3 intervention plans, MTSS documentation, data-based decision notes, and progress-monitoring schedules. Use this whenever an interventionist, teacher, or team needs targeted or intensive support planning — phrasings like 'a Tier 2 plan for students struggling with…', 'an RTI intervention for…', 'how should we progress-monitor…', or 'MTSS documentation for our team meeting'. It picks an evidence-aligned intervention for the target skill, sets a tier (1 universal / 2 targeted / 3 intensive), defines a progress-monitoring cadence and decision rules, and stays standards-aligned. Make sure to use this whenever the request is about tiered support, RTI/MTSS, or small-group/individual intervention (as opposed to whole-class lessons). Use placeholder student data only and treat plans as team decision support. Do NOT use it for IEP/504 individualized supports (special-education-support) or whole-class lessons (lesson-planner)."
---

# intervention-mtss

Builds tiered intervention and MTSS materials — team decision support, grounded in data and the
target skill.

> **Boundaries.** Tiers here are **MTSS instructional tiers**, not special-education eligibility. MTSS
> is not special education; if a request is about an IEP/504, route to `special-education-support`.
> Placeholder student data only; plans are decision support for the MTSS/grade-level team.

## 1. Follow the pipeline (`references/method.md`)
Within Generation: `Analysis → Standards Alignment → Differentiation → Generation`.

1. **Analysis** — identify the artifact (`references/artifact-types.md`), the **target skill**
   (specific, e.g., "multiplication fluency", "decoding CVC words"), the tier, and group size.
   Log assumptions where data isn't given.
2. **Standards Alignment** — tie the target skill to a real, verified standard
   (`shared/standards/`) so the intervention connects back to grade-level goals.
3. **Differentiation core** — interventions are inherently differentiated; apply UDL + scaffolds
   (`shared/differentiation/`); keep the target skill precise and the dosage realistic.
4. **Generation** — draft the plan from the template: target skill, tier + dosage (frequency ×
   duration × group size), the intervention routine, **progress-monitoring measure + cadence**, and
   **decision rules** (what data triggers continue / intensify / fade).

## 2. Validate, then gate
Run the universal + intervention checks (`references/verification-checklists.md`); self-score
against `references/quality-gates.md`, then hand to **quality-review**.

## 3. Always emit the metadata block
Per `references/metadata-schema.md`, with `human_review_required: true`. Placeholders only.

Artifact types: `references/artifact-types.md`. Template: `assets/templates/`. Example:
`examples/example-tier2-plan.md`.
