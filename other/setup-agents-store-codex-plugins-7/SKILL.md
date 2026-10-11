---
name: setup
description: This skill should be used when the user wants to "connect to Outline", "authenticate with Outline", "set up Outline access", "use my Outline API key", or before running any Outline REST API call. Establishes the API key + base URL from the environment and the global request conventions (RPC POST style, Bearer header, response envelope, limit/offset pagination, sorting, rate limits, policies).
---

# Outline Setup & Authentication

Establish access to an Outline workspace and learn the conventions every other call depends on. Do this once per session before any other Outline operation. Authentication is a single static key — there is no login/token-exchange step.

## Environment variables

The user sets these in their shell or repo `.env`. Read them — never hardcode or print the key.

| Variable | Required | Meaning |
|----------|----------|---------|
| `OUTLINE_API_URL` | yes | API base **including `/api`**. Cloud: `https://app.getoutline.com/api`. Self-hosted: `https://wiki.mycompany.com/api`. |
| `OUTLINE_API_KEY` | yes | Personal API key. Always begins with `ol_api_` followed by a random string. Sent as `Authorization: Bearer ${OUTLINE_API_KEY}`. |

If `OUTLINE_API_URL` is missing, ask the user for it. Normalize the trailing slash with `${OUTLINE_API_URL%/}` and build every endpoint as `${OUTLINE_API_URL%/}/<method>`. The URL already ends in `/api` — do **not** append `/api` yourself, and do not pass a URL that ends in a method name.

A user mints a key under **Settings → API & Apps** (or programmatically with `apiKeys.create` — see `api-reference` → `oauth-data-attributes.md`; the full key is shown only once). Keys grant full access to the user's data (or are scoped — see Scopes below), so treat them like passwords and never commit them.

## Step 1 — Verify access

```bash
curl -s -X POST "${OUTLINE_API_URL%/}/auth.info" \
  -H "Authorization: Bearer ${OUTLINE_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" | jq '.data | {user: .user.name, email: .user.email, team: .team.name}'
```

A `200` with `ok: true` and your user + workspace (`team`) confirms the key works. A `401` means the key is missing, wrong, or revoked — fix the key before continuing.

## Global conventions (apply to every call)

These rules hold across the entire API. Internalize them now so individual operations stay short.

- **RPC, not REST-by-noun.** Every endpoint is a **`POST`** to `${OUTLINE_API_URL%/}/<method>` where the method is dotted, e.g. `documents.info`, `collections.list`. There are **no path parameters and no GET requests** — all inputs go in the JSON body. An empty body is `-d '{}'`.
- **Headers.** Always send `Authorization: Bearer ${OUTLINE_API_KEY}`, `Content-Type: application/json`, and `Accept: application/json`. (Attachment uploads to cloud storage are the one exception — see `api-reference` → `attachments-fileops.md`.)
- **Response envelope.** Successful responses are `{ "ok": true, "status": 200, "data": …, "pagination"?: {…}, "policies"?: [...] }`. **The payload you want is under `.data`** — always `jq '.data'`. List endpoints put the array in `.data`; a few wrap it (e.g. `.data.users` + `.data.memberships`) — check the reference file.
- **Errors.** Failures return `{ "ok": false, "error": "…", "message": "…", "status": <code> }` with the matching HTTP status. `400` validation, `401` unauthenticated, `403` unauthorized (policy), `404` not found, `429` rate limited.
- **Pagination.** List methods take `{"limit": 25, "offset": 0}` in the body (**default limit 25**). The response `pagination` echoes them and adds `nextPath` (e.g. `/api/documents.list?limit=25&offset=25`) as a shortcut to the next page. Walk results by incrementing `offset` until a short/empty page returns.
- **Sorting.** List methods accept `{"sort": "updatedAt", "direction": "DESC"}` (`direction` is `ASC` or `DESC`). Document search uses `sort` values `relevance|createdAt|updatedAt|title`.
- **IDs.** Objects are addressed by UUID. Documents, collections, and templates also accept a short `urlId` (e.g. `hDYep1TPAM`), and `documents.info` additionally accepts a `shareId`. Humans speak in titles — resolve a title to an id first with `documents.search` / `documents.search_titles` / `collections.list` before acting.
- **Rate limits.** Mutating endpoints are stricter than reads. Exceeding a limit returns `429` with a `Retry-After` header (seconds to wait). Inspect with `curl -s -D - …` and back off. (Outline v1.7.1+ raised the default model-creation limit from 10 to 25 per minute; self-hosted admins can tune limits with `RATE_LIMITER_MULTIPLIER`.)
- **Policies.** Most responses include a `policies` array describing the current key's authorized actions on each object. For most uses you can ignore it; when a write returns `403`, the policy is telling you the key lacks that permission — respect it.

## Scopes (optional, for scoped keys)

API keys can be global (`read`, `write`) or narrowed — by namespace (`documents:read`, `collections:write`), by endpoint (`documents.info`), or by wildcard (`documents.*`). If a previously-working call starts returning `403`, the key may be scoped too narrowly for that method — Outline v1.10.1 validates API-key and OAuth scopes at the model layer, so a scoped key can become stricter after a server upgrade; re-check it.

## Optional: Outline's built-in MCP server

Every workspace also exposes an MCP server at `<workspace-origin>/mcp` (Streamable HTTP; OAuth by default, or `Authorization: Bearer <api-key>`; toggled under **Settings → Workspace → AI**). It is optional — this plugin works with REST alone. Setup, URL rules and the REST-vs-MCP choice are in the plugin `README.md` (section "Built-in Outline MCP server").

## Next steps

- For everyday workflows (create a doc, search, share, manage people, report) → use the `common-operations` skill.
- For the full endpoint catalog of every resource → load the `api-reference` skill and open the relevant `references/*.md` file (or the bundled `references/outline-openapi.yml` spec).
- When a call fails → use the `troubleshoot` skill.