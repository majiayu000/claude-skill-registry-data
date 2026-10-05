---
name: grok-image
description: Generate images with xAI's Grok image models (grok-2-image / grok-2-image-1212). Use when the user asks for Grok-generated images, mentions xAI image generation, or wants an OpenAI-compatible image API alternative. Generation only — Grok image models do not support edit, mask, or reference-image inputs.
---

# grok-image — image generation via xAI

Calls xAI's OpenAI-compatible image endpoint with the Grok image models. One capability:

- **Generate** — text → image(s), via `scripts/generate.py`.

For the full parameter table, response shape, and pricing notes, see `references/api-reference.md`. For Python recipes (URL download, base64 decoding, batch generation, prompt revision inspection), see `references/examples.md`.

## Prerequisites

1. `XAI_API_KEY` exported in the environment (get one at https://console.x.ai/).
2. Python 3.9+ with `openai` (the OpenAI SDK works against xAI by overriding `base_url`):
   ```bash
   pip install openai
   ```
   `requests` works too if you'd rather not pull the SDK; both are shown in `references/examples.md`.

## Quickstart

```bash
# 1 image, downloaded from the returned URL
python scripts/generate.py \
  --prompt "A cinematic portrait of a woman on a Hong Kong street with a vintage tram in the background" \
  --output portrait.png

# 4 images, base64 path (no extra HTTP roundtrip)
python scripts/generate.py \
  --prompt "Isometric pixel-art of a cozy cyberpunk noodle shop" \
  --n 4 --response-format b64_json \
  --output shop.png      # writes shop_0.png ... shop_3.png

# Pin to the dated snapshot
python scripts/generate.py \
  --prompt "..." --model grok-2-image-1212 --output out.png

# Inspect what Grok actually sent to the model after revision
python scripts/generate.py --prompt "..." --output out.png --print-revised
```

## Decision rules

When the user wants an image and chooses Grok (or asks for an OpenAI-compatible alternative), use `generate.py`. If the user wants **any** of the following, this skill is the wrong tool — escalate:

- Editing an existing image, inpainting, or mask-based changes → use `gpt-image-2` (Grok image models don't expose edit endpoints).
- Reference-image composition → use `gpt-image-2`'s `images.edit` with multiple `image=` files.
- Specific output resolution or aspect ratio → Grok doesn't accept `size` / `quality`; it picks them automatically. Use `gpt-image-2` if precise sizing matters.
- Streaming partial images → not supported by Grok image API.

## Parameters cheat sheet

| Flag | Values | Default | Notes |
|------|--------|---------|-------|
| `--model` | `grok-2-image`, `grok-2-image-1212` | `grok-2-image` | Alias and dated snapshot of the same model |
| `--n` | int 1–10 | 1 | Multiple images per call |
| `--response-format` | `url`, `b64_json` | `url` | `url` returns short-lived hosted URLs; `b64_json` embeds the bytes |
| `--base-url` | str | `https://api.x.ai/v1` | Override only if proxying |
| `--print-revised` | flag | off | Prints the `revised_prompt` Grok actually used |

**Not supported by the Grok image API** (don't pass these — the call will error or be ignored):

- `size`, `quality`, `style`, `response_format=image_url` extras
- `image` / `mask` (no edit endpoint)
- `stream`, `partial_images`
- `background`, `output_format`, `output_compression`, `moderation`
- `user` (not a useful knob here)

## Things to know about Grok image models

- **Auto everything.** Resolution, aspect ratio, and "quality" are decided by the model based on the prompt. To bias it, describe the framing in the prompt itself ("vertical 9:16", "wide cinematic 21:9 crop", "ultra-detailed").
- **Prompt revision.** The API rewrites the prompt before generation and returns the rewrite as `data[].revised_prompt`. Surface this to the user when the result drifts — they may want to feed the revised prompt back in directly.
- **URL TTL.** When `response_format=url`, the URLs are short-lived. Download immediately; don't store them.
- **Pricing.** Roughly **$0.07 per output image** at the time of writing. Confirm at https://docs.x.ai/docs/models#pricing — pricing changes more often than the model.
- **Rate limits.** Tier-dependent; long batches at `n=10` can hit per-minute caps. The script doesn't auto-retry.
- **Content filtering.** Grok applies its own moderation; there's no `moderation` knob to relax it. If a prompt is rejected, rewrite rather than retry.

## When to escalate

- → `gpt-image-2` for edits, masks, multi-image composition, or precise size/quality control.
- → A diffusion model (Flux, SD, Imagen, etc.) when the user needs specific aspect ratios, ControlNet-style guidance, LoRAs, or local/offline generation.
