---
name: graft
description: >-
  Use when building, refactoring, or documenting Graft apps and proxies,
  including when asked to create a tool server, API server, dual-protocol
  server, or MCP-HTTP bridge. Graft's core thesis: define tools once and serve
  them as both HTTP REST endpoints and MCP tools from the same server, with
  discovery, docs, and OpenAPI generated automatically. Covers concrete actions
  such as defining tools and handlers, configuring authentication middleware,
  setting up HTTP and stdio transports, generating OpenAPI documentation,
  wrapping existing APIs via proxy mode, and wiring up the full CLI workflow.
---

# Graft

Use this skill when the task is about creating or refining a Graft server, wrapping an existing API with Graft proxy mode, or updating contributor-facing docs and examples so they match the current `graft` package behavior.

## Product thesis

Graft's core value has three parts:

1. **Define once** — tools with a name, schema, and handler.
2. **Serve as HTTP and MCP** — from the same server, through a single shared pipeline (same auth, validation, middleware).
3. **Discovery is automatic** — agents find tools via `agent.json`, `mcp.json`, `llms.txt`. Humans get interactive docs (`/docs`) and an OpenAPI spec (`/openapi.json`). Zero configuration.

When explaining Graft, lead with all three parts. When showing examples, demonstrate both access patterns (MCP and HTTP) and mention what the server auto-serves. This applies to both source-based apps and proxy mode.

## Workflow

1. Identify the mode before proposing changes:
- App authoring: `createApp(...)`, tools, resources, prompts, HTTP routes, Node or fetch integration.
- Proxy/OpenAPI: `graft serve --openapi ...` or `graft.proxy.yaml`.
- Docs/release hygiene: README, install instructions, skills, examples, contributor checks.

2. Ground in the current repo before using memory:
- If tool access is available, inspect the current source, public exports, CLI commands, scaffold templates, and tests.
- If tool access is not available, ask for the smallest set of files or examples needed to avoid guessing.

3. Follow the current public contract in examples and reviews:
- Inline tool examples: prefer `app.tool('name', config)`.
- Modular tool examples: prefer `defineTool(...)` plus `app.tool(definedTool)`.
- Auth shapes: `true`, `['role']`, or `{ roles: [...] }`.
- MCP Streamable HTTP endpoint: `POST /mcp`.
- Auto-served framework endpoints: `/.well-known/agent.json`, `/.well-known/mcp.json`, `/openapi.json`, `/docs`, `/llms.txt`, `/llms-full.txt`, `/health`.
- Full CLI: `serve`, `dev`, `check`, `test`, `studio`, `install`, `add-tool`.
- When showing tool examples, demonstrate both the MCP `tools/call` invocation and the equivalent HTTP request (e.g. `GET /list-items?q=hello` or `POST /create-entry`).

4. Use tools where they materially improve correctness, but stay portable:
- With repo or shell access, inspect files and run validation commands after making changes.
- Without repo or shell access, state assumptions explicitly and keep recommendations tied to visible source or user-provided snippets.

5. Load only the reference you need:
- App authoring: [references/app-authoring.md](references/app-authoring.md)
- Proxy/OpenAPI wrapping: [references/proxy-openapi.md](references/proxy-openapi.md)
- Validation, docs, and release hygiene: [references/validation-release.md](references/validation-release.md)

## Quick examples

### Inline tool — both access patterns

```ts
import { createApp } from '@schrepa/graft'
import { z } from 'zod'

const app = createApp()

app.tool('list_items', {
  description: 'List items matching a query.',
  params: z.object({ q: z.string() }),
  auth: true,
  handler: async ({ q }) => ({
    items: ['hello', 'world'].filter((item) => item.includes(q)),
  }),
})

export default app
```

**MCP (`tools/call`):**
```json
{ "method": "tools/call", "params": { "name": "list_items", "arguments": { "q": "hello" } } }
```

**HTTP equivalent:**
```
GET /list-items?q=hello
Authorization: Bearer <token>
```

The same handler, auth middleware, and validation run for both.

### Proxy mode — `graft.proxy.yaml`

```yaml
target: https://petstore3.swagger.io/api/v3
tools:
  - method: GET
    path: /pet/findByStatus
    name: find_pets_by_status
    description: Find pets by status.
    parameters:
      type: object
      properties:
        status:
          type: string
  - method: POST
    path: /pet
    name: create_pet
    description: Create a pet.
    parameters:
      type: object
      properties:
        name:
          type: string
      required: [name]
```

Start the proxy server:
```
graft serve --config graft.proxy.yaml
```

Graft exposes each configured operation as both an HTTP endpoint and an MCP tool, and auto-generates `/openapi.json`, `/docs`, and discovery files.

For the direct OpenAPI path, use:
```
graft serve --openapi ./openapi.yaml --target https://api.example.com
```

## Guardrails

- Do not document unsupported behavior just because an older example mentioned it.
- Keep examples executable and small; prefer one correct pattern over many variants.
- Prefer current source and tests over stale notes, blog posts, or memory.
- Do not mention registry or publishing artifacts unless they actually exist in the repo being edited.
- When a docs claim is likely to drift, add or update an automated check.
