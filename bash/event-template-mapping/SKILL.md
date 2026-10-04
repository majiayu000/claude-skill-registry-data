---
name: event-template-mapping
description: Map LLM visual observations or method-level event results into final video monitoring Event Candidate semantics. Use when Codex has frame observations, visual timeline, template_name, template config, method_results, camera_id, score_policy, or review_threshold and needs event_type, confidence, severity, reason, evidence frames, and review flags.
---

# Event Template Mapping

## Execution Priority

Prioritize mapping visual observations into event candidates. Call `scripts/run.py` only when structured `method_results` already exist or the user explicitly asks for template-rule execution.

## Input Resolution

If `method_results` are missing but frame observations are available, map the visual observations directly into event candidates. If both visual observations and structured method results are missing, first extract and review frames through `analyze-video` or `frame-sampling`, then call the relevant method-level event skill instructions. Do not invent final event semantics from the user request alone.

## LLM Visual Mapping Rules

1. Use the visual timeline as the primary evidence source.
2. Select the event template whose preconditions are visibly satisfied.
3. Generate `reason` from concrete observations: subjects, action/state, location, timestamps, and frame ids.
4. Set confidence from evidence quality, temporal consistency, and template fit.
5. Set `requires_review=true` when the event is serious but visually ambiguous, when frames are sparse, or when only aftermath is visible.


## Atomic CLI

Run this skill directly with its own script. The script does not call other skill scripts and does not depend on shared `src`, `tools`, or registry modules.

```bash
python event-template-mapping/scripts/run.py --method-results-json <method_results.json> --template-name <template_name> --camera-id <camera_id> --config <config.json> --output <event.json>
```

Parameters: `--method-results-json`, `--template-json`, `--template-name`, `--camera-id`, `--config`, `--output`.

## Workflow

1. Read template name, join policy, score policy, visual observations, and method results.
2. Check whether the visible evidence satisfies required event semantics.
3. Compute event confidence and review status.
4. Return a standard Event Candidate schema with evidence frame ids and visual reason.

## Available Implementation

This skill is implemented as an atomic standalone script in its own `scripts/run.py`. The script contains the executable logic for this skill and must not import shared `src`, `tools`, or registry modules.

## Inputs

- `template_name`
- `template`
- `method_results`
- `camera_id`

## Outputs

Returns `matched=true` plus Event Candidate fields, or `matched=false`.

## Failure Modes

Returns `matched=false` when join policy fails or score is below `score_policy.min_score`.

## Constraints

Do not generate evidence files. Do not map an event type when the frame evidence does not visibly support it.
