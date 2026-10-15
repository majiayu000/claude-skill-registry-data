---
name: tokenlab-logos-and-vectors
description: "Make logo marks, app icons, badges, and flat vector-style graphics, then convert them to SVG, with TokenLab image models. Use when the user says \"design a logo\", \"make an icon for my app\", \"simple mark for my brand\", \"flat illustration\", \"I need this as an SVG\", \"vectorize this logo\", or \"turn this PNG into a vector\". The skill makes a raster mark first, then vectorizes it. For a poster or label with readable words, use tokenlab-text-in-image. For a realistic photo, use tokenlab-photoreal-stills. To change an existing raster image, use tokenlab-edit-image."
license: MIT
metadata:
  category: image
---

# Logos and Vectors

Make a simple mark or icon and deliver it as an SVG. The text-to-image models here return raster images (PNG or JPEG). A second step turns the chosen raster into an SVG.

## Inputs to collect

- **Brand name and what it does:** one line.
- **Mark type:** symbol only, symbol plus name, or name only (wordmark).
- **Style:** flat, geometric, line, rounded, hand-drawn; number of colors and the colors (hex if the user has them).
- **Use:** app icon, favicon, website header, print. Small uses need fewer, thicker shapes.
- **Existing raster logo**, if the task is vectorize-only: a public `https` URL or a TokenLab result URL.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `text-to-image` | `recraft-v4.1` | default | Mark or icon (raster) |
| `text-to-image` | `recraft-v4.1-pro` | alternative | Mark at a larger size (not live-tested) |
| `text-to-image` | `ideogram-4-5` | alternative | Mark with words |
| `text-to-image` | `recraft-v4.1-flash` | alternative | Low-cost draft |
| `image-edit` | `recraft-vectorize` | default | Raster to SVG |
| `image-edit` | `picsart-image-vectorizer` | alternative | Raster to SVG, alternative |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose, by stage:

- **Mark or icon** (`text-to-image`): Recraft V4.1. Use the Pro tier for a larger size and the Flash tier for a low-cost draft. Use Ideogram 4.5 when the mark has words.
- **Raster to SVG** (`image-edit`): Recraft vectorize, or the Picsart vectorizer as an alternative.

All use `/v1/images/generations`. Exact fields come from each model's contract.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract for each model. Each Recraft V4.1 text-to-image model lists one `size` value and `n` `1` only: `1024x1024` for the base and Flash tiers, `2048x2048` for the Pro tier.
2. Estimate the cost from `GET /v1/models/{model}/pricing`: marks times the price per image, plus one vectorize call per chosen mark.
3. **Marks.** Generate 3–4 options, one call each, with different shape ideas (see Technique). Send `operation: "text-to-image"`, the model's one `size` value, and `n: 1`.
4. Read each response. A sync response has `data[].url`. A response with `status: "pending"` and `poll_url` is a task: poll it every 5–10 s until `completed` or `failed`.
5. Let the user pick one mark. Vectorize only the pick.
6. **SVG.** Send `{"model": "MODEL_ID", "operation": "image-edit", "image_url": "MARK_URL"}`. Take `MODEL_ID` from the Models list above for the vectorize (`image-edit`) operation. Do not send `output_format: "svg"`; it returns `400` (the field accepts only `png`, `jpeg`, `webp`). Leave `output_format` out.
7. Download the result and check the file. In tests, both vectorizers returned real SVG (`Content-Type: image/svg+xml`) although the result URL ends in `.png`. Save it with a `.svg` name.
8. Return the SVG file or URL, the raster URL, the model per stage, and the task IDs.

## Technique

- **Say "flat vector logo mark" first.** Recraft's own API example uses the style cue "flat vector" in the prompt.
- **Few shapes, few colors.** "A simple rounded bread loaf made of two solid colors, warm orange and dark brown." Simple shapes vectorize into clean paths; gradients, shadows, and texture turn into hundreds of small shapes.
- **Plain white background, centered, no text.** Add "No text, no gradients, no shadows" unless the user wants a wordmark.
- **Words in a logo:** make the wordmark with `tokenlab-text-in-image` (quoted text, letter style described), check the spelling, then vectorize that result.
- **The background becomes a shape.** Both vectorizers put the white background into the SVG as a full-size filled path. Delete that path (or set it to `none`) when the user needs a transparent mark.
- **Check small sizes.** Look at the mark at 32 px. If it turns into a blob, ask for fewer, thicker shapes.

## Quality bar

- The mark reads clearly at 32 px and at full size.
- Only the colors the user asked for, as flat fills.
- The SVG opens in a browser, has a small number of paths, and has no raster image embedded.
- Any words are spelled right.
- The mark does not copy a known brand's logo.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-text-in-image`: wordmarks and posters with exact text.
- `tokenlab-edit-image`: change an existing raster image.
- `tokenlab-photoreal-stills`: realistic photos.
