---
name: youtube-analysis
description: Analyze YouTube video transcripts to extract summaries, key takeaways, and insights. Use when the user mentions YouTube, video transcript, video analysis, provides a YouTube URL, or wants to analyze a .txt file containing a video transcript.
---

# YouTube Video Transcript Analysis

Analyze YouTube video transcripts to generate structured reports with summaries, key takeaways, notable quotes, and action items.

## When to Use

Activate this skill when the user:
- Mentions "YouTube", "video", "transcript", or "video analysis"
- Provides a YouTube URL to analyze
- Wants to analyze a text file containing a video transcript
- Asks for a summary of a video they watched
- Provides a file path to a transcript

## Input Detection

The user can provide either:
1. **YouTube URL** - Contains `youtube.com/watch`, `youtu.be/`, or `youtube.com/shorts/`
2. **File path** - Path to a transcript file (e.g., `inbox/video.txt`)

## Instructions

### Step 0: Identify Input Type

Determine if the user provided a **YouTube URL** or **file path**.

### Step 1A: Fetch Transcript (URL Input)

If the user provided a YouTube URL:

1. Run yt-dlp to download the transcript:
   ```bash
   yt-dlp --write-auto-sub --write-sub --sub-lang en --skip-download --convert-subs srt -o "inbox/%(title)s" "<URL>"
   ```
2. Look for the output file in `inbox/` (format: `<video-title>.en.srt`)
3. If successful, proceed with the transcript file
4. Store the original YouTube URL for the report's Source field

**Error handling:**
- If yt-dlp not found: Tell user "yt-dlp not installed. Install with: pip install yt-dlp"
- If no captions available: Tell user "No English captions found for this video"
- If network error: Tell user "Failed to fetch transcript. Check URL and connection."

### Step 1B: Read Transcript (File Path Input)

If the user provided a file path:
1. Ask the user for the file path if not provided
2. Read the transcript file at the path provided
3. If file not found: Tell user and suggest checking the path

### Step 2: Read Analysis Prompt

Read the analysis prompt from `prompts/yt.md`

### Step 3: Extract Video Title

- From SRT file: Parse the filename (remove `.en.srt` suffix)
- From transcript content: Look for video title in first few lines
- If unclear: Ask user for the title

### Step 4: Generate Analysis

Generate analysis following the prompt structure exactly

### Step 5: Save the Report

Save to `reports/youtube/YYYY-MM-DD_sanitized-title.md` where:
- YYYY-MM-DD is today's date
- sanitized-title is the title in lowercase, spaces replaced with hyphens, special chars removed

### Step 6: Update Activity Log

Update the activity log at `logs/YYYY-MM-DD.md`:
- Create file if it doesn't exist
- Add entry under "## Videos Watched" section
- Format: `- [Title](../reports/youtube/filename.md) - HH:MM`

### Step 7: Confirm to User

Tell user what was saved and where

## Report Format

Include this header in the report:
```markdown
# [Video Title]

**Source**: [YouTube URL or file path]
**Date**: YYYY-MM-DD
**Type**: YouTube Video

---

[Analysis content following prompts/yt.md structure]

---

## My Notes

[Empty space for user notes]
```

## Error Handling

- If yt-dlp not installed: Tell user how to install it
- If no captions available: Inform user and suggest alternatives
- If file not found: Tell user and suggest checking the path
- If file is empty: Inform user and ask if they want to proceed
- If prompts/yt.md missing: Use a basic summary structure

## Related

- Slash command equivalent: `/yt <url-or-filepath>`
- Prompt file: `prompts/yt.md`
- Output location: `reports/youtube/`
- Transcript location: `inbox/` (for downloaded transcripts)
