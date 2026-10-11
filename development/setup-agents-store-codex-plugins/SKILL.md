---
name: setup
description: This skill should be used when verifying Dokploy MCP connection, CLI installation, and API access. Use when user says "set up dokploy", "verify dokploy connection", "check dokploy", "test dokploy access", or enables the dokploy-dev plugin for the first time.
---

# Dokploy Setup and Verification

Verify all three access methods to Dokploy: MCP tools, CLI, and REST API. Run each step in order. Report the result of each step before moving to the next.

---

## Prerequisites

The plugin needs two values — the Dokploy **base URL** (no `/api` suffix) and an **access token** — wired into all three interfaces:

| Interface | How it reads credentials | What to set |
|---|---|---|
| **MCP** (`@dokploy/mcp`) | `.mcp.json` `env` block expands `${DOKPLOY_URL}` / `${DOKPLOY_API_KEY}` from the Claude Code environment (e.g. the `env` block of `.claude/settings.local.json`, or your shell) | `DOKPLOY_URL`, `DOKPLOY_API_KEY` |
| **REST API** (`curl`) | Same env vars in your shell | `DOKPLOY_URL`, `DOKPLOY_API_KEY` |
| **CLI** (`@dokploy/cli`) | Reads the SAME `DOKPLOY_URL`/`DOKPLOY_API_KEY` env vars (or a CWD `.env`); falls back to `config.json` written by `dokploy auth -u <url> -t <token>` | `DOKPLOY_URL`, `DOKPLOY_API_KEY` (or run `dokploy auth`) |

- `DOKPLOY_URL` = the server **base URL without `/api`** (e.g. `https://dokploy.example.com`). MCP and REST endpoints live at `/api/…` under it.
- `DOKPLOY_API_KEY` = an access token from **Settings > API/Tokens** (or **Settings > Profile**). The **same token** works for MCP, REST, and the CLI.

Before verifying, confirm `DOKPLOY_URL` and `DOKPLOY_API_KEY` resolve to real values in the session environment. If either is missing, the MCP server fails with **"Invalid URL"** (empty `DOKPLOY_URL`) or **401** (bad key).

### Optional: reduce the exposed tool surface

The official `@dokploy/mcp` server exposes 604 tools across 57 categories. If that is more than you need, set one of these in the plugin's `.mcp.json` `env` block: `DOKPLOY_TOOL_PRESET` (`minimal`, `core`, `deploy`, `databases`, `git`; `@dokploy/mcp` ≥ 0.30.0), or `DOKPLOY_ENABLED_TAGS` — a comma-separated list of categories (e.g. `project,application,domain,compose,postgres,settings,deployment,docker,ai`) that takes priority over the preset — and optionally `DOKPLOY_DISABLED_TAGS` to drop categories from the result. No preset contains `docker`, `ai`, `settings`, `rollback` or `schedule`, which `/dokploy-dev:debug` needs.

### Secrets are redacted by default

`@dokploy/mcp` ≥ 0.30.0 runs with `DOKPLOY_REDACT_ENV=true`: MCP responses show `[REDACTED]` for `env`, `buildArgs`, passwords, tokens and keys (not even variable names), while REST and the CLI return real values. Writes still work. Details, the exact field rules and a names-only recipe are in the `mcp-patterns` skill ("Redaction"). Set `DOKPLOY_REDACT_ENV=false` in the `.mcp.json` `env` block only if you knowingly want raw values in the model context; reconnect the server afterwards.

### How to obtain an API key

1. Log in to the Dokploy dashboard.
2. Navigate to **Settings > API/Tokens**.
3. Click **Generate Token**.
4. Copy the token immediately — it is shown only once.

---

## Step 1: Verify MCP Connection

Call the MCP tool to list all projects:

```
mcp__plugin_dokploy-dev_dokploy__project-all
```

**No parameters required.**

### Expected result

A JSON array of project objects. Even an empty array `[]` confirms the MCP connection is working.

### If the call succeeds

Report: "MCP connection verified. Found N project(s)."

### If the call fails

Check these causes in order:

1. **MCP server not running** — The `.mcp.json` file must point to a running Dokploy MCP server. Verify the `command` and `args` fields are correct.
2. **Environment variables missing** — The MCP server needs `DOKPLOY_URL` and `DOKPLOY_API_KEY` passed via `env` in `.mcp.json`. Confirm they resolve to real values.
3. **npx resolution failure** — If the MCP server is launched via `npx`, ensure `@dokploy/mcp` is available. Run:
   ```bash
   npx @dokploy/mcp --version
   ```
4. **Network unreachable** — The MCP server connects to the Dokploy API. If the server is on a private network, verify the machine running Claude Code can reach it.

Report the specific error message from the MCP call to help diagnose.

---

## Step 2: Verify CLI Installation

Check the CLI is installed, then make a real call (there is NO `dokploy verify` command in the auto-generated 0.30.x CLI):

```bash
dokploy --version        # versions in lockstep with Dokploy, e.g. 0.30.7
dokploy project all      # real API call — succeeds only when auth works
```

### If the commands succeed

Report: "Dokploy CLI is installed and authenticated."

### If `dokploy` is not found

Install the CLI globally:

```bash
npm install -g @dokploy/cli
```

Then authenticate — non-interactive:

```bash
dokploy auth -u https://dokploy.example.com -t $DOKPLOY_API_KEY
```

Or simply export `DOKPLOY_URL` / `DOKPLOY_API_KEY` — the CLI reads the **same env vars** as MCP/REST, and env wins over `config.json`.

- **Server URL** — the Dokploy instance URL (e.g. `https://dokploy.example.com`). Do NOT include `/api` suffix for CLI auth.
- **Access token** — the same token used for `DOKPLOY_API_KEY` (Settings > API/Tokens). `dokploy auth` validates it against `/api/trpc/user.get` and saves it to the CLI's `config.json`.

After authentication, re-run:

```bash
dokploy project all
```

### If authentication fails

Check these causes:

1. **Wrong URL format** — The CLI expects the base URL without `/api`. If `dokploy_url` is `https://dokploy.example.com/api`, use `https://dokploy.example.com` for CLI auth.
2. **Expired token** — Generate a new token from the Dokploy dashboard.
3. **Self-signed certificate** — If the server uses a self-signed cert, set:
   ```bash
   export NODE_TLS_REJECT_UNAUTHORIZED=0
   ```
   Then retry. This is acceptable for local/dev environments only.

---

## Step 3: Verify API Access

Make a direct HTTP request to the health endpoint:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  "$DOKPLOY_URL/api/settings.health" \
  -H "x-api-key: $DOKPLOY_API_KEY"
```

Replace `$DOKPLOY_URL` (base URL, no `/api`) and `$DOKPLOY_API_KEY` with the actual configured values.

### Expected result

HTTP status code `200`.

### If 200 is returned

Report: "API access verified. Dokploy server is healthy."

### If a non-200 status is returned

| Status Code | Cause | Fix |
|---|---|---|
| `401` | Invalid or expired API key | Generate a new token in **Settings > API/Tokens**. Also verify you used the `x-api-key` header (NOT `Authorization: Bearer`) |
| `403` | Token lacks required permissions | Check token scope — it must have admin access |
| `404` | Wrong URL path | `dokploy_url` must be the base URL **without** `/api` (e.g. `https://dokploy.example.com`). Append `/api/<endpoint>` in curl calls |
| `000` or connection refused | Server unreachable | Check URL, DNS, firewall rules, and that Dokploy is running |
| `502` / `503` | Server is starting or overloaded | Wait 30 seconds and retry |

### Additional API verification (optional)

To confirm full read/write access, call a non-destructive endpoint:

```bash
curl -s "$DOKPLOY_URL/api/project.all" \
  -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json"
```

This should return the same project list as the MCP call in Step 1.

---

## Verification Summary

After completing all three steps, produce a summary table:

| Check | Status | Details |
|---|---|---|
| MCP Connection | PASS/FAIL | N projects found / error message |
| CLI Installation | PASS/FAIL | Version / not installed |
| API Access | PASS/FAIL | HTTP 200 / status code |

If all three pass, report: "Dokploy setup is complete. All access methods are working."

If any step fails, provide the specific fix instructions from the relevant section above.

---

## Common Issues

| Problem | Symptoms | Solution |
|---|---|---|
| MCP not connecting | Tool calls return "server not found" or timeout | Verify `.mcp.json` exists, `npx @dokploy/mcp` works, and env vars are set |
| MCP returns "Invalid URL" | `DOKPLOY_URL` empty/wrong **in the running server process** | Set `DOKPLOY_URL` (base URL, no `/api`, no trailing slash), then **restart Claude Code or `/mcp` → reconnect `dokploy`** — a stdio MCP server reads env once at spawn and won't pick up edits to `settings.local.json`/`.env` until reconnected |
| MCP returns 401 "Authentication failed" | `DOKPLOY_API_KEY` invalid/stale in the running process | Fix the token, then reconnect the server (as above). Confirm `settings.local.json` and `.env` hold the **same** key |
| CLI auth fails | `dokploy auth` fails (401 / invalid) | Check the base URL has no `/api` suffix; regenerate the token. Env vars `DOKPLOY_URL`/`DOKPLOY_API_KEY` override `config.json` — make sure they're not stale |
| API 401 Unauthorized | `curl` returns 401 | Token expired or invalid — regenerate in dashboard |
| API connection refused | `curl` returns 000 or "connection refused" | Wrong URL, server down, or firewall blocking the port |
| Self-signed cert errors | `UNABLE_TO_VERIFY_LEAF_SIGNATURE` | Set `NODE_TLS_REJECT_UNAUTHORIZED=0` for dev environments |
| MCP tools exist but return errors | Tool calls return API errors | `dokploy_url` is the **base URL without `/api`** for MCP, REST, and CLI. MCP server and REST endpoints live at `/api/…` under that base |
| Wrong port | Connection refused on default port | Dokploy defaults to port 3000; verify the actual port in your deployment |

---

## What This Skill Does NOT Cover

- **Application deployment workflows** — See the `mcp-patterns` skill for MCP tool sequences to deploy apps, provision databases, and manage domains.
- **API endpoint details** — See the `api-reference` skill for the REST API surface (604 endpoints across 57 routers, Dokploy v0.30.7) with parameters and response schemas.
- **Reading logs / debugging deploys** — See the `read-logs` and `debug-deploy` skills (and `/dokploy-dev:logs`, `/dokploy-dev:compose-logs`, `/dokploy-dev:debug`).
- **CLI command recipes** — See the `cli-recipes` skill for common CLI workflows like deploying from a local directory, managing Docker Compose stacks, and backup operations.
- **Troubleshooting deployment issues** — See the `troubleshoot` skill for diagnosing failed deployments, container crashes, and Traefik routing problems.