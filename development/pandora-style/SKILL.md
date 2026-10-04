---
name: pandora-style
description: Apply a chosen or automatically selected built-in or installed external visual style only inside source-aware regions while preserving the rest of a supplied photograph. Use for regional photo stylization, mixed-realism artwork, line-guided geometric cutouts, restrained or expanded semantic fragments, comparisons across style skills, or requests to try print, photographic, art-movement, drawing, craft, digital, poster, zine, and dynamically generated styles inside selected areas.
---

# Pandora Style

Transform only selected parts of a source photograph. Preserve the unselected photograph as the factual anchor. Support one geometric mode, two semantic coverage tiers, and a large modular style catalog.

## Required Resources

Read [references/style-index.md](references/style-index.md) for every run. Then read only the family file containing the requested or selected built-in style. For an installed or user-supplied Style Skill, also read [references/external-style-skills.md](references/external-style-skills.md), then read that Skill completely instead of loading a catalog family.

## Modes

### `line-guided-geometry`

Create normally 3–4 unequal geometric regions from dominant source lines. Use rectangles, trapezoids, parallelograms, wedges, or triangles that follow horizons, rooflines, streets, shadows, rails, bodies, or perspective axes.

- Balance visual weight, not equal area.
- Prefer one dominant region per broad row or column.
- Vary aspect ratio and size; do not default to squares.
- Allow only minor overlap when it improves continuity.
- Keep transformed coverage normally 15–30%.
- Avoid grids, uniform tiles, arbitrary floating geometry, and oversized corner blocks.

### `semantic-fragments`

Create normally 3–4 incomplete masks that follow real object, atmosphere, reflection, shadow, or material contours.

- Select partial objects, not automatically the whole object.
- Preserve interruptions, gaps, occlusion, mist, and reflection decay.
- Keep transformed coverage normally 15–30%.
- Avoid rectangular masks, sticker outlines, complete isolated cutouts, and generic blobs.

### `semantic-expanded`

Create normally 3–5 larger or linked masks that still follow real object, atmosphere, reflection, shadow, or material contours. Use this when the user wants a more immersive, expressive result while retaining clearly photographic anchor fields.

- Keep transformed coverage normally 32–52%.
- Allow one nearly complete object or object cluster when it improves the composition, but retain interruptions, tapering edges, occlusion, or photographic gaps elsewhere.
- Preserve at least two substantial untouched photographic fields in different parts of the frame.
- Let related semantic regions echo or connect across the image without becoming a global filter.
- Avoid rectangular masks, sticker outlines, generic blobs, full-scene conversion, or transforming every dominant layer at once.

## Workflow

1. Inspect the source image and build a compact Scene Card: core subject; supporting elements; spatial invariants; dominant lines; visual-weight map; quiet areas; native colors; meaningful minor colors; and candidate semantic contours.
2. Select the requested mode. If absent, choose `line-guided-geometry` for strong structural lines, `semantic-fragments` for a restrained intervention around distinctive objects or organic contours, and `semantic-expanded` only when the user asks for higher coverage, stronger continuity, or a more immersive artwork.
3. Resolve the style:
   - If the user names a Style Skill, read it fully and compile a regional adapter from it.
   - If the user names an `external:` selector, resolve it through `external-style-skills.md`, then read the complete external Skill and its selected variant file.
   - If the user names a catalog slug, load its family file.
   - If the user asks for a suitable style, use the selection rules in `style-index.md`.
4. Choose regions before compiling the style: normally 3–4 for `line-guided-geometry` or `semantic-fragments`, and 3–5 for `semantic-expanded`. Region selection and style selection are independent.
5. Compile a Regional Style Contract:
   - `medium`: visible material or reproduction process;
   - `abstraction`: what to retain, merge, omit, and transform;
   - `palette`: preserved source color plus added-color policy;
   - `mark_system`: line, field, rhythm, grain, facets, stitches, pixels, etc.;
   - `edge_behavior`: geometric cut, contour fade, torn fiber, ink bleed, lead line, stitch, or other style-appropriate handoff;
   - `density`: active transformed detail and internal quiet share;
   - `text`: exact wording and treatment, or `none`;
   - `hard_avoids`: style-specific failure modes.
6. Generate or edit using the source image as the only factual visual reference. Repeat the preservation constraint near the beginning and end of the prompt.
7. Inspect at normal and thumbnail scale. Correct at most once for an observed failure.
8. Return only the requested number of final images. If a retry is necessary, label the earlier output as a rejected draft and do not count it as a final image.

## Adapting Another Style Skill

Extract only locally renderable palette, texture, medium, line, shape, abstraction, reproduction behavior, local typography, edge behavior, and negative constraints.

Discard or localize global requirements such as full-canvas paper, poster ratio, overall layout share, global background replacement, global typography hierarchy, borders, and mockups. A regional adapter may introduce paper only inside selected masks.

When comparing two region modes with the same style, keep medium, added hue, text, abstraction level, and transformed-area budget constant. Change only mask logic.

The mode always owns the final outer mask silhouette; the external style owns only internal rendering. Apply the Mask-First Invariant in `external-style-skills.md`. Internal torn paper, blocks, facets, particles, or strokes must never make `line-guided-geometry` and either semantic tier converge into the same mask language. The two semantic tiers share contour logic and differ primarily in coverage, continuity, and how much photographic breathing room remains.

## Color Policy

Choose color after analyzing the source. Region mode never chooses the hue.

1. `source-resonance`: intensify one meaningful minor source color.
2. `quiet-harmony`: use a more saturated analogous source hue.
3. `focused-counterpoint`: use a complementary or near-complementary hue when the source lacks a usable minor color.
4. `process-native`: use a medium-defining color only when essential, such as cyanotype blue.
5. `random`: use only when the user explicitly requests random color exploration.

Natural colors outside transformed regions do not count as added hues. Use normally zero or one added hue. Bind added color to a real contour, rhythm, shadow, or object; never add a detached decorative swatch. Keep the same hue across mode comparisons.

## Prompt Contract

Compile prompts in this order:

1. source identity and outside-mask invariants;
2. exact mode and source-derived region descriptions, normally 3–4 or 3–5 according to the selected tier;
3. Regional Style Contract;
4. transformed-area budget, color role, and optional text;
5. repeated preservation rule and hard avoids.

Use decisive visible instructions. Do not include file paths, research notes, theory explanations, or internal scores in generation prompts.

## Quality Gate

- Preserve source crop, scene, perspective, lighting, color, and identity outside selected regions.
- Use normally 3–4 regions for geometry or restrained semantics and 3–5 for expanded semantics rather than a full-scene transformation.
- Make geometry follow source lines and avoid equal tiles.
- Make semantic masks follow incomplete real contours rather than boxes or stickers.
- Keep `semantic-fragments` normally at 15–30% coverage and `semantic-expanded` normally at 32–52%, with at least two substantial photographic anchor fields in the expanded tier.
- Confirm that the two modes remain distinguishable by outer mask silhouette at thumbnail scale, regardless of internal style.
- Vary region sizes and balance them atmospherically.
- Keep the selected style inside masks without global leakage.
- Make added color source-justified and structurally useful.
- Hold style and color constant when comparing modes.
- Avoid unwanted global typography, framing, mockup depth, invented objects, and watermarks.
- Return exactly the requested number of final images.

## Output

Label every final image with `mode × style-slug`. Add one short sentence explaining the region choice and color logic. Include full prompts only when the selected Style Skill requires them or the user asks.
