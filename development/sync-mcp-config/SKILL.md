---
name: sync-mcp-config
description: Synchronize MCP (Model Context Protocol) server settings across different Agent tools. Use when you want to copy, apply, or sync MCP settings between multiple Agent environments like Claude Code, VSCode, Cursor, Claude Desktop, Codex, and Gemini CLI. Supports both full synchronization and selective synchronization of specific MCP servers.
allowed-tools: Read, Write, Bash, Glob, WebSearch, WebFetch, AskUserQuestion
---

# MCP Settings Synchronization Skill

## Overview

This skill provides procedures for synchronizing MCP server settings across different Agent tool environments.

## What This Skill Does

1. Read MCP server settings registered in the configuration file of the specified Agent tool
2. Apply the settings to the MCP configuration file of the target Agent tool
3. Support both full synchronization and selective synchronization of specific MCP servers
4. Handle both global (user-level) and project-level configurations

## Configuration Scopes

MCP settings can exist at different scopes depending on the Agent tool:

| Agent Tool     | Global (User-Level)        | Project-Level           |
| -------------- | -------------------------- | ----------------------- |
| Claude Code    | `~/.claude.json`           | `.mcp.json`             |
| VS Code        | User `mcp.json`            | `.vscode/mcp.json`      |
| Cursor         | User `mcp.json`            | `.cursor/mcp.json`      |
| Gemini CLI     | `~/.gemini/settings.json`  | `.gemini/settings.json` |
| Claude Desktop | ✅ Supported               | ❌ Not Supported        |
| Codex CLI      | ✅ Supported               | ❌ Not Supported        |
| Antigravity    | ✅ Supported               | ❌ Not Supported        |

When synchronizing settings, consider:

- **Global settings**: Applied to all projects for the user
- **Project settings**: Applied only to the specific project directory

If the target Agent tool does not support project-level configuration, only global synchronization is possible.

## Operation Modes

### Synchronization Modes

#### Full Synchronization

Synchronize all MCP servers from the source to the target Agent tool.

#### Selective Synchronization

Synchronize only specified MCP servers from the source to the target Agent tool. Users can specify:

- A single MCP server name (e.g., `filesystem`)
- Multiple MCP server names (e.g., `filesystem`, `github`, `slack`)

This is useful when:

- You only want to add specific MCP servers to another environment
- You want to update a particular MCP server configuration without affecting others
- You want to avoid overwriting existing configurations for other servers

### Deletion Mode

#### Selective Deletion

Delete specified MCP servers from the target Agent tool's configuration. Users can specify:

- A single MCP server name to delete (e.g., `filesystem`)
- Multiple MCP server names to delete (e.g., `filesystem`, `github`, `slack`)

This is useful when:

- You want to remove unused or deprecated MCP servers from an environment
- You want to clean up MCP server configurations that are no longer needed
- You want to remove specific MCP servers without affecting others

**Important**: This operation does not require a source Agent tool - it operates directly on the target configuration.

## Procedures

### 1. Check Operating System Environment

Before starting the synchronization process, verify the current operating system environment using the Bash tool or by checking environment variables. This is important because:

- Configuration file paths may differ between operating systems (Windows, macOS, Linux)
- File path separators are different (Windows uses `\`, Unix-like systems use `/`)
- Default installation locations vary by OS

Use appropriate methods to determine:

- Operating system type (Windows, macOS, Linux, etc.)
- User home directory path
- Relevant environment-specific paths

### 2. Confirm Operation Parameters with User

Before proceeding, confirm with the user using the AskUserQuestion tool:

1. **Operation Type**: Synchronization or Deletion
2. **Source Agent Tool** (for synchronization only): Which Agent tool to read MCP servers from
3. **Target Agent Tool**: Which Agent tool to apply changes to
4. **Scope**: Global (user-level), project-level, or both
5. **Mode**: Full synchronization, selective synchronization, or selective deletion
6. **Server Selection** (if selective): Which specific MCP servers to synchronize or delete

For selective synchronization, present the list of available MCP servers from the source and confirm which servers to synchronize.
For selective deletion, present the list of existing MCP servers in the target and confirm which servers to delete.

### 3. Verify MCP Configuration File Specifications

Since MCP configuration methods may vary depending on the Agent tool, first verify and understand the specifications of the MCP configuration files for both the source and target Agent tools.

Refer to the md documents in the following directory for specifications:

- [MCP Configuration Method Reference](./reference/)

Available references:

- [Claude Code](./reference/claude_code.md)
- [VSCode](./reference/vscode.md)
- [Cursor](./reference/cursor.md)
- [Claude Desktop](./reference/claude_desktop.md)
- [Codex CLI](./reference/codex_cli.md)
- [Gemini CLI](./reference/gemini_cli.md)
- [Antigravity](./reference/antigravity.md)

**If reference documentation is not available for the target Agent tool:**

- Use WebSearch and WebFetch tools to search the web for the configuration file specifications
- Look for official documentation, README files, or configuration examples
- Verify the file format (JSON, YAML, TOML, etc.) and required structure
- Identify the correct configuration file path and naming convention
- Understand how MCP servers should be defined in that specific tool's format

### 4. Check Available MCP Servers

Read the configuration file containing the MCP server settings of the source Agent tool and check available MCP servers.
The configuration includes the following information:

- Server name
- Transport method (HTTP, stdio, etc.)
- Endpoint URL (for HTTP)
- Launch command (for stdio transport)
- Launch arguments (for stdio transport)
- Authentication information (API keys, etc.)
- Environment variables at launch (as needed)
- Settings to enable the MCP server

For selective synchronization, present the list of available MCP servers to the user and confirm which servers to synchronize.

### 5. Apply Changes to Target Agent Tool Configuration File

Read the target Agent tool's MCP configuration file and apply the changes based on the operation mode.

#### For Synchronization Operations

- For full synchronization: Apply all MCP servers from the source.
- For selective synchronization: Apply only the specified MCP servers.
- If the same server is already registered, compare the contents and let the user decide if an update is needed.
- Preserve existing MCP servers in the target that are not being synchronized.

#### For Deletion Operations

- For selective deletion: Remove only the specified MCP servers from the target configuration.
- Before deleting, confirm with the user which servers will be removed.
- Preserve all MCP servers that are not specified for deletion.

#### Common Guidelines

- Write correctly according to the target configuration file format.
- Create backups as necessary before making changes.

### 6. Validate Settings

After making changes, validate that the configuration file has no issues.

- Check file format integrity

## Special Cases / Exceptional Cases / Errors

In the following cases, notify the user and stop processing:

- There are no MCP servers registered in the source configuration file (for synchronization).
- The source configuration file does not exist (for synchronization).
- The target configuration file is not writable.
- The configuration file format is invalid.
- The requested MCP server for selective sync does not exist in the source.
- The requested MCP server for selective deletion does not exist in the target.
- There are no MCP servers registered in the target configuration file (for deletion).

In the following cases, use tools as necessary to handle the situation:

- The target configuration file does not exist.
  Create a new target configuration file. (use Bash tool if necessary)

- The MCP server settings are incompatible between the source and target Agent tools.
  Since configuration file formats and element names may differ, verify the specifications of both source and target, and rewrite the format so that the MCP server settings content remains the same.
  If there are unclear points, perform web searches to verify specifications. (use WebSearch WebFetch tool if necessary)

## Prohibited Actions

The following actions are prohibited when managing MCP server settings:

- Modifying settings other than MCP servers
- Leaking authentication information
- Applying invalid MCP server settings
- Overwriting existing MCP servers without user confirmation
- Deleting MCP servers without user confirmation
- Deleting MCP servers that are not specified for deletion

## When to Use This Skill

- When users want to synchronize MCP settings across multiple Agent environments
- When setting up new MCP servers
- When users want to remove specific MCP servers from an Agent environment
- When cleaning up unused or deprecated MCP server configurations

## Examples

**Example 1**: "I want to apply Claude Code's MCP settings to Codex" (Full Synchronization)

- Read Claude Code's MCP configuration file
- Apply all MCP server settings to Codex's MCP configuration file

**Example 2**: "Sync only the 'filesystem' and 'github' MCP servers from Claude Code to VS Code" (Selective Synchronization)

- Read Claude Code's MCP configuration file
- Extract only the 'filesystem' and 'github' MCP server configurations
- Apply those specific servers to VS Code's MCP configuration file
- Preserve any existing MCP servers in VS Code that are not being synchronized

**Example 3**: "Add the 'slack' MCP server from Cursor to Claude Desktop"

- Read Cursor's MCP configuration file
- Extract only the 'slack' MCP server configuration
- Apply the 'slack' server to Claude Desktop's MCP configuration file

**Example 4**: "Sync project-level MCP settings from VS Code to Cursor"

- Read the project's `.vscode/mcp.json` file
- Apply the MCP servers to the project's `.cursor/mcp.json` file

**Example 5**: "Delete the 'filesystem' MCP server from Claude Code" (Selective Deletion)

- Read Claude Code's MCP configuration file
- Confirm the 'filesystem' server exists
- Remove the 'filesystem' server from the configuration
- Preserve all other MCP servers

**Example 6**: "Remove the 'github' and 'slack' MCP servers from VS Code's global settings"

- Read VS Code's global MCP configuration file
- Confirm both 'github' and 'slack' servers exist
- Remove those specific servers from the configuration
- Preserve all other MCP servers

**Example 7**: "Clean up unused MCP servers from Cursor"

- Read Cursor's MCP configuration file
- List all available MCP servers to the user
- Ask user which servers to delete
- Remove the specified servers from the configuration

## Best Practices

- Always confirm the operation type (sync/delete), scope (global/project), and mode with the user before proceeding
- Back up configuration files before any changes
- For selective synchronization, show the user the available MCP servers before asking which to sync
- For selective deletion, show the user the existing MCP servers before asking which to delete
- When MCP servers exist in both source and target, show the differences and ask user preference
- Preserve existing MCP servers in the target that are not part of the operation
- Refer to documentation when configuration file specifications are unclear
- Perform web searches if reference documentation is not available
- Always require explicit user confirmation before deleting any MCP servers
