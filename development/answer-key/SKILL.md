---
name: answer-key
description: "Write an answer key with scoring notes for existing assessment items. Do NOT use to write the items (use assessment-item) or to grade students."
---

# answer-key

Creates an answer key with correct answers and scoring notes for each assessment item. Used after assessment-item generates the items. Includes point values and common error notes.

## Input

```json
{
  "items": [
    {"id": "q1", "stem": "What is the main idea of paragraph 2?", "type": "multiple_choice", "options": ["A", "B", "C", "D"]},
    {"id": "q2", "stem": "Explain how the author uses imagery.", "type": "constructed_response"}
  ],
  "standard_code": "ELA.5.R.2.1"
}
```

## Output

```json
{
  "tool": "answer-key",
  "answers": [
    {"id": "q1", "correct": "B", "points": 1, "scoring_note": "Accept B only; A is a detail, not the main idea"},
    {"id": "q2", "exemplar": "The author uses imagery such as... to create a sense of...", "points": 2, "scoring_note": "Full credit requires citing specific imagery AND connecting to effect"}
  ],
  "human_review_required": true
}
```

## Do NOT use this atom for
- Generating assessment items (use assessment-item)
- Grading actual student responses
- Building rubrics (use rubric-build)

## Pipeline note
Follows `references/method.md` at the Generation step (answer key). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — answer keys must be verified by a content expert.
