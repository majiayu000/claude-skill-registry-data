---
name: Draw Image
skill_key: draw_image
description: Generate an image from a text prompt using the default OpenAI-like LLM config (gpt-image-1-mini or compatible image generation API). The image is uploaded to the gofile.io public file sharing service and ONLY the public download page URL is returned.
instructions: Call by agent when user asks to draw, paint, generate, or create an image.
requires:
  always: true
runner:
  kind: python_file
  target: draw.py
---

# Draw Image

Generate images via the OpenAI-compatible `images/generations` endpoint using the default LLM configuration.

## Parameters

This skill accepts a JSON object as input params.

- `prompt` (string, **required**)
  - The text description of the image to generate.

- `size` (string, optional)
  - Image dimensions. Default: `1024x1024`
  - Common values: `1024x1024`, `1792x1024`, `1024x1792`

- `model` (string, optional)
  - The image generation model name. Default: `gpt-image-1-mini`

- `quality` (string, optional)
  - Image quality. Values: `low`, `medium`, `high`. Default: `low`

- `n` (integer, optional)
  - Number of images to generate. Default: `1`

## How to use

1. Call `read_skill` with `skill_key: "draw_image"` to read this document.
2. Then call `run_doc_skill` with `skill_key: "draw_image"` and `params`.

Example:

```json
{
  "skill_key": "draw_image",
  "prompt": "A futuristic cityscape at sunset with flying cars",
   "size": "1024x1024"

}
```

## Output

The runner prints a JSON object to stdout with:

- `ok` (bool): Whether the generation and upload succeeded.
- `download_page` (string): The public gofile.io download page URL of the generated image. **Only this URL is returned** as the result. Open this URL in a browser to download the generated image.
- `note` (string): A short hint explaining that `download_page` is used to download the generated image.
- `error` (string): Error message on failure.

Example success output:

```json
{
  "ok": true,
  "download_page": "https://gofile.io/d/WcWZKt",
  "note": "Use this URL to download the generated image."
}
```
