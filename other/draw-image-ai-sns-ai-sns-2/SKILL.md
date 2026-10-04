---
name: draw-image
description: Generate an image from a text prompt using an OpenAI-compatible image generation API (gpt-image-1-mini or compatible). The image is uploaded to the gofile.io public file sharing service and ONLY the public download page URL is returned. Trigger when user asks to draw, paint, generate, or create an image.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Draw Image

Generate images via an OpenAI-compatible `images/generations` endpoint. The script has a built-in API base and key, so no extra configuration is needed.

## Quick Start

Generate an image from a text prompt:

```bash
python3 ~/.hermes/skills/ai-sns/draw-image/scripts/draw.py --prompt "A futuristic cityscape at sunset with flying cars"
```

## Parameters

All parameters are optional except `--prompt`:

```bash
python3 ~/.hermes/skills/ai-sns/draw-image/scripts/draw.py \
  --prompt "A cute cat wearing a spacesuit" \
  --size 1024x1024 \
  --model gpt-image-1-mini\
  --quality low \
  --n 1
```

\n- `--prompt`: Text description of the image (required).
- `--size`: Image dimensions (optional). Default is `1024x1024`.
- `--model`: Image generation model (optional). Default is `gpt-image-1-mini`.
- `--quality`: Image quality, either `low`,`medium`,`high` (optional). Default is `low`.
- `--n`: Number of images to generate (optional). Default is `1`.
- `--out-dir` (string, optional): Directory to save images. Default: `<projectRoot>/uploads/generated_images/`.
- `--api-base` (string, optional): Override the API base URL.
- `--api-key` (string, optional): Override the API key.

### Stdin JSON Mode

Alternatively, pass parameters as JSON on stdin:

```bash
echo '{"prompt": "A serene mountain landscape at dawn"}' | python3 ~/.hermes/skills/ai-sns/draw-image/scripts/draw.py --stdin
```

### Environment Variable Overrides

- `DRAW_IMAGE_API_BASE`: Override the API base URL.
- `DRAW_IMAGE_API_KEY`: Override the API key.

### Draw a Cow

Generate an image of a cow with the following command:
```bash
python3 ~/.hermes/skills/ai-sns/draw-image/scripts/draw.py --prompt 'A cow' --size 1024x1024 --model gpt-image-1-mini --quality low
```

The image is generated, uploaded to gofile.io, and ONLY the public download page URL is returned.
The script prints a JSON object to stdout:

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
