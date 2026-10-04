---
name: to-artifact
description: Publish a page as an Artifact in the house style. Use when asked for an artifact, or for a report, brief, plan, comparison, dashboard, or tool built as one.
argument-hint: "[subject]"
---

The deliverable is an **Artifact**, published in the house style.

Load `artifact-design` and `humanize` before designing, and `dataviz` before writing any chart. [references/design.md](references/design.md) carries the house style: the voice, the type and color it is built from, the stylesheet that sets them, and the reflexes it leaves out. Every word of page copy follows `humanize`.

## 1. Fix the subject

Take the **subject** from the first source that has one: what the invocation names; the subject under discussion this session; a PR or issue related to the current task. If every source is empty, ask.

Done when the subject is one written line and the material it rests on is in hand.

## 2. Frame the reader's job

Inspect all available material before designing. Privately establish:

- Who opens this, in what context, to decide or understand what?
- What is the strongest supported answer?
- What evidence makes that answer credible?
- What tradeoff, uncertainty, or limit changes its interpretation?
- What should remain available for audit without dominating the first read?

Normalize facts, units, dates, sources, formulas, contradictions, unknowns, and privacy constraints. Distinguish observation, derivation, projection, recommendation, and causation. Never invent intent, ownership, urgency, certainty, deadlines, approvals, future behavior, or confidentiality.

Order by reader need rather than source order, and support two reading speeds: an **executive path** where title, headings, decisive values, captions, and conclusion carry the argument quickly, and an **audit path** where exact tables, assumptions, methodology, caveats, and sources preserve the record.

Done when the **argument** is written down — the reader's question, the strongest supported answer, and the evidence that makes that answer credible — every section answers a reader question no other section answers, and every claim has one **evidence home**: a later table may preserve exact lookup, but no second summary, chart, or conclusion restates the same answer at equal prominence.

## 3. Build and check

Let the argument choose the structure. The first viewport is the argument rather than a masthead and setup; past that, compose whatever the material warrants. Take type, color, and voice from [references/design.md](references/design.md), publish [assets/style.css](assets/style.css) beside the page as it sets out, and ship none of the **reflexes** it lists.

Render the published page and read it in both themes and at narrow width:

1. **First read:** would a reader who saw only the first viewport remember the central relationship, decision, or tool rather than the title or mood?
2. **Restraint:** can any surface, border, pill, icon, label, color, paragraph, or section go without losing meaning, affordance, or rhythm? If yes, remove it.
3. **Themes and reflow:** do light and dark carry equivalent hierarchy and contrast, and does the page recompose without overflow or character-level wrapping?

Fix the highest-impact defect, render again, and repeat.

Done when the page is published with the stylesheet beside it, a render clears all three checks, and the user holds the page itself: this review stays internal, so deliver no score, process diary, or self-critique.
