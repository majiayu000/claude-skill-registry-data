---
name: create
description: Create a fresh NeatContext context from a user-defined behavioral profile and an existing local knowledge folder. Use only when the user explicitly invokes this skill or asks to create a new context rather than save the current conversation.
---

# Create context

Resolve `<plugin-root>` as two directories above the directory containing this file.

Keep this workflow distinct from `$neatcontext:save`: create starts from user-provided purpose and existing knowledge; save distills work already in the conversation.

Collect these inputs, asking one question at a time only for information the user has not already supplied:

1. What the context covers, what Codex should do and avoid, and how it should behave.
2. The path to an existing folder containing its knowledge.
3. A short context name.

Run `list` before drafting so the routing description can distinguish adjacent contexts:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" list
```

Draft a Markdown profile beginning with `# <name>` and containing `## Purpose`, `## What to do`, `## What to avoid`, and `## Behavior`. Preserve the user's meaning and add no unsupported rules.

Draft one routing description under 200 characters. Describe scope only, using systems, symptoms, repos, ticket prefixes, and terminology someone would type. Make it contrastive with existing contexts. Do not include tone, behavior, or output-format instructions.

Show both drafts and wait for confirmation.

After confirmation, write the profile to a unique temporary Markdown file. Prefer a host scratch directory; otherwise use the workspace and remove the file after the CLI finishes. Run:

```text
node "<plugin-root>/src/codex/neatcontext-cli.mjs" create --name "<name>" --knowledge "<folder>" --profile-from "<profile-file>" --use-when "<routing-description>"
```

Pass each value as one argument. On Windows, remove a trailing backslash from the knowledge-folder argument before quoting it.

Relay the result and remove only the temporary profile file. Do not connect the new context automatically.
