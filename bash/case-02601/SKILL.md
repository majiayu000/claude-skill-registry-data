---
name: skill-video-caption-overlay
description: Render TikTok-style animated pill captions onto short-form videos using MoviePy + PIL. Takes a base MP4, a captions JSON, and optional background audio — outputs a final video with fade-in/out pill overlays. Fixes the PIL textbbox y-offset bug that causes text to sit outside pill boundaries. Use for TikTok ads, Reels, YouTube Shorts.
metadata:
  openclaw:
    requires: { bins: ["uv"] }
---

# Video Caption Overlay

Animated pill-style caption overlays for short-form video. No Premiere, no CapCut — pure Python.

## Usage

```bash
uv run --with moviepy --with pillow scripts/overlay.py \
  --video base.mp4 \
  --output final.mp4 \
  --captions scripts/example_captions.json \
  --audio music.mp3 \
  --audio-start 8 \
  --audio-vol 0.5
```

No `--audio` if you want to keep the original video audio.

## Custom fonts

```bash
--font-black /path/to/Montserrat-Black.ttf \
--font-bold  /path/to/Montserrat-Bold.ttf
```

Falls back to Montserrat from `~/.local/share/fonts/` if not specified.

## captions.json format

Array of **phases** — each phase is a time window with one or more pill lines stacked vertically.

```json
[
  {
    "start": 0,
    "end": 3.2,
    "y_frac": 0.06,
    "lines": [
      {
        "text": "POV:",
        "size": 28,
        "bold": true,
        "bg": [0, 195, 255],
        "fg": [0, 0, 0],
        "bg_opacity": 0.9,
        "px": 20, "py": 9, "r": 12
      },
      {
        "text": "drink more water",
        "size": 50,
        "bg": [255, 255, 255],
        "fg": [0, 0, 0]
      }
    ]
  }
]
```

| Field | Type | Default | Description |
|---|---|---|---|
| `start` | float | required | Phase start time (seconds) |
| `end` | float | required | Phase end time (seconds) |
| `y_frac` | float | 0.06 | Vertical position as fraction of video height |
| `lines[].text` | string | required | Caption text |
| `lines[].size` | int | 50 | Font size (px) |
| `lines[].bold` | bool | false | Use bold font (vs black/heavy) |
| `lines[].bg` | [R,G,B] | [255,255,255] | Pill background color |
| `lines[].fg` | [R,G,B] | [0,0,0] | Text color |
| `lines[].bg_opacity` | float | 0.93 | Pill background opacity (0–1) |
| `lines[].px` | int | 26 | Horizontal padding |
| `lines[].py` | int | 13 | Vertical padding |
| `lines[].r` | int | 18 | Border radius |

## PIL textbbox fix

PIL's `textbbox((0,0), text, font)` returns `(x0, y0, x1, y1)` where `y0` is a non-zero offset (typically 7–15px depending on font size). Drawing text at `(x, y)` without compensating for this offset causes text to appear below the pill's visual center.

**Fix implemented in `pill()`:**
```python
bb    = draw.textbbox((0, 0), text, font=font)
x_off, y_off = bb[0], bb[1]
vis_w = bb[2] - bb[0]   # actual visual width
vis_h = bb[3] - bb[1]   # actual visual height

# Compensate offsets when drawing text
tx = cx - vis_w // 2 - x_off
ty = y - y_off
draw.text((tx, ty), text, font=font, fill=fg)
```

## Emoji note

NotoColorEmoji.ttf fails with PIL at arbitrary sizes (bitmap font with limited supported sizes). Use text alternatives (`"Free delivery"` instead of `"Free delivery 🚚"`) for reliable rendering.

## Example output

See `scripts/example_captions.json` for the full 3-phase TikTok ad structure:
- Phase 1 (0–3.2s): Hook — top-screen pill stack
- Phase 2 (2.8–5.8s): Product claim — overlapping fade
- Phase 3 (5.3–8.0s): CTA — bottom-screen price + delivery + bio link
