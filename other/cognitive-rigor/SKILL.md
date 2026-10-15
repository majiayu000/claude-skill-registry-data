---
name: cognitive-rigor
description: "Classify an objective or question by Bloom's level and Webb's DOK. Do NOT use to write objectives (use objective-write)."
---

# cognitive-rigor

Tags an objective or item with Bloom level (Remember through Create) and Webb DOK (1-4). Used as a quality check to ensure assessments and activities hit the intended rigor level.

## Input

```json
{
  "text": "Students will analyze how the author develops the theme across multiple chapters.",
  "type": "objective",
  "intended_bloom": "Analyze",
  "intended_dok": 3
}
```

## Output

```json
{
  "tool": "cognitive-rigor",
  "bloom_level": "Analyze",
  "bloom_rank": 4,
  "dok_level": 3,
  "dok_label": "Strategic Thinking",
  "matches_intended": true,
  "rationale": "Verb 'analyze' + cross-chapter scope = Bloom Analyze (4) + DOK 3 (requires reasoning across text sections).",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Generating objectives (use objective-write)
- Scoring student work
- Replacing teacher professional judgment on rigor alignment

## Pipeline note
Follows `references/method.md` at the Analysis step (rigor classification). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — Bloom/DOK classification is model-inferred; teacher should verify alignment.
