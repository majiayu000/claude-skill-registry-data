---
name: nexus
description: "Agentic AI for your vault. Use Claude, ChatGPT, Gemini, and local models to chat, search, create, and manage your notes with semantic memory, image generation, and MCP server integration."
source: nexus
---

# Nexus

## Plugin metadata

- **id:** `nexus`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `nexus:open-chat` -- Nexus: Open chat
- `nexus:open-task-board` -- Nexus: Open task board
- `nexus:run-service-diagnostics` -- Nexus: Run service diagnostics
- `nexus:refresh-synced-data` -- Nexus: Refresh synced data
- `nexus:rebuild-cache` -- Nexus: Rebuild cache
- `nexus:experimental-run-claude-headless-session` -- Nexus: Launch a headless session
- `nexus:inline-ai-edit` -- Nexus: Edit selection
- `nexus:read-active-note-aloud` -- Nexus: Read note aloud
- `nexus:read-selection-aloud` -- Nexus: Read selection aloud
- `nexus:stop-read-aloud` -- Nexus: Stop read aloud
- `nexus:consolidate-retrieval-memory` -- Nexus: Consolidate retrieval memory (dream now)

# Nexus

**Description:** Agentic AI for your vault. Use Claude, ChatGPT, Gemini, and local models to chat, search, create, and manage your notes with semantic memory, image generation, and MCP server integration.
**Status:** Enabled
**Plugin ID:** nexus

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `nexus:open-chat` -- Nexus: Open chat
- `nexus:open-task-board` -- Nexus: Open task board
- `nexus:run-service-diagnostics` -- Nexus: Run service diagnostics
- `nexus:refresh-synced-data` -- Nexus: Refresh synced data
- `nexus:rebuild-cache` -- Nexus: Rebuild cache
- `nexus:experimental-run-claude-headless-session` -- Nexus: Launch a headless session
- `nexus:inline-ai-edit` -- Nexus: Edit selection
- `nexus:read-active-note-aloud` -- Nexus: Read note aloud
- `nexus:read-selection-aloud` -- Nexus: Read selection aloud
- `nexus:stop-read-aloud` -- Nexus: Stop read aloud
- `nexus:consolidate-retrieval-memory` -- Nexus: Consolidate retrieval memory (dream now)

## Configuration File

Settings path: `.obsidian/plugins/nexus/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/nexus/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/nexus/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
enabledVault: true
enableEmbeddings: true
enableIngestion: true
autoIngestion: false
storage:
  schemaVersion: 2
  rootPath: Nexus
  maxShardBytes: 4194304
  audioSubfolder: audio
customPrompts:
  enabled: true
llmProviders:
  providers:
    openai:
      enabled: false
    anthropic:
      enabled: false
    anthropic-claude-code:
      enabled: false
    google-gemini-cli:
      enabled: false
    google:
      enabled: false
    mistral:
      enabled: false
    groq:
      enabled: false
    deepseek:
      enabled: false
    deepgram:
      enabled: false
    assemblyai:
      enabled: false
    openrouter:
      enabled: false
    requesty:
      enabled: false
    perplexity:
      enabled: false
    openai-codex:
      enabled: false
    github-copilot:
      enabled: false
    ollama:
      enabled: false
    lmstudio:
      enabled: false
    webllm:
      enabled: false
      webllmModel: nexus-tools-q4f16
      webllmQuantization: q4f16
  defaultModel:
    provider: openai
    model: gpt-5.6-sol
  defaultImageModel:
    provider: google
    model: gemini-2.5-flash-image
  defaultVideoModel:
    provider: google
    model: veo-3.1-generate-preview
    aspectRatio: 16:9
    resolution: 720p
  defaultThinking:
    enabled: false
    effort: medium
  defaultTemperature: 0.5
pluginStorage:
  storageVersion: 2
  sourceOfTruthLocation: vault-root
  migration:
    state: not_needed
    activeDestination: Nexus/data
```
(18 sensitive field(s) redacted)

For full settings, read: `.obsidian/plugins/nexus/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/nexus.readme.md")

## Usage

When the user asks for functionality related to Nexus:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/nexus/data.json). If it does not exist, that is normal -- create it with the required settings
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
