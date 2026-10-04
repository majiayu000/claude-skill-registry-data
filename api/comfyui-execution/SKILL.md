---
name: comfyui-execution
description: Submits ComfyUI workflows via POST /prompt, subscribes to /ws for execution events, fetches results from /history, and supports targeted reruns via partial_execution_targets. Use when an agent needs to run, observe, interrupt, or partially re-execute a ComfyUI prompt.
---

# comfyui-execution

The **only** Skill in the system that speaks raw HTTP + WebSocket to ComfyUI.
Every other Skill (capability Skills, planner, repair, checkpoint) ultimately
calls the scripts bundled here.

## When to use

- Submitting a prompt JSON to a running ComfyUI backend
- Subscribing to execution events (`executing`, `progress`, `executed`,
  `execution_error`, `execution_interrupted`) for ReAct repair
- Fetching results for a `prompt_id` from `/history`
- Re-running only specific output nodes via `partial_execution_targets`
- Interrupting a running prompt (global or by `prompt_id`)
- Discovering node schemas from `/object_info` (cached)
- Releasing VRAM with `/free`

**Do not** use this Skill to author prompt JSON — capability Skills
(`generating-images`, `inpainting-regions`, …) produce prompts via template +
patch and then pipe the JSON into `scripts/submit_prompt.py`.

## Configuration

- `COMFYUI_BASE_URL` env var (default `http://127.0.0.1:8188`)
- `COMFYUI_WS_URL` env var (default `ws://127.0.0.1:8188/ws`)
- Object-info cache: `ComfyUI-Agent/host/.cache/object_info.json`

No API key. No custom_node install. The host talks to ComfyUI as an external
HTTP service; this is a hard boundary — see `CLAUDE.md` anti-patterns.

## Bundled files (table of contents)

### `reference/`

| File | What it documents |
|---|---|
| `reference/api.md` | Endpoint catalog mirroring `ComfyUI_workflow.md §2` — every HTTP surface the scripts here wrap. |
| `reference/error-payloads.md` | `node_errors` (pre-execution) schema + `execution_error` (runtime WS) 7-field payload. Read this before touching `repairing-workflows`. |

### `scripts/`

All scripts are runnable standalone. They exit non-zero only on transport-layer
failures; protocol errors are returned as JSON on stdout.

| Script | Wraps | Input | Output |
|---|---|---|---|
| `submit_prompt.py` | `POST /prompt` | stdin JSON `{prompt, prompt_id?, client_id?, extra_data?, partial_execution_targets?}` | `{prompt_id, number, node_errors}` on success, `{error, node_errors}` on validation failure |
| `subscribe_ws.py` | `GET /ws` (WebSocket) | `--client-id` flag; optional `--prompt-id` filter (see notes below) | one JSON line per event to stdout; exits when the filtered prompt reaches `executing` with `node=null` / `execution_error` / `execution_interrupted` |
| `get_object_info.py` | `GET /object_info` | optional `--node-class` | JSON on stdout. Filesystem-cached; invalidated when ComfyUI restart is detected. Cache path overridable via `COMFYUI_AGENT_OBJECT_INFO_CACHE`. Cache-write failures log to stderr and still emit a single JSON document on stdout. |
| `get_history.py` | `GET /history/{prompt_id}` | `--prompt-id` | `{outputs, meta}` on stdout |
| `interrupt.py` | `POST /interrupt` | optional `--prompt-id` for targeted cancel | `{ok: true}` or `{error}` |
| `free.py` | `POST /free` | none | `{ok: true}` or `{error}` |

> **`subscribe_ws.py` terminal event**: the ComfyUI protocol signals "graph
> finished" with an `executing` frame whose `data.node` is `null` (not an
> `executed` frame — that is a per-node progress event). The script
> therefore exits on the first of: `executing` with `node=null` for the
> target prompt, `execution_error`, or `execution_interrupted`. See
> `scripts/subscribe_ws.py::_is_prompt_terminal`.
>
> **`--prompt-id` filter semantics**: when a prompt id is supplied the
> filter passes through (a) per-prompt frames whose `data.prompt_id`
> matches, **plus** (b) global frames with no `data.prompt_id` at all
> (e.g. `status` queue-depth, `crystools.*` telemetry). Frames belonging
> to a different prompt are dropped. Global frames are kept because they
> carry session-level signal the host still needs.

## Typical call sequences

### One-shot txt2img

```
compile.py (capability Skill) → prompt.json
  → submit_prompt.py < prompt.json     # returns {prompt_id}
  → subscribe_ws.py --prompt-id $ID    # stream events until executed
  → get_history.py --prompt-id $ID     # fetch outputs
```

### ReAct repair loop

```
submit_prompt.py        # node_errors non-empty → feed to repairing-workflows
  or
subscribe_ws.py         # execution_error event → feed {node_id, exception_message, current_inputs} to repair
  → repairing-workflows patches prompt.json
  → submit_prompt.py with partial_execution_targets=[affected_output_node]
```

## Error handling contract

Every script must:

- Handle network errors (connection refused, timeout, DNS) explicitly and
  return `{error: {type, message}}` on stdout.
- Handle missing files / missing `prompt_id` explicitly.
- **Never** return a raw Python traceback to the caller.
- **Never** silently swallow an `execution_error` WS event — see
  `CLAUDE.md` anti-pattern "every `execution_error` must reach the repair loop".

## References

- `knowledge/workflows/ComfyUI_workflow.md` §2 (control surface), §3 (prompt
  JSON shape), §4.1 (submission flow), §4.4 (WebSocket events), §5
  (`/object_info` fields)
- `knowledge/plans/v1/plan_v1.md` §6 Group A (this Skill's description),
  §7 (integration contract)
- `knowledge/plans/v1/todo.md` §4 (Stage 1 tasks and acceptance)
