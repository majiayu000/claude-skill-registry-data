---
name: wizard-interview
description: "Run a guided Q&A intake from a question schema and return validated answers. Do NOT use to generate content."
---

# wizard-interview

Generic guided-intake atom: given a question schema (fields, types, validation rules, defaults, conditional branches), walks a user through structured Q&A and returns validated responses. Used by teacher-profile step 1 and reusable by any skill needing coached user input.

## Input

```json
{
  "question_schema": [
    {"field": "name", "prompt": "What is your name?", "type": "text", "required": true},
    {"field": "role", "prompt": "What is your primary role?", "type": "choice", "options": ["Teacher", "Coach", "Admin", "Counselor"], "required": true},
    {"field": "grades", "prompt": "What grades do you serve?", "type": "multi_choice", "options": ["K-2", "3-5", "6-8", "9-12"], "required": true}
  ],
  "defaults": {"role": "Teacher"}
}
```

## Output

```json
{
  "tool": "wizard-interview",
  "responses": {
    "name": "[Teacher Name]",
    "role": "Teacher",
    "grades": ["3-5"]
  },
  "validation_passed": true,
  "skipped_fields": [],
  "human_review_required": true
}
```

## Do NOT use this atom for
- Content generation (this collects input only)
- Assessment item generation
- Replacing direct user input with AI-generated answers

## Pipeline note
Follows `references/method.md` at the Intake step (user data collection). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — collected responses drive downstream generation and must be confirmed.
