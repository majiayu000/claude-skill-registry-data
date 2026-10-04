---
name: video-editing
description: Assemble and edit the paper video — timeline.json, inserting other videos (demos, screen recordings, study footage), trimming, cropping, optional speed changes, labels, picture-in-picture, crossfades, voice-over on clips, size limits, and reviewing the result. Use for stages 5-6 of paper-to-video or any ffmpeg-style edit in this repo.
---

# Video assembly and editing

## The timeline

`P/timeline.json` is the edit decision list. `uv run scripts/make_timeline.py P` writes a starter from
slides + narration; then edit it by hand.

```json
{
  "output": "out/video.mp4",
  "settings": {"width": 1920, "height": 1080, "fps": 30, "background": "#F4F1EA", "fade": 0.35,
               "max_mb": 200, "max_minutes": 5},
  "items": [
    {"slide": "01-title", "lead": 0.8, "chapter": "Introduction"},
    {"slide": "02-method"},
    {"clip": "media/demo.mp4", "start": 120, "end": 210, "crop": "1920:1040:0:40",
     "narration": "03-demo", "duck": 0.2,
     "label": {"text": "Live demo", "corner": "bl"}, "chapter": "Demo"},
    {"image": "figures/teaser.png", "duration": 4},
    {"slide": "09-takeaway", "tail": 1.0}
  ]
}
```

Item fields:

- **slide**: `slide` (id: uses `out/slides/<id>.png` and `audio/<id>.wav`), `lead` (silence before the
  voice, default 0.25 s), `tail` (after, 0.35 s), `duration` (minimum length, or fixed length if no audio),
  `audio` (another id or wav path; `false` = silent), `fade`, `chapter`.
- **image**: same as slide but `image` is any picture path; needs `duration` or `audio`.
- **clip**: `clip` (video path), `start`/`end` (seconds in the source), `crop` (`w:h:x:y` in source pixels, applied before
  scaling), `volume` (original audio, 0 = mute), `narration` (id or wav), `narration_offset` (0.5 s),
  `narration_volume`, `duck` (original volume while narration plays, 0.25), `extend` (hold last frame if
  narration is longer, true), `label` (text, or `{"text", "corner": tl|tr|bl|br|tc|bc, "from", "to", "size"}`),
  `fade`, `chapter`.
  Optional, off by default: `speed` (constant factor) and `smart_speed` (number, or
  `{"speed": 8, "noise": "-35dB", "min_silence": 1.2, "speech_speed": 1.0}`: speech at normal speed,
  silent stretches sped up, nothing cut).
- `note` is ignored (use it for comments).

**Clips play at normal speed by default.** Add `speed` or `smart_speed` only when the user asks to
shorten or speed up footage. If a clip is too long, suggest trimming or speeding up and let the user
choose.

Every item is converted to the same format (1920x1080, 30 fps, H.264, AAC 48 kHz stereo; other aspect
ratios are letterboxed in the background colour), so any source video can be mixed in. Put source
videos in `P/media/`.

## Build and review

```bash
uv run scripts/assemble_video.py P --draft --sheet   # 960x540 fast encode + contact sheet PNG
uv run scripts/assemble_video.py P                   # final
uv run scripts/assemble_video.py P --clean           # drop cached segments first
```

The script validates the whole timeline before encoding and lists every problem. It prints each item's
start time and length, writes `<output>.chapters.txt` from `chapter` fields, and warns when `max_mb` or
`max_minutes` is exceeded. Segments are cached; editing one item re-encodes only that item.

**Always review**: read the `--sheet` PNG, and for clips grab frames at specific moments:
`uv run scripts/videotools.py frame out/video.mp4 /tmp/f.png --at 42`. Check that crops remove what they
should (browser bars, desktop chrome, identifying info) and labels are legible.

## Before inserting footage

1. `uv run scripts/videotools.py probe media/x.mp4` for length, resolution, audio.
2. Find the part to use: make a sheet (`videotools.py sheet media/x.mp4 /tmp/s.png --cols 6 --rows 5`) or
   frames at candidate times; ask the user for timestamps when the content can't be judged from frames.
3. Long recordings: choose `start`/`end` around one representative episode. Speeding up (`speed`, or
   `smart_speed` for silent stretches only) is opt-in; when used, say so in a label or the narration.

## Standalone tools (`scripts/videotools.py`)

| command | does |
|---|---|
| `probe IN` | duration, size, streams |
| `trim IN OUT --start S --end E` (or `--dur`) | cut a range |
| `crop IN OUT --crop w:h:x:y` | crop |
| `speed IN OUT --factor F` | constant speed change (audio pitch preserved) |
| `smart-speed IN OUT --speed 8 [--start --end]` | optional: speed up silent stretches only |
| `normalize IN OUT [...]` | convert to the pipeline format |
| `still IMAGE OUT --dur 5 [--audio a.wav]` | image to video |
| `dub VIDEO VOICE OUT --offset 1 --duck 0.2` | voice-over with ducking |
| `pip BASE OVERLAY OUT --at 10 --corner br --width 560 [--with-audio]` | picture-in-picture (output has BASE's length) |
| `label IN OUT --text "..." --from 0 --to 5 --corner bl` | text pill overlay |
| `concat OUT IN1 IN2 ... [--normalize]` | join (use `--normalize` for clips from elsewhere) |
| `xfade A B OUT --dur 0.8` | crossfade two clips (both need audio) |
| `audio IN OUT.wav` / `frame IN OUT.png --at T` / `sheet IN OUT.png` | extract |
| `shrink IN OUT --target-mb 100` | two-pass encode to fit a size cap |

A pre-made composite (e.g. a `pip` result) becomes a normal `clip` item in the timeline.
This ffmpeg build may lack `drawtext`/`subtitles`; labels are rendered as PNGs with Playwright instead,
so do not switch to drawtext.
