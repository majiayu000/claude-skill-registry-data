---
name: xero-connect
description: "Sets up or reconnects the Xero OAuth 2.0 MCP integration. Use when connecting Xero for the first time, re-authenticating after token expiry, troubleshooting Xero MCP errors, or adding Xero to a new project. Handles app creation, credentials, MCP config, auth script, and verification."
---

# /xero-connect

Connect or reconnect the Xero accounting API via OAuth 2.0 MCP server.

## When to Use

- Setting up Xero on a new project
- Re-authenticating after token expiry or "Failed to get Xero token" errors
- Troubleshooting Xero MCP connection issues
- Migrating from Custom Connections to OAuth 2.0

## Key Constraints

- **Xero is READ ONLY** — never write to Xero under any circumstances
- Custom Connections are NOT available in Canada — must use OAuth 2.0 auth code flow
- Uses the `wspringer/xero-mcp-server` fork which supports browser-based OAuth with auto token refresh
- Tokens are stored at `~/.xero-mcp-tokens.json` (shared across all projects)
- Access tokens expire after 30 minutes; refresh tokens are single-use (each refresh returns a new one)

## Workflow

### Step 1: Detect Current State

Check what already exists:

1. Look for `xero` entry in the project's `.mcp.json`
2. Check if `xero_client_id` and `xero_client_secret` exist in Vault (via `$OUTWORKOS_ROOT/scripts/get-secret.sh`)
3. Check if `~/.xero-mcp-tokens.json` exists and contains valid tokens
4. Check if `scripts/xero-auth.sh` exists

Report findings and determine which steps to skip.

### Step 2: Xero Developer App Setup

If no credentials exist, guide the user through app creation:

1. Direct user to: https://developer.xero.com/app/manage
2. Click "New app"
3. Settings:
   - **App name**: Any name (e.g., "OutworkOS")
   - **Integration type**: Web app
   - **Company or application URL**: Any URL
   - **Redirect URI**: `http://localhost:8749/callback`
4. After creation, ask user for the **Client ID** and **Client Secret**

If credentials already exist, ask if they want to use the existing ones or enter new ones.

### Step 3: Store Credentials in Vault

Store the Xero credentials in Vault:

```bash
"$OUTWORKOS_ROOT/scripts/set-secret.sh" xero_client_id "<client-id>" "Xero OAuth client ID (READ ONLY)"
"$OUTWORKOS_ROOT/scripts/set-secret.sh" xero_client_secret "<client-secret>" "Xero OAuth client secret (READ ONLY)"
```

### Step 4: Configure .mcp.json

Add or update the `xero` entry in `.mcp.json`:

```json
"xero": {
  "command": "npx",
  "args": ["-y", "github:wspringer/xero-mcp-server"],
  "env": {
    "XERO_CLIENT_ID": "<client-id>",
    "XERO_CLIENT_SECRET": "<client-secret>",
    "XERO_USE_BROWSER_AUTH": "true"
  }
}
```

**Critical**: Must use `github:wspringer/xero-mcp-server` (NOT `@xeroapi/xero-mcp-server@latest`). The official package does not support OAuth 2.0 browser auth. The `XERO_USE_BROWSER_AUTH` env var activates the auth code flow in the fork.

### Step 5: Ensure .gitignore Protection

Before committing anything, verify `.gitignore` includes:

```
.mcp.json
```

If no `.gitignore` exists, create one. If it exists but is missing these entries, add them.

### Step 6: Deploy Auth Script

Check if `scripts/xero-auth.sh` exists in the project. If not, copy it from the template at `${CLAUDE_SKILL_DIR}/scripts/xero-auth.sh`.

The auth script:
- Reads credentials from Vault via `get-secret.sh`
- Starts a local callback server on port 8749
- Opens browser for Xero login with PKCE
- Exchanges auth code for tokens
- Saves tokens to `~/.xero-mcp-tokens.json` (mode 0600)
- Supports `--force` (re-auth) and `--check` (test only) flags

Make executable: `chmod +x scripts/xero-auth.sh`

### Step 7: Authenticate

Run the auth script:

```bash
./scripts/xero-auth.sh
```

This opens a browser. The user logs into Xero and grants access. The script captures the callback, exchanges the code for tokens, and saves them.

If re-authenticating: `./scripts/xero-auth.sh --force`

**Important**: The MCP server subprocess cannot reliably open a browser on its own. The standalone auth script handles initial authentication. After that, the MCP server uses saved tokens and refreshes them automatically.

### Step 8: Restart and Verify

1. Tell the user to restart Claude Code (so the MCP server reloads with new config)
2. After restart, use `ToolSearch` to find `xero organisation`
3. Call `mcp__xero__list-organisation-details`
4. If successful, report the org name, currency, and country

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Failed to get Xero token: [object Object]" | MCP server using Custom Connections flow (not browser auth) | Verify `.mcp.json` has `XERO_USE_BROWSER_AUTH: "true"` and uses `github:wspringer/xero-mcp-server`. Restart Claude Code. |
| "Using custom connections authentication" in logs | `XERO_USE_BROWSER_AUTH` env var not reaching the server | Check `.mcp.json` env block. The var must be inside the `env` object. |
| Token file exists but API returns 401 | Refresh token expired (unused for 60 days) | Run `./scripts/xero-auth.sh --force` |
| "No such tool: mcp__xero__*" | Xero MCP server failed to start | Check `npx -y github:wspringer/xero-mcp-server` runs manually. May need `npm cache clean --force`. |
| Port 8749 in use | Another process on the callback port | `lsof -i :8749` to identify and kill it |
| "Custom Connections not available" | Xero org is in Canada (or other unsupported region) | This is why we use OAuth 2.0 — Custom Connections only work in AU/NZ/UK/US |

## Architecture Notes

- **Token storage**: `~/.xero-mcp-tokens.json` — shared across all projects, contains access_token, refresh_token, expires_at
- **Token refresh**: The wspringer fork auto-refreshes tokens when they're within 5 minutes of expiry
- **Callback port**: 8749 (hardcoded in the fork) — must match the redirect URI in the Xero app
- **Scopes requested**: `openid profile email offline_access accounting.transactions.read accounting.contacts.read accounting.reports.read accounting.journals.read accounting.settings.read payroll.employees.read payroll.timesheets.read`
- **PKCE**: The auth flow uses S256 code challenge for security
