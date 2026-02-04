---
name: youtube-chapters
description: Generate chapter summaries with timestamps for YouTube videos using AI. Use when asked to create chapters, summarize video sections, or generate video outline.
---

# YouTube Chapter Generator

Use the `ai-chapters` CLI tool to generate chapter summaries for YouTube videos.

## Usage

```bash
ai-chapters "https://youtu.be/VIDEO_ID"
```

## Requirements

- `GEMINI_API_KEY` environment variable must be set
- The `hamel_tools` package must be installed: `pip install hamel_tools`

## Output

Returns chapter titles with timestamps suitable for YouTube descriptions.
