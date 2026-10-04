---
name: frame-sampling
description: Sample structured frames from video monitoring segments or streams. Use when Codex has raw_segment_uri, camera_id, source_type=local_file, sampling_strategy, capture_seconds, or provided frame records and needs stable Frame schema outputs. This skill exposes OpenCV-backed real video frame extraction and mock frame generation for tests.
---

# Frame Sampling

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If the user provides a video file instead of `frames`, do not ask the user to provide frames and do not write custom OpenCV extraction code. First call `video-stream-ingestion/scripts/run.py` when the source needs normalization, then call this skill with `camera_id`, `source_type=local_file`, `raw_segment_uri`, `capture_seconds`, and `sampling_strategy`. Use `sampling_strategy.mode=interval` and `interval_seconds=1` as the default unless the user requests a different cadence.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python frame-sampling/scripts/run.py --video <video.mp4> --camera-id <camera_id> --capture-seconds 10 --interval-seconds 1 --output-dir <run_dir> --config <config.json> --output <frames.json>
```

Parameters: `--video`, `--frames-json`, `--camera-id`, `--capture-seconds`, `--interval-seconds`, `--fps`, `--output-dir`, `--config`, `--output`.

## Workflow

1. Read camera id, raw segment URI, and sampling strategy.
2. Support interval, fps, keyframe, and adaptive strategies when available.
3. Generate stable frame ids from camera id, timestamp, and sequence.
4. Store sampled images and return Frame schema records.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

Required:
- `camera_id`

Common fields:
- `raw_segment_uri`
- `source_type`
- `started_at`
- `capture_seconds`
- `sampling_strategy.mode`: `interval` or `fps`
- `sampling_strategy.interval_seconds`
- `sampling_strategy.fps`

## Outputs

Returns `frames`, each with `frame_id`, `camera_id`, `timestamp`, `image_uri`, `width`, `height`, `sequence`, and for real video `source_elapsed_seconds`.

## Failure Modes

- `MISSING_CAMERA_ID`
- `VIDEO_OPEN_FAILED`

## Constraints

Do not run detection, tracking, event recognition, or evidence annotation.
