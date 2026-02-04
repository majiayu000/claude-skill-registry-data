---
name: transcription-helper
description: Guides users through video transcription workflow from input to output. Transcribes local video files and YouTube URLs using gpt-4o-transcribe. Use when users want to transcribe videos, audio files, YouTube content, or need help with media-to-text conversion.
---

# Transcription Helper

## Entry Points

This skill can be invoked at different stages:

| Entry Point | When | Start At |
|-------------|------|----------|
| New transcription | User wants to transcribe video | Phase 1 |
| Job completed | Background transcription job finished | Phase 4 |
| Resume workflow | User returns to a saved transcript | Phase 4 |

**Job Completion Flow**: When a transcription job completes, the system automatically
requests Phase 4 to present results and options to the user.

## Workflow Phases

### Phase 1: Gathering Input
1. Greet briefly (mention you use gpt-4o-transcribe for high accuracy)
2. Ask for:
   - Video source (local file path or YouTube URL)
   - Language (optional — e.g., 'en', 'es', 'zh' — auto-detects if not specified)
   - Domain vocabulary (optional — technical terms, proper nouns to improve accuracy)
3. Keep it concise. Don't overwhelm with detailed explanations.

### Phase 2: User Confirmation
ONLY proceed after explicit confirmation ("yes", "proceed", "confirm", "go ahead"):
- If changes requested → return to Phase 1
- If confirmed → proceed to Phase 3

### Phase 3: Transcription
1. Use `transcribe_video` with:
   - `video_source`: File path or YouTube URL
   - `language`: ISO 639-1 code if known (e.g., 'en', 'es', 'zh')
   - `temperature`: 0.0 for consistent results
   - `prompt`: Domain vocabulary if provided
2. The tool creates a **background job** and returns immediately with a job ID
3. Tell user to monitor progress in the Jobs panel
4. **DO NOT call `save_transcript`** — the job automatically saves the transcript when complete
   - **YouTube videos**: Title is auto-extracted from yt-dlp for evidence linking in KG
   - **Local files**: No title is extracted (title will be `None`)
   - The transcript is registered with a unique ID automatically

**IMPORTANT**: When the job completes, the system triggers Phase 4 directly.
The transcript is already saved — proceed to show results, do NOT call `save_transcript` again.

### Phase 4: Results & Follow-up
After successful transcription:
1. Report completion and share transcript ID
2. Show preview (~200 characters)
3. Share metadata (source type, length, splitting info)
4. Present 5 options:

| Option | Description |
|--------|-------------|
| 1. Summarize | Create concise summary with key points |
| 2. Extract Key Points | List main topics and actionable items |
| 3. Show Full | Display complete transcription |
| 4. Save Derived Content | Save summary/notes using `content-saver` skill |
| 5. Build Knowledge Graph | Extract entities and relationships (recommended for rich content) |

Ask: "What would you like me to do with this transcription? Choose 1-5, or describe something else."

**Option 4 Flow:** When user selects "Save Derived Content":
1. First generate the content to save (summary, notes, key points)
2. Invoke `content-saver` skill for format selection
3. The skill handles format templates, filename suggestions, and file saving

## Error Recovery

| Error Type | Troubleshooting |
|------------|-----------------|
| YouTube errors | Check URL validity, video availability, age restrictions |
| File errors | Verify path exists and is valid video format |
| FFmpeg errors | Ensure FFmpeg is installed |
| API errors | Check OPENAI_API_KEY is set correctly |
| Timeout errors | Video may be too long; suggest splitting |
