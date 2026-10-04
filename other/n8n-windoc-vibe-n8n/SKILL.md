---
name: n8n
description: Work with the n8n Public API safely and efficiently, including authentication, pagination, endpoint selection, request shaping, and troubleshooting. Use when Codex is asked to read, create, update, transfer, or delete n8n resources (workflows, executions, credentials, users, projects, variables, tags, data tables), or when converting n8n OpenAPI specs into runnable API calls or automation code.
---

# n8n API

Use this skill to plan and execute n8n Public API calls with consistent guardrails.

Python environment convention for this repo:
- Create/manage environments with `uv venv`.
- Run Python with `uv run`.
- Store API config in repo `.env` using:
  - `N8N_BASE_URL=https://your-n8n-host/`
  - `N8N_API_KEY=your-api-key`

## Quick Start

1. Confirm base URL for the target instance.
2. Send API key in `X-N8N-API-KEY`.
3. Use `/api/v1` as the API base path.
4. Default to `limit=100`; do not exceed `250`.
5. For list endpoints, follow `nextCursor` until null.
6. Validate required IDs and path parameters before mutating calls.
7. Prefer a read call before a write call when IDs are uncertain.

## Workflow

### 1. Establish API Context
- Build base endpoint as `{instanceBaseUrl}/api/v1`.
- Verify auth header exists: `X-N8N-API-KEY: <key>`.
- If available, inspect repository `api-1.json` first for operation IDs and schemas. This file is the OpenAPI document used for n8n API reference docs.

### 2. Choose Endpoint by Intent
- Workflows: list/get/create/update/delete/transfer.
- Executions: list/get/delete/retry/stop.
- Credentials: list/create/update/delete/schema/transfer.
- Projects, users, variables, tags, data tables: use corresponding resource endpoints.

### 3. Shape Request Correctly
- Keep `Content-Type: application/json` for request bodies.
- Include only fields supported by the endpoint schema.
- Respect role/ownership requirements, especially for credentials and admin-only operations.

### 4. Execute Safely
- For destructive operations, fetch the resource first and confirm ID.
- Prefer smaller test calls before bulk operations.
- Capture and surface HTTP status and response body when calls fail.

### 5. Handle Pagination
- If response contains `nextCursor`, request again with `?cursor=<nextCursor>`.
- Stop when `nextCursor` is `null` or missing.
- Aggregate `data` arrays across pages.

## Output Expectations

- Return runnable examples (`curl`, JavaScript `fetch`, or a language requested by user).
- Include full URL, headers, and body for each call.
- State assumptions explicitly (instance URL, API key source, project/workflow IDs).
- For troubleshooting, include likely causes for `400`, `401`, `403`, `404`, and `409`.

## References

- Prefer using `scripts/n8n_api.py` for Workflow and Execution tasks before hand-writing API calls.
- Script examples:
  - View workflow: `uv run .agents/skills/n8n/scripts/n8n_api.py workflow view --id <workflowId>`
  - Download workflow JSON: `uv run .agents/skills/n8n/scripts/n8n_api.py workflow download --id <workflowId> --out workflow.json`
  - Create workflow: `uv run .agents/skills/n8n/scripts/n8n_api.py workflow create --file workflow.json`
  - Edit workflow: `uv run .agents/skills/n8n/scripts/n8n_api.py workflow edit --id <workflowId> --file workflow-updated.json`
  - Delete workflow: `uv run .agents/skills/n8n/scripts/n8n_api.py workflow delete --id <workflowId>`
- Execution examples:
  - List executions: `uv run .agents/skills/n8n/scripts/n8n_api.py execution list --status running --all-pages`
  - Retry execution: `uv run .agents/skills/n8n/scripts/n8n_api.py execution retry --id <executionId> --load-workflow`
  - Stop execution: `uv run .agents/skills/n8n/scripts/n8n_api.py execution stop --id <executionId>`
- Read `references/n8n-reference.md` for base URL/auth rules, pagination model, and endpoint groups.
- Read `references/workflow-node-generation-guide.md` for workflow JSON generation rules, node wiring patterns, and full node catalog from local `workflow/*.json` analysis.
- Use `../api-1.json` as the repository-local copy of the n8n API reference OpenAPI document when generating exact payload shapes.
