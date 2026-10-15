---
name: aos-gateway
description: "Use the local MCP gateway and the per-app MCP picks. Use when the human asks to check, start, enable or disable the gateway, adopt other MCP servers behind it, wonder why an MCP server is direct or shared, or hit an After Effects MCP that will not start (Node >= 24)."
category: bdb-core
risk: safe
tools:
- claude-code
- opencode
---

# aos-gateway

The gateway is a local token-checking forwarder (`127.0.0.1:7790`) in front of `@1mcp/agent` (`127.0.0.1:7791`). Harness MCP files get one `aos` entry instead of many servers. Full reference (repo, not installed): https://github.com/hybridlabor-api/aos/blob/main/docs/mcp-gateway.md.

## Commands

```
aos-gateway serve | start | stop | restart | status [--json] | enable | direct | adopt [--dry-run] [--json]
```

- **Check:** `aos-gateway status` (exit 0 only when running). Upstream health is the state of 1mcp as a whole, not per server.
- **Enable:** `aos-gateway enable` points the harness MCP files at the gateway. **Direct:** `aos-gateway direct` reverses it and restores removed entries.
- **Start/stop/restart:** launchd on macOS. Windows (`schtasks`) is UNVERIFIED in the code. Elsewhere run `aos-gateway serve`.
- Config lives in `~/.agents/gateway/`. `token` must be mode 600. Never print or copy its content.

## Adopt

1. Run `aos-gateway adopt --dry-run` first and show the result.
2. Run `aos-gateway adopt` only after the human agrees. It edits harness MCP files.
3. Run `aos-gateway restart` afterwards.

Adopt skips remote (url/http/sse) entries, disabled ones, names the AOS install owns, names over 26 chars, entries with inline secrets and conflicting definitions. Secrets are never copied.

## Allow list vs direct

- Shared through the gateway: `github`, `open_design_mcp`, `bdb_resolume_mcp`, `bdb_grandma3_mcp`, `bdb_blender_mcp`, `bdb_davinci_mcp`, `adobe_uxp_mcp`, `bdb_unreal_mcp`, `bdb_after_effects_mcp`.
- Everything else stays direct (for example `deja`, `memb_mcp`, `mcsc`, `openwiki`, `bdb_td_minddesigner`, the official picks). A shipped entry with `shared: false` also stays direct.
- Do not add a server to the allow list by hand. It is defined in `lib/gateway/config.js`.

## Node for After Effects

`bdb_after_effects_mcp` needs Node >= 24. `aos-gateway serve` warns on an older Node and the AE upstream will not start. Fix the Node version, then restart the gateway.

## One MCP per app

`mcp_picks.json` keeps the first satisfied candidate per app and removes the others.

- Blender: `bdb_blender_official_mcp` when Blender >= 5.1 is found, else `bdb_blender_mcp`.
- Resolume: `bdb_resolume_official_mcp` when the Arena `mcp/resolume_arena_mcp_server` binary is found, else `bdb_resolume_mcp`.
- After Effects: `bdb_after_effects_mcp_legacy` only with `AOS_AE_MCP=legacy`, else `bdb_after_effects_mcp`.

## Limits

- The token stops browsers, not local processes.
- Do not edit `~/.agents/gateway/` files by hand. Use the commands above.
