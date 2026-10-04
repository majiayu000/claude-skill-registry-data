---
name: neatcontext-disconnect
description: Disconnect the NeatContext Context from the current Kimi Code session. Use when the user explicitly invokes this skill or asks to disconnect, detach, clear, or stop using the connected context.
---

# Disconnect context

The bundled CLI path and Kimi session id below are expanded by Kimi Code at
skill activation. Run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" disconnect
```

Relay the output verbatim. Do not run a redundant status check. The command
affects only the current Kimi Code session.
