---
name: openrouter-text2video
description: Generate videos via OpenRouter using ByteDance Seedance 2.0.
---

# openrouter-text2video

Text → video via OpenRouter. Default model: `bytedance/seedance-2.0`.

Uses the async video-generation endpoint: submit job → poll → download.

## Usage

Resolve `TOOL_DIR` = the directory containing this `SKILL.md`. Commands below use `TOOL_DIR` as a symbolic placeholder; replace it with the resolved, quoted path before running Bash.

```bash
export OPENROUTER_API_KEY=sk-or-v1-...

python3 TOOL_DIR/scripts/generate_video.py \
  --prompt "A slow dolly push through a retro-futuristic arcade, neon signs reflecting in a puddle" \
  --duration 5 \
  --aspect-ratio 16:9 \
  --resolution 720p \
  --download PROJECT_DIR/assets/hero.mp4
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `--prompt` | required | Text prompt |
| `--download` | required | Output MP4 path |
| `--model` | `bytedance/seedance-2.0` | Any OpenRouter video model |
| `--duration` | `5` | Seconds |
| `--aspect-ratio` | `16:9` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, `9:21` |
| `--resolution` | `720p` | Model-dependent (e.g. `480p`, `720p`, `1080p`) |
| `--generate-audio` | off | Generate audio with video (if model supports) |
| `--poll-interval` | `5` | Seconds between polls |
| `--max-wait` | `600` | Max total wait time |

## Flow

1. `POST /api/v1/videos` → returns `{id, polling_url, status: "pending"}`
2. `GET /api/v1/videos/{id}` every 5s until `status == "completed"`
3. `GET /api/v1/videos/{id}/content` → raw MP4 bytes

## Pricing

Seedance 2.0: ~$7/M tokens with `(height × width × duration × 24) / 1024` token formula. A 5-second 720p 16:9 clip ≈ 145k tokens ≈ $1.

## Notes

- Supports text-to-video, image-to-video (first/last frame control via `frame_images`), and reference-to-video.
- This script only wires text-to-video. Extend the body to add `frame_images` or `input_references` for advanced modes.
