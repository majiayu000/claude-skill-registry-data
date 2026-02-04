---
name: youtube-summary
description: Summarize YouTube videos. Check if transcript exists at `youtube/{Channel Name}/transcript-{Video Title}.md`. If exists, skip to summarization. If not, download first. Create summary at `youtube/{Channel Name}/summary-{Video Title}.md` with topics and clickable timestamp links.
allowed-tools: Bash,Read,Write
---

# YouTube Video Summarization

## Quick Start

**Check if transcript exists first:**
1. Look for `youtube/{Channel Name}/transcript-{Video Title}.md` located at the root of this project
2. **If exists**: Skip to Step 2 (Create Summary)
3. **If not exists**: Run Step 1 (Download Transcript)

### Step 1: Download Transcript (Only if needed)

```bash
uv run script.py "YOUTUBE_URL"
```

Creates: `youtube/{Channel Name}/transcript-{Video Title}.md` located at the root of this project

### Step 2: Create Summary

1. Read the transcript file
2. Identify main topics with start/end timestamps
3. Create `youtube/{Channel Name}/summary-{Video Title}.md` located at the root of this project

Summary format:
- Executive summary paragraph
- Topics with clickable timestamp links: `https://www.youtube.com/watch?v=VIDEO_ID&t=XXXs`
- Key points for each topic

## Script Details (for reference)

Downloads subtitles (manual or auto-generated), converts to timestamped markdown in 1-minute windows, saves to `youtube/{channel_name}/transcript-{video_title}.md`. UV handles dependencies.

## Output Files

### Transcript File: `transcript-{Video Title}.md`

The transcript file includes:
- Video title and URL at the top
- Full transcript organized into 1-minute time windows
- Each line prefixed with its timestamp (e.g., `[00:45]`)
- Time window headers (e.g., `[00:00 - 01:00]`)

Example structure:
```markdown
# Video Title

**Video URL:** https://youtube.com/...

---

## Full Transcript

### [00:00 - 01:00]

**[00:05]** Introduction to the topic...

**[00:32]** First main point...
Summary Format

Create `summary-{Video Title}.md` with clickable timestamp links (`https://www.youtube.com/watch?v=VIDEO_ID&t=XXXs`)

**Timestamp Conversion**: Convert MM:SS or HH:MM:SS timestamps to seconds for the URL:
- `00:00` → `0s`
- `02:30` → `150s` (2×60 + 30)
- `08:15` → `495s` (8×60 + 15)
- `01:05:30` → `3930s` (1×3600 + 5×60 + 30)

## Error Handling

The script handles common issues:

**1. No subtitles available**
- Script tries manual subtitles first, then auto-generated
- If both fail, exits with error message

**2. Invalid or private video**
- Check if URL is correct format: `https://www.youtube.com/watch?v=VIDEO_ID`
- Some videos may be private, age-restricted, or geo-blocked
- Script will show the specific error from yt-dlp

**3. Download interrupted or failed**
- Check internet connection
- Verify sufficient disk space

## Notes

- The script automatically downloads the first available subtitle language (usually English)
- YouTube's auto-generated VTT files contain duplicate lines due to progressive captions - the script deduplicates while preserving speaking order
- Timestamps are preserved and formatted as clickable references
- Output is organized by channel in the `youtube/` directory
- Filenames are sanitized for filesystem compatibility
- Temporary VTT files are automatically cleaned up
- **The script creates only the transcript file. After reviewing the transcript, create the summary file separately with topic analysis and timestamps**`MM:SS` → seconds (e.g., `02:30` → `150s`, `08:15` → `495s`)