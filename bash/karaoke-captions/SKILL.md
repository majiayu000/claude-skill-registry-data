---
name: karaoke-captions
description: >
  Generate TikTok/Shorts-style karaoke captions using MLX Whisper, ASS subtitles,
  and FFmpeg libass. Use when burning word-level highlight captions into a video,
  matching caption style from a screenshot, rendering ASS karaoke subtitles, or
  when the user runs /karaoke-captions.
user_invocable: true
---

# Karaoke Captions Skill

Generate dynamic, TikTok/Shorts-style karaoke captions with word-level highlight sweeps using ASS subtitles and FFmpeg `libass`. Supports style matching from a reference screenshot.

Scripts, presets, and references live next to this skill. Run the commands from the skill directory (or pass absolute paths).

## Requirements

- macOS with Apple Silicon (MLX Whisper)
- Python 3.10+
- [FFmpeg](https://ffmpeg.org/) with `libass` (`brew install ffmpeg`)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```text
reference.png --------(match_style_from_image.py)--------> style.json --+
                                                                   +--(gen_ass.py)--> captions.ass --(render.sh)--> output.mp4
input.mp4 ---------------------------------->(extract_words.py)--> words.json --+
```

---

## File Architecture

| File | Purpose | Role |
|---|---|---|
| `input.mp4` | Source video | Input |
| `reference.png` | Style reference image (optional) | Visual Prompt |
| `words.json` | Word-level timestamps `[{"word": ..., "start": ..., "end": ...}]` | Persistent Raw Data |
| `style.json` | Font, size, highlight color, outline, soft shadow, margin, words per line | Style Config |
| `captions.ass` | ASS subtitle script with two-layer blurred drop shadow and inline color overrides | Generated Intermediate |
| `output.mp4` | Final video with burned-in subtitles | Output Deliverable |

---

## Standard Workflow

### Step 1. Extract Word Timestamps

```bash
python scripts/extract_words.py \
  input.mp4 words.json \
  --model mlx-community/whisper-large-v3-turbo
```

*(For Chinese videos, add `--language zh`)*.

### Step 2. Select Style or Auto-match from Reference Image

- **From Reference Image**:
  ```bash
  python scripts/match_style_from_image.py \
    reference.png style.json --video input.mp4
  ```
- **From Presets**:
  - `presets/style.json`: Default neon green highlight (`#00FF00`), Arial Black, all-caps, 4 words/line.
  - `presets/yellow.json`: Yellow highlight (`#FFFF00`), Arial Black, all-caps.

To adjust appearance manually, see [Style Guide](./references/style-guide.md).

### Step 3. Generate ASS Subtitles

```bash
python scripts/gen_ass.py \
  words.json style.json captions.ass --video input.mp4
```

### Step 4. Render Preview & Visual Check

```bash
# Preview segment:
scripts/render.sh input.mp4 captions.ass preview.mp4 3 8

# Frame snapshot:
scripts/render.sh frame input.mp4 captions.ass preview_frame.png 4.5
```

### Step 5. Render Final Video

```bash
scripts/render.sh input.mp4 captions.ass output.mp4
```

---

## References & Presets

- [Style Guide](./references/style-guide.md)
- Presets:
  - [presets/style.json](./presets/style.json)
  - [presets/yellow.json](./presets/yellow.json)
- Scripts:
  - [scripts/extract_words.py](./scripts/extract_words.py)
  - [scripts/match_style_from_image.py](./scripts/match_style_from_image.py)
  - [scripts/gen_ass.py](./scripts/gen_ass.py)
  - [scripts/render.sh](./scripts/render.sh)
