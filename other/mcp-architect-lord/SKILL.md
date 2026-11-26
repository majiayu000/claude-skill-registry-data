---
name: mcp-architect-lord
description: Lord skill for designing and securing MCP servers per the 2026-07-28 spec — stateless core, OAuth 2.1 Resource Server, tool-poisoning defense, and dual-era migration.
triggers:
  - mcp architect lord
  - mcp server
  - mcp design
  - mcp protocol
  - mcp security
  - tool naming
  - oauth resource server
  - mcp architect
  - خادم mcp
personas:
  - ARCH
  - API
  - SEC
  - DEVX
  - DEV
  - UX
tech_stack: []
lord: true

---

# MCP Architect Lord

[OBJ] Design, secure, and migrate MCP servers compliant with the 2026-07-28 protocol specification.

## Problem

MCP servers are the bridge between LLM agents and real-world tools, data, and APIs. A poorly designed server leaks secrets, accepts poisoned tool definitions, breaks under transport changes, or fails OAuth handshake — turning the integration surface into an attack surface. The 2026-07-28 spec introduces breaking changes (CIMD, Resource Server, FastMCP v4) that require deliberate migration, not patch-on-patch.

## Rules

1. [REQ] **Stateless core.** The server core (tool dispatch, resource reads, prompt rendering) MUST be stateless. Session state lives in external stores (Redis, DB) keyed by session ID, never in process memory. Enables horizontal scaling and crash recovery.
2. [REQ] **Tool naming conventions.** Tool names MUST be `snake_case`, `verb_noun` format, ≤32 characters. Examples: `get_issue`, `create_ticket`, `search_docs`. No camelCase, no kebab-case, no abbreviations beyond well-known ones (id, url, api).
3. [REQ] **OAuth 2.1 Resource Server.** The MCP server acts as a Resource Server per RFC 9728. Protected Resource Metadata is served at `/.well-known/oauth-protected-resource`. Authorization Server metadata discovered via `issuer` field. No hardcoded auth server URLs.
4. [REQ] **CIMD not DCR.** Use Client-Initiated Metadata Discovery (CIMD) per RFC 9728. Do NOT use Dynamic Client Registration (DCR) — deprecated in 2026-07-28. Clients discover metadata from the protected resource, not by registering.
5. [REQ] **PKCE on all flows.** Proof Key for Code Exchange (RFC 7636) MUST be enforced on every authorization code flow, including confidential clients. No `response_type=code` without `code_challenge`.
6. [REQ] **DPoP for sender-constrained tokens.** Demonstrating Proof-of-Possession (RFC 9449) binds access tokens to the client's key. Prefer DPoP over bearer tokens for high-security tools. Resource Server MUST validate DPoP proof on each request.
7. [REQ] **Dual-era support.** Servers MUST support both legacy (2025-11-25) and current (2026-07-28) protocol versions simultaneously. Detect era from `protocolVersion` in `_meta`. Modern path = stateless. Legacy path = backward-compat shim. Deprecation timeline: 12 months from spec release.
8. [REQ] **Tool poisoning defense.** Hash-pin tool definitions at registration time. On each load, verify the hash matches. A mismatch (definition tampering) = BLOCK + alert. Never execute a tool whose definition hash differs from the pinned version.
9. [REQ] **Per-tool scopes.** Each tool declares required OAuth scopes in its definition (`annotations.scopes`). The Resource Server validates the access token has ALL required scopes before dispatch. No blanket scope access.
10. [REQ] **MRTR pattern.** Model-Reads-Tool-Returns: tools return structured data (JSON), not prose. The model interprets results; the tool does not narrate. Enables caching, validation, and replay.
11. [REQ] **Extensions framework.** The server MUST support the extensions framework: `tasks` (long-running async), `apps` (UI surfaces), `skills` (declarative capabilities), `EMA` (Enterprise Management API). Extensions are opt-in via capability negotiation.
12. [REQ] **Cacheable listings.** `tools/list`, `resources/list`, `prompts/list` responses MUST include `ETag` and `Last-Modified` headers. Clients use conditional requests (`If-None-Match`). Reduces bandwidth and latency on large catalogs.
13. [REQ] **Header-based routing.** Use `Mcp-Method` and `Mcp-Name` headers for routing and rate-limiting, not URL paths or query params. Enables clean reverse-proxy and load-balancer configurations without parsing JSON bodies. `Mcp-Session-Id` is REMOVED in 2026-07-28 — do not use it.
14. [REQ] **One server = one domain = one auth boundary.** A single MCP server serves one logical domain (e.g., "GitHub issues" or "Linear tickets"). Do not mix domains in one server — it breaks scope granularity and audit clarity.
15. [REQ] **CVE tracking.** Monitor CVEs for the MCP SDK, transport libraries, and OAuth libraries in use. Subscribe to security advisories. Patch within 72h for critical, 7d for high.
16. [REQ] **Inspector testing.** Every server MUST pass the MCP Inspector test suite before deployment. Run `mcp-inspector` locally during development; run it in CI before merge. No server ships without a green Inspector run.
17. [REQ] **Client config generation.** The server MUST auto-generate client configuration snippets (Claude Desktop, VS Code, Cursor) from its own metadata. No hand-written JSON configs that drift from the server's actual capabilities.
18. [REQ] **Registry registration.** Publish server to an MCP registry (local or remote) with: name, version, description, transport, auth metadata, tool count, health endpoint. Enables discovery and governance.
19. [REQ] **Transport selection.** Use stdio for local single-user tools (CLI integrations, local file access) — stdio does NOT follow OAuth auth spec. Use Streamable HTTP (single POST endpoint, per-request SSE stream) for remote multi-user services. HTTP+SSE transport is DEPRECATED — do not use for new servers. Document the rationale. Never expose stdio servers over network without a wrapper.
20. [PROHIBIT] Shipping an MCP server without OAuth Resource Server metadata, tool hash pinning, and Inspector validation — these three are non-negotiable for production.

## References

- MCP 2026-07-28 specification (protocol version, CIMD, extensions framework)
- RFC 9728: OAuth 2.0 Protected Resource Metadata
- RFC 8707: Resource Indicators for OAuth 2.0
- RFC 7636: PKCE
- RFC 9449: DPoP
- FastMCP v4 / Python SDK v2 migration guide
- MCP Inspector: https://github.com/modelcontextprotocol/inspector
