---
name: on
description: Turn cc-cache-warming back on for THIS session after /cc-cache-warming:off. Use when the user wants the prompt-cache warming re-enabled for the current session.
disable-model-invocation: true
allowed-tools: Bash(bash:*)
---

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cache-warming-ctl.sh" on`

Confirm in one or two lines that warming is on again for this session and
restarts after the next real turn. If the output mentions the global kill
switch, say that `on-all` clears it. Do not run any other command.
