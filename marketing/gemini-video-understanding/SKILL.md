---
name: gemini-video-understanding
description: Analyze and understand videos using Google's Gemini API. Use when the user asks to analyze, understand, describe, summarize, transcribe, or extract information from videos. Supports local video files (MP4, MOV, WebM, etc.) and YouTube URLs. Can answer questions about video content, describe scenes, identify objects/people/actions, extract text/timestamps, and more. Use this skill when user provides a video file path or YouTube link and wants to understand its content.
---

# Gemini Video Understanding

```bash
uv run ~/.claude/skills/gemini-video-understanding/scripts/understand_video.py \
  --source "path/to/video.mp4" \
  --prompt "Describe what happens in this video" \
  [--fast] \
  [--fps 1] \
  [--start 0] \
  [--end 60]
```

## Source Types

- **Local files**: `--source "video.mp4"` — MP4, MOV, WebM, AVI, MKV, etc.
- **YouTube**: `--source "https://youtube.com/watch?v=..."` — Any YouTube URL

## Options

| Option | Description |
|--------|-------------|
| `--fast` | Use faster flash model instead of pro |
| `--fps` | Frame rate sampling (default: 1 fps). Use 2+ for fast action |
| `--start` | Start time in seconds for clipping |
| `--end` | End time in seconds for clipping |

## Example Prompts

- "Summarize this video in 3 bullet points"
- "What text appears on screen? Include timestamps"
- "Describe the main actions and events with timestamps"
- "Identify all people and what they're doing"

## API Key

Uses `GEMINI_API_KEY` env var, or pass `--api-key KEY`.

## Updating Models

Edit `~/.claude/skills/gemini-video-understanding/config.json`:

```json
{
  "default_model": "gemini-3-pro-preview",
  "fast_model": "gemini-3-flash-preview"
}
```
