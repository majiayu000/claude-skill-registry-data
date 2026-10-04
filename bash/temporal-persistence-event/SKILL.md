---
name: temporal-persistence-event
description: Determine whether a visually observed object, action, or scene state persists long enough to count as sustained occupancy or anomaly through extracted-frame LLM review. Use for lingering, illegal parking, fallen person, congestion, crowding, smoke/fire, blockage, or other temporal video event evidence.
---

# Temporal Persistence Event

## Execution Priority

Prioritize extracted-frame visual analysis. Call `scripts/run.py` only when reliable tracks already exist or the user explicitly asks for track-based duration checks.

## Input Resolution

If `tracks` are missing but the user provided frames or a video, do not ask the user to provide tracks. Extract timestamped frames first with `analyze-video/scripts/extract_frames.py` or `frame-sampling/scripts/run.py`, then visually compare adjacent timestamps to decide whether the same state persists. Use detection/tracking scripts only as optional support.

## LLM Visual Workflow

1. Identify the target state, for example stopped vehicle, person lying down, crowd remains, smoke continues, road blockage, or intrusion.
2. Review timestamped frames in order and note when the state first appears, continues, changes, and ends.
3. Estimate duration from visible evidence timestamps, not from a single frame.
4. Allow small gaps only when adjacent frames strongly show the same state before and after the gap.
5. Return matched=false or requires_review when identity continuity or visual state continuity is unclear.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python temporal-persistence-event/scripts/run.py --tracks-json <tracks.json> --target-labels person --min-duration-seconds 5 --output <method_result.json>
```

Parameters: `--tracks-json`, `--target-labels`, `--movement-states`, `--min-duration-seconds`, `--method-config`, `--output`.

## Workflow

1. Read target labels, movement states, and minimum duration.
2. Review extracted frames to identify visually persistent subjects or states.
3. Optionally compare track duration when reliable tracks are available.
4. Return method-level matches with subject description or id, duration, state, confidence, evidence frames, and time range.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `method_config.target_labels`
- `method_config.movement_states`
- `method_config.min_duration_seconds`
- `tracks`

## Outputs

Returns `method="temporal_persistence"`, `matched`, and `matches` with `subject_id`, `duration_seconds`, `movement_state`, `confidence`, `start_time`, and `end_time`.

## Failure Modes

Returns `matched=false` when no track reaches the configured duration and movement filters.

## Constraints

Do not perform final event mapping. Do not claim persistence from a single timestamp unless the event template allows single-frame aftermath evidence.
