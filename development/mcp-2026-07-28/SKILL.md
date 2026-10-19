---
name: mcp-2026-07-28
description: "Build and consume stateless MCP servers and clients on the 2026-07-28 revision: server/discover, per-request metadata via _meta, tasks extension, OAuth 2.1 with PKCE, backward-compat negotiation down to 2025-11-25 and 2025-06-18. Use when an agent must scaffold an MCP server or client, debug a protocol handshake, map error codes to actions, or verify that a deployment is stateless and version-pinned. Not for general API design or non-MCP integrations."
compatibility: MCP spec revisions 2026-07-28 (primary), 2025-11-25, 2025-06-18 (fallback)
license: MIT
---
# MCP 2026-07-28 — stateless servers and clients

## When to invoke
Scaffolding an MCP server or client; debugging a protocol handshake; mapping error
codes to actions; verifying statelessness or version pinning in a deployment; integrating
OAuth for an MCP tool consumer. Do NOT use for generic REST APIs or non-MCP integrations.

## When to invoke (concrete triggers — if none match, do not load this skill)
| Trigger (what the user says or the repo shows) | Load? |
|---|---|
| "scaffold an MCP server/client", "write an MCP tool", "add an MCP integration" | YES |
| "handshake fails", "initialize not found", "Mcp-Session-Id rejected", "400 on POST" | YES |
| "which protocol version", "negotiate a version", "-32022", "UnsupportedProtocolVersion" | YES |
| "long-running tool", "tool times out", "poll a task", "tasks/get", "InputRequiredResult" | YES |
| "set up OAuth for MCP", "PKCE", "Client ID Metadata Document", "DCR" | YES |
| "is my deployment stateless", "replay test", "repeated call returns different result" | YES |
| "build a plain REST API", "design a GraphQL schema", "write a gRPC service" | NO |
| "use an SDK function", "call an existing API" (no MCP involved) | NO |
| "chat with a model" (no tool protocol) | NO |

**Trigger rule**: the description is pushy by design — a prompt that merely *mentions*
MCP loads this skill. The table above is the *precision* half: if a prompt matches a row
in the left column but the task is really about something else, narrow the description,
not the body.

## Procedure (numbered — follow in order)
1. **Pin the revision in config, never in logic.** Primary `2026-07-28`, fallbacks
   `2025-11-25` and `2025-06-18`. Read from env `MCP_PROTOCOL_VERSION` with a pinned
   default; validate against the vendored list in `references/changelog.md`.
2. **Server: implement `server/discover` (MUST).** Advertise supported versions,
   capabilities and identity. Clients MAY call it up front for version selection or as a
   backward-compat probe on STDIO.
3. **Client: send per-request `_meta`.** Every request carries
   `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientInfo` and
   `io.modelcontextprotocol/clientCapabilities`. There is no `initialize` handshake.
4. **Streamable HTTP: no sessions.** No `Mcp-Session-Id`, no protocol-level sessions. Send
   the `MCP-Protocol-Version` header and the standard `Mcp-Method`/`Mcp-Name` headers on
   POST. SSE stream resumability and `Last-Event-ID` are removed.
5. **Tasks extension.** Long-running tools return a result with `resultType` set; use
   `tasks/get` to poll and `tasks/update` for client-to-server input. The extension
   identifier is `io.modelcontextprotocol/tasks` and it is only available to clients that
   declare it in per-request `clientCapabilities.extensions`.
6. **OAuth 2.1.** Authorization Code with PKCE (`S256` only; `code_verifier` 43-128
   chars). Client ID Metadata Documents replace Dynamic Client Registration, which is
   **deprecated but kept for backwards compatibility** with ASes that do not support
   the document flow (2026-07-28 changelog, PR #2858). Key persisted credentials by
   issuer and re-register when the issuer changes. Validate `iss` before redeeming the
   code (RFC 9207, SEP-2468). Full ordered flow in `references/oauth-flow.md`.
7. **Map error codes.** `-32000..-32019` implementation-defined (grandfathered),
   `-32020..-32099` reserved for MCP: `-32020` HeaderMismatch, `-32021` MissingRequiredClient
   Capability, `-32022` UnsupportedProtocolVersion. `server/discover` failures return
   `-32601` (Method not found) with HTTP 404.
8. **Verify statelessness.** Replay a request with the same `_meta` and assert an
   identical result; assert no session state between requests.

## Decision tables
- **Capability negotiation**: client version ∈ server `supportedVersions` -> use the
  highest common version; no overlap -> refuse with `-32022`, never silently downgrade.
- **Result handling**: `resultType: "complete"` -> ordinary result; `"input_required"` ->
  Multi Round-Trip Request, retry with `inputResponses`; `"task"` -> Tasks extension.
- **Deprecations**: Roots, Sampling, Logging are deprecated (pass roots as tool params or
  resource URIs, call provider APIs directly, log to stderr or OpenTelemetry). HTTP+SSE is
  deprecated; use Streamable HTTP.
- **`_meta` completeness**: all four reserved keys must be present on every request —
  `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientInfo`,
  `io.modelcontextprotocol/clientCapabilities`, and optionally
  `io.modelcontextprotocol/logLevel`. Missing any of the first three -> `-32021` (HTTP 403).
- **Tasks availability**: the `io.modelcontextprotocol/tasks` extension is usable only when
  BOTH the server advertised it in `server/discover.capabilities.extensions` AND the client
  declares it in per-request `clientCapabilities.extensions`. Either missing -> the tasks
  methods return `-32601` or `-32021`.
- **`resultType` dispatch**: `complete` -> ordinary result; `input_required` -> Multi
  Round-Trip Request, respond with `tasks/update` + `inputResponses`; `task` -> Tasks
  extension, poll with `tasks/get`. Absent `resultType` -> short tool, block normally.

## Near-miss triggers (stop and re-check before proceeding)
- A server still sending `Mcp-Session-Id` or an `initialize` handshake -> not 2026-07-28.
- Hardcoding a version string in logic -> it goes stale; read from config/env.
- Assuming `tasks/result` exists -> it was removed; use `tasks/get`.
- Using Dynamic Client Registration for a new client -> it is deprecated; use Client ID
  Metadata Documents.
- Reusing credentials across authorization servers -> credentials are bound to the issuer.
- Sending `_meta` only on the first request -> `-32021` on the second. Per-request means
  per-request.
- Calling `tasks/result` or `tasks/list` -> `-32601`. Use `tasks/get` / `tasks/update`.
- Treating `input_required` as an error -> it is a legitimate MRTR; respond, do not abort.
- A server that advertises `tasks` in `server/discover` but the client omits the extension
  from `clientCapabilities` -> the tasks methods are unavailable (`-32021`).

## Pitfalls from research
- P1: Shipping a 2025-06-18 server that breaks on a 2026-07-28 client because the
  initialize handshake was removed.
- P2: Neglecting `server/discover` — it is a MUST, not a MAY.
- P3: Forgetting that per-request `clientCapabilities` must be sent on *every* request;
  servers MUST NOT infer capabilities from prior requests.
- P4: Treating `allowed-tools` as a hard gate — it is experimental metadata.
- P5: Casing of `Mcp-*` headers — treat as case-insensitive per HTTP and pin in config.

## Verification checklist
- [ ] Revision pinned in config, read from env with fallback.
- [ ] `server/discover` implemented and returning supportedVersions, capabilities, serverInfo.
- [ ] Every request carries `_meta` with protocolVersion, clientInfo, clientCapabilities.
- [ ] No `Mcp-Session-Id`, no `initialize` handshake, no SSE resumability.
- [ ] Tasks handled via `tasks/get` + `tasks/update`, never `tasks/result`.
- [ ] OAuth uses Authorization Code + PKCE with Client ID Metadata Documents.
- [ ] Error codes mapped to actions; `-32022` used for version refusal.
- [ ] Statelessness proven by a replay test.
- [ ] `server/discover` result validated by `scripts/protocol_check.py --json` (valid: true).
- [ ] Version agreement recorded by `scripts/version_negotiate.py --json`.
- [ ] `_meta` present on every request with all four reserved keys.
- [ ] Tasks extension declared on both sides before any `tasks/*` call.
- [ ] `resultType` dispatch table applied: complete / input_required / task.
- [ ] `scripts/stateless_probe.py` passes on a replay pair.

## Worked examples
Good and bad client behaviour, with the detection signal for each, live in
`references/examples.md` (discover-first negotiation, `-32022` refusal, tasks
extension, header-casing trap).

## Related skills
- [skill-authoring-evals](../skill-authoring-evals/SKILL.md) — an MCP skill is a skill like any other; audit its description and evals the same way.

## References
- changelog: references/changelog.md
- error codes: references/error-codes.md
- oauth flow: references/oauth-flow.md
- server/discover: references/server-discover.md
- per-request _meta: references/meta-schema.md
- tasks extension: references/tasks-extension.md
- compat matrix: references/compat-matrix.md
- compat versions: references/compat-versions.md
- examples: references/examples.md
- DESIGN: references/DESIGN.md
- EVALS: references/EVALS.md
- SOURCES: references/SOURCES.md
