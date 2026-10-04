---
name: camera-health-check
description: Check video monitoring camera quality from sampled frames and return health status before downstream event generation. Use when Codex has camera_id and frames and needs to gate or downgrade event confidence for offline, unavailable, degraded, black-screen, blurred, occluded, frozen, corrupted, or shifted camera feeds.
---

# Camera Health Check

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If `frames` are missing but the user provided a video source, do not ask the user to provide frames and do not write custom camera diagnostics. First call `frame-sampling/scripts/run.py` to generate frames, then call this skill.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python camera-health-check/scripts/run.py --frames-json <frames.json> --camera-id <camera_id> --config <config.json> --output <health.json>
```

Parameters: `--frames-json`, `--camera-id`, `--health-status`, `--config`, `--output`.

## Workflow

1. Read camera id and sampled frames.
2. Check frame availability and configured/manual health overrides.
3. Compute or accept quality signals for black screen, blur, occlusion, freeze, corruption, and view shift.
4. Return health status, health score, and issue reasons.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `camera_id`
- `frames`
- Optional `health_status` override
- Optional `context.config["camera_health"][camera_id]` override

## Outputs

Returns `health_status`, `health_score`, and `issues`.

## Failure Modes

The current implementation returns success with `health_status="unavailable"` when no frames are available.

## Constraints

Do not create events or evidence. Low quality should reduce downstream confidence or trigger review.
