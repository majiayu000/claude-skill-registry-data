---
name: bookmarks
description: "Bookmark and organize favorite notes"
source: bookmarks
---

# Bookmarks

## Plugin metadata

- **id:** `bookmarks`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `bookmarks:bookmark-current-view` -- Bookmark current view
- `bookmarks:unbookmark-current-view` -- Remove current bookmark

Plugin "Bookmarks" (formerly Starred) manages favorite notes.

Available commands:
- bookmarks:bookmark-current-view -- Add the current note or view to bookmarks
- bookmarks:unbookmark-current-view -- Remove the current note from bookmarks

Use this skill when the user wants to bookmark or unbookmark notes.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/bookmarks.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/bookmarks.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/bookmarks.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/bookmarks.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
