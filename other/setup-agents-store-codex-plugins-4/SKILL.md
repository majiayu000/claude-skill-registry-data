---
name: setup
description: |
  Verify NocoDB connection and MCP setup. Use when:
  - "check my NocoDB connection"
  - "verify MCP is working"
  - "test NocoDB setup"
  - "is NocoDB connected?"
  - "troubleshoot NocoDB access"
---

# NocoDB Setup Verification

`nocodb-ops` works through the NocoDB **MCP server**. The optional REST variables (`NOCODB_URL`, `NOCODB_TOKEN`) are only for the `curl` recipes in **cli-reference**.

## Prerequisites

Before running verification, confirm these environment variables are set:

| Variable | Required | Description |
|----------|----------|-------------|
| `NOCODB_MCP_URL` | Yes (MCP) | Full MCP endpoint URL. NocoDB Cloud and licensed self-hosted: `https://<host>/mcp` (Cloud: `https://app.nocodb.com/mcp`). Community Edition: the per-endpoint URL `https://<host>/mcp/<ncId>` shown in the base's MCP settings. |
| `NOCODB_MCP_TOKEN` | Yes (MCP) | MCP token, sent as the `xc-mcp-token` header (still accepted; NocoDB's newer primary header is `x-api-key`). Create it where the MCP connection is created -- see "MCP connection options". |
| `NOCODB_URL` | No (REST) | Base instance URL without a trailing slash, e.g. `https://<host>` (`https://app.nocodb.com` on NocoDB Cloud). Used by the `curl` recipes. |
| `NOCODB_TOKEN` | No (REST) | NocoDB API token, sent as the `xc-token` header. Create it under **Team & Settings → API Tokens → Add New Token**. |
| `NOCODB_VERBOSE` | No | Set to `1` to print resolved IDs from the optional official `nocodb.sh` script. |

Legacy alias: `NOCODB_API_TOKEN` is the former name of `NOCODB_TOKEN`. Wrappers may keep reading it as an alias (`export NOCODB_TOKEN="${NOCODB_TOKEN:-$NOCODB_API_TOKEN}"`); the official `nocodb.sh` reads only `NOCODB_TOKEN`, and every recipe in this plugin uses `NOCODB_TOKEN`.

The MCP token and the API token are **distinct** and are created in different places. Do not reuse one variable for both transports (see `LEARNINGS.md`, 2026-05-06).

The plugin's `.mcp.json` uses `${NOCODB_MCP_URL}` and `${NOCODB_MCP_TOKEN}` (via the `xc-mcp-token` header) to configure the `nocodb` HTTP MCP server.

### MCP connection options

| Option | How |
|--------|-----|
| MCP token | Cloud / licensed: Account Settings → **MCP** tab → New connection (choose Access and Tools & Permissions). Community Edition: Overview → Settings → Model Context Protocol → New MCP Endpoint. Put the token in `NOCODB_MCP_TOKEN`. |
| OAuth | Cloud: connect to `https://app.nocodb.com/mcp` without a token. Self-hosted: `https://<host>/mcp`. |

Also confirm:
1. **MCP server connected** -- the plugin's `nocodb` server is active and its tools appear as `mcp__plugin_nocodb-ops_nocodb__<tool>`
2. **Base accessible** -- at least one NocoDB base is shared with the connection's user

## Verification Steps

Run these checks in order. Stop at the first failure and check the troubleshooting table below.

### Step 1 -- Who am I? (`whoami`)

Call `mcp__plugin_nocodb-ops_nocodb__whoami` with no parameters (Cloud / licensed servers).

- **Pass:** names the user the connection acts as, the base it is pinned to, and the permissions granted -- "what you can do". Effective authority is the intersection of that grant and the user's role on each resource.
- **Tool missing or an error:** the server may be Community Edition or an older release without `whoami`; go to Step 2.

### Step 2 -- Test connection

Call `mcp__plugin_nocodb-ops_nocodb__getTablesList` with no parameters.

- **Pass:** Returns a list of table names and IDs.
- **Fail:** Connection error or authentication error. See troubleshooting.

### Step 3 -- Verify read access

Pick any table ID from Step 2. Call `mcp__plugin_nocodb-ops_nocodb__queryRecords` with that `tableId` and `pageSize: 1`.

- **Pass:** Returns one record (or an empty list if the table has no data).
- **Fail:** Permission error or invalid table ID.

### Step 4 -- Verify count access

Call `mcp__plugin_nocodb-ops_nocodb__countRecords` with the same `tableId`.

- **Pass:** Returns a number (even zero is fine).
- **Fail:** Aggregation permissions may be restricted.

### Step 5 -- Verify base info

Call `mcp__plugin_nocodb-ops_nocodb__getBaseInfo` with no parameters.

- **Pass:** Returns base name, ID, and metadata.
- **Fail:** The connection may lack base-level access.

### Step 6 -- Which edition? (`listTools`)

```
mcp__plugin_nocodb-ops_nocodb__listTools  category: "records"
```

- **Cloud / licensed:** the answer names `upsertRecords`, `updateRecordsByCondition` and `linkRecordsByDisplayValue` -- the extra record tools are available through `callTool` (see **mcp-patterns**).
- **Community Edition:** `listTools` is absent or errors. The server offers the original record tools only; everything in this plugin still works, with batches of up to 100 records via `createRecords` / `updateRecords`.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Protected resource does not match" | `NOCODB_MCP_URL` does not match the endpoint the server expects | Cloud / licensed: `https://<host>/mcp`. Community Edition: use the full `/mcp/<ncId>` URL from the base's MCP settings |
| Connection refused | Server down or wrong URL | Check `NOCODB_MCP_URL`, then `curl -sSI "$NOCODB_URL"` to confirm the host answers; restart the session |
| 401 Unauthorized | `NOCODB_MCP_TOKEN` is wrong, **revoked**, or the connection was restricted (its Tools & Permissions allowlist) | Recreate or re-open the connection where it was created (see "MCP connection options") and update `NOCODB_MCP_TOKEN` |
| 403 Forbidden | The connection's user lacks permission for this base | Share the base with the user, or use a connection with a higher role |
| Timeout | Network issue or server overloaded | Check server status, try again |
| Empty table list | No tables in the base, or wrong base | Ask `whoami` which base the connection is pinned to |
| "Tool not found" for `mcp__plugin_nocodb-ops_nocodb__<tool>` | The plugin's MCP server did not start (missing `NOCODB_MCP_URL` / `NOCODB_MCP_TOKEN`), or the tool is a hidden one | Confirm both variables are set in the shell that launched Claude Code, then restart the session. For `upsertRecords`, `importCsv`, `listTrash` and the like call `listTools(category)` then `callTool` |
| `listTools` missing | Community Edition (record tools only) | Use the listed record tools; hidden tools do not exist on this edition |

## What This Skill Does NOT Cover

- **Installing or configuring the MCP server** -- that is an admin task handled during provisioning.
- **Creating tokens** -- the MCP token is created with the MCP connection (Account Settings → MCP tab on Cloud / licensed; the base's MCP settings on Community Edition); the API token under Team & Settings → API Tokens.
- **Database or base creation** -- create bases through the NocoDB web interface first.

## After Verification

Once all steps pass, you are ready to:

- Browse tables and schemas with the **mcp-patterns** skill
- Create, read, update, and delete records with the **record-management** skill
- Build filtered views and reports with other plugin skills