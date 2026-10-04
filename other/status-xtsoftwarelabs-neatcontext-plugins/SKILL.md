---
name: neatcontext-status
description: Report the NeatContext context and routing mode active in the current Kimi Code session, including missing-file or stale-routing warnings. Use when the user asks which context is connected or explicitly invokes this skill.
---

# Context status

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation. Run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" status
```

Relay the status concisely. If none is connected, mention `/neatcontext:use`.

If the CLI reports a missing context file or knowledge folder, preserve that warning and its recovery guidance.

If it reports a stale routing description, offer to refresh it. Read the connected profile, derive a fresh scope-only line under 200 characters, and record it with:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" describe "<exact-name>" --use-when "<routing-description>"
```
