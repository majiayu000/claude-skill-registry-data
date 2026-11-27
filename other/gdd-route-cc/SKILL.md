---
name: gdd-route-cc
description: >-
  Configure the Claude Code headless route for gdd's shared runner. Use for
  route configuration and troubleshooting, not for interactive sessions or
  the overall delivery protocol.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "Claude Code stream-JSON route with session resume and native JSON schema"
  summary_zh: "Claude Code stream-JSON 路由，支持会话恢复和原生 JSON schema"
  kind: "mechanism"
---

# gdd-route-cc

Requires [gdd](../gdd/SKILL.md) and the Claude Code CLI in PATH, or an executable
path in `CLAUDE_BIN`. Install both skills in the same skills root. Select
`GDD_AGENT=claude` for gdd stages, or pass `--agent claude` to
[gdd's runner](../gdd/scripts/agent_run.py).

Verified on Claude Code 2.1.326. The route runs
`-p --output-format stream-json --verbose --permission-mode bypassPermissions`
and reads the prompt from stdin. Exit 0 also requires the `result` subtype
`success` with `is_error: false`.

- A fresh run gets a UUID via `--session-id`; a continuation uses `--resume ID`.
- `--model` and `--thinking` (or `GDD_MODEL` and `GDD_THINKING` on `gdd.py stage`)
  map to `--model` and `--effort`, only when set.
- Native structured results use inline `--json-schema`. Use a native
  executable on Windows: quotes in the JSON are refused for a batch shim.
- The permission mode bypasses prompts; it is not isolation. When running as
  root, Claude Code requires `IS_SANDBOX=1` for this permission mode.

See [gdd transport](../gdd/references/transport.md) for detach, logs and
recovery. Check the stage result and run the repository's gates independently.
