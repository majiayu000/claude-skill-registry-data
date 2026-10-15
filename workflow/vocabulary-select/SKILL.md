---
name: vocabulary-select
description: "Pick key academic vocabulary from a topic or passage, with tiers and definitions. Do NOT use for vocabulary quizzes (use assessment-item)."
---

# vocabulary-select

Identifies 5-10 key vocabulary words for a topic/passage, classified by Marzano tier (1/2/3) with student-friendly definitions and teaching suggestions. References the Coxhead Academic Word List when applicable.

## Input

```json
{
  "topic": "photosynthesis",
  "grade": "5",
  "subject": "Science",
  "text_passage": "During photosynthesis, plants convert carbon dioxide and water into glucose...",
  "max_words": 6
}
```

## Output

```json
{
  "tool": "vocabulary-select",
  "vocabulary": [
    {"word": "photosynthesis", "tier": 3, "definition": "The process plants use to turn sunlight, water, and carbon dioxide into food (glucose) and oxygen", "teaching_suggestion": "Use a diagram showing inputs/outputs; connect to students' experience with plants growing toward light"},
    {"word": "convert", "tier": 2, "definition": "To change from one form to another", "teaching_suggestion": "AWL word — connect to math conversions students already know"}
  ],
  "awl_words_found": ["convert"],
  "human_review_required": true
}
```

## Do NOT use this atom for
- Vocabulary assessment or quizzes (use assessment-item)
- Full glossary creation
- Vocabulary for texts not yet selected (provide topic or passage)

## Pipeline note
Follows `references/method.md` at the Analysis step (vocabulary selection). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — vocabulary selection depends on students' prior knowledge; teacher should adjust.
