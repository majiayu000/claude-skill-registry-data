---
name: evo-template-matching-counter
description: Counts occurrences of template objects (coins, enemies, turtles) in grayscale keyframe images using OpenCV matchTemplate with TM_CCOEFF_NORMED and Non-Maximum Suppression, then aggregates results into a CSV file.
---

# evo-template-matching-counter

## Overview
Counts game sprites (coins, enemies, turtles) in grayscale keyframe images using OpenCV template matching with NMS deduplication, outputs results to CSV.

## Key Concepts
- Uses `cv2.TM_CCOEFF_NORMED` - normalized correlation coefficient, best for rigid 2D pixel art
- Default threshold: 0.8 (optimal for Super Mario sprites with MP4 compression artifacts)
- Non-Maximum Suppression (NMS) with IoU overlap threshold of 0.3 to deduplicate detections
- Both frame and template MUST be grayscale (single channel) for matching
- `np.where(result >= threshold)` returns (y_coords, x_coords) - row/column order
- Template must be smaller than frame in both dimensions
- CSV output columns: frame_id (full path like /root/keyframes_001.png), coins, enemies, turtles

## Functions

### `load_template(template_path)`
Loads template image as grayscale. Returns 2D numpy array.

### `non_max_suppression(boxes, overlap_thresh=0.3)`
Malisiewicz et al. NMS algorithm. Input: (N,4) array of [x1,y1,x2,y2]. Returns filtered boxes.

### `count_objects_in_frame(frame_gray, template_gray, threshold=0.8, nms_overlap=0.3)`
Counts single object type in a frame. Returns integer count.

### `count_all_objects_in_frame(frame_path, templates_dict, threshold=0.8, nms_overlap=0.3)`
Counts all object types in one frame. templates_dict maps label->template array. Returns dict of counts.

### `generate_results_csv(frame_paths, templates_dict, output_csv, threshold=0.8, nms_overlap=0.3)`
Processes all keyframes and writes CSV with columns: frame_id, coins, enemies, turtles. Returns DataFrame.

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-template-matching-counter/scripts')
from counter_utils import load_template, generate_results_csv

# Load templates as grayscale
templates = {
    "coins": load_template('/root/coin.png'),
    "enemies": load_template('/root/enemy.png'),
    "turtles": load_template('/root/turtle.png'),
}

# frame_paths from extraction step
frame_paths = [f'/root/keyframes_{i:03d}.png' for i in range(1, 28)]

# Generate CSV
df = generate_results_csv(frame_paths, templates, '/root/counting_results.csv', threshold=0.8)
```

## Depends On
- evo-video-keyframe-extraction (provides keyframe extraction and grayscale conversion)
