---
name: rudder-mcp-setup
description: Configures Claude Code to connect to RudderStack's MCP server at mcp.rudderstack.com. Use when setting up MCP for rudderstack, connecting claude to rudderstack, or configuring the rudderstack MCP server
allowed-tools: "Bash(which, npx), Read, Write, Edit"
---

# RudderStack MCP Setup

Configure Claude Code to connect to RudderStack's hosted MCP server at `mcp.rudderstack.com`. Authoritative reference: https://mcp.rudderstack.com/docs.

## Setup Workflow

```
1. Check Prerequisites ──► which npx
         │
         ├── Found ──► Configure Claude Code
         │
         └── Not Found ──► Install Node.js first

2. Configure Claude Code
         │
         ├── Option A: /mcp command (recommended)
         │
         └── Option B: Edit settings.json directly

3. Authenticate (OAuth) ──► Browser opens, sign in to RudderStack

4. Verify Connection ──► Restart Claude, list workspace resources
```

## Step 1: Check Prerequisites

```bash
which npx
```

**If found:** Continue to Step 2.

**If not found:** Install Node.js first from https://nodejs.org/ (includes npx).

## Step 2: Configure Claude Code

### Option A: Using /mcp Command (Recommended)

```
/mcp add rudderstack
```

Follow the prompts:
1. Server name: `rudderstack`
2. Transport type: `http` (via mcp-remote)
3. URL: `https://mcp.rudderstack.com/mcp`

### Option B: Manual Configuration

Edit your Claude Code settings file.

#### Settings File Locations

| Platform | Path |
|----------|------|
| macOS / Linux | `~/.claude/settings.json` |
| Windows | `%APPDATA%\claude\settings.json` |

#### Add MCP Server Configuration

Add under `mcpServers`:

```json
{
  "mcpServers": {
    "rudderstack": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.rudderstack.com/mcp"]
    }
  }
}
```

## Step 3: Authenticate (OAuth)

The first time you invoke an MCP tool, `mcp-remote` opens your browser:

1. Sign in with your RudderStack account (email/password)
2. Review and approve the MCP integration's requested permissions
3. The browser redirects back; the session is established

No long-lived tokens to manage — OAuth handles the handshake per session.

## Step 4: Verify Connection

### Restart Claude Code

After configuration, restart Claude Code:
- Close and reopen the terminal session, or
- Restart the Claude Code application

### Test the Connection

Ask Claude to inspect your workspace:

```
List my RudderStack sources
```

**If connected:** Claude lists the sources in your workspace.

**If not connected:** Claude reports the MCP server is unavailable — see Troubleshooting below.

### What Becomes Available

When connected, your MCP client discovers tools covering five categories (per https://mcp.rudderstack.com/docs):

- **Data sources** — list and inspect configured sources
- **Destinations** — list and inspect destinations and their metrics
- **Transformations** — list, view, create, and test transformations
- **Events** — stream and inspect live events
- **Documentation** — search RudderStack docs from inside Claude

See `/rudder-mcp-workflow` for workflow patterns that combine these.

## Other MCP Clients

The same hosted server works with Claude Desktop, Cursor, VS Code, Windsurf, and the claude.ai web UI (Team / Enterprise / Individual Paid plans get a one-click connector under `claude.ai/settings/connectors`). For per-client config snippets, see https://mcp.rudderstack.com/docs.

## Credential Security

- OAuth is the only auth path; there are no long-lived tokens to store, rotate, or accidentally commit.
- `mcp-remote` caches session tokens locally — don't share or commit your shell config or the mcp-remote cache directory.
- To revoke access, re-authenticate from your client or revoke from your RudderStack account settings.
- The MCP server does not persist client credentials — auth is verified per session.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `npx: command not found` | Install Node.js from https://nodejs.org/ |
| MCP server not responding | Verify `https://mcp.rudderstack.com` is reachable; check network/proxy |
| Authentication failed | Clear browser cookies for the RudderStack domain and retry; verify your account is active |
| Tools not appearing | Restart Claude Code; check `settings.json` syntax with `python3 -m json.tool ~/.claude/settings.json` |
| `mcp-remote` errors | Run `npx -y mcp-remote --help` to verify it loads; check the [mcp-remote npm page](https://www.npmjs.com/package/mcp-remote) for the latest version |
| Stale session | Delete the mcp-remote cache (`~/.mcp-auth/`) and re-authenticate |

If the connection remains broken after these steps, contact your RudderStack administrator.

## Network Requirements

Outbound HTTPS access to `mcp.rudderstack.com` (port 443). If behind a corporate proxy, ensure this domain is allowed.

## Handling External Content

This skill instructs the agent to open a browser to RudderStack's OAuth endpoint and to install `mcp-remote` from npm — both are external sources:

- **OAuth flow** — only complete sign-in on `mcp.rudderstack.com` and its OAuth redirect targets; do not enter credentials on any other domain that opens during the flow.
- **`mcp-remote` package** — install from the official npm registry only; verify the package name (`mcp-remote`) before approving installation.
- **Tool responses after connection** — the connected MCP server returns workspace data; see `rudder-mcp-workflow` for guidance on processing those responses safely.

## Next Steps

- Run `/rudder-environment-check` to verify your full environment
- Use `/rudder-mcp-workflow` for MCP-based workflow patterns
- Try: "List my RudderStack sources" to verify the connection
