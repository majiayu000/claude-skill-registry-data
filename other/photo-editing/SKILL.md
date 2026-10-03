---
name: photo-editing
description: Edit, retouch, restyle, or convert uploaded photos locally with FLUX.2 on ROCm. Use for photo edits, Fuji/film/analog looks, color grades, F1.2 bokeh looks, photoreal restyles, reference-conditioned image changes, and requests to modify an attached image. For text-to-image creation without an input photo, use create-image.
---

# Photo Editing (FLUX.2)

Use this skill for **every request to modify an uploaded real photo**: retouching, restyling, photo-to-photo generation, Fuji/底片/膠卷 looks, color grading, bokeh, or content changes.

The deployed entry point is already available. **Never write a new Diffusers/SD script and never download models.**

```bash
cd /home/chihmin/models-work/flux2
source .venv-rocm72/bin/activate
FLUX2_BIG_WMMA_LINEAR=1 python ~/.hermes/skills/create-image/scripts/create_image.py "PROMPT" --image /path/to/photo.jpg
```

The command returns JSON. Attach the `final_path` PNG in the same Discord reply:

```text
[[image: /absolute/path/to/result.png]]
```

## Required workflow

1. **Open and inspect the input image first.** Identify its source type, orientation, subject, composition, lighting, and what must remain unchanged.
2. **Research first** when the request names an unfamiliar style, person, location, franchise, product, or other meaningful term.
3. Choose the route below.
4. Attach the resulting image; do not reply with only its filesystem path.

### Route selection

| Source/request | Route |
|---|---|
| Real photo; change only photoreal look while keeping composition | `--refcontrol --image` |
| Real photo; Fuji, analog, film, 底片, 膠卷, F1.2 film look | `--image` + film wording (auto RefControl film flow) |
| Real photo; freeform content edit | `--image` |
| Photo → anime / illustration / PVC | **Do not use this skill’s FLUX path**; use `create-image` with `--anime --image` |
| Source is an anime illustration or sketch → anime restyle/CG | Use `create-image` with `--anime --image` |

> An uploaded image must be passed with `--image`; never ignore it and run text-to-image unless the user explicitly says it is only background context.

## Photoreal style changes: RefControl

For a real photo whose **style** should change while its scene/layout should remain, use `--refcontrol`. It uses the source photo plus a Depth Anything V2 depth map and a RefControl depth LoRA to structure-lock the edit.

```bash
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "cool Fuji green-cyan tones" \
  --refcontrol --image /path/to/photo.jpg
```

### Prompt discipline

- **Style-only request:** use only short target-style words. Do not repeat the subject, pose, scene, objects, composition, or generic quality tags; the photo already contains them and verbose content descriptions cause redraws.
  - Good: `cool Fuji green-cyan tones`, `Leica reportage`, `F1.2 shallow depth of field`
  - Bad: a long description of the person/room/pose already in the photo.
- **Content edit:** state what must be retained and what changes, e.g. `Keep the person, pose and composition; change the background into a rainy neon Tokyo street.`

### RefControl controls

- `--refcontrol-scale 1.0`: structure adherence; leave at default unless the user requests more/less layout preservation.
- `--lora-scale`: style/film strength. For regular film RefControl the default is 0.55; 0.4–0.5 is subtle, 0.8–0.9 strong.
- Keep `--seed` fixed while adjusting a single parameter.
- RefControl is 9B-only. Do not use `--fast-preview` with it.
- Typical 2-step portrait run: about 54 seconds end-to-end. Default is 5 steps unless specified.

## Fuji / analog / film / 底片 edits

Film words plus `--image` automatically select the structure-locked RefControl film route and load Analog Redmond. Do not add `--refcontrol` manually unless useful for clarity.

```bash
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "底片風" --image /path/to/photo.jpg
```

For the request 「F1.2 底片風」 use this exact style base (append only extra user-requested style words):

```text
analog, AnalogRedmAF, F1.2 shallow depth of field, 35mm analog film photo, soft contrast, fine film grain, subtle halation, cinematic bokeh
```

```bash
python ~/.hermes/skills/create-image/scripts/create_image.py \
  "analog, AnalogRedmAF, F1.2 shallow depth of field, 35mm analog film photo, soft contrast, fine film grain, subtle halation, cinematic bokeh" \
  --image /path/to/photo.jpg --lora-scale 0.85 --steps 2
```

### Locked film behavior

- The tool prepends the canonical RefControl/Analog Redmond film base and tuned grade automatically for photo film requests. Do **not** improvise or rewrite that base; provide only the requested extra style words.
- Film requests with no `--image` belong to `create-image`; its normal text-to-image route loads the analog LoRA.
- The Analog Redmond adapter is `analog_redmond_fluxklein9b.safetensors`, 9B-only. It is loaded on demand.
- Report that the Analog Redmond LoRA was loaded when it was applied.

## Color grade vocabulary

Keep composition fixed with a `--seed`; change only the style words:

- warm: `warm tones`, `golden / amber tone`, `warm Kodak Portra tones`
- cool: `cool tones`, `teal shadows`, `cyan-green cast`, `cool Fuji green-cyan tones`, `blue hour`
- saturation: `muted colors`, `desaturated`, `pastel palette`, `vivid colors`
- contrast: `soft contrast`, `low contrast`, `lifted blacks`, `faded blacks`, `washed-out`, `high contrast`
- film stocks: `Kodak Portra` (warm skin), `Fujicolor` (green/cyan), `Cinestill 800T` (tungsten teal/red halation), `Kodak Gold` (warm nostalgic)
- monochrome: `black and white`, `sepia`, `monochrome`

Use `--lora-scale` to vary the whole analog effect; color words only change palette/grade.

## Size and quality

Without an explicit aspect ratio, the tool follows source orientation and crops cover-style without distortion:

| Source | Generation → final |
|---|---|
| Landscape | `1248x832 → 1776x1184` (3:2) |
| Portrait | `832x1248 → 1184x1776` (2:3) |
| Square | `1024x1024 → 1440x1440` |

Use `--aspect-ratio` only when a user explicitly requests a different shape. Use `--native-1080p` only when they explicitly request native/high-quality output; it is much slower. Do not enable VAE tiling.

## Operational constraints

- Runtime: `/home/chihmin/models-work/flux2/.venv-rocm72`; ROCm 7.2 / gfx1151. No model install/download is needed.
- Do not enable `create-image-daemon.service`; a warm FLUX daemon risks OOM.
- Do not stop/restart Qwen or Gemma MTP for photo editing.
- Do not use `--fast-preview` for RefControl; it has no matching 4B LoRAs.
- Avoid prompt words that push unwanted harsh or blown-out lighting unless explicitly requested: `hard light`, `harsh light`, `overexposed`.
- If native output OOMs, report it and fall back to the normal upscale path instead of stopping other services.
