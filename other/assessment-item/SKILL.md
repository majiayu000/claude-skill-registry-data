---
name: assessment-item
description: "Write ONE assessment question with its answer for an objective. Do NOT use for a full quiz or test (use assessment-designer) or rubrics (use rubric-build)."
---

# assessment-item

Generates a single assessment item with answer key. Supports multiple-choice, short-answer, constructed-response, true/false, and matching. Accepts a verified standard and objective; returns item text + answer key + DOK level.

## Input

```json
{
  "objective": "Students will be able to represent fractions greater than one on a number line.",
  "standard_code": "MA.4.FR.1.1",
  "grade": "4",
  "subject": "Math",
  "item_type": "multiple_choice | short_answer | constructed_response | true_false | matching",
  "dok_level": 2,
  "context": "post-lesson check"
}
```

`item_type`: default is `multiple_choice`. `dok_level`: 1–4 (default 2). `context` (optional): helps calibrate complexity (pre-assessment, exit ticket, unit test, etc.).

## Output

```json
{
  "tool": "assessment-item",
  "item": {
    "stem": "Which point on the number line below shows the location of 7/4?",
    "type": "multiple_choice",
    "dok_level": 2,
    "options": {"A": "Between 0 and 1", "B": "Between 1 and 2", "C": "Between 2 and 3", "D": "Greater than 3"},
    "answer_key": "B",
    "rationale": "7/4 = 1¾, which falls between 1 and 2 on the number line.",
    "distractor_analysis": "A: Students may confuse 7/4 with 7÷4 without estimating. C/D: Magnitude errors.",
    "standard_code": "MA.4.FR.1.1",
    "bloom_level": "Apply"
  },
  "human_review_required": true,
  "note": "Review item for clarity and fairness before use in a formal assessment."
}
```

## Do NOT use this atom for
- Full assessments (use assessment-designer, which calls this atom per item)
- Rubrics or scoring guides
- Items without a standard — always pass a verified standard code

## Pipeline note
Follows `references/method.md` at the Generation step. Output conforms to `references/metadata-schema.md`. Generation step only. Run through quality-check and reading-level before including in a formal assessment. `human_review_required: true`.
