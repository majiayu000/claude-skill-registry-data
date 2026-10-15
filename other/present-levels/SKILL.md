---
name: present-levels
description: "Draft a PLAAFP (present levels) statement from placeholder data. Do NOT use with real student data."
---

# present-levels

Generates a PLAAFP statement that describes a student's current performance across academic and functional domains, using placeholder data. Follows the strengths-needs-impact format required by IDEA.

> **Read first — boundaries (`references/security-and-safety.md` §1-2).** A PLAAFP draft is
> **decision support for the IEP team**, never a final present-levels statement and never an
> eligibility determination. It must be validated against the student's **actual** evaluation data,
> IEP, and local and state policy — IDEA requires the team, not a draft, to establish present
> levels. Where a request needs a specific student's data, **escalate** rather than infer
> (`references/assumptions-protocol.md`). **Never request, infer, or include real student data —
> placeholders only.**

## Input

```json
{
  "student_name": "[Student Name]",
  "grade": "3",
  "disability_category": "SLD-Reading",
  "placeholder_data": {
    "reading_level": "mid-1st grade",
    "strengths": "strong oral comprehension, enjoys being read to",
    "needs": "decoding multisyllabic words, reading fluency"
  }
}
```

## Output

```json
{
  "tool": "present-levels",
  "plaafp": "[Student Name] is a 3rd-grade student identified with a Specific Learning Disability in Reading. [He/She/They] demonstrates strong oral comprehension and enthusiastically engages when text is read aloud. Currently reading at a mid-1st grade level, [Student Name] struggles with decoding multisyllabic words and reading fluency, which impacts access to grade-level content across all subjects...",
  "format": "strengths-needs-impact",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Using real student data (placeholders only)
- Writing IEP goals (use iep-goal after this atom)
- Diagnostic assessment or evaluation

## Pipeline note
Follows `references/method.md` at the Generation step (PLAAFP drafting). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — PLAAFP must be completed with actual assessment data by the IEP team.
