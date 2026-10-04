---
name: openrouter-image2video
description: Animate a still image into a short video via OpenRouter. Default model google/veo-3.1-fast.
---

# openrouter-image2video

Image + motion-prompt → video via OpenRouter. Default model: `google/veo-3.1-fast`.

Use this when you already have a strong still image and want to bring it to life with subtle motion (camera pan, parallax, gentle animation) while preserving the composition. For motion-from-scratch, use `openrouter-text2video` instead.

The script accepts either a remote image URL or a local image path; local files are base64-encoded and inlined into the request as a data URL.

## Usage

Resolve `TOOL_DIR` = the directory containing this `SKILL.md`. Commands below use `TOOL_DIR` as a symbolic placeholder; replace it with the resolved, quoted path before running Bash.

```bash
export OPENROUTER_API_KEY=sk-or-v1-...

# From a local image you already generated with text2image
python3 TOOL_DIR/scripts/generate_video_from_image.py \
  --image PROJECT_DIR/assets/teaser.png \
  --prompt "slow parallax push-in, soft drift of ambient particles, no camera shake" \
  --duration 5 \
  --aspect-ratio 16:9 \
  --download PROJECT_DIR/assets/teaser.mp4

# Or from a remote URL
python3 TOOL_DIR/scripts/generate_video_from_image.py \
  --image-url "https://example.com/still.png" \
  --prompt "subtle camera dolly forward, gentle depth-of-field shift" \
  --download PROJECT_DIR/assets/scene.mp4
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `--prompt` | required | Motion prompt — describe what should move and how |
| `--download` | required | Output MP4 path |
| `--image` | one of `--image` / `--image-url` required | Local image path (PNG/JPG); will be base64-encoded |
| `--image-url` | one of `--image` / `--image-url` required | Remote image URL |
| `--model` | `google/veo-3.1-fast` | Any OpenRouter image-to-video-capable model |
| `--duration` | `5` | Seconds |
| `--aspect-ratio` | `16:9` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, `9:21` |
| `--resolution` | `720p` | Model-dependent (e.g. `480p`, `720p`, `1080p`) |
| `--frame-role` | `first` | `first` or `last` — anchor frame role for the input image |
| `--generate-audio` | off | Generate audio with video (if model supports) |
| `--poll-interval` | `5` | Seconds between polls |
| `--max-wait` | `600` | Max total wait time |

## Flow

1. `POST /api/v1/videos` with body:
   ```json
   {
     "model": "google/veo-3.1-fast",
     "prompt": "...motion prompt...",
     "aspect_ratio": "16:9",
     "duration": 5,
     "resolution": "720p",
     "frame_images": [
       {
         "type": "image_url",
         "frame_type": "first_frame",
         "image_url": {"url": "data:image/png;base64,..." }
       }
     ]
   }
   ```
   The `--frame-role first|last` flag maps to `frame_type: "first_frame"|"last_frame"`.
2. `GET /api/v1/videos/{id}` every 5s until `status == "completed"`
3. `GET /api/v1/videos/{id}/content` → raw MP4 bytes

## Notes

- Veo 3.1 Fast is optimized for low-latency image-to-video. Typical render ≈ 60-180s for a 5s 720p clip.
- The motion prompt should describe motion only, not the subject (the subject comes from the image).
- For subjects with prominent faces, keep motion subtle to avoid uncanny artifacts.
- If you also want a defined ending state, supply two images via `frame_images` with roles `first` and `last`. The current script wires only one anchor frame; extend `body["frame_images"]` to add a second.
