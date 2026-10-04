---
name: comfyui-discover
description: Inspect a live ComfyUI server for version, hardware, feature flags, queue depth, installed node schemas, model categories, and model filenames before selecting or validating a workflow.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# ComfyUI Discover

## Read

- `../../references/COMFYUI_OPERATIONS.md`
- `../../references/COMFYUI_NATIVE_API.md`

## Procedure

1. In Pi, begin with `story_comfy action=server-info`. Do this before any shell, filesystem, or guessed-path attempt to locate ComfyUI.
2. If the Story-Film project is a child of Pi's current working directory, pass `project=<project-root>` to project-scoped `story_comfy` actions. Project creation does not change Pi's working directory.
3. Use the user-supplied server URL when present. Otherwise use the configured environment URL or loopback default.
4. Probe the server before doing generation work.
5. Read system stats and features.
6. Query exact node classes or filtered node catalog only when the task needs them. In Pi use `story_comfy action=node-search` or `action=node-info`.
7. Before building a workflow, run the bundled workflow catalog. In Pi use `story_comfy action=workflow-catalog`. It reads only Story-Film's `comfyui_workflows/` directory: built-ins plus `custom/<task>/<model>/`.
8. Query model categories and filenames only when model availability matters. In Pi use `story_comfy action=model-inventory` and `action=model-search`. The server registries include model roots registered through `extra_model_paths.yaml`.
9. Use `/object_info` through Story-Film's managed/native control layer for node schemas. Its node input schema is under `input.required` and `input.optional`. Do not treat an empty result from an incorrectly parsed `inputs` field as evidence that models are missing.
10. Save a project snapshot to `04_generation/comfyui/server_snapshot.json` when reproducibility or later diagnosis benefits.

Bundled commands:

```text
python scripts/comfyui_control.py probe
python scripts/comfyui_control.py nodes --query <term>
python scripts/comfyui_control.py models
python scripts/workflow_catalog.py catalog PROJECT --query <term>
python scripts/comfyui_control.py models --folder <category>
```

## Do not

- use Bash, `find`, `ls`, `which`, `locate`, directory globbing, home-directory scans, or guessed personal paths to locate ComfyUI or model files; use `story_comfy` and the live server registry instead
- infer that ComfyUI is absent from a failed `cd`, a missing guessed directory, or a failed filesystem search
- infer that models are absent from an empty guessed `checkpoints`, `vae`, `loras`, `unet`, or `diffusion_models` directory
- invoke managed comfy-cli discovery commands directly through Bash when `story_comfy` can perform the operation
- write one-off model inventory scripts or raw `/models` curl loops when `model_inventory.py` is available; use the bundled inventory tool for Story-Film model selection
- search `/workflow_templates`, `/userdata`, ComfyUI saved workflows, project workflow folders, or arbitrary external paths for selectable workflows; custom workflow JSON must be copied into `comfyui_workflows/custom/<task>/<model>/`
- write one-off `/object_info` or `/prompt` parsers/loops when the bundled controller already owns live validation and execution
- infer that models are absent because they are outside the ComfyUI application directory
- create mock media or download substitute models when discovery is incomplete
- assume a custom node exists from an online workflow
- treat a stale saved snapshot as current capability data
- guess model filenames from model family names

## Done

The next step has live evidence for the server, required node classes, and relevant models instead of assumptions.
