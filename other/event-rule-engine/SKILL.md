---
name: event-rule-engine
description: Detect video monitoring events through frame extraction plus LLM visual review, then map visual evidence into Event Candidate schema. Use when Codex has a video, frame images, camera_id, event_templates, or a request such as fight, traffic accident, crowding, illegal parking, smoke/fire, fall, intrusion, occupancy, or other monitoring incident detection.
---

# Event Rule Engine

## Execution Priority

Prioritize LLM visual analysis over detector-only event rules. For event detection from real video, first extract frames, inspect the images directly, and build a visual timeline. Only call this skill's `scripts/run.py` when the user already provides reliable `detections`, `tracks`, `roi_matches`, or explicitly asks for rule-engine execution.

## Input Resolution

If the user provides a video, do not ask for `detections`, `tracks`, or `roi_matches` first. Build visual evidence by calling `analyze-video/scripts/extract_frames.py` for forensic scene/keyframe extraction, or `frame-sampling/scripts/run.py` for regular interval sampling. Use 1 FPS as the default coarse pass and add denser sampling around suspected moments when motion, contact, crowding, lane change, fall, smoke, flame, or other state changes are visible.

After frame extraction, inspect representative frames with the available image-viewing capability. Treat object detection, tracking, and ROI scripts as optional helpers, not the source of truth, because event semantics such as fighting, accident, fall, congestion, dumping, smoke/fire, or intrusion usually require visual reasoning across frames.

## LLM Visual Event Workflow

1. Extract frames with timestamps and metadata.
2. Review frames in chronological order, first coarse frames, then dense frames around candidate moments.
3. For each candidate event, write frame-level observations: visible subjects, actions, spatial relationships, scene context, and uncertainty.
4. Compare observations across adjacent timestamps to determine temporal change, persistence, contact, escalation, disappearance, or recovery.
5. Map the observed pattern to the closest event template only when the visual evidence supports it.
6. Return event candidates with evidence frame ids, time range, reason, confidence, and any uncertainty requiring human review.

## Visual Evidence Rules

- Prefer "unknown" or `requires_review=true` over overconfident classification when frames are blurry, occluded, too sparse, or ambiguous.
- Do not infer off-camera causes. Only state what is visible in sampled frames.
- Use at least two timestamps for temporal events unless the event is evident in a single frame, such as visible fire, smoke, crash aftermath, or a person lying on the ground.
- Increase confidence when multiple adjacent frames show the same event pattern and lower confidence when the event depends on a single low-quality frame.
- Include negative evidence when relevant, for example "no visible collision before 00:12" or "crowd disperses by 00:26".


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python event-rule-engine/scripts/run.py --frames-json <frames.json> --detections-json <detections.json> --tracks-json <tracks.json> --roi-matches-json <roi_matches.json> --camera-id <camera_id> --config <config.json> --output <events.json>
```

Parameters: `--frames-json`, `--detections-json`, `--tracks-json`, `--roi-matches-json`, `--rois-json`, `--camera-health-json`, `--camera-id`, `--templates`, `--config`, `--output`.

## Workflow

1. Read enabled event templates from input or config.
2. Extract or load timestamped frame images.
3. Perform LLM visual review over coarse and dense frame sets.
4. Convert visual observations into method-level evidence such as spatial occupancy, temporal persistence, object composition, or density aggregation.
5. Apply template mapping and confidence scoring.
6. Return event candidates with visual reasons, evidence frame ids, and review flags.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `camera_id`
- `frames`
- `detections`
- `tracks`
- `roi_matches`
- `segments`
- `camera_health`
- `templates`

Config required:
- `context.config["event_templates"]`
- Optional `context.config["enabled_event_templates"]`

## Outputs

Returns `events` and `method_outputs`. Each event includes `event_id`, `event_type`, `camera_id`, `confidence`, `reason`, `method_hits`, `rule_hits`, `related_tracks`, and `evidence_frame_ids`.

## Failure Modes

- `MISSING_REGISTRY`
- Propagates failures from called method skills.

## Constraints

Do not hard-code local policies or create evidence files. Do not rely on detector labels alone for final event semantics when frame images are available.
