---
name: mode
description: Show or set NeatContext routing to auto, ask, or manual for Codex, with an optional default shared with every other NeatContext host. Use only when the user explicitly invokes this skill or clearly asks to change routing behavior.
---

# Routing mode

Resolve `<plugin-root>` as two directories above the directory containing this file.

Accept only no mode, exactly one of `auto`, `ask`, or `manual`, and an optional explicit request to make it the global default. Reject other values without running them.

Run one of:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" mode
node "<plugin-root>/src/codex/neatcontext-cli.mjs" mode <auto|ask|manual>
node "<plugin-root>/src/codex/neatcontext-cli.mjs" mode <auto|ask|manual> --global
```

Relay the CLI output. Do not switch contexts as part of this workflow.
