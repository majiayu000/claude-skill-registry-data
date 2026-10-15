---
name: misconception
description: "List common student misconceptions for a topic and grade. Do NOT use to diagnose one student or to write content."
---

# misconception

Returns a short list (2–5) of documented common student misconceptions for a topic, with a brief note on why each occurs and how instruction can address it. Used to seed distractor analysis in assessment-item and to inform activity design in activity-generate.

## Input

```json
{
  "topic": "fractions greater than one",
  "grade": "4",
  "subject": "Math",
  "standard_code": "MA.4.FR.1.1"
}
```

## Output

```json
{
  "tool": "misconception",
  "topic": "fractions greater than one",
  "grade": "4",
  "misconceptions": [
    {
      "misconception": "A fraction must be less than 1 (the numerator must always be smaller than the denominator).",
      "why_it_occurs": "Students over-generalize early fraction instruction where all examples show proper fractions.",
      "instructional_remedy": "Show number lines extending past 1; use real-world examples (1¼ pizzas, 5/4 cups of water)."
    },
    {
      "misconception": "The fraction 7/4 is the same as 7 ÷ 4 ≈ 1.something unrelated to fractions.",
      "why_it_occurs": "Confusion between fraction notation and division algorithm taught separately.",
      "instructional_remedy": "Connect fraction-as-division explicitly; show 7/4 on a number line alongside the division result."
    }
  ],
  "sources": ["FL B.E.S.T. vertical progression", "NCTM misconception research (model-inferred)"],
  "human_review_required": true,
  "note": "Misconceptions are model-inferred from common research patterns — verify against current curriculum resources."
}
```

## Do NOT use this atom for
- Diagnosing a specific student's errors (use intervention-mtss)
- Generating assessment items or activities (pass this output to assessment-item or activity-generate)

## Pipeline note
Follows `references/method.md` at the Analysis step (pre-Generation). Output conforms to `references/metadata-schema.md`. Pre-Generation step. `human_review_required: true` — misconceptions are research-based but model-inferred; teacher should verify against district curriculum materials.
