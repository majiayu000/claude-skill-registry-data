---
name: youtube-video-to-audio
description: Download YouTube videos as audio files using yt-dlp
---

# YouTube Video to Audio

Extract and download audio from YouTube videos.

## Usage

```bash
python scripts/download_audio.py --video-url "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Options

- `--video-url` (required) - YouTube video URL to download
- `--quality` - Quality selector (default: "bestaudio[abr<=64]/worstaudio")
- `--audio-format` - Output format: mp3, aac, wav (default: mp3)
- `--bitrate` - Audio bitrate: 64K, 128K, 192K, 320K (default: 64K)
- `--output` - Custom output path (default: ~/tmp/download_audio_result.mp3)

## Examples

```bash
# Basic usage (default: 64K bitrate MP3 to ~/tmp/download_audio_result.mp3)
python scripts/download_audio.py --video-url "https://www.youtube.com/watch?v=d6rZtgHcbWA"

# High quality with custom bitrate
python scripts/download_audio.py --video-url "https://youtu.be/xyz" --quality "bestaudio" --bitrate "128K"

# Custom output location
python scripts/download_audio.py --video-url "https://youtu.be/xyz" --output "/path/to/output.mp3"
```

## Requirements

- Python 3.11+
- ffmpeg installed at `~/ffmpeg`
- yt-dlp (auto-downloaded on first run)
