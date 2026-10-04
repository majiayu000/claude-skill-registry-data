---
name: human-review-routing
description: Decide whether video monitoring event candidates require manual review. Use after event generation and evidence creation when Codex has event confidence, event_type, review_threshold, camera_health, high_risk_event_types, newly added camera signals, or enforcement-impact flags and needs review queue routing.
---

# Human Review Routing

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## Input Resolution

If event confidence or event fields are missing but the user provided a video analysis request, do not write custom review-routing logic. First call `event-rule-engine/scripts/run.py` and any required upstream skills to produce candidate events, then call this skill for review routing.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python human-review-routing/scripts/run.py --event-json <event.json> --camera-health-json <health.json> --config <config.json> --output <review.json>
```

Parameters: `--event-json`, `--camera-health-json`, `--review-threshold`, `--config`, `--output`.

## Workflow

1. Read event confidence, event type, camera health, and review threshold.
2. Require review for low confidence, high-risk types, degraded cameras, new cameras, or enforcement impact.
3. Return review flag, reasons, threshold, and queue.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `event`
- `camera_health`
- Optional `review_threshold`

Config:
- `default_review_threshold`
- `event_templates.<event_type>.review_threshold`
- `high_risk_event_types`

## Outputs

Returns `event_id`, `review_required`, `reasons`, `review_threshold`, and `queue`.

## Failure Modes

The current implementation tolerates missing optional config and falls back to threshold `0.85`.

## Constraints

Do not merge duplicate events or generate evidence.
