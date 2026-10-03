---
name: mcp-builder
description: MCP (Model Context Protocol) server building principles. Tool design, resource patterns, best practices.
when_to_use: "When building MCP (Model Context Protocol) servers, designing MCP tools, or implementing MCP resource patterns."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# MCP Builder

> Principles for building MCP servers.

---

## 1. MCP Overview

### What is MCP?

Model Context Protocol - standard for connecting AI systems with external tools and data sources.

### Core Concepts

| Concept | Purpose |
|---------|---------|
| **Tools** | Functions AI can call |
| **Resources** | Data AI can read |
| **Prompts** | Pre-defined prompt templates |

---

## 2. Server Architecture

### Project Structure

```
my-mcp-server/
├── src/
│   └── index.ts      # Main entry — McpServer from @modelcontextprotocol/sdk
├── package.json      # dep: @modelcontextprotocol/sdk
└── tsconfig.json
```

> TypeScript SDK: `@modelcontextprotocol/sdk` (`McpServer`). Python SDK: `mcp` (`pip install "mcp[cli]"`, `FastMCP` bundled in `mcp.server.fastmcp`).

### Transport Types

| Type | Use |
|------|-----|
| **stdio** | Local, CLI-based |
| **Streamable HTTP** | Remote/web servers (replaced the deprecated HTTP+SSE transport) |

> The current spec (2025-06-18) defines two standard transports: stdio and Streamable HTTP. WebSocket is not a standard transport. Validate the `Origin` header on Streamable HTTP servers.

---

## 3. Tool Design Principles

### Good Tool Design

| Principle | Description |
|-----------|-------------|
| Clear name | Action-oriented (get_weather, create_user) |
| Single purpose | One thing well |
| Validated input | Schema with types and descriptions |
| Structured output | Predictable response format |

### Input Schema Design

| Field | Required? |
|-------|-----------|
| Type | Yes - object |
| Properties | Define each param |
| Required | List mandatory params |
| Description | Human-readable |

---

## 4. Resource Patterns

### Resource Types

| Type | Use |
|------|-----|
| Static | Fixed data (config, docs) |
| Dynamic | Generated on request |
| Template | URI with parameters |

### URI Patterns

| Pattern | Example |
|---------|---------|
| Fixed | `docs://readme` |
| Parameterized | `users://{userId}` |
| Collection | `files://project/*` |

---

## 5. Error Handling

### Error Types

| Situation | Response |
|-----------|----------|
| Invalid params | Validation error message |
| Not found | Clear "not found" |
| Server error | Generic error, log details |

### Best Practices

- Return structured errors
- Don't expose internal details
- Log for debugging
- Provide actionable messages

---

## 6. Multimodal Handling

### Supported Types

| Type | Encoding |
|------|----------|
| Text | Plain text |
| Images | Base64 + MIME type |
| Files | Base64 + MIME type |

---

## 7. Security Principles

### Input Validation

- Validate all tool inputs
- Sanitize user-provided data
- Limit resource access

### API Keys

- Use environment variables
- Don't log secrets
- Validate permissions

---

## 8. Configuration

### Client Config (Claude Desktop, Claude Code, IDEs)

| Field | Purpose |
|-------|---------|
| command | Executable to run (stdio servers) |
| args | Command arguments |
| env | Environment variables |

> MCP is multi-client — the same server works across Claude Desktop, Claude Code, and IDE hosts. Remote (Streamable HTTP) servers authenticate via OAuth rather than a local command.

---

## 9. Current Spec Features

Worth using in modern servers (spec 2025-06-18):

| Feature | Purpose |
|---------|---------|
| Tool annotations | Hint read-only/destructive behavior to the client |
| Structured content / `outputSchema` | Typed, predictable tool results |
| Resource links | Return references to resources from tool results |
| OAuth | Auth for remote/Streamable HTTP servers |

---

## 10. Testing

### Test Categories

| Type | Focus |
|------|-------|
| Unit | Tool logic |
| Integration | Full server |
| Contract | Schema validation |

---

## 11. Best Practices Checklist

- [ ] Clear, action-oriented tool names
- [ ] Complete input schemas with descriptions
- [ ] Structured JSON output
- [ ] Error handling for all cases
- [ ] Input validation
- [ ] Environment-based configuration
- [ ] Logging for debugging

---

> **Remember:** MCP tools should be simple, focused, and well-documented. The AI relies on descriptions to use them correctly.
