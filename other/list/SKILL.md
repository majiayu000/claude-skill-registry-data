---
name: neatcontext-list
description: List the local NeatContext Contexts available to the current Kimi Code session. Use when the user asks what contexts exist, what can be connected, or explicitly invokes this skill.
---

# List contexts

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation. Run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" list
```

Relay the output verbatim. Do not reformat or explain its `(none - ...)` notes.

Close with one short line: connect a context with `/neatcontext:use <name>`. Only when both sections are empty, also mention `/neatcontext:create` and `/neatcontext:save`.
