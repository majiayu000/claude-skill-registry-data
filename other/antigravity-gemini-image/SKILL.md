---
name: antigravity-gemini-image
description: Generate or edit images using the Antigravity-hosted Gemini image model via the local gateway. Use when the user asks to create an image, generate an avatar, or edit/transform an existing image with text instructions. Supports text-to-image and image-to-image editing.
---

# Antigravity Gemini Image

## Overview
Use the Gemini REST endpoint (via the local gateway base URL) to create or edit images. This skill wraps the correct request format for the **gemini-3.1-flash-image** model, which does **not** work reliably with `/v1/responses` + `image_generation`.

## Quick start

### Text → Image
```bash
mkdir -p ~/.openclaw/workspace/tmp
/usr/bin/python3 {baseDir}/scripts/generate_gemini_image.py \
  --prompt "A cute yellow chick mascot, vector style" \
  --out ~/.openclaw/workspace/tmp/chick.jpg
```

### Image → Image (edit)
```bash
mkdir -p ~/.openclaw/workspace/tmp
/usr/bin/python3 {baseDir}/scripts/generate_gemini_image.py \
  --prompt "Add a tiny red scarf, keep the style" \
  --image /path/to/input.jpg \
  --out ~/.openclaw/workspace/tmp/chick_edit.jpg
```

Optional (explicit .env path):

```bash
/usr/bin/python3 {baseDir}/scripts/generate_gemini_image.py \
  --env-file ~/.openclaw/workspace/.env \
  --prompt "A cute yellow chick mascot, vector style" \
  --out ~/.openclaw/workspace/tmp/chick.jpg
```

macOS Keychain (optional): service `openclaw-local-160`, accounts `base-url` and `api-key`.

## Workflow (always follow)
1) Confirm the prompt (and optional input image) with the user.
2) Run the script in `scripts/generate_gemini_image.py`.
3) Return the generated image file to the user.

## Parameters
- `--prompt` (required): text instruction.
- `--image` (optional): input image for edits.
- `--out` (required): output path (jpg/png).
- `--env-file` (optional): load a specific `.env` file.
- `--base-url` (optional): defaults to `LOCAL_160_BASE_URL`.
- `--api-key` (optional): defaults to `LOCAL_160_API_KEY`.
- `--model` (optional): defaults to `gemini-3.1-flash-image`.
- `--temperature` (optional): default 0.3.
- `--size` (optional): default **4K** (set via `GEMINI_IMAGE_SIZE`).
- `--ratio` (optional): default **16:9** (set via `GEMINI_IMAGE_RATIO`).
- `--timeout` (optional): HTTP 超时（秒），默认 1200（也可用 `GEMINI_IMAGE_TIMEOUT` 或 `LOCAL_160_TIMEOUT`）。

## Notes
- The gateway endpoint is:
  `POST {BASE_URL}/v1beta/models/gemini-3.1-flash-image:generateContent`
- Auth header uses `x-goog-api-key`.
- Image generation can be slow; 10–20 minutes is possible. Keep timeouts high (default 1200s or override via `--timeout` / env).
- Output image is returned as base64 under:
  `candidates[0].content.parts[*].inlineData.data`.
- 4K 输出必须写在 `generationConfig.imageConfig`（**不要**直接写 `image_size`）：
  ```json
  {"imageConfig": {"imageSize": "4K", "aspectRatio": "16:9"}}
  ```

## References
- See `references/API.md` for request/response shape.
