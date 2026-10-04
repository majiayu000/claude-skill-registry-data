---
name: table-editor-obsidian
description: "Improved table navigation, formatting, manipulation, and formulas."
source: table-editor-obsidian
---

# Advanced Tables

## Plugin metadata

- **id:** `table-editor-obsidian`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `table-editor-obsidian:next-row` -- Advanced Tables: Go to next row
- `table-editor-obsidian:next-cell` -- Advanced Tables: Go to next cell
- `table-editor-obsidian:previous-cell` -- Advanced Tables: Go to previous cell
- `table-editor-obsidian:format-table` -- Advanced Tables: Format table at the cursor
- `table-editor-obsidian:format-all-tables` -- Advanced Tables: Format all tables in this file
- `table-editor-obsidian:insert-column` -- Advanced Tables: Insert column before current
- `table-editor-obsidian:insert-row` -- Advanced Tables: Insert row before current
- `table-editor-obsidian:escape-table` -- Advanced Tables: Move cursor out of table
- `table-editor-obsidian:left-align-column` -- Advanced Tables: Left align column
- `table-editor-obsidian:center-align-column` -- Advanced Tables: Center align column
- `table-editor-obsidian:right-align-column` -- Advanced Tables: Right align column
- `table-editor-obsidian:move-column-left` -- Advanced Tables: Move column left
- `table-editor-obsidian:move-column-right` -- Advanced Tables: Move column right
- `table-editor-obsidian:move-row-up` -- Advanced Tables: Move row up
- `table-editor-obsidian:move-row-down` -- Advanced Tables: Move row down
- `table-editor-obsidian:delete-column` -- Advanced Tables: Delete column
- `table-editor-obsidian:delete-row` -- Advanced Tables: Delete row
- `table-editor-obsidian:sort-rows-ascending` -- Advanced Tables: Sort rows ascending
- `table-editor-obsidian:sort-rows-descending` -- Advanced Tables: Sort rows descending
- `table-editor-obsidian:transpose` -- Advanced Tables: Transpose
- `table-editor-obsidian:evaluate-formulas` -- Advanced Tables: Evaluate table formulas
- `table-editor-obsidian:table-control-bar` -- Advanced Tables: Open table controls toolbar

# Advanced Tables

**Description:** Improved table navigation, formatting, manipulation, and formulas.
**Status:** Enabled
**Plugin ID:** table-editor-obsidian

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `table-editor-obsidian:next-row` -- Advanced Tables: Go to next row
- `table-editor-obsidian:next-cell` -- Advanced Tables: Go to next cell
- `table-editor-obsidian:previous-cell` -- Advanced Tables: Go to previous cell
- `table-editor-obsidian:format-table` -- Advanced Tables: Format table at the cursor
- `table-editor-obsidian:format-all-tables` -- Advanced Tables: Format all tables in this file
- `table-editor-obsidian:insert-column` -- Advanced Tables: Insert column before current
- `table-editor-obsidian:insert-row` -- Advanced Tables: Insert row before current
- `table-editor-obsidian:escape-table` -- Advanced Tables: Move cursor out of table
- `table-editor-obsidian:left-align-column` -- Advanced Tables: Left align column
- `table-editor-obsidian:center-align-column` -- Advanced Tables: Center align column
- `table-editor-obsidian:right-align-column` -- Advanced Tables: Right align column
- `table-editor-obsidian:move-column-left` -- Advanced Tables: Move column left
- `table-editor-obsidian:move-column-right` -- Advanced Tables: Move column right
- `table-editor-obsidian:move-row-up` -- Advanced Tables: Move row up
- `table-editor-obsidian:move-row-down` -- Advanced Tables: Move row down
- `table-editor-obsidian:delete-column` -- Advanced Tables: Delete column
- `table-editor-obsidian:delete-row` -- Advanced Tables: Delete row
- `table-editor-obsidian:sort-rows-ascending` -- Advanced Tables: Sort rows ascending
- `table-editor-obsidian:sort-rows-descending` -- Advanced Tables: Sort rows descending
- `table-editor-obsidian:transpose` -- Advanced Tables: Transpose
- `table-editor-obsidian:evaluate-formulas` -- Advanced Tables: Evaluate table formulas
- `table-editor-obsidian:table-control-bar` -- Advanced Tables: Open table controls toolbar

## Configuration File

Settings path: `.obsidian/plugins/table-editor-obsidian/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/table-editor-obsidian/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/table-editor-obsidian/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
formatType: normal
showRibbonIcon: true
bindEnter: true
bindTab: true
```

For full settings, read: `.obsidian/plugins/table-editor-obsidian/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/table-editor-obsidian.readme.md")

## Usage

When the user asks for functionality related to Advanced Tables:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/table-editor-obsidian/data.json). If it does not exist, that is normal -- create it with the required settings
3. Configure the plugin by writing data.json with the values needed for the task
4. Execute the task using the appropriate tool:
   - For Obsidian-native commands (including file export): use execute_command
   - For CLI-based conversion needing Pandoc/LaTeX: use execute_recipe
   - For data queries: use call_plugin_api
5. If a command opens a UI dialog, tell the user what to click.

CRITICAL RULES:
- Prefer native Obsidian commands over external tools when both can accomplish the task.
- NEVER create fake output files. If the user asks for a PDF/DOCX/image export, use execute_recipe -- do NOT write content to a .pdf file yourself.
- If a dependency is missing (e.g. Pandoc), tell the user what to install.
IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
