---
name: paper-signal
description: >-
  Plan, art-direct, generate, edit, and quality-check tactile minimal-zine bitmap imagery from almost any subject: landscapes, portraits, objects, products, architecture, interiors, existing photographs, moods, article ideas, cultural essays, data, reviews, and social-media card series. Use for 小红书图片, Instagram carousels, poetic posters, editorial covers, photo restyling, visual essays, evidence-aware explainers, or any request for aged paper, photocopy, risograph, letterpress, sparse type, and restrained single-ink character. Routes the subject before choosing composition, preserves identity and factual content when editing, saves reproducible prompts, invokes the runtime-native image generator, and audits the real raster output. Do not use for glossy commercial ads, deterministic UI/vector assets, or exact diagram rendering.
---

# Paper Signal

Turn a subject or source into a complete visual production: understand it, choose a subject-aware minimal-zine composition, save the final prompt, render the bitmap, and judge the actual image rather than the intention.

## Route the job

1. Read `manifest.yaml`.
2. Read every file listed under `always_load`.
3. Select one delivery route:
   - `single-card` — one poster, cover, landscape treatment, portrait, object plate, or concept image.
   - `restyle-existing` — one or more supplied images are edit targets.
   - `new-series` — a social carousel, visual essay, story sequence, or evidence-led card set.
4. Select one subject route from `references/subject-routing.md` before choosing a layout.
5. Read only the route-specific and on-demand references needed for the job.
6. State the detected delivery route, subject route, and intended deliverables in one short user-facing line before production.

Default to `single-card` for a theme, sentence, scene, person, place, object, or one supplied photo. Default to `new-series` only when the user asks for several images or supplies content that clearly needs a sequence. Use `restyle-existing` when preservation of an existing image is the primary goal.

## Non-negotiable contract

- Preserve the subject before styling it. A landscape must still feel spatial, a portrait must retain identity, and a product or object must keep its defining form.
- Preserve factual and semantic invariants when editing. Never invent or silently alter text, numbers, labels, identity, architecture, product features, or scene-defining details.
- Use `minimal-zine-standard` as a material kernel, not a universal template. Choose an adaptive composition mode; do not force every subject into one tiny central data cluster.
- Build texture from one plausible reproduction process. Do not simulate quality by piling random scratches, tape, coffee stains, and generic grunge onto a clean design.
- Use real language or intentional abstraction. Never add faux Japanese/Korean characters, fake archival codes, fake coordinates, or meaningless pseudo-text to manufacture atmosphere.
- Keep public source labels hidden by default while retaining provenance internally when facts or licensed material are involved.
- Separate truth, interpretation, and voice. Never invent a rating, quote, review consensus, first-hand experience, or source.
- Save the exact final prompt to `prompts/NN-{role}-{slug}.md` before generation.
- Use a runtime-native raster image tool. In Codex, use the built-in `imagegen` skill/tool; do not substitute SVG, HTML, canvas, or programmatic poster rendering.
- Never repair generated text by painting over the bitmap. Reduce text, correct the prompt, and regenerate to a versioned output.
- Preserve user files and generated candidates. Never overwrite an existing artifact without a versioned sibling or timestamped backup.

## Production workflow

### 1. Resolve the brief

Extract the intended use, subject, mood, audience, output count, aspect ratio, exact visible text, edit invariants, reference-image roles, and any factual or rights constraints.

Use these defaults when the request leaves them open:

- delivery route: `single-card`
- subject route: infer from `references/subject-routing.md`
- aspect ratio: preserve the edit target; otherwise `3:4` for social cards and `3:5` for standalone posters
- visible text: one short phrase or none
- public source labels: hidden
- preset: `minimal-zine-standard`
- anchor hue: derive from the subject; cobalt is the fallback

Load the first available preference file, if present:

1. `.paper-signal/PREFERENCES.md`
2. `${XDG_CONFIG_HOME:-$HOME/.config}/paper-signal/PREFERENCES.md`

When a file exists, read `references/preferences.md` and apply its contract. Preferences refine the brief but never override the current request.

### 2. Inspect and classify inputs

For each image, label it `edit-target`, `style-reference`, `content-reference`, or `series-anchor`. Inspect local images with `view_image` before editing or using them for detailed art direction.

For an existing photo, record the subject, crop, horizon or pose, identity, light, key colors, text, and protected details. For a new image, extract one imageable core rather than illustrating every idea.

### 3. Choose subject and composition modes

Read `references/subject-routing.md`, then apply `references/visual-language.md` and select a preset from `references/presets.md`.

Choose one composition mode that serves the subject:

- `airy-fragment`
- `photo-window`
- `panorama-strip`
- `dual-frame`
- `specimen-plate`
- `portrait-archive`
- `type-object`

Lock paper family, reproduction process, type character, anchor hue, and texture intensity. Let image scale, crop, and negative space adapt to the selected mode.

### 4. Add editorial structure only when needed

For a series, read `references/content-architecture.md` and plan the swipe rhythm before styling. For facts, reviews, data, rankings, or source documents, create `evidence.json` using `references/evidence-ledger.md`. For personal sharing or recommendation copy, apply `references/human-voice.md`.

Do not make a single landscape, portrait, object, or mood poster carry a social-card evidence workflow it does not need.

### 5. Create a reproducible project

For a project that needs an artifact trail, run:

```bash
python scripts/init_project.py <topic-slug> --path <parent-directory> --cards <count> \
  --subject <subject-route> --composition <composition-mode>
```

Use a 2-5 word lowercase kebab-case slug. Create a versioned sibling when the directory exists. Follow `references/project-schema.md`.

### 6. Compile and save prompts

Read `references/prompt-compiler.md`. Save only the compact final image prompt that will reach the raster model. Use four paragraphs:

1. canvas, paper field, adaptive image geometry, and protected crop/safe zones
2. subject, spatial or identity invariants, and one physical image treatment
3. exact sparse text, type behaviour, anchor hue/form, and valid print defects
4. emotional temperature, flat-material finish, and targeted hard avoids

When editing, repeat the preservation clause in every prompt. Keep text short enough for image generation.

### 7. Confirm once, then render

Before rendering, show the route, subject route, composition mode, preset, hue, output count, edit invariants, and output directory. Ask for confirmation unless the user explicitly requested direct generation or default execution.

Then:

1. Generate a single image without an unnecessary series reference.
2. For a series, accept card 1 as the material anchor before generating later cards.
3. Generate each distinct image with a distinct call; use the accepted anchor as a style reference when supported.
4. Keep batches to four or fewer calls.
5. Inspect every result at full size and thumbnail size.
6. Retry a failed image once with one targeted correction.
7. Copy selected project-bound outputs into `outputs/` with stable filenames.

### 8. Audit and deliver

Apply `references/quality-contract.md`, then run the project validator when a project manifest exists:

```bash
python scripts/validate_project.py <project-directory> --require-images
```

Return the rendered images inline, absolute output paths, final prompt or prompt directory, detected modes, validation result, and honest caveats. Include caption and evidence files only when that route required them.

## Failure policy

- Subject lost under styling: restore crop, silhouette, horizon, face, or defining object geometry; reduce graphic intervention.
- Output resembles a generic clean poster: introduce one real image-bearing fragment, imperfect ink edges, and paper-specific tonal variation; simplify the layout.
- Output resembles a scrapbook: remove decorative layers until one reproduction process and one anchor relation remain.
- Image feels too empty for the subject: move from `airy-fragment` to `photo-window`, `panorama-strip`, `portrait-archive`, or `dual-frame`; do not fill space with arbitrary text.
- Image feels like a dashboard: retain one decision-worthy signal, collapse boxes into printed fragments, and move nuance to the caption.
- Garbled text: shorten or remove exact strings and regenerate; never overlay replacements.
- No raster backend: report the blocker and return saved prompts; do not silently ship code-rendered substitutes.

## Reference map

- `manifest.yaml`: route and progressive-loading map.
- `references/core-workflow.md`: production state machine.
- `references/subject-routing.md`: subject detection, preservation rules, and mode selection.
- `references/visual-language.md`: universal Paper Signal material and composition kernel.
- `references/presets.md`: controlled material variants.
- `references/prompt-compiler.md`: subject-aware prompt grammar.
- `references/restyle-contract.md`: existing-image invariants.
- `references/content-architecture.md`: social-series pacing and card budgeting.
- `references/evidence-ledger.md`: factual provenance.
- `references/human-voice.md`: truthful conversational copy.
- `references/quality-contract.md`: visual, factual, and delivery QA.
- `references/project-schema.md`: manifest and file schemas.
- `references/preferences.md`: optional project/user defaults and precedence.
