---
name: grok-imagine-video
description: Generate, edit, and extend videos with xAI's grok-imagine-video model. Use when the user wants to create a video from text, animate a still image, build a reference-driven video (virtual try-on, character consistency), edit an existing video, or extend one. Asynchronous — the script handles polling.
---

# grok-imagine-video — video generation, editing, and extension via xAI

Calls xAI's video API (`grok-imagine-video`). Five modes, all in `scripts/video.py`:

| Mode | When to use | CLI |
|------|-------------|-----|
| **text-to-video** | Pure prompt → video | `--prompt "..."` |
| **image-to-video** | Animate a still image (image becomes the first frame) | `--prompt "..." --image PATH_OR_URL` |
| **reference-to-video** | Make a video featuring people / clothing / objects from reference images (no first-frame lock) | `--prompt "..." --reference-image URL [URL ...]` |
| **edit-video** | Modify an existing video while preserving the rest | `--prompt "..." --edit-video URL` |
| **extend-video** | Continue a video from its last frame | `--prompt "..." --extend-video URL` |

For full parameters, status flow, and gotchas, see `references/api-reference.md`. For Python recipes (xai-sdk, manual polling, async batches), see `references/examples.md`.

## Prerequisites

1. `XAI_API_KEY` exported in the environment.
2. Python 3.9+ with stdlib only — no SDK required (the script uses `urllib`). If the user prefers the official SDK, `pip install xai-sdk` and use the snippets in `references/examples.md`.

## Quickstart

```bash
# Text-to-video
python scripts/video.py \
  --prompt "Glowing crystal-powered rocket launching from red Mars dunes, ancient alien ruins lighting up" \
  --duration 10 --aspect-ratio 16:9 --resolution 720p \
  --output rocket.mp4

# Image-to-video (local file → animated)
python scripts/video.py \
  --prompt "Camera pushes in slowly. The leaves rustle in a gentle breeze." \
  --image ./still.jpg \
  --output animated.mp4

# Reference-to-video (virtual try-on / character consistency)
python scripts/video.py \
  --prompt "The model from <IMAGE_1> walks the runway wearing the shirt from <IMAGE_2>, slow motion, dramatic lighting" \
  --reference-image https://.../model.jpg https://.../shirt.jpg \
  --duration 10 --aspect-ratio 16:9 --resolution 720p \
  --output runway.mp4

# Edit an existing video (preserves duration / aspect / resolution)
python scripts/video.py \
  --prompt "Give the woman a silver necklace" \
  --edit-video https://.../source.mp4 \
  --output edited.mp4

# Extend an existing video (duration = length of NEW portion only)
python scripts/video.py \
  --prompt "The cat notices a butterfly and leaps off the windowsill" \
  --extend-video https://.../cat.mp4 --duration 6 \
  --output extended.mp4
```

The script polls until `status=done`, downloads the resulting MP4 to `--output`, and prints both the local path and the source URL on stderr.

## Decision rules

When the user wants a video, route by which inputs they have:

1. **No inputs, just a description** → text-to-video.
2. **One image, "make this move"** → image-to-video. The image becomes the first frame; aspect ratio defaults to the image's unless overridden.
3. **One or more images, "use these people/clothes/objects"** → reference-to-video. Refer to images in the prompt as `<IMAGE_1>`, `<IMAGE_2>`, etc.
4. **An existing video, "change X about it"** → edit-video. Duration / aspect / resolution are inherited and **cannot be overridden** (capped at 720p).
5. **An existing video, "show what happens next"** → extend-video. `--duration` is the length of the **extension only**; output total = original + extension.

Mutually exclusive — don't combine `--image` with `--reference-image`, and don't pass `--edit-video` with `--extend-video`. The script enforces this.

## Parameters cheat sheet

| Flag | Values | Default | Notes |
|------|--------|---------|-------|
| `--prompt` | str | required | Use `<IMAGE_1>`, `<IMAGE_2>` markers when referencing images |
| `--duration` | int 1–15 (seconds) | model default | For extend, this is the **added** length only. Edit mode ignores. |
| `--aspect-ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3` | `16:9` | Edit mode ignores; image-to-video defaults to image's ratio |
| `--resolution` | `480p`, `720p` | `480p` | Edit mode ignores (caps at 720p) |
| `--image` | path or `https://` URL or `data:` URI | — | Image-to-video. Local files auto-encoded as base64 data URIs. |
| `--reference-image` | one or more URLs / paths | — | Reference-to-video. Local files auto-encoded. |
| `--edit-video` | URL | — | Edit-video mode. Must be an HTTPS URL (xAI-hosted is fine). |
| `--extend-video` | URL | — | Extend-video mode. Source must be 2–15 s. |
| `--poll-interval` | seconds | 5 | How often to check status |
| `--poll-timeout` | seconds | 900 (15 min) | Bail out if not done by then |
| `--output` | path | required | Where to save the downloaded MP4 |
| `--keep-url` | flag | off | Skip the download, only print the xAI-hosted URL |

## Things to know

- **Asynchronous.** Generation typically takes a couple minutes; long / 720p / edit jobs take longer. The script handles polling — don't introduce your own loop on top.
- **URLs are ephemeral.** xAI returns a temporary hosted MP4 URL. The script downloads it immediately. Pass `--keep-url` only if you'll fetch within minutes.
- **Edit mode is constrained.** Editing inherits the source video's duration, aspect, and resolution; passing those flags is silently ignored by the API. Editing input is also capped at **8.7 seconds**.
- **Extend mode bookkeeping.** `--duration` is the length of the **new portion**. A 10s source + `--duration 5` → 15s output.
- **Mode collisions error out 400.** Don't combine `--image` and `--reference-image`, and don't combine `--edit-video` and `--extend-video`.
- **Moderation.** Output may be filtered. The response carries a `respect_moderation` flag; if the model declines the prompt, rewrite rather than retry verbatim.
- **Status enum.** `pending` → keep polling, `done` → download, `expired` → request lifecycle ended (re-submit), `failed` → permanent failure (rewrite prompt or check inputs).

## When to escalate

- Need still images, not video → use the sibling `grok-image` or `gpt-image-2` skills.
- Need precise editing of specific regions / masks → not supported here; use `gpt-image-2` for image masking and consider re-animating.
- Need >15 s of fully novel content → chain extends (each adds up to 10s) or generate multiple clips and stitch them externally.
