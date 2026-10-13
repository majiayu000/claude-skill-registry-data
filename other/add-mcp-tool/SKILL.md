---
name: add-mcp-tool
description: Add a tool to one of the MCP servers MCP clients (Claude, IDEs, agents) connect to - the api's (todos, at /api/mcp) or the AI service's (documents, at /ai/mcp). Use when the user wants an AI client to be able to read or do something new in a workspace.
argument-hint: <tool name> <api|ai>
---

# Add an MCP tool

Both servers expose only allowlisted tools, each behind a scope the user approved for
one workspace on the consent page. Tools act as the user, in that workspace, under
row-level security, like any request. docs/auth.md, "OAuth for MCP clients", has the
whole flow.

1. **Scope.** Reuse one from `MCP_SCOPES` in `packages/contracts/src/mcp.ts`, or add
   one there and to `MCP_SERVER_SCOPES` for the server that serves it. A new scope needs
   its consent text, `oauth.scopes.<scope>`, in every `packages/i18n/messages/*.json`,
   and the api's resource policy in `apps/api/src/auth/auth-plugins.ts` (the `mcp`
   plugin's `resources`) picks it up from `MCP_SERVER_SCOPES`.
2. **The tool, in the api** (`apps/api/src/mcp/mcp.server.ts`): register it in
   `createMcpServer` behind its scope, as an explicit adapter over a service method, with
   the contract's own input schema (`packages/contracts/src/api`). Errors are `AppError`s,
   which `run()` turns into a tool error in the caller's language. A service the tool
   needs goes into `McpServerDependencies`.
3. **The tool, in the AI service** (`apps/ai/app/mcp_server.py`): a `@server.tool` in
   `create_mcp_server`, starting with `guard()` for the caller, through `tenant(org_id)`
   for data, returning a Pydantic model from `app/schemas.py`.
4. **Tests.** api: `apps/api/test/mcp.integration.test.ts` (real OAuth tokens through the
   official MCP client): the tool is listed only with its scope, it acts in the approved
   workspace only, and a revoked grant stops it. ai: `apps/ai/tests/test_mcp.py`.
5. Update the tools table in `docs/auth.md`.

## Done when

- `bun run test:integration` passes (the MCP suites), and `bun run check-types`.
- The `security-reviewer` agent (a new capability for outside clients) reports nothing
  blocking; for the AI service, the `python-reviewer` agent too.
- By hand, once: a real MCP client connected to the local site lists and calls it
  (docs/testing.md, "Not tested automatically").
