---
name: object-composition-event
description: Detect configured multi-object compositions through extracted-frame LLM visual review. Use when Codex needs visual evidence for person-vehicle interaction, fight/contact, accident aftermath, crowd grouping, dumping, obstruction, intrusion with tool/object, or other multi-subject event patterns.
---

# Object Composition Event

## Execution Priority

Prioritize extracted-frame visual analysis. Call `scripts/run.py` only when reliable detections/tracks already exist or the user explicitly asks for label-count rule execution.

## Input Resolution

If `detections`, `tracks`, or `roi_matches` are missing but the user provided a video, do not ask the user to provide them. Extract timestamped frames first with `analyze-video/scripts/extract_frames.py` or `frame-sampling/scripts/run.py`, inspect the frames visually, and identify object groups, contact, distance, orientation, and interaction. Use object detection/tracking only as optional support.

## LLM Visual Workflow

1. Identify required subject groups from the event request or template.
2. Inspect frames for co-occurrence, proximity, contact, collision, carrying/placing objects, group movement, or other visual relations.
3. Compare adjacent frames to distinguish static co-presence from interaction.
4. Record subject descriptions, relation, timestamps, evidence frame ids, and confidence.
5. Mark as ambiguous when subjects are occluded, too small, or the relation cannot be visually confirmed.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python object-composition-event/scripts/run.py --detections-json <detections.json> --tracks-json <tracks.json> --required-json '[{"labels":["person"],"min_count":2}]' --output <method_result.json>
```

Parameters: `--detections-json`, `--tracks-json`, `--roi-matches-json`, `--required-json`, `--group-by`, `--spatial-relation`, `--max-distance-pixels`, `--method-config`, `--output`.

## Workflow

1. Read required label groups, minimum counts, spatial relation, and grouping mode.
2. Review extracted frames to identify visual groups and relationships.
3. Optionally use detections/tracks for counts and rough positions.
4. Return groups with subject descriptions or object ids, labels, relation, ROI id, confidence, and evidence frame ids.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `method_config.required`
- `method_config.spatial_relation`
- `method_config.max_distance_pixels`
- `method_config.group_by`
- `detections`
- `tracks`
- `roi_matches`

## Outputs

Returns `method="object_composition"`, `matched`, and `groups`.

## Failure Modes

Returns `matched=false` when required label counts or spatial relation rules are not satisfied.

## Constraints

Do not decide final business semantics without template mapping. Do not classify interactions such as fighting or collision from labels alone without visual action evidence.
