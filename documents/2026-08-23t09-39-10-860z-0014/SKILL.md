---
name: editor
description: "Editor operations: formatting, headings, inserts, folding, view mode"
source: editor
---

# Editor

## Plugin metadata

- **id:** `editor`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `editor:save-file` -- Save current file
- `editor:attach-file` -- Attach file
- `editor:insert-link` -- Insert link
- `editor:insert-callout` -- Insert callout
- `editor:insert-tag` -- Insert tag
- `editor:set-heading-0` -- Set as paragraph (remove heading)
- `editor:set-heading-1` -- Set as heading 1
- `editor:set-heading-2` -- Set as heading 2
- `editor:set-heading-3` -- Set as heading 3
- `editor:set-heading-4` -- Set as heading 4
- `editor:set-heading-5` -- Set as heading 5
- `editor:set-heading-6` -- Set as heading 6
- `editor:rename-heading` -- Rename heading
- `editor:toggle-bold` -- Toggle bold
- `editor:toggle-italic` -- Toggle italic
- `editor:toggle-code` -- Toggle inline code
- `editor:toggle-highlight` -- Toggle highlight
- `editor:toggle-strikethrough` -- Toggle strikethrough
- `editor:fold-all` -- Fold all headings and lists
- `editor:unfold-all` -- Unfold all headings and lists
- `editor:toggle-source` -- Toggle reading/source view

Plugin "Editor" provides text editing commands for the active note.

Available commands:
- editor:save-file -- Force-save the current file
- editor:attach-file -- Open the attachment picker to embed a file
- editor:insert-link -- Insert a wikilink or markdown link
- editor:insert-callout -- Insert a callout block (> [!type])
- editor:insert-tag -- Insert a tag (#tag)
- editor:set-heading-0..6 -- Set the current line to paragraph (0) or heading level 1-6
- editor:rename-heading -- Rename a heading and update all links pointing to it
- editor:toggle-bold/italic/code/highlight/strikethrough -- Toggle formatting on selection
- editor:fold-all -- Collapse all foldable sections
- editor:unfold-all -- Expand all foldable sections
- editor:toggle-source -- Switch between source/live-preview and reading view

Note: These commands operate on the currently active editor. For programmatic content changes, prefer edit_file or append_to_file tools. Use editor commands when the user wants interactive editing behavior (e.g., "make this bold", "add a callout").

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/editor.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/editor.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/editor.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/editor.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
