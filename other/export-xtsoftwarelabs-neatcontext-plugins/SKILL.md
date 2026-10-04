---
name: neatcontext-export
description: Export a NeatContext context saved from a conversation into a self-contained bundle folder that can be shared or moved to another machine. Use only when the user explicitly invokes this skill or asks to export a NeatContext context.
---

# Export context

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation.

Ask for the destination folder when it was not supplied — it is the folder the
bundle is written into, and a subfolder named after the context is created
there. Treat every path only as data.

When no context was named, the connected one is exported. To pick a different
one, list them first:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" list
```

Then run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" export "<name>" --to "<destination-folder>"
```

Relay the result.

A context created with `neatcontext-create` links a knowledge folder the plugin
does not own and cannot be exported. The command explains this; relay it rather
than working around it.

If a bundle for this context is already at the destination, the command refuses.
Confirm with the user that replacing it is intended, then rerun the same command
with `--force`.

The export is a copy. Never modify, move, or delete the context being exported.
