---
name: decisions-yt-dlp
description: Use yt-dlp for YouTube (and supported sites) metadata, subtitles, and search inside Decisions workflows — not for Bilibili (use bili-cli via agent-reach).
---

# Decisions yt-dlp

[yt-dlp](https://github.com/yt-dlp/yt-dlp) runs in the Decisions venv (`pip install yt-dlp` via `bin/setup.py`).

## When to use

| Job | Tool |
|-----|------|
| Video metadata / title / description | yt-dlp `--dump-single-json` |
| Subtitles / transcript for editing | yt-dlp `--write-sub --skip-download` |
| YouTube search (no API key) | `ytsearch5:query` |
| 30-day multi-source research | **last30days** (uses yt-dlp internally) |
| General social/web fetch | **agent-reach** |
| Cut/edit/remotion pipeline | **video-editing**, **remotion-video-creation** |

## Workflow step (`ytdlp` action)

```json
{"mode": "metadata", "url": "https://www.youtube.com/watch?v=VIDEO_ID"}
{"mode": "subtitles", "url": "...", "sub_lang": "en"}
{"mode": "search", "query": "LLM agents 2026", "limit": 5}
{"mode": "download", "urls": ["https://www.youtube.com/watch?v=VIDEO_ID"], "title": "My clips"}
```

For downloads, use agent tool **`ytdlp_download`** or workflow `download` mode — opens **Download Manager** (`/downloads/`) with live progress.

Output is JSON in the step result (truncated to 2k chars). Attach full subtitle files from `/tmp` in agent steps when needed.

## Agent CLI cheatsheet

```bash
# Metadata
yt-dlp --dump-single-json --no-download "URL"

# Subtitles to /tmp
yt-dlp --write-sub --write-auto-sub --sub-lang en --skip-download -o "/tmp/%(id)s" "URL"

# Search
yt-dlp --dump-single-json --flat-playlist "ytsearch5:your query"
```

## Rules

- **Do not use yt-dlp for Bilibili** — blocked by site; use `bili search` (agent-reach).
- Keep downloads under `/tmp` unless the ticket asks to commit media.
- Upgrade if captions break: `pip install -U yt-dlp` or `brew upgrade yt-dlp`.
- Cite `webpage_url` and `title` in workflow evidence packets.

Reference source: `../reference/yt-dlp` (upstream repo clone).
