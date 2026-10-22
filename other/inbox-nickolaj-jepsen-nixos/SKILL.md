---
name: inbox
description: Triage the vault's Inbox by proposing a folder, name, frontmatter and links for each note, then filing the ones I approve. Use when asked to process, triage or file the inbox.
---

# Inbox triage

1. List `Inbox/*.md`, plus any stray `.md` at the vault root other than `AGENTS.md`.
   Read each one.
2. Decide for each note, following `AGENTS.md`:
   - the destination (folder, or a project's sub-folder), or "leave" if it isn't ready;
   - a new file name only if the current one is `Untitled…` or unclear
     (meetings: `YYYY-MM-DD Topic`);
   - the frontmatter to add or fix, including a one-line `summary`;
   - links to notes that already exist (check each target);
   - whether it's really two notes: say so, don't split it.
3. Show one table: note | new path | frontmatter changes | links | doubts. Then stop
   and wait; I may approve all rows, some, or amend them.
4. For approved rows, edit frontmatter and links first, then move with
   `obsidian-cli vault=notes move path="Inbox/<name>.md" to="<Folder>/<new name>.md"`. If Obsidian
   isn't running, make the edits and list the moves for me instead.
5. Run `obsidian-vault-check`, fix what you caused, and finish with `git status --short`.
