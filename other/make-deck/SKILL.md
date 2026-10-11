---
name: make-deck
description: Turn findings into a clear, downloadable slide deck (.pptx).
trigger: when the user asks for a PPT / slides / presentation / deck
---
## When to use
The user wants a presentation — of an analysis, a project explanation, or a plan.

## How
1. Decide the narrative **before** building: a title + 4–8 slides, one idea each,
   arced as context → findings → recommendation.
2. Call **`make_slides`** with `{title, slides: [{heading, bullets: [...]}]}`.
   - 3–6 short bullets per slide; lead each with the takeaway.
   - Keep bullets skimmable — phrases, not paragraphs.
3. Tell the user the deck is ready and can be downloaded.

## Avoid
- One giant slide — split by idea.
- Paragraph-length bullets.
- Building slides before you have the content (analyse / read the source first).

## Done well
A tight deck a non-expert can follow: a title slide, a clear arc, and skimmable
bullets that carry the actual findings.
