---
name: nano-banana-2
description: "Full image generation system — property images, avatars, backgrounds. Triggers: generate image, create image, nano banana 2, avatar, seedream, property photo, background edit, image generation"
allowed-tools: Bash(infsh *), Bash(~/bin/gh *)
---

# Image Generation System — Full Guide

## DECISION TREE — which workflow to use

Ask: does this image involve a REAL PERSON with a specific identity?

YES (agent, client, Mike, Matt, Alexandra) → use avatar_generate.yml (Seedream 4.5)
NO (property, background, scene, co-stars, extras) → use generate_image.yml (Nano Banana 2)
BACKGROUND EDIT on existing Seedream output → use generate_image.yml with reference image + "keep person exactly as is"

---

## WORKFLOW 1 — generate_image.yml (Nano Banana 2 / inference.sh)

USE FOR: property images, scenes, backgrounds, co-stars, background edits

```bash
~/bin/gh workflow run generate_image.yml \
  --repo priihigashi/oak-park-ai-hub \
  -f prompt="Your scene prompt here" \
  -f filename="output_name" \
  -f aspect_ratio="16:9" \
  -f drive_folder_id="1Md5BRAfWTUBOtl_LvdTAyBhat8ZfXamN"
```

Optional — pass a reference image for background editing:
```bash
  -f reference_image_url="https://url-to-existing-image.jpg"
```

When editing background only (after Seedream), always include in prompt:
"Keep the person exactly as is — do not change the face, hair, clothing or body. Only change the background to [scene]"

Aspect ratio options: 1:1 / 3:4 / 4:3 / 16:9 / 9:16
Model: google/gemini-3-1-flash-image-preview via inference.sh
Secret: PRI_OP_INFSH_API_KEY

---

## WORKFLOW 2 — avatar_generate.yml (Seedream 4.5 / Replicate)

USE FOR: real people, face/identity preservation, Alexandra, Mike, Matt, clients

```bash
~/bin/gh workflow run avatar_generate.yml \
  --repo priihigashi/oak-park-ai-hub \
  -f prompt="Elegant woman in luxury real estate office, professional attire, warm lighting" \
  -f reference_image_url="https://url-to-persons-photo.jpg" \
  -f filename="alexandra_office" \
  -f drive_folder_id="1WCW29iHlftMOSdu0qKLga1nwwlUw962K"
```

Optional — also refine background with Nano Banana 2 after generating:
```bash
  -f background_edit_only="true"
```

Model: bytedance/seedream-4.5 via Replicate
Secret: PRI_OP_REPLICATE_API_KEY
Default save folder: Alexandra/Avatar AI Created

---

## 2-STEP AVATAR PIPELINE (Priscila's proven method)

Step 1 → avatar_generate.yml (Seedream 4.5): creates the image with face locked
Step 2 → generate_image.yml (Nano Banana 2): edits background ONLY, preserves face

NEVER ask Nano Banana 2 to regenerate the person. Pass the Seedream output as reference image and explicitly say "keep the person exactly as is."

---

## DRIVE FOLDER MAP (Higashi — Shared Drives > Higashi Imobiliária - Claude > Claude Flow)

AI Images Created root:              1ZInVJlr7mDnz3nogI6ED7rZI64gvCPhh
Alexandra/Avatar AI Created:         1WCW29iHlftMOSdu0qKLga1nwwlUw962K  ← default avatar_generate.yml
Alexandra/Character Originals:       1F3n-8MS2Q6YZxbYfa5-Edf6GWk-uPwoV  ← drop real photos here
AI Property Images/Completely Gen:   1Md5BRAfWTUBOtl_LvdTAyBhat8ZfXamN  ← default generate_image.yml
AI Property Images/Edited with AI:   1hpfLTWZpYBrP9jm_0McQkQwUJm7jqCF4

---

## AI IMAGES FOLDER MAP — ALL NICHES

### Higashi (Shared Drives > Higashi Imobiliária - Claude > Claude Flow)
AI Images Created root:              1ZInVJlr7mDnz3nogI6ED7rZI64gvCPhh
Alexandra/Avatar AI Created:         1WCW29iHlftMOSdu0qKLga1nwwlUw962K
Alexandra/Character Originals:       1F3n-8MS2Q6YZxbYfa5-Edf6GWk-uPwoV
AI Property Images/Completely Gen:   1Md5BRAfWTUBOtl_LvdTAyBhat8ZfXamN
AI Property Images/Edited with AI:   1hpfLTUZpYBrP9jm_0McQkQwUJm7jqCF4

### OPC / Marketing (Shared Drives > Marketing > Claude Code Workspace)
AI Images Created root:              1kdKioUGpS5O23vrzCKMitLMBdhc6X6c8
Mike/Character Originals:            1qTDBdhaZ1SrY0zdPClMqxGuHHsZThdQ_
Mike/Avatar AI Created:              1e2qHh1WQBQIYCcxPP88leVmvD8bZHnbY
Matt/Character Originals:            1tod90UwvXQknPHQD6OBgbMo4NBCzbGXQ
Matt/Avatar AI Created:              1De_tCLEG2JkPefrKWSiib8FqBM2Op4Cq

### News (Shared Drives > News)
AI Images Created root:              1nKliyh3m4x_KJ9EPM2GLrdzA4KRwQAye
Presenter Placeholder/Originals:     1eT8-D4YOsYc9WLNeSvGSX6nixex1gTuS
Presenter Placeholder/Avatar AI:     1ze0lpz1InnFnlNFkhJnD3fcI8rIR1t10

---

## HIGASHI LOCATION RULE

São José dos Campos = URBAN/SUBURBAN. Never mountains or dense forest in property images unless explicitly requested. Always add "São José dos Campos, Vale do Paraíba, SP, Brazil, urban residential" to exterior prompts.

---

## SECRETS

PRI_OP_INFSH_API_KEY   → inference.sh (Nano Banana 2) — already set
PRI_OP_REPLICATE_API_KEY → Replicate (Seedream 4.5) — already set

---

# Nano Banana 2 - Gemini 3.1 Flash Image Preview (CLI Reference)

Generate images with Google Gemini 3.1 Flash Image Preview via [inference.sh](https://inference.sh) CLI.

## Quick Start

> Requires inference.sh CLI (`infsh`). [Install instructions](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

```bash
infsh login

infsh app run google/gemini-3-1-flash-image-preview --input '{"prompt": "a banana in space, photorealistic"}'
```


## Examples

### Basic Text-to-Image

```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "A futuristic cityscape at sunset with flying cars"
}'
```

### Multiple Images

```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "Minimalist logo design for a coffee shop",
  "num_images": 4
}'
```

### Custom Aspect Ratio

```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "Panoramic mountain landscape with northern lights",
  "aspect_ratio": "16:9"
}'
```

### Image Editing (with input images)

```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "Add a rainbow in the sky",
  "images": ["https://example.com/landscape.jpg"]
}'
```

### High Resolution (4K)

```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "Detailed illustration of a medieval castle",
  "resolution": "4K"
}'
```

### With Google Search Grounding

```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "Current weather in Tokyo visualized as an artistic scene",
  "enable_google_search": true
}'
```

## Input Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | **Required.** What to generate or change |
| `images` | array | Input images for editing (up to 14). Supported: JPEG, PNG, WebP |
| `num_images` | integer | Number of images to generate |
| `aspect_ratio` | string | Output ratio: "1:1", "16:9", "9:16", "4:3", "3:4", "auto" |
| `resolution` | string | "1K", "2K", "4K" (default: 1K) |
| `output_format` | string | Output format for images |
| `enable_google_search` | boolean | Enable real-time info grounding (weather, news, etc.) |

## Output

| Field | Type | Description |
|-------|------|-------------|
| `images` | array | The generated or edited images |
| `description` | string | Text description or response from the model |
| `output_meta` | object | Metadata about inputs/outputs for pricing |

## Prompt Tips

**Styles**: photorealistic, illustration, watercolor, oil painting, digital art, anime, 3D render

**Composition**: close-up, wide shot, aerial view, macro, portrait, landscape

**Lighting**: natural light, studio lighting, golden hour, dramatic shadows, neon

**Details**: add specific details about textures, colors, mood, atmosphere

## Sample Workflow

```bash
# 1. Generate sample input to see all options
infsh app sample google/gemini-3-1-flash-image-preview --save input.json

# 2. Edit the prompt
# 3. Run
infsh app run google/gemini-3-1-flash-image-preview --input input.json
```

## Python SDK

```python
from inferencesh import inference

client = inference()

# Basic generation
result = client.run({
    "app": "google/gemini-3-1-flash-image-preview@0c7ma1ex",
    "input": {
        "prompt": "A banana in space, photorealistic"
    }
})
print(result["output"])

# Stream live updates
for update in client.run({
    "app": "google/gemini-3-1-flash-image-preview@0c7ma1ex",
    "input": {
        "prompt": "A futuristic cityscape at sunset"
    }
}, stream=True):
    if update.get("progress"):
        print(f"progress: {update['progress']}%")
    if update.get("output"):
        print(f"output: {update['output']}")
```

## Related Skills

```bash
# Original Nano Banana (Gemini 3 Pro Image, Gemini 2.5 Flash Image)
npx skills add inference-sh/skills@nano-banana

# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@infsh-cli

# All image generation models
npx skills add inference-sh/skills@ai-image-generation
```

Browse all image apps: `infsh app list --category image`

## Documentation

- [Running Apps](https://inference.sh/docs/apps/running) - How to run apps via CLI
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) - Real-time progress updates
- [File Handling](https://inference.sh/docs/api/sdk/files) - Working with images

