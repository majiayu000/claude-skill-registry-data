---
name: concat-mp4
description: Concatenate multiple MP4 files in order into a single MP4 using ffmpeg stream copy.
dependencies:
  - python>=3.11
  - ffmpeg (cli tool)
---

# Concatenate MP4 Files

Join several `.mp4` files in sequence without re-encoding (ffmpeg concat demuxer).

### Run

```bash
.venv/Scripts/python .claude/skills/concat_videos/scripts/concat_videos.py "output.mp4" "clip1.mp4" "clip2.mp4" "clip3.mp4"
```

### Parameters

- Required: `output` (destination mp4), `inputs` (>=2 mp4 files, ordered)
- Optional: none

### Example

```bash
.venv/Scripts/python .claude/skills/concat_videos/scripts/concat_videos.py "./out/combined.mp4" "./out/part1.mp4" "./out/part2.mp4"
```
