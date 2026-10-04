---
name: object-tracking
description: Track detected objects across video frames and return Track schema. Use when Codex has frame-level detections and needs stable track ids, trajectories, duration, last bbox, movement state, confidence, and evidence frame ids before ROI mapping and temporal event rules.
---

# Object Tracking

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If `detections` are missing but the user provided frames or a video, do not ask the user to provide detections and do not write tracking code. Call upstream skills in order: `frame-sampling/scripts/run.py` when frames are missing, then `object-detection/scripts/run.py`, then this skill. Use the detection labels implied by the task, such as `person` for people, fight, crowd, or behavior analysis.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python object-tracking/scripts/run.py --detections-json <detections.json> --camera-id <camera_id> --config <config.json> --output <tracks.json>
```

Parameters: `--detections-json`, `--camera-id`, `--association-distance-pixels`, `--stationary-distance-pixels`, `--config`, `--output`.

## Workflow

1. Sort detections by timestamp.
2. Associate same-label detections across frames.
3. Build track trajectory, start/end times, duration, last bbox, and confidence.
4. Classify movement state as stationary or moving.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `camera_id`
- `detections`
- Optional `tracks` to pass through precomputed tracks

## Outputs

Returns `tracks`, each with `track_id`, `label`, `start_time`, `end_time`, `duration_seconds`, `trajectory`, `movement_state`, `confidence`, `last_bbox`, and `evidence_frame_ids`.

## Failure Modes

The current implementation tolerates empty detections and returns an empty track list.

## Constraints

Do not apply ROI rules or emit event candidates.
