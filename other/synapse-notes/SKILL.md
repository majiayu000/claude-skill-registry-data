---
name: synapse.notes
description: "Save, retrieve, and organise personal notes locally in ~/.synapse/notes/."
version: "1.0.0"
author: "synapse-core"
triggers: ["take a note", "save a note", "note this", "my notes", "show notes"]
model_hint: "casual"
permissions: ["filesystem:write"]
cloud_safe: true
enabled: true
---

# Notes Skill

You are helping the user capture and organise their thoughts as notes.

## When invoked

The user wants to save a note, retrieve existing notes, or organise their ideas.

## How to respond

### Saving a note

1. **Identify the note content** — extract the key thought or information from the user's message.
2. **Confirm the save** — tell the user the note has been recorded (e.g., "Saved! Note titled
   'Project ideas' stored in your notes.").
3. **Suggest a title if none given** — pick a short, descriptive label based on the content.

### Retrieving notes

1. **List available notes** — if the user asks to see their notes, summarise what's stored.
2. **Surface the most relevant ones** — if they're looking for something specific, filter by topic.

## Storage

Notes are stored locally at `~/.synapse/notes/` as plain Markdown files. Each file is named
`YYYY-MM-DD-<slug>.md` for easy sorting. Notes never leave the device — they are fully private.

## Notes

- Keep confirmations short and friendly.
- If the user's note is a list of items, format it as a bulleted list in the saved file.
- Do not add unsolicited commentary on the content of notes — just record them faithfully.
