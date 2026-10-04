---
name: image_Hermes
description: Use whenever Kosta invokes /image or asks Hermes to generate, draw, create, render, edit, improve, or debug an image using the default Codex/GPT Image 2 path. Produces strong prompts, picks practical aspect ratio/quality defaults, calls image_generate when appropriate, and uses the bundled GPT Image Craft references for scientific figures, infographics, UI mockups, product shots, photorealism, sprites, posters, typography, and image-edit workflows.
version: 0.4.0
author: Hermes Agent
license: MIT
targets: [hermes-default, hermes-gpt, claude-hermes]
metadata:
  hermes:
    command_priority: 500
    tags: [image-generation, gpt-image-2, codex, image, prompt]
---
# Image — Codex GPT Image 2

Use this as Kosta's default image command. `/image <request>` means: understand the desired artifact, build a production-grade GPT Image 2 prompt, choose the practical Hermes aspect ratio, and call `image_generate` directly unless the user is only asking for prompt help.

The skill now includes the full GPT Image Craft pack from `references/gpt-image-craft/`, plus the local non-generating prompt audit script at `scripts/image_prompt_audit.py`. Use those resources instead of winging it when the request is more than a simple one-shot picture.

## First move

Generate immediately when the user clearly wants an image. Do not ask about style, aspect ratio, detail level, palette, realism, number of variants, or background unless the request is genuinely ambiguous or contradictory. Infer defaults from the use case and proceed.

Return a prompt package instead of calling the tool when the user asks for a reusable prompt, API parameters, critique/debugging, or a production workflow that may run outside Hermes.

## Pick the lane

- **Simple visual request:** write one concise, concrete prompt and call `image_generate`.
- **Prompt/debug/API request:** return a prompt package with use case, prompt, parameters, iteration notes, and quality checks.
- **Scientific figure, chart, infographic, UI, poster, product, sprite, or typography-heavy request:** read the matching GPT Image Craft reference first. If Kosta specifically wants the local RTX text/design lane, load `media/ideogram4-prompting` and use Ideogram 4 JSON captions rather than plain prose.
- **Exact numeric charts, audited diagrams, legal/medical claims, or source-dependent factual graphics:** separate the factual artifact from the generated image. Use deterministic code/SVG/document tooling for exact data; use GPT Image 2 for styled explainers, covers, mockups, or visual companions. If Kosta explicitly asks GPT Image 2/Codex to clean up a chart image, label it as a model redraw and require visual checking of labels, bar heights, error bars, and geometry before grant/paper use.
- **Image edits/reference workflows:** explicitly separate **Change** from **Preserve**. Do not promise reference-conditioned editing through Hermes `image_generate` unless the active provider/tool schema supports image inputs; use a direct script/API path if source images must be submitted.

## Hermes aspect ratio inference

Hermes `image_generate` currently accepts only `square`, `landscape`, or `portrait`. Pick before prompting:

- `landscape`: wide, banner, hero, desktop, cinematic, panorama, scene, slide, dashboard, chart, infographic, wallpaper-horizontal.
- `portrait`: phone, mobile, portrait, poster, story, character sheet, book cover, wallpaper-vertical.
- `square`: product shot, logo mark, avatar, icon, thumbnail, sprite sheet, default.

When signals conflict, optimize for the deliverable: human portrait → `portrait`; scene/slide/chart → `landscape`; product/icon/avatar → `square`.

## GPT Image 2 prompt architecture

For serious prompts, use this structure. For casual art, collapse it into a crisp paragraph carrying the same information.

```text
Goal: [deliverable and audience]
Canvas: [aspect ratio/orientation/output context]
Subject: [main subject, setting, action]
Visual system: [medium, style, lighting, palette, texture, typography]
Composition: [layout, hierarchy, camera/viewpoint, spacing]
Required content: [exact text, labels, data, UI components]
Constraints: [what to preserve, avoid, or keep unchanged]
Quality bar: [photorealistic, textbook-clear, print-ready, sprite-readable, etc.]
```

Why this order: it makes the model choose the visual mode and artifact type before filling detail, which reduces style drift and incoherent layouts.

## Model and parameter defaults

Kosta's default Hermes path is Codex/OpenAI GPT Image 2 through `image_generate`.

- Use `gpt-image-2` / `gpt-image-2-medium` for most finished assets.
- Use low/fast draft quality only for exploratory variants or thumbnails.
- Use high quality for small text, scientific diagrams, dense infographics, UI mockups, publication figures, close portraits, product details, or anything where one better attempt is cheaper than several retries.
- Use `png` for normal outputs; use `jpeg`/`webp` only when an external API path explicitly needs it.
- Do not promise true transparent backgrounds in the current GPT Image 2 API path. Generate on a plain high-contrast background and remove it downstream, or use another provider/workflow that supports transparency.

Useful direct-API sizes from GPT Image Craft when not constrained by the Hermes wrapper: `1024x1024`, `1536x1024`, `1024x1536`, `2048x1152`, `2560x1440`. Current GPT Image 2 flexible-size constraints still apply; use the Codex provider/direct script path for arbitrary sizes rather than pretending `image_generate` accepts them.

## Prompt details that matter

- Use action words: **create**, **draw**, **render**, or **edit**. For edits, say “edit the image by changing X,” not vague “combine/merge.”
- For photorealism, say **photorealistic**, “real photograph,” “professional photography,” or “iPhone photo,” plus camera/lighting cues. Skip boilerplate like “8K masterpiece.”
- Be concrete about materials, shapes, texture, placement, lighting, camera angle, and mood.
- For exact text, quote the exact copy, specify typography and placement, and say “render once, verbatim, no extra text.” Spell unusual words if accuracy matters.
- For dense charts/spreadsheets/tiny labels, warn that image generation is the wrong final-format tool and use deterministic rendering if precision matters.
- For brands, characters, living artists, real people, or protected logos, prefer original designs and broad style descriptors unless the user has rights/authorization.
- Do not promise C2PA/provenance removal.

## Use the bundled references

Read only the relevant file under `references/gpt-image-craft/`:

- `model-and-workflow.md` — GPT Image 2 API/UI choices, size, quality, formats, streaming, limitations.
- `prompt-framework.md` — prompt architecture, iteration tactics, text-in-image guidance.
- `styles/science-education-figures.md` — scientific textbook art and academic figures.
- `styles/data-graphs-infographics.md` — charts, dashboards, timelines, infographics.
- `styles/realism-photography-cinematic.md` — photorealism, documentary, portraits, product, cinematic.
- `styles/design-marketing-ui.md` — ads, logos, UI mockups, branding, pitch/social assets.
- `styles/game-assets-icons-sprites.md` — sprites, icons, pixel art, thumbnails, game art.
- `styles/illustration-comics-character.md` — manga, comics, children's books, character sheets, storyboards.
- `styles/print-editorial-typography.md` — magazine spreads, covers, posters, multilingual type.
- `styles/product-ecommerce-editing.md` — product extraction, virtual try-on, object edits, interior swaps, style transfer.
- `styles/niche-style-atlas.md` — compact formulas for many aesthetics.
- `prompt-recipes.md` — ready-to-adapt templates.
- `troubleshooting.md` — fixes for common failure modes.
- `research-sources.md` — source notes and evidence levels.

## Prompt package output

When not generating directly, include:

1. Use case and intent — what the image is for and how it should be judged.
2. Prompt — ready to paste into ChatGPT or an image API.
3. Parameters — model, aspect/size, quality, format, number of variants, generation vs edit.
4. Iteration notes — one to three targeted follow-ups.
5. Quality check — what to inspect after generation: text, labels, hands, layout, factual claims, identity consistency, transparency/background.

For API-oriented users, include a compact spec:

```text
model: gpt-image-2
endpoint: images.generate or images.edit
size: 1536x1024
quality: high
output_format: png
n: 1 to 4
prompt: ...
```

## Optional prompt audit

For complex, text-heavy, API-oriented, or constraint-heavy prompts, run the non-generating checker before calling an API/direct path:

```bash
python scripts/image_prompt_audit.py --prompt-file prompt.txt --model gpt-image-2 --size 1536x1024 --quality high
```

It flags invalid sizes, transparency mismatch, exact chart/data risks, missing quoted text, style overload, and prompt overloading. It does not spend image quota.

## Calling the Hermes tool

```python
image_generate(prompt=<final prompt>, aspect_ratio="landscape" | "square" | "portrait")
```

After generation, return the image directly. Add only a short useful note, e.g. “I kept it square and optimized for product-shot realism.”

## Failure recovery

If `image_generate` errors or returns empty:

1. Content/policy rejection: clean real-brand, protected-character, celebrity-likeness, sexual, or risky wording; retry once.
2. Tool unavailable/timeout: report the exact error and the generated prompt so Kosta can rerun or diagnose.
3. Missed explicit constraint: inspect the output. If text, orientation, subject count, layout, or core content is clearly wrong, rewrite only the failed section and retry once automatically. If the second attempt also misses, report both attempts and the mismatch.

## Examples

User: `/image a slick product shot of a black ceramic mug for a coffee brand`

Tool prompt:
```text
Create a photorealistic studio product photograph for a premium coffee brand.

Subject: a matte black ceramic mug with a subtle curved handle, empty, centered on a warm stone surface.
Visual details: soft ceramic texture, tiny rim highlights, faint coffee-bean shadows nearby, no visible logo.
Composition: square crop, mug centered with tasteful negative space, eye-level product photography.
Lighting: soft warm key light from upper left, gentle fill, natural contact shadow.
Constraints: no text, no watermark, no fake brand logo, no extra objects except subtle coffee beans/shadows.
```

User: `/image mobile onboarding screen for a meditation app, calm but not generic`

Tool prompt:
```text
Generate one realistic iPhone portrait screenshot of a native iOS meditation app onboarding screen.

Product intent: help a new user choose a calming daily practice without feeling like a wellness cliché.
Screen state: first onboarding screen with a single hero illustration, short headline, one primary CTA, and small secondary sign-in link.
Layout: native iOS safe areas, SF Pro-like typography, generous spacing, bottom CTA above the home indicator.
Visual style: calm editorial UI, warm off-white background, muted sage and clay accents, subtle grain, no stock-photo look.
Exact visible text: headline "Find your quiet minute", CTA "Start", secondary link "Sign in". No other text.
Constraints: straight-on screenshot, normal iPhone proportions, no device mockup frame, no poster layout, no duplicate buttons, no fake logos, no watermark.
```
