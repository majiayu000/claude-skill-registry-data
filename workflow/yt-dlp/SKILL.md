---
name: yt-dlp
description: Download audio and video from YouTube and 1000+ other platforms using yt-dlp.
---

# yt-dlp Skill

## Purpose

This skill provides a clean interface to yt-dlp for downloading audio and video content from YouTube and other platforms. It's designed to be used by AI agents and automation systems, with a focus on reliability, clear error handling, and consistent output.

## Usage

The skill exposes a single command on the command line:

```bash
yt-dlp [OPTIONS] <URL>
```

Where `<URL>` is a YouTube, Vimeo, or other supported platform URL.

## Features

- Downloads video/audio from YouTube, Vimeo, and 1000+ other sites
- Extracts audio only (MP3, AAC, etc.)
- Downloads playlists and channels
- Uses a configuration file for defaults
- Embeds metadata and thumbnails
- Supports cookies and proxies
- Provides clear, human-readable output

## Command Line Options

The skill supports all yt-dlp options. The most commonly used options are:

- `-x` or `--extract-audio` - Extract audio from video
- `--audio-format <format>` - Audio format (mp3, aac, wav, best)
- `-f <format>` - Select format (e.g., "bv*+ba" for best video/audio)
- `-F` - List all available formats
- `--embed-metadata` - Embed video metadata
- `--embed-thumbnail` - Embed video thumbnail
- `--recode-video <format>` - Re-encode video (e.g., mp4)
- `-o <template>` - Custom output template (e.g., "%(title)s.%(ext)s")
- `-a <file>` - Download URLs from file
- `--download-archive <file>` - Skip already downloaded videos
- `--no-overwrites` - Don't overwrite existing files
- `--no-cache-dir` - Disable caching
- `--cookies <file>` - Use cookies from file
- `--cookies-from-browser <browser>` - Extract cookies from browser (chrome, firefox, etc.)

## Configuration File

The skill uses the standard yt-dlp configuration file located at `$HOME/.config/yt-dlp/config` (on Linux/Mac) or `%APPDATA%\yt-dlp\config` (on Windows).

Example configuration file:

```
--extract-audio
--audio-format mp3
--audio-quality 0
--embed-metadata
--embed-thumbnail
--no-cache-dir
-o "%(uploader)s - %(title)s.%(ext)s"
--download-archive /home/user/youtube-archive/archive.txt
```

This configuration will:
- Always extract audio
- Convert to MP3 at highest quality
- Embed metadata and thumbnail
- Disable caching
- Save files with uploader name and title
- Record downloads in an archive file to avoid duplicates

## Output

The skill returns:
- Standard output with clear progress info
- Exit code 0 on success
- Exit code 1 on user error or invalid URL
- Exit code 2 on network/downloading error

The downloaded file is saved to the current working directory unless otherwise specified with `-o`.

## Error Handling

- Fails fast with descriptive messages
- Never silently swallows errors
- Returns specific exit codes to indicate error type
- Includes URLs and context in error messages

## Best Practices for Agents

1. Always use `--download-archive` to avoid duplicate downloads
2. Use `--no-cache-dir` to ensure consistent behavior across agent runs
3. For audio-only needs, use `-x --audio-format mp3` consistently
4. Use `--embed-metadata --embed-thumbnail` to create self-contained media files
5. When processing URLs from files, use `-a` instead of looping individually
6. Always check exit codes before proceeding with downstream processing

## Example Usage

```bash
# Download audio as MP3
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=example"

# Download best quality video and merge with audio
yt-dlp -f "bv*+ba" "https://www.youtube.com/watch?v=example"

# Download playlist properly
yt-dlp --download-archive archive.txt "https://www.youtube.com/playlist?list=example"

# Extract cookies from Chrome and download
yt-dlp --cookies-from-browser chrome "https://www.youtube.com/watch?v=example"

# Download from list of URLs
yt-dlp -a urls.txt
```

## Skill Implementation

This is a simple wrapper around the yt-dlp command-line tool. The skill does not modify yt-dlp behavior but provides:
- Clear documentation
- Consistent interface
- Proper error handling
- Standardized configuration

The tool is intended to be more reliable and predictable when used by agents compared to direct shell execution.