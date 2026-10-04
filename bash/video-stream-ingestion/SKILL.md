---
name: video-stream-ingestion
description: Ingest video monitoring sources and return raw segment/session metadata. Use when Codex needs to connect or normalize RTSP, GB28181, platform API, local MP4, or mock video sources before frame sampling; especially when input includes camera_id, source_type, stream_url, file_path, capture_seconds, or raw_segment_uri. This skill exposes the production Python implementation and FFprobe-backed local-file probing, but must not run vision inference or event logic.
---

# Video Stream Ingestion

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If the user provides a video path, local file, stream URL, or uploaded video, build the input JSON for this skill instead of writing ingestion code. Use a stable default `camera_id` when the user does not provide one, infer `source_type=local_file` for file paths, and pass the path as `file_path`, `stream_url`, or `raw_segment_uri` as appropriate. Only ask the user for clarification when no usable video source can be inferred.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python video-stream-ingestion/scripts/run.py --video <video.mp4> --camera-id <camera_id> --source-type local_file --capture-seconds 10 --config <config.json> --output <result.json>
```

Parameters: `--video`, `--stream-url`, `--camera-id`, `--source-type`, `--capture-seconds`, `--started-at`, `--config`, `--output`.

## Workflow

1. Read camera id, source type, stream URL or local file, and capture duration.
2. Select the source adapter for RTSP, GB28181, API, local file, or mock input.
3. Capture a short segment with timeout and retry-aware failure handling.
4. Store the raw segment and return session metadata.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

Required:
- `camera_id`
- `source_type`: `local_file`, `mock`, `rtsp`, `gb28181`, or `api`

Common fields:
- `stream_url` or `file_path`
- `capture_seconds`
- `started_at`
- `raw_segment_uri`

## Outputs

Returns `raw_segment_uri`, `video_session_id`, `started_at`, `ended_at`, `duration_seconds`, and optional video width/height.

## Failure Modes

- `MISSING_CAMERA_ID`
- `UNSUPPORTED_SOURCE`
- `SOURCE_NOT_FOUND`

## Constraints

Do not detect objects, sample frames, create events, or generate evidence.
