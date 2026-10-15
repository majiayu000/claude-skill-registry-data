---
name: connect
description: Use when the user wants to connect, set up, or configure Fusionaly in their AI client, or when the fusionaly MCP tools are missing. Verifies the Fusionaly URL and agent key, then adds the MCP server to Claude Code, Codex, Cursor, Gemini CLI, or another client.
---

# Connect Fusionaly

Connect the user's Fusionaly server to their AI client, so the `fusionaly` MCP tools work. Verify first, write config second.

## 1. Collect the two values

Check what is already there, and only ask for what is missing:

- `env | grep -E '^FUSIONALY_(URL|AGENT_KEY|HOST|API_KEY)='` (`FUSIONALY_HOST` and `FUSIONALY_API_KEY` are older names for the same two values)
- the client's existing config (see step 3)

When you ask:

- **URL**: the Fusionaly address, for example `https://data.yoursite.com`. Strip a trailing slash and a trailing `/mcp`.
- **Agent key**: from **Administration > Agents** in Fusionaly. It is read-only. It is not the website id or the tracking snippet.

Never echo the key back in full. Show the last four characters at most.

## 2. Verify before writing anything

```bash
curl -sS -o /dev/null -w '%{http_code}' -X POST "<url>/mcp" \
  -H "Authorization: Bearer <key>" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

| Code | Meaning | Say this |
|------|---------|----------|
| `200` | Works | Continue to step 3. |
| `401` | Key rejected | Wrong key, or no key generated yet. Get it from Administration > Agents. |
| `404` | No MCP endpoint | The server predates v2.3.0. Run `sudo fusionaly update` on it. |
| `429` | Rate limited | Wait a minute and try again. |
| `000` | Unreachable | Check the URL, and whether the host is reachable from here. |

Do not write config for a setup that does not answer. Fix it with the user first.

## 3. Write the config for the client you run in

**The key never goes into a config file.** Config files get synced, shared, and committed; many people keep them in a dotfiles repo. Every client below reads the key from the `FUSIONALY_AGENT_KEY` environment variable instead. Only the URL, which is not a secret, goes into config.

**Where the key goes.** Before writing `FUSIONALY_AGENT_KEY=...` into any file, check that git does not track it:

```bash
f="$(readlink -f ~/.zshrc)"; git -C "$(dirname "$f")" ls-files --error-unmatch "$f" >/dev/null 2>&1 && echo tracked
```

- Not tracked: offer to add `export FUSIONALY_AGENT_KEY=...` to the user's shell profile.
- Tracked (a dotfiles repo): do not write it. Show the `export` line and tell the user to put it in an untracked file their profile sources (for example `~/.secrets`) or in their secret manager.

Keep everything else in each file. Create a config file if it does not exist.

**Claude Code** (plugin installed). The plugin's MCP config reads `${FUSIONALY_URL}` and `${FUSIONALY_AGENT_KEY}` from the environment. Add only the URL to the `env` block of `~/.claude/settings.json`, and the key as above:

```json
{ "env": { "FUSIONALY_URL": "https://data.yoursite.com" } }
```

**Codex.** Codex reads the key from the environment by design:

```bash
codex mcp add fusionaly --url https://data.yoursite.com/mcp --bearer-token-env-var FUSIONALY_AGENT_KEY
```

**Cursor.** `~/.cursor/mcp.json`, with the key read from the environment:

```json
{ "mcpServers": { "fusionaly": { "url": "https://data.yoursite.com/mcp", "headers": { "Authorization": "Bearer ${env:FUSIONALY_AGENT_KEY}" } } } }
```

**Gemini CLI.** The extension asks for both values on install and keeps the key in the system keychain. To change them later: `gemini extensions config fusionaly`.

**Another client.** Use the client's environment-variable syntax for the header if it has one. A stdio bridge reads it from the shell: `npx -y mcp-remote <url>/mcp --header "Authorization: Bearer ${FUSIONALY_AGENT_KEY}"`. If a client can only hold the key in plain text, say so, and tell the user not to commit that file.

GUI apps started from the dock do not read your shell profile. If a desktop client does not see the variable, it must be started from a terminal, or the key set in that client's own settings.

## 4. Confirm

Tell the user: connected to `<url>` and verified. Most clients read MCP config only at startup, so they must restart it. Then they can ask "How is my traffic this week?".
