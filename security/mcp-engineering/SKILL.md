---
name: mcp-engineering
description: "Build MCP servers with well-named tools, workflow-oriented coverage, and clear errors. Use when exposing capabilities to agents via MCP. Pair with security/agent-security for the audit side."
---

# mcp-engineering

Build the tool the agent wishes existed: workflow-shaped, narrowly permissioned, loudly correct on misuse.

## Activate when

- Creating or extending an MCP server (Python FastMCP or TypeScript).
- Deciding tool boundaries, naming, or error formats.

## Do NOT activate for

- Auditing an existing MCP server for security (see security/agent-security).

## Procedure

1. Scope: one tool per user-meaningful workflow step, not per internal function; prefer fewer, composable tools over exhaustive coverage.
2. Naming: `verb-object` names, typed inputs, documented preconditions; errors state what was wrong, what was expected, and the safe retry.
3. Permissions: least privilege per tool; destructive tools require confirmation params and log intent.
4. Versioning: additive changes first; breaking tool-shape changes get a version bump + migration note.
5. Evaluate: scripted happy-path + misuse + adversarial-input runs before shipping.
6. Verify: run the eval script, exercise tools from a real client, and confirm logs show who called what.

## References
- Related: `../agent-architecture/`, `../../security/agent-security/`.
