---
name: image
description: >-
  Generate or edit images on the user's own GPU through Guaardvark: single images,
  instruction edits, background cut-outs, inpaint and outpaint, consistent
  characters from the Cast Library, and batch runs of many prompts. Use when the user asks to create, draw, render, visualize, edit,
  or batch-generate images locally.
---

# Images with Guaardvark

Read `setup` first if the backend or the `comfyui` plugin state is unknown.

## One image: MCP `generate_image`

- `prompt` is scene, pose, lighting, setting. Plain prose. Do not paste JSON or tag soup; the
  default model (Z-Image Turbo) reads prompts as language, and SD-era tag lists hurt it.
- `model` default `auto` picks the best downloaded model. Only override when the user names one:
  `zimage-turbo`, `krea2-turbo`, `krea2-raw`, `flux-dev`, `sd-xl`, `sdxl-turbo`,
  `realistic-vision`, `epic-realism`.
- `width` / `height`: 512, 768 or 1024. `style`: realistic, artistic, anime, photographic, digital-art.
- **Consistent character**: pass `subject_ids=[<cast id>]` as its own array. Never put the
  trigger word alone in the prompt and expect the LoRA to load. Find ids with
  `GET /api/cast-library` (see the cast skill).
- On-image text: quote the exact words in double quotes inside the prompt.
- The tool returns the image URL (`/api/outputs/generated_images/<file>.png`, relative to the
  backend), the model that ran, steps, seed and whether a Cast LoRA was applied. Show the URL
  and the prompt you used. Measured: 768x768 on Z-Image Turbo in ~20 s on a free 16 GB card.
- **Over MCP the call queues by default** (`wait_for_result` defaults to false there) and
  returns `Image queued as batch ImageBatch_...` at once. Poll
  `get_generation_status(batch_id=...)` every few seconds until `completed`; it returns the
  file URL. Pass `wait_for_result: true` to block for the render instead (allowed up to 30
  minutes). A call that exceeds the server's timeout answers with an error that says the
  render is still running; it is not lost.
- A failed call carries the backend's reason (plugin off, out of memory, bad model). Read it
  and act on it; `inspect_gpu` and `GET /api/plugins/status` are the two checks that resolve most.

## Photo edits over MCP run as jobs

`edit_image`, `inpaint_image`, `outpaint_image` and `remove_background` answer at once over
MCP with `... queued as job tooljob_...`: the work runs in the Guaardvark backend and keeps
going if the client disconnects. Poll `get_generation_status(batch_id="tooljob_...")` every few
seconds until `done` (it gives the file URL) or `failed` (it gives the error). Pass
`wait_for_result: true` to wait up to 60 s (half the server's MCP timeout when that is
shorter) for the result; a longer edit still comes back as the job id. A Qwen-Image-Edit takes
about three minutes on a 16 GB card, and a job waits its turn while another render holds the GPU.

## Edit an existing image: MCP `edit_image`

- `instruction` is the change ("put a cowboy hat on him", "make the shirt red"). The image the
  user just attached is used automatically; otherwise pass `image` as a path or URL.
  Optional `reference_image_2` / `reference_image_3` (Qwen-Image-Edit only) for extra people or
  style; the call is refused when a reference cannot be read or the edit would run on another backend.
- `model` `auto` uses **Qwen-Image-Edit** when installed, else FLUX.1 Kontext. With neither
  installed the call is refused and names the pack; relay that instead of retrying.
  Override with `qwen-image-edit` or `kontext`. Install those packs from Manage Image Models →
  Image editing (`qwen-image-edit`, `flux-kontext-dev`) — do not Install unless the user asked.
  Naming another downloaded image model runs a light img2img pass that keeps most of the picture.
- Same canvas, same pose. For a brand-new picture use `generate_image`. For a **new scene
  that keeps a face** use `generate_identity`.

## New scene from a face: MCP `generate_identity` (off by default)

- Not exposed unless the server runs with `GUAARDVARK_IDENTITY_TOOL=1`: the likeness it keeps
  has not passed verification yet. If the tool is absent, say so and offer `edit_image` instead.
- Attach a likeness the user has the right to use (their photo or a Cast subject they uploaded).
  `consented` must be `true`. Refuse if they have not confirmed that.
- `prompt` is the new scene. Needs the PuLID identity pack (`pulid-flux`; Manage Image Models →
  Image editing installs it with its face files, EVA02-CLIP and `flux-dev`). Comfy must have
  been restarted after the PuLID-Flux custom node was added.
- This is not a face swap onto an existing poster, and not an instruction edit of the same photo.

## Background remove: MCP `remove_background`

- Cuts the subject out of the attached photo (transparent PNG). ONNX matting, no diffusion;
  needs a background-removal model from Manage Image Models → Image editing.
- For a new background, remove first then `edit_image` / `generate_identity`, or describe the
  new scene in `edit_image` if Qwen-Image-Edit is installed.

## Inpaint / outpaint

- `inpaint_image`: change or remove something ("remove the coffee cup"). Runs on Qwen-Image-Edit
  or FLUX.1 Kontext; refused when neither is installed.
- `outpaint_image`: extend the canvas (`left`/`right`/`top`/`bottom` pixels) and fill. Prefers Qwen.

## Many images: REST batch

```bash
B=${GUAARDVARK_URL:-http://localhost:5000}
curl -s -X POST $B/api/batch-image/generate/prompts -H 'Content-Type: application/json' -d '{
  "prompts": ["prompt one", "prompt two"],
  "model": "auto",
  "subject_ids": []
}'
```
- `prompts` may be strings or `{"prompt": "..."}` objects. There is a per-batch maximum; if the
  server answers 400 "Too many prompts", split the list.
- Optional `adapters` (user LoRAs from the models skill) and `subject_ids` (Cast Library).
- The response is `data.batch_id` (`ImageBatch_<date>_<n>`). Poll
  `GET $B/api/batch-image/status/<batch_id>?include_results=true`: `status` goes
  running → completed, with `completed_images` / `total_images`, `output_dir`, and one
  `results[]` entry per prompt (`success`, `image_path`, `thumbnail_path`, `generation_time`,
  `metadata.model_used`). A contact sheet: `GET $B/api/batch-image/preview/<batch_id>`; one file:
  `GET $B/api/batch-image/image/<batch_id>/<image_name>` (the basename of `image_path`).
  Cancel with `POST $B/api/batch-image/cancel/<batch_id>`. Measured: one 1024x1024 prompt
  completed in ~30 s.
- Helpers: `POST /api/batch-image/enhance-prompt`, `/analyze-prompt`, `/expand-concept` (JSON
  body with the prompt) when the user wants prompt help before spending GPU time.

## Rules

- Say which model actually ran (the response names it). Do not promise a model that is not installed.
- Generation time depends on the GPU; a first image after Ollama held the card can take longer
  because the orchestrator swaps models. That is normal.
- Never upload the user's images anywhere. Everything here is local.
