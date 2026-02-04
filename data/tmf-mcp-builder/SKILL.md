---
name: tmf-mcp-builder
description: Build TM Forum (TMF) MCP servers from TMF OpenAPI specs (TMF6xx/7xx YAML). Use when you are given a TMF OpenAPI file and asked to (1) implement an MCP server exposing TMF operations as tools, (2) generate a mock TMF API server + client + MCP layer, or (3) standardize tool naming, create/update inputs, $ref/allOf handling, and /hub event-subscription patterns for TMF APIs.
---

# TMF MCP Builder

## Workflow (decision tree)

1. **Choose the product shape**
   - **Wrap a real TMF API**: Implement only the MCP server + HTTP client; no mock server.
   - **Generate a full dev sandbox**: Mock server (FastAPI) + HTTP client + MCP server that proxies to the mock.

2. **Choose the MCP framework (Python)**
   - **Use the official `mcp` Python SDK + `FastMCP`** (recommended): implement tools directly with `@mcp.tool` and choose the transport (stdio or HTTP) based on your deployment needs.

3. **Choose the implementation approach**
   - **Hand-build**: Use this skill as a checklist and build the server normally.
   - **LLM-assisted generation (this repo)**: Use `tmf_llm_agent.py` to generate a starter implementation from an OpenAPI YAML, then tighten tool schemas and edge cases.

## Conventions (TMF-specific)

### Naming

- **Files** (recommended for generated outputs)
  - `tmf###_mock_server.py`
  - `tmf###_client.py`
  - `tmf###_mcp_server.py`
  - `run_mock_server.py`, `run_mcp_server.py`
- **Tools**
  - Use snake_case with TMF prefix: `tmf{tmf_number}_{action}_{resource}`
  - Standard actions: `list`, `get`, `create`, `patch` (or `update`), `delete`, plus `health_check`

### Input ergonomics: create/update tools

For TMF  create  operations, prefer **field-level parameters** (LLM-friendly) and rebuild the TMF JSON internally.

- Read `references/resource-creation-guidelines.md` before implementing `create_*` tools.
- Avoid a single  blob  parameter like `customer: dict` unless you also provide ergonomic field inputs.

### OpenAPI-driven behavior

When generating mock behavior from TMF OpenAPI:

- Treat `$ref` resolution as mandatory for realistic sample payloads.
- Treat `allOf` as mandatory (TMF uses it heavily). Merge allOf schemas (including cases where `type: object` and `allOf` both exist).
- Identify  main resources  from the path set (e.g., `/customer`, `/product`, `/service`) and implement full CRUD for those first.

### /hub and event endpoints

- Implement `/hub` endpoints only if required by the spec or your use case.
- If you implement them, keep them consistent: create/get/delete subscription, and store subscriptions in-memory for mocks.

## Practical build steps (Python)

1. **Inventory the spec**
   - Find the correct TMF OpenAPI YAML in https://github.com/tmforum-apis (users must pick the TMFxxx spec/version that matches their API).
   - Determine base paths, main resources, and required operations.
   - Extract required fields for create/patch input models.

2. **Ensure tmf_commons is available**
   - Copy `assets/tmf_commons` into your project root (or otherwise ensure it is importable). You can use `scripts/copy_tmf_commons.py --dest <project-root>`.

3. **Implement the HTTP client**
   - Use `httpx.AsyncClient`.
   - Provide consistent error handling and timeouts.

4. **Implement the mock server (optional)**
   - Use in-memory storage keyed by resource.
   - Pre-populate sample objects.
   - Support: list (filter/paginate), get by id, create, patch, delete.

5. **Implement the MCP server**
   - Expose tools for the main resources.
   - Make list tools pageable (`limit`, `offset` or cursor).
   - Return predictable structured JSON (and optionally a markdown view if your framework supports it).

6. **Validate tool usability**
   - Tool names are discoverable.
   - Create/update inputs are not "blob-only".
   - Errors are actionable.

7. **Add an evaluation set (recommended)**
   - Create 10 read-only questions that require multiple tool calls.
   - If you need a template, follow the approach in the general mcp-builder evaluation guidance.
8. **Generate README-TMFxxxx (required)**
   - Create a `README-TMF####.md` file as the final step (after servers and tools are implemented).
   - Use the TMF number from the OpenAPI spec (for TMF620, generate `README-TMF620.md`).
   - Include: overview, endpoints/tools list, run instructions (mock server + MCP server), and environment variables.
9. **Add requirements.txt (required)**
   - Create a `requirements.txt` in the output folder that lists runtime dependencies.
   - Include at least: `fastapi`, `uvicorn`, `httpx`, `mcp`, `pyyaml`.
## Bundled assets

- **tmf_commons**: copy ssets/tmf_commons into your project root when you want the shared mock server utilities (or run scripts/copy_tmf_commons.py --dest <project-root>).
## References (load as needed)

- **Bundled assets**: ssets/tmf_commons (copy into your project root if you need the shared mock server utilities).

- **All-in-one generator prompt**: `references/TMF_MCP_SERVER_CREATION_PROMPT_all-in-one.md`
- **Libraries-based generator prompt**: `references/TMF_MCP_SERVER_CREATION_PROMPT_libraries.md`
- **Create/update input rule (important)**: `references/resource-creation-guidelines.md`




