---
name: setup
description: |
  Verify NocoDB connection for schema-development work — MCP and REST (curl on Meta API v3). Use when:
  - "check NocoDB dev setup"
  - "verify NocoDB API access"
  - "is my NocoDB token working?"
  - "can I modify schema?"
  - "test NocoDB MCP connection"
---

# NocoDB Dev Setup Verification

`nocodb-dev` uses two NocoDB surfaces:

- **MCP** — discovery on every edition; on Cloud / licensed self-hosted also schema writes through `listTools(category)` → `callTool` (Community Edition has record tools only). Authenticated by an MCP token or OAuth.
- **REST (Meta API v3, `curl`)** — every schema write on Community Edition, and the fallback everywhere else. Authenticated by an API token.

Both should work before you plan and apply schema changes.

## Required Environment Variables

| Variable | Required | Surface | Description |
|----------|----------|---------|-------------|
| `NOCODB_MCP_URL` | Yes (MCP) | MCP | Full MCP endpoint URL. Cloud/licensed: `https://<host>/mcp`. Community Edition: the per-endpoint URL `https://<host>/mcp/<ncId>` from the base's MCP settings. |
| `NOCODB_MCP_TOKEN` | Yes (MCP) | MCP | MCP token, sent as the `xc-mcp-token` header (still accepted; `x-api-key` is the newer primary header). |
| `NOCODB_URL` | Yes (REST) | REST | Base instance URL without a trailing slash, e.g. `https://<host>` (`https://app.nocodb.com` on NocoDB Cloud). |
| `NOCODB_TOKEN` | Yes (REST) | REST | API token — NocoDB → Team & Settings → API Tokens → Add New Token. Sent as the `xc-token` header. |
| `NOCODB_VERBOSE` | No | official CLI script | Set to `1` to print resolved IDs from the optional `nocodb.sh` script. |

Legacy alias: `NOCODB_API_TOKEN` is the former name of `NOCODB_TOKEN`. Wrappers may keep reading it as an alias (`export NOCODB_TOKEN="${NOCODB_TOKEN:-$NOCODB_API_TOKEN}"`); the official `nocodb.sh` reads only `NOCODB_TOKEN`, and every recipe in this plugin uses `NOCODB_TOKEN`.

The two tokens are **distinct**. Sharing one variable across both transports is the regression captured in `LEARNINGS.md` of the `nocodb-ops` plugin (2026-05-06).

### MCP connection options

| Option | How |
|--------|-----|
| MCP token | Cloud / licensed: Account Settings → **MCP** tab → New connection (choose Access and Tools & Permissions). Community Edition: Overview → Settings → Model Context Protocol → New MCP Endpoint. Put the token in `NOCODB_MCP_TOKEN` (header `xc-mcp-token`; `x-api-key` also works). |
| OAuth | Cloud: connect to `https://app.nocodb.com/mcp` without a token. Self-hosted: `https://<host>/mcp`. |

## Verification Steps

Run in order. Stop at the first failure and consult the troubleshooting table.

### Step 1 — MCP discovery

Call `mcp__plugin_nocodb-dev_nocodb__getTablesList` with no parameters.

- **Pass:** returns a list of table names and IDs.
- **Fail:** see Troubleshooting → MCP rows.

### Step 2 — MCP schema read

Pick any table ID from Step 1. Call `mcp__plugin_nocodb-dev_nocodb__getTableSchema` with `tableId` (or `getBaseSchema` for every table at once).

- **Pass:** returns fields + views.
- **Fail:** the token may lack base-level access.

### Step 3 — Which edition? (`listTools`)

```
mcp__plugin_nocodb-dev_nocodb__listTools  category: "tables"
```

- **Pass (Cloud / licensed):** the answer names `createTable`, `updateTable`, `deleteTable`. Use **MCP-first** for schema writes (see **mcp-patterns**).
- **Community Edition:** `listTools` is absent or empty for `tables`. Schema writes use REST (Steps 4-5).

### Step 4 — REST: list workspaces and the base's tables

```bash
curl -sS -H "xc-token: ${NOCODB_TOKEN}" "${NOCODB_URL}/api/v3/meta/workspaces" | jq
```

- **Pass:** returns a list of workspaces (listing is open on all plans).
- **Fail:** see Troubleshooting → REST rows.

Using a base ID (prefix `p`, from the MCP `getBaseInfo` answer or the NocoDB UI URL):

```bash
curl -sS -H "xc-token: ${NOCODB_TOKEN}" "${NOCODB_URL}/api/v3/meta/bases/<baseId>/tables" | jq
```

- **Pass:** returns table IDs (prefix `m`).
- **Fail:** the API token may not be shared with that base.

### Step 5 — Optional data ping

```bash
curl -sS -H "xc-token: ${NOCODB_TOKEN}" "${NOCODB_URL}/api/v3/data/<baseId>/<tableId>/count" | jq
```

- **Pass:** returns `{ "count": <number> }`.
- **Fail:** likely an auth or path issue — confirm the token has read access to the base.

## Troubleshooting

| Symptom | Surface | Likely cause | Fix |
|---------|---------|--------------|-----|
| "Protected resource does not match" | MCP | `NOCODB_MCP_URL` does not match the endpoint the server expects | Cloud/licensed: `https://<host>/mcp`. Community Edition: use the full `/mcp/<ncId>` URL from the MCP settings |
| 401 Unauthorized | MCP | `NOCODB_MCP_TOKEN` invalid/expired | Regenerate the connection token (see MCP connection options) |
| 401 Unauthorized | REST | `NOCODB_TOKEN` invalid/expired | Regenerate in NocoDB → Team & Settings → API Tokens |
| 403 Forbidden | Either | Token lacks permission for the base | Share the base with the token's user, or use a higher-privilege token |
| `NOCODB_TOKEN` empty in curl (`401`, `xc-token:` header blank) | REST | Variable not exported into the shell | `export NOCODB_TOKEN=…`; check with `[ -n "$NOCODB_TOKEN" ] && echo set` |
| "Tool not found" for `mcp__plugin_nocodb-dev_nocodb__<tool>` | MCP | The plugin's MCP server did not start (missing `NOCODB_MCP_URL` / `NOCODB_MCP_TOKEN`), or the tool is a hidden schema tool | Confirm both variables are set and restart the session; for schema tools call `listTools(category)` then `callTool` |
| `listTools` missing, or `createTable` not in its answer | MCP | Community Edition (record tools only) | Use the REST recipes in **api-reference** |
| Connection refused | Either | Server down or wrong host | `curl -sSI "$NOCODB_URL"` to confirm reachability |
| Empty table list | REST | Token has no shared bases | Have an admin share at least one base with the token's user |

## Optional: the Official CLI Script

NocoDB publishes a Bash wrapper (`nocodb.sh`, needs `curl` + `jq`) as an agent skill: `npx skills add nocodb/agent-skills`. It reads `NOCODB_TOKEN`, `NOCODB_URL` and `NOCODB_VERBOSE`. The script lives at `scripts/nocodb.sh` inside the installed skill directory — that skill's README gives the exact path. It is **not** bundled in this plugin; every recipe here is plain `curl`. There is no standalone `nc` binary — `nc` is the netcat utility and must not be used.

## What This Skill Does NOT Cover

- Provisioning a NocoDB instance (admin task).
- Generating tokens (done in the NocoDB UI).
- Selecting which base / source to operate on (use the **table-management** skill).
- Schema modification itself (use **table-management**, **field-management**, **view-management**, **webhooks**).

## After Verification

Once all steps pass:

1. Read **mcp-patterns** for the Community vs Cloud/licensed contract and the `listTools` → `callTool` flow.
2. Read **api-reference** when you need the REST API surface.
3. Read **cli-reference** for `curl` recipes by resource and the optional official script.
4. Use **table-management**, **field-management**, **view-management**, **webhooks** to make changes.