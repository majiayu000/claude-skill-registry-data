---
name: cf-mcp-expert
description: When the user asks to create an MCP server, configure MCP integrations, design MCP tools, troubleshoot MCP connections, or set up Model Context Protocol servers — activate this MCP expert skill
---

# MCP Expert

Guide for creating, configuring, and debugging MCP (Model Context Protocol) servers and integrations.

## Activation

- User says "create an MCP server", "configure MCP", "set up MCP tools"
- User wants to wrap an API or database as MCP tools
- User is troubleshooting MCP connection failures or initialization errors
- User needs help designing tool schemas for an MCP server
- User asks about `.mcp.json` configuration

## Process

### 1. Design MCP Server

Determine what the MCP server exposes and how it communicates.

**Tools vs Resources**: Tools are actions the model can invoke (query a database, send a message). Resources are read-only data the model can reference (documentation, schema definitions).

**Tool Schema Design**:
- Use clear, verb-noun names: `query_database`, `send_slack_message`, `list_issues`
- Write descriptions that explain what the tool does AND when to use it
- Define input schemas using JSON Schema with required fields and sensible defaults
- Keep individual tool responses under 10k tokens to preserve context window

**Transport Selection**:
- **stdio** — Local processes, low latency, simplest setup. Best for personal dev tools
- **SSE (Server-Sent Events)** — Remote servers, shareable across machines, requires HTTP hosting

### 2. Standard Config Format

MCP servers are configured in `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name@latest"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```

**Key fields**: `command` (executable), `args` (arguments), `env` (environment variables), `cwd` (optional working directory).

For SSE transport, use `url` instead of `command`/`args`, with optional `headers` for auth tokens.

### 3. Common MCP Patterns

**Database MCP** — Connect to PostgreSQL, MySQL, MongoDB, or SQLite. Expose tools for running queries, listing tables, describing schemas. Always use read-only connections unless write access is explicitly needed.

**API MCP** — Wrap REST or GraphQL APIs as MCP tools. Map each API endpoint to a tool. Examples: Slack (send/read messages), GitHub (issues, PRs, repos), Jira (issues, boards), Linear (tasks, projects). Handle pagination within the tool so the model gets complete results.

**File System MCP** — Extended file operations beyond default Claude tools. Useful for bulk operations, glob patterns, file watching, or working with binary formats.

**Search MCP** — Web search, documentation search, code search integrations. Return structured results with titles, URLs, and snippets. Limit result count to avoid context bloat.

**Composite MCP** — A single server exposing tools from multiple domains. Useful when tools need shared state (e.g., a project management MCP that reads issues AND updates timelines).

### 4. Building a Custom MCP Server

Use `@modelcontextprotocol/sdk` with `zod` for schema validation. Minimal TypeScript skeleton:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.tool("my_tool", "Description of what this tool does", {
  input_param: z.string().describe("What this parameter controls"),
}, async ({ input_param }) => {
  const result = await doSomething(input_param);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
});

await server.connect(new StdioServerTransport());
```

### 5. Security Best Practices

- Never hardcode API keys in `.mcp.json` — use environment variables or reference a `.env` file
- Add `.mcp.json` to `.gitignore` — it contains project-specific and potentially sensitive config
- Minimize tool permissions: read-only database connections, scoped API tokens, least-privilege access
- Set timeouts for external API calls to prevent hanging tools
- Validate and sanitize all tool inputs — MCP servers are attack surface if exposed remotely
- For SSE transport, enforce HTTPS and authenticate incoming connections
- Audit tool usage logs periodically for unexpected patterns

### 6. Troubleshooting

- `claude mcp list` — Show all configured servers and status
- `claude mcp get <server-name>` — Detailed config for a specific server
- Run the server command manually to see stderr initialization errors

**Common fixes**:
- Server missing from `mcp list` — validate `.mcp.json` syntax and file location
- "Connection refused" — server crashed on startup, run command manually to see error
- Tools not showing — check tool schema validation, ensure descriptions exist
- Stale npx package — run `npx clear-npx-cache` then retry
- Missing env vars — add to `.env` or export in shell rc file
- "Method not found" — SDK version mismatch, pin versions and check compatibility

**Test stdio servers**: `echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | npx <server-package>`

## Output

- Working MCP server code or configuration
- `.mcp.json` configuration snippet ready to use
- Tool schema definitions with descriptions and input validation
- Troubleshooting diagnosis if debugging an existing setup

## Gotchas

- MCP servers run as separate processes — they can crash independently of Claude, and a crashed server gives no error in the chat, just missing tools
- Large tool responses eat context window — always paginate or summarize rather than dumping full datasets
- Some MCP packages require Node 18+ — check engine requirements before debugging mysterious failures
- SSE transport needs CORS configuration for browser-based clients
- `.mcp.json` is project-scoped, not global — each repo needs its own configuration
- Tool names must be unique across ALL active MCP servers — name collisions cause silent shadowing
- The `env` field in `.mcp.json` does not inherit from your shell — every needed variable must be explicitly listed
- When using `npx`, the `-y` flag is required to skip interactive prompts that would hang the server process
- Requires `python3` or `jq` for JSON parsing in hook scripts — if neither is available, hooks silently pass
