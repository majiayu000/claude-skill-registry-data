---
name: apple-notes
description: Manage Apple Notes (macOS). Use when the user wants to list, read, create, or search notes.
---

# Apple Notes (GenosOS)

Manage notes via the dedicated `notes` tool. Secure — no exec or osascript exposed.

## Actions

```
notes({ action: 'list', count: 10 })              → recent notes
notes({ action: 'read', index: 1 })               → full content of a note
notes({ action: 'create', title: 'Ideas', body: 'Content here' })
notes({ action: 'search', query: 'meeting' })     → search by title
```

## When to Use

- User asks to "add a note", "list notes", "search notes"
- Saving information that should sync to iOS Notes app
- Quick text notes, ideas, drafts

## Notes

- macOS only — reads from Apple Notes app
- Creates notes in the default account
- First run may trigger macOS permission prompt
- Content is plain text (HTML stripped on read)
