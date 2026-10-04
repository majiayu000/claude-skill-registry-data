---
name: backlink
description: "View and navigate backlinks between notes"
source: backlink
---

# Backlinks

## Plugin metadata

- **id:** `backlink`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `backlink:open` -- Open backlinks pane
- `backlink:open-backlinks` -- Open backlinks for current note
- `backlink:toggle-backlinks-in-document` -- Toggle backlinks in document

Plugin "Backlinks" shows which notes link to the current note.

Available commands:
- backlink:open -- Open the backlinks pane in the sidebar
- backlink:open-backlinks -- Open backlinks for the current note
- backlink:toggle-backlinks-in-document -- Toggle inline backlinks at the bottom of the note

Use this skill when the user asks about connections between notes, what links to a specific note, or wants to see the backlink panel. For programmatic backlink analysis, prefer the get_linked_notes tool.

## Configuration File

Settings path: `.obsidian/backlink.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/backlink.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/backlink.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Current Configuration

```
backlinkInDocument: true
```

For full settings, read: `.obsidian/backlink.json`

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/backlink.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
