---
name: reading-level
description: "Estimate a passage's grade band and Lexile. Do NOT use for whole documents or student data."
---

# reading-level

Estimates reading level of a text passage and returns a grade-band label, approximate Lexile range, and a brief rationale. Zero-token path when the `readability` library is installed (Flesch-Kincaid); model-based estimate otherwise. Used by lesson-planner, assessment-item, and differentiate atoms to verify appropriateness before passing content downstream.

## Input

```json
{
  "text": "The water cycle describes how water moves...",
  "target_grade": "5",
  "context": "science passage for a quiz"
}
```

`target_grade`: the intended audience grade. `context` (optional): helps calibrate the estimate.

## Output

```json
{
  "tool": "reading-level",
  "estimated_grade_band": "4-5",
  "lexile_estimate": "700-750L",
  "match_for_target": true,
  "rationale": "Sentence length averages 14 words; academic vocabulary present but not dense; Flesch-Kincaid grade ~4.8.",
  "method": "flesch_kincaid | model_estimate",
  "recommendation": "Appropriate for grade 5. For ELL/below-grade readers, simplify vocabulary in sentences 2 and 4.",
  "human_review_required": true
}
```

`match_for_target`: true if the estimated band includes the target grade. `method` is `flesch_kincaid` when the `readability` or `textstat` library is installed, `model_estimate` otherwise (less precise).

## Do NOT use this atom for
- Full document readability audits (call this atom once per passage)
- Student performance data or reading assessment scores
- Assigning a Lexile as a guaranteed authoritative measure — it's an estimate

## Pipeline note
Follows `references/method.md` at the Analysis step (reading-level estimation). Output conforms to `references/metadata-schema.md`. Standards and Differentiation steps are skipped. This atom is a quality pre-check only. `human_review_required: true` — Lexile estimates are directional, not certified.
