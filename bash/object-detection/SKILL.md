---
name: object-detection
description: Detect objects in sampled video frames and return standard Detection schema. Use when Codex has frames and labels and needs YOLO detections with labels, confidences, and bounding boxes. This skill exposes the ultralytics YOLO backend; use it before tracking, ROI mapping, and event rules.
---

# Object Detection

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If `frames` are missing but the user provided a video path or upload, do not ask the user to provide frames and do not write detection or frame extraction code. First call `video-stream-ingestion/scripts/run.py` if needed, then `frame-sampling/scripts/run.py` to generate `frames`, then call this skill. If `labels` are missing, infer common labels from the task when safe, such as `person` for crowd, fight, behavior, or pedestrian analysis; otherwise ask only for target labels.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python object-detection/scripts/run.py --frames-json <frames.json> --labels person,car --provider ultralytics --config <config.json> --output <detections.json>
```

Parameters: `--frames-json`, `--labels`, `--provider`, `--model-path`, `--config`, `--output`.

## Workflow

1. Read frames and target labels.
2. Load the configured ultralytics YOLO detector.
3. Map model labels to internal labels.
4. Apply per-label confidence thresholds.
5. Return frame-level Detection records.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `frames`
- `labels`
- Optional `detections` to pass through precomputed results

## Outputs

Returns `detections`, each with `frame_id`, `timestamp`, and `objects` containing `object_id`, `label`, `confidence`, `bbox`, and optional `model_label`.

## Failure Modes

- `YOLO_DEPENDENCY_MISSING`
- `YOLO_MODEL_LOAD_FAILED`
- `YOLO_MODEL_NOT_FOUND`
- `YOLO_INFERENCE_FAILED`
- `FRAME_NOT_FOUND`

## Constraints

Do not infer business events, track identities, or create evidence.
