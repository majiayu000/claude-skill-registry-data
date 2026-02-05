---
name: mindwork-transcribe
description: Transcribe therapy session recordings to formatted text. Converts audio to clean, speaker-labeled transcripts (Me/Therapist format) with grammar correction and English translation. Use when processing therapy recordings, session audio, or any two-person conversation recording.
---

# Therapy Session Transcriber

Part of the **mindwork** suite. Converts therapy session recordings into clean, formatted transcripts.

## What It Does

1. **Chunks** large audio files at natural silence points (sentence boundaries)
2. **Transcribes** using OpenAI Whisper API
3. **Formats** as two-person conversation with **Me:** / **Therapist:** labels
4. **Corrects** grammar and transcription errors
5. **Translates** to English (for non-English sessions)

## Prerequisites

- Docker installed and running
- `OPENAI_API_KEY` environment variable set
- The `mindwork-transcribe` Docker image built (see Setup)

## Setup (One-Time)

Build the transcription Docker image from the plugin's transcribe directory:

```bash
# Find the mindwork plugin location and build the image
docker build -t mindwork-transcribe ~/src/mindwork/transcribe
```

Or if installed as a plugin, find the plugin path first:
```bash
# The transcribe tool is in the 'transcribe/' directory of this plugin
docker build -t mindwork-transcribe /path/to/mindwork/transcribe
```

## Usage

### Full Therapy Session Processing (Recommended)

Transcribe, format as conversation, and translate to English:

```bash
docker run --rm \
  -e OPENAI_API_KEY \
  -v $(pwd):/data \
  mindwork-transcribe /data/session.m4a --format-conversation --output /data/transcript.txt
```

### Raw Transcription Only

Just transcribe without formatting or translation:

```bash
docker run --rm \
  -e OPENAI_API_KEY \
  -v $(pwd):/data \
  mindwork-transcribe /data/session.m4a --output /data/transcript.txt
```

### With Speaker Diarization

For automatic speaker detection (alternative to --format-conversation):

```bash
docker run --rm \
  -e OPENAI_API_KEY \
  -v $(pwd):/data \
  mindwork-transcribe /data/session.m4a --diarize --output /data/transcript.txt
```

### Only Chunk (No Transcription)

Split a large file into chunks for later processing:

```bash
docker run --rm \
  -v $(pwd):/data \
  mindwork-transcribe /data/session.m4a --no-transcribe --keep-chunks
```

### Process Existing Chunks

Resume from previously created chunks:

```bash
docker run --rm \
  -e OPENAI_API_KEY \
  -v $(pwd):/data \
  mindwork-transcribe /data/chunks/ --format-conversation --output /data/transcript.txt
```

## Options Reference

| Option | Description |
|--------|-------------|
| `--output FILE` | Save transcript to file (default: stdout) |
| `--format-conversation` | Format as Me/Therapist dialogue + translate to English |
| `--diarize` | Auto-detect speakers (uses gpt-4o-transcribe-diarize) |
| `--no-transcribe` | Only chunk, skip transcription |
| `--keep-chunks` | Preserve chunk files after processing |
| `--model MODEL` | `whisper-1` (default, fast) or `gpt-4o-transcribe` (better accuracy) |

## Supported Audio Formats

mp3, mp4, m4a, wav, webm, ogg, flac

## Configuration (mindwork.yaml)

If a `mindwork.yaml` config file exists, use it to determine output paths:

```yaml
vault: ~/Therapy

sources:
  recordings:
    paths: [recordings/]

outputs:
  transcriptions: transcriptions/
```

**Config locations** (checked in order):
1. `./mindwork.yaml` (current directory)
2. `~/.config/mindwork/config.yaml`
3. `~/.mindwork.yaml`

**Default behavior** (no config):
- Save to current directory or user-specified `--output` path

**With config**:
- Save to `{vault}/{outputs.transcriptions}/{date}-{filename}.md`
- Example: `~/Therapy/transcriptions/2024-01-15-session-001.md`

See `config/mindwork.example.yaml` for full configuration options.

## Output Format

With `--format-conversation`, output looks like:

```
**Me:** I've been feeling anxious about work lately. The deadlines keep piling up.

**Therapist:** That sounds overwhelming. Can you tell me more about what specifically triggers that anxiety?

**Me:** It's mostly when I have multiple projects due at the same time...
```

## Cost Estimate

OpenAI Whisper API: ~$0.006/minute of audio
GPT-4o for formatting/translation: ~$0.01-0.02 per session (varies by length)

A typical 50-minute session costs approximately $0.30-0.50 total.

## Troubleshooting

**"Docker image not found"**
Build the image from the plugin's transcribe directory:
```bash
docker build -t mindwork-transcribe /path/to/mindwork/transcribe
```

**"OPENAI_API_KEY not set"**
```bash
export OPENAI_API_KEY="sk-..."
```

**"File not found"**
Ensure you're in the directory containing your audio file, or use absolute paths.

**Transcription quality issues**
Try `--model gpt-4o-transcribe` for better accuracy (same price as whisper-1).
