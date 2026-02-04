---
name: whisper-transcribe
description: |
  Transcribes audio and video files to text using OpenAI's Whisper CLI with contextual grounding.
  Converts audio/video to text, transcribes recordings, and creates transcripts from media files.
  Use when asked to "whisper transcribe", "transcribe audio", "convert recording to text", or
  "speech to text". Uses markdown files in the same directory as context to improve transcription
  accuracy for technical terms, proper nouns, and domain-specific vocabulary.
version: 1.0.0
category: media-processing
triggers:
  - whisper
  - transcribe
  - transcription
  - audio to text
  - video to text
  - speech to text
  - convert recording
  - meeting transcript
  - .mp3
  - .wav
  - .m4a
  - .mp4
  - .webm
author: Claude Code
license: MIT
tags:
  - whisper
  - transcription
  - audio
  - video
  - speech-to-text
  - context-grounding
---

# Whisper Transcribe Skill

Transcribe audio and video files to text using OpenAI's Whisper with contextual grounding from markdown files.

## Purpose

Intelligent audio/video transcription that:
1. Converts media files to accurate text transcripts
2. Uses markdown context files to correct technical terms, names, and jargon
3. Handles various audio/video formats (mp3, wav, m4a, mp4, webm, etc.)

## When to Use

- User asks to transcribe an audio or video file
- User wants to convert a recording to text
- User mentions "whisper" in context of transcription
- User needs meeting notes or interview transcripts
- User has media files with domain-specific terminology

## Installation

### macOS (Recommended for MacBook Pro)

```bash
# Install via Homebrew (recommended)
brew install ffmpeg openai-whisper

# Verify installation
whisper --version
```

### Linux/pip Installation

```bash
# Install ffmpeg first
sudo apt install ffmpeg  # Debian/Ubuntu
# or: sudo dnf install ffmpeg  # Fedora

# Install Whisper
pip install openai-whisper
```

### Verify Installation

```bash
whisper --version
ffmpeg -version
```

## Transcription Workflow

### Step 1: Identify Media File and Context

1. Locate the audio/video file to transcribe
2. Check for markdown files in the same directory (context files)
3. If no context files exist, optionally create one using `assets/context-template.md`

### Step 2: Run Whisper Transcription

Basic transcription:
```bash
whisper "/path/to/audio.mp3" --output_dir "/path/to/output"
```

With model selection (trade-off: speed vs accuracy):
```bash
# Fast (less accurate)
whisper "audio.mp3" --model tiny

# Balanced (recommended)
whisper "audio.mp3" --model base

# High quality
whisper "audio.mp3" --model small

# Best quality (slower, requires more RAM)
whisper "audio.mp3" --model medium
whisper "audio.mp3" --model large
```

With language specification:
```bash
whisper "audio.mp3" --language en
```

Output format options:
```bash
whisper "audio.mp3" --output_format txt    # Plain text
whisper "audio.mp3" --output_format srt    # Subtitles
whisper "audio.mp3" --output_format vtt    # Web subtitles
whisper "audio.mp3" --output_format json   # Detailed JSON
whisper "audio.mp3" --output_format all    # All formats
```

### Step 3: Apply Context Grounding

Use the `scripts/transcribe_with_context.py` script for automated grounding, or manually apply corrections:

```bash
# Automated approach (recommended)
python scripts/transcribe_with_context.py /path/to/audio.mp3
```

For manual grounding:
1. Read the transcript output
2. Read all `.md` files in the media file's directory
3. Extract terminology, names, and technical terms from context files
4. Search transcript for likely misrecognitions
5. Apply corrections based on context

**Common corrections:**
- "cooler net ease" -> "Kubernetes"
- "sequel" -> "SQL"
- "post gress" -> "Postgres"
- Names: Match phonetic variations to names in context files

### Step 4: Save Corrected Transcript

Save the grounded transcript with a clear filename:
```
original_filename_transcript.txt
original_filename_transcript.md
```

## Context Files

Context files are markdown files in the same directory as the media file. They provide grounding information to improve transcription accuracy.

### What to Include in Context Files

- **People**: Names of speakers, team members, interviewees
- **Technical Terms**: Domain-specific vocabulary, product names
- **Acronyms**: Abbreviations and their expansions
- **Organizations**: Company names, department names
- **Projects**: Project codenames, feature names

### Context File Example

See `assets/context-template.md` for a complete template.

```markdown
# Meeting Context

## Speakers
- Richard Hightower (host)
- Jane Smith (engineering lead)

## Technical Terms
- Kubernetes (container orchestration)
- FastAPI (Python web framework)
- AlloyDB (Google Cloud database)

## Acronyms
- CI/CD - Continuous Integration/Continuous Deployment
- PR - Pull Request
```

## Model Selection Guide

Use `base` for general use, `medium` for important recordings. See `references/whisper-options.md` for full model comparison and all available options.

**Quick reference:** `tiny` (fastest) < `base` (balanced) < `small` (better) < `medium` (high) < `large` (best accuracy)

For MacBook Pro with Apple Silicon: `small` or `medium` models recommended for best speed/accuracy balance.

## Troubleshooting

### "whisper: command not found"
```bash
# macOS
brew install openai-whisper

# Linux
pip install openai-whisper
export PATH="$HOME/.local/bin:$PATH"
```

### "ffmpeg not found"
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### Out of memory errors
Use a smaller model:
```bash
whisper "audio.mp3" --model tiny
```

### Slow transcription
- Use `tiny` or `base` model for faster results
- Ensure correct architecture is being used (Apple Silicon vs Intel)

## Resources

### scripts/

The `scripts/transcribe_with_context.py` script automates the full workflow:
- Finds context files automatically
- Runs Whisper transcription
- Applies context-based corrections
- Saves the final transcript

Usage:
```bash
python scripts/transcribe_with_context.py /path/to/audio.mp3
```

### references/

See `references/whisper-options.md` for complete CLI reference and advanced options.

### assets/

The `assets/context-template.md` provides a template for creating context files to improve transcription accuracy.
