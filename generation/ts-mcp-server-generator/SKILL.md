---
name: ts-mcp-server-generator
description: 'Generate an MCP server in TypeScript with tools, resources and prompts (@modelcontextprotocol/sdk + zod). Use when asked to create or scaffold an MCP server in TypeScript or Node.js.'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

Generate an MCP server in TypeScript. Paths to `scripts/` and `templates/` are relative to this skill's directory.

## Stack

- `@modelcontextprotocol/sdk` — McpServer, transports
- `zod` — schema validation
- `tsx` for dev

## Steps

### Phase 1 — Scaffold

```powershell
pwsh scripts/New-McpServer.ps1 -ServerName my-mcp-server
```

The script copies `templates/package.json`, `templates/tsconfig.json` and `templates/src/index.ts`, then installs dependencies.

### Phase 2 — Implement

See `templates/examples/tool-registration.ts` for tool pattern.
See `templates/examples/resource-prompt-registration.ts` for resources + prompts.

### Phase 3 — Configure & Test

See `templates/examples/transport-config.ts` for transport + env validation.

Test with MCP Inspector:
```powershell
npx @modelcontextprotocol/inspector node dist/index.js
```

## Conventions

- Always provide `title` for tools/resources/prompts
- Return `isError: true` on failure — never throw
- Import from specific SDK paths: `@modelcontextprotocol/sdk/server/mcp.js`
- ESM only: `"type": "module"` in package.json

## Gotchas

- MCP Inspector connects to stdio, SSE and Streamable HTTP servers; for HTTP start the server first and enter its URL in the Inspector
- Resource URIs must be valid
- Env validation before server start, not in tools
