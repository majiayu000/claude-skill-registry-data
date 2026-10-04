---
name: delete
description: Preview and permanently delete a NeatContext context while preserving any externally linked knowledge folder. Use only when the user explicitly invokes this skill or clearly asks to delete a context.
---

# Delete context

Resolve `<plugin-root>` as two directories above the directory containing this file.

List contexts first:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" list
```

If the requested name is missing or does not resolve to exactly one context, show the list and ask which one. Never guess.

Preview the deletion without changing anything:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" delete "<exact-name>"
```

Relay exactly what the preview says will be removed or retained and wait for explicit confirmation.

After confirmation, run:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" delete "<exact-name>" --yes
```

Relay the result. If it was connected, say that this thread is no longer grounded and suggest `$neatcontext:use`.
