---
name: codex-doctor
description: Check the Codex CLI, its login, quota and model list, git and the runner's folders (the runner's --doctor --read-only), with no write probe and no Codex model call.
disable-model-invocation: true
allowed-tools: 'Bash(node "${CLAUDE_PLUGIN_ROOT}/run-codex-task.mjs" --doctor --read-only)'
---

!`node "${CLAUDE_PLUGIN_ROOT}/run-codex-task.mjs" --doctor --read-only || echo "codex-doctor: a nonzero exit status; doctor names each problem on a problem= line"`

Show the output above to the user exactly as it is, in one code block, and add nothing else.
