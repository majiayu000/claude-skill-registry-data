---
name: slide-gen-images
description: "AI image generation for presentation slides using Gemini Pro. Supports batch generation, style consistency, and visual validation."
version: "2.0.0"
author: "davistroy"
---

# Image Generation Skill

Generates slide images using Google Gemini Pro with style consistency.

## Capabilities

- **Batch Generation**: Generate all slide images in one run
- **Style Consistency**: Maintain visual coherence across slides
- **Resolution Options**: Low (fast), Medium (balanced), High (quality)
- **Visual Validation**: Optional AI-based quality check (experimental)

## Usage

```bash
python -m plugin.cli generate-images content.md --resolution high
```

## Input Requirements

Content file must include graphics descriptions in each slide:

```markdown
## Graphics Description
A professional business chart showing quarterly growth with blue and green color scheme...
```

## Resolution Options

| Resolution | Size      | Use Case               | Generation Time |
|------------|-----------|------------------------|-----------------|
| low        | 512x512   | Draft/preview          | ~5 sec/image    |
| medium     | 1024x1024 | Standard presentations | ~10 sec/image   |
| high       | 1536x1536 | High-quality output    | ~20 sec/image   |

## Dependencies

- Google Gemini Pro API
- GOOGLE_API_KEY environment variable
- Pillow for image processing
