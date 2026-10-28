---
name: engineer-plugin-mcp
description: >-
  Build AI-IDE plugin MCP elements - stdio JSON-RPC servers, tool schemas, host
  wiring for Claude Code/Codex, event-name mapping and validation. Use when
  building or adding an MCP server to a plugin. Not for plugin manifests or
  packaging.
---

# Plugin MCP Engineer

Use this skill for MCP tools inside an AI IDE plugin. Keep server implementation host-neutral and generate host-specific wiring separately.

## Official Docs First

Do not treat this skill as a full MCP protocol or host configuration
specification. Protocol versions, SDK APIs, host config fields, approval
policies, and validation commands can change. Before implementation, open the
current official docs for the MCP protocol and every requested host, then cite
or link the pages used in the output.

- MCP intro: https://modelcontextprotocol.io/docs/getting-started/intro
- MCP latest specification: https://modelcontextprotocol.io/specification/latest
- Claude Code MCP: https://code.claude.com/docs/en/mcp
- Claude Code plugins: https://code.claude.com/docs/en/plugins
- Codex MCP: https://developers.openai.com/codex/mcp
- Codex plugin build guide: https://developers.openai.com/codex/plugins/build
- Cursor MCP: https://cursor.com/docs/mcp
- Cursor extension API: https://cursor.com/docs/extension-api

Fetch only the sections needed for the current task. For any host not listed,
find its official MCP, plugin, extension, or connector docs first. If no
official docs exist, say so and separate verified behavior from assumptions.

## Workflow

1. Classify the request.
   - Design, plan, evaluate, or "help me design" -> output an MCP design only;
     do not create files or run tests.
   - Create, implement, scaffold, write files, or modify this repo -> implement
     after the protocol docs, host docs, and validation path are clear.
   - A concrete server or tool name does not make a request an implementation
     request. The verbs decide.
2. Define the tool contract.
   - Server name, tool names, input schema, result shape, errors.
   - Whether calls read, write, or trigger external side effects.
3. Choose the transport and implementation path from current docs.
   - Prefer official MCP SDKs or the current MCP specification for protocol
     details instead of copying method schemas into this skill.
   - Use stdio, HTTP, or host-supported transports only after checking host docs.
   - Keep request/response handling deterministic and fail clearly on bad input.
4. Keep server state explicit.
   - Prefer environment or command arguments for config.
   - Validate required paths and credentials at startup.
   - Fail clearly when dependencies are missing.
5. Generate host wiring.
   - Use each host's current docs for config file location, field names,
     environment expansion, approval policy, and plugin-scoped server settings.
   - Keep host wiring outside the server implementation.
   - Document how each host exposes tool names to the model, logs, approvals,
     and hooks. Treat server/tool prefixes or event names as host-specific until
     current docs prove otherwise.
6. Validate with a probe.
   - Confirm the protocol handshake and tool call using the current MCP spec or
     official SDK tooling.
   - Confirm arguments and result returned to the model.
   - Capture server logs for evidence.

## Server Rules

- Keep protocol strict and deterministic.
- Use stable tool names and task-level input/output contracts; do not freeze full
  MCP protocol schemas in this skill.
- Do not infer required fields silently.
- Separate host config generation from server code.
- Do not depend on a specific model or IDE binary in server logic.
- Tool names should be stable even if host event names are prefixed differently.

## Output Shape

For implementation requests, produce:

- Server file.
- Tool schema.
- Official docs consulted.
- Host-specific wiring snippets.
- Host-specific exposed tool-name and event-name mapping.
- Smoke-test command or fixture.
- Notes for approvals or trust prompts.

For design-only requests, return the same shape as a concise design response
without writing files or running smoke tests.

## Validation Notes

- Non-interactive hosts may need documented approval settings for automated MCP calls.
- Host output can show connected MCP servers and tool calls; verify from the
  current host docs before relying on a specific event shape.
- Hook matchers for MCP may use host-specific tool-event names; keep that mapping in wrapper code or documentation.
