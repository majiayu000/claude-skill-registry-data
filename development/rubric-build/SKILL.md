---
name: rubric-build
description: "Build ONE rubric (criteria by performance levels) for a task or standard. Do NOT use to write items (use assessment-item) or to score work."
---

# rubric-build

Builds a single rubric with criteria rows and performance-level columns (e.g. Exceeds/Meets/Approaching/Below). Used by assessment-designer and reusable by any skill needing a scoring rubric aligned to an objective or standard.

## Input

```json
{
  "objective": "Students will analyze character motivation using text evidence.",
  "grade": "7",
  "subject": "ELA",
  "levels": 4,
  "level_labels": ["Exceeds", "Meets", "Approaching", "Below"],
  "standard_code": "ELA.7.R.1.1"
}
```

## Output

```json
{
  "tool": "rubric-build",
  "rubric": {
    "objective": "Students will analyze character motivation using text evidence.",
    "criteria": [
      {
        "criterion": "Identification of character motivation",
        "levels": {
          "Exceeds": "Identifies multiple motivations with nuanced text evidence",
          "Meets": "Identifies primary motivation with supporting evidence",
          "Approaching": "Identifies motivation but evidence is vague",
          "Below": "Does not identify character motivation"
        }
      }
    ]
  },
  "standard_code": "ELA.7.R.1.1",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Generating assessment items (use assessment-item)
- Scoring or grading student work
- Building multi-objective rubrics (call once per objective)

## Pipeline note
Follows `references/method.md` at the Generation step (rubric construction). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — rubric descriptors must be reviewed for grade-level appropriateness.
