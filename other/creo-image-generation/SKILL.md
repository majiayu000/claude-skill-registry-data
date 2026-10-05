---
name: creo-image-generation
description: >
  Generate marketing images using DALL-E 3 or ComfyUI (Stable Diffusion XL).
  Batch generation, optimization, cost estimation. Requires image-generation extension.
  Triggers on: /creo image-generation, generate images, DALL-E, ComfyUI.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Creo Image Generation

Generate, optimize, and manage marketing images using AI (DALL-E 3 or ComfyUI with Stable Diffusion XL).

## Commands

| Command | Description |
|---------|-------------|
| `/creo image-generation generate` | Generate all images using DALL-E 3 |
| `/creo image-generation generate --seo-only` | Generate only SEO/OG images |
| `/creo image-generation generate --optimize-only` | Optimize existing images (resize, compress) |
| `/creo image-generation estimate` | Show cost estimation without generating |
| `/creo image-generation optimize` | Optimize all images in output directory |
| `/creo image-generation comfyui` | Generate images using local ComfyUI (SDXL) |
| `/creo image-generation comfyui landing` | Generate only landing page images via ComfyUI |

## How It Works

### DALL-E 3 (Cloud)

1. Reads image configuration from `paths.js` (or uses defaults)
2. Loads prompts from a `prompts.js` file (set via `PROMPTS_FILE` env var)
3. Generates images via the OpenAI DALL-E 3 API
4. Skips images that already exist on disk
5. Optionally generates SEO overlay images
6. Optimizes all images (resize, compress with sharp)

### ComfyUI (Local)

1. Requires a running ComfyUI instance (see `comfyui/SETUP.md`)
2. Sends workflows to ComfyUI via its REST/WebSocket API
3. Uses Stable Diffusion XL models for photorealistic output
4. Supports batch generation by category

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes (DALL-E) | OpenAI API key for DALL-E 3 generation |
| `IMAGE_CONFIG_DIR` | No | Directory containing `paths.js` config |
| `IMAGE_OUTPUT_DIR` | No | Output directory for generated images |
| `PROMPTS_FILE` | No | Path to prompts.js with generation prompts |
| `APP_NAME` | No | Application name for SEO image overlays |
| `COMFYUI_URL` | No | ComfyUI server URL (default: http://127.0.0.1:8000) |

## Cost Reference (DALL-E 3)

| Quality | Size | Cost per Image |
|---------|------|----------------|
| Standard | 1024x1024 | $0.040 |
| HD | 1792x1024 | $0.080 |

Always run `--estimate` first to review costs before generating.

## Library Reference

The extension code lives in the `lib/` directory:

- **`lib/ImageGenerator.js`** -- Main generator class. Handles DALL-E 3 API calls, SEO image generation, and optimization.
- **`lib/PathManager.js`** -- Manages image path generation from configuration. Supports dynamic config parsing.
- **`lib/ConfigParser.js`** -- Parses TypeScript image configuration files to extract categories and image types.
- **`lib/utils.js`** -- Utility functions: file existence checks, cost calculation, file stats, sleep.
- **`comfyui/generate-batch.js`** -- ComfyUI batch generator. Sends workflows via WebSocket, supports category filtering.

## Usage Examples

### Generate with cost estimate first

```bash
# Check cost
node index.js generate --estimate

# Generate all
OPENAI_API_KEY=sk-... node index.js generate

# Generate HD quality
OPENAI_API_KEY=sk-... node index.js generate --quality=hd
```

### ComfyUI local generation

```bash
# Start ComfyUI first, then:
node comfyui/generate-batch.js
node comfyui/generate-batch.js landing
node comfyui/generate-batch.js features audio
```

### Optimize existing images

```bash
node index.js generate --optimize-only
```
