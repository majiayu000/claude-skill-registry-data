---
name: xquik-data
description: Use when collecting or analyzing X/Twitter data through Xquik REST, OpenAPI, MCP, webhooks, or SDK workflows.
---

# Xquik Data

## Overview

Use Xquik as a source-backed X/Twitter data workflow layer. This skill helps an agent choose between the REST API, OpenAPI schema, MCP server, SDKs, and webhooks, then return traceable output with clear setup gaps.

## When to Use

Use this skill when the user asks for:

- Collecting X/Twitter posts, profiles, trends, monitors, or extraction results through Xquik
- Building an agent workflow around the Xquik REST API, OpenAPI schema, MCP server, SDKs, or webhooks
- Turning Xquik results into a report, table, exported dataset, or monitoring handoff
- Checking which Xquik integration surface best fits a task

## Do not use

Do not use this skill for:

- Private messages, non-public data, or login-gated content the user is not authorized to access
- Guessing endpoint behavior without checking Xquik docs or the OpenAPI schema
- Posting, deleting, or changing accounts unless the user explicitly asks and has authorized the action
- Bypassing platform rules, access controls, or rate limits

## Instructions

1. Identify the user's goal.
   - Classify the task as `extract`, `monitor`, `report`, `webhook`, `mcp`, `sdk`, or `api-design`.
   - Note the required entities: keywords, accounts, post URLs, date range, output format, and refresh cadence.
   - Ask for missing required inputs before claiming a run can proceed.

2. Pick the integration surface.
   - Use the docs at `https://docs.xquik.com/api-reference/overview` for REST API workflow design.
   - Use `https://xquik.com/openapi.json` when endpoint names, request fields, or response shapes matter.
   - Use `https://docs.xquik.com/mcp/overview` when the user wants an agent-native MCP connection.
   - Use webhooks when the user needs event delivery instead of polling.

3. Check access and secrets safely.
   - Confirm whether the user already has an Xquik API key, MCP configuration, SDK client, or webhook secret.
   - Never print, store, or repeat API keys or webhook secrets.
   - If credentials are missing, prepare the exact setup steps without inventing a key.

4. Build the request plan.
   - State the endpoint or tool, inputs, output fields, pagination plan, and retry expectations.
   - Keep unsupported endpoints or uncertain fields out of runnable examples until the OpenAPI schema confirms them.
   - Prefer read-only collection for analysis tasks.

5. Run or prepare the workflow.
   - If a configured client or MCP tool is available, run the smallest safe request first.
   - If no client is available, provide a copy-ready plan using documented endpoints and required fields.
   - For repeated jobs, include webhook or monitor setup notes and failure handling.

6. Return traceable output.
   - Include the input scope, source surface, result count, important fields, limits, and follow-up steps.
   - Separate returned Xquik data from analysis or recommendations.
   - Mark partial data, missing credentials, empty results, or unsupported operations clearly.

## Default Output

```markdown
# Xquik Data Workflow

## Scope
- Goal:
- Source surface:
- Inputs:
- Credentials:

## Request Plan
- Endpoint or tool:
- Required fields:
- Pagination or refresh:
- Output fields:

## Result Summary
- Status:
- Items:
- Notable fields:
- Limits:

## Next Steps
- ...
```

## References

- Xquik API overview: https://docs.xquik.com/api-reference/overview
- Xquik OpenAPI schema: https://xquik.com/openapi.json
- Xquik MCP overview: https://docs.xquik.com/mcp/overview
- Xquik MCP manifest: https://xquik.com/.well-known/mcp.json

## Limits and Known Issues

- Live execution requires a valid Xquik API key, configured MCP connection, or SDK client.
- X/Twitter data access depends on the user's authorization, request scope, and Xquik API limits.
- Current API details can change, so check the public docs or OpenAPI schema before writing runnable code.
