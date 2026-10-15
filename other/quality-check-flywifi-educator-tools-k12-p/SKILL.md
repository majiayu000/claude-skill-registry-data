---
name: quality-check
description: "Run ONE quality gate check on a draft and return pass/fail with a fix. Do NOT use for a full review (use quality-review)."
---

# quality-check

Runs a single quality gate from `references/quality-gates.md` and returns a structured pass/fail result with a corrective action. Designed to be called once per gate, not all at once. Workflow skills call this atom after each generation step to catch issues early without spending tokens on a full review.

## Input

```json
{
  "artifact": "Students will be able to place fractions on a number line...",
  "artifact_type": "objective | activity | assessment_item | passage | lesson_plan | iep_goal",
  "gate": "standard_alignment | measurable_objective | reading_level | differentiation | no_fabrication | student_data_policy",
  "standard_code": "MA.4.FR.1.1",
  "grade": "4",
  "subject": "Math",
  "context": "checking objective before handing off to activity generation"
}
```

`gate`: which quality gate to apply (from `references/quality-gates.md`). Supported gates: `standard_alignment`, `measurable_objective`, `reading_level`, `differentiation_present`, `no_fabrication`, `student_data_policy`, `bloom_level_match`, `dok_appropriate`.

## Output

```json
{
  "tool": "quality-check",
  "gate": "measurable_objective",
  "result": "pass | fail | warn",
  "finding": "Objective uses measurable verb 'place' (Apply level); condition and criteria are explicit.",
  "corrective_action": null,
  "human_review_required": true,
  "note": "One gate checked. Run quality-check again for each additional gate, or use quality-review for a full audit."
}
```

On `fail`: `corrective_action` describes exactly what to change. On `warn`: issue flagged but not blocking. On `pass`: `corrective_action` is null.

## Do NOT use this atom for
- Full quality audits across all gates (use quality-review)
- Legal or IEP compliance review (escalate to human)
- Certifying an artifact as Final

## Pipeline note
Output conforms to `references/metadata-schema.md`. Called at the Validation step of `references/method.md`. `human_review_required: true` — a passing gate is a positive signal, not a certification.
