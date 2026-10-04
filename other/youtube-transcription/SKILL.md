---
name: youtube-transcript
description: Download YouTube video transcripts when user provides a YouTube URL or asks to download/get/fetch a transcript from YouTube. Also use when user wants to transcribe or get captions/subtitles from a YouTube video.
allowed-tools: Bash,Read,Write
---

# YouTube Transcript Downloader

This skill helps download transcripts (subtitles/captions) from YouTube videos using yt-dlp.

## When to Use This Skill

Activate this skill when the user:
- Provides a YouTube URL and wants the transcript
- Asks to "download transcript from YouTube"
- Wants to "get captions" or "get subtitles" from a video
- Asks to "transcribe a YouTube video"
- Needs text content from a YouTube video

## Available Scripts

This skill includes modular scripts in the `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `check-ytdlp.sh` | Check if yt-dlp is installed, attempt installation if not |
| `download-transcript.sh` | Main workflow: download subtitles with automatic fallback |
| `whisper-transcribe.sh` | Last resort: download audio and transcribe with Whisper |
| `vtt-to-text.py` | Convert VTT subtitle files to plain text with deduplication |

### Script Location

```bash
# Scripts are located at:
SKILL_DIR="$(dirname "$0")"  # When running from skill directory
# Or use absolute path from wrangler installation
```

## Quick Start

### Option 1: Use the Main Download Script

```bash
# Download transcript (tries manual subs, then auto-generated)
./scripts/download-transcript.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Specify output directory
./scripts/download-transcript.sh "https://www.youtube.com/watch?v=VIDEO_ID" ./transcripts
```

### Option 2: Manual Step-by-Step

```bash
# 1. Check/install yt-dlp
./scripts/check-ytdlp.sh --install

# 2. Download transcript
./scripts/download-transcript.sh "YOUTUBE_URL"

# 3. If no subtitles available, use Whisper
./scripts/whisper-transcribe.sh "YOUTUBE_URL"
```

## How It Works

### Priority Order:
1. **Check if yt-dlp is installed** - install if needed
2. **List available subtitles** - see what's actually available
3. **Try manual subtitles first** (`--write-sub`) - highest quality
4. **Fallback to auto-generated** (`--write-auto-sub`) - usually available
5. **Last resort: Whisper transcription** - if no subtitles exist (requires user confirmation)
6. **Confirm the download** and show the user where the file is saved
7. **Automatically convert** VTT to plain text with deduplication

## Script Details

### check-ytdlp.sh

Check if yt-dlp is installed and optionally install it.

```bash
# Just check
./scripts/check-ytdlp.sh

# Check and install if missing
./scripts/check-ytdlp.sh --install
```

**Exit codes:**
- `0` - yt-dlp is available
- `1` - yt-dlp not found and installation not attempted
- `2` - Installation failed

### download-transcript.sh

Main workflow script that handles the complete download process.

```bash
./scripts/download-transcript.sh <youtube_url> [output_dir]
```

**What it does:**
1. Fetches video info (title, ID)
2. Lists available subtitles
3. Tries manual subtitles first
4. Falls back to auto-generated if needed
5. Converts VTT to plain text automatically
6. Cleans up temporary files

**Exit codes:**
- `0` - Success
- `1` - Invalid arguments
- `2` - yt-dlp not found
- `3` - No subtitles available
- `4` - Download failed

### whisper-transcribe.sh

For videos without any subtitles, download audio and transcribe locally.

```bash
./scripts/whisper-transcribe.sh <youtube_url> [output_dir] [--auto-confirm]
```

**What it does:**
1. Shows file size and duration
2. Asks for confirmation before downloading
3. Checks/installs Whisper if needed
4. Downloads audio as MP3
5. Transcribes with Whisper (base model)
6. Converts to plain text
7. Optionally cleans up audio file

**Options:**
- `--auto-confirm` - Skip confirmation prompts (for automation)

**Exit codes:**
- `0` - Success
- `1` - Invalid arguments
- `2` - yt-dlp not found
- `3` - Whisper not found and user declined installation
- `4` - Download failed
- `5` - Transcription failed
- `6` - User cancelled

### vtt-to-text.py

Convert VTT subtitle files to plain text with deduplication.

```bash
# Output to file
python3 ./scripts/vtt-to-text.py input.vtt output.txt

# Output to stdout
python3 ./scripts/vtt-to-text.py input.vtt
```

**Features:**
- Removes VTT headers and timestamps
- Strips HTML-like tags
- Decodes HTML entities
- Removes duplicate lines (common in auto-generated subs)
- Preserves original speaking order

## Manual Commands Reference

If you prefer to run commands manually instead of using the scripts:

### Check yt-dlp Installation

```bash
which yt-dlp || command -v yt-dlp
```

### Install yt-dlp

```bash
# macOS (Homebrew)
brew install yt-dlp

# Linux (apt)
sudo apt update && sudo apt install -y yt-dlp

# Any system (pip)
pip3 install yt-dlp
```

### List Available Subtitles

```bash
yt-dlp --list-subs "YOUTUBE_URL"
```

### Download Manual Subtitles

```bash
yt-dlp --write-sub --sub-langs "en.*" --skip-download --output "transcript" "YOUTUBE_URL"
```

### Download Auto-Generated Subtitles

```bash
yt-dlp --write-auto-sub --sub-langs "en.*" --skip-download --output "transcript" "YOUTUBE_URL"
```

### Get Video Title

```bash
yt-dlp --print "%(title)s" "YOUTUBE_URL"
```

### Download Audio Only (for Whisper)

```bash
yt-dlp -x --audio-format mp3 --output "audio_%(id)s.%(ext)s" "YOUTUBE_URL"
```

### Transcribe with Whisper

```bash
whisper audio.mp3 --model base --output_format vtt
```

## Output Formats

- **VTT format** (`.vtt`): Includes timestamps and formatting, good for video players
- **Plain text** (`.txt`): Just the text content, good for reading or analysis

The scripts automatically convert VTT to plain text and clean up the VTT file.

## Error Handling

### Common Issues and Solutions

**1. yt-dlp not installed**
```bash
./scripts/check-ytdlp.sh --install
```

**2. No subtitles available**
- Try the Whisper transcription option
- Some videos may be private, age-restricted, or geo-blocked

**3. Whisper installation fails**
- May require system dependencies (ffmpeg, rust)
- Check available disk space (models require 1-10GB)
- Try: `pip3 install openai-whisper`

**4. Download interrupted**
- Check internet connection
- Verify sufficient disk space
- Try again with `--no-check-certificate` if SSL issues

**5. Multiple subtitle languages**
- The scripts default to English (`en.*`)
- Modify the `--sub-langs` parameter for other languages

## Best Practices

- Always check what's available before downloading (`--list-subs`)
- Verify success at each step before proceeding
- Ask user before large downloads (audio files, Whisper models)
- Clean up temporary files after processing
- Provide clear feedback about what's happening at each stage
