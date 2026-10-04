---
name: random-note
description: "Open a random note from the vault"
source: random-note
---

# Random Note

## Plugin metadata

- **id:** `random-note`
- **source:** core
- **plugin-type:** core
- **status:** disabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `random-note:open` -- Open random note

Plugin "Random Note" opens a randomly selected note.

Available commands:
- random-note:open -- Open a random note from the vault

Use this skill when the user wants to explore their vault randomly or asks for a surprise note.

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.

## Configuration File

Settings path: `.obsidian/random-note.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/random-note.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/random-note.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/random-note.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
