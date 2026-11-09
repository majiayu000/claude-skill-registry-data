---
name: codex-limits
description: Show the remaining Codex quota on one line (the runner's --limits). Starts one probe app-server for about 1-2 s, with no thread and no Codex model call.
disable-model-invocation: true
allowed-tools: 'Bash(node "${CLAUDE_PLUGIN_ROOT}/run-codex-task.mjs" --limits)'
---

!`node "${CLAUDE_PLUGIN_ROOT}/run-codex-task.mjs" --limits || echo "codex-limits: the runner exited with an error"`

Show the output above to the user exactly as it is, in one code block, and add nothing else.
