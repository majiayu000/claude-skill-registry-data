---
name: minimal-zine-poster
description: Create one sparse vertical editorial poster or extract a reusable visual system from supplied references using aged paper, 70–90% negative space, one small focal event, restrained typography, one vivid accent, and print/scan texture. Use for a theme, sentence, article idea, photo, brief, or reference set; unlike $poster-design (relationship 0.86), choose this fixed house style rather than broad poster exploration or information-heavy promotion; unlike $article-handdrawn-illustrations (relationship 0.43), choose this for one poster rather than passage-linked body illustrations.
---

# Minimal Zine Poster

Turn content or visual references into one quiet paper-poster system. Generate by default; analyze references or return only a production prompt when explicitly requested.

## Catalog

- Display name: Minimal Zine Poster
- Categories: Layout & Design
- Status: Ready
- Route label: GPT Image 2 minimal-zine poster
- Tone: coral
- Short description: Create sparse editorial posters with aged paper, radical negative space, and one vivid accent.
- Similar skills: poster-design, article-handdrawn-illustrations

## What this skill does

- Reduces a theme, sentence, article, or idea to one imageable relation and one small focal event.
- Turns a photo into an edit target, supporting insert, or style reference with explicit preservation.
- Learns fixed and variable rules from references without copying wording, identity, branding, or exact composition.
- Produces one sparse vertical raster poster, or a reusable prompt and style system when requested.

## How to use

Provide a theme, short text, article or substantive excerpt, photo, or references. Optionally specify exact short copy, ratio, accent color, and what a source photo must preserve.

#### Create from an article

```text
把这篇文章提炼成一个视觉隐喻，做成留白很多、旧纸质感的极简独立杂志海报。
```

#### Transform a supplied photo

```text
用这张人物照片做一张 minimal zine poster，保留人物身份和服装，只改变裁切、排版与纸张质感。
```

## Workflow

1. Choose the smallest mode: generate by default; analyze without generation when asked only for a style system; return prompt-only only when explicit; analyze then generate when both are requested.
2. Parse the core subject, emotional temperature, approved short text, and one imageable relation. Do not invent claims, quotations, dates, credits, brands, or missing article content. Do not illustrate the whole argument as a scene.
3. Inspect supplied images before describing them. Assign each `edit target`, `supporting insert`, or `reference`. Treat a photo plus only “做一张” as an edit target; ask only when two materially different roles remain equally plausible.
4. Use high preservation for recognizable people, pets, characters, artworks, and products unless reinterpretation is authorized. Preserve visible identity, defining markings, silhouette, product geometry, object count, recognizable colors, and relevant pose; prefer a crop, clipping, or printed-photo fragment over redrawing. Medium preservation may change crop, scale, palette, surface, and surroundings while retaining the subject.
5. Build one coherent recipe: a supported portrait ratio; 70–90% calm negative space; one focal element using roughly 5–20% of the canvas; restrained editorial type; one exact high-chroma accent; aged off-white paper; and limited xerox, risograph, halftone, letterpress, or scanned-print treatment. Vary layout, focal structure, and type distribution—not only color or position.
6. Compile concise natural prose containing the purpose and exact short copy, visual metaphor, preservation contract, focal position and scale, paper/type/color/print treatment, and exclusions. Exclude glossy advertising, cinematic scenes, 3D, neon, dense scrapbook collage, full-bleed commercial layout, unrelated icons, watermarks, invented microcopy, and copied reference identity.
7. Generate one image through `gpt-image` v1.0 / GPT Image 2 with `quality: "medium"`, `imageSize: "2K"`, `batchCount: 1`, and the requested supported portrait ratio or `3:4` by default. Use one durable operation key, require a non-empty `executionId`, and poll that accepted execution to terminal state without recreating it.
8. Inspect at full and thumbnail scale. Require a sparse vertical paper poster, one clear event, the accent, restrained type, print reproduction, correct short copy, declared preservation, safe crop, and no commercial/full-bleed drift. Retry at most once with a new linked key and a non-identical Prompt naming only the failure. Disclose unresolved identity, type, or ratio limitations.

For reference analysis, report observed canvas, negative space, subject scale, collage method, composition, typography, color, texture, marks, mood, and avoid directions. Separate fixed rules, variable rules, and sample residue; never copy source text, brands, watermarks, signatures, dates, places, subjects, or exact layouts.

## User-facing output

- Media type: One raster poster plus final Prompt and compact recipe; or explicit reference-analysis / prompt-only output
- Default quantity: 1 image
- Default layout: Supported portrait ratio, normally 3:4, with 70–90% negative space
- Preservation: High or medium invariants for edit targets; visual grammar only for references
- Model policy: GPT Image 2 Medium/2K, one image per operation, one issue-specific retry maximum
- Downstream use: Editorial covers, cultural posters, article hero images, personal art prints, and visual-system exploration
