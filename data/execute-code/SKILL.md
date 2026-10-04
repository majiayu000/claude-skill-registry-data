---
name: execute-code
description: "Allows you to execute code snippets within a note. Support C, C++, Python, R, JavaScript, TypeScript, LaTeX, SQL, and many more."
source: execute-code
---

# Execute Code

## Plugin metadata

- **id:** `execute-code`
- **source:** vault-native
- **plugin-type:** community
- **status:** disabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

# Execute Code

**Description:** Allows you to execute code snippets within a note. Support C, C++, Python, R, JavaScript, TypeScript, LaTeX, SQL, and many more.
**Status:** Disabled
**Plugin ID:** execute-code

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Configuration File

Settings path: `.obsidian/plugins/execute-code/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/execute-code/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/execute-code/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/execute-code.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("execute-code") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
