---
name: coze-image-gen
description: Create images from text prompts. Use when you need to generate/draw/create images based on descriptions.
homepage: https://www.coze.com
metadata: { "openclaw": { "emoji": "🎨", "requires": { "bins": ["npx"] } } }
---

# Coze Image Generation

Generate high-quality images from text prompts using coze-coding-dev-sdk. Returns image URLs directly.

## Quick Start

### Single Image

```bash
npx ts-node {baseDir}/scripts/gen.ts --prompt "A futuristic city at sunset"
```

### Batch Generation (Random Prompts)

```bash
npx ts-node {baseDir}/scripts/gen.ts --count 4
```

### With Custom Size

```bash
npx ts-node {baseDir}/scripts/gen.ts \
  --prompt "A serene mountain landscape" \
  --size 4K
```

### Sequential Image Generation (Story Mode)

```bash
npx ts-node {baseDir}/scripts/gen.ts \
  --prompt "A hero's journey through magical lands" \
  --sequential \
  --max-sequential 5
```

## Script Options

| Option                 | Description                               |
| ---------------------- | ----------------------------------------- |
| `--prompt <text>`      | Image prompt (random if omitted)          |
| `--count <n>`          | Number of images (default: 1)             |
| `--size <size>`        | 2K, 4K, or WIDTHxHEIGHT (default: 2K)     |
| `--sequential`         | Enable sequential generation (story mode) |
| `--max-sequential <n>` | Max images for sequential (default: 5)    |

## Output

The script outputs image URLs directly to stdout:

```
[1/1] A futuristic city at sunset
  https://example.com/generated-image.png
```

## Text in Images

Wrap text in quotes for accurate rendering:

```bash
npx ts-node {baseDir}/scripts/gen.ts \
  --prompt 'A poster with the text "Hello World" on it'
```

## Notes

- Size range for custom dimensions: 2560x1440 to 4096x4096
- Image URLs have valid expiration - use directly when possible
