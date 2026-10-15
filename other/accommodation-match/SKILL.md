---
name: accommodation-match
description: "Match accommodations to a documented student need (IEP, 504, ELL). Do NOT use without a documented need, or for UDL (use udl-options)."
---

# accommodation-match

Given a documented student need (from IEP, 504 plan, or ELL profile), suggests specific research-based accommodations with implementation notes. Never fabricates accommodation categories.

## Input

```json
{
  "need": "Student has difficulty with written expression due to fine motor challenges",
  "source": "IEP",
  "grade": "5",
  "context": "writing assignment — persuasive essay"
}
```

## Output

```json
{
  "tool": "accommodation-match",
  "accommodations": [
    {"accommodation": "Speech-to-text software for drafting", "category": "assistive_technology", "implementation": "Allow student to dictate first draft; edit on screen after"},
    {"accommodation": "Extended time (1.5x) for writing tasks", "category": "timing", "implementation": "Pre-arrange with student so they know the expectation"},
    {"accommodation": "Graphic organizer for essay structure", "category": "organizational_support", "implementation": "Provide before drafting begins; reduce cognitive load of planning + writing simultaneously"}
  ],
  "need_category": "fine_motor",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Suggesting accommodations without a documented need
- UDL options for general classroom design (use udl-options)
- Writing IEP goals (use iep-goal)
- Using real student data (placeholders only)

## Pipeline note
Follows `references/method.md` at the Differentiation step (accommodation matching). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — accommodations must align with the student's actual IEP/504 plan; teacher/case manager must verify.
