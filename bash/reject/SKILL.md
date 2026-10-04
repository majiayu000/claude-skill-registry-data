---
name: reject
description: Harmonia reject - record that the developer rejected the built work, blocking capture until it is re-accepted or abandoned. Use ONLY when explicitly invoked as /harmonia:reject.
disable-model-invocation: true
---

This is a human-invoked touchpoint. Rejection is a human act: no other skill or agent - flow explicitly - runs it or `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh reject` on the developer's behalf.

`--reason <text>` is required - a reason-less rejection carries no signal. Ask the developer for the reason if they did not give one, then run:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh reject --repo . --reason "<the developer's reason>"
```

Surface the script's output verbatim. The script is the single source of truth - it resolves the workspace, guards the base ref, supersedes any prior acceptance, and writes the `rejected` marker (timestamp, reason, diff digest). A live rejection blocks `/harmonia:capture` through `verify-acceptance` until the developer re-accepts (which supersedes it) or abandons the task. Do not fork its logic.
