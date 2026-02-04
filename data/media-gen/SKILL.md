---
name: media-gen
description: Generate images and videos using Google GenAI models. Use when user asks to "generate image with Gemini/Nano Banana", "create video with Veo", "make an image using Imagen", or requests media generation with specific models like gemini-2.5-flash-image, gemini-3.0-pro-image, imagen-3.0, veo-3.1, or veo-3.0.
---

# Media Generation

Generate images and videos using Google GenAI SDK (`google-genai`).

## Model Selection

| Task | Model | Use Case |
|------|-------|----------|
| Image | `gemini-2.5-flash-image` (Nano Banana) | Fast, cheap ($0.039/img) |
| Image | `gemini-3.0-pro-image` (Nano Banana Pro) | High quality, 4K |
| Image | `imagen-3.0-generate-002` | Imagen, negative prompts |
| Video | `veo-3.1-generate-preview` | Best quality, audio |
| Video | `veo-3.1-fast-generate-preview` | Faster generation |

**Auto-selection logic:**
- Image without special needs → `gemini-2.5-flash-image`
- Image needing 4K or high quality → `gemini-3.0-pro-image`
- Image with negative prompt → `imagen-3.0-generate-002`
- Video → `veo-3.1-generate-preview`

## Environment

Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable.

```bash
fnox get gemini-api-key  # or set GEMINI_API_KEY
```

## Image Generation

```bash
scripts/gen_image.py "A sunset over mountains" output.png
scripts/gen_image.py "A cat portrait" cat.jpg --model gemini-3.0-pro-image --aspect-ratio 9:16
scripts/gen_image.py "Product photo" product.png --model imagen-3.0-generate-002 --negative-prompt "blurry"
```

**Parameters:**
- `--model`: Model choice (default: `gemini-2.5-flash-image`)
- `--aspect-ratio`: 1:1, 16:9, 9:16, 4:3 (default: 1:1)
- `--negative-prompt`: What to avoid (Imagen only)

## Video Generation

```bash
scripts/gen_video.py "A cat walking through grass" cat.mp4
scripts/gen_video.py "Timelapse of clouds" clouds.mp4 --model veo-3.1-fast-generate-preview
scripts/gen_video.py "Camera panning over city" city.mp4 --image reference.jpg
```

**Parameters:**
- `--model`: Model choice (default: `veo-3.1-generate-preview`)
- `--image`: Input image for image-to-video
- `--negative-prompt`: What to avoid
- `--poll-interval`: Seconds between status checks (default: 10)

Video generation is async - script polls until complete.
