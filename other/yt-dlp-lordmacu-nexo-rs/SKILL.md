---
name: yt-dlp
description: Download videos, extract audio, or fetch metadata from YouTube, Twitter/X, Instagram, TikTok, and many more sites.
requires:
  bins:
    - yt-dlp
  env: []
---

# yt-dlp

Wraps the `yt-dlp` CLI. Use for metadata extraction, format listing, and
(gated) downloads to local disk.

## Use when

- "Download this video" / "grab the audio as mp3"
- "What's the title / duration / channel of this link?"
- Piping into `openai-whisper` for transcription (download audio → whisper)
- Piping into `summarize` with video metadata + captions

## Do not use when

- Live streaming playback — use a media player
- Bulk scraping of large channels — run yt-dlp directly with a queue

## Tools

- `status` — yt-dlp binary version + output dir
- `info` — `url` → title, duration, channel, upload date, webpage URL
- `formats` — `url` → list of available formats (id, ext, resolution, codecs, size)
- `download` — `url` + optional `mode` (`video` default / `audio`), `format` (yt-dlp -f selector),
  `audio_format` (mp3 default / m4a / opus), `output_dir`

## Write gate

`download` requires `YTDLP_ALLOW_DOWNLOAD=true`. Without it, returns `-32041`.

## Env

| Var | Default |
|-----|---------|
| `YTDLP_BIN` | `yt-dlp` |
| `YTDLP_OUTPUT_DIR` | `$TMPDIR/agent-yt-dlp` |
| `YTDLP_ALLOW_DOWNLOAD` | — (must be `true` to download) |

## Typical flow

1. `info` to confirm the URL is valid and preview title/duration.
2. `download` with `mode=audio` for podcast-style content, then feed the
   `output_path` into `openai-whisper` → `summarize`.
