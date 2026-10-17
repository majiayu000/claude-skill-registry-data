---
name: parse-youtube
description: Extract a transcript, timestamps, metadata and chapters from a public YouTube URL. Use when someone drops a YouTube link and wants the gist, a quotable moment, or the text to feed into something else.
---

# Skill: parse-youtube

Extract transcripts, timestamps, metadata and chapters from any public YouTube video.

## When to use

- Someone pastes a YouTube URL and asks a question about it
- A draft needs a quote or a claim sourced from a talk
- You need to find a specific moment inside a long video without watching it
- Pre-step before indexing video content into a vector store

## CLI contract

```bash
python3 "$PARSE_YOUTUBE_SCRIPT" <url_or_video_id> [--lang en] [--format json|markdown|both] [--no-metadata]
```

`$PARSE_YOUTUBE_SCRIPT` is exported by the plugin's env contract and points at
`scripts/parse-youtube.py` inside the plugin directory. Standalone, call the
script by path.

**Arguments:**

- `url_or_video_id` - any YouTube URL shape (`youtube.com/watch?v=`, `youtu.be/`, `/embed/`, or a raw 11-character ID)
- `--lang` - preferred language code, comma-separated for priority order. Overrides the configured `default_language`. The configured `fallback_languages` are always appended after it.
- `--format` - `json` (default), `markdown`, or `both`
- `--no-metadata` - skip the yt-dlp call for a faster transcript-only run

**JSON output schema:**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "...",
  "channel": "...",
  "duration_seconds": 213,
  "language": "en",
  "description": "... (truncated to description_max_chars)",
  "chapters": [{"title": "...", "start": 0}],
  "transcript": [{"start": 0.0, "duration": 2.5, "text": "..."}],
  "full_text": "...",
  "markdown": "..."
}
```

`markdown` is present only when `--format` is `markdown` or `both`.

**Markdown output:** `# Title`, then channel and duration, a chapters section if
the video has one, the description, and the transcript with bold `[M:SS]`
timestamp anchors on every line. Drops straight into a draft.

## Configuration

| Key | Default | What it controls |
|---|---|---|
| `default_language` | `en` | Caption language tried first |
| `fallback_languages` | `["en"]` | Languages tried after the preferred one. Set this to the languages your install actually reads. |
| `metadata` | `true` | Whether to spend the yt-dlp call on title/channel/chapters |
| `metadata_timeout_seconds` | `30` | When yt-dlp is abandoned. Metadata goes null; the transcript is unaffected. |
| `description_max_chars` | `1000` | Description truncation. Descriptions are often link dumps. |

## Examples

```bash
# JSON with full transcript
python3 "$PARSE_YOUTUBE_SCRIPT" "https://youtu.be/dQw4w9WgXcQ"

# Markdown, ready to paste into a draft
python3 "$PARSE_YOUTUBE_SCRIPT" "https://youtu.be/dQw4w9WgXcQ" --format markdown

# Prefer the Portuguese caption track, fall back to whatever is configured
python3 "$PARSE_YOUTUBE_SCRIPT" "https://youtu.be/VIDEOID" --lang pt

# Transcript only, no metadata round-trip
python3 "$PARSE_YOUTUBE_SCRIPT" "https://youtu.be/VIDEOID" --no-metadata
```

## Limitations

- The video must have captions, auto-generated or manual. Captions-disabled videos error out.
- Metadata adds roughly 5 seconds. On failure or timeout the metadata fields come back null and the transcript still succeeds.
- Age-restricted, private, and members-only videos fail. There is no authenticated path here on purpose.
- YouTube changes its player often enough that yt-dlp needs periodic updating. A stale yt-dlp shows up as null metadata, not as an error.

## Downstream: vector indexing

The `transcript` array is already the right shape for chunked embedding. Each
segment becomes one chunk: `start` is the seek offset to link back to, `text` is
the embedding input, `video_id` is the source reference. Segments are short, so
most installs will want to merge adjacent ones up to a token budget before
embedding rather than indexing each line.
