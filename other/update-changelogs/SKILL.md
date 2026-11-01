---
name: update-changelogs
description: Updates changelogs for all packages with consumer-facing changes.
---

When asked to update changelogs, follow these steps:

1. Read the instructions in [`docs/contributing/updating-changelogs.md`](../../../docs/contributing/updating-changelogs.md) and follow them to the letter.
2. Run the prose pass over the entries you drafted: Skill tool with skill="prose-pass", args="changelogs". Apply its cuts before committing.
3. Commit the changes to the current branch with the commit message "docs: Update changelogs" before creating the PR.
4. Return the commit hash and the commit message.
