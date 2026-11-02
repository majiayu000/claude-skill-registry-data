---
name: build-mcp-server
description: Use when exposing a service or dataset to AI clients through the Model Context Protocol — few task-shaped tools with typed inputs, read-only by default, server-enforced confirmation for writes, stdio or Streamable HTTP, OAuth for remote, size limits, tests with the Inspector.
---

# Build an MCP Server

An MCP server is an API whose caller is a model: it reads your tool descriptions on every turn and recovers from errors by reading your messages. Design it for that reader. Spec revision **2026-07-28** (stateless, no sessions) and the **v2** TypeScript SDK (`@modelcontextprotocol/server`) are the targets; the older single-package `@modelcontextprotocol/sdk` 1.x is the previous line.

## 1. Audit current state

Read `.claude/stack-profile.md` (`languages`, `backend.track`, `ai`). If absent, detect per [stack-profile.md](../../core/_shared/stack-profile.md). Change nothing yet:

```bash
grep -n "modelcontextprotocol" package.json pyproject.toml 2>/dev/null           # which SDK and line
grep -rn "Mcp-Session-Id\|StreamableHTTPServerTransport\|SSEServerTransport\|initialize" src | head   # 2025-era code
ls .mcp.json mcp.json src/server.ts src/server.py 2>/dev/null
grep -rn "registerTool\|server.tool(\|@mcp.tool" src | wc -l                      # tool count
npm view @modelcontextprotocol/server version 2>/dev/null                          # current v2 line
```

Report: SDK line (v1 or v2), transport, tool count and names, whether any tool writes, how callers are authenticated, whether tool outputs are bounded.

## 2. Decide what to do

- No server → full install (steps 4–6).
- v1 server (`@modelcontextprotocol/sdk`, sessions, SSE) → migrate to v2 with the SDK's upgrade guide (`ts.sdk.modelcontextprotocol.io/v2/migration/upgrade-to-v2`); v1 still gets fixes for at least six months after 2026-07-27, so plan it, do not panic.
- Server exists → check each tool against [mcp-patterns.md](./mcp-patterns.md) and apply the delta.
- A thin wrapper over one HTTP endpoint with one user → ask whether a plain CLI, a script or a skill is simpler. MCP earns its cost with several clients, several tools, or shared auth.
- Everything present and `Verify` passes → "already in place".

## 3. Detect the track

| Signal | Branch |
|---|---|
| Local, one user, launched by the host as a child process | **stdio**. No OAuth: credentials come from the environment the host passes |
| Remote or multi-user | **Streamable HTTP** behind OAuth 2.1 (the server is a resource server). Stateless: no session |
| TypeScript | `@modelcontextprotocol/server` + `@modelcontextprotocol/hono` (Hono) or `@modelcontextprotocol/node` / `express` |
| Python | `mcp` 2.x: `from mcp.server import MCPServer` |
| Go, Rust | Use the official SDK for that language; apply [mcp-patterns.md](./mcp-patterns.md) unchanged. No canonical code here |

## 4. Install only what's missing

```bash
pnpm add @modelcontextprotocol/server @modelcontextprotocol/hono hono @hono/node-server zod    # remote, TypeScript
pnpm add -D @modelcontextprotocol/client vitest tsx typescript @types/node                      # tests
uv add mcp                                                                                      # Python
```

TypeScript 6 or later needs `"types": ["node"]` in `tsconfig.json`. Zod must be 4.2 or later (peer of the server package).

## 5. Generate the seams

Code: [mcp-code.md](./mcp-code.md).

```
src/server.ts     # createServer(auth): tools, resources; no transport code
src/http.ts       # Streamable HTTP: Hono app, bearer auth, protected-resource metadata
src/stdio.ts      # stdio entry for local use
tests/server.test.ts
```

Design the tools **before** writing code: list the 3 to 7 things a user asks, make one tool per intent, and write each description as "what it does, when to use it, what it returns, limits". Rules and examples: [mcp-patterns.md](./mcp-patterns.md). Identity (tenant, user) comes from `auth` (the verified token) passed to `createServer`, never from a tool argument.

## 6. Wire it up

1. Local: `claude mcp add my-server -- npx tsx src/stdio.ts` (Claude Code). Remote: `claude mcp add --transport http my-server https://host/mcp`; the client discovers the authorization server from the `401` challenge.
2. Remote only: point the protected-resource metadata at your authorization server (`AUTH_ISSUER`) and set `PUBLIC_URL` to the exact public URL of the endpoint; tokens must be issued for that audience. Use an existing authorization server (Auth0, Keycloak, Entra ID, a cloud IdP); do not write one.
3. Behind a reverse proxy, set the allowed hosts and origins explicitly; disable response buffering for the MCP route.
4. Log to stderr (stdio) or your logger (HTTP), never to stdout on stdio: stdout is the protocol channel.

## 7. Verify

```bash
pnpm typecheck && pnpm vitest run tests/server.test.ts           # in-memory client: tools, structured output, scoping, confirmation
npx @modelcontextprotocol/inspector --cli npx tsx src/stdio.ts --method tools/list
npx @modelcontextprotocol/inspector --cli npx tsx src/stdio.ts --method tools/call --tool-name search_tickets --tool-arg status=open
curl -si -X POST http://127.0.0.1:3000/mcp -H 'Content-Type: application/json' -d '{}' | grep -i www-authenticate
```

Expected: tests green (6 in the example); `tools/list` returns your tools in a stable order with annotations; the `tools/call` result carries `structuredContent`; the unauthenticated `curl` returns `401` with `www-authenticate: Bearer … resource_metadata="…/.well-known/oauth-protected-resource/mcp"`. For a visual check run the Inspector without `--cli` and click through each tool, including a bad input and a request with the wrong token.

## References
- [mcp-patterns.md](./mcp-patterns.md): rules and why. [mcp-code.md](./mcp-code.md): TypeScript and Python code.
- [llm-security.md](../_shared/llm-security.md): tool outputs are untrusted text for the client; least privilege by token.
- [stack-versions.md](../_shared/stack-versions.md): spec revision, SDK lines, Inspector.
- [security-baseline.md](../../core/_shared/security-baseline.md), [config.md](../../backend/_shared/config.md).
