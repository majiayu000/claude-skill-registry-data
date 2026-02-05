---
name: mcp-tool
description: Understanding the Model Context Protocol (MCP) and how to use it in Claude Code. Use when user asks about MCP, Model Context Protocol, connecting external tools, MCP servers, or extending Claude's capabilities.
---

# Model Context Protocol (MCP)

## Core Concept

MCP is an open protocol that standardizes how applications provide context to LLMs. Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect your devices to various peripherals and accessories, MCP provides a standardized way to connect AI models to different data sources and tools.

## Purpose & Use Cases

MCP enables developers to connect AI models to custom tools and data sources in a standardized, interoperable manner—addressing a key need in extending Claude's capabilities beyond its base training.

## MCP in Anthropic Products

The protocol integrates across multiple Anthropic offerings:

1. **Messages API** - Developers can use the MCP connector to link to MCP servers programmatically
2. **Claude Code** - Supports adding custom MCP servers or using Claude Code as a server itself
3. **Claude.ai** - Teams can enable MCP connectors through the platform
4. **Claude Desktop** - Allows local MCP server configuration

## Build Your Own MCP Products

For protocol details, server/client development guidance, and community-created implementations, refer to the official MCP Documentation at **modelcontextprotocol.io**.

## MCP in Claude Code

### MCP Tool Integration

MCP tools follow the pattern: `mcp__<server>__<tool>`

### Using MCP in Hooks

Configure MCP tools with regex matchers in hooks:
```json
{
  "matcher": "mcp__memory__.*",
  "hooks": [{"type": "command", "command": "validate.py"}]
}
```

### MCP Slash Commands

MCP servers expose prompts as commands with the pattern:

```
/mcp__<server-name>__<prompt-name> [arguments]
```

These are dynamically discovered from connected MCP servers and automatically available when the server is active.

### Managing MCP Servers

Use the `/mcp` built-in command to manage MCP server connections.

## Plugin Integration

Plugins can include MCP servers via `.mcp.json` configuration for external tool integration.

## Resources

- Official MCP Documentation: modelcontextprotocol.io
- Anthropic's MCP implementation guides
- Community-created MCP servers and implementations
