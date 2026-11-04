---
name: podcast-to-md
description: "Podcast to Markdown — Turn any Apple Podcast into structured Markdown files with full metadata and transcripts. Use when the user wants to transcribe, archive, or extract content from podcast episodes. Supports search by name or Apple Podcasts URL, date filtering, automatic transcript detection (RSS/Podcasting 2.0), and local Whisper transcription as fallback."
---

# Podcast to Markdown

Turn podcast episodes into structured Markdown files. Each output file is a self-contained knowledge unit with rich frontmatter, show notes, and timestamped transcript — designed for downstream processing: summarization, search, quote extraction, knowledge graphs.

## Scripts

```bash
# Find a podcast
.agents/skills/podcast-to-md/scripts/search "podcast name or Apple Podcasts URL"

# List episodes with metadata
.agents/skills/podcast-to-md/scripts/episodes <rss_url> [--from YYYY-MM] [--to YYYY-MM] [--recent N] [--all]

# Transcribe audio locally
.agents/skills/podcast-to-md/scripts/transcribe <audio_url_or_file> [--model medium] [--language xx]
```

### search

| Flag | Effect |
|------|--------|
| `--limit N` | Max results (default: 5) |

Accepts a podcast name, Apple Podcasts URL (`podcasts.apple.com/...`), or numeric Apple ID. Returns JSON array.

### episodes

| Flag | Effect |
|------|--------|
| `--from YYYY-MM[-DD]` | Start date (inclusive) |
| `--to YYYY-MM[-DD]` | End date (inclusive) |
| `--recent N` | Last N episodes (default: 10) |
| `--all` | All episodes |

Returns JSON with podcast metadata, episode list, and counts.

### transcribe

| Flag | Effect |
|------|--------|
| `--model SIZE` | Whisper model: tiny, base, small, medium, large-v3 (default: medium) |
| `--language XX` | Language hint (auto-detect if omitted) |

Outputs `[HH:MM:SS] text` per line to stdout. Progress to stderr. First run downloads the model (~1-3GB).

## Workflow

Follow these steps in order. Each step requires the previous step's output.

### Step 1: Identify the podcast

- If the user gives a podcast name: run `search "name"`
  - If multiple results, present them and ask the user to pick one
  - Show: name, artist, episode count, genre
- If the user gives an Apple Podcasts URL: run `search "URL"` — should return exactly one result
- Confirm the podcast with the user before proceeding

### Step 2: Get episode list

- Run `episodes <rss_url>` with the user's time filter
- Show the user a summary:
  - Number of episodes found
  - Date range
  - Episodes with existing transcript URLs vs. those needing Whisper
- Ask the user to confirm before processing

### Step 2.5: Dedup — diff against existing files

Before processing, check what's already been transcribed:

1. Determine the output directory: `./podcast-transcripts/<podcast-slug>/`
2. Use Glob to list all existing `.md` files in that directory (excluding `index.md`)
3. For each episode from Step 2, generate its expected filename (`YYYY-MM-DD-slug.md`)
4. Categorize:
   - **New:** no matching file exists → will process
   - **Exists:** file already present → skip
   - **Upgradeable:** file exists with `source: whisper` but `transcript_url` is now available → offer to re-process with better source

Show the user a diff summary:
```
Episode diff:
  New (will process):     3 episodes
  Already transcribed:    2 episodes (skipped)
  Upgradeable (whisper → RSS transcript): 0 episodes

Proceed with 3 new episodes?
```

If all episodes already exist, report "No new episodes to process" and stop.

To check if a file is upgradeable, read the first 5 lines and look for `source: whisper` in the frontmatter.

### Step 3: Process each episode

Process only **new** and **user-confirmed upgradeable** episodes, in **chronological order** (oldest first):

**3a. Obtain transcript:**

1. **If `transcript_url` is present:** fetch it with WebFetch or curl. Parse SRT/VTT into `[HH:MM:SS] text` format (see parsing instructions below). Record source as `rss-transcript`.
2. **If no transcript URL:** run `transcribe <audio_url>`. Record source as `whisper`.

**3b. Render the episode .md file:**

Write the file with this exact structure:

```
---
title: "EP42: Title Here"
podcast: "Podcast Name"
date: 2024-03-15
duration: "01:23:45"
season: 2
episode: 42
explicit: false
source: rss-transcript
audio_url: "https://..."
episode_url: "https://..."
artwork_url: "https://..."
categories:
  - Technology
keywords:
  - keyword1
  - keyword2
guests: []
---

## Show Notes

[RSS description content — convert HTML to Markdown]

## Transcript

[00:00:00] First segment text here.
[00:00:05] Second segment text here.

## Links

- [Link text](URL) — extracted from show notes HTML
```

**Frontmatter rules:**
- Omit fields that are null/empty (don't include `season: null`)
- `source` must be one of: `rss-transcript`, `whisper`
- `date` format: YYYY-MM-DD
- `duration` format: HH:MM:SS
- `guests`: empty array by default; populate if mentioned in show notes

**3c. File naming:** `YYYY-MM-DD-slug.md` where slug is the title lowercased, spaces to hyphens, non-alphanumeric stripped, max 60 chars.

**3d. Output directory:** `./podcast-transcripts/<podcast-slug>/` unless user specifies otherwise.

### Step 4: Generate index.md

After processing, regenerate `index.md` from **all** `.md` files in the output directory (both newly created and previously existing). Read each file's frontmatter to build the table. This ensures the index is always complete and up-to-date.

Create `index.md` in the output directory:

```
---
type: podcast-index
podcast: "Podcast Name"
artist: "Artist Name"
language: zh
categories:
  - Technology
episode_count: 15
date_range:
  from: 2024-01-15
  to: 2024-06-20
total_duration: "18:45:30"
generated: 2026-04-07
sources:
  rss-transcript: 2
  whisper: 13
---

# Podcast Name — Transcript Index

| # | Date | Title | Duration | Source | File |
|---|------|-------|----------|--------|------|
| 1 | 2024-01-15 | Episode Title | 01:23:45 | whisper | [link](./2024-01-15-episode-title.md) |

## Statistics

- Total episodes: 15
- Total duration: 18h 45m 30s
- Transcript sources: 2 RSS, 13 Whisper
- Date range: 2024-01-15 to 2024-06-20
```

**Index frontmatter rules:**
- `total_duration`: sum all episode durations, format as HH:MM:SS
- `generated`: today's date
- `sources`: count per source type

### Step 5: Report completion

Summarize:
- New episodes processed: N
- Skipped (already existed): N
- Upgraded (whisper → RSS): N
- Transcript sources breakdown: N RSS, N Whisper
- Output directory path
- Any failures

## SRT/VTT Parsing Instructions

When fetching an existing transcript via `transcript_url`, convert to `[HH:MM:SS] text` format:

**SRT format:**
```
1
00:00:01,000 --> 00:00:04,500
First subtitle line.

2
00:00:05,000 --> 00:00:08,200
Second subtitle line.
```

Parse: take the start timestamp from each entry, truncate to `HH:MM:SS` (drop milliseconds), pair with the text. Skip numeric sequence lines and blank lines.

**VTT format:**
```
WEBVTT

00:00:01.000 --> 00:00:04.500
First subtitle line.

00:00:05.000 --> 00:00:08.200
Second subtitle line.
```

Parse: same as SRT but skip the `WEBVTT` header line. Timestamps use `.` instead of `,` for milliseconds.

**JSON transcript format:** structure varies; extract `text` and `start`/`startTime` fields, convert seconds to `[HH:MM:SS]`.

## Error Handling

- **Network errors:** Retry once, then skip the episode and note the failure
- **Whisper model download:** Inform the user on first run (model is ~1-3GB), ask to proceed
- **Transcript parse errors:** Fall back to Whisper, report the fallback
- **Empty/unavailable audio:** Skip, note in index
- **Rate limiting:** Pause and retry

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- For local transcription: a machine capable of running faster-whisper (CPU works, GPU is faster)
