---
name: transcript-video-section-splitter
description: Use when transcribing a video, deriving topic-based section boundaries from the transcript, and splitting the video into named clips with ffmpeg plus a manifest, instead of cutting by fixed duration.
triggers:
  - split video by transcript
  - split video into sections
  - transcript based video split
  - video chapters from transcription
  - content based video clips
  - Whisper video sections
  - split panda face video
  - split edited video as before
  - reuse section JSON for new video
  - generate section clips from transcript
---

# Transcript Video Section Splitter

Use this skill when the user wants a long video divided into meaningful content sections based on what is said. The output should include a timestamped transcript, section metadata, and split video clips.

## Core Rules

- Transcribe first; do not guess section boundaries from duration alone.
- Keep the original media unchanged. Split from a derived edited video when the user asks to section that edited version.
- If the user asks to split a regenerated or edited variant "as before", reuse the existing section JSON only when the variant preserves the same timeline and final duration.
- Use topic changes, long pauses, repeated framing phrases, and concrete action shifts to set boundaries.
- Store section boundaries in durable JSON before cutting clips.
- Preserve audio and avoid unnecessary re-encoding when exact keyframe cuts are acceptable; re-encode when frame-accurate starts matter.
- Write variant clips to a variant-specific folder such as `artifacts/.../v2/sections/` so older split outputs are not overwritten.
- Keep private or raw transcripts separate when the clips or section summaries will be published.

## Recommended Layout

```text
text/
  source.md                         # timestamped transcript
artifacts/video_sections/
  source_sections.json              # machine-readable boundaries
  source_sections.md                # human-readable chapter table
  clips/
    01_topic-slug.mp4
    manifest.json
```

## Transcription

Use the project convention first. Common commands:

```bash
python transcribe.py \
  -i video/source.mp4 \
  -o text/source.md \
  -m medium \
  -l zh
```

For higher-quality alignment or speaker labels:

```bash
conda run -n whisperx whisperx video/source.mp4 \
  --model large-v2 \
  --language zh \
  --task transcribe \
  --output_dir text/source.whisperx \
  --output_format json
```

## Section Metadata

Create JSON with explicit starts, ends, slugs, titles, and summaries:

```json
[
  {
    "index": 1,
    "start": "00:00:00.000",
    "end": "00:00:52.000",
    "slug": "problem-framing",
    "title": "Problem framing",
    "summary": "The opening defines the key problem and constraints."
  }
]
```

Boundary guidance:

- Use `00:00:00.000` for the first start unless there is a clear pre-roll to remove.
- End the final section at the media duration from `ffprobe`.
- Prefer section lengths that match natural content, not equal sizes.
- Avoid cutting in the middle of a sentence unless the user asks for short social clips.
- Include a Markdown table for review before cutting if the sectioning is subjective.

## Splitting

Stream-copy is fast but may cut on nearby keyframes:

```bash
ffmpeg -y -ss 12.000 -i edited_video.mp4 -t 48.000 -c copy clips/01_topic.mp4
```

Use re-encoding for frame-accurate cuts:

```bash
ffmpeg -y -ss 12.000 -i edited_video.mp4 -t 48.000 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac clips/01_topic.mp4
```

Write a `manifest.json` with clip index, title, start, end, duration, and path.

When a helper script already exists, prefer it over hand-running many `ffmpeg` commands. For example:

```bash
python3 split_video_by_sections.py \
  --input artifacts/edited_variant/source_edited.mp4 \
  --sections text/source_sections.json \
  --output-dir artifacts/edited_variant/sections \
  --reencode \
  --overwrite
```

For a new edited variant that shares the same transcript timeline:

1. Probe the variant duration with `ffprobe`.
2. Confirm it matches the section JSON final end time, allowing only normal container padding.
3. Reuse the previous `text/*_sections.json`.
4. Save clips under the variant output folder.
5. Validate every clip with `ffprobe` for both video and audio streams.

Validation helper:

```bash
python3 - <<'PY'
import json, subprocess
from pathlib import Path
manifest = json.loads(Path('artifacts/edited_variant/sections/manifest.json').read_text())
print('clips', len(manifest))
for item in manifest:
    path = Path(item['path'])
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration,size',
        '-show_entries', 'stream=codec_type',
        '-of', 'json',
        str(path),
    ], text=True))
    types = [s['codec_type'] for s in probe['streams']]
    fmt = probe['format']
    print(f"{item['index']:02d} {float(fmt['duration']):8.3f}s {int(fmt['size'])/1024/1024:7.1f} MB {types} {path.name}")
PY
```

## Validation Checklist

- Transcript exists and includes timestamps.
- Section JSON covers the full intended duration without overlap or gaps.
- Section titles and summaries are content-based and neutral.
- Clips exist, play, and preserve audio.
- Reused section JSON is timeline-compatible with the edited variant.
- Variant clips are written to a new folder rather than overwriting previous clips.
- Manifest matches the generated clip filenames.
- At least the first, middle, and final clips are spot-checked.
- Generated sections are derived from transcript content, not private chat context.
