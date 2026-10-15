---
name: tokenlab-character-consistency
description: "Keep one character, mascot, person, or product looking the same across many new images and short video clips with TokenLab models. Use when the user says \"same character in different scenes\", \"keep her face the same\", \"make a series with our mascot\", \"storyboard with the same hero\", \"this person at the beach, then in an office\", \"consistent character\", or \"turn these character images into a short clip\". The skill makes or takes one anchor image and generates every new scene from it. For one change to a single image, use tokenlab-edit-image. For a product shoot, use tokenlab-product-photography. To animate one still without references, use tokenlab-animate-image."
license: MIT
metadata:
  category: image
---

# Character Consistency

Show the same character in new scenes, poses, and clips. The method: lock one anchor image, then pass it as a reference to every new generation. Never regenerate the character from text alone.

## Inputs to collect

- **Anchor image**, if the user has one: a public `https` URL or a TokenLab result URL. A clear, front-facing, evenly lit image works best.
- **Character sheet in words:** face, hair, eye color, age range, body type, clothing, and one or two marks that must not change (freckles, a scar, a logo on the shirt).
- **Scenes:** one line per new image or clip: place, action, camera angle, light.
- **Format:** aspect ratio per scene, image count, and for clips the duration and resolution.
- **Rights:** the user owns or has permission to use any real person's image.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `image-to-image` | `nano-banana-2` | default | New scene from the anchor |
| `image-to-image` | `ideogram-character-remix-v3` | alternative | New scene, alternative (not live-tested) |
| `image-to-image` | `seedream-5.0` | alternative | New scene, alternative (not live-tested) |
| `image-to-image` | `nano-banana-2-lite` | alternative | Low-cost new scene (not live-tested) |
| `text-to-image` | `nano-banana-2` | default | Make the anchor image |
| `text-to-image` | `flux-2-pro` | alternative | Anchor image, alternative |
| `text-to-image` | `ideogram-character-v3` | alternative | New image from one face reference (not live-tested) |
| `text-to-image` | `p-image` | alternative | Low-cost anchor |
| `reference-to-video` | `grok-imagine-video` | default | Short clip with the character |
| `reference-to-video` | `kling-omni-video` | alternative | Clip, alternative (not live-tested) |
| `reference-to-video` | `seedance-2.0` | alternative | Clip with many references |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose, by stage:

- **Anchor** (`text-to-image`): Nano Banana or FLUX.2. Ideogram Character makes a new image from one face reference. P-Image is the low-cost anchor.
- **New scene** (`image-to-image`): Nano Banana first. Ideogram Character remix and Seedream are alternatives. The Nano Banana lite tier is the low-cost option.
- **Clip** (`reference-to-video`): Grok Imagine video for a short clip, Kling Omni video as an alternative, Seedance 2 when you have many references.

Exact fields and reference limits come from each model's contract. `references/request-bodies.md` has tested bodies for the anchor, a new scene, and a clip.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract for each model and operation. Note the reference field (`image_urls`, `reference_image_urls`, `image_url`, or `reference_images`), its maximum item count, and the size fields.
2. Estimate the cost: price per image times scenes, plus price per second times clip length for video. Video is priced per second and can add a per-reference-image charge; read the pricing formula. Tell the user the total before a batch or any video.
3. **Anchor.** Use the user's image, or generate one from the character sheet. Show it to the user. Every later call depends on it, so get approval before you go on.
4. **Scenes.** For each scene, call the image-to-image model with the anchor URL in the reference field and a prompt that restates the character sheet plus the new scene. One scene per call.
5. Read each response. A sync response has `data[].url`. A response with `status: "pending"` and `poll_url` is a task: poll it every 5–10 s until `completed` or `failed`.
6. Compare every result with the anchor (face shape, hair, eyes, clothing, marks). Re-run only the scenes that drift. Do not use a drifted result as a new reference.
7. **Clip (optional).** Send the anchor plus one or two approved scene images to the reference-to-video model. Video is always async: store the task ID, then poll.
8. Return each result URL with its scene line, the model, and the task IDs.

## Technique

- **Repeat the character sheet in every prompt.** Start with "The same woman from the reference image:" and list the fixed traits. Then describe the new scene. The model does not remember earlier calls.
- **Change one axis at a time.** New place, or new pose, or new outfit. A prompt that changes all three makes drift more likely.
- **Keep references clean.** Use the anchor and approved results only. A blurry or off-model reference spreads its errors.
- **Name the clothing, even when it stays the same.** "same mustard yellow knit sweater" holds the outfit better than "same clothes".
- **Reference counts are per model.** `ideogram-character-*` takes one reference image. Grok Imagine video reference-to-video takes up to 7. Read the contract limit for other models before you send more than one.
- **Video prompts describe motion only.** The references carry the look. "She turns her head toward the camera and smiles. Static camera." Keep the clip short for a first test.

## Quality bar

- Face shape, hair, eye color, skin marks, and clothing match the anchor in every image and clip frame.
- Proportions and age stay the same across scenes.
- Each scene shows the place, action, and angle from its scene line.
- No extra people who look like the character, and no merged faces.
- Clips keep the face stable from the first to the last frame.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-edit-image`: one change to a single image.
- `tokenlab-product-photography`: the same product across catalog shots.
- `tokenlab-animate-image`: animate one still image.
- `tokenlab-prompting`: prompt craft per model family.
