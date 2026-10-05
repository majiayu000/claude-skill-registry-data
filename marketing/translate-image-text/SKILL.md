---
name: translate-image-text
description: Detect, transcribe, translate, remove, and replace text inside a supplied image while preserving layout and visual style. Use for posters, menus, product graphics, comics, or screenshots where translation accuracy and per-block typesetting must be reviewed.
---
# Translate Image Text
## Catalog
- Display name: Translate Image Text
- Categories: Social Media, Utility
- Status: Ready
- Route label: GPT Image 2 native visual translation
- Tone: teal
- Short description: Translate image text and keep the original layout.
## What this skill does
- Uses GPT Image 2 to understand text, context, layout, and style directly from the image.
- Replaces source text only after linguistic review, then checks every rendered block.
## How to use
Provide image, languages, locale, terminology, and protected text.
#### Translate a poster
```text
Translate all English copy to Simplified Chinese; keep layout and brand name.
```
## Workflow
1. Let GPT Image 2 inspect the whole image natively; list each visible source block, its meaning, reading order, placement, and style in a translation review table without routing through OCR.
2. Translate in visual context; preserve names, numbers, units, legal meaning, and glossary. Freeze the reviewed source-to-target table.
3. Use `gpt-image` v1.0 at Medium to replace source text and typeset the approved translations in one image-aware edit.
4. Keep non-text imagery and protected terms unchanged; edit translation to fit rather than making illegible type.
5. Visually compare every rendered block against the reviewed table, checking characters, punctuation, numbers, omissions, overlaps, and reading order.
When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output
- Media type: One translated image plus translation table
- Default quantity: 1
- Content per image: Original visual with reviewed target text
- Default layout: Source layout
- Model policy: GPT Image 2 Medium with agent-led translation verification and revision
- Downstream use: Localized marketing and information graphics
