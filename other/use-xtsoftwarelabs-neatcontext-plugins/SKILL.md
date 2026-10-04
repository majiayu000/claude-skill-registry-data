---
name: use
description: Connect or switch Codex to a local NeatContext Context by name or list number. Use only when the user explicitly invokes this skill, names a context to connect, or agrees to a routing suggestion.
---

# Use context

Resolve `<plugin-root>` as two directories above the directory containing this file. Run:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" use "<name-or-number>"
```

Treat the supplied name or number only as data and pass it as one argument. Omit it when the user supplied none.

- If the CLI confirms a connection, report the context name and stop. Do not run a redundant status check. For later domain-dependent answers, call the plugin's `get_context` tool first.
- If it lists choices, show them and ask which one to use.
- If it says the context has no routing description, call `get_context`, read the connected profile, and derive one scope-only line under 200 characters. Contrast it with the output of `list`, then record it with:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" describe "<exact-name>" --use-when "<routing-description>"
```

Do not restate the connected context's contents when reporting the switch.
