---
name: tokenlab-photoreal-stills
description: "Make realistic photos of people, places, food, interiors, and scenes from a written brief with TokenLab image models. Use when the user says \"a realistic photo of ...\", \"looks like a real photograph\", \"stock photo of a team meeting\", \"food photo for the menu\", \"travel photo\", \"candid street shot\", \"editorial portrait\", or \"hero background image\". The skill writes the prompt like a photographer and picks a photoreal model. For a product as the subject, use tokenlab-product-photography. For readable words in the image, use tokenlab-text-in-image. For the same person across several images, use tokenlab-character-consistency. To change an existing photo, use tokenlab-edit-image."
license: MIT
metadata:
  category: image
---

# Photoreal Stills

Make images that look like real photographs. The prompt does most of the work: subject, action, place, light, and camera, in that order.

## Inputs to collect

- **Subject and action:** who or what, doing what.
- **Place and time:** setting, time of day, weather, season.
- **Look:** documentary, editorial, stock, cinematic, or a film look.
- **Format:** aspect ratio or pixel size per use (16:9 hero, 4:5 feed, 1:1 card), and image count.
- **Limits:** no real, named people without consent; no brand logos the user does not own.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `text-to-image` | `flux-2-pro` | default | General photoreal |
| `text-to-image` | `flux-2-max` | alternative | Highest-detail hero image (not live-tested) |
| `text-to-image` | `seedream-5.0-pro` | alternative | Photoreal, alternative look (not live-tested) |
| `text-to-image` | `krea-2-large` | alternative | Photoreal, alternative look (not live-tested) |
| `text-to-image` | `stable-image-ultra` | alternative | Photoreal, alternative look (not live-tested) |
| `text-to-image` | `flux-2-klein-9b` | alternative | Low-cost draft |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose:

- **General photoreal:** FLUX.2. Its top tier gives the most detail for a hero image.
- **Alternative look:** Seedream, Krea, or Stable Image Ultra.
- **Low-cost draft:** a FLUX.2 Klein model.

All use `/v1/images/generations`. Send `operation: "text-to-image"` when the contract lists `operation` (Stable Image Ultra lists only `prompt` and `aspect_ratio`). Exact fields come from each model's contract.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract. Note the size field: `resolution` as `WIDTHxHEIGHT`, `aspect_ratio`, `width` / `height`, or none. Send only listed fields.
2. Estimate the cost from `GET /v1/models/{model}/pricing`: price per image times the image count.
3. Write the prompt (see Technique). Set the frame size for the use.
4. Read the response. A sync response has `data[].url`. A response with `status: "pending"` and `poll_url` is a task: poll it every 5–10 s until `completed` or `failed`. In tests, a FLUX.2 model returned a task without `async: true`.
5. Check the result against the Quality bar. Re-run with a changed prompt, not the same one, when a detail is wrong.
6. Return the result URLs, the model, the task IDs, and the prompt you sent.

## Technique

- **Order the prompt by priority.** Black Forest Labs' FLUX.2 guide: "Subject + Action + Style + Context", and word order matters because the model pays more attention to what comes first.
- **Aim for 30–80 words.** The FLUX.2 guide calls this range usually ideal. Go longer only for complex scenes.
- **Name the camera, lens, and light.** "Shot on Fujifilm X-T5, 35mm f/1.4" gives a more real result than "professional photo" (FLUX.2 guide). Add the light: "warm tungsten stall lights", "overcast soft daylight", "low sun from behind".
- **Use positive words, not negatives.** FLUX.2 does not support negative prompts. Say "sharp focus throughout", not "no blur".
- **Colors by hex.** For brand colors on FLUX.2, tie the code to an object: "the awning is color #1F6F5C".
- **Skin and hands.** Ask for "natural skin texture" and keep hands in a simple pose, such as holding one object. Check fingers in every result.
- **Frame size.** On the FLUX family, `resolution` takes pixels: a FLUX.2 Klein model with `1344x768` returned 1344 × 768. A wrong value returns `400` with `param: "resolution"`. P-Image lists `width` / `height`, but a 768 × 768 test returned 1024 × 1024; use it for square drafts.
- **Draft cheap, then finish.** Explore the composition with a low-cost model, then run the chosen prompt on the default for the final image.

## Quality bar

- Looks like a photo: real light falloff, believable depth of field, no plastic skin, no painted look.
- Hands, teeth, eyes, and text-like shapes in the background have no obvious errors.
- Light direction and color are the same on the subject and the background.
- The frame size and aspect ratio fit the use.
- No real person's likeness or brand mark that the user did not ask for.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-product-photography`: a product as the subject.
- `tokenlab-text-in-image`: readable words in the image.
- `tokenlab-character-consistency`: the same person across a series.
- `tokenlab-edit-image`: change an existing photo.
- `tokenlab-prompting`: prompt craft per model family.
