---
name: image-to-video
description: Generate videos from static images using FAL AI models — Kling V2.6 Pro for premium quality with audio, Wan V2.6 for fast generation. Handles avatar animations, product demos, and marketing clips.
allowed-tools: Bash, Read, Write
env:
  - FAL_KEY
---

# Image to Video Skill

Generate videos from static images using FAL AI's video generation models.

## Available Models

| Model | ID | Best For |
|-------|-----|----------|
| Kling V2.6 Pro | `fal-ai/kling-video/v2.6/pro/image-to-video` | High quality, motion consistency, audio |
| Wan V2.6 | `wan/v2.6/image-to-video` | Fast generation, good quality |

## Prerequisites

- FAL AI API key set as `FAL_KEY` environment variable

## Usage

```bash
bun .claude/skills/image-to-video/scripts/image-to-video.ts \
  --image "https://example.com/image.png" \
  --prompt "A character waving and smiling" \
  --output "./output.mp4"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--image` | Yes | - | URL or local path to source image |
| `--prompt` | Yes | - | Motion/action description |
| `--output` | No | `./output.mp4` | Output file path |
| `--duration` | No | `5` | Video duration (5 or 10 seconds) |
| `--model` | No | `kling` | Model to use (`kling` or `wan`) |
| `--negative` | No | See below | Negative prompt |
| `--audio` | No | `false` | Generate audio (Kling only) |

### Default Negative Prompt
```
blur, distort, low quality, low resolution, error, worst quality, defects
```

## Examples

### Animate an Avatar
```bash
bun .claude/skills/image-to-video/scripts/image-to-video.ts \
  --image "/path/to/avatar.png" \
  --prompt "Character nodding and blinking naturally" \
  --duration 5 \
  --output "./avatar-animation.mp4"
```

### Generate with Audio (Kling)
```bash
bun .claude/skills/image-to-video/scripts/image-to-video.ts \
  --image "/path/to/character.png" \
  --prompt "Character says 'Hello, welcome!'" \
  --audio \
  --model kling \
  --output "./speaking-character.mp4"
```

## Tips for Avatar Animation

1. **Subtle motions work best**: "blinking", "nodding slightly", "breathing"
2. **Avoid large movements**: Keep the character mostly in place
3. **Loop-friendly prompts**: End state similar to start state
4. **Square images**: 1:1 aspect ratio works best for avatars

## Cost Considerations

- Kling V2.6 Pro: Higher quality, higher cost (~$0.35/5s video)
- Wan V2.6: Good balance of quality and cost
- 5-second videos are more cost-effective than 10-second
