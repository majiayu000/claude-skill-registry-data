---
name: video-transcribe
description: Use when the user asks to transcribe, extract subtitles, summarize a raw transcript, translate, or get text from a YouTube or Bilibili video URL through Stardust Video Transcribe.
metadata:
  requires:
    bins:
      - python3
---

# Video Transcribe

Use Stardust Video Transcribe to extract transcript text from YouTube and
Bilibili video URLs.

## Endpoint

```text
https://video-transcribe.preseen.ai/transcribe
```

OpenAPI:

```text
https://video-transcribe.preseen.ai/openapi.json
```

## Authentication

The bundled client authenticates through the shared Stardust Cloudflare Access
client. The first normal request opens a browser for company login; sign in
with an authorized `@stardust.ai` identity. Refresh tokens stay in the local
owner-only store and are isolated by service origin.

Check or remove the Video Transcribe session without starting a job:

```bash
python3 "$HOME/.agents/skills/video-transcribe/scripts/video_transcribe.py" --auth-status
python3 "$HOME/.agents/skills/video-transcribe/scripts/video_transcribe.py" --logout
```

Approved headless workloads set both `CF_ACCESS_CLIENT_ID` and
`CF_ACCESS_CLIENT_SECRET` from their secret manager. Never set only one or
expose either value in chat, source, logs, or reports.

## Request

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "prefer_subtitles": true,
  "langs": ["zh.*", "en.*"],
  "combine_subtitles": false,
  "keep_workdir": false
}
```

## Usage

```bash
python3 "$HOME/.agents/skills/video-transcribe/scripts/video_transcribe.py" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

Return the complete response as JSON and save it:

```bash
python3 "$HOME/.agents/skills/video-transcribe/scripts/video_transcribe.py" \
  "https://www.bilibili.com/video/BV..." \
  --format json \
  --output "/absolute/path/to/transcript.json"
```

Prefer server-side ASR instead of platform subtitles, or choose language
patterns explicitly:

```bash
python3 "$HOME/.agents/skills/video-transcribe/scripts/video_transcribe.py" \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --no-prefer-subtitles \
  --lang 'zh.*' \
  --lang 'en.*'
```

Return the `text` field to the user or use it as source material for
summarization, translation, or analysis. Preserve `source`, `title`, and
`video_id` in citations when useful.

## Notes

- `source=subtitles` means the service used platform captions.
- `source=funasr` means the service downloaded audio and ran server-side ASR.
- For private Bilibili or member videos, configure server-side cookies. Do not
  send browser cookies in chat.
- The hostname needs its own Cloudflare Access application and AUD. If metadata
  is missing, rule out a local `198.18.x.x` fake-IP/proxy path before treating
  it as a service-side configuration problem.
