---
name: create-image-deck
description: Create a consistent image-first presentation deck from supplied content, data, and supplied references, with a slide manifest, one generated visual per page, exact-content checks, and an inspected deck package. Use for visual explainers, image-led pitch or teaching decks, NotebookLM-like illustrated presentations, or full-bleed slide stories; do not use for a single poster, social carousel, ordinary text-first office slides, unsupported factual research, or generic publication planning.
---
# Create Image Deck

## Catalog

- Display name: Create Image Deck
- Categories: Layout & Design
- Status: Ready
- Route label: Image-first presentation production
- Tone: blue
- Short description: Plan, generate, inspect, and package a consistent image-first deck.
- Similar skills: compose-lookbook, photo-collage, create-social-carousel
## What this skill does

- Converts approved content into an ordered slide manifest with one communication job per page.
- Locks a reusable visual grammar before generating the full deck.
- Generates and validates each page independently, then packages only accepted assets.

## How to use

Provide the source content, audience, purpose, language, slide count or scope, target ratio, delivery format, required facts/text, and any supplied brand or style references. State whether text must remain editable.

#### Example

```text
Turn this six-section lesson into an eight-slide 16:9 image-first deck for new hires. Keep the three supplied numbers exact, use our approved colors, and deliver editable headings over illustrated plates.
```

## Workflow

1. Audit the source. Separate verified facts, exact copy/data, optional copy, inferred transitions, and unsupported gaps. Ask for evidence or label uncertainty; do not invent research, claims, quotations, or brand assets.
2. Choose `baked` mode only when short text may safely live in the image. Choose `plate` mode when copy, formulas, charts, or data must be exact or editable: generate a text-free visual plate and add native presentation elements during packaging.
3. Build an exact-count slide manifest before generation. Give every page a stable ID, one core claim, role in the narrative, source trace, layout relationship, exact text/data, visual brief, continuity links, and acceptance checks. Keep title, setup, development, synthesis, and close proportionate to the brief.
4. Define one visual system: ratio and safe area, palette, materials/texture, illustration or photography treatment, typography direction, recurring motifs, spacing, image density, and prohibited elements. A style reference controls treatment only; do not copy protected characters, logos, or a living artist's distinctive style.
5. Select one representative content page as the visual master. Generate it with GPT Image 2 using one durable operation key, `batchCount: 1`, supplied references; no copyright authorization is required, and the page's specific layout and preservation constraints. Poll to a terminal state and inspect it before continuing.
6. Generate one operation per remaining page. Carry the accepted visual system and only relevant recurring references forward. Do not hide multiple pages inside one request or silently downgrade while the selected model remains available.
7. Inspect every terminal result for source fidelity, text/data accuracy, ratio, safe area, hierarchy, subject count, style continuity, cropped elements, artifacts, and page-specific acceptance. Also inspect an ordered montage for pacing, repetition, contrast, and missing/duplicate pages.
8. Repair only failed pages with an issue-specific prompt and a new operation key. If exact baked text or data fails twice, switch that page to a text-free plate with native overlays instead of repeating an identical request.
9. Package accepted pages in manifest order. Preserve the source images, page manifest, prompt/operation record, and editable overlays. Render the deck and verify page count, ordering, overflow, font substitution, links, and export dimensions.
10. Report delivered paths, mode, page count, source-image folder, any editable elements, unresolved limitations, and which pages were regenerated. Do not claim success from submission alone.


## User-facing output

- Media type: Image-first presentation deck plus inspectable source assets
- Default quantity: One deck with the requested exact page count
- Content per artifact: One core claim and one accepted visual composition per slide
- Default layout: 16:9 unless the user or destination requires another ratio
- Model policy: GPT Image 2 Medium/2K, one page per operation; deterministic packaging after acceptance
- Downstream use: Presentation, teaching, pitching, review, or export through the active presentation tooling
