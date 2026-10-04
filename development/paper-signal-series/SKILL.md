---
name: paper-signal-series
description: >-
  Plan, write, art-direct, generate, and package a coherent 2-10 image minimal-zine social series from notes, articles, photographs, travel stories, products, reviews, cultural topics, data, PDFs, or mixed subjects. Use for Xiaohongshu/小红书图片, Instagram carousels, social visual essays, recommendation posts, photo diaries, evidence-backed explainers, or any multi-image editorial sequence. Produces analysis, card roles, subject-aware composition, saved prompts, real raster images, natural caption copy, evidence provenance when needed, and series-level QA.
---

# Paper Signal Series

Turn content into a sequence with one editorial promise and several visually distinct images. Shared material creates continuity; each card's subject controls its composition.

## Load the shared system

Read these companion files from `../paper-signal/`:

1. `references/core-workflow.md`
2. `references/subject-routing.md`
3. `references/visual-language.md`
4. `references/content-architecture.md`
5. `references/presets.md`
6. `references/prompt-compiler.md`
7. `references/quality-contract.md`

Read `references/evidence-ledger.md` for factual claims and `references/human-voice.md` for personal-sharing or recommendation copy.

## Workflow

### 1. Resolve the post promise

Write one sentence describing what the viewer will feel, understand, or decide after the final swipe. Split unrelated outcomes into separate posts.

Extract platform, audience, source material, language, image count, visible text, supplied photos, exact facts, caption need, public-source-label policy, and output destination.

### 2. Choose the sequence strategy

Select one:

- `story-led` — atmosphere or experience opens the sequence; reveal context gradually.
- `value-led` — conclusion first; follow with useful evidence, tradeoffs, and fit.
- `visual-led` — hero image first; alternate context, detail, object, person, and pause.

Recommend one strategy and count. Default to 4-6 images for ordinary social posts and three substantial items when each needs facts, tradeoffs, and fit.

### 3. Build the content architecture

Create:

- `analysis.md` — promise, audience tension, source/evidence map, scope, and visual opportunities
- `outline.md` — one job, takeaway, exact on-image text, subject route, composition mode, caption handoff, and swipe reason per image
- `caption.md` — natural publishable copy when requested
- `evidence.json` — only when facts, reviews, rankings, numbers, or source documents are involved

Keep one dominant idea per image. Move nuance to the caption.

### 4. Route every image independently

Assign each image a subject route and composition mode. A landscape card may use `panorama-strip`; a portrait may use `portrait-archive`; an object may use `specimen-plate`; evidence may use `dual-frame` or `airy-fragment`.

Lock across the series:

- paper family and aging level
- one lead reproduction process
- type pairing
- anchor hue or tightly controlled hue progression
- texture intensity and safe-zone behaviour

Vary image scale, crop, composition, subject route, color form, and type behaviour. Do not clone the cover layout.

### 5. Save every prompt

Write every four-paragraph prompt to `prompts/NN-{role}-{slug}.md` before any generation call. Verify the complete prompt group exists.

Use exact strings only. Never invent quotes, reviews, dates, coordinates, archive codes, pseudo-language, or first-person experience.

### 6. Confirm once

Show strategy, count, card roles, subject/composition sequence, preset, process, hue, caption voice, source-label policy, and output directory. Skip only when the user explicitly asks for direct/default generation.

### 7. Generate the series

1. Render image 1 without a previous-card reference.
2. Inspect and accept it as the material anchor.
3. Render images 2+ as distinct calls, using image 1 as a style/series reference when supported.
4. Keep direct batches to four or fewer calls.
5. Retry only failed images, once each, with one targeted correction.
6. Copy selected outputs into `outputs/` with stable ordered filenames.

Use the runtime-native bitmap generator. In Codex, use built-in `imagegen`. Never substitute code-rendered posters or patch generated text with overlays.

### 8. Audit and deliver

Run the shared quality contract and project validator. Inspect every image at full size and thumbnail size, then inspect the whole sequence as a strip.

Deliver images inline, absolute paths, final caption, selected strategy, material system, validation result, and any honest evidence or rendering caveats.

## Sequence anti-patterns

- every card uses a tiny centered fragment regardless of subject
- every card is a different visual style
- cover reference forces identical layout later
- atmosphere is manufactured with random pseudo-text
- information cards become dashboard grids on vintage paper
- landscapes are decorative thumbnails and portraits lose identity
- caption repeats the bitmap instead of adding nuance
- generic ending demands likes/follows without helping the reader
