---
name: tokenlab-text-in-image
description: "Make images with exact, readable words in them, or fix wrong text in an image, with TokenLab image models. Use when the user says \"make a poster that says ...\", \"a sign with our shop name\", \"label design\", \"packaging mockup with the product name\", \"event flyer\", \"a UI mockup with these buttons\", \"social card with this headline\", or \"the text in this image is misspelled\". Every word must be spelled right. For a logo mark or an SVG, use tokenlab-logos-and-vectors. For a product photo where the label already exists, use tokenlab-product-photography. For a non-text change to an image, use tokenlab-edit-image."
license: MIT
metadata:
  category: image
---

# Text in Image

Make posters, signs, packaging, and mockups with words that are spelled right and easy to read. Image models still misspell words, so this skill always checks the text and fixes it.

## Inputs to collect

- **Exact copy:** every word, with the spelling and capital letters the user wants. Get it in writing; do not paraphrase.
- **Layout:** which text is the headline, which is smaller, and where each block goes (top, center, bottom, on an object).
- **Look:** letter style (bold sans-serif, thin serif, script, art deco), colors, background, and any image in the design.
- **Format:** aspect ratio or pixel size, and image count.
- **Existing image**, if the task is a text fix: a public `https` URL or a TokenLab result URL.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `text-to-image` | `ideogram-4-5` | default | New design with exact text |
| `text-to-image` | `ideogram-generate-v3-turbo` | alternative | Design with text, alternative |
| `text-to-image` | `nano-banana-pro` | alternative | Design with text, alternative (not live-tested) |
| `text-to-image` | `gpt-image-2` | alternative | Design with text, alternative (not live-tested) |
| `text-to-image` | `p-image-ideogram` | alternative | Low-cost draft |
| `image-edit` | `ideogram-4-5` | default | Fix or replace text in an image |
| `image-edit` | `nano-banana-2` | alternative | Fix text, alternative |
| `image-edit` | `gpt-image-2` | alternative | Fix text with a mask (not live-tested) |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose:

- **New design with exact text** (`text-to-image`): Ideogram 4.5 first. Ideogram V3 turbo, Nano Banana Pro, and GPT Image are alternatives. The P-Image Ideogram model is a low-cost square draft.
- **Fix text in an image** (`image-edit`): Ideogram 4.5, or Nano Banana. Use GPT Image when you need a mask.

All of these use `/v1/images/generations` for the operation shown, except GPT Image edits, which use `/v1/images/edits`. Exact fields come from each model's contract.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract for the model and operation. Note the size fields and the allowed values. On Ideogram 4.5, `quality` has different allowed values for text-to-image and image-edit.
2. Estimate the cost from `GET /v1/models/{model}/pricing`. On Ideogram 4.5 the price changes with `operation` and `quality`. Multiply by `n`.
3. Write the prompt (see Technique). Put every word to render in double quotes. Send `operation: "text-to-image"`.
4. Read the response. A sync response has `data[].url`. A response with `status: "pending"` and `poll_url` is a task: poll it every 5–10 s until `completed` or `failed`.
5. **Read every word in the result, letter by letter,** against the user's copy. Look for missing, doubled, or swapped letters and for extra text the user did not ask for.
6. If a word is wrong: generate again (a new seed often fixes it), shorten or simplify the copy, or fix only that word with an image-edit call on the result URL. Keep an image whose text is right and fix the scene, not the other way round.
7. Return the result URL, the model, the task ID, and a note that you checked the text.

## Technique

- **Quote the exact words.** Ideogram's guide: anything inside quotation marks is text to render. Type the spelling and capitals exactly as they must appear.
- **Text first.** Ideogram's guide says text named near the start of the prompt comes out more reliably than text added at the end.
- **Short copy.** Each extra word raises the odds of a typo. Titles and short lines work best. Add long body text later in a design tool.
- **Describe the letters, not a font name.** Ideogram does not load real fonts. Say "bold condensed sans-serif", "thin serif", or "tall gold art deco capitals".
- **One place and one style per block, in reading order.** "Headline \"JAZZ NIGHT\" in tall gold art deco capitals across the top. Below it, smaller text \"Friday 8pm\" in a thin gold sans-serif."
- **Forbid extra text.** End the prompt with "No other text." Google's text examples use the same line. In a 2026-10-12 test, Ideogram 4.5 spelled the copy right but added a venue line the prompt did not ask for.
- **Keep the scene simple.** A busy background leaves less room for clean letters.
- **Size controls.** The P-Image Ideogram model lists `width` and `height`, but two tests at 768 × 1024 and 1024 × 1536 both returned 1024 × 1024. Use it for square drafts only. Ideogram 4.5 with `width: 832, height: 1248` returned 1664 × 2496 (same 2:3 ratio).

## Quality bar

- Every word matches the user's copy exactly: spelling, capitals, numbers, and punctuation.
- No extra words, fake logos, or gibberish text anywhere in the image.
- The headline is readable at the size the user will show it.
- Text color has strong contrast with the background.
- Layout matches the brief: each block in its place and in the right order.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-logos-and-vectors`: logo marks and SVG output.
- `tokenlab-product-photography`: product photos that keep the real label.
- `tokenlab-edit-image`: changes that do not involve text.
- `tokenlab-prompting`: prompt craft per model family.
