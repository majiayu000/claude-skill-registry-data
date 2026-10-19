---
name: mcp-server-development
description: >
  Build, test, debug, and secure Model Context Protocol (MCP) servers that expose
  tools, resources, and prompts to AI clients. Use when writing a custom MCP server
  with the TypeScript or Python SDK, choosing between stdio and Streamable HTTP,
  validating tool inputs, hardening a local or remote server (Origin checks,
  localhost binding, OAuth resource-server rules, path and command safety), migrating
  an older HTTP+SSE or SDK v1 server, or debugging a server with the MCP Inspector.
  Do not use for configuring or consuming existing MCP servers in a client (that is
  client configuration), for building non-MCP REST APIs, or for generic agent-skill
  authoring.
compatibility: >
  Agent Skills-compatible coding agents implementing MCP servers in TypeScript
  (Node.js) or Python 3.10+. Protocol facts checked against spec revision 2026-07-28
  and the official SDK READMEs in October 2026; re-check SDK docs before pinning versions.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "mcp, model-context-protocol, ai-agents, tools, resources, stdio, streamable-http, zod, security"
  topics: "ai-agents, devtools, software-development"
---

# Model Context Protocol (MCP) Server Development

The [Model Context Protocol](https://modelcontextprotocol.io/) is an open JSON-RPC 2.0 protocol that lets AI clients call tools, read resources, and fetch prompts from servers. A server is code you write; the client and the model are not trusted to behave. Design every tool as if its arguments were hostile.

Deeper material:
- [Protocol architecture, primitives, revisions](references/mcp-spec-guide.md)
- [Transports, versions, and migration (HTTP+SSE, SDK v1 to v2, stateless revision)](references/transports-and-migration.md)
- [Troubleshooting a server that will not connect or misbehaves](references/troubleshooting.md)

## When to use / not use

Use this skill to design, write, harden, test, or migrate an MCP server. Do not use it to wire an existing server into Claude Desktop/Cursor/etc. (client config), and do not use it for REST/GraphQL APIs that merely sit next to an MCP server. For auditing third-party agent extensions see `skill-security-audit`; for reviewing server code for vulnerabilities see `security-code-review`.

## Version facts to check first (they change)

- The latest spec revision at time of writing is **2026-07-28** (previous: 2025-11-25, 2025-06-18, 2025-03-26, 2024-11-05). Always confirm at `modelcontextprotocol.io/specification/latest`.
- Transports defined by the spec: **stdio** and **Streamable HTTP**. The 2024-11-05 **HTTP+SSE** transport is deprecated since 2025-03-26 and must not be used for new servers. A bare "SSE transport" in older tutorials means that deprecated transport.
- Revision 2026-07-28 made MCP stateless: no `initialize` handshake, no `Mcp-Session-Id`, no standalone GET stream; each POST carries protocol version and client capabilities in `_meta`. Servers must implement `server/discover`. Older clients still speak the 2025-xx shape, so a public server decides deliberately which eras it supports (see the migration reference).
- TypeScript SDK: current line publishes `@modelcontextprotocol/server` (and `/client`); the older v1 line is `@modelcontextprotocol/sdk` on the `v1.x` branch. Python SDK: PyPI package `mcp` (v2 line; `MCPServer` in `mcp.server`; v1 exposed `FastMCP` in `mcp.server.fastmcp`). Read the SDK README for the version you install; do not mix v1 and v2 imports.

## Core rules

1. **Validate every argument** with a schema (Zod/Standard Schema in TypeScript, type hints/Pydantic in Python) and re-check semantic limits (ranges, allowed enums, path containment) in handler code. A JSON Schema alone does not enforce policy.
2. **stdio: stdout is the protocol channel.** Any `console.log`/`print` corrupts framing. Log to stderr or a file.
3. **Least capability per tool.** One narrow, typed tool beats `run_command`/`execute_sql`. Never build shell strings from arguments; call executables with an argument array.
4. **Pick the right primitive.** Tools are model-invoked actions; resources are application-controlled read-only context; prompts are user-invoked templates.
5. **Tool failures are results, not crashes.** Return `isError: true` with a short, non-secret message for execution failures; use protocol errors for malformed requests. Never leak stack traces, tokens, or absolute server paths.
6. **Annotations are hints, not enforcement.** `readOnlyHint`/`destructiveHint` help clients prompt users, but a client may ignore them and a malicious server can lie. Enforce authorization in the server.
7. **Treat tool output as untrusted data on the client side and as a prompt-injection channel on yours.** Do not return fetched web or file content that you have not bounded in size, and never put secrets into tool results.
8. **Remote servers need transport security** (below). Local convenience defaults are not safe on a network.

## Workflow

1. **Define the surface**: list the 3-10 verbs users need. For each, decide tool vs resource vs prompt, inputs, side effects (read-only, idempotent write, destructive), and who may call it.
2. **Choose transport**: stdio for a local process launched by the client; Streamable HTTP for anything shared, remote, or multi-user. Decision rule: if more than one user or machine will connect, you need HTTP plus authentication.
3. **Implement with the high-level server class** (`McpServer.registerTool` in TypeScript; `@mcp.tool()` in Python). Use the low-level request-handler API only when you need custom protocol behavior.
4. **Harden**: path containment, allow-lists, size/time limits, secret handling, authz, rate limits (checklist below).
5. **Test**: unit-test handlers directly; run the server under the Inspector; test one hostile input per tool (traversal, oversized, wrong type, injection string).
6. **Document** the tool contract (description precise enough that the model picks the right tool; state side effects and limits).

## Minimal TypeScript server (SDK v2 line)

```typescript
import { McpServer } from "@modelcontextprotocol/server";
import { StdioServerTransport } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";

const server = new McpServer({ name: "calculator", version: "1.0.0" });

server.registerTool(
  "calculate_sum",
  {
    description: "Add two finite numbers and return the sum. No side effects.",
    inputSchema: z.object({ a: z.number().finite(), b: z.number().finite() }),
    annotations: { readOnlyHint: true },
  },
  async ({ a, b }) => ({ content: [{ type: "text", text: String(a + b) }] }),
);

await server.connect(new StdioServerTransport());
console.error("calculator MCP server running on stdio"); // stderr only
```

On the v1 SDK the same shape is `import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"` with `StdioServerTransport` from `@modelcontextprotocol/sdk/server/stdio.js`. Confirm exact imports against the README of the installed version.

## Minimal Python server (SDK v2 line)

```python
from mcp.server import MCPServer

mcp = MCPServer("Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum. No side effects."""
    return a + b
```

Run it with the SDK CLI (`mcp[cli]` extra): `uv run mcp run server.py` for stdio, or `uv run mcp run server.py --transport streamable-http` for HTTP. On v1, import `FastMCP` from `mcp.server.fastmcp` instead.

## Path containment (the most common real bug)

```typescript
import { realpath } from "node:fs/promises";
import path from "node:path";

export async function resolveInside(baseDir: string, userPath: string): Promise<string> {
  const base = await realpath(baseDir);
  const target = await realpath(path.resolve(base, userPath)); // follows symlinks
  const rel = path.relative(base, target);
  if (rel.startsWith("..") || path.isAbsolute(rel)) {
    throw new Error("path escapes the allowed directory");
  }
  return target;
}
```

`realpath` fails for files that do not exist yet; for create operations resolve the parent directory and re-join the validated file name. A plain `startsWith(base)` string check is wrong (`/data` also prefixes `/data-secret`).

## Remote (Streamable HTTP) hardening checklist

- Validate the `Origin` header on every request and answer 403 when it is present and not allow-listed (DNS-rebinding defense; required by the spec).
- Local development servers bind to `127.0.0.1`, not `0.0.0.0`.
- Authenticate every connection. For HTTP the spec's authorization model treats the MCP server as an OAuth 2.x resource server: publish protected-resource metadata, validate access tokens (signature, expiry, issuer, and that the audience is this server), and never forward a client's token to an upstream API (no token passthrough).
- Do not trust identifiers a client supplies for tenancy; derive the tenant from the validated token.
- Set request body size limits, per-call timeouts, and rate limits.
- Behind nginx or similar, send `X-Accel-Buffering: no` on SSE responses so events are not buffered.
- If you must serve pre-2026 clients, treat `Mcp-Session-Id` as an untrusted correlation id, never as authentication.

## Testing

```bash
# Interactive inspector (stdio server)
npx @modelcontextprotocol/inspector node build/index.js
```

Verify: tool list renders, a valid call succeeds, each invalid call returns `isError` or a protocol error without crashing, and nothing but JSON-RPC appears on stdout. For HTTP servers, start the server separately and connect the Inspector to its URL. Inspector UI details change between releases; follow its README rather than memorized menus.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
| :--- | :--- | :--- |
| `console.log`/`print` in a stdio server | Corrupts JSON-RPC frames; client drops the connection | stderr or file logging |
| New server built on the HTTP+SSE transport | Deprecated since 2025-03-26; clients migrate away | Streamable HTTP |
| `startsWith(baseDir)` containment check | Prefix and symlink bypass | `realpath` + `path.relative` |
| Building a shell command string from arguments | Command injection | `execFile("git", [subcommand, ...])` with allow-listed subcommands |
| Relying on `readOnlyHint` for safety | Hints are advisory | Server-side authz and read-only DB roles |
| Passing the client's bearer token to a downstream API | Confused deputy; breaks audience binding | Separate server credential or proper token exchange |
| Returning raw upstream error bodies | Leaks internals and secrets | Short mapped message; log detail to stderr |
| Copying a 2025-era tutorial that depends on sessions or `initialize` | Wrong for the stateless revision | Check the revision your SDK targets |

## Verification checklist

- [ ] Every tool has a schema and handler-side semantic checks.
- [ ] Nothing but protocol frames on stdout in stdio mode.
- [ ] Failure paths return errors without crashing or leaking secrets.
- [ ] Path, command, and URL arguments are allow-listed or contained.
- [ ] HTTP servers validate Origin, authenticate, and bind to localhost in dev.
- [ ] Spec revision and SDK version recorded in the README of the server.
- [ ] Hostile-input test exists for each tool.

## Sources

- MCP specification (latest), transports and changelog: https://modelcontextprotocol.io/specification/latest
- TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
