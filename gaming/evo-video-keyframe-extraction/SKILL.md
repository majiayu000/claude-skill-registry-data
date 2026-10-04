---
name: evo-video-keyframe-extraction
description: Extracts keyframes from an MP4 video at uniform temporal intervals using OpenCV VideoCapture, saves them with sequential naming (keyframes_001.png, keyframes_002.png, etc.), and converts them in-place from BGR to grayscale.
---

# evo-video-keyframe-extraction

## Overview
Extracts keyframes from gameplay video using uniform temporal sampling, saves with zero-padded sequential naming, and converts to grayscale in-place.

## Key Concepts
- Uses `cv2.VideoCapture` for video decoding with embedded FFmpeg backend
- Uniform temporal sampling: extract 1 frame per second (frame_interval = int(fps * 1.0))
- Frames saved as PNG with `cv2.imwrite()` using zero-padded naming: `keyframes_001.png`, `keyframes_002.png`, etc.
- Grayscale conversion done in-place: read with `cv2.IMREAD_GRAYSCALE`, overwrite original file
- OpenCV uses BGR channel order (not RGB)
- For a 27-second 60fps video, extracts 27 keyframes (one per second)

## Functions

### `get_video_metadata(video_path)`
Returns dict with: fps, frame_count, width, height, duration_seconds

### `extract_keyframes(video_path, output_dir, sample_interval_seconds=1.0, name_format="keyframes_{:03d}.png")`
Extracts keyframes at uniform intervals. Returns list of saved file paths in timeline order.
- `sample_interval_seconds=1.0` means 1 frame per second
- `name_format` uses Python format string with {:03d} for zero-padded numbering starting at 1
- Keyframe counter is 1-based (keyframes_001.png, keyframes_002.png, ...)

### `convert_frames_to_grayscale(frame_paths)`
Converts images to grayscale IN-PLACE (overwrites original files). Returns list of converted paths.
Reads with cv2.IMREAD_GRAYSCALE and writes back with cv2.imwrite.

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-video-keyframe-extraction/scripts')
from video_utils import extract_keyframes, convert_frames_to_grayscale, get_video_metadata

# Get video info
meta = get_video_metadata('/root/super-mario.mp4')
print(f"Duration: {meta['duration_seconds']}s, FPS: {meta['fps']}")

# Extract keyframes (1 per second) to /root
paths = extract_keyframes('/root/super-mario.mp4', '/root', sample_interval_seconds=1.0)

# Convert to grayscale in-place
convert_frames_to_grayscale(paths)
```
