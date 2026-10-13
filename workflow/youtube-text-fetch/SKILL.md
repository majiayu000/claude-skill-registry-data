---
name: youtube-text-fetch
description: "Fetch transcript/caption text from YouTube videos using youtube-transcript-api. Use when: (1) User wants text from a YouTube video, (2) User provides YouTube URLs and needs transcripts, (3) User says 'fetch youtube text', 'get captions', 'youtube transcript'. Outputs plain text saved to the repo-scoped cclogs dir (resolved via get-logdir.js) as youtube-{VIDEO_ID}.txt."
user-invocable: true
argument-hint: "YouTube URL(s) — space-separated if multiple. Optional flags: --timestamps (include timestamps in output)"
---

# YouTube Text Fetch

Fetch transcript/caption text from YouTube videos.

**Note**: For visual analysis of a YouTube video (extracting frames and reading them
chronologically with vision to produce a timestamped narrative, e.g. debugging a
recording or answering "what happens in this video"), use the `/video-reader` skill
instead. This skill is for quick transcript-only extraction.

## Prerequisites

Requires `youtube-transcript-api` Python package:

```bash
pip3 install youtube-transcript-api
```

If not installed, install it automatically before proceeding.

## Workflow

### 1. Parse Video IDs

Extract video IDs from provided URLs. Supported formats:

- `https://youtu.be/<ID>`
- `https://youtu.be/<ID>?si=...`
- `https://www.youtube.com/watch?v=<ID>`
- `https://youtube.com/watch?v=<ID>&...`

Check if `--timestamps` flag is present (include timestamps in output).

### 2. Fetch Transcripts

For each video ID, run:

**With timestamps** (default when `--timestamps` flag is used, or when writing guide articles):

```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
snippets = YouTubeTranscriptApi().fetch('VIDEO_ID')
for s in snippets:
    minutes = int(s.start // 60)
    seconds = int(s.start % 60)
    print(f'[{minutes:02d}:{seconds:02d}] {s.text}')
"
```

**Plain text** (default):

```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
snippets = YouTubeTranscriptApi().fetch('VIDEO_ID')
for s in snippets:
    print(s.text)
"
```

If the default language fails, try fetching with specific language codes:

```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
snippets = YouTubeTranscriptApi().fetch('VIDEO_ID', languages=['en', 'ja'])
for s in snippets:
    print(s.text)
"
```

### 3. Save Output

Determine the log directory first:

```bash
LOGDIR=$(node $HOME/.claude/scripts/get-logdir.js)
mkdir -p "$LOGDIR"
```

Save each transcript to `$LOGDIR/youtube-<VIDEO_ID>.txt`.

If multiple videos are provided, also create a combined file `$LOGDIR/youtube-combined.txt` with clear separators between each video's transcript.

### 4. Report

Print a summary of what was fetched:

- Video ID
- Language detected
- Approximate word/character count
- Output file path

## Alternative: yt-tools Sub-Package

If the project has the `sub-packages/yt-tools/` sub-package, it provides a more
comprehensive workflow including video download and frame capture:

```bash
cd sub-packages/yt-tools
pnpm download <youtube-url>        # Downloads video + metadata + transcript
pnpm capture:auto <video-id>       # Auto-captures frames at intervals
```

Use yt-tools when you need the full video processing pipeline (download, capture,
transcript). Use this skill (`/youtube-text-fetch`) when you only need the transcript
text.
