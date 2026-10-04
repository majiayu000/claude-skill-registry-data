---
name: chatgpt-md
description: "Chat with cloud and local AI providers directly in Obsidian notes."
source: chatgpt-md
---

# ChatGPT MD

## Plugin metadata

- **id:** `chatgpt-md`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `chatgpt-md:call-chatgpt-api` -- ChatGPT MD: Chat
- `chatgpt-md:select-model-command` -- ChatGPT MD: Select Model
- `chatgpt-md:add-hr` -- ChatGPT MD: Add divider
- `chatgpt-md:add-comment-block` -- ChatGPT MD: Add comment block
- `chatgpt-md:stop-streaming` -- ChatGPT MD: Stop streaming
- `chatgpt-md:infer-title` -- ChatGPT MD: Infer title
- `chatgpt-md:move-to-chat` -- ChatGPT MD: Create new chat with highlighted text
- `chatgpt-md:choose-chat-template` -- ChatGPT MD: Create new chat from template
- `chatgpt-md:clear-chat` -- ChatGPT MD: Clear chat (except frontmatter)
- `chatgpt-md:choose-agent` -- ChatGPT MD: Choose agent
- `chatgpt-md:create-agent` -- ChatGPT MD: Create new agent

# ChatGPT MD

**Description:** Chat with cloud and local AI providers directly in Obsidian notes.
**Status:** Enabled
**Plugin ID:** chatgpt-md

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `chatgpt-md:call-chatgpt-api` -- ChatGPT MD: Chat
- `chatgpt-md:select-model-command` -- ChatGPT MD: Select Model
- `chatgpt-md:add-hr` -- ChatGPT MD: Add divider
- `chatgpt-md:add-comment-block` -- ChatGPT MD: Add comment block
- `chatgpt-md:stop-streaming` -- ChatGPT MD: Stop streaming
- `chatgpt-md:infer-title` -- ChatGPT MD: Infer title
- `chatgpt-md:move-to-chat` -- ChatGPT MD: Create new chat with highlighted text
- `chatgpt-md:choose-chat-template` -- ChatGPT MD: Create new chat from template
- `chatgpt-md:clear-chat` -- ChatGPT MD: Clear chat (except frontmatter)
- `chatgpt-md:choose-agent` -- ChatGPT MD: Choose agent
- `chatgpt-md:create-agent` -- ChatGPT MD: Create new agent

## Configuration File

Settings path: `.obsidian/plugins/chatgpt-md/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/chatgpt-md/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/chatgpt-md/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/chatgpt-md.readme.md")

## Usage

When the user asks for functionality related to ChatGPT MD:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/chatgpt-md/data.json). If it does not exist, that is normal -- create it with the required settings
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
