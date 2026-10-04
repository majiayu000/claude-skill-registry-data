---
name: video-merger
description: Merge multiple video files or all videos in a directory into a single output file using ffmpeg. Use when user wants to combine clips, stitch recordings, or join video segments.
---

# Video Merger Skill

Merge multiple video files into one using `ffmpeg`.

## Prerequisites

- `ffmpeg` must be installed on the system.

## Usage

Use the provided Python script to merge video files by specifying individual files or a directory.

### Commands

**Merge individual files**:
```bash
python3 <path-to-skill>/scripts/merge_videos.py video1.mp4 video2.mp4 -o final_video.mp4
```

**Merge all videos in a directory**:
```bash
# Merges all supported video files in the specified directory
python3 <path-to-skill>/scripts/merge_videos.py --dir ./my_videos -o final_video.mp4
```

**Merge and sort by time**:
```bash
python3 <path-to-skill>/scripts/merge_videos.py --dir ./my_videos --sort time -o final_video.mp4
```

### Important Considerations

- **Codec Compatibility**: The current implementation uses the `concat` demuxer with `-c copy`, which is extremely fast because it doesn't re-encode the video. However, it requires all input videos to have the same stream parameters (resolution, frame rate, codecs, etc.).
- **Natural Sorting**: When using `--dir`, files are sorted using "natural sort" (e.g., `1.mp4` comes before `10.mp4`).
- **Supported Extensions**: `.mp4`, `.mkv`, `.avi`, `.mov`, `.flv`, `.wmv`, `.m4v`.

## Workflow

1. Identify the list of video files or the directory to be merged.
2. Determine the desired order (individual list, natural name sort, or modification time).
3. Call the `merge_videos.py` script with the appropriate arguments.
4. If the fast merge fails, inform the user about codec compatibility issues.
