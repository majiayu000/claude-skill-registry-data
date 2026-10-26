---
name: design-brief
description: Use when an interface change needs visual or interaction criteria, or a vague design preference must become a bounded design task.
---

# Design brief

Use this optional route for visual/interaction judgment. API or infrastructure
work does not need a design score. Reuse the canonical product brief and delivery
slice; preserve their OUT/RQ IDs and specification ownership. For a small brand
fix, a concise combined record is enough; keep existing components and navigation.

Read `docs/templates/design-brief.md` and `docs/templates/design-rubric.md`.
Use `docs/examples/design-evaluation/library-rooms.md` for original anchored
examples, not evidence about the current product.

In the ai-dlc source repository, these templates/examples live under
`agents/templates/` and `agents/examples/`. In older projects without copied
assets, use the record contract below directly; do not require adoption.

Before generation, produce these linked records under `docs/design/<work-id>/`
(or the project's approved equivalent):

1. `brief.md`: owner/status, source brief and delivery slice, OUT/RQ references,
   audience/journey, supplied evidence versus hypotheses, scope/non-goals, brand
   constraints, compatibility/accessibility target, unresolved decisions.
2. `rubric.md`: ID/version; each criterion's local ID and RQ reference; required
   behavior with setup/action/expected/evidence; rated criteria with specific
   1/3/4 anchors, task thresholds and evidence methods; states/viewports/fixtures.
3. Run decisions: generator tool, evaluator/access handoff, candidate ID plus
   revision or digest, iteration ceiling AND time or token ceiling, budget owner,
   approval source/status and stop/plateau condition.

Keep proposed choices distinct from reviewed task decisions. Permission to use
this workflow is not approval for a task budget or paid generation. Missing
material decisions or ceilings leave a draft and a concrete next decision.
Use discovery/needs-spec when the outcome or behavior needs clarification.

Proposed starters: 0–4 ratings; minimum 3 for required rated criteria; initial
candidate plus two revisions; plateau after two comparable evaluations without
criterion improvement or a required defect resolved. Projects review/adapt these
before generation. Required behavior must pass and required evidence must exist;
optional averages cannot compensate. Unobserved is unverified, never 0 or pass.
Novelty means useful fit to the brief; appropriate brand reuse is not a defect.

Once the task contract and budget are settled, hand generation to the user's
selected existing tool/skill within its authorization. Preserve each candidate
and rubric version. Give design-evaluate the brief, rubric, identified candidate
and access instructions, keeping generator self-ratings out of the evidence.
A separate session or human can evaluate; otherwise label self-review explicitly.
Readable artifacts do not establish any client/browser/delegation capability.
