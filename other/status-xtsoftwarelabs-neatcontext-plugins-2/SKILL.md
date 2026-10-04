---
name: status
description: Report the NeatContext context and routing mode active in Codex, including missing-file or stale-routing warnings. Use when the user asks which context is connected or explicitly invokes this skill.
---

# Context status

Resolve `<plugin-root>` as two directories above the directory containing this file. Run:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" status
```

Relay the status concisely. If none is connected, mention `$neatcontext:use`.

If the CLI reports a missing context file or knowledge folder, preserve that warning and its recovery guidance.

If it reports a stale routing description, offer to refresh it. Read the connected profile, derive a fresh scope-only line under 200 characters, and record it with:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" describe "<exact-name>" --use-when "<routing-description>"
```
