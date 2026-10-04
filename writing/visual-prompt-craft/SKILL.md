---
name: visual-prompt-craft
description: Craft Higgsfield-grade, hyper-structured image-generation prompts for every blog visual. MANDATORY before any image generation call (generate-visuals, Replicate, GPT-Image, Nano Banana). A weak one-line prompt is a gate failure — every [VISUAL] placeholder gets a full structured prompt built with this skill first.
---

# Visual Prompt Craft — structured prompts for blog imagery

Bad images come from bad prompts. A one-line prompt ("diagram comparing AI girlfriend apps")
produces generic slop. A structured 200-400 word prompt with explicit composition, materials,
lighting, palette, and mood produces agency-grade output from the same model. This skill defines
the mandatory prompt anatomy, calibrated against reference prompts of proven quality
(see `references/example-prompts.md` — study one before writing your first prompt of a session).

## The 9-part prompt anatomy (write ALL parts, in this order)

1. **Subject declaration** — one dense opening sentence: image type + subject + aesthetic school +
   mood. Example pattern: "Horizontal editorial illustration for a premium tech-lifestyle blog
   article about X. Minimalist editorial layout combined with [style], [mood] mood."

2. **Canvas** — aspect ratio and exact background: color WITH hex code, texture/grain.
   Blog targets: hero/featured 16:9, in-article 3:2, comparison panels 16:9.

3. **Composition map** — name every zone and what sits in it (center subject, supporting elements
   upper-right, caption strip bottom). Use positional language: "spanning ~60% width, centered",
   "arranged diagonally from upper-right to lower-left", "tilted at 35°".

4. **Per-element specification** — the quality multiplier. EVERY major element gets its own block:
   material ("hand-thrown stoneware", "brushed aluminum", "soft-touch matte plastic"), exact color
   (+hex), state/emotion, position/rotation, and 2-3 micro-details ("visible brushstroke texture",
   "small beads of melted snow on her temples", "subtle paper grain"). Micro-details are what make
   renders read as photographed rather than generated.

5. **Character & emotion** — give subjects (even objects) personality and a felt emotional state.
   Faces: specify exact expression mechanics ("one winking eye and a small crooked grin",
   "lips slightly parted as if mid-breath, jaw relaxed"). For people: hair, skin detail, wardrobe
   texture, what they are doing and feeling — never just "an attractive woman".

6. **Style triangulation** — anchor the style with X-meets-Y references AND explicit negatives:
   "1970s Scandinavian children's book illustration meets Eastern European folk ceramics —
   NOT anime, NOT chibi". The negative side is as load-bearing as the positive.

7. **Lighting & render spec** — light direction and quality ("soft studio lighting from
   upper-left", "cinematic side-light with snow-bounce highlights"), material behavior
   ("authentic glazed ceramic behavior", "sharp lens reflections"), depth of field, shadows
   ("soft cast shadows beneath, as if gently levitating").

8. **Palette block** — every color in the image listed with hex codes, mapped to its element.

9. **Mood line + quality anchor** — closing line: comma-separated mood adjectives, then the bar:
   "Awwwards / Behance site-of-the-day quality, 4k." For photoreal: "crisp commercial beauty
   photography, cinematic color grading."

If in-image text/UI is needed, add a **typography block**: font archetype by name ("bold condensed
uppercase grotesk like Druk Wide Bold"), casing, tracking, and the exact strings. Keep in-image
text minimal — models still mangle long copy.

## Blog visual archetypes (pick one, then apply the anatomy)

- **Hero / featured image** — the article's emotional headline. Photoreal or stylized-3D scene
  expressing the article's core promise. This is the image that earns the click from SERP/social.
- **Editorial diagram** — concept made spatial (hub-and-spoke, decision tree, layered stack).
  Clean vector-editorial style, brand palette, generous whitespace, max 7 labeled nodes.
- **Comparison panel** — N options side by side as styled cards with consistent iconography.
  NOT a screenshot of a spreadsheet.
- **Photoreal scene** — a person in a moment that illustrates the section (using an AI companion
  app at night, morning coffee with chat open). Cinematic, shallow depth of field, full
  per-element + lighting spec.
- **Data chart** — matplotlib renders from `{slug}-data.json` stay canonical for real numbers;
  this skill styles their framing (title card, palette), never invents data points.

## Pleasur.AI brand constraints (hard)

- Palette, persona and voice: pull from `brand-config.md` (visual-gen config section) — do not invent.
- Adult brand, tasteful: suggestive at most, NO nudity/explicit imagery in blog visuals; 18+ adult
  subjects only; AI-generated persons only — no real-person likeness, no celebrity resemblance,
  no deepfake framing.
- No real third-party logos or trademarks; fictional/generic glyphs only.
- Internal-stack ban applies to image text, captions and alt text (no tool/vendor names).
- Alt text: written for readers and SEO (descriptive, keyword-aware), never the generation prompt.

## Workflow (mandatory)

1. For each `[VISUAL:type=...]` placeholder, draft the full 9-part prompt in
   `content-pipeline/images/{slug}/prompts.md` BEFORE any generation call.
2. Self-check against the anatomy: all 9 parts present? Per-element micro-details? Negatives?
   Palette hexes? If any part is missing, the prompt is not done.
3. Generate, then judge the output like an art director: composition, faces/hands, text artifacts,
   brand fit. If weak, diagnose WHICH anatomy part under-specified the failure, strengthen it,
   regenerate (up to 2 retries per visual), and log the diagnosis in prompts.md.
4. Record final prompt + model + retry count in the visuals manifest (`manifest.json`).

The bar: every blog visual should look like it came from a design agency, not a stock generator.
