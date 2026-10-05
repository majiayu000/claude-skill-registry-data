---
name: mono-color
description: Create one original one- or two-ink editorial print image from a theme, sentence, article idea, object, or authorized reference photo, with assigned ink plates, exposed neutral paper, typographic tension, controlled halftone or screen-print texture, exact short copy, and a final Prompt plus compact recipe. Unlike $minimal-zine-poster (relationship 0.88), choose this for 25–55% active paper and a dominant plate/type event rather than aged paper, 70–90% negative space, and a tiny focal event; unlike $poster-design (relationship 0.86), choose this when one/two-ink mechanics are the requested visual system rather than broad poster or flyer exploration; unlike $apply-photo-filter (relationship 0.54), choose this when the source may be cropped and recomposed rather than keeping its composition unchanged.
---

# Mono Color

Build one contemporary or tactile editorial artifact from exposed paper, one or two assigned ink plates, one dominant subject event, and typography that actively participates in the composition. Generate by default; return prompt-only only when explicitly requested.

## Catalog

- Display name: Mono Color
- Categories: Layout & Design
- Status: Ready
- Route label: GPT Image 2 one/two-ink editorial print
- Tone: blue
- Short description: Create one- or two-ink editorial print images with active paper, typographic tension, and controlled halftone texture.
- Similar skills: minimal-zine-poster, poster-design, apply-photo-filter

## What this skill does

- Converts a theme, short text, article idea, object, or authorized image into one original raster editorial print artifact.
- Locks one or two ink plates to explicit image, type, rule, or annotation roles while leaving the neutral substrate visibly active.
- Preserves exact supplied short copy and declared subject anchors without copying a reference composition, wording, logo, lettering, or artwork.
- Returns the generated image, final Prompt, and a compact palette/layout/type/process recipe.

## How to use

Provide one subject or idea and any exact short copy. Optionally provide an authorized image, output ratio, named ink or pair, contemporary or tactile direction, and the identity or factual details that must remain recognizable.

#### Create a two-ink editorial poster

```text
用钴蓝和陶土橙做一张凌晨便利店的双色孔版印刷海报，标题是 “STILL OPEN”。
```

#### Transform a supplied photograph

```text
把这张骑行照片做成群青单色编辑封面，保留人物身份和车轮结构，让标题局部压过车轮。
```

## Workflow

1. Resolve one recognizable subject, one intent, approved exact copy, supplied-image role, preservation anchors, ratio, and faithful versus abstract representation. Do not invent claims, dates, brands, credits, scientific facts, or long body copy. For a complex article, reduce it to one concrete visual metaphor.
2. Treat an authorized subject image as an edit reference and a style image only as visual grammar. Preserve declared identity, expression, product geometry, object count, and factual anchors. Crop, isolate, screen, simplify, or recolor only as authorized. Never copy the reference's composition, wording, logo, distinctive lettering, or artwork.
3. Choose `3:4` unless the user supplies another supported ratio. Keep 25–55% of the canvas as visible Neutral White, Cool Gray, or Pale Beige paper. Use one alignment system, one dominant object or typographic event, one release zone, and at most one deliberate disruption; avoid evenly filled templates and detached headline/photo splits.
4. Use pure one-ink when the user requests monochrome, one ink, or one named color. Otherwise use two plates: a dominant plate at roughly 70–85% of printed coverage and an accent plate at 15–30%. Assign each plate a distinct role before writing the Prompt. Never add a third ink, gradient, decorative color, or full-page digital tint; density variations and a two-plate overlap do not create a new plate.
5. Select restrained mechanical reproduction—clean separation, halftone, risograph, screen print, photocopy, clipped highlights, or slight registration drift—to serve the subject. Contemporary work stays on clean neutral paper with zero to two subtle imperfections; use aged paper or heavier distress only when explicitly requested.
6. Compile a concise natural-language Prompt containing the subject and exact copy, preservation anchors, one concrete visual relation, ratio and active-paper geometry, ink names/hexes and plate roles, type/image interaction, print process, and a short exclusion clause. Do not expose internal field labels or source-specific syntax.
7. Apply the shared [model-selection policy](../../shared/model-selection.md). Use `gpt-image` v1.0 / GPT Image 2 with `quality: "medium"`, `imageSize: "2K"`, `batchCount: 1`, and one durable operation key. Keep the authorized reference attached for an edit. Poll the accepted execution to a terminal state without recreating it. If the user asks for prompt-only, stop before submission.
8. Inspect full-size and thumbnail output. Require one or two inks only, visible substrate, correct copy, recognizable protected anchors, one clear focal event, a quiet release zone, readable hierarchy, requested ratio, and no copied or invented branding. A raster image is not a physical spot-color separation or print-ready file; disclose that boundary.
9. Retry at most once after a known terminal result, with a linked new key and a non-identical Prompt naming only the failed property. Preserve copy, palette, plate roles, composition intent, and reference bindings. Stop and disclose unresolved typography, identity, ratio, or plate drift rather than silently changing models or resubmitting.

## User-facing output

- Media type: One raster editorial print image, final generation Prompt, and compact recipe
- Default quantity: 1 image
- Content per image: One recognizable subject or visual metaphor, one focal event, one or two assigned ink plates, exact approved short copy, and exposed neutral paper
- Default layout: 3:4 with 25–55% visible substrate unless specified
- Preservation: Declared identity and factual anchors for edit references; visual grammar only for style references
- Model policy: GPT Image 2 Medium/2K, one image per operation, one issue-specific retry maximum
- Downstream use: Editorial covers, cultural posters, article hero images, art prints, event graphics, and visual-system exploration
