---
name: neatcontext-delete
description: Preview and permanently delete a NeatContext context while preserving any externally linked knowledge folder. Use only when the user explicitly invokes this skill or clearly asks to delete a context.
---

# Delete context

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation.

List contexts first:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" list
```

If the requested name is missing or does not resolve to exactly one context, show the list and ask which one. Never guess.

Preview the deletion without changing anything:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" delete "<exact-name>"
```

Relay exactly what the preview says will be removed or retained and wait for explicit confirmation.

After confirmation, run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" delete "<exact-name>" --yes
```

Relay the result. If it was connected, say that this session is no longer grounded and suggest `/neatcontext:use`.
