---
name: neatcontext-create
description: Create a fresh NeatContext context from a user-defined behavioral profile and an existing local knowledge folder. Use only when the user explicitly asks to create a new context, or runs /neatcontext-create — not to save the current conversation.
---

# Create context

Keep this workflow distinct from `neatcontext-save`: create starts from a purpose
the user states and a knowledge folder they already have; save distills work
already visible in the conversation.

Collect these inputs, asking one question at a time and only for information the
user has not already supplied:

1. What the context covers, what you should do and avoid on it, and how you
   should behave.
2. The absolute path to an existing folder containing its knowledge.
3. A short context name.

The folder is linked read-only. NeatContext never writes into it.

## Draft

Run `/neatcontext-list`, or call `preview_context` on anything adjacent, before
drafting — the routing description has to distinguish this context from the ones
that already exist.

Draft a Markdown profile beginning with `# <name>` and containing `## Purpose`,
`## What to do`, `## What to avoid`, and `## Behavior`. Preserve the user's
meaning and add no rules they did not ask for.

Draft one routing description under 200 characters. Describe scope only —
systems, symptoms, repos, ticket prefixes, and terminology someone would
actually type. Make it contrastive with the existing contexts. Never include
tone, behavior, or output-format instructions: that line is read while *other*
contexts are connected.

Show both drafts and wait for confirmation.

## Apply

After confirmation, call the `neatcontext_create` tool with `name`,
`knowledgeFolder`, `profile`, and `useWhen`. Pass the profile Markdown directly —
there is no scratch file to write and nothing to clean up.

On Windows, strip a trailing backslash from the knowledge-folder path first.

Relay the result. Do not connect the new context automatically.
