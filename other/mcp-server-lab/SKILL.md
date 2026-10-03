---
name: mcp-server-lab
description: >
  Inspect, test, debug, or integrate MCP servers for Codex workflows. Use for
  MCPJam, MCP Inspector, stdio/HTTP MCP configs, tools/resources/prompts,
  Apps SDK widgets, OAuth checks, conformance, evals, or creating a local MCP
  integration plan. Skip when the task is specifically to design repeatable CI
  conformance gates or release diffs; use
  `$auto-skill-build-mcp-conformance-harness` instead.
---

# MCP Server Lab

Treat every MCP server as a tool surface that needs inspection before trust.

## Intake Checklist

1. Read README and license.
2. Inspect manifests and install scripts.
3. Identify transport: stdio, HTTP, SSE, hosted.
4. Identify auth and secrets.
5. List tools/resources/prompts.
6. Classify each tool by capability: read, write, shell, network, filesystem, credential-sensitive.
7. Test with a disposable project first.

## MCPJam Flow

When MCPJam is available, prefer JSON outputs:

```bash
npx @mcpjam/inspector@latest
mcpjam server probe --url <url> --quiet --format json
mcpjam tools list --url <url> --quiet --format json
```

For CI gates, JUnit/XML reports, protocol/OAuth/apps conformance matrices, or
tool-surface release diffs, switch to
`$auto-skill-build-mcp-conformance-harness`.

For local stdio servers, use the terminal or desktop inspector rather than the
hosted web app.

## Output

```md
# MCP Integration Report
## Server
## Transport/Auth
## Tools
## Safe Use Cases
## Risky Capabilities
## Test Result
## Codex Config Snippet
```

Read `references/mcp-server-catalog.md` for server selection and safety rules.

## Validation

- Transport, auth, and tool list are documented before integration.
- Shell/filesystem/network/account-control tools route through `$mcp-safety-review`.
- CI/release-gate requests route to `$auto-skill-build-mcp-conformance-harness`.
