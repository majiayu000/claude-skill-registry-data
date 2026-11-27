---
name: gdd-route-pi
description: >-
  Configure the Pi headless route for gdd's shared runner. Use for
  route configuration and troubleshooting, not for interactive sessions or
  the overall delivery protocol.
disable-model-invocation: true
metadata:
  revision: "6"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "Pi stdin and JSON event route with session resume"
  summary_zh: "Pi stdin 与 JSON 事件路由，支持会话恢复"
  kind: "mechanism"
---

# gdd-route-pi

Requires [gdd](../gdd/SKILL.md) and the Pi CLI in PATH, or an executable
path in `PI_BIN`. Install both skills in the same skills root. Select
`GDD_AGENT=pi` for gdd stages, or pass `--agent pi` to
[gdd's runner](../gdd/scripts/agent_run.py).

Verified on Pi 1.5.2. The route reads the prompt from stdin and runs
`--mode json --no-approve`. Pi has no tool approval prompts; `--no-approve`
skips unapproved project-local files and is not a sandbox.

- `--model` and `--thinking` (or `GDD_MODEL` and `GDD_THINKING` on `gdd.py stage`)
  pass through only when set; `--resume ID` maps to `--session ID`.
- Exit 0 also requires a last assistant `message_end.stopReason` other than
  `error`, `aborted`, or `length`. An aborted settlement is a failure even
  after an assistant stop.
- There is no native schema flag in this route: the stage prompts for JSON
  and the runner validates the result.

See [gdd transport](../gdd/references/transport.md) for detach, logs and
recovery. Check the stage result and run the repository's gates independently.

For timeouts, isolation, gates and brief shape when the model is DeepSeek, read
[DeepSeek workers](references/deepseek-workers.md).
