---
name: comfyui-cli
description: Use the official comfy-cli safely for ComfyUI workspace discovery, setup, launch and stop, structured JSON automation, workflow execution including UI-format conversion, jobs, uploads, downloads, nodes, models, templates, memory, updates, and approved dependency changes.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# comfy-cli

## Read

- `../../references/COMFYUI_CLI.md`
- `../../references/COMFYUI_SECURITY.md`

## Procedure

1. Detect `comfy` from `COMFY_BIN` or PATH. Do not guess a personal binary path.
2. Ask the installed CLI for help when command syntax is uncertain.
3. Prefer `--json` for machine-readable automation.
4. Resolve the target workspace with `comfy which` or the user's explicit workspace option.
5. Use background launch for an agent-controlled server lifecycle.
6. Probe ComfyUI after launch.
7. Use comfy-cli's run path when a UI-format workflow needs its supported conversion.
8. Keep the prompt ID and use jobs/download for long runs.

Bundled bridge:

```text
python scripts/comfyui_cli_bridge.py info
python scripts/comfyui_cli_bridge.py launch
python scripts/comfyui_cli_bridge.py stop
python scripts/comfyui_cli_bridge.py run --workflow WORKFLOW.json
```

The bridge is intentionally narrow. For commands not wrapped there, inspect the installed CLI help and call `comfy` directly.

## Mutating dependencies

Custom node installs, broad updates, version switching, and model downloads change the execution environment. Require user intent, then restart and revalidate as appropriate.

## Cloud

Do not add `--where cloud` as an automatic fallback. Cloud and partner operations can spend credits.

## Live dependency operations

Use the bridge's read-only model and package discovery before changing the environment:

```text
python scripts/comfyui_cli_bridge.py models-search --text MODEL
python scripts/comfyui_cli_bridge.py node-deps PACK
python scripts/comfyui_cli_bridge.py deps-in-workflow --workflow WORKFLOW.json --out DEPS.json
```

For an approved custom-node or model change, use the guarded bridge command. Never add `--confirm` merely because a command refused to proceed. The user must already have approved that exact environment change.

After a custom-node install, update, reinstall, repair, or dependency installation, restart ComfyUI and run live workflow validation again.
