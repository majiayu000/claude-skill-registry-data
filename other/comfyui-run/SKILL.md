---
name: comfyui-run
description: Execute API-format workflows on ComfyUI, keep prompt IDs, poll authoritative history, inspect queue state, cancel selected runs, free ComfyUI memory, capture errors, and record outputs for story-film production.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# ComfyUI Run

## Read

- `../../references/COMFYUI_NATIVE_API.md`
- `../../references/COMFYUI_OPERATIONS.md`
- `../../references/COMFYUI_SECURITY.md`

## Procedure

1. Probe the intended server.
2. Validate the API workflow when practical.
3. Upload required inputs first.
4. Submit the workflow and retain `prompt_id`. When a stable story-film item is being rendered, pass its ID and append the mapping to the project run index at submit time.
5. For long work, return control to the agent and poll history rather than using one opaque blocking shell command.
6. On failure, retain the server error and node errors.
7. On completion, extract both media outputs and text outputs.
8. Download requested media through the server output endpoint.
9. Write a run record under `04_generation/comfyui/runs/` without credentials.

Bundled commands:

```text
python scripts/comfyui_control.py --project PROJECT submit --workflow WORKFLOW.json --item-id SHOT-001
python scripts/comfyui_control.py wait PROMPT_ID
python scripts/comfyui_control.py queue
python scripts/comfyui_control.py history --prompt-id PROMPT_ID
python scripts/comfyui_control.py cancel PROMPT_ID
python scripts/comfyui_control.py free --unload-models
```

## Cancellation

Prefer targeted job cancellation. Do not clear every queued job to stop one run.

## Paid nodes

If the workflow contains partner/API nodes and execution can consume credits, confirm the intended paid run before submission when the user has not already requested it.

## Done

The exact run has a prompt ID, final state, preserved error details if any, and project-linked outputs.
