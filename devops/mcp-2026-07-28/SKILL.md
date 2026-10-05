---
name: mcp-2026-07-28
description: This skill should be used when the user mentions "MCP 2026-07-28", "MCP spec", "Model Context Protocol spec", "stateless MCP", "Streamable HTTP", "HTTP+SSE", "MCP transport", "MCP lifecycle", "MCP capabilities", "MCP Apps", "MCP Tasks", "versioned extensions", "protocolVersion", or building/upgrading an MCP server to the current spec. It provides the 2026-07-28 stateless core, transport, lifecycle, and versioned-extensions model.
---

# MCP 2026-07-28 Spec

## Purpose
The MCP **2026-07-28** specification is the largest revision since the protocol launched. It moves MCP from a bidirectional, stateful protocol toward a **stateless request/response core**, so servers deploy on serverless and edge infrastructure and scale horizontally; it formalizes **versioned extensions** (MCP Apps for interactive UI, Tasks for long-running work) so capabilities can be added without touching the core; and it aligns authorization with production **OAuth 2.1 / OIDC** (covered in the `mcp-authorization` skill). This skill is the reference for the core, transport, and lifecycle so a server is shaped correctly, not merely functional.

## What changed, at a glance
| Area | Before | 2026-07-28 |
|---|---|---|
| Transport | HTTP+SSE dual endpoint (`GET /sse` + `POST /messages`) | **Streamable HTTP**, single endpoint; HTTP+SSE removed |
| Core model | Stateful, long-lived bidirectional session | **Stateless request/response** core; each request self-contained |
| Deployment | Sticky, single-instance | Serverless / edge / multi-replica behind a load balancer |
| Extensions | Ad-hoc | **Versioned extensions** framework (MCP Apps, Tasks) |
| Auth | Custom / bearer, loosely specified | OAuth 2.1 + OIDC aligned (see `mcp-authorization`) |

## The stateless core
The single most important shape change: **do not require per-connection server memory to serve a request.** A request carries what it needs; any replica can answer it. Concretely:
- No in-process session map that a second instance would not share. If you must correlate requests, key off an external store (Redis, a DB) by a stable id, not a module-level `Map`.
- Long-running work is not a sticky session held open, it is the **Tasks** extension: start returns a task id, the client polls/subscribes, any replica can report status. See `references/versioned-extensions.md`.
- stdio servers are inherently single-process and per-user; the stateless rule is about **remote (HTTP)** servers that scale out.

## Transport: Streamable HTTP
One HTTP endpoint (commonly `/mcp`) handles `POST` for client→server messages and streams responses; the removed HTTP+SSE dual-endpoint design (`GET /sse` establishing a channel + `POST /messages` for calls) should be migrated. See `references/transport-and-lifecycle.md` for the before/after wiring per SDK (TypeScript `StreamableHTTPServerTransport`, Python `streamable_http_app` / `FastMCP`) and how to run it statelessly.

## Lifecycle
1. **initialize** — client sends `protocolVersion`, `capabilities`, `clientInfo`; server replies with the version it supports, its `capabilities`, and `serverInfo`. Report `2026-07-28` only if you actually implement it.
2. **capability negotiation** — declare only what you implement (`tools`, `resources`, `prompts`, `logging`, `completions`, and any extensions). A declared-but-unimplemented capability is a compliance bug.
3. **operation** — tool calls, resource reads, prompt gets; each request self-contained under the stateless core.
4. **shutdown** — transport-level; do not rely on a graceful close to flush server-side session state (there should be none to flush).

## Versioned extensions
Capabilities that are not part of the core, **MCP Apps** (interactive/embedded UI surfaced to the user) and **Tasks** (long-running, resumable work), ship as versioned extensions negotiated at initialize. This lets the ecosystem add and revise these features without breaking core interop. If your server surfaces UI or runs long jobs, model them as extensions, not as overloaded core methods. See `references/versioned-extensions.md`.

## Golden rules
- **Stateless first.** If a design needs a sticky session to work, redesign it (external store, or Tasks) before reaching for session affinity.
- **One transport.** Streamable HTTP for remote, stdio for local; never the removed HTTP+SSE for anything new.
- **Report the version you implement.** `protocolVersion: "2026-07-28"` is a claim your handshake and capabilities must back up.
- **Declared == implemented.** Every capability you advertise must have a working handler.
- **Extensions for extras.** UI → MCP Apps; long jobs → Tasks; both versioned and negotiated, not bolted onto core.

## Additional Resources
### Reference Files
- **`references/transport-and-lifecycle.md`**: Streamable HTTP wiring and the HTTP+SSE→Streamable migration per SDK, stateless request handling, the initialize handshake and capability negotiation, and the removed-transport checklist.
- **`references/versioned-extensions.md`**: the extensions framework, MCP Apps (interactive UI) and Tasks (long-running work) shapes, when to use each, and how to keep long-running work stateless.
