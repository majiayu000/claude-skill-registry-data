---
name: paper-signal-art-director
description: >-
  Art-direct and generate one high-craft minimal-zine bitmap from a landscape, portrait, person, object, product, food, plant, building, interior, photograph, mood, sentence, or article concept. Use when the user wants a standalone poetic poster, editorial cover, visual concept, aesthetic photo upgrade, photo-to-zine restyle, or a subject-aware minimal-zine image without the overhead of a social carousel. Chooses adaptive composition and a physically coherent print process, preserves subject identity, saves the final prompt, invokes the runtime-native image generator, and audits the raster result.
---

# Paper Signal Art Director

Create one authored image. Make the subject, not the style label, drive the composition.

## Load the shared kernel

This skill ships inside the Paper Signal plugin. Resolve shared files relative to this folder and read:

1. `../paper-signal/references/subject-routing.md`
2. `../paper-signal/references/visual-language.md`
3. `../paper-signal/references/presets.md`
4. `../paper-signal/references/prompt-compiler.md`
5. `../paper-signal/references/quality-contract.md`

For an existing-image edit, also read `../paper-signal/references/restyle-contract.md`.

## Workflow

1. **Resolve the asset.** Identify intended use, subject, mood, aspect ratio, exact visible text, references, edit target, protected details, and destination.
2. **Inspect images.** Label each input as `edit-target`, `style-reference`, `content-reference`, or `series-anchor`. Use `view_image` for every local edit target and for any style reference that needs visual interpretation.
3. **Route the subject.** Choose `landscape`, `portrait`, `object`, `architecture`, `concept`, or `evidence`.
4. **Choose composition.** Select `airy-fragment`, `photo-window`, `panorama-strip`, `dual-frame`, `specimen-plate`, `portrait-archive`, or `type-object`. Prefer the mode that keeps the subject rewarding at phone size.
5. **Choose material.** Select one preset, one lead reproduction process, one type pairing, and one meaningful saturated hue. Do not automatically choose cobalt when the subject suggests another ink.
6. **Write the visual thesis.** Reduce the brief to `subject / action or state / emotional tension`.
7. **Save the prompt.** Write the exact four-paragraph raster prompt to `prompts/01-{role}-{slug}.md` before rendering. Use no visible text when words do not improve the image.
8. **Confirm once.** Show subject route, composition, preset, process, hue, text, protected details, and output path unless the user explicitly asked to generate directly.
9. **Render.** Use the runtime-native bitmap generator. In Codex, use the built-in `imagegen` skill/tool. Never substitute SVG, HTML, canvas, or programmatic poster rendering.
10. **Inspect and correct.** Judge subject integrity, material causality, authored composition, exact text, chromatic signal, and phone-size readability. Retry once with one targeted change.
11. **Deliver.** Copy the selected image into the project or requested destination, show it inline, and return its absolute path and saved prompt.

## Existing-photo rule

Use the least invasive transformation that meets the brief:

1. reframe
2. print-transfer
3. editorial-composite
4. scene-transform only when explicitly requested

Preserve identity, crop logic, horizon or pose, scene geometry, object features, approved text, and aspect ratio. Do not beautify faces, redesign products, replace architecture, or invent atmosphere-specific metadata.

## Taste decisions

- Let a landscape occupy a real panorama or photo window; do not reduce it to an atmospheric icon.
- Keep a portrait large enough for the expression to survive. Keep type away from the eyes and mouth.
- Show an object's material and silhouette. Avoid glossy product-ad staging.
- Preserve architectural proportions and light logic.
- Give a concept one metaphor and one tension, not a collage of every sentence.
- Prefer meaningful silence to pseudo-text, fake dates, faux Asian characters, decorative archive codes, or generic birds/moons/stairs.

## Regeneration triggers

Regenerate when the result:

- loses identity, horizon, geometry, silhouette, or defining details
- looks like a clean beige template with grain
- uses arbitrary zine symbols unrelated to the brief
- contains meaningless or incorrect text
- combines several incompatible print defects
- makes the image too small to reward looking
- becomes glossy, cinematic, commercial, scrapbook-like, or UI-like

Never paint over generated text or alter the main composition with code.
