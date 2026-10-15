---
name: sentence-frame
description: "Write sentence frames and stems for English learners or struggling writers. Do NOT use for translation (use translate-comm)."
---

# sentence-frame

Creates sentence frames (fill-in-the-blank structures) and sentence stems (opening phrases) calibrated to a WIDA/ELP proficiency level. Helps ELL students participate in grade-level academic tasks.

## Input

```json
{
  "task": "Write a claim about whether the character made the right decision",
  "proficiency_level": "emerging",
  "grade": "6",
  "subject": "ELA"
}
```

## Output

```json
{
  "tool": "sentence-frame",
  "frames": [
    {"frame": "I think [character name] made a [good/bad] decision because ___.", "level": "emerging", "scaffold_type": "sentence_frame"},
    {"frame": "The character decided to ___ because ___.", "level": "emerging", "scaffold_type": "sentence_frame"},
    {"frame": "Based on the text, I believe...", "level": "developing", "scaffold_type": "sentence_stem"}
  ],
  "proficiency_target": "emerging",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Translation to another language (use translate-comm)
- Full lesson differentiation (use differentiate or lesson-planner)
- Assessment accommodation (use accommodation-match)

## Pipeline note
Follows `references/method.md` at the Differentiation step (ELL scaffolding). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — frames must match the actual proficiency level of students in the class.
