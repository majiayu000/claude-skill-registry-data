---
name: gdd-route-copilot
description: >-
  Configure the GitHub Copilot CLI headless route for gdd's shared runner.
  Use for route configuration and troubleshooting, not for interactive
  sessions or the overall delivery protocol.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "GitHub Copilot CLI prompt and JSONL result route with session resume"
  summary_zh: "GitHub Copilot CLI prompt 与 JSONL 结果路由，支持会话恢复"
  kind: "mechanism"
---

# gdd-route-copilot

Requires [gdd](../gdd/SKILL.md) and an authenticated GitHub Copilot CLI in
PATH, or an executable path in `COPILOT_BIN`. On Windows use the real
`copilot.exe`, not a batch shim. Install both skills in the same skills root.
Select `GDD_AGENT=copilot` for gdd stages, or pass `--agent copilot` to
[gdd's runner](../gdd/scripts/agent_run.py).

Verified on Copilot CLI 1.0.114. The route sets the working directory through
the runner and sends the prompt with `--prompt`, stdin closed. It disables
`ask_user`, eager PowerShell resolution, and CLI auto-update. `--allow-all`
allows tools, paths and URLs without approval; it is not a sandbox.

- With no override, Copilot selects its own model. Optional `--model` and
  `--thinking` map to `--model` and `--reasoning-effort`, respectively.
- `--resume ID` maps to `--resume ID` with an explicit session ID. Keep
  the original working directory and Copilot configuration for a resume.
- `--output-format json` selects JSONL instead of plain text. The runner
  requires both process exit 0 and a terminal `result.exitCode` of 0; it
  reads answer text from `assistant.message`, not streaming deltas.
- There is no native schema flag in this route: the stage prompts for JSON
  and the runner validates the result.

See [gdd transport](../gdd/references/transport.md) for detach, logs and
recovery. Check the stage result and run the repository's gates independently.
