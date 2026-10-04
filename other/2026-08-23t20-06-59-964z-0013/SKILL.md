---
name: app
description: "Core app operations: navigation, delete, reload, sidebars"
source: app
---

# App

## Plugin metadata

- **id:** `app`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `app:delete-file` -- Delete current file
- `app:go-back` -- Navigate back
- `app:go-forward` -- Navigate forward
- `app:reload` -- Reload app
- `app:open-vault` -- Open another vault
- `app:open-settings` -- Open settings
- `app:toggle-left-sidebar` -- Toggle left sidebar
- `app:toggle-right-sidebar` -- Toggle right sidebar

Plugin "App" provides global Obsidian app commands.

Available commands:
- app:delete-file -- Delete the currently active file (moves to trash)
- app:go-back -- Navigate to the previous file in history
- app:go-forward -- Navigate to the next file in history
- app:reload -- Reload the Obsidian app
- app:open-vault -- Open a different vault
- app:open-settings -- Open the Obsidian settings dialog
- app:toggle-left-sidebar -- Show or hide the left sidebar
- app:toggle-right-sidebar -- Show or hide the right sidebar

Note: For programmatic file deletion, prefer the delete_file tool. Use app:delete-file only when the user explicitly wants the native Obsidian delete behavior (trash + UI confirmation).

## Setup Required

Settings are empty. Plugin likely needs configuration via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/app.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/app.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/app.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/app.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
