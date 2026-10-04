---
name: evo-video-sampling
description: Extracts frames from an MP4 video file at a specified target FPS using sequential reading. Returns sampled grayscale frames and their original frame indices.
---

# evo-video-sampling

Extracts frames from an MP4 video at a target FPS using reliable sequential reading
(avoids unreliable CAP_PROP_POS_FRAMES seeking in compressed MP4s).

## Key Function

- `sample_video_frames(video_path, target_fps=6)` — Returns `(sampled_frames, frame_indices, original_fps)`
  - `sampled_frames`: list of grayscale np.uint8 2D arrays
  - `frame_indices`: list of original frame indices (0-based)
  - `original_fps`: the video's native FPS

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-video-sampling/scripts')
from utils import sample_video_frames

frames, indices, fps = sample_video_frames('/root/input.mp4', target_fps=6)
print(f"Sampled {len(frames)} frames from video at {fps} FPS")
```

## Implementation Details

- Uses `cv2.VideoCapture` with sequential `read()` loop (no seeking)
- Frame step = `max(1, int(round(original_fps / target_fps)))`
- Converts BGR to grayscale immediately via `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`
- Fallback FPS of 30.0 if `CAP_PROP_FPS` returns <= 0
