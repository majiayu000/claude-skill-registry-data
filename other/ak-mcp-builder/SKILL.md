---
name: ak-mcp-builder
description: "Build, upgrade, test and publish MCP servers (spec 2026-07-28, TypeScript SDK v2, Python mcp v2 MCPServer), OAuth, evals, MCP Registry."
when_to_use: "Invoke for MCP server or tool design; not for configuring clients or calling existing servers."
category: engineering
keywords: [MCP, server, tools, integration, TypeScript SDK, Python SDK, OAuth, MCP Registry]
license: Proprietary; includes Apache-2.0 material from anthropics/skills, see LICENSE.txt and NOTICE.txt
argument-hint: "[service or API to integrate]"
metadata:
  author: agentkit
  version: "2.0.0"
---

# MCP server development

Target the current protocol, **2026-07-28** (stateless core, `server/discover`, multi
round-trip requests, extensions), unless the project pins an older client base. Read
`references/protocol-2026-07-28.md` when the project uses v1 SDKs, deprecated features
(sampling, roots, logging, SSE), or when behavior differs from older examples.

## Start from the task

Define the user task and the first tool contract (inputs, output shape, side effects,
auth) before choosing infrastructure. Inspect the project's language, SDK version, and
transport first; upgrade a v1 SDK only when the user asked or a required feature needs it.
Read only the upstream API sections that tool needs.

| Need | Read |
|---|---|
| Tool names, descriptions, schemas, errors, annotations, confirmation flows | `references/tool-design.md` |
| TypeScript server (`@modelcontextprotocol/server` v2) | `references/typescript-server.md` |
| Python server (`mcp` v2, `MCPServer`) | `references/python-server.md` |
| HTTP auth, scopes, token handling, threat checklist | `references/security-and-auth.md` |
| Spec changes, deprecations, v1 → v2 migration | `references/protocol-2026-07-28.md` |
| Inspector checks, evaluation questions, harness | `references/evaluation-authoring.md` |
| `server.json` and MCP Registry publishing | `references/publishing.md` |

Default to stdio for local single-user servers and Streamable HTTP for remote or
multi-user servers. Never start a new server on the deprecated HTTP+SSE transport.

## Implement one complete tool

Build one working path from validated input through authorized upstream calls to bounded,
structured output before adding more tools. Use the reference example for the chosen SDK
as the pattern: input schema with constraints, `outputSchema` with `structuredContent`,
accurate annotations, actionable `isError` results, timeouts, and pagination. Extract
shared helpers only once logic repeats.

Annotations are hints, not enforcement: authorize every operation server-side. Confirm
destructive actions through elicitation (input-required results on 2026-era connections);
for clients that cannot prompt, refuse until an explicit confirmation argument arrives and
treat it as the model's claim, not proof of user consent. Keep
credentials in environment variables or OAuth tokens validated for this server; never pass
client tokens upstream or place secrets in tool output.

## Verify and expand

1. Type-check or import-check the server.
2. Drive it with a real client: MCP Inspector CLI or an SDK client in tests, covering
   valid calls, invalid input, upstream failures, pagination, and (HTTP) 401/403/Origin.
3. For task quality, write read-only evaluation questions and run `scripts/evaluation.py`.
4. Add tools only as the requested workflow needs them; re-run checks after each change.

Start servers for testing with bounded, harness-owned processes and stop those you started.
Report working tools, observed client results, and missing or unverified capabilities;
registration alone is not completion. Publish to a registry only when the user asks.
