---
name: gdd-route-omo
description: >-
  Configure the Omo headless route for gdd's shared runner. Use for
  route configuration and troubleshooting, not for interactive sessions or
  the overall delivery protocol.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "Omo stdin and Senpi JSON event route with session resume"
  summary_zh: "Omo stdin 与 Senpi JSON 事件路由，支持会话恢复"
  kind: "mechanism"
---

# gdd-route-omo

Requires [gdd](../gdd/SKILL.md) and the configured Omo CLI in PATH, or an
executable path in `OMO_BIN`. On Windows use the real executable, not a batch
shim. Install both skills in the same skills root. Select `GDD_AGENT=omo` for
gdd stages, or pass `--agent omo` to [gdd's runner](../gdd/scripts/agent_run.py).

Verified with Omo 5.1.72 (Senpi). The route reads the prompt from stdin in
`--print --mode json` and disables extensions and `ask_user`. The built-in
tools do not wait for interactive approval; this is not a sandbox.

- Use the CLI's configured provider credentials and model default; no extra
  route environment is required. An optional `--model` accepts
  `provider/model`, and `--thinking` passes through when set.
- `--resume ID` maps to `--session ID` (session ID or file path). For ID
  lookup, use the same working directory and Omo agent directory.
- Exit 0 requires a last assistant `message_end.stopReason` other than
  `error`, `aborted`, or `length`. An aborted settlement is a failure.
- There is no native schema flag in this route: the stage prompts for JSON
  and the runner validates the result.

See [gdd transport](../gdd/references/transport.md) for detach, logs and
recovery. Check the stage result and run the repository's gates independently.
