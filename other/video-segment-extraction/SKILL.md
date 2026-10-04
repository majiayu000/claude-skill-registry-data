---
name: video-segment-extraction
description: Extract playable short video evidence clips around event times. Use when Codex has event_id, camera_id, raw_segment_uri, event_time, event_elapsed_seconds, pre_seconds, or post_seconds and needs an MP4 clip URI plus clip time range. This skill exposes FFmpeg-backed clipping for real local videos and memory-backed synthetic clips for tests.
---

# Video Segment Extraction

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If event timing is missing but the user provided a video analysis request, do not write custom clipping code. First call upstream event skills, especially `event-rule-engine/scripts/run.py`, to produce an event with `event_time` or `event_elapsed_seconds`; then call this skill with `raw_segment_uri`, `event_id`, and the pre/post window.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python video-segment-extraction/scripts/run.py --event-id <event_id> --raw-segment-uri <video.mp4> --event-time <iso_time> --event-elapsed-seconds <seconds> --config <config.json> --output <clip.json>
```

Parameters: `--event-id`, `--raw-segment-uri`, `--event-time`, `--start-time`, `--event-elapsed-seconds`, `--pre-seconds`, `--post-seconds`, `--output-dir`, `--config`, `--output`.

## Workflow

1. Read event id, source segment, event time, and pre/post window.
2. Locate the source media range.
3. Clip or synthesize a short segment in a playable format.
4. Store and return the clip URI and time range.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

Required:
- `event_id`
- `event_time` or `start_time`

Common fields:
- `camera_id`
- `raw_segment_uri`
- `event_elapsed_seconds`
- `pre_seconds`
- `post_seconds`

## Outputs

Returns `event_id`, `clip_uri`, `start_time`, and `end_time`.

## Failure Modes

- `MISSING_EVENT`
- `FFMPEG_CLIP_FAILED`

## Constraints

Do not decide whether an event occurred. Do not modify event confidence.
