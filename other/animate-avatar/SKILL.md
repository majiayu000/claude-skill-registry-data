---
name: animate-avatar
description: Generate animated videos from static avatar images using FAL AI. Create looping work and relax animations with Kling V2.6 Pro, LTX, or Veo models.
allowed-tools: Bash, Read, Write
env:
  - FAL_KEY
---

# Animate Avatar Skill

Generate animated videos from static avatar images for use in apps, websites, or social profiles.

## Overview

This skill automates the process of:
1. Generating multiple video animations from a static avatar image
2. Optimizing videos for web delivery

## Activity Philosophy

**Default Generation**: Create **3 videos** per avatar:
- **2 Work activities** - Shows the character being productive
- **1 Relax activity** - Shows the character taking a break

This 2:1 ratio of work-to-relax creates variety and humanizes characters.

### Work Activity Prompts (pick 2)
- "Character typing on a computer keyboard"
- "Character writing or signing documents"
- "Character giving a presentation with gestures"
- "Character thinking deeply, tapping chin"
- "Character nodding while listening attentively"
- "Character examining something closely"
- "Character taking notes with a pen"

### Relax Activity Prompts (pick 1)
- "Character drinking coffee or tea"
- "Character playing a small guitar"
- "Character eating a snack happily"
- "Character stretching and yawning"
- "Character listening to music, bobbing head"
- "Character waving hello cheerfully"

## Models & Pricing

| Model | Flag | Cost | Notes |
|-------|------|------|-------|
| **Kling V2.6 Pro** | `--model kling` | $0.07/sec ($0.35/5s video) | Default, best quality/cost |
| LTX-2-19B | `--model ltx` | ~$0.20/video | Cheaper for small res |
| Veo 3.1 | `--model veo` | $0.20/sec ($1.00/5s video) | Highest quality |

## Prerequisites

- FAL AI API key set as `FAL_KEY` environment variable
- ffmpeg installed for video optimization

## Usage

```bash
bun .claude/skills/animate-avatar/scripts/animate-avatar.ts \
  --avatar "avatar-name" \
  --prompts "Character typing on keyboard,Character signing a document,Character drinking coffee"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--avatar` | Yes | - | Avatar name or path to image |
| `--count` | No | `3` | Number of videos to generate |
| `--prompts` | No | Auto | Comma-separated motion prompts |
| `--model` | No | `kling` | Model: `kling`, `ltx`, or `veo` |
| `--skip-optimize` | No | `false` | Skip ffmpeg optimization |

## Output

Videos are:
1. Generated via FAL AI (~70s each)
2. Optimized with ffmpeg (320x320, ~150-250KB)
3. Saved to the output directory

## Tips for Best Results

### Good Prompts
- Keep motions subtle - loops better
- Match the character's personality
- Work: typing, writing, presenting, thinking
- Relax: drinking, stretching, waving

### Avoid
- Large movements that break the loop
- "Walking", "running", "jumping" - too dynamic
- Complex multi-step actions

## Video Specifications

| Property | Value |
|----------|-------|
| Resolution | 320x320 |
| Format | MP4 (H.264) |
| Duration | 5 seconds |
| Target Size | ~150-250 KB |
