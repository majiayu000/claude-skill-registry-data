---
name: iep-goal
description: "Draft ONE IEP annual goal from a present-level baseline. Do NOT use for a full IEP (use special-education-support) or real student data."
---

# iep-goal

Drafts a single SMART IEP annual goal in the standard format (condition + behavior + criterion). Includes a measurement method and a suggested short-term objective. Requires a present-level baseline (PLOP) and a target area. Always advisory — IEP goals must be finalized by a qualified SPED professional.

## Input

```json
{
  "area": "reading_fluency | math_computation | writing | behavior | communication | social_skills | ELD",
  "plop": "Student currently reads grade 1 passages at 42 words per minute with 85% accuracy.",
  "target_grade": "3",
  "standard_code": "ELA.3.F.1.4",
  "timeframe_months": 12,
  "measurement_method": "curriculum_based | standardized_probe | observation | rubric",
  "context": "annual IEP review"
}
```

`plop`: the Present Level of Performance — required. `timeframe_months`: typically 12 for annual goals. `standard_code`: the FL standard this goal is aligned to (optional but strongly recommended).

## Output

```json
{
  "tool": "iep-goal",
  "area": "reading_fluency",
  "goal": {
    "condition": "When given a grade 3 reading passage,",
    "behavior": "[Student] will read aloud with accuracy and appropriate rate",
    "criterion": "at 90 words per minute with 95% accuracy",
    "timeframe": "by [Annual Review Date], as measured across 3 consecutive probes.",
    "full_text": "When given a grade 3 reading passage, [Student] will read aloud with accuracy and appropriate rate at 90 words per minute with 95% accuracy by [Annual Review Date], as measured across 3 consecutive probes."
  },
  "short_term_objective": "By [Date + 6 months], [Student] will read grade 2 passages at 70 WPM with 93% accuracy on 2 of 3 weekly probes.",
  "measurement_method": "curriculum_based (weekly 1-minute reading probes)",
  "standard_alignment": "ELA.3.F.1.4 — Read grade-level text orally with accuracy, appropriate rate, and expression",
  "plop_used": "42 WPM / 85% accuracy (grade 1 passages)",
  "placeholders": ["[Student]", "[Annual Review Date]", "[Date + 6 months]"],
  "human_review_required": true,
  "legal_notice": "IEP goals are legal documents. This draft must be reviewed and approved by the IEP team (SPED teacher, LEA rep, parent/guardian, and general ed teacher as applicable) before inclusion in any IEP. Never finalize without qualified professional review."
}
```

## Do NOT use this atom for
- Full IEP document generation (use special-education-support)
- Goals without a PLOP — the baseline is required for a legally sound goal
- Any communication that includes real student names, IDs, or scores
- Behavior Intervention Plans (BIPs) — those require FBA data, not a standard goal format

## Pipeline note
Follows `references/method.md` at the Generation step. Output conforms to `references/metadata-schema.md`. This atom is advisory only. `human_review_required: true`. `legal_notice` must be preserved in any output shown to users. IEP goals require qualified professional review before inclusion in a legal document.
