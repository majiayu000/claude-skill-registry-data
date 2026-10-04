---
name: ffmpeg
description: "Transcode and compress video with FFmpeg, inspect streams with ffprobe, build filtergraphs and HLS outputs, and diagnose codec or hardware-encoder failures."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["ffmpeg", "video-transcoding", "hls-streaming", "nvenc", "ffprobe", "filtergraph", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# FFmpeg Media Engineering AI Skill Guide (Claude)

## Overview & Engine Architecture
FFmpeg is the universal open-source command-line framework for video/audio decoding, transcoding, streaming, muxing, and complex filtergraph processing. Claude operates as a Principal Video Streaming and Codec Engineer, specializing in **codec rate control (CRF, CBR, VBR, CQP)**, **hardware acceleration (NVIDIA NVENC, Intel QuickSync/QSV, Apple VideoToolbox, VAAPI)**, **adaptive bitrate HLS/DASH packaging**, and **Python `asyncio` batch automation**.

### FFmpeg Core Subsystems & Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 FFmpeg Transcoding Pipeline                 │
│                                                             │
│  Demuxing & Decoding Layer                                  │
│  ├── `libavformat` (Container Demuxer: MP4, MKV, MOV, TS)   │
│  ├── `libavcodec` (Decoders: H.264, HEVC, AV1, ProRes, AAC) │
│  └── Hardware Decoders (`cuvid`, `qsv`, `videotoolbox`)     │
│                                                             │
│  Processing & Encoding Layer                                │
│  ├── `libavfilter` (Complex Filtergraphs: scale, pad, fps)  │
│  ├── `libswscale` & `libswresample` (Color & Audio Resample)│
│  └── Hardware Encoders (`h264_nvenc`, `hevc_qsv`, `libsvtav1`)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Hardware-Accelerated Codec Optimization**: Configure optimal encoding flags for target hardware platforms (`-hwaccel cuda -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 19`).
2. **Deterministic Filtergraph Authoring**: Author multi-input/multi-output `-filter_complex` graphs for watermark overlay, side-by-side video stitching, loudness normalization (`loudnorm`), and subtitle burn-in.
3. **Adaptive Bitrate (ABR) HLS Streaming**: Construct multi-rendition HLS pipelines (1080p, 720p, 480p) with keyframe interval alignment (`-g 60 -keyint_min 60 -sc_threshold 0`).
4. **Automated Stream Health Diagnostics**: Analyze `ffprobe` JSON outputs to detect variable framerates (VFR), corrupted audio PTS/DTS timestamps, and pixel format incompatibilities.

---

## Production Python Automation: Adaptive Multi-Rendition HLS Packager

Save this script as `hls_packager.py` and run with Python 3 to generate a production-ready Master HLS playlist with 1080p, 720p, and 480p streams:

```python
"""
FFmpeg Automated Adaptive Bitrate (ABR) HLS Packager
Generates aligned keyframe HLS renditions and a Master Playlist.
"""

import sys
import os
import subprocess
import json

def get_video_info(input_file: str) -> dict:
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", input_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFprobe failed: {result.stderr}")
    return json.loads(result.stdout)

def encode_hls_stream(input_file: str, output_dir: str):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    
    # FFmpeg Command for Multi-Rendition HLS
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", input_file,
        # Common encoding parameters: 2s GOP at 30fps = 60 frames
        "-filter_complex",
        "[0:v]split=3[v1][v2][v3]; "
        "[v1]scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v1out]; "
        "[v2]scale=w=1280:h=720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v2out]; "
        "[v3]scale=w=854:h=480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2[v3out]",
        
        # Rendition 1 (1080p)
        "-map", "[v1out]", "-c:v:0", "libx264", "-b:v:0", "5000k", "-maxrate:v:0", "5350k", "-bufsize:v:0", "7500k",
        # Rendition 2 (720p)
        "-map", "[v2out]", "-c:v:1", "libx264", "-b:v:1", "2800k", "-maxrate:v:1", "2996k", "-bufsize:v:1", "4200k",
        # Rendition 3 (480p)
        "-map", "[v3out]", "-c:v:2", "libx264", "-b:v:2", "1400k", "-maxrate:v:2", "1498k", "-bufsize:v:2", "2100k",
        
        # Map Audio
        "-map", "0:a?", "-c:a", "aac", "-b:a", "128k", "-ac", "2",
        
        # Strict GOP alignment for HLS
        "-g", "60", "-keyint_min", "60", "-sc_threshold", "0",
        
        # HLS Packaging Flags
        "-f", "hls",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-hls_flags", "independent_segments",
        "-hls_segment_type", "mpegts",
        "-hls_segment_filename", os.path.join(output_dir, "stream_%v_data%03d.ts"),
        "-master_pl_name", "master.m3u8",
        "-var_stream_map", "v:0,a:0 v:1,a:0 v:2,a:0",
        os.path.join(output_dir, "stream_%v.m3u8")
    ]

    print(f"Starting Multi-Rendition HLS encoding for {input_file}...")
    proc = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    if proc.returncode == 0:
        print(f"HLS package generated successfully at: {os.path.join(output_dir, 'master.m3u8')}")
    else:
        print(f"Encoding failed:\n{proc.stderr}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python hls_packager.py <input_video> <output_dir>")
        sys.exit(1)
    encode_hls_stream(sys.argv[1], sys.argv[2])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Unknown encoder 'h264_nvenc'`** | FFmpeg build does not include NVENC compilation flags, or NVIDIA GPU driver is missing/outdated. | 1. Run `ffmpeg -encoders \| grep nvenc` to check support.<br>2. Fallback to software encoder `libx264` or Intel `h264_qsv`.<br>3. Install latest NVIDIA Studio / Data Center drivers. |
| **Audio/Video Drift / Desync in Output** | Input video has Variable Frame Rate (VFR) from smartphone or screen recording. | 1. Force constant frame rate (CFR): `-vsync cfr -r 30`.<br>2. Use the `fps` filter: `-vf fps=30`.<br>3. Use `aresample=async=1` in audio filter chain to align timestamps. |
| **`Non-monotonous DTS in output stream` Warnings** | Source container contains out-of-order presentation timestamps or corrupted B-frame headers. | 1. Add `-fflags +genpts` before input `-i`.<br>2. Re-mux container using `-c copy -avoid_negative_ts make_zero`. |
| **Colors Appear Washed Out on QuickTime / iOS** | Encoded video uses 4:2:2 / 4:4:4 chroma subsampling or missing standard color metadata tags. | 1. Enforce universal 4:2:0 subsampling: `-pix_fmt yuv420p`.<br>2. Explicitly tag BT.709 color space: `-color_primaries bt709 -color_trc bt709 -colorspace bt709`. |

---

## Command Line Syntax & Production Recipes

```bash
# 1. High-Quality Web Transcode (Software CRF 23, Faststart for Web Streaming)
ffmpeg -i input.mov -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k output.mp4

# 2. Ultra-Fast GPU Transcode (NVIDIA NVENC Hardware Encoding)
ffmpeg -hwaccel cuda -i input.mkv -c:v h264_nvenc -preset p6 -cq 20 -c:a copy output.mp4

# 3. Lossless Stream Remux (Instant Container Conversion without Re-encoding)
ffmpeg -i input.mkv -c copy -movflags +faststart output.mp4

# 4. Two-Pass Audio Loudness Normalization (EBU R128 Broadcast Standard)
ffmpeg -i input.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a pcm_s24le output.wav
```

---

## Agent Operational Directive
> **MANDATORY**: For web-distributed MP4 files, always include `-pix_fmt yuv420p` for broad browser compatibility and `-movflags +faststart` to move the MOOV atom to the beginning of the file for instant streaming playback.
