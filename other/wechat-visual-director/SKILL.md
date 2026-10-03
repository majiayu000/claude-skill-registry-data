---
name: wechat-visual-director
description: Project-level visual direction skill for WeChat Official Account articles. Use when planning, improving, diversifying, generating, or reviewing cover images and body illustrations for公众号文章, especially when Codex image generation should be used without being constrained by repetitive preset-based illustration skills.
---

# WeChat Visual Director

Use this skill before generating article visuals. Its job is to choose visual concepts that fit the article, not to force every image through the same style preset.

## Core Rule

Design first, generate second.

Do not start with `type + style + palette`. Start with article role, reader emotion, evidence type, and what the image must make easier to understand.

## Visual Workflow

1. Classify each needed visual.
   - Cover: promise, tension, or central metaphor.
   - Evidence visual: real screenshot, repo evidence, chart, table, UI state.
   - Explanation visual: architecture, workflow, comparison, framework, timeline.
   - Scene visual: workplace pain, decision moment, human context.
2. Decide whether the visual should be generated.
   - Use real screenshots for UI, repo pages, CLI output, dashboards, and product states.
   - Use generated images for conceptual covers, scenes, metaphors, and explanatory illustrations.
   - Do not generate decorative filler.
3. Create 2-3 distinct visual routes for important images.
   - Each route must differ in metaphor, composition, and rendering language.
   - Avoid minor palette-only variation.
4. Pick one route and write a prompt file.
   - Save prompts before generation.
   - Keep on-image text minimal; prefer no text for complex Chinese labels.
   - If text is required, use short Chinese labels only.
5. Generate with Codex native image generation when available.
   - Use the native `image_gen`/`imagegen` capability directly in Codex.
   - Do not route through a separate Codex CLI on another computer.
   - Use `baoyu-image-gen` only when an explicit API provider is needed.
6. Review the image.
   - Reject images that look like generic AI stock art, repetitive template covers, fake dashboards, unreadable text, or unrelated metaphors.
   - Regenerate from a revised prompt; do not patch generated text with programmatic overlays.

## Diversity Matrix

For a multi-image article, intentionally vary at least three dimensions:

- Composition: close-up, overhead map, split-screen, layered system, single object, human scene.
- Visual language: editorial photo-real, hand-drawn notes, precise product diagram, magazine infographic, cinematic metaphor, paper cutout, UI screenshot.
- Cognitive function: hook, proof, compare, sequence, explain, summarize.
- Texture: clean digital, paper, marker, screen glow, realistic workplace, blueprint.
- Camera: macro, desk-level, isometric, documentary, top-down, wide scene.

Never make every body image share the same border, palette, icon style, or abstract blob background.

## Use External Skills As References

- Use `visual-storytelling-design` when the article has data, comparisons, mechanisms, or claim framing that needs annotation and honest context.
- Use `aesthetic` when visual hierarchy, mood, typography, or inspiration-quality review is needed.
- Use `baoyu-article-illustrator` only after this skill has decided image roles and routes.
- Use `baoyu-cover-image` only for cover generation, not for all body images.

## Output Contract

For visual planning, produce:

- Visual inventory with image role, evidence/generation decision, and placement.
- Route options for cover and key body visuals.
- Final prompt file paths to create.
- Generation aspect ratios.
- Review checklist and rejection criteria.

For direct generation, create prompt files first, then generate.

