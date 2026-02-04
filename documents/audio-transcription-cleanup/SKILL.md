---
name: audio-transcription-cleanup
description: Transform messy voice transcription text into well-formatted, human-readable documents while preserving original meaning
---

# Audio Transcription Cleanup

Clean up raw audio transcriptions by removing filler words, fixing errors, and adding proper structure.

## Usage

Use the `audio_transcript_cleanup.py` script to process transcript files:

```bash
# Use default output location (~/tmp/cleaned_transcript.md - allows overwrite)
python scripts/audio_transcript_cleanup.py --transcript-file /path/to/transcript.txt

# Specify custom output location (cannot overwrite existing files)
python scripts/audio_transcript_cleanup.py --transcript-file /path/to/transcript.txt --output /path/to/output.md
```

## What It Does

The script automatically:
- Removes verbal artifacts (um, uh, like, you know, 呃, 啊, 那个, etc.)
- Fixes spelling and grammar errors
- Adds semantic paragraph breaks and section headings
- Converts spoken fragments into complete sentences
- Preserves all original information (no summarization)
- Auto-detects language and maintains natural expression

## Options

- `--transcript-file` (required) - Path to the transcript file to clean up
- `--output` (optional) - Custom output path (default: `~/tmp/cleaned_transcript.md`)

## Output Behavior

- **Default location**: `~/tmp/cleaned_transcript.md` - Allows overwrite
- **Custom location**: Cannot overwrite existing files (raises error if file exists)

## Language Support

Auto-detects and works with:
- English
- Chinese (Mandarin, Cantonese)
- Mixed language content
- Multi-speaker transcriptions

## Requirements

- Python 3.11+
- Claude CLI must be installed and accessible
- Transcript file must exist at specified path
