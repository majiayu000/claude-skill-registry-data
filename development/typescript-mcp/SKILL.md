---
name: typescript-mcp
description: |
  Build stateless MCP servers with TypeScript on Cloudflare Workers using @modelcontextprotocol/sdk. Provides patterns for tools, resources, prompts, and authentication (API keys, OAuth, Zero Trust).

  Use when exposing APIs to LLMs, integrating Cloudflare services (D1, KV, R2, Vectorize), or troubleshooting export syntax errors, unclosed transport leaks, or CORS misconfigurations.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# TypeScript MCP on Cloudflare Workers

**Last Updated**: 2026-01-03
**Versions**: @modelcontextprotocol/sdk@1.25.1, hono@4.11.3, zod@3.24.2
**Spec Version**: 2025-11-25

---

## Quick Start

```bash
npm install @modelcontextprotocol/sdk@latest hono zod
npm install -D @cloudflare/workers-types wrangler typescript
```

**Basic MCP Server**:
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { Hono } from 'hono';
import { z } from 'zod';

const server = new McpServer({ name: 'my-mcp-server', version: '1.0.0' });

server.registerTool(
  'echo',
  {
    description: 'Echoes back input',
    inputSchema: z.object({ text: z.string() })
  },
  async ({ text }) => ({ content: [{ type: 'text', text }] })
);

const app = new Hono();

app.post('/mcp', async (c) => {
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true
  });

  // CRITICAL: Close transport to prevent memory leaks
  c.res.raw.on('close', () => transport.close());

  await server.connect(transport);
  await transport.handleRequest(c.req.raw, c.res.raw, await c.req.json());
  return c.body(null);
});

export default app; // CRITICAL: Direct export, not { fetch: app.fetch }
```

**Deploy**: `wrangler deploy`

---

## Authentication

**API Key** (KV-based):
```typescript
app.use('/mcp', async (c, next) => {
  const apiKey = c.req.header('Authorization')?.replace('Bearer ', '');
  const isValid = await c.env.MCP_API_KEYS.get(`key:${apiKey}`);
  if (!isValid) return c.json({ error: 'Unauthorized' }, 403);
  await next();
});
```

**Cloudflare Zero Trust**:
```typescript
const jwt = c.req.header('Cf-Access-Jwt-Assertion');
const payload = await verifyJWT(jwt, c.env.CF_ACCESS_TEAM_DOMAIN);
```

---

## Tasks (v1.24.0+)

Tasks enable **long-running operations** that return a handle for polling results later. Useful for expensive computations, batch processing, or operations that may need input.

**Task States**: `working` → `input_required` → `completed` / `failed` / `cancelled`

**Server Capability Declaration**:
```typescript
const server = new McpServer({
  name: 'my-server',
  version: '1.0.0',
  capabilities: {
    tasks: {
      list: {},
      cancel: {},
      requests: {
        tools: { call: {} }
      }
    }
  }
});
```

**Tool with Task Support**:
```typescript
server.registerTool(
  'long-running-analysis',
  {
    description: 'Analyze large dataset',
    inputSchema: z.object({ datasetId: z.string() }),
    execution: { taskSupport: 'optional' }  // 'forbidden' | 'optional' | 'required'
  },
  async ({ datasetId }, extra) => {
    // If invoked as task, extra.task contains taskId
    const result = await performAnalysis(datasetId);
    return { content: [{ type: 'text', text: JSON.stringify(result) }] };
  }
);
```

**Client Task Request**:
```json
{
  "method": "tools/call",
  "params": {
    "name": "long-running-analysis",
    "arguments": { "datasetId": "abc123" },
    "task": { "ttl": 60000 }
  }
}
```

**Task Lifecycle**:
1. Client sends request with `task` param → receives `taskId`
2. Client polls via `tasks/get` with `taskId`
3. When status is `completed`, client calls `tasks/result` to get output
4. Optional: Client can `tasks/cancel` to abort

📚 **Spec**: https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks

---

## Sampling with Tools (v1.24.0+)

Servers can now include **tool definitions in sampling requests**, enabling server-side agent loops.

**Use Case**: Server needs to orchestrate multi-step reasoning using LLM + tools without custom frameworks.

```typescript
// Server initiates sampling with tools available
const result = await server.requestSampling({
  messages: [{ role: 'user', content: 'Analyze this data and fetch more if needed' }],
  maxTokens: 4096,
  tools: [
    {
      name: 'fetch_data',
      description: 'Fetch additional data from API',
      inputSchema: { type: 'object', properties: { query: { type: 'string' } } }
    }
  ]
});

// Handle tool calls in response
if (result.content[0].type === 'tool_use') {
  const toolResult = await executeLocalTool(result.content[0]);
  // Continue conversation with tool result...
}
```

**Key Points**:
- Server-side agentic behavior as first-class MCP feature
- Standard MCP primitives (no custom frameworks)
- Tool definitions follow same schema as `tools/list`

📚 **Spec**: SEP-1577

---

## Cloudflare Service Tools

**D1 Database**:
```typescript
server.registerTool('query-db', {
  inputSchema: z.object({ query: z.string(), params: z.array(z.union([z.string(), z.number()])).optional() })
}, async ({ query, params }, env) => {
  const result = await env.DB.prepare(query).bind(...(params || [])).all();
  return { content: [{ type: 'text', text: JSON.stringify(result.results) }] };
});
```

**KV, R2, Vectorize**: See `references/cloudflare-integration.md`

---

## Known Issues Prevention

This skill prevents 10+ production issues documented in official MCP SDK and Cloudflare repos:

### Issue #1: Export Syntax Issues (CRITICAL)
**Error**: `"Cannot read properties of undefined (reading 'map')"`
**Source**: honojs/hono#3955, honojs/vite-plugins#237
**Why It Happens**: Incorrect export format with Vite build causes cryptic errors
**Prevention**:
```typescript
// ❌ WRONG - Causes cryptic build errors
export default { fetch: app.fetch };

// ✅ CORRECT - Direct export
export default app;
```

### Issue #2: Unclosed Transport Connections
**Error**: Memory leaks, hanging connections
**Source**: Best practice from SDK maintainers
**Why It Happens**: Not closing StreamableHTTPServerTransport on request end
**Prevention**:
```typescript
app.post('/mcp', async (c) => {
  const transport = new StreamableHTTPServerTransport(/*...*/);

  // CRITICAL: Always close on response end
  c.res.raw.on('close', () => transport.close());

  // ... handle request
});
```

### Issue #3: Tool Schema Validation Failure
**Error**: `ListTools request handler fails to generate inputSchema`
**Source**: GitHub modelcontextprotocol/typescript-sdk#1028
**Why It Happens**: Zod schemas not properly converted to JSON Schema
**Prevention**:
```typescript
// ✅ CORRECT - SDK handles Zod schema conversion automatically
server.registerTool(
  'tool-name',
  {
    inputSchema: z.object({ a: z.number() })
  },
  handler
);

// No need for manual zodToJsonSchema() unless custom validation
```

### Issue #4: Tool Arguments Not Passed to Handler
**Error**: Handler receives `undefined` arguments
**Source**: GitHub modelcontextprotocol/typescript-sdk#1026
**Why It Happens**: Schema type mismatch between registration and invocation
**Prevention**:
```typescript
const schema = z.object({ a: z.number(), b: z.number() });
type Input = z.infer<typeof schema>;

server.registerTool(
  'add',
  { inputSchema: schema },
  async (args: Input) => {
    // args.a and args.b properly typed and passed
    return { content: [{ type: 'text', text: String(args.a + args.b) }] };
  }
);
```

### Issue #5: CORS Misconfiguration
**Error**: Browser clients can't connect to MCP server
**Source**: Common production issue
**Why It Happens**: Missing CORS headers for HTTP transport
**Prevention**:
```typescript
import { cors } from 'hono/cors';

app.use('/mcp', cors({
  origin: ['http://localhost:3000', 'https://your-app.com'],
  allowMethods: ['POST', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization']
}));
```

### Issue #6: Missing Rate Limiting
**Error**: API abuse, DDoS vulnerability
**Source**: Production security best practice
**Why It Happens**: No rate limiting on MCP endpoints
**Prevention**:
```typescript
app.post('/mcp', async (c) => {
  const ip = c.req.header('CF-Connecting-IP');
  const rateLimitKey = `ratelimit:${ip}`;

  const count = await c.env.CACHE.get(rateLimitKey);
  if (count && parseInt(count) > 100) {
    return c.json({ error: 'Rate limit exceeded' }, 429);
  }

  await c.env.CACHE.put(
    rateLimitKey,
    String((parseInt(count || '0') + 1)),
    { expirationTtl: 60 }
  );

  // Continue...
});
```

### Issue #7: TypeScript Compilation Memory Issues
**Error**: `Out of memory` during `tsc` build
**Source**: GitHub modelcontextprotocol/typescript-sdk#985
**Why It Happens**: Large dependency tree in MCP SDK
**Prevention**:
```bash
# Add to package.json scripts
"build": "NODE_OPTIONS='--max-old-space-size=4096' tsc && vite build"
```

### Issue #8: UriTemplate ReDoS Vulnerability
**Error**: Server hangs on malicious URI patterns
**Source**: GitHub modelcontextprotocol/typescript-sdk#965 (Security)
**Why It Happens**: Regex denial-of-service in URI template parsing
**Prevention**: Update to SDK v1.20.2 or later (includes fix)

### Issue #9: Authentication Bypass
**Error**: Unauthenticated access to MCP tools
**Source**: Production security best practice
**Why It Happens**: Missing or improperly implemented authentication
**Prevention**: Always implement authentication for production servers (see Authentication Patterns section)

### Issue #10: Environment Variable Leakage
**Error**: Secrets exposed in error messages or logs
**Source**: Cloudflare Workers security best practice
**Why It Happens**: Environment variables logged or returned in responses
**Prevention**:
```typescript
// ❌ WRONG - Exposes secrets
console.log('Env:', JSON.stringify(env));

// ✅ CORRECT - Never log env objects
try {
  // ... use env.SECRET_KEY
} catch (error) {
  // Don't include env in error context
  console.error('Operation failed:', error.message);
}
```

---

## Deployment

```bash
# Local
wrangler dev  # http://localhost:8787/mcp

# Production
wrangler deploy
```

**Testing**: `npx @modelcontextprotocol/inspector` (connect to http://localhost:8787/mcp)

---

## Templates & References

**Templates**: `basic-mcp-server.ts`, `tool-server.ts`, `resource-server.ts`, `authenticated-server.ts`, `tasks-server.ts`, `wrangler.jsonc`

**References**: `tool-patterns.md`, `authentication-guide.md`, `testing-guide.md`, `cloudflare-integration.md`, `common-errors.md`

---

## Critical Rules

**Always**:
- ✅ Close transport on response end (`c.res.raw.on('close', () => transport.close())`)
- ✅ Use direct export (`export default app`, NOT `{ fetch: app.fetch }`)
- ✅ Implement authentication for production
- ✅ Update to SDK v1.25.1+ for security fixes and Tasks support

**Never**:
- ❌ Export with object wrapper
- ❌ Forget to close StreamableHTTPServerTransport
- ❌ Log environment variables or secrets
- ❌ Use outdated SDK versions (<1.20.2 has ReDoS vulnerability)
