---
name: gdd-route-codex
description: >-
  Configure the Codex headless route for gdd's shared runner. Use for
  route configuration and troubleshooting, not for interactive sessions or
  the overall delivery protocol.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "Codex exec and resume route with native JSON schema and integrations off by default"
  summary_zh: "Codex exec 与 resume 路由，支持原生 JSON schema，默认关闭集成"
  kind: "mechanism"
---

# gdd-route-codex

Requires [gdd](../gdd/SKILL.md) and the Codex CLI in PATH, or an executable
path in `CODEX_BIN`. Install both skills in the same skills root. Select
`GDD_AGENT=codex` for gdd stages, or pass `--agent codex` to
[gdd's runner](../gdd/scripts/agent_run.py).

Verified on Codex CLI 0.171.0. The runner invokes `codex exec --json` with the prompt
on stdin (`-`); `--resume ID` maps to `exec resume ... ID -`. Exit 0 also requires
the last turn event to be `turn.completed`. For native structured results the
runner passes `--output-schema FILE`.

**No sandbox or approval prompts.** This route passes
`--dangerously-bypass-approvals-and-sandbox`. A working directory or a Git
worktree does not confine writes; use only for trusted tasks in an externally
isolated environment.

- `--model` and `--thinking` (or `GDD_MODEL` and `GDD_THINKING` on `gdd.py stage`)
  map to `-m` and `-c model_reasoning_effort=LEVEL`. When unset, the route keeps
  the user's provider, model and effort settings.
- The route disables `computer_use`, `browser_use`, `browser_use_external`,
  `in_app_browser`, `remote_plugin`, `image_generation`, `skill_search`,
  `plugins`, `apps` and `memories` by default.
- It does not discard user config. MCP servers remain as configured by the
  user. To disable a configured server for a run, pass for example
  `--extra "-c mcp_servers.example.enabled=false"` to the runner's `start`
  command. Replace `example` with the server name; repeat the `-c` pair for
  each server to disable.

See [gdd transport](../gdd/references/transport.md) for detach, logs and
recovery. Check the stage result and run the repository's gates independently.
