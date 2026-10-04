---
name: note-composer
description: "Split, merge, and extract content between notes"
source: note-composer
---

# Note Composer

## Plugin metadata

- **id:** `note-composer`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `note-composer:merge-file` -- Merge current file with another file
- `note-composer:split-file` -- Extract selection to new note
- `note-composer:extract-heading` -- Extract heading to new note

Plugin "Note Composer" restructures content across notes.

Available commands:
- note-composer:merge-file -- Merge the current note with another note
- note-composer:split-file -- Extract the selected text into a new note
- note-composer:extract-heading -- Extract a heading and its content into a new note

Use this skill when the user wants to reorganize notes: splitting long notes, merging related notes, or extracting sections. These commands operate on the currently open note in the editor.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/note-composer.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/note-composer.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/note-composer.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/note-composer.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
