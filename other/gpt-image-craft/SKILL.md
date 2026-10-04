---
name: gpt-image-craft
description: >
  Use when the user asks any agent to create, edit, improve, render, or debug AI-generated images, ChatGPT Images, GPT Image 2 prompts, visual style recipes, design assets, thumbnails, sprites, infographics, scientific figures, charts-as-images, UI mockups, posters, product images, photorealistic scenes, or multi-step image workflows. Produce ready-to-run prompts and parameter guidance; do not trigger for deterministic charts, spreadsheets, slides, documents, or code unless the user explicitly wants a generated image prompt or visual-art concept.
version: 1.0.0
compatibility: >
  Open skill format for coding agents. Research updated 2026-05-11 for ChatGPT Images 2.0 and gpt-image-2.
---

# GPT Image Craft

Create useful, controllable image-generation prompts and workflows for ChatGPT Images, GPT Image models, and compatible image tools. The skill is strongest when the user wants a visual asset, visual prompt, style system, prompt critique, image-edit plan, or repeatable image pipeline.

## Core behavior

Turn the user's request into an image brief that makes the visual intent, constraints, and generation parameters explicit. Prefer a small number of high-signal constraints over a bloated prompt; GPT Image 2 responds well to clear structure, concrete visual language, and iterative follow-ups.

Use the image-generation tool directly when available and the user clearly asked for an image. When no image tool is available, when the user asks for prompting help, or when production/API details matter, return a prompt package instead.

For exact numeric charts, audited diagrams, production typography, legal/medical claims, or source-dependent factual graphics, separate the factual artifact from the generated image. Use code or verified source data for exact charts; use image generation for styled explainers, mockups, and concept visuals.

## Read references as needed

Use only the reference files relevant to the user's task:

- `references/model-and-workflow.md` — GPT Image 2 release facts, API/UI choices, size, quality, formats, streaming, limitations.
- `references/prompt-framework.md` — prompt architecture, prompt forms, iteration tactics, text-in-image guidance.
- `references/styles/science-education-figures.md` — scientific textbook art, classroom diagrams, academic figures.
- `references/styles/data-graphs-infographics.md` — charts, dashboards, infographics, timelines, visual wikis.
- `references/styles/realism-photography-cinematic.md` — photorealism, documentary, portrait, product, cinematic styles.
- `references/styles/design-marketing-ui.md` — ads, logos, UI mockups, branding, pitch slides, social assets.
- `references/styles/game-assets-icons-sprites.md` — sprites, icons, pixel art, thumbnails, game art.
- `references/styles/illustration-comics-character.md` — manga, comics, children's book, character sheets, storyboards.
- `references/styles/print-editorial-typography.md` — magazine spreads, book covers, posters, print pieces, multilingual type.
- `references/styles/product-ecommerce-editing.md` — product extraction, virtual try-on, object edits, interior swaps, style transfer.
- `references/styles/niche-style-atlas.md` — compact style formulas for many visual aesthetics.
- `references/prompt-recipes.md` — ready-to-adapt prompt templates.
- `references/troubleshooting.md` — fixes for common failure modes.
- `references/research-sources.md` — source notes and evidence levels.

## Prompt package output

When returning a prompt package, include:

1. **Use case and intent** — what the image is for and how it should be judged.
2. **Prompt** — ready to paste into ChatGPT or an image API.
3. **Parameters** — model, size/aspect ratio, quality, format, number of variants, whether to use image editing or generation.
4. **Iteration notes** — one to three targeted follow-ups to fix likely issues.
5. **Quality check** — what to inspect after generation: text, labels, hands, layout, factual claims, identity consistency, or transparency.

For an API-oriented user, also include a compact JSON-like spec:

```text
model: gpt-image-2
endpoint: images.generate or images.edit
size: 1536x1024
quality: high
output_format: png
n: 1 to 4
prompt: ...
```

## Prompt architecture

Use this structure for most serious prompts:

```text
Goal: [deliverable and audience]
Canvas: [aspect ratio, orientation, output context]
Subject: [main subject, setting, action]
Visual system: [medium, style, lighting, palette, texture, typography]
Composition: [layout, hierarchy, camera, viewpoint, spacing]
Required content: [exact text, labels, data, components]
Constraints: [what to preserve, avoid, or keep unchanged]
Quality bar: [realistic, textbook-clear, print-ready, sprite-readable, etc.]
```

This order helps the model first choose the visual mode, then fill in details inside the correct frame. For casual art, a natural paragraph is fine; for dense diagrams, UI, ads, or exact text, labeled segments reduce ambiguity.

## Model and parameter defaults

Use `gpt-image-2` for new high-quality generation/editing workflows. Use `quality: low` for fast drafts, thumbnails, exploratory variants, and inexpensive ideation. Use `medium` for most finished assets. Use `high` for small text, scientific diagrams, dense infographics, graphs, UI mockups, publication figures, close portraits, or anything likely to require fewer retries.

Common sizes:

- `1024x1024` — square, general purpose, icons, thumbnails.
- `1536x1024` — landscape, slides, charts, UI mockups, posters.
- `1024x1536` — portrait, posters, character sheets, mobile assets.
- `2048x1152` or `2560x1440` — 16:9 hero/slide work when detail matters.

For GPT Image 2, avoid promising true transparent backgrounds. Use an opaque background plus downstream background removal, or a fallback model/workflow that supports transparency.

## Style and use-case selection

Choose style by job, not by vibes alone:

- Teaching or explanation: prioritize readable labels, spacing, consistent visual language, and a known audience level.
- Charts and data graphics: require actual data, axis labels, and a deterministic chart if precision matters.
- Realism: use the word `photorealistic` plus camera/lighting cues; avoid excessive cinema language when the goal is believable everyday photography.
- Branding and marketing: write like a creative brief with audience, brand position, exact copy, placement, and output format.
- Sprites and small assets: specify grid, pixel dimensions, outline, palette, pose count, background, and no anti-aliasing when needed.
- Editing: explicitly lock what must not change, then name the allowed change.

## Safety, rights, and provenance

Respect platform policy and user intent. Prefer original designs and broad style descriptors over copying protected characters, logos, living artists' exact styles, or private people without consent. For real people, preserve identity only when the user has provided or is authorized to use the image. Do not create deceptive, harmful, sexualized, exploitative, or rights-violating imagery. When the request is adjacent to a restricted area, provide a safe alternative prompt that captures lawful visual traits without copying protected material.

Images may include provenance metadata depending on platform. Do not promise removal of C2PA or provenance metadata.

## Running the prompt audit script

Use `scripts/image_prompt_audit.py` when a prompt is complex, text-heavy, API-oriented, or likely to fail on technical constraints:

```bash
python scripts/image_prompt_audit.py --prompt-file prompt.txt --model gpt-image-2 --size 1536x1024 --quality high
```

The script does not call an API. It checks size validity, risky prompt patterns, missing exact data, transparency mismatch, and prompt overloading.

## Examples

### Scientific figure

```text
Goal: Create a textbook-style figure for first-year biology students.
Canvas: Landscape 1536x1024, clean white background.
Subject: Cellular respiration overview from glucose to ATP.
Visual system: Flat scientific textbook illustration, consistent icon style, muted colors, readable sans-serif labels.
Composition: Left-to-right flow with three grouped stages: glycolysis, Krebs cycle, electron transport chain.
Required content: Title "Cellular Respiration at a Glance". Labels: glucose, pyruvate, ATP, NADH, FADH2, CO2, O2, H2O.
Constraints: No tiny text, no decorative clutter, no inaccurate organelles, no extra pathways.
Quality bar: It should read like a polished classroom handout.
```

### Product ad with exact text

```text
Create a polished outdoor billboard mockup for a sparkling water brand called Luma.
Scene: highway billboard at golden hour, realistic environment, believable shadows.
Product: slim can, citrus flavor, clean modern label.
Exact billboard copy, render once and verbatim: "Light up your water."
Typography: bold sans-serif, high contrast, centered, clean kerning.
Constraints: original brand only, no existing logos, no watermark, no extra text.
```

### Sprite sheet

```text
Create a pixel-art sprite sheet for an original cozy-fantasy mushroom courier character.
Canvas: square 1024x1024, transparent-looking plain solid background for extraction later.
Grid: 4 columns x 3 rows, equal cells, each cell contains one centered sprite.
Required poses: idle front, idle side, walk 1, walk 2, run, jump, carry satchel, wave, sleep, surprised, deliver letter, victory.
Style: 32-bit pixel art, crisp silhouette, limited warm palette, dark 1-pixel outline, no anti-aliasing, no blur.
Constraints: no text, no UI, no shadows crossing cell boundaries.
```
