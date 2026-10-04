---
name: data-storytelling-and-business-translation
description: "Translates the logic of data, an analysis, or an AI model into a story a decision-maker understands, using the Data-Information-Insight-Action ladder and the 'so what' test. Use when data or a model needs to be presented to a stakeholder so that it drives a decision instead of just sitting in a report."
---

# Data Storytelling & Business Translation

## Purpose

A data analysis or an AI model doesn't produce value the moment it's
technically finished — it produces value the moment someone makes a
different decision because of it than they would have made without it.
Many otherwise solid analyses end up as a report on a shelf because they
were never translated into language the recipient can act on. This skill
produces the transition from data to action: what the data shows, what it
MEANS, and what the recipient should DO based on it.

## Anchored in research

- The "Engaging through data" area of data literacy (see
  `../data-literacy-competency-assessment/SKILL.md`): synthesizing,
  visualizing, and narrating data is its own skill that has to be
  developed separately, not an automatic byproduct of good analysis.
- The Data-Information-Knowledge-Wisdom hierarchy (Ackoff, 1989), applied
  here as a business Data → Information → Insight → Action ladder: raw
  data becomes information once it's structured, information becomes
  insight once it's interpreted in context, insight becomes action only
  once someone decides to do something based on it.
- Minto, Barbara — the Pyramid Principle (*The Minto Pyramid Principle*,
  1996): the answer/recommendation first, the reasoning and data after —
  the reverse of how analysis is usually built.

## Method

1. **Place the finding on the Data → Information → Insight → Action
   ladder** before presenting it, and identify what stage the
   presentation is currently at:
   - **Data:** raw numbers, tables — not yet structured.
   - **Information:** structured, visualized — tells WHAT happened.
   - **Insight:** interpreted in context — tells WHY it happened and
     what it means for the business.
   - **Action:** a concrete recommendation for what the recipient should
     do next.
   Most reports stay at the Information level. Don't present anything to
   a stakeholder until the finding has been taken at least to the
   Insight level, ideally all the way to Action.
2. **Test every figure/chart with the "so what" question** before it goes
   into the presentation: *"If the recipient sees this, what should they
   think or do differently?"* If you can't answer, either drop the chart
   or add an interpretive sentence that answers the question — don't
   leave "so what" for the recipient to figure out themselves.
3. **Structure the presentation answer-first (Pyramid Principle):** start
   with the recommendation/conclusion, not the chronology of how the
   data was gathered. Reasoning and data come afterward to support the
   claim already made, not as a long path leading up to it. Exception:
   if the audience is skeptical of the conclusion, it may be justified to
   build the evidence first — but that's a deliberate choice, not the
   default.
4. **Anchor the story to one critical business question**, don't try to
   tell everything the data shows. If the analysis has several
   interesting findings, pick the one that answers the recipient's most
   important open question right now — other findings can be attached as
   an appendix.
5. **Show openly where the interpretation departs from the raw data.** If
   the analysis contains assumptions or identified biases (see
   `../data-bias-and-quality-critical-reading/SKILL.md`), mention them
   briefly as part of the story — don't hide them, because a hidden bias
   that surfaces later erodes trust in the whole analysis.
6. **Match tone and depth to the audience.** For a technical audience, the
   model's logic and uncertainty ranges can be shown directly; for a
   leadership audience the same content needs to be condensed into
   business impact first, with technical depth left as backup material.
   For a mixed audience, build a layered presentation (summary first,
   depth available on request).

## What this skill does NOT do

- Doesn't do the data analysis or modeling itself — translates an
  already-existing finding into a message.
- Doesn't replace a general presentation/storytelling skill for
  leadership more broadly — see
  `../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md`
  for the general storyline structure; this skill is its data-specific
  application.
- Doesn't dress up or hide uncertainty to make the story more
  persuasive — transparency about uncertainty is part of credible data
  storytelling, not its opposite.
- Doesn't confirm figures from memory — uses the inputs you provide, or
  marks an assumption clearly (`[assumption — verify]`).

## Refinement notes

Areas to keep deepening with real practice:

- your own examples of an analysis that stayed at the Information level
  and how it should have been taken to Insight/Action
- a concrete presentation template for the Data→Information→Insight→Action
  structure (into `../../references/`)
- rules of thumb for which type of audience requires which depth of
  technical background to be shown

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this: `../data-bias-and-quality-critical-reading/SKILL.md`
  — confirm reliability before building the story on top of it.
- Before this (if the audience's data literacy is unclear):
  `../data-literacy-competency-assessment/SKILL.md`
- Related skill in another pack: `../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md`
  — the general executive storyline structure that this skill
  specializes for data.
- Related skill in another pack: `../../../prototyping-and-demonstration/skills/demo-to-business-case-bridge/SKILL.md`
  — if the story concerns the results of a demo/PoC, use that bridge
  instead.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
