---
name: abandon
description: Harmonia abandon - retire the active task workspace so resolution skips it. Use ONLY when explicitly invoked as /harmonia:abandon.
disable-model-invocation: true
---

This is a human-invoked touchpoint. Retiring a task is the developer's call: no other skill or agent - flow explicitly - runs it or `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh abandon` on the developer's behalf.

Run the abandon subcommand against the active workspace and surface its output verbatim:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh abandon --repo .
```

The script is the single source of truth - it resolves the workspace and writes the retirement marker so resolution skips it. Do not fork its logic; report what it prints.
