---
name: ingest
description: Download a source video from a YouTube/URL into ./work/<id>/source.mp4 using yt-dlp, and emit ingest.json with metadata (title, duration, fps, url, source_id). First step of the shorts pipeline.
---

# ingest

Thin yt-dlp wrapper. Atomic: one URL in, one source.mp4 + ingest.json out.
Idempotent — if `source.mp4` and `ingest.json` already exist for the same
URL hash, skips the download.

## Inputs
- `url`: video URL (required)
- `id` (optional): source id slug; defaults to a short sha1 of the URL
- `workdir` (optional): root work directory; defaults to `./work`

## Output
- `./work/<id>/source.mp4` — the downloaded video, mp4 container
- `./work/<id>/ingest.json` — metadata, shaped as:

```json
{
  "id": "<id>",
  "url": "<url>",
  "title": "...",
  "duration": 183.4,
  "fps": 30.0,
  "width": 1920,
  "height": 1080,
  "path": "work/<id>/source.mp4"
}
```

## How
1. Compute `id` from URL (`sha1(url)[:10]`) if not given.
2. `mkdir -p work/<id>`.
3. `yt-dlp -f 'bv*+ba/b' --merge-output-format mp4 --embed-metadata --print-to-file '%(title)s' work/<id>/.title.txt -o 'work/<id>/source.%(ext)s' <url>`
4. `ffprobe -v error -print_format json -show_format -show_streams work/<id>/source.mp4`
   → extract duration, fps, width, height.
5. Title comes from yt-dlp's `.title.txt` (merged-mp4 container tags are unreliable and often empty); falls back to the container `title` tag.
6. Write `ingest.json`.

## Invoke
```bash
.claude/skills/ingest/ingest.sh <url> [id]
```

## Status
Implemented. See `ingest.sh`.
