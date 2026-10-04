---
name: cloudflare-mcp-usage
description: Use when working with the official Cloudflare API MCP server, especially when querying or changing Cloudflare account resources, debugging MCP/API/GraphQL errors, or when the model might otherwise guess Cloudflare API endpoints, parameters, datasets, permissions, or time formats. Guides correct docs/search/execute usage, authentication checks, entitlement handling, GraphQL analytics calls, and common Cloudflare API failure modes.
---

# Cloudflare MCP Usage

Use this skill when a task asks to use Cloudflare MCP, Cloudflare API MCP, or a Cloudflare MCP server to inspect, query, configure, deploy, or debug Cloudflare resources.

The official broad Cloudflare API MCP is a Code Mode server. Treat it as a discovery-and-execution interface, not as a set of memorized product tools.

## Core Rule

Never invent Cloudflare API paths, GraphQL datasets, request bodies, parameter names, or tool call shapes from memory.

Use this order:

1. Use MCP documentation/search capability to find the relevant endpoint, schema, dataset, permissions, and examples.
2. Confirm whether the request is account-scoped, zone-scoped, user-scoped, or token-scoped.
3. Use MCP execute capability only after the call shape is known.
4. Inspect Cloudflare response bodies, not just HTTP status. GraphQL can return HTTP 200 with `errors`.

If the MCP server exposes `docs`, `search`, and `execute`, prefer:

- `docs`: learn how the MCP server expects calls to be written.
- `search`: find Cloudflare API endpoints, OpenAPI operations, GraphQL datasets, parameter names, and permission requirements.
- `execute`: run the final request, using the discovered endpoint and exact parameter names.

## Before Calling

Check these details before execute:

- Resource identity: account ID, zone ID, worker/script name, route, DNS record ID, or rule ID.
- Scope: account APIs usually need account ID; zone APIs usually need zone ID.
- Permission: token must include the product-specific read/edit permission and the resource must be inside the token's allowed account or zone scope.
- Operation risk: for create, update, delete, purge, deploy, rotate, or security policy changes, explain the impact and get confirmation unless the user has already clearly approved it.
- Time window: analytics/log queries should start with a narrow range.

## Authentication Errors

Treat these as authentication/session problems first:

- `10000: Authentication error`
- `401 Unauthorized`
- `Authentication failed`
- `Invalid token`
- Missing OAuth/session/token errors

Do not fix these by changing business parameters. Diagnose:

- Is the MCP client authenticated to the Cloudflare MCP server?
- Is the Cloudflare API token present in the runtime where the request executes?
- Is the request using `Authorization: Bearer <API_TOKEN>` rather than legacy API-key headers?
- Has the token expired, been deleted, or been revoked?
- Does the token use Client IP Address Filtering? The broad official Cloudflare MCP does not support those tokens.

Useful verification request:

```text
GET /client/v4/user/tokens/verify
```

## Permission And Entitlement Errors

Treat these as authorization or product-availability problems:

- `403`
- `not authorized for that account`
- `zones [...] are not authorized`
- `does not have access to the path`
- `requires entitlement: ...`
- `node is not available`
- `node is disabled`

Diagnose in this order:

1. Confirm account ID or zone ID is correct.
2. Confirm the token is scoped to that account or zone.
3. Confirm the token has the required read/edit permission.
4. For `requires entitlement: ...`, explain that the account lacks the required product capability, plan, or subscription. Do not keep retrying with random parameters.
5. Offer a fallback dataset or endpoint only after searching for an available alternative.

Example: `requires entitlement: cfone.threat.events` means the account is not entitled to that Cloudflare One threat-events capability. It is not a datetime or JSON-format issue.

## GraphQL And Analytics

For analytics, logs, security events, Workers metrics, DNS analytics, firewall/WAF events, or account-wide reporting:

- Search for the correct GraphQL dataset first.
- Confirm whether it belongs under `viewer.accounts(...)` or `viewer.zones(...)`.
- Check dataset availability when possible with settings/introspection before assuming it exists.
- Always specify `limit` where the dataset requires it.
- Prefer a small time range first, then expand.
- Request only needed fields and dimensions.
- Check response `errors` even when HTTP status is 200.

Common GraphQL errors and likely meaning:

- `unknown field`: wrong dataset, wrong field, or wrong account-vs-zone scope.
- `query contains error`: invalid schema, bad variables, or malformed GraphQL.
- `number of fields can't be more than...`: requested too many fields.
- `limit must be positive...`: missing or excessive limit.
- `query time range is too large...`: reduce the time window.
- `cannot request data older than...`: requested beyond retention for the account/product.
- `rate limiter budget depleted` or `query consumed excessive resources`: simplify query, reduce range, or wait before retrying.

## Time Format Rules

Cloudflare GraphQL `Time` filters such as `datetime_gt`, `datetime_geq`, `datetime_lt`, and `datetime_leq` must use UTC ISO 8601 seconds:

```text
2026-06-16T00:00:00Z
```

Do not pass:

- `2026-06-16`
- `2026-06-16 00:00:00`
- `2026-06-16T08:00:00+08:00`
- natural language such as `yesterday`
- local timezone strings

If user gives local dates or relative times, convert them to UTC before calling. If the API rejects milliseconds, remove milliseconds and keep seconds only.

For GraphQL `Date` filters, use date-only format:

```text
2026-06-16
```

Only use date-only format when the schema says the field type is `Date`, not `Time`.

## Rate Limits

Cloudflare APIs can return `429` when REST, IP, or GraphQL budgets are exhausted.

When rate limited:

- Read `Retry-After` if available.
- Do not immediately loop retries.
- Reduce query time range, number of accounts/zones, fields, and dimensions.
- Batch compatible data in one GraphQL query only when it lowers total cost.
- Cache repeated discovery results during the current task.

## Response Style

When reporting an MCP/API failure to the user:

- State which category it is: authentication, permission, entitlement, datetime, schema, retention, rate limit, or unknown.
- Mention the next smallest useful check.
- Avoid exposing tokens, full auth headers, or sensitive account data.
- If the failure is caused by account capability or plan, say so plainly and stop retrying that unavailable capability.
