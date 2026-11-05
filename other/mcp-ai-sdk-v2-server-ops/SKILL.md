---
name: mcp-ai-sdk-v2-server-ops
description: Operational playbook for building and debugging MCP HTTP servers on the @modelcontextprotocol/server v2 SDK — the dual-era wire model (2026-07-28 modern dialect vs the 2025-era stateless fallback), the exact modern request shape (params._meta envelope keys, SEP-2243 MCP-Protocol-Version/Mcp-Method/Mcp-Name headers, server/discover replacing initialize), the validation ladder and its HTTP status mapping, the createMcpHandler + toNodeHandler factory contract (and the registerTool-returns-tool gotcha), layering auth and guards outside the SDK entry, the node:http conformance-test recipe, and how to re-derive shapes from the minified dist sources when the SDK changes. Use when serving MCP over Streamable HTTP with the SDK v2, debugging 400/-32020/-32602/500 responses from an MCP endpoint, writing handshake conformance tests, or upgrading a legacy initialize-only server to dual-era serving.
---

# MCP SDK v2 Server Ops — dual-era wire playbook

## What this is

How to run an MCP **server** on `@modelcontextprotocol/server` v2.x
(`createMcpHandler` + `McpServer`) so it speaks **both** protocol eras the
SDK serves, and how to debug it when requests come back 400/500. Everything
below was reverse-engineered from the shipped dist and verified over a real
socket (2026-10-30, SDK 2.4.0 / `@modelcontextprotocol/node` 2.1.2). The
working reference implementation is `examples/nvoos-astro-velocity/mcp/`
(Proposal 095, PR #7301) — read it alongside this skill.

## The two eras in one endpoint

| | 2026-07-28 (modern) | 2025-era (legacy) |
|---|---|---|
| Negotiation | **`server/discover`** (there is NO `initialize` in the modern era) | `initialize` with `params.protocolVersion` |
| Per-request identity | `params._meta` envelope + SEP-2243 headers | sessionless (stateless fallback) |
| Response | `application/json`, `resultType: "complete"` stamp | `text/event-stream` |
| NV oOS MCP Apps client | `PROTOCOL_VERSION='2026-07-28'` — it speaks modern | fallback only |

`createMcpHandler(factory, { legacy: 'stateless' })` serves modern requests
natively and routes claim-less 2025 traffic to a per-request stateless
fallback (GET/DELETE → 405). `legacy: 'reject'` = modern-only endpoint (the
`isLegacyRequest(request)` export lets you branch by era in user land).

## Modern request shape (exact)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "ping",
    "arguments": { "echo": "hi" },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

Headers (SEP-2243 — **required on every modern request POST**):

| Header | When required | Rule |
|---|---|---|
| `MCP-Protocol-Version` | always | must name a supported modern revision; must equal the envelope's claim |
| `Mcp-Method` | always | must equal the body `method` |
| `Mcp-Name` | `tools/call`, `prompts/get`, `resources/read`, `tasks/get|update|cancel` | must equal `params.name` / `params.uri` / `params.taskId` |

Rules that cost real debugging time:

- The envelope lives in **`params._meta`**, NOT at the JSON-RPC top level.
  The claim key is `io.modelcontextprotocol/protocolVersion` — **not**
  `spec-version` (that key was a wrong guess from an early session).
- Required envelope keys: `protocolVersion` + `clientCapabilities`
  (`{}` is valid — all capability fields are optional). `clientInfo` is
  optional (demoted to SHOULD by spec PR #3002).
- **Notifications are exempt** from the standard headers (envelope still
  required).
- `server/discover` result carries `supportedVersions` (modern revisions
  only — 2025 versions are negotiated via `initialize`, never listed).
- Every modern result is stamped `resultType: "complete"` (+
  `io.modelcontextprotocol/serverInfo` in `_meta`).
- A legacy `initialize` POST sent with a modern `MCP-Protocol-Version`
  header is rejected: **400 / -32020** ("an initialize request (legacy
  handshake) was sent with a modern MCP-Protocol-Version header").

## The validation ladder (what each failure looks like)

Order observed by the entry: era-classification → envelope → standard-header
→ client-capabilities → method-registry → request-params (in-band).
Ladder-origin errors map to HTTP statuses (`LADDER_ERROR_HTTP_STATUS`);
handler-produced errors stay **in-band on HTTP 200**.

| Symptom | Cause | Answer |
|---|---|---|
| 400 `-32020` "headers and body disagree" | missing/mismatched `Mcp-Method`, `Mcp-Name`, `MCP-Protocol-Version`; legacy initialize + modern header | fix headers, not the body |
| 400 `-32602` "missing the required per-request envelope key(s)" | envelope absent or keys missing (modern header present, no claim) | add `params._meta` |
| 400 `-32022` Unsupported protocol version | claim-less request on a modern-only endpoint | send the envelope (or keep `legacy: 'stateless'`) |
| 400 `-32600` invalid body / `-32700` | body not valid JSON-RPC / unreadable | check Content-Type `application/json` too (415) |
| **500 `-32603` on EVERY request** | **the factory returned the wrong thing** — see the `registerTool` gotcha below | fix the factory |

## Wiring recipe (`createMcpHandler` + `toNodeHandler`)

```ts
import { McpServer, createMcpHandler } from '@modelcontextprotocol/server';
import { toNodeHandler, hostHeaderValidation, originValidation } from '@modelcontextprotocol/node';

const handler = createMcpHandler(() => buildServer(), {
  legacy: 'stateless', // or 'reject'
  onerror: (error) => console.error('[mcp]', error.message), // NEVER omit: 500s are silent otherwise
});
const nodeHandler = toNodeHandler(handler); // optional 3rd arg: pre-parsed body (see below)
```

- **Factory contract differs per era.** The legacy fallback calls
  `await product.connect(transport)` **directly on the factory result**; the
  modern path unwraps with
  `product instanceof McpServer ? product.server : product`. Return a fresh
  `McpServer` per call (stateless), and return the `McpServer` itself — see
  the gotcha.
- **`McpServer.registerTool(name, config, cb)` returns the registered tool
  record, NOT the server.** Chaining `.registerTool(...)` inside a factory
  (`new McpServer(...).registerTool(...)`) returns the tool → the handler
  crashes with `TypeError: Cannot read properties of undefined (reading
  '_supportedProtocolVersions')` → silent 500s. Assign to a variable and
  return the server.
- **Read the body first only if you pass it back:** if your wrapper drains
  the Node stream (auth inspection), pass the parsed body as
  `toNodeHandler(handler)(req, res, parsedBody)` — the SDK would otherwise
  clone an already-consumed stream. `bff.ts` in the storefront does exactly
  this.
- **Auth and guards live OUTSIDE the SDK entry.** The handler is
  deliberately validation-free (no token verification; `authInfo` is
  pass-through only). Put `hostHeaderValidation` / `originValidation`
  (non-browser clients send no Origin and pass) and your own token/session
  gate in front; answer denials yourself with a JSON-RPC error body (401,
  `-32001`) and **never** fall through.
- `onerror` is reporting-only — a 500 already happened; always set it to see
  the real exception.

## Conformance-test recipe (vitest + node:http)

Spin a real socket with the actual handler and POST raw JSON-RPC — no mocks
(see `examples/nvoos-astro-velocity/tests/mcp/handshake.test.ts`):

1. `createServer((req, res) => void handler(req, res))` on an ephemeral
   port; build the handler once per describe.
2. Cover **both eras**: `server/discover` (assert `supportedVersions`
   contains the modern revision + `resultType`), claim-less legacy
   `initialize` (assert `text/event-stream` + negotiated 2025 version),
   the legacy-initialize+modern-header 400 boundary, modern `tools/list`
   and `tools/call` with all three SEP-2243 headers, and one ladder
   rejection (e.g. missing `Mcp-Name`).
3. SSE parse helper: split on `\n`, keep `data: ` lines, join + `JSON.parse`
   (single-event responses only).
4. Write-auth tests: build a second server with a token env and assert
   401 fail-closed without credentials.

## Re-deriving shapes when the SDK changes

The `dist/` files are minified but greppable (and `node_modules` is excluded
from editor reads — use the terminal):

- `@modelcontextprotocol/server/dist/index.mjs` — `createMcpHandler`,
  `classifyEntryRequest`, `isLegacyRequest`, `standardHeadersOf`,
  `serveModern`/`serveLegacyRoute`, `createLegacyStatelessFallback`.
- `.../dist/src-DdvbAHrR.mjs` — `classifyInboundRequest`,
  `validateStandardRequestHeaders`, `MCP_NAME_HEADER_SOURCE`,
  `REQUIRED_ENVELOPE_KEYS`, `LADDER_ERROR_HTTP_STATUS`,
  `RequestMetaEnvelopeSchema`, `SUPPORTED_PROTOCOL_VERSIONS`.
- `.../dist/mcp-oHn3ureC.mjs` — `McpServer` wrapper (`.server` property),
  `installModernOnlyHandlers`, `registerTool` return value.

A 20-line probe script (real `node:http` + `fetch`) beats reading the code —
but get the **factory right first**: a broken factory produces misleading
500s that look like wire-shape failures. This exact trap wasted the
handshake session that produced this skill.

## References

- `examples/nvoos-astro-velocity/mcp/bff.ts` — canonical dual-era wiring
- `examples/nvoos-astro-velocity/tests/mcp/handshake.test.ts` — conformance suite
- `docs/project/proposals/095-astro-design-system-mcp-research.md` — SDK v2 selection rationale
- Related: `mcp-ai-wpoos-astro-storefront` (storefront ops), `mcp-ai-artcraft-ops` (generic MCP handshake debugging for third-party servers)
