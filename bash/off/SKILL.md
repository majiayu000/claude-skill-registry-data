---
name: off
description: Turn cc-cache-warming off for THIS session only; other and future sessions keep running. Use when the user wants to stop the prompt-cache warming pings for the current session.
disable-model-invocation: true
allowed-tools: Bash(bash:*)
---

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cache-warming-ctl.sh" off`

Confirm in one or two lines that warming is off for this session only (a ping
already queued will be refused by the prompt hook). Mention that
`/cc-cache-warming:on` turns it back on, and that the script also takes
`off-all` / `on-all` for every session. Do not run any other command.
