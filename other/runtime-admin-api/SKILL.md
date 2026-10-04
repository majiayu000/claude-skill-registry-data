---
name: runtime-admin-api
description: "Call the Mendix M2EE admin API on port 8090 directly — OQL, runtime info, and the rest, with curl examples. Use when querying a running app from a script, or when debugging connectivity to the admin port."
---

# Runtime Admin API Skill

This skill documents the Mendix M2EE admin API exposed on port 8090, including how to call it directly with curl.

## When to Use This Skill

Use this when:
- The user wants to query the running Mendix app directly (OQL, runtime info)
- The user needs to debug connectivity to the admin port
- The user wants to call the M2EE admin API from scripts or external tools
- The user asks about the Mendix admin console or management API

## Admin API Overview

The Mendix runtime exposes an HTTP admin API on port **8090** (configurable via `ADMIN_PORT` in `.docker/.env`). This API is used by the Mendix Cloud, M2EE tools, and `mxcli oql` to manage and query the runtime.

**Default credentials** (from `.docker/.env`):
- **Port**: 8090
- **Password**: `AdminPassword1!`
- **Auth method**: `X-M2EE-authentication` header with the password **base64-encoded**

## Authentication

All requests require the `X-M2EE-authentication` header containing the base64-encoded admin password:

```bash
# Encode the password
echo -n 'AdminPassword1!' | base64
# Result: QWRtaW5QYXNzd29yZDEh
```

The header value is `base64(password)` — NOT `base64(user:password)` (this is not HTTP Basic Auth).

## curl Examples

### OQL Query (Read-Only Preview)

> **Mendix 11.11 changed the wire protocol.** OQL preview moved off the M2EE
> action dispatch onto a dedicated REST endpoint `POST /dev/preview_execute_oql`,
> where the request body is the params object **directly** and the response is
> `{"data":[...]}` (no `action`/`params` wrapper, no `feedback` envelope). The
> auth header is unchanged. `mxcli oql` tries this endpoint first and falls back
> to the legacy action below on a 404 (older runtimes), so it works on both.

**11.11+ (new endpoint):**
```bash
curl -sf -X post http://localhost:8090/dev/preview_execute_oql \
  -H 'Content-Type: application/json' \
  -H "X-M2EE-authentication: $(echo -n 'AdminPassword1!' | base64)" \
  -d '{"oql":"SELECT Name FROM System.User","numberHandling":"asString"}'
# -> {"data":[{"Name":"MxAdmin"}, ...]}
```

A **failed query** on the dev endpoint returns **HTTP 200** (not 4xx/5xx) with an
`{"error":"..."}` body and no `data` field, e.g.:
```json
{"error":"An exception has occurred for the following request(s):\n\tInternalOqlTextGetRequest (depth = -1): SELECT ..."}
```
So an error must be detected by the presence of the `error` field, not by the
HTTP status. `mxcli oql` surfaces this message instead of returning empty.

**Pre-11.11 (legacy action):**
```bash
curl -sf -X post http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -H "X-M2EE-authentication: $(echo -n 'AdminPassword1!' | base64)" \
  -d '{"action":"preview_execute_oql","params":{"oql":"SELECT Name FROM System.User","numberHandling":"asString"}}'
```

**Response format** (all M2EE responses use this envelope):
```json
{
  "result": 0,
  "feedback": {
    "data": [
      {"Name": "MxAdmin"},
      {"Name": "demo_user"}
    ]
  }
}
```

- `result: 0` = success, non-zero = error
- On error: `cause` and/or `message` fields contain the error description
- Data rows are JSON objects with column names as keys

### More OQL Examples

```bash
# count entities
curl -sf -X post http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -H "X-M2EE-authentication: $(echo -n 'AdminPassword1!' | base64)" \
  -d '{"action":"preview_execute_oql","params":{"oql":"SELECT count(*) AS Total FROM MyModule.Customer","numberHandling":"asString"}}'

# join query
curl -sf -X post http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -H "X-M2EE-authentication: $(echo -n 'AdminPassword1!' | base64)" \
  -d '{"action":"preview_execute_oql","params":{"oql":"SELECT o.OrderNumber, c.Name FROM MyModule.Order o JOIN o/MyModule.Order_Customer/MyModule.Customer c","numberHandling":"asString"}}'
```

### Runtime Info

```bash
curl -sf -X post http://localhost:8090/ \
  -H 'Content-Type: application/json' \
  -H "X-M2EE-authentication: $(echo -n 'AdminPassword1!' | base64)" \
  -d '{"action":"runtime_status"}'
```

## Using mxcli oql (Preferred)

`mxcli oql` wraps the admin API with automatic credential resolution and output formatting:

```bash
# table output (default)
./mxcli oql -p app.mpr "select Name from System.User"

# json output for piping
./mxcli oql -p app.mpr --json "SELECT Name FROM System.User" | jq '.[].Name'

# Explicit connection (no project needed)
./mxcli oql --host localhost --port 8090 --token 'AdminPassword1!' "SELECT 1"
```

`mxcli oql` auto-reads credentials from `.docker/.env` when `-p` is provided.

## Devcontainer / DinD Connectivity

In a devcontainer with Docker-in-Docker, port 8090 on the Mendix container may bind to `127.0.0.1` inside the DinD daemon and be unreachable from the devcontainer host. `mxcli oql` handles this automatically by routing through `docker compose exec`:

```bash
# What mxcli does internally (docker exec mode):
docker compose -f .docker/docker-compose.yml exec -T mendix sh -c \
  "curl -sf -X post http://localhost:8090/ \
   -H 'Content-Type: application/json' \
   -H 'X-M2EE-Authentication: QWRtaW5QYXNzd29yZDEh' \
   -d '{\"action\":\"preview_execute_oql\",\"params\":{\"oql\":\"SELECT 1\",\"numberHandling\":\"asString\"}}'"
```

Use `--direct` to bypass docker exec and connect via HTTP directly (when the port is reachable):

```bash
./mxcli oql -p app.mpr --direct "SELECT 1"
```

## Prerequisites

The `preview_execute_oql` action requires a JVM flag on the runtime:

```
-Dmendix.live-preview=enabled
```

This is included in the default docker-compose template generated by `mxcli docker init`. If you get `"action not found: preview_execute_oql"`, re-initialize:

```bash
./mxcli docker init -p app.mpr --force
./mxcli docker run -p app.mpr --wait
```

## Configuration Reference

All settings are in `.docker/.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_PORT` | `8080` | Web application port |
| `ADMIN_PORT` | `8090` | Admin API port |
| `M2EE_ADMIN_PASS` | `AdminPassword1!` | Admin password (used for auth header) |
| `DB_PORT` | `5432` | PostgreSQL port (exposed to host) |
| `DB_NAME` | `mendix` | Database name |
| `DB_USER` | `mendix` | Database user |
| `DB_PASSWORD` | `mendix` | Database password |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Connection refused on :8090 | App not running | `mxcli docker up -p app.mpr --wait` |
| HTTP 401/403 | Wrong password | Check `M2EE_ADMIN_PASS` in `.docker/.env` |
| "Action not found: preview_execute_oql" | Missing JVM flag | `mxcli docker init -p app.mpr --force` then restart |
| Empty response | Runtime still starting | Wait for "Runtime successfully started" in logs |
| Can't reach port from devcontainer | DinD network isolation | Use `mxcli oql` (auto-routes via docker exec) or `--direct` if port is forwarded |
| Admin API binds to localhost only | Default HOCON config | Rebuild with `mxcli docker build` — auto-patches `admin.addresses = ["*"]` |

### `--direct` Mode

By default, `mxcli oql` routes queries through `docker compose exec` to avoid DinD networking issues. When the admin port is directly reachable (e.g., after the `admin.addresses` build patch), use `--direct` for faster queries:

```bash
# Direct HTTP connection (no docker exec overhead)
mxcli oql -p app.mpr --direct "SELECT Name FROM System.User"
```

The build patch `admin.addresses = ["*"]` is applied automatically by `mxcli docker build`. After rebuilding, `--direct` mode works out of the box.

## Related Skills

- [/run-app](../run-app/SKILL.md) — Start the Mendix app in Docker
- [/write-oql-queries](../write-oql-queries/SKILL.md) — OQL syntax reference
- [/docker-workflow](../docker-workflow/SKILL.md) — Full Docker build/run workflow
- [/database-connections](../database-connections/SKILL.md) — Direct PostgreSQL access
