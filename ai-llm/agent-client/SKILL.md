---
name: agent-client
description: "Chat with AI agents via the Agent Client Protocol directly from your vault."
source: agent-client
---

# Agent Client

## Plugin metadata

- **id:** `agent-client`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `agent-client:open-chat-view` -- Agent Client: Open chat view
- `agent-client:focus-next-chat-view` -- Agent Client: Focus next chat view
- `agent-client:focus-previous-chat-view` -- Agent Client: Focus previous chat view
- `agent-client:open-new-chat-view` -- Agent Client: Open new chat view
- `agent-client:open-session-manager` -- Agent Client: Open session manager
- `agent-client:switch-agent-to-claude-code-acp` -- Agent Client: Switch agent to Claude Code
- `agent-client:switch-agent-to-codex-acp` -- Agent Client: Switch agent to Codex
- `agent-client:switch-agent-to-gemini-cli` -- Agent Client: Switch agent to Gemini CLI
- `agent-client:switch-agent-to-mistral-vibe` -- Agent Client: Switch agent to Mistral Vibe
- `agent-client:switch-agent-to-opencode` -- Agent Client: Switch agent to OpenCode
- `agent-client:switch-agent-to-kiro-cli` -- Agent Client: Switch agent to Kiro
- `agent-client:switch-agent-to-hermes-agent` -- Agent Client: Switch agent to Hermes Agent
- `agent-client:approve-active-permission` -- Agent Client: Approve active permission
- `agent-client:reject-active-permission` -- Agent Client: Reject active permission
- `agent-client:toggle-auto-mention` -- Agent Client: Toggle auto-mention
- `agent-client:new-chat` -- Agent Client: New chat
- `agent-client:cancel-current-message` -- Agent Client: Cancel current message
- `agent-client:export-chat` -- Agent Client: Export chat
- `agent-client:broadcast-prompt` -- Agent Client: Broadcast prompt
- `agent-client:broadcast-send` -- Agent Client: Broadcast send
- `agent-client:broadcast-cancel` -- Agent Client: Broadcast cancel
- `agent-client:open-floating-chat-view` -- Agent Client: Open floating chat view
- `agent-client:open-new-floating-chat-view` -- Agent Client: Open new floating chat view
- `agent-client:minimize-floating-chat-view` -- Agent Client: Minimize floating chat view
- `agent-client:close-floating-chat-view` -- Agent Client: Close floating chat view

# Agent Client

**Description:** Chat with AI agents via the Agent Client Protocol directly from your vault.
**Status:** Enabled
**Plugin ID:** agent-client

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `agent-client:open-chat-view` -- Agent Client: Open chat view
- `agent-client:focus-next-chat-view` -- Agent Client: Focus next chat view
- `agent-client:focus-previous-chat-view` -- Agent Client: Focus previous chat view
- `agent-client:open-new-chat-view` -- Agent Client: Open new chat view
- `agent-client:open-session-manager` -- Agent Client: Open session manager
- `agent-client:switch-agent-to-claude-code-acp` -- Agent Client: Switch agent to Claude Code
- `agent-client:switch-agent-to-codex-acp` -- Agent Client: Switch agent to Codex
- `agent-client:switch-agent-to-gemini-cli` -- Agent Client: Switch agent to Gemini CLI
- `agent-client:switch-agent-to-mistral-vibe` -- Agent Client: Switch agent to Mistral Vibe
- `agent-client:switch-agent-to-opencode` -- Agent Client: Switch agent to OpenCode
- `agent-client:switch-agent-to-kiro-cli` -- Agent Client: Switch agent to Kiro
- `agent-client:switch-agent-to-hermes-agent` -- Agent Client: Switch agent to Hermes Agent
- `agent-client:approve-active-permission` -- Agent Client: Approve active permission
- `agent-client:reject-active-permission` -- Agent Client: Reject active permission
- `agent-client:toggle-auto-mention` -- Agent Client: Toggle auto-mention
- `agent-client:new-chat` -- Agent Client: New chat
- `agent-client:cancel-current-message` -- Agent Client: Cancel current message
- `agent-client:export-chat` -- Agent Client: Export chat
- `agent-client:broadcast-prompt` -- Agent Client: Broadcast prompt
- `agent-client:broadcast-send` -- Agent Client: Broadcast send
- `agent-client:broadcast-cancel` -- Agent Client: Broadcast cancel
- `agent-client:open-floating-chat-view` -- Agent Client: Open floating chat view
- `agent-client:open-new-floating-chat-view` -- Agent Client: Open new floating chat view
- `agent-client:minimize-floating-chat-view` -- Agent Client: Minimize floating chat view
- `agent-client:close-floating-chat-view` -- Agent Client: Close floating chat view

## Configuration File

Settings path: `.obsidian/plugins/agent-client/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/agent-client/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/agent-client/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/agent-client.readme.md")

## Usage

When the user asks for functionality related to Agent Client:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/agent-client/data.json). If it does not exist, that is normal -- create it with the required settings
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
