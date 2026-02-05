---
name: podcast-analysis
description: Analyze podcast episodes from transcripts, audio URLs, or audio files. Use when the user mentions podcast, episode, audio transcript, interview, or provides a podcast file/URL.
---

# Podcast Episode Analysis

Analyze podcast episodes to generate structured reports with summaries, guest insights, key quotes, and actionable takeaways. Supports transcript files, audio URLs (YouTube, podcast platforms), and audio files.

## When to Use

Activate this skill when the user:
- Mentions "podcast", "episode", "audio", "interview"
- Provides a transcript file path (.txt, .srt, .md)
- Provides an audio file path (.mp3, .m4a, .wav)
- Provides a podcast URL (YouTube, Apple Podcasts, Spotify, etc.)
- Asks to summarize a podcast they listened to
- Wants to extract insights from an interview
- Mentions a specific podcast show or episode

## Supported Inputs

- **Transcript file**: `.txt`, `.srt`, `.md` file with episode transcript
- **Audio URL**: Direct audio link or podcast platform URL (will be transcribed)
- **Audio file**: `.mp3`, `.m4a`, `.wav` file (will be transcribed)

## Instructions

1. **Determine input type**:
   - If file path with text extension (.txt, .srt, .md): Read transcript directly
   - If audio file path (.mp3, .m4a, .wav, etc.): Transcribe with Whisper
   - If URL provided: Download and transcribe audio with Whisper
   - Ask user for input if not provided

2. **For audio transcription** (URLs or audio files):
   - Use yt-dlp to download audio (supports many podcast platforms)
   - Transcribe using OpenAI Whisper API (requires OPENAI_API_KEY in .env)
   - Fallback to local Whisper if available
   - Note: Transcription may take a few minutes for long episodes

3. **For transcript files**:
   - Verify file exists and is readable
   - Read the transcript content
   - Parse SRT format if applicable

4. If content retrieval fails:
   - Inform user about the issue
   - For audio: Check OPENAI_API_KEY is set
   - For files: Suggest checking file path
   - Stop here

5. **Read the analysis prompt** from `prompts/podcast.md`
6. **Extract episode metadata**:
   - Podcast name
   - Episode title
   - Host(s) and guest(s)
   - Duration if mentioned
7. **Generate analysis** following the prompt structure exactly
8. **Create output directory** `reports/podcasts/` if needed
9. **Save the report** to `reports/podcasts/YYYY-MM-DD_sanitized-title.md`
10. **Update the activity log** at `logs/YYYY-MM-DD.md`:
    - Add entry under "## Podcasts Listened" section
    - Format: `- [Title](../reports/podcasts/filename.md) - HH:MM`
11. **Confirm to user** what was saved

## Report Format

```markdown
# [Episode Title]

**Podcast**: [Show Name]
**Host(s)**: [Names]
**Guest(s)**: [Names if any]
**Source**: [file path or URL]
**Date**: YYYY-MM-DD
**Type**: Podcast Episode

---

[Analysis content following prompts/podcast.md structure]

---

## My Notes

[Empty space for user notes]
```

## Error Handling

- If file doesn't exist: Ask for correct path
- If transcript too short: Note but analyze
- If no speaker identification: Best effort analysis
- If prompts/podcast.md missing: Use prompts/default.md
- If audio download fails: Check yt-dlp is installed (`pip install yt-dlp`)
- If transcription fails: Check OPENAI_API_KEY is configured in .env
- If audio file too large: OpenAI API limit is 25MB, suggest splitting

## Requirements for Audio

- yt-dlp for downloading audio (`pip install yt-dlp`)
- OpenAI API key for transcription (set OPENAI_API_KEY in web/backend/.env)
- Alternatively: Local Whisper installation (`pip install openai-whisper`)

## Related

- Slash command: `/podcast <filepath-or-url>`
- Prompt file: `prompts/podcast.md`
- Output: `reports/podcasts/`
- Transcription service: `web/backend/services/transcription.py`
