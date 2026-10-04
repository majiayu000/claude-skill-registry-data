---
name: spatial-occupancy-event
description: Determine whether visually observed subjects occupy configured video monitoring ROI regions through extracted-frame LLM review. Use when Codex has video frames, camera_id, ROI hints, method_config, or needs visual evidence for illegal parking, lane occupancy, sidewalk occupancy, intrusion, or public-area occupation.
---

# Spatial Occupancy Event

## Execution Priority

Prioritize extracted-frame visual analysis. Call `scripts/run.py` only when reliable `roi_matches` and `tracks` already exist or the user explicitly asks for geometric rule execution.

## Input Resolution

If `roi_matches`, `tracks`, or objects are missing but the user provided a video, do not ask the user to provide them. Extract timestamped frames first with `analyze-video/scripts/extract_frames.py` or `frame-sampling/scripts/run.py`, inspect the frames visually, and decide whether the subject is inside or overlapping the configured ROI. Use object detection/tracking/ROI scripts only as optional measurements to support the visual conclusion.

## LLM Visual Workflow

1. Identify the ROI from user text, camera config, visible lane/sidewalk/door/entrance boundaries, or provided polygons.
2. Inspect coarse frames to find possible occupancy moments.
3. Inspect adjacent or dense frames around each moment to confirm the subject remains in the ROI.
4. Record the subject, ROI, visible boundary cue, timestamps, evidence frame ids, and confidence.
5. Mark ambiguous cases for review when perspective, occlusion, or missing ROI definitions make the boundary unclear.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python spatial-occupancy-event/scripts/run.py --roi-matches-json <roi_matches.json> --tracks-json <tracks.json> --target-labels person --roi-types public_area --output <method_result.json>
```

Parameters: `--roi-matches-json`, `--tracks-json`, `--target-labels`, `--roi-types`, `--excluded-roi-types`, `--min-overlap-ratio`, `--min-confidence`, `--method-config`, `--output`.

## Workflow

1. Read target labels, ROI types, excluded ROI types, position strategy, and thresholds.
2. Review extracted frames to locate visually relevant subjects and ROI boundaries.
3. Optionally use tracks or ROI matches as supporting geometry.
4. Return method-level matches with subject ids or visual subject descriptions, ROI ids, confidence, and evidence frame ids.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `method_config.target_labels`
- `method_config.roi_types`
- `method_config.excluded_roi_types`
- `method_config.min_overlap_ratio`
- `method_config.min_confidence`
- `tracks`
- `roi_matches`

## Outputs

Returns `method="spatial_occupancy"`, `matched`, and `matches`.

## Failure Modes

Returns `matched=false` when no subject passes label, ROI, overlap, and confidence filters.

## Constraints

Do not generate evidence, route work orders, or emit final business event types directly. Do not treat detector boxes as sufficient when visual boundary evidence is available.
