---
name: activity-generate
description: "Generate ONE learning activity for an objective, grade, and subject. Do NOT use for a full lesson (use lesson-planner) or quiz items (use assessment-item)."
---

# activity-generate

Generates a single, structured learning activity (not a whole lesson). Each activity includes a procedure, materials, timing, and DOK level. Accepts an objective from objective-write and optional differentiation flags.

## Input

```json
{
  "objective": "Students will be able to represent fractions greater than one on a number line.",
  "standard_code": "MA.4.FR.1.1",
  "grade": "4",
  "subject": "Math",
  "activity_type": "hands_on | discussion | independent | partner | whole_class",
  "duration_minutes": 20,
  "differentiation": ["ELL", "IEP"],
  "materials_available": ["number line strips", "whiteboards"]
}
```

`activity_type`: optional; if omitted the atom selects an appropriate type. `differentiation`: list of profiles to weave in (see differentiate for a separate full differentiation pass). `materials_available`: optional constraint.

## Output

```json
{
  "tool": "activity-generate",
  "activity": {
    "title": "Number Line Fraction Hunt",
    "type": "hands_on",
    "duration_minutes": 20,
    "dok_level": 2,
    "procedure": ["1. Distribute number line strips (0–2).", "2. Teacher models placing 5/4 on the strip.", "3. Students independently place 3 fractions > 1.", "4. Partner check + class debrief."],
    "materials": ["number line strips", "dry-erase markers"],
    "ell_support": "Provide visual fraction vocabulary card (numerator/denominator in English + Spanish).",
    "iep_support": "Pre-labeled number lines; allow peer partner for Step 3.",
    "standard_code": "MA.4.FR.1.1",
    "objective": "Students will be able to represent fractions greater than one on a number line."
  },
  "human_review_required": true,
  "note": "One activity — combine with other activity-generate calls to build a full lesson."
}
```

## Do NOT use this atom for
- Full lesson plans (use lesson-planner, which calls this atom multiple times)
- Assessment items (use assessment-item)
- Differentiated rewrites of an existing activity (use differentiate)

## Pipeline note
Follows `references/method.md` at the Generation step. Output conforms to `references/metadata-schema.md`. Generation step only. Pass the output to quality-check before including in a lesson. `human_review_required: true`.
