---
name: mcp
description: "Model Context Protocol expert: spec revisions (2025-11-25 stable, 2026-07-28 draft), client-host-server architecture, stdio and Streamable HTTP transports and message flow, server primitives (tools/resources/prompts), client capabilities (elicitation, deprecated sampling/roots), OAuth 2.1 authorization (RFC 9728 discovery, RFC 8707 audience binding), protocol-level security mitigations, building servers with the official SDKs, and consuming MCP from Claude Code, the Claude API MCP connector, and OpenAI's Responses API. WHEN: \"MCP\", \"Model Context Protocol\", \"MCP server\", \"MCP client\", \"Streamable HTTP\", \"stdio transport\", \"tools/list\", \"tools/call\", \"resources/read\", \"prompts/get\", \"elicitation\", \"sampling\", \"roots\", \"Mcp-Session-Id\", \"MCP-Protocol-Version\", \".mcp.json\", \"claude mcp add\", \"mcp_toolset\", \"MCP connector\", \"MCP Inspector\", \"protected resource metadata\", \"tool poisoning\". Do NOT use for: Claude Code harness configuration (settings.json, permissions, hooks, subagents, plugins) — `claude-code`; the Messages API beyond the MCP connector (model IDs, pricing, caching, non-MCP tool use) — `claude-api`; building an agent loop around MCP tools — `claude-agent-sdk`, `openai-agents-sdk`, or `google-adk`; wiring MCP servers into another harness — `codex`, `github-copilot`, `cursor`, `pi`; the broad LLM/agent threat catalog (OWASP GenAI Top 10, prompt-injection taxonomy, governance) — `ai-security`; container/VM isolation mechanics — `sandboxing` (containers plugin for Kubernetes depth); authoring SKILL.md files — `agent-skills`."
license: MIT
---

# Model Context Protocol (MCP)

MCP is an open, JSON-RPC 2.0 protocol that standardizes how LLM applications connect to external data and tools — LSP for AI context instead of programming languages. This skill covers the protocol itself: the spec, transports, primitives, authorization, and the mechanics of building and consuming servers.

## Target the right spec revision first

Always establish which revision the user is on before answering wire-level questions. Behavior differs materially.

| Revision | Status (2026-08-05) | Use it when |
|---|---|---|
| `2025-11-25` | **Stable** | Default for anything shipping to production |
| `2026-07-28` | Release candidate / draft | Only when the user explicitly targets it or is reading draft docs |

Default every answer to `2025-11-25` unless told otherwise. The draft removes and renames enough (mandatory `server/discover`, per-request `_meta`, deprecation of sampling/roots/logging, `subscriptions/listen`) that mixing revisions produces code that will not connect. Read `references/versions/2025-11-25.md` and `references/versions/2026-07-28.md` before writing revision-sensitive wire format.

## Routing

| Request | Load |
|---|---|
| Transport choice, session IDs, SSE resumption, HTTP status semantics | `references/transports.md` |
| Tool/resource/prompt design, JSON-RPC method shapes, elicitation/sampling/roots | `references/primitives.md` |
| OAuth discovery, CIMD/DCR, PKCE, `resource` param, step-up scopes | `references/authorization.md` |
| Confused deputy, token passthrough, SSRF, session hijacking, local-server compromise | `references/security.md` |
| Writing a server in Python/TypeScript/Java/Kotlin/C#/Ruby, Inspector | `references/building-servers.md` |
| Wiring servers into Claude Code, the Claude API, or OpenAI | `references/consuming-mcp.md` |
| Wiring servers into any other harness or vendor SDK | that tool's skill — see "Consuming MCP" |
| "What changed in revision X" | `references/versions/<revision>.md` |

## Architecture

Three roles. Never conflate them.

- **Host** — the AI application (Claude Code, Claude Desktop, VS Code) that coordinates clients.
- **Client** — a protocol connector inside the host; exactly **one client per server connection**, 1:1.
- **Server** — the program supplying context and capabilities. "Server" says nothing about where it runs: local stdio servers typically serve a single client, remote Streamable HTTP servers serve many concurrently.

Two layers: a **data layer** (JSON-RPC 2.0 — version/capability negotiation, primitives, notifications) and a **transport layer** (stdio, Streamable HTTP, or a custom transport). The message format is identical across transports; only carriage changes. Design against the data layer and let the SDK own the transport.

Connections are **stateful with explicit capability negotiation** — each side may only use features the other declared. Never call a method whose capability the peer did not advertise; that is a protocol error, not a graceful degradation.

### Where MCP stops

MCP standardizes context exchange only. It does not dictate how an application uses the LLM, selects context, or orchestrates agents — and it **cannot enforce its own security principles at the protocol level**. The spec's four principles (user consent and control, data privacy, tool safety, sampling controls) are obligations on implementors, so every answer about "is MCP safe" must resolve to what the host and server actually enforce, never to the protocol.

## Transports

**Choose stdio for local, Streamable HTTP for remote.** Clients SHOULD support stdio whenever possible; a server meant to run on the user's machine SHOULD use stdio precisely because it limits reach to the launching client.

**stdio — the rules that break servers when violated:**
- Client launches the server as a subprocess; server reads JSON-RPC on `stdin`, writes on `stdout`.
- Messages are newline-delimited and **MUST NOT** contain embedded newlines. UTF-8 always.
- The server **MUST NOT** write anything to stdout that is not a valid MCP message. This is the single most common stdio server bug — one stray `print()` corrupts the stream.
- `stderr` is free for logging. Clients **SHOULD NOT** treat stderr output as an error signal.

**Streamable HTTP — one endpoint, POST and GET:**
- A single MCP endpoint (e.g. `https://example.com/mcp`) accepting POST and GET. Replaces the deprecated 2024-11-05 HTTP+SSE transport.
- Client POSTs every message; `Accept: application/json, text/event-stream` is mandatory — the server may answer a request with either a single JSON object or an SSE stream, and the client **MUST** handle both.
- Responses and notifications POSTed by the client get `202 Accepted` with no body.
- Server **MUST NOT** broadcast one JSON-RPC message across multiple streams — each message goes on exactly one stream.
- **Disconnection is not cancellation.** To cancel, send an explicit `CancelledNotification`.

**Non-negotiable HTTP hardening** (normative in the spec, not advice):
- Validate the `Origin` header on every connection; respond `403 Forbidden` when present and invalid — this is the DNS-rebinding defense.
- Bind local servers to `127.0.0.1`, never `0.0.0.0`.
- Implement authentication for all connections.

**Session and version headers:** if the server issues `Mcp-Session-Id` on the `InitializeResult`, the client **MUST** echo it on every subsequent request; a `404` means the session is gone and the client **MUST** re-initialize without an ID. The client **MUST** send `MCP-Protocol-Version: <negotiated>` on all post-initialization HTTP requests; a server seeing no such header **SHOULD** assume `2025-03-26`. Read `references/transports.md` for resumability, `Last-Event-ID` replay rules, and the backwards-compatibility probe for pre-2025 servers.

## Server primitives

Pick the primitive by **who controls invocation** — this is the design decision, not an implementation detail.

| Primitive | Controlled by | Use for | Methods |
|---|---|---|---|
| **Tools** | Model | Actions with effects: writes, API calls, computation | `tools/list`, `tools/call` |
| **Resources** | Application | Passive read-only context: files, schemas, docs | `resources/list`, `resources/templates/list`, `resources/read` |
| **Prompts** | User | Explicitly-invoked workflow templates (slash commands) | `prompts/list`, `prompts/get` |

Rules that keep servers usable:
- **One clearly-defined operation per tool.** Tools carry a JSON Schema `inputSchema`; the schema and description are the entire contract the model sees.
- Give every tool a `description` that states what it does and when to use it — the model has nothing else to route on.
- `tools/call` `name` **MUST** exactly match a discovered tool name; `arguments` **MUST** conform to `inputSchema`. Results come back as a `content` array, so return multiple blocks (text, image, resource) rather than stuffing everything into one string.
- Use **resource templates** (`weather://forecast/{city}/{date}`) instead of enumerating thousands of direct resources; templates self-document via `title`/`description`/`mimeType` and support parameter completion.
- `tools/list` supports a `cursor` for pagination — paginate rather than returning an unbounded catalog.
- Declare `"tools": {"listChanged": true}` only if you actually emit the notification. Delivery is **best-effort**: clients should still re-poll after reconnects rather than trusting they saw every change.

Expect the host to gate tool execution behind user approval, per-tool enable/disable, and activity logs. Design tools so a human reviewing the call in a dialog can tell what it will do.

### Server design review

Reject or fix a server design that does any of these:

- Exposes one mega-tool with a `mode` or `action` string parameter — the model routes on tool names and descriptions, so collapse the surface and it stops choosing correctly.
- Returns a wall of text when the caller needed a resource link or a structured content block.
- Ships tools whose descriptions describe implementation rather than purpose and preconditions.
- Uses tools where the data is passive and read-only — that is a resource, and making it a tool forces the model to spend a turn fetching what the application could have attached.
- Declares capabilities it does not implement, or emits notifications it never declared.

## Client capabilities

Servers can call back into the client — but only where the client advertised support.

| Capability | Status (2026-08-05) | Guidance |
|---|---|---|
| **Elicitation** | Current | Use it to ask the user for missing input mid-operation instead of failing |
| **Roots** | **Deprecated** in `2026-07-28` | Pass directories via tool params, resource URIs, or server config in new work |
| **Sampling** | **Deprecated** in `2026-07-28` | Integrate directly with an LLM provider API in new work |

**Elicitation has two modes and one hard privacy rule.** Form mode sends a JSON Schema the client renders and validates. URL mode hands the user a URL to complete out-of-band so the data never transits the client. **Never request passwords, API keys, access tokens, or payment credentials in form mode** — those belong in URL mode so secrets never enter client or model context. Clients must show which server is asking and why, must show the full URL, and must never auto-fetch a URL-mode target.

**Roots are advisory, not a security boundary.** The spec says servers SHOULD respect them; a server runs code the client does not control. Enforce real boundaries with OS permissions and sandboxing. Roots prevent accidents, not attacks — say so explicitly when a user proposes them as containment.

Sampling, where still used, carries two human-in-the-loop checkpoints: approval of the outbound request and approval of the returned generation. Read `references/primitives.md` for the full elicitation schema example and the draft's `InputRequiredResult` multi-round-trip pattern.

## Authorization

Authorization is OPTIONAL overall, but the rules are strict where it applies. **HTTP transports SHOULD follow the OAuth 2.1 profile; stdio transports SHOULD NOT** — stdio servers take credentials from the environment instead.

The MCP server is an OAuth **resource server**; the MCP client is the OAuth **client**. Requirements a review must confirm:
- Server **MUST** implement RFC 9728 Protected Resource Metadata; client **MUST** use it to discover the authorization server. Prefer the `resource_metadata` value from a `401` `WWW-Authenticate` header over well-known probing.
- Client **MUST** implement PKCE (S256) and **MUST** refuse to proceed if the AS does not advertise `code_challenge_methods_supported`.
- Client **MUST** send RFC 8707 `resource` on both the authorization and token requests, set to the server's canonical URI (scheme required, no fragment) — **even if the AS does not advertise support**. This is what binds the token's audience.
- Tokens go in `Authorization: Bearer` on **every** request, never in a query string. Servers **MUST** validate audience and reject anything else with `401`.
- Prefer registration in this order: pre-registered credentials → Client ID Metadata Documents (`client_id` is an HTTPS URL to a JSON doc) → Dynamic Client Registration → manual entry.

**Scope strategy:** use the `scope` from the `401` challenge when present; otherwise request `scopes_supported`. Servers should start clients on a minimal scope set and escalate through targeted `403` + `WWW-Authenticate: Bearer error="insufficient_scope"` step-up challenges rather than granting a catalog up front. Read `references/authorization.md` for the discovery probe order, CIMD document shape, and the full flow sequence.

## Protocol-level security

Cover these mitigations here; send broad LLM/agent threat modeling (prompt-injection taxonomy, OWASP GenAI Top 10, governance) to the `ai-security` skill, and container/VM isolation design to `sandboxing`.

- **Never pass client tokens through to upstream APIs.** A server that forwards a token it was given, unvalidated, breaks audience separation, downstream rate limiting, and audit attribution. The server obtains its own token for upstream calls. This is explicitly forbidden by the spec.
- **Proxy servers must keep a per-user registry of approved `client_id`s** checked before starting a third-party flow, or the confused-deputy attack lets an attacker harvest an authorization code through a stale consent cookie. Exact-match redirect URIs; single-use, short-expiry `state` stored only after consent.
- **Treat every URL received from a server as SSRF input.** Enforce HTTPS (loopback only in dev), block private and link-local ranges including `169.254.169.254`, validate each redirect hop, and use an egress proxy in server-side deployments. Do not hand-roll IP validation — encoding tricks defeat custom parsers.
- **Sessions are not authentication.** Use CSPRNG session IDs, verify authorization on every inbound request, and bind session IDs to user identity (`<user_id>:<session_id>`) so a guessed ID cannot impersonate.
- **Validate authorization URL schemes with an allowlist** (`http`/`https` only) and **never shell out to open a URL** — `javascript:` payloads and shell metacharacters turn a malicious server into client-side RCE.
- **Tool annotations and descriptions are untrusted input** unless the server is trusted. Never let a tool description alter agent policy.
- Local server config is arbitrary code execution: clients offering one-click install **MUST** show the exact untruncated command and require explicit approval.

Read `references/security.md` for the eight attack classes with full flows and required mitigations.

## Building servers

- **Log to stderr, never stdout, in stdio servers** — `print()`, `console.log()`, `System.out.println()`, `println()`, `Console.WriteLine()`, and `puts` all corrupt the stream. HTTP servers may log to stdout freely.
- In C#, use `Host.CreateEmptyApplicationBuilder`, not `CreateDefaultBuilder`, or the host's own banner output breaks stdio.
- Let the SDK derive schemas: Python type hints + docstrings via `@mcp.tool()`, TypeScript Zod objects via `registerTool`. Hand-written JSON Schema drifts from the implementation.
- **Build TypeScript servers before connecting a client** — an unbuilt project will not connect.
- Use absolute paths in host config (`claude_desktop_config.json`, `.mcp.json`); relative paths and bare interpreter names are the usual "failed to connect" cause.
- Develop against **MCP Inspector** (`npx @modelcontextprotocol/inspector`) before wiring a host — it also produces OAuth access tokens for testing remote authenticated servers.

Read `references/building-servers.md` for Python and TypeScript quickstart code, per-language SDK notes, and host config examples.

## Consuming MCP

**Claude Code** — `claude mcp add` defaults to stdio; `--transport http` for remote; everything after `--` is the launch command.

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
claude mcp add playwright -- npx -y @playwright/mcp@latest
claude mcp add --scope project --transport http docs https://code.claude.com/docs/mcp
```

Scope is fixed at add time — remove and re-add to change it. `local` (default) is you-only and **tied to the exact project directory**, `project` writes committable `.mcp.json`, `user` applies across your projects. Claude Code reads only `~/.claude.json` and `<project>/.mcp.json` (or under `$CLAUDE_CONFIG_DIR`) — no other path is consulted, which is the answer to most "my config is ignored" reports. Authenticate OAuth servers with `/mcp` inside a session.

**Claude API MCP connector** — remote servers only, tool calls only. Send `anthropic-beta: mcp-client-2025-11-20`, declare servers in `mcp_servers`, and reference each by exactly one `mcp_toolset` in `tools`. Local stdio servers, MCP prompts, and MCP resources require the client-side SDK helpers instead. Not covered by Zero Data Retention.

**OpenAI Responses API** — `type: "mcp"` tools over Streamable HTTP or HTTP/SSE, with `require_approval` policies and first-party `connector_id` connectors. The `authorization` token is **not persisted** and must be resent on every request.

**Every other host** — this skill covers the protocol plus the three clients above and nothing further. Send per-harness server wiring to the harness's own skill (`codex`, `github-copilot`, `cursor`, `pi`) and MCP-consuming agent loops to the owning SDK skill (`claude-agent-sdk`, `openai-agents-sdk`, `google-adk`). Take the protocol rules from this skill with you — transport choice, capability negotiation, the protocol-level security mitigations — and get the config surface there.

Read `references/consuming-mcp.md` for full field tables, allowlist/denylist toolset patterns, response content-block shapes, the deprecated-beta migration, and the OpenAI approval flow.

## Diagnosing a broken connection

Work in this order — it isolates the layer before the protocol.

1. **Reachability (HTTP):** `curl -I <url>`. A `404`/`405` means the server is up and only answers POST — that is healthy, not a failure. `401`/`403` means auth is required. No response is a network or URL problem.
2. **Auth:** a `401` with `WWW-Authenticate` names the resource metadata URL and required scopes; follow it before assuming the server is broken.
3. **Launch (stdio):** run the configured command directly in a terminal. Most failures are a wrong path, a missing build, or stdout pollution.
4. **Zero tools but "connected":** almost always a missing required environment variable — add it with `claude mcp add --env KEY=value`.
5. **Timeout:** raise the 30s startup budget with `MCP_TIMEOUT` in milliseconds (`MCP_TIMEOUT=60000 claude`).
6. **Wire-level:** reproduce in MCP Inspector, which shows raw JSON-RPC and isolates server bugs from host bugs.

Run `scripts/probe-mcp-http-endpoint.sh <url>` for steps 1–2 in one pass.

## Reference files

- `references/transports.md` — stdio and Streamable HTTP in full: message flow, SSE rules, multiple connections, resumability, session lifecycle, protocol-version header, backwards compatibility with HTTP+SSE.
- `references/primitives.md` — tools/resources/prompts with JSON-RPC examples and schemas; elicitation, roots, sampling including the draft MRTR pattern; multi-server composition.
- `references/authorization.md` — OAuth 2.1 profile: discovery order, CIMD vs DCR, scope selection, `resource` canonical URIs, token usage, status codes, step-up authorization.
- `references/security.md` — the eight attack classes from the spec's security best practices, each with the vulnerable conditions and required mitigations.
- `references/building-servers.md` — Python and TypeScript quickstarts, the stdout prohibition per language, other-language SDK notes, host config, MCP Inspector.
- `references/consuming-mcp.md` — Claude Code CLI and scopes, Claude API MCP connector fields and patterns, client-side SDK helpers, OpenAI Responses API MCP tools and connectors.
- `references/versions/2025-11-25.md` — the stable baseline: what is normative in this revision.
- `references/versions/2026-07-28.md` — draft deltas: `server/discover`, per-request `_meta`, `subscriptions/listen`, deprecations, extensions.

## Scripts

- `scripts/probe-mcp-http-endpoint.sh` — read-only reachability and OAuth-discovery probe for a remote MCP endpoint (HEAD/POST reachability, `WWW-Authenticate` parsing, protected-resource and authorization-server metadata fetch). Makes no state-changing calls.

## Sources

- https://modelcontextprotocol.io/specification/2025-11-25
- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
- https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices
- https://modelcontextprotocol.io/docs/learn/architecture
- https://modelcontextprotocol.io/docs/learn/server-concepts
- https://modelcontextprotocol.io/docs/learn/client-concepts
- https://modelcontextprotocol.io/quickstart/server
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/mcp-quickstart
- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
- https://developers.openai.com/api/docs/guides/tools-connectors-mcp

Fetched: 2026-08-05
