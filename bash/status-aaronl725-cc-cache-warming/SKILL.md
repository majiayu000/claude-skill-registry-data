---
name: status
description: Show whether cc-cache-warming is keeping this session's prompt cache warm, its 6h window, ping counters and verification results. Use when the user asks about cache warming status.
disable-model-invocation: true
allowed-tools: Bash(bash:*)
---

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cache-warming-ctl.sh" status`

Summarise the status above in at most five short lines: on/off, the state and
when the window ends, pings sent vs. the cap, and how many reached each
verification level (Ping Sent / Cache Hit Verified / Main Session Warm
Verified). Do not run any other command.
