---
name: youtube-transcribe
description: Download YouTube video transcripts with timestamps. Use when asked to transcribe a YouTube video, get transcript, or extract text from a video URL.
---

# YouTube Transcript Downloader

Use the `ai-transcribe` CLI tool to download transcripts from YouTube videos.

## Usage

```bash
ai-transcribe "https://youtu.be/VIDEO_ID"
ai-transcribe "https://youtu.be/VIDEO_ID" --seconds  # Use seconds for timestamps
ai-transcribe "https://youtu.be/VIDEO_ID" > transcript.txt  # Save to file
```

## Requirements

- The `hamel_tools` package must be installed: `pip install hamel_tools`

## Output

Returns transcript text with timestamps in HH:MM:SS format (default) or seconds with `--seconds` flag.
