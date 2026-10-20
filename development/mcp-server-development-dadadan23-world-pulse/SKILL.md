---
name: "mcp-server-development"
description: 'Build Model Context Protocol (MCP) servers that expose tools, resources, and prompts to AI agents. Use when creating MCP servers in TypeScript or Python, defining MCP tools, implementing resource providers, or integrating MCP servers with AI agent workflows.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 languages: ["typescript", "python", "csharp"]
 frameworks: ["mcp-sdk"]
 platforms: ["windows", "linux", "macos"]
---

# MCP Server Development

> Build [Model Context Protocol](https://modelcontextprotocol.io) servers that expose tools, resources, and prompts to AI coding agents.

## When to Use

- Building a tool server for Copilot, Claude, or other MCP-compatible agents
- Exposing an API, database, or service as agent-callable tools
- Creating reusable prompt templates for agent workflows
- Providing file/resource access to agents through a standard protocol

## Decision Tree

```
Need to expose capabilities to AI agents?
+- Read-only data access?
| - Use MCP Resources (URI-based, typed)
+- Execute actions / side effects?
| - Use MCP Tools (JSON Schema input, structured output)
+- Reusable prompt templates?
| - Use MCP Prompts (parameterized, multi-turn)
- Combine multiple?
 - Single MCP server with mixed capabilities
```

## Architecture Overview

```
-------------- stdio/SSE --------------
| AI Agent | ------------- | MCP Server |
| (Copilot) | JSON-RPC 2.0 | (your code) |
-------------- ------+-------
 |
 -------------+-------------
 | | |
 Tools Resources Prompts
 (actions) (read data) (templates)
```

## Quick Start: TypeScript

```bash
npm init -y
npm install @modelcontextprotocol/sdk zod
```

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
 name: "my-server",
 version: "1.0.0",
});

// Tool: execute actions
server.tool("greet", { name: z.string() }, async ({ name }) => ({
 content: [{ type: "text", text: `Hello, ${name}!` }],
}));

// Resource: read-only data
server.resource("config", "config://app", async () => ({
 contents: [{ uri: "config://app", text: JSON.stringify({ env: "prod" }) }],
}));

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Quick Start: Python

```bash
pip install mcp
```

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def greet(name: str) -> str:
 """Greet a user by name."""
 return f"Hello, {name}!"

@mcp.resource("config://app")
def get_config() -> str:
 """Read application configuration."""
 return '{"env": "prod"}'

# Run: python server.py
```

## Core Rules

### 1. Transport Selection

| Transport | Use When | Pros |
|-----------|----------|------|
| **stdio** | Local tools, VS Code extensions | Simple, secure, no network |
| **SSE** | Remote servers, shared services | Network accessible, multi-client |
| **Streamable HTTP** | Production APIs | Scalable, stateless-friendly |

### 2. Tool Design

- **One tool, one action**: Don't create God-tools that do everything
- **Descriptive names**: `search-issues` not `doThing`
- **Typed inputs**: Use JSON Schema / Zod / Pydantic for all parameters
- **Structured output**: Return `{ content: [{ type: "text", text: "..." }] }`
- **Error handling**: Return `isError: true` with descriptive messages, don't throw

### 3. Resource Design

- **URI scheme**: Use descriptive schemes (`db://`, `file://`, `config://`)
- **Typed content**: Set `mimeType` on all resource contents
- **Templates**: Use URI templates for parameterized resources: `db://users/{id}`
- **Pagination**: For large collections, support cursor-based pagination

### 4. Security

- **Validate all inputs**: Never trust agent-provided data
- **Least privilege**: Only expose necessary capabilities
- **No secrets in responses**: Filter sensitive data before returning
- **Rate limiting**: Protect against excessive tool calls
- **Audit logging**: Log all tool invocations with parameters

### 5. Configuration for VS Code

Add to `.vscode/mcp.json` (or user settings):

```json
{
 "servers": {
 "my-server": {
 "command": "node",
 "args": ["./dist/server.js"],
 "env": { "API_KEY": "${input:apiKey}" }
 }
 }
}
```

## Anti-Patterns

- **Mega-tools**: One tool that accepts a "command" string and switches behavior
- **Untyped inputs**: Using `any` or `object` for tool parameters
- **Swallowed errors**: Catching exceptions without returning `isError: true`
- **Stateful servers**: Storing session state in memory (use external stores)
- **Missing descriptions**: Tools without clear descriptions -> agents can't use them effectively
- **Hardcoded secrets**: API keys in server code -> use environment variables

## Testing

```typescript
// Use MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector node dist/server.js

// Programmatic testing
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
const client = new Client({ name: "test", version: "1.0.0" });
// ... connect and call tools
```

## Project Structure

```
my-mcp-server/
+-- src/
| +-- server.ts # Server setup + transport
| +-- tools/ # Tool implementations
| | +-- search.ts
| | -- create.ts
| +-- resources/ # Resource handlers
| | -- config.ts
| -- prompts/ # Prompt templates
| -- review.ts
+-- package.json
+-- tsconfig.json
-- .vscode/mcp.json # Local server config
```

## Further Reading

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [VS Code MCP Integration](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
