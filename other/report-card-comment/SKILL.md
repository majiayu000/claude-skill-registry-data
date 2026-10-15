---
name: report-card-comment
description: "Draft ONE standards-based report card comment from placeholder data. Do NOT use with real student data or for IEP progress reports (use iep-goal)."
---

# report-card-comment

Generates one standards-based report card comment with growth language, aligned to grade-level expectations. Uses placeholder data only — never real student data.

## Input

```json
{
  "student_name": "[Student Name]",
  "grade": "3",
  "subject": "Math",
  "standard_codes": ["MA.3.NSO.1.1", "MA.3.NSO.1.2"],
  "placeholder_performance": "approaching grade level in place value; meets expectations in addition/subtraction",
  "tone": "encouraging"
}
```

## Output

```json
{
  "tool": "report-card-comment",
  "comment": "[Student Name] is making steady progress in mathematics. [He/She/They] demonstrates solid understanding of addition and subtraction strategies and is building confidence with place value concepts. Next steps include practicing representing numbers in different forms (standard, expanded, word). Keep up the great effort!",
  "standards_referenced": ["MA.3.NSO.1.1", "MA.3.NSO.1.2"],
  "human_review_required": true
}
```

## Do NOT use this atom for
- Using real student data (placeholders only)
- IEP progress reports (use iep-goal)
- Parent conference notes (use parent-comm)

## Pipeline note
Follows `references/method.md` at the Generation step (narrative composition). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — comment must be personalized with real data by the teacher.
