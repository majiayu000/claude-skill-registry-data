---
name: sync-mcp-config
description: Synchronize MCP (Model Context Protocol) server settings across different Agent tools. Use when you want to copy, apply, or sync MCP settings between multiple Agent environments like Claude Code, VSCode, Claude Desktop, Codex, and Gemini CLI.
allowed-tools: Read, Write, Bash, WebSearch, WebFetch
---

# MCP Settings Synchronization Skill

## Overview

This skill provides procedures for synchronizing MCP server settings across different Agent tool environments.

## What This Skill Does

1. Read MCP server settings registered in the configuration file of the specified Agent tool
2. Apply the settings to the MCP configuration file of the target Agent tool

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

### 2. Verify MCP Configuration File Specifications

Since MCP configuration methods may vary depending on the Agent tool, first verify and understand the specifications of the MCP configuration files for both the source and target Agent tools.

Refer to the md documents in the following directory for specifications:

- [MCP Configuration Method Reference](./reference/)

Available references:

- [Claude Code](./reference/claude_code.md)
- [VSCode](./reference/vscode.md)
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

### 2. Check Available MCP Servers

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

### 3. Apply Available MCP Server Information to Target Agent Tool Configuration File

Read the target Agent tool's MCP configuration file, apply the MCP server information obtained from the source, and save it.

- If the same server is already registered, compare the contents and let the user decide if an update is needed.
- Write correctly according to the target configuration file format.
- Create backups as necessary.

### 4. Validate Settings

After making changes, validate that the configuration file has no issues.

- Check file format integrity

## Special Cases / Exceptional Cases / Errors

In the following cases, notify the user and stop processing:

- There are no MCP servers registered in the source configuration file.
- The source configuration file does not exist.
- The target configuration file is not writable.
- The configuration file format is invalid.

In the following cases, use tools as necessary to handle the situation:

- The target configuration file does not exist.
  Create a new target configuration file. (use Bash tool if necessary)

- The MCP server settings are incompatible between the source and target Agent tools.
  Since configuration file formats and element names may differ, verify the specifications of both source and target, and rewrite the format so that the MCP server settings content remains the same.
  If there are unclear points, perform web searches to verify specifications. (use WebSearch WebFetch tool if necessary)

## Prohibited Actions

The following actions are prohibited when synchronizing MCP server settings:

- Modifying settings other than MCP servers
- Leaking authentication information
- Applying invalid MCP server settings

## When to Use This Skill

- When users want to synchronize MCP settings across multiple Agent environments
- When setting up new MCP servers

## Examples

**Example 1**: "I want to apply Claude Code's MCP settings to Codex"

- Read Claude Code's MCP configuration file
- Apply the same settings to Codex's MCP configuration file

## Best Practices

- Always check both project scope and user scope settings
- Back up configuration files before synchronization
- Refer to documentation when configuration file specifications are unclear
- Perform web searches if reference documentation is not available
