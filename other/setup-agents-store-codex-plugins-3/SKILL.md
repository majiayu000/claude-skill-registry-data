---
name: setup
description: This skill should be used when the user wants to "connect to Taiga", "log into Taiga", "authenticate with Taiga", "get a Taiga auth token", "set up Taiga access", or before running any Taiga REST API call. Establishes the auth token and the global request conventions (headers, pagination, version locking, the resolver).
---

# Taiga Setup & Authentication

Establish access to a Taiga instance and learn the conventions every other call depends on. Do this once per session before any other Taiga operation.

## Environment variables

The user sets these in their shell or repo `.env`. Read them — never hardcode credentials.

| Variable | Required | Meaning |
|----------|----------|---------|
| `TAIGA_API_URL` | yes | Base instance URL, e.g. `https://api.taiga.io` (hosted Taiga Cloud — has plans with project and storage limits, see the note below) or `https://taiga.mycompany.com` (self-hosted). The API lives under `${TAIGA_API_URL}/api/v1`. |
| `TAIGA_ADMIN_USERNAME` | yes | Username or email used to obtain a token. |
| `TAIGA_ADMIN_PASSWORD` | yes | Password for that account. |
| `TAIGA_AUTH_TOKEN` | derived | Obtained at runtime from the login call below; reused for the rest of the session. |

**Taiga Cloud limits.** Since 2025-10-15 the hosted service enforces plan limits on project count and storage (existing accounts had until 2026-01-01 to choose a plan). A `POST /projects`, a privacy change or a file upload on a Cloud account can therefore be refused for hitting a limit — for example `"No room left for more projects."`; read the response body before retrying. Self-hosted instances are not subject to the Cloud plans (an admin can set `MAX_PRIVATE_PROJECTS_PER_USER`-style limits of their own).

If `TAIGA_API_URL` is missing, ask the user for it. If it does not already end without a trailing slash, normalize it (`${TAIGA_API_URL%/}`).

## Step 1 — Obtain the auth token

Taiga issues a JWT from username + password via the `normal` login type. The `type` field is mandatory — omitting it is the most common login failure.

```bash
# Log in and capture both the auth token and the refresh token.
RESP=$(curl -s -X POST "${TAIGA_API_URL%/}/api/v1/auth" \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"normal\",\"username\":\"${TAIGA_ADMIN_USERNAME}\",\"password\":\"${TAIGA_ADMIN_PASSWORD}\"}")

export TAIGA_AUTH_TOKEN=$(echo "$RESP" | jq -r '.auth_token')
export TAIGA_REFRESH=$(echo "$RESP" | jq -r '.refresh')
echo "Logged in as $(echo "$RESP" | jq -r '.username') (id $(echo "$RESP" | jq -r '.id'))"
```

The response also contains `id`, `username`, `full_name`, `email`, `is_superuser`, and more. Keep `TAIGA_AUTH_TOKEN` for all subsequent requests.

## Step 2 — Verify access

```bash
curl -s -H "Authorization: Bearer ${TAIGA_AUTH_TOKEN}" \
  "${TAIGA_API_URL%/}/api/v1/users/me" | jq '{id, username, full_name}'
```

A `200` with your user object confirms the token works.

## Refreshing the token

Auth tokens expire. When a call returns `401`, refresh instead of re-logging in:

```bash
export TAIGA_AUTH_TOKEN=$(curl -s -X POST "${TAIGA_API_URL%/}/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"${TAIGA_REFRESH}\"}" | jq -r '.auth_token')
```

## Application tokens (for external/long-lived integrations)

For unattended integrations, Taiga supports application tokens instead of password login. These use a different header — `Authorization: Application <token>` rather than `Bearer`. The flow is `POST /api/v1/application-tokens/authorize` → `POST /api/v1/application-tokens/validate` → decipher the JWE. See `api-reference` → `references/auth-users.md`. For interactive ops, the username/password flow above is simpler and preferred.

## Global conventions (apply to every call)

These rules hold across the entire API. Internalize them now so individual operations stay short.

- **Base path**: every endpoint is `${TAIGA_API_URL%/}/api/v1/...`.
- **Headers**: send `Authorization: Bearer ${TAIGA_AUTH_TOKEN}` on authenticated calls and `Content-Type: application/json` on any request with a body.
- **Optimistic locking (`version`)**: editing an object (`PATCH`/`PUT` on stories, tasks, issues, epics, milestones, wiki, statuses, attachments, custom-attribute values) **requires the object's current `version`**. Always `GET` the object first, read `.version`, and include it in the body. A `400` complaining about version means the object changed — re-`GET` and retry. This prevents silently overwriting someone else's edit.
- **PATCH vs PUT**: use `PATCH` with only the changed fields (plus `version`) for partial edits. Reserve `PUT` for full-object replacement.
- **Pagination**: list endpoints paginate by default. Read the response headers — `x-pagination-count` (total), `x-pagination-current`, `x-paginated-by` (page size), `x-pagination-next` / `x-pagination-prev` (page URLs). Pass `?page=N` to walk pages, or send the header `x-disable-pagination: True` to fetch everything in one response (use sparingly on large projects). Use `-D -` with curl to inspect headers.
- **Filtering**: list endpoints accept resource filters — commonly `?project=`, `?milestone=`, `?status=`, `?assigned_to=`, `?user_story=` (tasks). Each work-item type also exposes `GET .../filters_data?project=<id>` describing the available filter values.
- **Slugs vs IDs (`/resolver`)**: the API works with numeric IDs, but humans use slugs and references (`#42`). Convert with one call:

```bash
curl -s -H "Authorization: Bearer ${TAIGA_AUTH_TOKEN}" \
  "${TAIGA_API_URL%/}/api/v1/resolver?project=my-project-slug&us=42" | jq .
# -> {"project": 7, "us": 1234}
```

- **i18n**: add `Accept-Language: <locale>` to localize server messages.

## Next steps

- For everyday workflows (create a sprint, add a story, triage an issue, build a report) → use the `common-operations` skill.
- For the full endpoint catalog of every resource → load the `api-reference` skill and open the relevant `references/*.md` file.
- When a call fails → use the `troubleshoot` skill.