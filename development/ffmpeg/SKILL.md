---
name: ffmpeg
description: FFmpeg/FFprobe command reference for media operations — transcode, probe, extract, concat, filter, stream copy, HW accel. Use when an agent needs to manipulate audio/video files directly without a higher-level abstraction (HyperFrames, Remotion, video-use). Covers the installed build (8.1.1, Homebrew, Apple Silicon) with its enabled libraries.
---

# ffmpeg

Direct media manipulation via `ffmpeg` and `ffprobe`. Use this skill for operations that don't need a full video editing pipeline (video-use) or composition framework (HyperFrames/Remotion).

## Installed Build

```
ffmpeg 8.1.1 — Homebrew, Apple Silicon (aarch64)
Path: /opt/homebrew/bin/ffmpeg
HW accel: VideoToolbox (encode/decode), AudioToolbox
Codecs: libx264, libx265, libsvtav1, libvpx, libopus, libmp3lame, libdav1d
Scoring: libvmaf
TLS: openssl
```

## Probe Before Act

Always `ffprobe` before processing. Never assume codec, resolution, framerate, or duration.

```bash
# JSON probe (agent-friendly)
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Quick duration
ffprobe -v quiet -show_entries format=duration -of csv=p=0 input.mp4

# Stream summary
ffprobe -v quiet -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate,channels,sample_rate -of json input.mp4
```

## Common Operations

### Transcode

```bash
# H.264 (universal compatibility)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# H.265 (smaller files, good device support)
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset medium -c:a aac -b:a 128k output.mp4

# AV1 (best compression, slower encode)
ffmpeg -i input.mp4 -c:v libsvtav1 -crf 30 -preset 6 -c:a libopus -b:a 128k output.webm

# VP9 + Opus (web)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus -b:a 128k output.webm
```

### HW-Accelerated (Apple Silicon)

```bash
# VideoToolbox H.264 encode (fast, lower quality control)
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M -c:a aac output.mp4

# VideoToolbox H.265 encode
ffmpeg -i input.mp4 -c:v hevc_videotoolbox -b:v 3M -c:a aac output.mp4

# HW decode + SW encode (best quality with fast decode)
ffmpeg -hwaccel videotoolbox -i input.mp4 -c:v libx264 -crf 23 -c:a aac output.mp4
```

### Stream Copy (no re-encode)

```bash
# Trim without re-encoding
ffmpeg -ss 00:01:30 -to 00:03:00 -i input.mp4 -c copy trimmed.mp4

# Extract audio
ffmpeg -i input.mp4 -vn -c:a copy audio.aac
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3

# Strip audio
ffmpeg -i input.mp4 -an -c:v copy video_only.mp4

# Remux (change container)
ffmpeg -i input.mkv -c copy output.mp4
```

### Extract

```bash
# Single frame at timestamp
ffmpeg -ss 00:00:05 -i input.mp4 -frames:v 1 frame.png

# Frame sequence (1 fps)
ffmpeg -i input.mp4 -vf "fps=1" frames/frame_%04d.png

# Thumbnail grid (4x4)
ffmpeg -i input.mp4 -vf "select='not(mod(n,100))',scale=320:-1,tile=4x4" -frames:v 1 grid.png

# GIF from segment
ffmpeg -ss 5 -t 3 -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" out.gif
```

### Concat

```bash
# File list concat (same codec)
printf "file '%s'\n" clip1.mp4 clip2.mp4 clip3.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Re-encode concat (mixed codecs/resolutions)
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" output.mp4
```

### Filters

```bash
# Scale
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:a copy output.mp4

# Overlay (picture-in-picture)
ffmpeg -i main.mp4 -i overlay.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# Color correction (ASC CDL model)
ffmpeg -i input.mp4 -vf "eq=brightness=0.06:contrast=1.1:saturation=1.2" output.mp4

# Fade in/out
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" -af "afade=t=in:st=0:d=1,afade=t=out:st=9:d=1" output.mp4

# Speed change (2x)
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" output.mp4

# Burn subtitles
ffmpeg -i input.mp4 -vf "subtitles=subs.srt:force_style='FontSize=24,PrimaryColour=&H00FFFFFF'" output.mp4

# Audio normalization (loudnorm two-pass)
ffmpeg -i input.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | tail -12
# Then apply measured values in second pass
```

### Audio

```bash
# WAV extraction (for processing)
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# Mix audio tracks
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[a]" -map 0:v -map "[a]" -c:v copy output.mp4

# Volume adjustment
ffmpeg -i input.mp4 -af "volume=1.5" output.mp4

# Silence detection
ffmpeg -i input.mp4 -af "silencedetect=noise=-30dB:d=0.5" -f null - 2>&1 | grep silence
```

### Batch / Scripting Patterns

```bash
# Process all MP4s in directory
for f in *.mp4; do ffmpeg -i "$f" -c:v libx264 -crf 23 -c:a aac "out/${f}"; done

# Parallel with xargs (4 jobs)
ls *.mp4 | xargs -P4 -I{} ffmpeg -i {} -c:v libx264 -crf 23 -c:a aac out/{}
```

## Quality Guidelines

| Use case | Codec | CRF/Bitrate | Notes |
|----------|-------|-------------|-------|
| Archive | libx264 | CRF 18 | Visually lossless |
| Web delivery | libx264 | CRF 23 | Good balance |
| Social media | libx264 | CRF 20-22 | Platforms re-encode anyway |
| Transparent overlay | VP9/WebM | CRF 30 | `-pix_fmt yuva420p` |
| Audio podcast | libmp3lame | `-q:a 2` | ~190kbps VBR |
| Voice-only | libopus | 64k | Mono, 16kHz |

## Hard Rules

1. **Probe first.** Never assume input properties.
2. **Stream copy when possible.** If you're not changing the codec, use `-c copy`.
3. **Use `-movflags +faststart`** on MP4 outputs for web delivery.
4. **30ms audio fades at cut boundaries** to prevent pops: `afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03`.
5. **Interleaved stream order for concat** filter: `[v0][a0][v1][a1]`, not `[v0][v1][a0][a1]`.
6. **Never merge duplicate filters** silently — two `scale` filters in a chain must be collapsed into one or separated by a split.
7. **Verify output** after every operation: `ffprobe` the result, check duration, check file size > 0.
8. **Quote paths** — filenames with spaces or special chars break unquoted.

## VMAF Quality Scoring

```bash
# Compare transcoded output against original
ffmpeg -i distorted.mp4 -i reference.mp4 -lavfi libvmaf -f null -
```

## Relationship to Other Skills

| Skill | When to use instead |
|-------|-------------------|
| video-use | Full editing pipeline: multi-take selection, EDL, color grade, overlays, subtitles |
| hyperframes | HTML/CSS video compositions, animated overlays, captions |
| hyperframes-cli | HyperFrames project lifecycle (init, lint, render) |
| cli-anything | Building a full CLI harness around ffmpeg for a specific workflow |

Use this ffmpeg skill for **direct, one-off media operations** that don't need the orchestration layer of video-use or the composition model of HyperFrames.
