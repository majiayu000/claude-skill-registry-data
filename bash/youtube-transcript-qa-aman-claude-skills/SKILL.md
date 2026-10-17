---
name: youtube-transcript
description: Fetch transcripts from YouTube videos. Use when user says "get transcript", "fetch transcript", "YouTube transcript", "pull captions", "what does this video say", or pastes a YouTube URL and wants the text content extracted. Also use when user wants to research or summarize a YouTube video.
---

# YouTube Transcript Extractor

Fetch and return transcripts from YouTube videos using the bundled Python script.

## When to Activate

- User pastes a YouTube URL and wants the transcript
- User asks to "get the transcript" or "fetch captions" for a video
- User wants to research, summarize, or extract learnings from a YouTube video
- User provides multiple YouTube URLs for batch transcript extraction

## How It Works

### Step 1: Extract the transcript

Run the script with the video URL or ID:

```bash
uv run .claude/skills/youtube-transcript/scripts/get_transcript.py "VIDEO_URL_OR_ID"
```

For timestamped output:

```bash
uv run .claude/skills/youtube-transcript/scripts/get_transcript.py "VIDEO_URL_OR_ID" --timestamps
```

### Step 2: Handle the output

**Supported URL formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- Raw 11-character video ID

**Output rules:**
- Never modify the returned transcript text. Present it exactly as returned.
- When timestamps are not used, arrange the raw text into coherent paragraphs by topic for readability.
- When timestamps are used, keep the `[MM:SS]` or `[HH:MM:SS]` format as-is.

### Step 3: Save if requested

If the user asks to save the transcript:
- Default filename: `{video_id}-transcript.txt`
- Save to the location the user specifies, or to the current working directory

## Multiple Videos

When given multiple URLs, run the script for each video sequentially. Present each transcript with a clear heading identifying the video.

## Limitations

- Requires the video to have captions enabled (manual or auto-generated)
- Will not work on videos with captions disabled
- Auto-generated captions may contain transcription errors - flag this to the user
- Requires Python 3.10+ and `uv` installed locally
