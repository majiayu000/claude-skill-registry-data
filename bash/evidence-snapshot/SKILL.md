---
name: evidence-snapshot
description: Generate snapshot evidence for video monitoring event candidates. Use when Codex has an event, event_id, evidence_frame_ids, image_uri, or frame list and needs a snapshot URI, SHA-256 integrity hash, created_at timestamp, privacy masking status, and Evidence schema output.
---

# Evidence Snapshot

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If `event` or `frames` are missing but the user provided a video or event analysis request, do not ask the user to provide evidence frames and do not write custom snapshot code. First call upstream skills to produce frames and events: `frame-sampling/scripts/run.py`, `object-detection/scripts/run.py`, `object-tracking/scripts/run.py`, `roi-mapping/scripts/run.py`, and `event-rule-engine/scripts/run.py` as needed. Then call this skill using the event's `evidence_frame_ids` and available frames.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python evidence-snapshot/scripts/run.py --event-json <event.json> --frames-json <frames.json> --config <config.json> --output <evidence.json>
```

Parameters: `--event-json`, `--frames-json`, `--output-dir`, `--sensitive-regions-json`, `--config`, `--output`.

## Workflow

1. Select the most relevant evidence frame from the event or input frames.
2. Copy the source frame into evidence storage.
3. Call privacy masking when enabled.
4. Compute SHA-256 integrity hash.
5. Return Evidence schema.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `event` or top-level event fields
- `frames`
- Required event field: `event_id`
- Useful event fields: `evidence_frame_ids`, `image_uri`

## Outputs

Returns `evidence_id`, `event_id`, `type=snapshot`, `uri`, `hash`, `created_at`, and `privacy_masked`.

## Failure Modes

- `MISSING_EVENT_ID`
- Propagates `privacy-masking` failures only when caller explicitly checks that nested result.

## Constraints

Do not change event confidence or decide review routing.
