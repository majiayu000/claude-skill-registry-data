---
name: gpt-image-2
description: Generate and edit images with OpenAI's gpt-image-2 model. Use when the user asks to create, generate, render, edit, modify, inpaint, or composite images via OpenAI / GPT Image. Supports text-to-image generation, single- and multi-image edits, mask-based inpainting, reference-image composition, and transparent backgrounds via gpt-image-1.5.
---

# gpt-image-2 — image generation & editing

Calls OpenAI's Image API with the `gpt-image-2` model (default). Switch to `gpt-image-1.5` with `--model gpt-image-1.5` when you need transparent backgrounds. Two capabilities:

- **Generate** — text → image (`scripts/generate.py`)
- **Edit** — image(s) + optional mask → image (`scripts/edit.py`)

For full parameter reference and advanced patterns (Responses API multi-turn, streaming, custom resolutions), see `references/api-reference.md` and `references/examples.md`.

## Prerequisites

1. `OPENAI_API_KEY` exported in the environment.
2. Python 3.9+ with `openai` installed. If `Pillow` is needed for mask alpha-channel fixup, install `pillow` too.
   ```bash
   pip install openai pillow
   ```
3. The OpenAI org must be **API-verified** to call GPT Image models. If a 403 mentions verification, point the user to https://platform.openai.com/settings/organization/general.

## Quickstart

### Generate
```bash
python scripts/generate.py \
  --prompt "A children's book drawing of a vet listening to a baby otter's heartbeat" \
  --output otter.png \
  --size 1024x1024 \
  --quality medium
```

### Generate with transparent background (requires `--model gpt-image-1.5`)
```bash
python scripts/generate.py \
  --model gpt-image-1.5 \
  --prompt "A shiny red apple on a transparent background" \
  --output apple.png \
  --background transparent
```

### Edit (single image, prompt-only)
```bash
python scripts/edit.py \
  --image input.png \
  --prompt "Add a small red balloon in the upper-left corner" \
  --output edited.png
```

### Edit with mask (inpainting)
```bash
python scripts/edit.py \
  --image sunlit_lounge.png \
  --mask mask.png \
  --prompt "A pool containing a flamingo" \
  --output lounge.png
```

### Edit using multiple references (composition)
```bash
python scripts/edit.py \
  --image lotion.png bath-bomb.png incense.png soap.png \
  --prompt "A photorealistic gift basket on a white background labeled 'Relax & Unwind' containing all the items in the references" \
  --output basket.png
```

## Decision rules

When the user asks to make/edit an image, follow this order:

1. **Pure text → image** → use `generate.py`.
2. **Has 1+ input images, no specific region** → use `edit.py` (the model treats them as references).
3. **Has 1 input image + a region to change** → use `edit.py` with `--mask`. The mask must:
   - Be the **same dimensions and format** as the first input image.
   - Have an **alpha channel** where transparent = "edit this area", opaque = "keep this area".
   - If the user supplies a black-and-white mask, run `scripts/edit.py --fix-mask <path>` first (auto-adds alpha) — see `references/examples.md`.

## Parameters cheat sheet

| Flag | Values | Default | Notes |
|------|--------|---------|-------|
| `--size` | `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, custom `WxH`, or `auto` | `auto` | Both edges multiples of 16; max edge 3840; ratio ≤ 3:1; total pixels in [655 360, 8 294 400] |
| `--quality` | `low`, `medium`, `high`, `auto` | `auto` | Use `low` for drafts; `medium`/`high` for final |
| `--format` | `png`, `jpeg`, `webp` | `png` | `jpeg` is fastest |
| `--compression` | 0–100 | unset | Only with `jpeg` / `webp` |
| `--n` | int ≥ 1 | 1 | Multiple images per call |
| `--moderation` | `auto`, `low` | `auto` | `low` is less restrictive |
| `--model` | `gpt-image-2`, `gpt-image-1.5` | `gpt-image-2` | `gpt-image-1.5` supports `transparent` backgrounds |
| `--background` | `auto`, `opaque`, `transparent` | `auto` | `transparent` only works with `--model gpt-image-1.5` |

## Things to know about `gpt-image-2`

- **Transparent backgrounds need `gpt-image-1.5`.** `gpt-image-2` does not support `--background transparent`; use `--model gpt-image-1.5 --background transparent` instead.
- **Always high-fidelity inputs.** The `input_fidelity` param does not apply — every reference image is processed at high fidelity (and counted as more input tokens accordingly).
- **Latency.** Complex prompts at `high` quality can take up to ~2 min. Use `low` while iterating, then re-run at `high`.
- **Cost (USD per output image, approximate):** low `1024x1024` ≈ $0.006, medium ≈ $0.053, high ≈ $0.211. Larger sizes cost more. See `references/api-reference.md` for the full table.
- **Output is base64.** Both scripts decode and write the bytes to `--output`; no manual base64 handling needed.

## When to escalate to the Responses API

The Image API (used by these scripts) is the right call for one-shot generate/edit. Switch to the Responses API instead when the user wants:

- **Multi-turn iterative editing** ("now make it realistic", "now add a hat") with conversation state via `previous_response_id`.
- **Streaming partial images** (1–3 progressive previews while the final renders).
- **Mixed text + image conversations** where the LLM decides whether to generate or edit.

`references/examples.md` has working snippets for both.
