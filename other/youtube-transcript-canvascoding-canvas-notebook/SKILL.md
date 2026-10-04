---
name: youtube-transcript
description: "Fetch transcripts from YouTube videos for summarization, analysis, or reference. Accepts video ID or full URL. No API key required. Triggers: YouTube transcript, video transcript, get subtitles, what did they say in the video, summarize YouTube, extract video text, caption from video."
allowed-tools: Bash(youtube-transcript:*)
metadata:
  version: "1.0"
  author: canvas-studios
---

# YouTube Transcript

Fetch transcripts from YouTube videos. Works with both auto-generated and manually added captions.

## When to Use

- Summarizing YouTube videos
- Analyzing video content without watching
- Extracting quotes or references from videos
- Any task involving YouTube video content

## Usage

```bash
youtube-transcript <video-id-or-url>
```

Accepts video ID or any YouTube URL format:
```bash
youtube-transcript EBw7gsDPAYQ
youtube-transcript https://www.youtube.com/watch?v=EBw7gsDPAYQ
youtube-transcript https://youtu.be/EBw7gsDPAYQ
```

## Output

Timestamped transcript entries:

```
[0:00] All right. So, I got this UniFi Theta
[0:15] I took the camera out, painted it
[1:23] And here's the final result
```

## Notes

- Requires the video to have captions/transcripts available (auto-generated or manual)
- No API key required
