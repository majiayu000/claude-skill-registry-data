---
name: repairing-workflows
description: Classifies ComfyUI prompt/execution errors and plans a minimal partial rerun. Use whenever a submit_prompt result contains node_errors, or a WebSocket execution_error frame is observed, to decide between parameter patch, link repair, default substitution, or missing-resource resolution before re-running only the affected subgraph via partial_execution_targets.
---

# repairing-workflows

Repair loop for ComfyUI prompts. Consumes the two error channels documented in
`../comfyui-execution/reference/error-payloads.md`:

- **Channel 1** `node_errors` from `POST /prompt` validation
- **Channel 2** `execution_error` frames from `/ws`

Produces a structured repair plan and a `partial_execution_targets` list that
minimises re-execution.

## When this Skill applies

Invoke when **any** of the following is true:

- `submit_prompt.py` stdout contains a non-empty `node_errors`
- `subscribe_ws.py` stdout has an `{"type":"execution_error"}` frame
- A capability Skill's `compile.py` output failed to submit successfully
- A downstream evaluator flagged a run as failed due to an engine error

Do **not** invoke for evaluator "criteria not met" failures — those route to the
planner, not the repair loop.

## Pipeline

1. `scripts/classify_error.py` — reads a unified error envelope on stdin,
   emits an error class ∈ {`link`, `parameter`, `default`, `missing_resource`}
   plus per-class hints.
2. Repair authoring (caller): apply the class-appropriate patch to the prompt
   JSON. Patches are deterministic JSON edits, not LLM-authored graph rewrites.
3. `scripts/plan_partial_rerun.py` — reads `{prompt, failed_node_id,
   output_nodes}` on stdin and emits `{partial_execution_targets}` covering
   only the failing subgraph and its descendants up to output nodes.
4. Re-submit via `comfyui-execution`'s `submit_prompt.py` with the targets.

## Error classes

See `reference/error-classes.md`.

| Class | Trigger | Repair |
|---|---|---|
| `link` | `bad_linked_input`, `return_type_mismatch`, `invalid_prompt` | Fix link tuple or add converter node |
| `parameter` | `exception_during_validation`, `custom_validation_failed`, runtime TypeError/ValueError with named input | Patch parameter value |
| `default` | `required_input_missing` | Supply default from `object_info` |
| `missing_resource` | `value_not_in_list` on a filename field (`ckpt_name`, `lora_name`, `vae_name`, `embeddings`) | Route to setup wizard / list substitution |

Copilot's `debug_agent.py analyze_error_type()` covers three of these.
`missing_resource` is v1-specific and required by the acceptance test.

## Repair strategies

See `reference/repair-strategies.md` for the patch recipes.

## Scripts

- `scripts/classify_error.py` — pure function, stdlib only. Input envelope:

  ```json
  {"channel": "node_errors" | "execution_error", "payload": { ... }}
  ```

  Output:

  ```json
  {"class": "link|parameter|default|missing_resource",
   "node_id": "...", "hint": "...", "input_name": "..."}
  ```

- `scripts/plan_partial_rerun.py` — computes descendants of the failing node in
  the prompt graph up to any node in `output_nodes`, returns their IDs as
  `partial_execution_targets`.

## Explicit error handling

Both scripts must never raise an unhandled exception to the caller. On bad
input they emit `{"error": "...", "code": "..."}` with a non-zero exit code.

## References

- `../comfyui-execution/reference/error-payloads.md`
- `knowledge/workflows/ComfyUI_workflow.md` §3 (partial_execution_targets), §4.4
- `knowledge/plans/v1/plan_v1.md` §6 Group C
