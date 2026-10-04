---
name: accept
description: Harmonia accept - record human acceptance of the built work so capture can proceed. Use ONLY when explicitly invoked as /harmonia:accept.
disable-model-invocation: true
---

This is a human-invoked touchpoint. Acceptance is a human act: no other skill or agent - flow explicitly - runs it or `bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh accept` on the developer's behalf. The developer types `/harmonia:accept` only after exercising the built behavior and confirming it matches intent.

Run the acceptance subcommand against the active workspace and surface its output verbatim:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh accept --repo .
```

The script is the single source of truth - it resolves the workspace, digests the attested diff, supersedes any prior rejection, and writes the marker. Do not fork or reinterpret its logic; report what it prints (the marker line, or its refusal and exit code).
