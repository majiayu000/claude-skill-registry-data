---
name: banana
description: Generate images using Google's Gemini image generation model with Deno. Use this skill when the user wants to create AI-generated images, perform image-to-image transformations, or generate visual content from text prompts. Triggers include requests like "generate an image of...", "create a picture of...", "make an image with...", or "transform this image to...".
---

# Banana Image Generation Skill

Generate images using Google's Gemini 2.0 Flash image generation model, running with Deno.

## Quick Start

Generate an image from a text prompt:

```bash
deno run --allow-all scripts/generate-image.ts "A cat eating a nano-banana in a fancy restaurant"
```

Transform an existing image:

```bash
deno run --allow-all scripts/generate-image.ts "Make this cat wear a top hat" --input cat.png --output fancy-cat.png
```

## Requirements

- `GOOGLE_API_KEY` environment variable must be set
- Deno runtime

## Script Usage

The `scripts/generate-image.ts` script supports:

| Flag | Description |
|------|-------------|
| `<prompt>` | Text description of the image to generate (required) |
| `--input <path>` | Input image for image-to-image generation (optional) |
| `--output <path>` | Output path for generated image (default: `generated-image.png`) |

## Examples

Text-to-image:
```bash
deno run --allow-all scripts/generate-image.ts "A futuristic city at sunset"
```

Image-to-image with custom output:
```bash
deno run --allow-all scripts/generate-image.ts "Add a rainbow to the sky" --input landscape.jpg --output rainbow-landscape.png
```

## Programmatic Usage

Import and use in Deno scripts:

```typescript
import { generateImage } from "./scripts/generate-image.ts";

await generateImage({
  prompt: "A nano-banana floating in space",
  outputPath: "space-banana.png"
});
```

With input image:

```typescript
await generateImage({
  prompt: "Make this banana purple",
  imagePath: "banana.png",
  outputPath: "purple-banana.png"
});
```
