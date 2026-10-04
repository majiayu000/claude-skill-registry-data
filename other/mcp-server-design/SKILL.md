---
name: mcp-server-design
description: 'Use when designing, building, or debugging a Model Context Protocol (MCP) server in Node/TypeScript. Triggers: stdio JSON-RPC handshake, tool descriptions as discovery surface, lazy startup vs eager catalog loading, telemetry placement, schema design for tool inputs (zod), tool naming conventions for discoverability, error handling that does not leak stack traces, MCP client compatibility (Claude Desktop, Claude Code, Cursor), local resource fetching, secrets and env var handling, distributing as npm + claude mcp add. NOT for MCP client implementation, MCP HTTP transport (different surface), Anthropic Agent SDK building, or non-MCP plugin systems.'
category: AI & Machine Learning
tags:
  - mcp
  - model-context-protocol
  - claude
  - server
  - jsonrpc
  - stdio
---

# MCP Server Design

The Model Context Protocol is a JSON-RPC 2.0 dialect over stdio (most commonly). The protocol is small; the design space is in *what tools you expose*, *how you describe them*, and *how the server starts up*. The descriptions are the discovery surface — a tool the client doesn't understand from its description never gets called.

## When to use

- Building an MCP server for a domain (skill catalog, code search, internal data).
- Server starts but tools don't appear in the client.
- Tool descriptions are technically accurate but the client never invokes them.
- Latency budget tight; first-call cost too high.
- Need to ship as a single npm command (`claude mcp add foo -- npx -y foo-mcp`).

## Core capabilities

### The handshake

```
client → server  initialize   { protocolVersion, capabilities, clientInfo }
server → client  result       { protocolVersion, capabilities, serverInfo }
client → server  notifications/initialized   (no response)
client → server  tools/list
server → client  result       { tools: [...] }
client → server  tools/call   { name, arguments }
server → client  result       { content: [...], isError? }
```

The high-level SDK (`@modelcontextprotocol/sdk`) handles framing. You declare tools; the SDK serializes the schema and dispatches calls.

### Minimal server with the SDK

```ts
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new McpServer({ name: 'mything', version: '1.0.0' });

server.tool(
  'mything_search',
  'Search the catalog. Returns ranked candidates with descriptions only ' +
  '(no full bodies). Pair with mything_load to fetch the chosen item. ' +
  'Local-only, no API keys.',
  {
    query: z.string().describe('Natural-language search query'),
    limit: z.number().int().min(1).max(50).optional().default(10).describe('Max results (default 10)'),
  },
  async ({ query, limit }) => {
    const results = await search(query, limit ?? 10);
    return { content: [{ type: 'text', text: JSON.stringify({ query, results }, null, 2) }] };
  },
);

await server.connect(new StdioServerTransport());
```

### Tool descriptions are the API

The model picks tools based on the description. Two rules:

1. **Lead with capability, not implementation.** "Search the catalog with a 5-stage cascade" is fine, but lead with "find the right skill for a task" because that's what the model is searching for.
2. **Tell the model when NOT to use the tool.** "Returns descriptions only — pair with mything_load for full bodies."

A discoverable description includes:
- What it does (one sentence, capability-first)
- What it returns (shape hints help the model parse)
- When to use it vs an adjacent tool
- Cost hints (local? requires download? rate-limited?)
- Zero-config caveats ("no API keys" is a strong invocation signal)

### Lazy initialization

Servers should start fast. The MCP client times out the handshake; long-loading models or large indices belong behind the first tool call.

```ts
let _catalog: Promise<Catalog> | null = null;
function ensureCatalog() {
  if (!_catalog) _catalog = loadCatalog();
  return _catalog;
}

server.tool('mything_search', '...', schema, async (args) => {
  const cat = await ensureCatalog();
  // ... use cat ...
});
```

Print a status line to stderr at startup so logs in the client are interpretable:

```ts
console.error(`[mything] ${count} items, telemetry=${mode}, version=${VERSION}`);
```

stdout is reserved for JSON-RPC frames. Anything you accidentally log there breaks the client.

### Schema design with zod

```ts
const SearchInput = {
  query: z.string().min(1).max(500).describe('Natural-language query'),
  limit: z.number().int().min(1).max(50).optional().default(10),
  category: z.enum(['frontend', 'backend', 'devops']).optional(),
};
```

Constraints (`min`, `max`, `enum`) become tool-input metadata the client surfaces. The model uses them to decide which arguments to fill.

### Returning content

```ts
return {
  content: [
    { type: 'text', text: 'Markdown body here' },
    { type: 'text', text: 'Structured JSON:\n```json\n' + JSON.stringify(data) + '\n```' },
  ],
};

// On error:
return {
  content: [{ type: 'text', text: JSON.stringify({ error: msg }, null, 2) }],
  isError: true,
};
```

JSON inside a text block is a workable convention; the model can parse it. Avoid throwing — return `isError: true` instead so the client gets a typed error.

### Handling secrets

Servers run in the user's environment. `process.env` works, but:

- Document required env vars in the README.
- Fail fast at startup if a required secret is missing — don't fail the first tool call.
- Never log the secret value, even truncated.

```ts
const apiKey = process.env.MY_API_KEY;
if (!apiKey) {
  console.error('MY_API_KEY required. Set in your shell or in claude mcp config.');
  process.exit(2);
}
```

### Path-traversal safety for file tools

If a tool reads a file by path:

```ts
const root = path.resolve(skillsDir, skillId);
const requested = path.resolve(root, filePath.replace(/^\//, ''));
if (!requested.startsWith(root + path.sep)) {
  return { content: [{ type: 'text', text: 'invalid path' }], isError: true };
}
```

This is the #1 vulnerability in file-reading tools. Test with `../../../../etc/passwd`.

### Telemetry placement

If you record analytics, do it fire-and-forget at the top of each tool handler:

```ts
server.tool('mything_search', '...', schema, async (args) => {
  recordEvent({ tool: 'mything_search', taskText: args.query });
  // ... work ...
});
```

Never block on telemetry. Wrap in a 1.5s AbortController. Default to anonymous. Document `WINDAGS_TELEMETRY=off` (or your equivalent) prominently.

### Distribution

Three install patterns:

```bash
# 1. npm global
npm install -g mything-mcp
claude mcp add mything -- mything-mcp

# 2. npx (no install)
claude mcp add mything -- npx -y mything-mcp@latest

# 3. From a plugin marketplace
claude plugin marketplace add yourorg/your-skills
claude plugin install your-skills
```

For (2), include `"bin": { "mything-mcp": "./index.js" }` in package.json with a shebang on `index.js`. For (3), the plugin manifest declares the MCP server alongside skills/commands.

### Testing the handshake

```ts
// scripts/handshake-test.mjs
import { spawn } from 'node:child_process';

const proc = spawn('node', ['./index.js']);
function send(msg) { proc.stdin.write(JSON.stringify(msg) + '\n'); }

send({ jsonrpc: '2.0', id: 1, method: 'initialize',
       params: { protocolVersion: '2024-11-05', capabilities: { tools: {} }, clientInfo: { name: 't', version: '1' } }});
send({ jsonrpc: '2.0', method: 'notifications/initialized' });
send({ jsonrpc: '2.0', id: 2, method: 'tools/list', params: {} });

proc.stdout.on('data', (b) => {
  for (const line of b.toString().split('\n')) {
    if (!line.trim()) continue;
    const msg = JSON.parse(line);
    if (msg.id === 2) {
      console.log('tools:', msg.result.tools.map((t) => t.name).join(','));
      process.exit(0);
    }
  }
});
setTimeout(() => { console.error('timeout'); process.exit(1); }, 30_000);
```

Run this in CI on every commit. It catches startup regressions before they reach users.

## Anti-patterns

### Logging to stdout

**Symptom:** Client says "invalid JSON-RPC frame" or "unexpected character".
**Diagnosis:** Anything written to stdout after `connect` corrupts the frame stream.
**Fix:** All non-protocol output → stderr. Audit `console.log` and any logger that defaults to stdout.

### Eager loading at startup

**Symptom:** Client times out the handshake; tool list never appears.
**Diagnosis:** Loading a 100MB index synchronously at boot.
**Fix:** Lazy-load behind first tool call. Print a one-liner status to stderr; do real work later.

### Tool description that reads like a docstring

**Symptom:** Model doesn't invoke the tool even when the query matches its purpose.
**Diagnosis:** Description starts with "This tool will..." instead of the capability.
**Fix:** Lead with the verb. "Find skills relevant to a task." Then implementation details.

### Path traversal vulnerability

**Symptom:** Reading a file by `skill_id` + `file_path` lets the user escape the skill dir.
**Diagnosis:** No `startsWith` check after path resolution.
**Fix:** `path.resolve` both, then `startsWith(root + path.sep)`. Test with `../../../etc/passwd`.

### Secret leak in error message

**Symptom:** A failed call returns `"invalid auth: Bearer sk_live_..."` to the client.
**Diagnosis:** Error formatting includes the auth header verbatim.
**Fix:** Sanitize errors at the tool boundary. Return generic messages; log the detailed error to stderr.

### Tool that does too much

**Symptom:** Model wastes turns trying to figure out which arguments to pass.
**Diagnosis:** One tool with 12 optional args covering 3 unrelated capabilities.
**Fix:** Split into 3 tools with focused schemas. Cross-reference each in their descriptions.

## Quality gates

- [ ] Handshake test runs in CI on every commit.
- [ ] Server starts in <100ms (heavy work behind first tool call).
- [ ] No stdout writes after `connect`.
- [ ] Every tool description includes capability, return shape, and when-not-to-use.
- [ ] Path-traversal test (`../../../etc/passwd`) returns an error.
- [ ] Required env vars validated at startup with actionable error.
- [ ] Telemetry fire-and-forget; never blocks tool response.
- [ ] Tool inputs validated by zod with `min`/`max`/`enum` constraints.
- [ ] Errors return `isError: true`, not thrown exceptions.
- [ ] Distribution path tested: install + register + handshake on a clean machine.

## NOT for

- **MCP client implementation** — different surface; pair with the MCP-client skill.
- **MCP HTTP transport** — same protocol but different framing concerns.
- **Anthropic Agent SDK** — building agents, not protocol servers.
- **Non-MCP plugin systems** (LSP, VS Code extensions) — different protocols.
- **MCP resource subscriptions** — separate area, see resources/list and notifications/resources/updated.
