---
name: openapi-to-mcp-skill
description: >
  Convert OpenAPI/Swagger APIs into Codex-friendly MCP/tool workflows and
  generated skills. Use when the user wants to expose an API to agents, create
  a skill from API docs, use toolcast-style conversion, or design safe API
  tool schemas. Triggers: OpenAPI to MCP, Swagger to tools, API tool plan,
  generate MCP server from API spec. Skip when there is no stable spec or the
  user only needs one ad-hoc HTTP request.
---

# OpenAPI To MCP Skill

Use this to turn an API into a narrow, safe agent tool surface.

## Workflow

1. Prefer a local OpenAPI/Swagger spec file. If the spec must be fetched, record
   the URL and do not send credentials.
2. Run the read-only surface audit when a local spec is available:

   ```bash
   python3 plugins/codex-supercharge/scripts/openapi_surface_audit.py path/to/openapi.json
   ```

3. Inspect auth, servers, paths, schemas, request bodies, response shapes, rate
   limits, and write methods.
4. Group endpoints into workflows, not raw endpoint dumps.
5. Mark each operation:
   - read-only
   - write
   - destructive
   - admin
   - credential-sensitive
6. Generate a minimal MCP/tool plan or capability manifest.
7. Create a Codex skill that teaches when and how to use the API.
8. Add safety confirmations for write/destructive/admin operations.

## Tool Plan Template

```md
# API Tool Plan
## Auth
## Read Tools
## Write Tools
## Destructive Tools
## Admin And Credential-Sensitive Tools
## Rate Limits
## Error Handling
## Required Confirmations
## Example Prompts
```

## Skill Rule

The skill should describe business workflows, not every endpoint. Keep endpoint
details in a reference file.

## References

- `references/openapi-tool-surface.md`
- `references/mcp-server-catalog.md`
- Source inspiration only, code not executed: `sources/toolcast`
- Capability-manifest inspiration: `sources/roam-code/src/roam/capability.py`

## Skip When

- The API has no spec or stable docs to inspect.
- The user only needs a one-off HTTP call, not an agent/tool surface.
- The task is only MCP conformance/release gating; use
  `$auto-skill-build-mcp-conformance-harness`.

## Validation

- Auth, rate limits, write/destructive operations, and confirmations are explicit.
- Generated tool groups map to workflows rather than raw endpoint dumps.
- Credential-sensitive operations route through `$mcp-safety-review`.
- `openapi_surface_audit.py` was run or the reason it could not run is stated.
