---
name: youtube-video-creator
description: Create YouTube videos from scratch — script, images, narration, assembly, upload. Full production pipeline from topic to published video.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
env:
  - ELEVENLABS_API_KEY
  - FAL_KEY
---

# YouTube Video Creator

Create complete YouTube videos programmatically — from a topic or brief to a fully assembled, uploadable video with AI-generated images, narration, Ken Burns effects, and background music.

## Quick Start

```bash
# 1. Create project directory
mkdir -p ~/videos/my-project/audio

# 2. Write a script (see JSON format below)
# 3. Generate visuals (screenshots, HTML slides, or AI images per scene)

# 4. Generate narration
bun .claude/scripts/generate-narration.ts --script ~/videos/my-project/script.json --output-dir ~/videos/my-project/audio

# 5. Assemble video
bun .claude/scripts/assemble-video.ts --script ~/videos/my-project/script.json --output ~/videos/my-project/final.mp4

# 6. Upload (optional, needs youtube-auth.ts setup first)
bun .claude/scripts/upload-youtube.ts --video ~/videos/my-project/final.mp4 --script ~/videos/my-project/script.json
```

## Pipeline Overview

```
Topic/Brief
    |
    v
[Write script.json] --- scenes[], narration, image prompts, metadata
    |
    v
[Generate visuals] --- AI images (generate-image skill) or HTML screenshots
[Generate narration] --- ElevenLabs TTS (generate-narration.ts)
[Optional: AI video clips] --- FAL AI Kling/Wan (image-to-video skill)
    |
    v
[Assemble video] --- FFmpeg: Ken Burns + crossfades + narration + music
    |
    v
[Upload to YouTube] --- YouTube Data API v3 (resumable upload)
```

## Video Script JSON Format

```json
{
  "title": "Video Title",
  "description": "YouTube video description",
  "tags": ["tag1", "tag2"],
  "category": "28",
  "privacy": "private",
  "scenes": [
    {
      "id": "scene-1",
      "narration": "Text to speak",
      "imagePrompt": "Prompt for AI image generation",
      "type": "ken-burns",
      "imagePath": null,
      "audioPath": null,
      "audioDuration": null,
      "videoClipPath": null
    }
  ],
  "backgroundMusic": "/path/to/music.mp3",
  "backgroundMusicVolume": 0.05,
  "voice": {
    "voiceId": "21m00Tcm4TlvDq8ikWAM",
    "modelId": "eleven_multilingual_v2",
    "stability": 0.5,
    "similarityBoost": 0.75,
    "speed": 1.0
  }
}
```

### Scene Types

| Type | Description | Visual Source |
|------|-------------|--------------|
| `ken-burns` | Pan/zoom on static image (default) | `imagePath` |
| `ai-video` | Full motion AI video clip | `videoClipPath` |

### Visual Strategies

**AI Images** (most scenes): Use `generate-image` skill for abstract concepts, backgrounds, illustrations.

**HTML Screenshots** (for text/data/UI): Write an HTML file, screenshot with headless browser. Great for code snippets, data tables, charts, UI mockups.

**AI Video Clips** (1-2 hero scenes): Use `image-to-video` skill for scenes needing motion.

## Scripts Reference

| Script | Purpose | Key Args |
|--------|---------|----------|
| `generate-narration.ts` | ElevenLabs TTS | `--text`, `--script`, `--voice`, `--list-voices` |
| `assemble-video.ts` | FFmpeg assembly | `--script`, `--output`, `--resolution`, `--transition` |
| `youtube-auth.ts` | OAuth2 setup | `--credentials` (one-time) |
| `upload-youtube.ts` | YouTube upload | `--video`, `--script`, `--privacy`, `--thumbnail` |

## Narration

```bash
# Standalone
bun .claude/scripts/generate-narration.ts --text "Hello" --output ./hello.mp3

# Batch (from script)
bun .claude/scripts/generate-narration.ts --script ./script.json --output-dir ./audio

# List voices
bun .claude/scripts/generate-narration.ts --list-voices
```

### Popular ElevenLabs Voices

| Name | ID | Type |
|------|-----|------|
| Rachel | `21m00Tcm4TlvDq8ikWAM` | Female, calm, narration |
| Adam | `pNInz6obpgDQGcFmaJgB` | Male, deep, authoritative |
| Josh | `TxGEqnHWrfWFTfGW9XjX` | Male, casual, friendly |

## Assembly Options

```bash
bun .claude/scripts/assemble-video.ts \
  --script ./script.json \
  --output ./final.mp4 \
  --resolution 1920x1080 \
  --transition fade \
  --fps 30
```

Ken Burns presets rotate automatically: center zoom, left pan, right pan, top pan.

## YouTube Setup

### One-Time Auth
```bash
bun .claude/scripts/youtube-auth.ts --credentials ./client_secret.json
```

### Upload
```bash
bun .claude/scripts/upload-youtube.ts \
  --video ./final.mp4 \
  --script ./script.json \
  --privacy private
```

**Note**: Unverified OAuth apps can only upload as private. Submit your Google Cloud app for verification to upload public videos.

## Cost Estimate

| Component | Per Scene | 8-Scene Video |
|-----------|-----------|---------------|
| AI Image (Flux 2) | ~$0.05 | ~$0.40 |
| Narration (ElevenLabs) | ~$0.15-0.25 | ~$1.50 |
| AI Video Clip (optional) | ~$0.35 | ~$0.70 (2 clips) |
| FFmpeg Assembly | Free | Free |
| **Total** | | **~$2-3** |

## Prerequisites

- **ffmpeg**: `brew install ffmpeg`
- **ELEVENLABS_API_KEY**: ElevenLabs account
- **FAL_KEY**: FAL AI account
- **YouTube upload**: Google Cloud project with YouTube Data API v3 + OAuth credentials
