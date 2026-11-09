---
name: codex-list
description: List this Claude session's retained Codex runs (the runner's --list --mine) without touching them or starting any process.
disable-model-invocation: true
allowed-tools: 'Bash(node "${CLAUDE_PLUGIN_ROOT}/run-codex-task.mjs" --list --mine)'
---

!`node "${CLAUDE_PLUGIN_ROOT}/run-codex-task.mjs" --list --mine || echo "codex-list: the runner exited with an error"`

Show the output above to the user exactly as it is, in one code block, and add nothing else.
