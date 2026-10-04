---
name: neatcontext-mode
description: Show or set NeatContext routing to auto, ask, or manual for the current Kimi Code session, with an optional global default for new sessions. Use only when the user explicitly invokes this skill or clearly asks to change routing behavior.
---

# Routing mode

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation.

Accept only no mode, exactly one of `auto`, `ask`, or `manual`, and an optional explicit request to make it the global default. Reject other values without running them.

Run one of:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" mode
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" mode <auto|ask|manual>
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" mode <auto|ask|manual> --global
```

Relay the CLI output. Do not switch contexts as part of this workflow.
