---
name: startup-portrait
description: Transform team photos into professional startup portraits using fal.ai Nano Banana Pro image-to-image API.
---

# Startup Team Portrait Generator

This skill transforms existing photos into professional startup team portraits while preserving each person's face and features.

## When to Use

Use this skill when:
- You have casual photos and need professional headshots
- Building an "About Us" or "Team" section for your website
- Creating consistent portrait styles across your team

## Prerequisites

The `FAL_KEY` environment variable must be set with your fal.ai API key.

## How to Use

```bash
$CLAUDE_CONFIG_DIR/skills/startup-portrait/scripts/startup-portrait.sh
```

The script will:
1. Scan current directory for images (jpg, jpeg, png, webp)
2. Upload each image to fal.ai
3. Transform into professional portraits using image-to-image AI
4. Save generated portraits to the current directory

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --style | No | founder | Portrait style: founder, corporate, creative, casual, natural |
| --output-dir | No | . | Where to save generated images |

### Examples

```bash
# Transform photos with default founder style
$CLAUDE_CONFIG_DIR/skills/startup-portrait/scripts/startup-portrait.sh

# Use corporate style
$CLAUDE_CONFIG_DIR/skills/startup-portrait/scripts/startup-portrait.sh --style creative

# Save to specific folder
$CLAUDE_CONFIG_DIR/skills/startup-portrait/scripts/startup-portrait.sh --output-dir ./team-photos
```

## Output

- Generated portraits are saved as `portrait_[name]_[timestamp]_generated.png`
- Images are 1:1 aspect ratio (square) at 1K resolution
- Preserves the person's face from the original photo
