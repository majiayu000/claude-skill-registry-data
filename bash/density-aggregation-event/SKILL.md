---
name: density-aggregation-event
description: Detect excessive counts, density, or clustering through extracted-frame LLM visual review. Use when Codex needs visual evidence for crowding, congestion, gathering, queues, blocked areas, or dense person/vehicle/object aggregation in monitoring video.
---

# Density Aggregation Event

## Execution Priority

Prioritize extracted-frame visual analysis. Call `scripts/run.py` only when reliable tracks and ROI matches already exist or the user explicitly asks for numeric rule execution.

## Input Resolution

If `tracks` or `roi_matches` are missing but the user provided a video, do not ask the user to provide them. Extract timestamped frames first with `analyze-video/scripts/extract_frames.py` or `frame-sampling/scripts/run.py`, inspect the frames visually, and estimate aggregation level from visible subjects, spacing, blockage, and persistence. Use tracking/ROI scripts only as optional count support. Use task-implied labels such as `person` for crowd, density, fight, or people aggregation analysis.

## LLM Visual Workflow

1. Review coarse frames to locate high-density moments.
2. Estimate visible count by category and describe whether subjects are clustered, queued, blocked, or freely moving.
3. Compare adjacent frames to determine whether the density is momentary or sustained.
4. Record count range rather than a false precise count when subjects overlap or are partially occluded.
5. Return matched=false or requires_review when the frame quality is insufficient for a reliable density judgment.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python density-aggregation-event/scripts/run.py --tracks-json <tracks.json> --roi-matches-json <roi_matches.json> --target-labels person --min-count 3 --config <config.json> --output <method_result.json>
```

Parameters: `--tracks-json`, `--roi-matches-json`, `--rois-json`, `--target-labels`, `--roi-types`, `--min-count`, `--min-density`, `--min-duration-seconds`, `--method-config`, `--config`, `--output`.

## Workflow

1. Review extracted frames for visible aggregation patterns.
2. Estimate subject count, cluster area, spacing, and persistence.
3. Optionally use tracks and ROI matches for supporting counts.
4. Return clusters that exceed count or density thresholds with evidence frame ids and visual reasoning.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `method_config.target_labels`
- `method_config.roi_types`
- `method_config.min_count`
- `method_config.min_density`
- `method_config.min_duration_seconds`
- `tracks`
- `roi_matches`
- Optional `rois`

## Outputs

Returns `method="density_aggregation"`, `matched`, and `clusters` with `cluster_id`, `count`, `density`, `roi_id`, `duration_seconds`, and `confidence`.

## Failure Modes

Returns `matched=false` when no ROI exceeds configured count and density thresholds.

## Constraints

Do not create evidence or final business events directly. Do not report exact counts when the frame only supports a range.
