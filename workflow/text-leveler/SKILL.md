---
name: text-leveler
description: "Rewrite a passage at a target reading level, keeping its meaning. Do NOT use for translation (use translate-comm) or new content."
---

# text-leveler

Rewrites a passage to hit a target grade-band reading level (simpler vocabulary, shorter sentences for lower; richer vocabulary, complex syntax for higher). Preserves factual accuracy and key concepts.

## Input

```json
{
  "text": "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods from carbon dioxide and water.",
  "current_level": "8",
  "target_level": "4",
  "preserve_terms": ["photosynthesis"]
}
```

## Output

```json
{
  "tool": "text-leveler",
  "leveled_text": "Photosynthesis is how plants make their own food. They use sunlight, water, and a gas called carbon dioxide from the air. The plant turns these into sugar, which gives it energy to grow.",
  "original_level": "8",
  "target_level": "4",
  "estimated_result_level": "3-4",
  "changes_made": ["simplified vocabulary", "split compound sentence", "added explanation of carbon dioxide"],
  "preserved_terms": ["photosynthesis"],
  "human_review_required": true
}
```

## Do NOT use this atom for
- Translation to another language (use translate-comm)
- Original content generation (this rewrites existing text)
- Modifying meaning or factual content

## Pipeline note
Follows `references/method.md` at the Differentiation step (reading-level adaptation). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — leveled text must preserve accuracy; teacher should verify.
