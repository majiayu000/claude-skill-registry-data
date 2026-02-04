---
name: Transcribe Vaam Video with Gemini
description: Transcribe Vaam videos using Google Gemini AI. Takes a Vaam share URL, downloads the video, and returns a full text transcription. Supports any language without translation.
version: 1.0.0
author: Claude Assistant
tags: [vaam, transcription, gemini, video]
---

**IMPORTANT - Path Resolution:**
This skill can be installed in different locations. Before executing any commands, determine the skill directory based on where you loaded this SKILL.md file, and use that path in all commands below. Replace `$SKILL_DIR` with the actual discovered path.

# Transcribe Vaam Video with Gemini

Transcribe Vaam video recordings using Google Gemini AI. Provide a Vaam share URL and get back a complete text transcription.

## Setup (First Time Only)

```bash
cd $SKILL_DIR && bun install
```

This installs the required dependencies (Google Generative AI SDK).

## Requirements

**Environment Variable:**
- `GEMINI_API_KEY` - Required. Your Google Gemini API key.
  - Get one at: https://aistudio.google.com/apikey

## Usage

```bash
cd $SKILL_DIR && bun lib/transcribe-with-gemini.ts <vaam-url>
```

### Options

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help message |
| `--verbose`, `-v` | Enable progress logging (only use for debugging) |

### Examples

```bash
# Basic transcription
cd $SKILL_DIR && bun lib/transcribe-with-gemini.ts https://app.vaam.io/share/abc123

# With verbose output (shows progress)
cd $SKILL_DIR && bun lib/transcribe-with-gemini.ts --verbose https://app.vaam.io/share/abc123
```

## Input

- **Vaam Share URL**: Must be in format `https://app.vaam.io/share/[id]`
  - The ID can contain letters, numbers, and hyphens

## Output

**On Success:**
- Plain text transcription to stdout
- Exit code: 0

**On Error:**
- JSON error object to stdout with structure:
  ```json
  {
    "success": false,
    "error": {
      "code": "ERROR_CODE",
      "message": "Human-readable message",
      "details": "Technical details",
      "suggestion": "How to fix it"
    }
  }
  ```
- Exit code: 1 (validation errors) or 2 (runtime errors)

## Error Codes

| Code | Description | Exit Code |
|------|-------------|-----------|
| `MISSING_ARGUMENT` | No URL provided | 1 |
| `INVALID_URL` | URL doesn't match expected format | 1 |
| `MISSING_API_KEY` | GEMINI_API_KEY not set | 1 |
| `VIDEO_EXTRACTION_FAILED` | Couldn't get video from Vaam | 2 |
| `VIDEO_DOWNLOAD_FAILED` | Couldn't download video file | 2 |
| `TRANSCRIPTION_FAILED` | Gemini API error | 2 |

## How It Works

1. Parses the Vaam share URL to extract the capture ID
2. Fetches the video URL from Vaam's API
3. Downloads the video to a temporary file
4. Sends the video to Gemini for transcription
5. Returns the transcription text
6. Cleans up temporary files

## Notes

- Videos are transcribed in their original language (no automatic translation)
- Includes spoken content and important visual information shown on screen
- Timestamps are not included in the transcription
- Temporary files are automatically cleaned up after processing
- Gemini supports videos up to 2GB
