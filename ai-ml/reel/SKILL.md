---
name: reel
description: >
  Auto-edit a raw talking-head clip into a finished vertical 9:16 reel — local
  transcription, word-synced burned captions, hook card, scale/crop, NVENC export.
  Trigger when the user says "auto-edit this clip", "make a reel from this", "/reel",
  or drops a raw .mp4 and wants it captioned + hook-carded with no manual editing.
---

# AI Auto-Edit Reel Pipeline (SkynetLabs)

You turn ONE raw take into a publish-ready reel. No timeline, no human editor.

## When to use

User drops a raw vertical (or any) clip and wants it captioned + hook-carded automatically.

## Steps

1. **Deps:** ensure `ffmpeg` is on PATH. Ensure `faster-whisper` installed
   (`pip install -r requirements.txt` if not).
2. **Run:**
   ```
   python auto_reel.py "<clip>" --hook "<HOOK TEXT>" --sub "<SUBLINE>" --out reel.mp4
   ```
3. **Verify:** `ffprobe` the output → confirm 1080x1920 and sane duration.
4. **Report** the path and offer next step (schedule / caption pack).

## What the script does

- `faster-whisper` → word-level timestamps (local, $0)
- builds an ASS subtitle track, 3 words per line, burned in
- hook card (`drawtext`, semi-transparent box) for the first 2.5s
- scale to 1080x1920 + center-crop to 9:16
- export: `h264_nvenc` → falls back to `libx264` if no GPU

## Flags

- `--hook` on-screen hook (default "THIS REEL EDITED ITSELF")
- `--sub` gold subline (default "FULLY AI / ZERO HUMAN EDITOR")
- `--model` whisper size tiny|base|small|medium (default base)
- `--hook-len` seconds the hook card shows (default 2.5)
- `--wpl` words per caption line (default 3)

## Gotchas

- Windows: the script runs ffmpeg from a temp dir so the `subtitles=` path needs no
  colon-escaping. Don't "fix" it to an absolute path.
- No audio in clip → script exits early; that's correct.

Built by SkynetLabs — www.skynetjoe.com
