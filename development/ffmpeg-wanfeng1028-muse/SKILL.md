---
name: ffmpeg
version: 1.0.0
description: Expert guide for FFmpeg video/audio processing, conversion, streaming, and filtering. Use when working with video, audio, multimedia files, transcoding, format conversion, or when the user mentions ffmpeg, media processing, video conversion, audio conversion, streaming, or codecs.
---

# FFmpeg Expert

Expert guide for FFmpeg command-line tool for video/audio processing, transcoding, streaming, and filtering.

## Quick Start

Basic format conversion:
```bash
ffmpeg -i input.mp4 output.avi
```

Convert video with specific codec:
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

Extract audio from video:
```bash
ffmpeg -i input.mp4 -vn -acodec copy output.aac
```

## Instructions

### Step 1: Understand the User's Goal

First, clarify what the user wants to do:

- **Format conversion**: Change container format (e.g., MP4 to MKV, AVI to MP4)
- **Transcoding**: Re-encode video/audio with different codecs
- **Stream extraction**: Extract video, audio, or subtitle streams
- **Stream mapping**: Select specific streams from input
- **Filtering**: Apply video/audio filters (scale, crop, overlay, etc.)
- **Streaming**: Process live streams or network protocols
- **Screen recording**: Capture desktop or application windows
- **GIF creation**: Convert video to GIF or create from images

### Step 2: Analyze Input Files

Use `ffprobe` to inspect media files:
```bash
ffprobe -v error -show_format -show_streams input.mp4
```

Key information to gather:
- Container format (MP4, MKV, AVI, etc.)
- Video codec (H.264, H.265, VP9, etc.)
- Audio codec (AAC, MP3, Opus, etc.)
- Resolution, frame rate, bitrate
- Duration
- Number and type of streams

### Step 3: Build the Command

FFmpeg follows this syntax:
```bash
ffmpeg [global_options] {[input_file_options] -i input_url} ... {[output_file_options] output_url} ...
```

#### Input Options (placed before -i)
- `-ss position`: Seek to position
- `-t duration`: Limit input duration
- `-r fps`: Set frame rate (input)

#### Output Options (placed before output url)
- `-c[:stream_specifier] codec`: Set codec (use `copy` for streamcopy)
- `-b[:stream_specifier] bitrate`: Set bitrate
- `-s size`: Set frame size (WxH)
- `-r fps`: Set frame rate (output)
- `-vf filtergraph`: Video filter
- `-af filtergraph`: Audio filter
- `-map input_file_id[:stream_specifier]`: Map streams
- `-an / -vn / -sn`: Disable audio/video/subtitle

### Step 4: Handle Common Operations

#### Format Conversion (Streamcopy)
Fast, no quality loss:
```bash
ffmpeg -i input.mp4 -c copy output.mkv
```

#### Video Transcoding
```bash
# CRF-based quality (recommended)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac output.mp4

# Bitrate-based
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -maxrate 2M -bufsize 4M -c:a aac output.mp4
```

#### Resolution Scaling
```bash
# Scale to specific size
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4

# Scale maintaining aspect ratio
ffmpeg -i input.mp4 -vf scale=-1:720 output.mp4  # Height 720, auto width
ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4  # Width 1280, auto height
```

#### Extract Streams
```bash
# Extract audio
ffmpeg -i input.mp4 -vn -acodec copy audio.aac

# Extract video
ffmpeg -i input.mp4 -an -vcodec copy video.h264

# Extract subtitle
ffmpeg -i input.mkv -map 0:s:0 subs.srt
```

#### Trim Video
```bash
# Using -ss (inputseek - fast)
ffmpeg -ss 00:01:00 -i input.mp4 -to 00:02:00 -c copy output.mp4

# Using -ss (outputseek - accurate but slow)
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy output.mp4
```

#### Combine Videos
```bash
# Concatenate with filter
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
# filelist.txt contains:
# file '/path/to/video1.mp4'
# file '/path/to/video2.mp4'
```

#### Create GIF
```bash
# High quality GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif

# Simple GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif
```

#### Screen Recording
```bash
# macOS
ffmpeg -f avfoundation -i "1:0" -r 30 output.mp4

# Linux (X11)
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0.0 output.mp4

# Windows
ffmpeg -f gdigrab -framerate 30 -i desktop output.mp4
```

### Step 5: Use Stream Specifiers

Apply options to specific streams:
- `:v` - All video streams
- `:a` - All audio streams
- `:s` - All subtitle streams
- `:v:0` - First video stream
- `:a:1` - Second audio stream
- `:0:v:0` - Video stream 0 from input 0

Examples:
```bash
# Different codecs for different streams
ffmpeg -i input.mkv -c:v:0 libx264 -c:v:1 libx265 output.mkv

# Copy audio, re-encode video
ffmpeg -i input.mp4 -c:v libx264 -c:a copy output.mp4
```

### Step 6: Apply Filters

#### Video Filters (via -vf)
```bash
# Deinterlace
ffmpeg -i input.mp4 -vf yadif output.mp4

# Crop
ffmpeg -i input.mp4 -vf crop=1280:720:0:0 output.mp4  # W:H:X:Y

# Rotate
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# Overlay text
ffmpeg -i input.mp4 -vf "drawtext=text='Hello':fontsize=24:fontcolor=white:x=10:y=10" output.mp4

# Overlay image on video
ffmpeg -i video.mp4 -i overlay.png -filter_complex overlay output.mp4

# Stack videos horizontally
ffmpeg -i left.mp4 -i right.mp4 -filter_complex hstack output.mp4
```

#### Audio Filters (via -af)
```bash
# Volume adjustment
ffmpeg -i input.mp4 -af "volume=1.5" output.mp4

# Normalize audio
ffmpeg -i input.mp4 -af "loudnorm" output.mp4

# Fade in/out
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=2,afade=t=out:st=50:d=2" output.mp4
```

### Step 7: Advanced Scenarios

#### Two-Pass Encoding
```bash
# Pass 1
ffmpeg -i input.mp4 -c:v libx264 -pass 1 -an -f null /dev/null

# Pass 2
ffmpeg -i input.mp4 -c:v libx264 -pass 2 -b:v 2M output.mp4
```

#### Hardware Acceleration
```bash
# NVIDIA (NVENC)
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4

# Intel (QSV)
ffmpeg -hwaccel qsv -i input.mp4 -c:v h264_qsv output.mp4

# macOS (VideoToolbox)
ffmpeg -hwaccel videotoolbox -i input.mp4 -c:v h264_videotoolbox output.mp4
```

#### HLS Streaming
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -f hls -hls_time 4 -hls_playlist_type vod output.m3u8
```

#### Extract Frames
```bash
# Extract one frame per second
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.png

# Extract frame at specific time
ffmpeg -ss 00:00:05 -i input.mp4 -frames:v 1 frame.png
```

## Best Practices

### Quality Settings

- **CRF (Constant Rate Factor)**: Recommended for quality-based encoding
  - Range: 0-51 (lower = better quality, larger file)
  - Recommended: 18-28 for H.264
  - Default: 23 for H.264

- **Presets**: Balance encoding speed vs compression
  - `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`
  - `medium` (default)
  - `slow`, `slower`, `veryslow`

### Performance Tips

1. **Use streamcopy (`-c copy`)** when not transcoding - much faster
2. **Avoid re-encoding** when possible - quality loss accumulates
3. **Use hardware acceleration** when available
4. **Presets**: `veryfast` for live, `veryslow` for final encode
5. **Thread count**: `-threads` option (usually auto is best)

### Common Pitfalls

- **Aspect ratio**: Always consider aspect ratio when scaling
- **Audio sync**: Use `-vsync` options if audio drift occurs
- **Codec compatibility**: Ensure target device supports chosen codecs
- **Bitrate vs quality**: Don't set both CRF and bitrate
- **File extensions**: Use correct extension for output format

## Common Codecs

### Video Codecs
- `libx264` - H.264 (most compatible)
- `libx265` / `hevc` - H.265 (better compression)
- `libvpx-vp9` - VP9 (WebM)
- `libaom-av1` - AV1 (next-gen)
- `mpeg4` - MPEG-4 Part 2 (legacy)
- `copy` - Streamcopy (no re-encoding)

### Audio Codecs
- `aac` - AAC (standard)
- `libmp3lame` - MP3
- `libopus` - Opus (modern)
- `libvorbis` - Vorbis (WebM)
- `pcm_s16le` - Uncompressed PCM
- `copy` - Streamcopy

### Container Formats
- `mp4` - Most compatible
- `mkv` - Feature-rich
- `webm` - Web optimized (VP8/VP9)
- `avi` - Legacy
- `mov` - QuickTime
- `flv` - Flash video

## Stream Selection Examples

```bash
# Map all streams from input
ffmpeg -i input.mp4 -map 0 output.mkv

# Map only video from first input
ffmpeg -i input.mp4 -map 0:v output.mp4

# Map specific streams
ffmpeg -i1.mkv -i2.mp4 -map 0:0 -map 1:1 output.mp4

# Negative mapping (exclude)
ffmpeg -i input.mp4 -map 0 -map -0:a output.mp4  # Exclude all audio

# Map by language
ffmpeg -i input.mkv -map 0:m:language:eng output.mp4
```

## Troubleshooting

### Command fails
- Check if input file exists and is readable
- Verify codec is supported: `ffmpeg -codecs`
- Check syntax: options go before the file they affect

### Quality issues
- Increase CRF value for better quality (lower number)
- Use slower preset for better compression
- Check bitrate settings

### Audio sync issues
- Try different `-vsync` modes
- Use `-async 1` to sync audio to video
- Check frame rate settings

### Performance issues
- Use hardware acceleration
- Try faster preset
- Reduce resolution first, then encode
- Check CPU usage with `-threads`

## Advanced Reference

For complex filtergraphs, see [filter documentation](https://ffmpeg.org/ffmpeg-filters.html)

For codec options, use:
```bash
ffmpeg -h encoder=libx264
ffmpeg -h decoder=h264
```

For format options:
```bash
ffmpeg -h muxer=mp4
ffmpeg -h demuxer=mp4
```
