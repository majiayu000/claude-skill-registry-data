---
name: metadata-menu
description: "For data quality enthusiasts (and dataview users): manage the metadata of your notes."
source: metadata-menu
---

# Metadata Menu

## Plugin metadata

- **id:** `metadata-menu`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `metadata-menu:fileClassAttr_options` -- Metadata Menu: All fileClass attributes options
- `metadata-menu:insert_fileClassAttr` -- Metadata Menu: Insert a new fileClass attribute
- `metadata-menu:field_options` -- Metadata Menu: Fields options
- `metadata-menu:insert_field_at_cursor` -- Metadata Menu: Choose a field to insert at cursor
- `metadata-menu:field_at_cursor_options` -- Metadata Menu: Manage field at cursor
- `metadata-menu:insert_missing_fields` -- Metadata Menu: Bulk insert missing fields
- `metadata-menu:open_fields_modal` -- Metadata Menu: Open this note's fields modal
- `metadata-menu:update_file_lookups` -- Metadata Menu: Update active file lookups fields
- `metadata-menu:update_file_formulas` -- Metadata Menu: Update active file formulas fields
- `metadata-menu:open_fileclass_view` -- Metadata Menu: Open fileClass view
- `metadata-menu:add_fileclass_to_file` -- Metadata Menu: Add fileClass to file
- `metadata-menu:update_all_lookups` -- Metadata Menu: Update all lookups and formulas

# Metadata Menu

**Description:** For data quality enthusiasts (and dataview users): manage the metadata of your notes.
**Status:** Enabled
**Plugin ID:** metadata-menu

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `metadata-menu:fileClassAttr_options` -- Metadata Menu: All fileClass attributes options
- `metadata-menu:insert_fileClassAttr` -- Metadata Menu: Insert a new fileClass attribute
- `metadata-menu:field_options` -- Metadata Menu: Fields options
- `metadata-menu:insert_field_at_cursor` -- Metadata Menu: Choose a field to insert at cursor
- `metadata-menu:field_at_cursor_options` -- Metadata Menu: Manage field at cursor
- `metadata-menu:insert_missing_fields` -- Metadata Menu: Bulk insert missing fields
- `metadata-menu:open_fields_modal` -- Metadata Menu: Open this note's fields modal
- `metadata-menu:update_file_lookups` -- Metadata Menu: Update active file lookups fields
- `metadata-menu:update_file_formulas` -- Metadata Menu: Update active file formulas fields
- `metadata-menu:open_fileclass_view` -- Metadata Menu: Open fileClass view
- `metadata-menu:add_fileclass_to_file` -- Metadata Menu: Add fileClass to file
- `metadata-menu:update_all_lookups` -- Metadata Menu: Update all lookups and formulas

## Plugin API

This plugin exposes a JavaScript API. Use call_plugin_api to call these methods:
- `hasOwnProperty` -- call via call_plugin_api("metadata-menu", "hasOwnProperty", [args])
- `isPrototypeOf` -- call via call_plugin_api("metadata-menu", "isPrototypeOf", [args])
- `propertyIsEnumerable` -- call via call_plugin_api("metadata-menu", "propertyIsEnumerable", [args])
- `toString` -- call via call_plugin_api("metadata-menu", "toString", [args])
- `valueOf` -- call via call_plugin_api("metadata-menu", "valueOf", [args])
- `toLocaleString` -- call via call_plugin_api("metadata-menu", "toLocaleString", [args])

Note: Dynamically discovered methods require user approval for each call unless marked as safe in settings.

## Configuration File

Settings path: `.obsidian/plugins/metadata-menu/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/metadata-menu/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/metadata-menu/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
displayFieldsInContextMenu: true
isAutosuggestEnabled: true
fileClassAlias: fileClass
settingsVersion: 5.0
firstDayOfWeek: 1
enableLinks: true
enableTabHeader: true
enableEditor: true
enableBacklinks: true
enableStarred: true
enableFileExplorer: true
enableSearch: true
enableProperties: true
tableViewMaxRecords: 20
frontmatterListDisplay: asArray
showIndexingStatusInStatusBar: true
fileIndexingExcludedExtensions: [.excalidraw.md]
frontmatterOnly: false
showFileClassSelectInModal: true
chooseFileClassAtFileCreation: false
autoInsertFieldsAtFileClassInsertion: false
fileClassIcon: package
isAutoCalculationEnabled: true
disableDataviewPrompt: false
```

For full settings, read: `.obsidian/plugins/metadata-menu/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/metadata-menu.readme.md")

## Usage

When the user asks for functionality related to Metadata Menu:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/metadata-menu/data.json). If it does not exist, that is normal -- create it with the required settings
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
