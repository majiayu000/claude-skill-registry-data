---
name: typescript-server
description: Build, extend, test and migrate Model Context Protocol (MCP) servers in TypeScript with the official v2 SDK (@modelcontextprotocol/server 2.x) and the 2026-07-28 protocol revision. Covers registerTool/registerResource/registerPrompt with zod 4 or Standard Schema, outputSchema + structuredContent, isError tool results versus protocol errors, resource templates that list, serveStdio versus server.connect, stdout hygiene on stdio, progress and cancellation through ctx.mcpReq, Streamable HTTP via createMcpHandler, and porting v1 (@modelcontextprotocol/sdk) code. Use when writing or reviewing an MCP server or tool in Node/TypeScript, adding MCP tools, resources or prompts, upgrading the MCP SDK, or debugging "server.tool is not a function", "Cannot find package '@modelcontextprotocol/sdk'", "Schema appears to be from zod 3", "has an output schema but no structured content", ERA_NEGOTIATION_FAILED, or a host that cannot connect on 2026-07-28.
license: MIT
---

# MCP servers with the TypeScript SDK (v2)

Facts below were checked against `@modelcontextprotocol/server@2.4.0`, `@modelcontextprotocol/client@2.4.0`,
`zod@4.6.7` and the 2026-07-28 specification (the current revision). Re-check `package.json` before you
trust anything else, including your own memory: most MCP code on the internet is v1.

## 1. Decide which SDK line you are on

Look at `package.json` first and write code for what is installed.

| Dependency present | API line | Notes |
| --- | --- | --- |
| `@modelcontextprotocol/server` 2.x (+ `@modelcontextprotocol/client` 2.x) | **v2** | Current. Released 2026-07-27. Requires `zod >= 4.2`, Node 20+. |
| `@modelcontextprotocol/sdk` 1.x | v1 | Maintenance line (bug and security fixes for at least six months after v2). Speaks protocol revisions up to 2025-11-25 only. |

Rules:

- New servers: v2. Never mix the two lines in one package.
- A repo already on v2 with v1-style code is a **port**, not a reason to reinstall
  `@modelcontextprotocol/sdk`. v1 cannot serve 2026-07-28 clients at all.
- Import paths in v2 have no `.js` suffix and no `sdk/server/...` segments. See the table in section 9.

## 2. The minimal correct v2 stdio server

```ts
import { McpServer } from '@modelcontextprotocol/server'
import { serveStdio } from '@modelcontextprotocol/server/stdio'
import * as z from 'zod' // zod 4; 'zod/v4' also works. Never 'zod/v3'.

export function createServer(): McpServer {
  const server = new McpServer({ name: 'orders', version: '1.0.0' })

  server.registerTool(
    'get_order',
    {
      title: 'Get order',
      description: 'Look up one order by id.',
      inputSchema: z.object({ id: z.string().describe('Order id, e.g. "o-1001"') }),
      annotations: { readOnlyHint: true },
    },
    async ({ id }, ctx) => {
      const order = await findOrder(id, ctx.mcpReq.signal)
      if (!order) {
        return { content: [{ type: 'text', text: `No order "${id}". Use list_orders to find ids.` }], isError: true }
      }
      return { content: [{ type: 'text', text: `${order.id}: ${order.status}` }] }
    },
  )

  return server
}

serveStdio(createServer) // serves 2025-era AND 2026-07-28 clients from one factory
console.error('orders MCP server ready') // stderr only, never stdout
```

Why each line matters:

- `serveStdio(factory)` is the stdio entry that negotiates the protocol era per connection. The older
  wiring `await server.connect(new StdioServerTransport())` still exists and still compiles, but it only
  speaks the 2025 `initialize` handshake. A client pinned to 2026-07-28 gets
  `SdkError ERA_NEGOTIATION_FAILED` against it. Most tutorials, and the v2 README quick start, still
  show `connect`; do not copy that when a modern host must connect.
- Register everything inside the factory. Keep expensive shared state (data, pools) at module level
  and close over it.
- `console.error`/`process.stderr` for logs. The spec says the server MUST NOT write anything to stdout
  that is not an MCP message.

## 3. Tools

### Registration

`server.registerTool(name, config, handler)`. Config keys: `title`, `description`, `inputSchema`,
`outputSchema`, `annotations`, `icons`, `_meta`.

| You have | Pass | Handler signature |
| --- | --- | --- |
| zod 4 object | `inputSchema: z.object({...})` | `(args, ctx)` |
| other Standard Schema (Valibot, ArkType) | the schema object | `(args, ctx)` |
| a JSON Schema literal | `inputSchema: fromJsonSchema(jsonSchema)` | `(args, ctx)` |
| no parameters | omit `inputSchema` | `(ctx)` - **first argument is the context** |
| raw shape `{ q: z.string() }` | works, but `@deprecated`; wrap in `z.object` | `(args, ctx)` |

A raw JSON Schema object passed straight to `inputSchema` throws a `TypeError` at registration
("must be a Standard Schema"). zod 3 schemas type-check against loose types but fail at the first
`tools/list` with "Schema appears to be from zod 3".

Schema details that change what clients see:

- `.default(x)` and `.optional()` fields are left out of `required`. Use `.default()` when the handler
  needs a value, so the default lives in one place.
- Put constraints in the schema (`.int().min(1).max(50)`, `.trim().min(1)`). Failing input never
  reaches the handler: the SDK answers with an `isError: true` result whose text names the field,
  which the model can read and correct.
- `.describe()` every parameter. Descriptions are the model's only documentation.
- Tool names: 1-128 characters from `A-Z a-z 0-9 _ - .`, no spaces, unique per server, case-sensitive.

### Results and errors

Two different failure channels exist; pick deliberately.

| Situation | Do | What the client sees |
| --- | --- | --- |
| Expected domain failure (not found, invalid combination, upstream 4xx) | `return { content: [{ type: 'text', text: '<what went wrong + how to recover>' }], isError: true }` | normal result, `isError: true`; the model can retry |
| Bug or unexpected exception inside the handler | let it throw | SDK converts it to `isError: true` with the message as text |
| Unknown tool name, malformed request | nothing, the SDK does it | JSON-RPC error `-32602`; `client.callTool` rejects |

Return `isError` yourself for expected failures: you control the message, and a thrown error leaks
whatever the exception text happened to be. Never return a "not found" message as a successful
result: hosts and models treat it as data.

### Structured output

```ts
const Order = z.object({ id: z.string(), status: z.enum(['open', 'shipped']), totalCents: z.number().int() })

server.registerTool(
  'get_order',
  { description: 'Look up one order', inputSchema: z.object({ id: z.string() }), outputSchema: Order },
  async ({ id }) => {
    const order = await findOrder(id)
    if (!order) return { content: [{ type: 'text', text: `No order ${id}` }], isError: true }
    const output = { id: order.id, status: order.status, totalCents: order.totalCents }
    return {
      content: [{ type: 'text', text: JSON.stringify(output) }], // for clients that ignore structuredContent
      structuredContent: output,
    }
  },
)
```

- Declaring `outputSchema` makes `structuredContent` mandatory on every non-error result. Missing it
  turns the call into `isError: true` "has an output schema but no structured content was provided";
  a value that does not match becomes "Invalid structured content". Error results skip this check.
- Keep a text block too (the spec says SHOULD): a JSON string, or a readable summary when people read
  the transcript.
- `outputSchema` may have a non-object root (array, string) in v2. On the client,
  `structuredContent` is typed `unknown`: test `=== undefined`, then narrow.

### Annotations

`annotations: { readOnlyHint, destructiveHint, idempotentHint, openWorldHint }` (all booleans). They
tell hosts whether to ask the user before calling; they never change execution, and clients treat
them as untrusted. Set `readOnlyHint: true` on every tool that only reads.

## 4. Resources

```ts
import { ResourceNotFoundError, ResourceTemplate } from '@modelcontextprotocol/server'

server.registerResource(
  'order',
  new ResourceTemplate('orders://{id}', {
    list: async () => ({
      resources: orders.map((o) => ({ uri: `orders://${o.id}`, name: o.id, title: o.label, mimeType: 'application/json' })),
    }),
  }),
  { title: 'Order', mimeType: 'application/json' }, // metadata argument is required; {} if none
  async (uri, { id }) => {
    const order = orders.find((o) => o.id === id)
    if (!order) throw new ResourceNotFoundError(uri.href)
    return { contents: [{ uri: uri.href, mimeType: 'application/json', text: JSON.stringify(order) }] }
  },
)
```

- `ResourceTemplate`'s `list` key is required on purpose. `list: undefined` means the resources exist
  but `resources/list` will not show them. If clients should discover them, pass a function.
- Static resources: `registerResource(name, 'config://app', metadata, async (uri) => ...)`.
- Resource and prompt callbacks have no `isError` channel. A missing item must **throw**:
  `ResourceNotFoundError` (code -32602, URI in `data`) or `ProtocolError(ProtocolErrorCode.InvalidParams, msg)`.
  Any other exception surfaces as -32603. Returning empty `contents` or a "not found" text is a bug.
- Template variables arrive as `string | string[]`; narrow before use. Set `mimeType` on both the
  listed entries and the contents.

## 5. Prompts

```ts
server.registerPrompt(
  'review_order',
  { description: 'Draft a reply about one order', argsSchema: z.object({ id: z.string() }) },
  ({ id }) => ({ messages: [{ role: 'user', content: { type: 'text', text: `Draft a reply about order ${id}.` } }] }),
)
```

Unknown arguments: throw `ProtocolError(ProtocolErrorCode.InvalidParams, ...)`. Use `completable(schema, fn)`
on an `argsSchema` field to offer argument completion.

## 6. The request context (`ctx`)

| Need | v2 | v1 equivalent (do not use) |
| --- | --- | --- |
| cancellation | `ctx.mcpReq.signal` (AbortSignal) | `extra.signal` |
| progress token | `ctx.mcpReq._meta?.progressToken` | `extra._meta?.progressToken` |
| send progress | `await ctx.mcpReq.notify({ method: 'notifications/progress', params: { progressToken, progress, total } })` | `extra.sendNotification(...)` |
| auth info (HTTP) | `ctx.http?.authInfo` | `extra.authInfo` |
| request headers (HTTP) | `ctx.http?.req?.headers.get('x-…')` | `extra.requestInfo?.headers[...]` |
| log to the client | `ctx.mcpReq.log(level, data)`: **deprecated** in 2026-07-28 (SEP-2577) | `server.sendLoggingMessage` (also deprecated) |
| ask the user / sample the model | return `inputRequired({ inputRequests: { k: inputRequired.elicit({...}) } })` | `ctx.mcpReq.elicitInput` / `requestSampling` throw on 2026-07-28 requests |

Only send progress when a `progressToken` was supplied, and keep `progress` increasing. Check
`signal.aborted` (or `signal.throwIfAborted()`) inside loops; after cancellation send nothing more for
that request. For logging on stdio, write to stderr; hosts capture it.

## 7. Transports and protocol eras

The 2026-07-28 revision replaced the `initialize` handshake with per-request `_meta` and a
`server/discover` call. Servers that must work with both generations:

| Transport | Entry | Eras |
| --- | --- | --- |
| stdio | `serveStdio(factory, { legacy: 'serve' })` from `@modelcontextprotocol/server/stdio` | both (default); `legacy: 'reject'` = modern only |
| stdio, old wiring | `server.connect(new StdioServerTransport())` | 2025 only |
| HTTP (Workers, Deno, Bun, Hono) | `createMcpHandler(factory)` then `handler.fetch(request)` | both; stateless fallback for 2025 |
| HTTP (node:http, Express, Fastify) | `toNodeHandler(createMcpHandler(factory))` from `@modelcontextprotocol/node` | both |

HTTP details (Host/Origin validation, sessions, auth) are in
[references/http-and-eras.md](references/http-and-eras.md). `SSEServerTransport` is gone in v2.

## 8. stdout hygiene on stdio

- Nothing but JSON-RPC lines on stdout: no `console.log`, no banners, no `console.table`, no
  progress bars, no dependency that prints on import. `console.error` is fine.
- The v2 **client** silently skips non-JSON stdout lines, so your own SDK-based tests stay green while
  Claude Desktop-style hosts and other SDKs break. Test the raw stream (see the testing reference).
- The server should exit when stdin closes. The SDK transport closes on EOF; do not hold the event
  loop open with timers or watchers you never clear (clear them in `server.server.onclose`).

## 9. Porting v1 code to v2

Do these in order, then run the type checker and the tests.

1. Imports:

   | v1 | v2 |
   | --- | --- |
   | `@modelcontextprotocol/sdk/server/mcp.js` (`McpServer`, `ResourceTemplate`) | `@modelcontextprotocol/server` |
   | `@modelcontextprotocol/sdk/server/stdio.js` | `@modelcontextprotocol/server/stdio` (`serveStdio`, `StdioServerTransport`) |
   | `@modelcontextprotocol/sdk/types.js` (`McpError`, `ErrorCode`) | `@modelcontextprotocol/server` (`ProtocolError`, `ProtocolErrorCode`) |
   | `@modelcontextprotocol/sdk/client/index.js`, `.../client/stdio.js` | `@modelcontextprotocol/client`, `@modelcontextprotocol/client/stdio` |
   | `StreamableHTTPServerTransport` | `NodeStreamableHTTPServerTransport` (`@modelcontextprotocol/node`) or `createMcpHandler` |

2. `server.tool(name, description, shape, cb)` -> `server.registerTool(name, { description, inputSchema: z.object(shape) }, cb)`.
   An annotations positional argument becomes `annotations:` in the config.
3. `server.resource(name, uriOrTemplate, cb)` -> `server.registerResource(name, uriOrTemplate, {}, cb)`.
4. `server.prompt(name, description, shape, cb)` -> `server.registerPrompt(name, { description, argsSchema: z.object(shape) }, cb)`.
5. `extra` -> `ctx` per the table in section 6. A tool with no `inputSchema` now receives `ctx` first:
   either keep `inputSchema: z.object({})` with `(_args, ctx)` or change the handler to `(ctx)`.
6. `McpError`/`ErrorCode` -> `ProtocolError`/`ProtocolErrorCode`. Remember tool handlers turn any throw
   into `isError`; resource/prompt callbacks surface it as a JSON-RPC error.
7. Low-level `server.setRequestHandler(CallToolRequestSchema, …)` -> `setRequestHandler('tools/call', …)`.
8. zod 3 pins -> zod `>= 4.2`. The SDK converts schemas to JSON Schema itself; MCP code no longer
   needs `zod-to-json-schema`.
9. Wiring -> `serveStdio(createServer)` if any client speaks 2026-07-28.
10. Behaviour changes to re-test: unknown tools now reject instead of returning `isError`; list calls
    without a cursor auto-paginate; `structuredContent` is `unknown` on the client.

Full map, including client-side and auth changes: [references/v1-to-v2.md](references/v1-to-v2.md).

## 10. Verify before you say it works

Run the type checker (`npx tsc -p .` or the repo's script) and an end-to-end test that spawns the
server over stdio with the official client. Check, at minimum:

- [ ] `listTools()` shows each tool, `required` lists exactly the mandatory parameters, `outputSchema` present where declared.
- [ ] A valid call returns the expected `content` and `structuredContent`.
- [ ] Bad input and domain failures return `isError: true` with a readable message; the server keeps serving.
- [ ] Resources you expect to be discoverable appear in `listResources()`; unknown URIs reject.
- [ ] Connect once with the default client and once with `versionNegotiation: { mode: { pin: '2026-07-28' } }` if modern hosts matter.
- [ ] Raw stdout contains only JSON-RPC lines; the process exits after stdin closes.

Copy-paste harness: [references/testing.md](references/testing.md).

## Anti-patterns

| Anti-pattern | Fix |
| --- | --- |
| `server.tool(...)`, `server.resource(...)`, `server.prompt(...)` | `registerTool` / `registerResource` / `registerPrompt` |
| `inputSchema: { type: 'object', properties: {...} }` | `z.object({...})`, or `fromJsonSchema(...)` for real JSON Schema |
| `import { z } from 'zod/v3'` or zod 3.x pinned | zod `>= 4.2`, `import * as z from 'zod'` |
| `outputSchema` declared, only text returned | return `structuredContent` that matches, plus a text block |
| "not found" returned as a normal tool result | `isError: true` with a recovery hint |
| resource callback returns `{ contents: [] }` for a missing item | throw `ResourceNotFoundError(uri.href)` |
| `new ResourceTemplate(uri, { list: undefined })` for things clients must find | pass a `list` function |
| `console.log` anywhere in a stdio server | `console.error` |
| `await server.connect(new StdioServerTransport())` when a host speaks 2026-07-28 | `serveStdio(createServer)` |
| `(_args, ctx)` handler on a tool with no `inputSchema` | `(ctx)`, or add `inputSchema: z.object({})` |
| `extra.sendNotification` / `extra.signal` | `ctx.mcpReq.notify` / `ctx.mcpReq.signal` |
| `server.sendLoggingMessage` for diagnostics | stderr (stdio) or OpenTelemetry |
| reinstalling `@modelcontextprotocol/sdk` to make old code run | port to v2 |

Sources and dates: [references/sources.md](references/sources.md).
