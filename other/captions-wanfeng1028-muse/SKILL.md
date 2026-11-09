---
name: captions
version: 1.0.0
description: Add subtitles/captions to a video — burn them into the picture, or export an .srt/.vtt file (for YouTube etc.). Use whenever the user wants captions, subtitles, on-screen text of what's being said, an SRT/VTT file, or accessibility text. Covers auto-transcription, editing for accuracy, styling, and the verbatim-vs-clean gotcha.
---

# Captions & subtitles

Two outputs, one transcription engine (mlx-whisper, same as `transcribe`):
- **Sidecar file** (`.srt` / `.vtt`) — for YouTube/Vimeo upload, re-editing, or other tools.
- **Burned-in** — pixels baked into the video (social clips where the player won't show a
  subtitle track). Rendered via PIL → ffmpeg overlay (mise ffmpeg lacks `drawtext`).

## CRITICAL: use `--clean` for captions

This is the opposite of `filler-removal`. Whisper is **verbatim by default** here (keeps
um/uh) because filler-removal needs them. Subtitles do **not** — viewers don't want "um, uh"
on screen. Always pass `--clean` when transcribing for captions:

```bash
uv run video-agent transcribe video.mp4 --clean --srt -o subs.srt
```

## Export a subtitle file (no burn-in)

```bash
uv run video-agent transcribe video.mp4 --clean --srt -o subs.srt   # SubRip
uv run video-agent transcribe video.mp4 --clean --vtt -o subs.vtt   # WebVTT
```

Upload `subs.srt` alongside the video, or hand-edit it (fix names/typos, retime) and burn
that edited file — see below.

## Burn captions into the video

```bash
# Auto-transcribe and burn in one step (uses --clean transcription internally? NO — pass it)
uv run video-agent captions video.mp4 -o captioned.mp4 --clean

# Best workflow for accuracy: transcribe → hand-edit the .srt → burn the edited file
uv run video-agent transcribe video.mp4 --clean --srt -o subs.srt
#   ...fix typos, proper nouns, retime any off lines in subs.srt...
uv run video-agent captions video.mp4 --srt subs.srt -o captioned.mp4
```

`--srt` accepts both `.srt` and `.vtt`. When `--srt` is given, no transcription runs — it
just burns the file you pass, so this is also how you re-burn after editing.

### Styling

```bash
uv run video-agent captions video.mp4 -o out.mp4 --srt subs.srt \
    --size 48 --color yellow --position bottom --no-box
```

- `--size` px (default ~5% of frame height) · `--color` white|yellow|red|black
- `--position` bottom (default) | top | center
- `--no-box` removes the semi-transparent legibility box (keep it for busy backgrounds)
- Text auto-wraps to ~90% of frame width, centered.

## Gotchas

- **Caption count = encode passes? No — one pass.** Every segment becomes a full-frame RGBA
  PNG overlaid with an `enable='between(t,…)'` gate, all in a single ffmpeg encode. Fine for
  clips and typical talks. For a very long video (many hundreds of segments) the command
  line gets large; split the video, caption each part, then concat.
- **Timing comes from whisper segment boundaries**, which read fine but can be ~0.3s loose.
  For tight sync, edit the times in the `.srt` and re-burn with `--srt`.
- **Word-level "karaoke" captions** (one or two words popping per beat) aren't built in here.
  Approximate by transcribing `--words`, grouping into short segments, and writing your own
  `.srt` with tight start/end per group, then `captions --srt`. For *animated* per-word pops
  (eased, scaled), use the optional `remotion-graphics` skill's `KineticCaption` — fed the same
  `--words` timestamps. Either way the timing is **grepped from the `--words` transcript, never
  scrubbed.**
- **Burn on the final-resolution video.** If you're also reframing for social
  (`reframe` skill), reframe **first**, then caption — so font size and wrapping match the
  output frame, not the original.
