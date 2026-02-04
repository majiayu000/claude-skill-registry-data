---
name: transcribe-audio-to-text
description: Transcribe audio files to text using audinota cli
---

# Transcribe Audio to Text

Convert audio files to text using audinota transcription service.

## Usage

```bash
# Use default audio file (output from youtube-video-to-audio skill)
python scripts/transcribe_audio.py

# Specify custom audio file
python scripts/transcribe_audio.py --audio-file-path "/path/to/audio.mp3"
```

## Options

- `--audio-file-path` - Path to audio file to transcribe (default: ~/tmp/download_audio_result.mp3)

## Examples

```bash
# Transcribe default audio file
python scripts/transcribe_audio.py

# Transcribe custom audio file
python scripts/transcribe_audio.py --audio-file-path "~/Music/podcast.mp3"

# Get help
python scripts/transcribe_audio.py -h
```

## Requirements

- Python 3.11+
- audinota installed at `~/Documents/GitHub/audinota-project/.venv/bin/audinota`
- Audio file must exist at specified path

## Integration

This skill works seamlessly with the `youtube-video-to-audio` skill. By default, it transcribes the audio file downloaded by that skill at `~/tmp/download_audio_result.mp3`.
