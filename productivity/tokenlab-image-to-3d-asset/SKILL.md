---
name: tokenlab-image-to-3d-asset
description: "Turn a product photo, a concept image, or a text description into a downloadable 3D model (GLB and other formats) with TokenLab 3D models. Use when the user says \"make a 3D model of this\", \"turn this photo into a GLB\", \"3D asset for my game\", \"3D version of my product for AR\", \"text to 3D\", or \"I need a mesh of a chair\". Prepares a clean single-object input, runs the async job, and returns the model file URLs. For a whole explorable scene or room instead of one object, use tokenlab-world-generation. To clean up the source photo first, use tokenlab-product-photography."
license: MIT
metadata:
  category: 3d
---

# Image to 3D Asset

Make one downloadable 3D object from an image or a short description. 3D jobs are async and paid per request, so the main levers are a clean input and the right model for the use (web preview, game, AR, or print).

## Inputs to collect

- **Source:** an image (public `https` URL or a TokenLab result URL) or a text description.
- **The object:** what it is, and what is not part of it (table, background, hands).
- **Use:** web or AR preview, game asset, or 3D print. This decides file format and how heavy the mesh may be.
- **Format:** `glb` for web and most tools; `fbx`, `obj`, or `usdz` only when the model returns them.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `image-to-3d` | `tripo-h3.1` | default | Photo or text to a 3D object |
| `image-to-3d` | `rodin-gen-2` | alternative | Lighter mesh for games or the web |
| `image-to-3d` | `seed3d-2.0` | alternative | Photo to 3D, alternative (not live-tested) |
| `image-to-3d` | `tripo-p1.0` | alternative | Alternative (not live-tested) |
| `image-to-3d` | `meshy-6` | alternative | Alternative (not live-tested) |
| `text-to-3d` | `tripo-h3.1` | default | Photo or text to a 3D object |
| `text-to-3d` | `rodin-gen-2` | alternative | Lighter mesh for games or the web |
| `text-to-3d` | `tripo-3d-v3-1` | alternative | Text to 3D, alternative (not live-tested) |
| `text-to-3d` | `tripo-p1.0` | alternative | Alternative (not live-tested) |
| `text-to-3d` | `meshy-6` | alternative | Alternative (not live-tested) |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose:

- **Photo or text to one 3D object:** Tripo (H3.1). It gives a detailed, heavy mesh.
- **Lighter mesh for games or the web:** Rodin.
- **Alternatives:** Seed3D for photo to 3D, an earlier Tripo tier for text to 3D, Tripo P1.0, and Meshy. Confirm the operation in the contract.

Exact fields, operations, and output formats come from the model contract.

In a 2026-10-12 check on the same mug photo, Tripo (H3.1) returned a 43 MB GLB with about 755k vertices, and Rodin returned a 7 MB GLB with about 17k vertices. Check size before you ship a model to a web page or a game.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL_ID --operation image-to-3d`. Take `MODEL_ID` from the Models list above. Confirm the model publishes the operation you need (`image-to-3d` or `text-to-3d`). Send only fields in `supported_parameters`.
2. Do not send `operation`. `/v1/3d/generations` infers it: `prompt` alone is text-to-3d; `image` or `image_url` makes it image-to-3d. Some contracts list `operation`; requests without it still work.
3. Estimate with `GET /v1/models/{model}/pricing`. Prices are per request and can differ by operation and option. Read the entry that matches your operation and the `default_selection`. Example: for Tripo (H3.1) image-to-3d, read the entry for the default `texture: none` selection; that is the price per model. Tell the user before you start.
4. Check the input URL opens without login. Then call and wait: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/3d/generations --json @body.json --wait --interval 8`. Save the task `id` and `poll_url` first. Jobs took about 2–4 minutes in testing. On a timeout, resume with `poll TASK_ID`.
5. Read the result: `model_url` always; `glb_url`, `fbx_url`, `obj_url`, `usdz_url` when the model returns them. Some models also return a preview render in `output`. URLs stay valid for 30 days.
6. Download the file. Check it is a real model file (a GLB starts with the bytes `glTF`), its size, and a preview. Return the URLs, model, and task ID.

Body examples (take `MODEL_ID` from the Models list above):

```json
{"model": "MODEL_ID", "prompt": "A white ceramic mug with a bare tan clay base and a rounded handle. Only the mug, no table or background.", "image_url": "https://..."}
{"model": "MODEL_ID", "prompt": "a stylized low-poly robot mascot, rounded body, short antenna"}
```

## Technique

- **One object, full view.** Use an image where the whole object is in frame, not cut off, and not covered by other things. A product photo on a plain background works best.
- **Name the object and exclude the rest.** With an image, the `prompt` should say what the object is and what is not part of it: "only the mug, no table or background". In testing this kept the table out of the mesh.
- **Clean the photo first** when the background is busy: cut it out with `tokenlab-product-photography` (background removal) and send that result URL.
- **Text prompts:** object, shape, material, style, and level of detail. "a weathered wooden treasure chest with iron bands, game-ready, stylized". Leave out scenes and lighting.
- **Keep the user's product true.** Compare the preview with the photo: shape, proportions, handle, colors, and labels.
- **Format by use:** `glb` for web and most engines; `usdz` for Apple AR; `fbx` or `obj` for DCC tools. If the format you need is missing, use `model_url` and convert, or pick a model that returns it.
- **Retries cost.** Each new task is a new charge. Fix the input before you retry.

## Quality bar

- The model is the requested object only, with no table, floor, or background stuck to it.
- Shape, proportions, and colors match the source image.
- The file opens as a valid model, in the requested format, with a size that fits the use.
- The final answer has the model URL(s), model ID, task ID, and the estimate the user saw.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-world-generation`: an explorable scene instead of one object.
- `tokenlab-product-photography`: a clean product shot to use as input.
- `tokenlab-edit-image`: remove a background or extra objects first.
