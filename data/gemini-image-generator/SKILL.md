---
name: Gemini Image Generator
description: This skill should be used when the user asks to "generate an image", "create project images", "make illustrations", "generate icons", "create visual assets", "use Gemini for images", "generate with nono banana", or needs AI-generated images for their project using Google's Gemini API.
version: 0.1.0
---

# Gemini Image Generator

Generate high-quality images for projects using Google's Gemini 3 Pro Image Preview model. This skill provides workflows for creating various types of project images including icons, illustrations, banners, and concept art.

## Overview

The Gemini 3 Pro Image Preview model (`gemini-3-pro-image-preview`) offers native image generation capabilities through the Generative Language API. It supports:

- Text-to-image generation
- Image editing and transformation
- Style transfer
- Multi-image composition

## Prerequisites

Before using this skill:

1. Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set the environment variable: `export GEMINI_API_KEY="your-api-key"`

## Quick Start

### Generate Image via Python Script

Execute the bundled script to generate images:

```bash
python3 "${SKILL_DIR}/scripts/generate_image.py" \
  --prompt "A cute banana character mascot for a mobile app, kawaii style, yellow and brown colors" \
  --output "./generated_image.png"
```

### Generate Image via cURL

For direct API calls without dependencies:

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Your prompt here"}]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }' | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
    if 'inlineData' in part:
        img_data = base64.b64decode(part['inlineData']['data'])
        with open('output.png', 'wb') as f:
            f.write(img_data)
        print('Image saved to output.png')
"
```

## Image Generation Workflows

### Workflow 1: Project Icon Generation

Generate app icons or project logos:

```bash
python3 "${SKILL_DIR}/scripts/generate_image.py" \
  --prompt "Modern flat design app icon for [PROJECT_TYPE], minimalist style, vibrant colors, suitable for iOS/Android" \
  --output "./icon.png" \
  --aspect-ratio "1:1"
```

### Workflow 2: Banner/Hero Image

Create marketing banners or hero images:

```bash
python3 "${SKILL_DIR}/scripts/generate_image.py" \
  --prompt "Professional banner image for [PROJECT_NAME], modern tech aesthetic, gradient background" \
  --output "./banner.png" \
  --aspect-ratio "16:9"
```

### Workflow 3: Illustration Generation

Generate illustrations for documentation or UI:

```bash
python3 "${SKILL_DIR}/scripts/generate_image.py" \
  --prompt "Clean vector-style illustration showing [CONCEPT], soft colors, professional look" \
  --output "./illustration.png"
```

### Workflow 4: Image Editing/Transformation

Transform or edit existing images:

```bash
python3 "${SKILL_DIR}/scripts/generate_image.py" \
  --prompt "Transform this image into a watercolor painting style while preserving the main subject" \
  --input "./source_image.png" \
  --output "./transformed.png"
```

## Prompt Engineering Tips

### Effective Prompt Structure

```
[Subject] + [Style] + [Details] + [Technical specs]
```

**Example:**
```
A friendly robot mascot (subject)
in pixel art style (style)
with blue and orange colors, waving hand (details)
on transparent background, 512x512 resolution (technical)
```

### Style Keywords

| Category | Keywords |
|----------|----------|
| Art Style | minimalist, flat design, 3D render, watercolor, pixel art, vector, cartoon |
| Mood | professional, playful, elegant, modern, vintage, futuristic |
| Quality | high detail, photorealistic, clean lines, sharp edges |
| Colors | vibrant, pastel, monochrome, gradient, neon |

### Project-Specific Prompts

For different project types:

- **Mobile App**: "Modern app icon, rounded corners, gradient background, single symbolic element"
- **Web Dashboard**: "Clean UI illustration, data visualization theme, blue corporate colors"
- **Game**: "Game asset sprite, detailed pixel art, fantasy theme, transparent background"
- **Documentation**: "Technical diagram style, clean vector illustration, explanatory visual"

## Configuration Options

### Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| 1:1 | App icons, profile pictures |
| 16:9 | Banners, hero images |
| 4:3 | Standard images, thumbnails |
| 9:16 | Mobile stories, vertical banners |
| 5:4 | Group photos, presentations |

### Image Sizes

| Size | Description |
|------|-------------|
| default | Standard resolution |
| 2K | Higher quality (2048px) |
| 4K | Maximum quality (4096px) |

## Error Handling

Common issues and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify GEMINI_API_KEY is set correctly |
| 400 Bad Request | Invalid prompt | Check prompt format, remove prohibited content |
| 429 Rate Limited | Too many requests | Wait and retry, implement backoff |
| Safety Block | Content policy violation | Modify prompt to comply with guidelines |

## Bundled Resources

### Scripts

- **`scripts/generate_image.py`** - Main image generation script with full configuration options
- **`scripts/batch_generate.py`** - Generate multiple images from a prompt list

### References

- **`references/api-reference.md`** - Complete Gemini API documentation
- **`references/prompt-templates.md`** - Ready-to-use prompt templates for various project types

### Examples

- **`examples/generate_icon.sh`** - Example: Generate app icon
- **`examples/generate_banner.sh`** - Example: Generate project banner
- **`examples/batch_config.json`** - Example: Batch generation configuration

## Best Practices

1. **Be Specific**: Include detailed descriptions of desired output
2. **Specify Style**: Always mention the artistic style explicitly
3. **Define Colors**: List specific colors when brand consistency matters
4. **Set Constraints**: Specify aspect ratio and size requirements upfront
5. **Iterate**: Generate multiple variations and refine prompts based on results
6. **Save Prompts**: Document successful prompts for future consistency

## Integration Notes

When integrating generated images into projects:

1. Check image dimensions match target requirements
2. Verify file format compatibility (PNG recommended for transparency)
3. Consider compression for web assets
4. Store original prompts alongside images for reproducibility
