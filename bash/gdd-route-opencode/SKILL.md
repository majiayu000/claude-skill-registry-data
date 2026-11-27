---
name: gdd-route-opencode
description: >-
  Configure the OpenCode headless route for gdd's shared runner. Use for
  route configuration and troubleshooting, not for interactive sessions or
  the overall delivery protocol.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "OpenCode standalone server route with session resume and model variant selection"
  summary_zh: "OpenCode 独立服务器路由，支持会话恢复和模型变体选择"
  kind: "mechanism"
---

# gdd-route-opencode

Requires [gdd](../gdd/SKILL.md) and the OpenCode CLI in PATH, or an executable
path in `OPENCODE_BIN`. Install both skills in the same skills root. Select
`GDD_AGENT=opencode` for gdd stages, or pass `--agent opencode` to
[gdd's runner](../gdd/scripts/agent_run.py).

Verified on OpenCode 2.3.0. The route runs
`run --standalone --format json --auto`, taking the prompt as the last argv
element. The private standalone server lives inside the agent process tree
so the runner can stop it with the run. Exit 0 also requires the last
`step_finish` reason to be `stop` with no error event.

- `--resume ID` maps to `-s ID`. A model maps to `-m MODEL`; if thinking is
  set, it becomes `-m MODEL#VARIANT`. Thinking without a model is rejected
  before a run directory is created. For `gdd.py stage`, these values come
  from `GDD_MODEL` and `GDD_THINKING` when set.
- On Windows, use a native executable for multiline prompts; the shared runner
  refuses newlines or shell metacharacters in argv passed to a batch shim.
- There is no native schema flag in this route: the stage prompts for JSON
  and the runner validates the result.

See [gdd transport](../gdd/references/transport.md) for detach, logs and
recovery. Check the stage result and run the repository's gates independently.
