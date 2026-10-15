---
name: graphic-organizer
description: "Choose and scaffold ONE graphic organizer (Frayer, T-chart, Venn, concept map). Do NOT use to write the content that fills it."
---

# graphic-organizer

Picks the most appropriate graphic organizer type for a learning task, provides the template structure, labels, and teacher directions for use. Does not fill in content — that is the student's job.

## Input

```json
{
  "objective": "Students will compare and contrast two ecosystems.",
  "grade": "4",
  "subject": "Science",
  "organizer_type": null
}
```

## Output

```json
{
  "tool": "graphic-organizer",
  "organizer": {
    "type": "venn_diagram",
    "why_chosen": "Compare/contrast task maps directly to Venn diagram structure",
    "labels": {"left": "Desert Ecosystem", "right": "Rainforest Ecosystem", "overlap": "Both"},
    "teacher_directions": "Have students list 3-4 characteristics in each section. Guide them to notice overlap in basic needs (water, sunlight, nutrients) despite different amounts.",
    "scaffolding_prompts": ["What does each ecosystem need to survive?", "How do the amounts differ?"]
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Filling in the organizer content (students do that)
- Creating full lesson activities (use activity-generate)
- Digital/interactive organizer rendering

## Pipeline note
Follows `references/method.md` at the Generation step (organizer selection). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — organizer choice depends on classroom context; teacher should adapt.
