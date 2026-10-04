---
name: moonpay-mcp
description: Set up MoonPay as an MCP server for Claude Desktop or Claude Code. Provides all MoonPay CLI tools via the Model Context Protocol.
tags: [setup]
---

# MoonPay MCP Setup

## Goal

Configure the MoonPay CLI as an MCP server so Claude Desktop, Claude Code, or any MCP-compatible client can use all MoonPay tools directly.

## Prerequisites

```bash
npm i -g @moonpay/cli
mp login --email user@example.com
mp verify --email user@example.com --code <code>
```

## Claude Code setup

```bash
claude mcp add moonpay -- mp mcp
```

## Claude Desktop setup

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "moonpay": {
      "command": "mp",
      "args": ["mcp"]
    }
  }
}
```

Then restart Claude Desktop.

## What it provides

All MoonPay CLI tools are available as MCP tools:

- **Wallet management** — create, import, list, retrieve, delete, export wallets
- **Token operations** — search, retrieve, trending, swap, bridge, transfer
- **Fiat** — buy crypto with card/bank, virtual accounts with on-ramp
- **x402 payments** — paid API requests with automatic payment handling
- **Transactions** — sign locally, send, list, retrieve

## Verification

After setup, ask Claude: "What MoonPay tools do you have?" — it should list all available tools.

## Auth

The MCP server uses the same credentials as the CLI (`~/.config/moonpay/credentials.json`). Run `mp login --email <email>` then `mp verify --email <email> --code <code>` to authenticate.

## PayBox MCP (separate product)

Agent credential vault with OAuth 2.1:

```text
https://api.paybox.sh/mcp
```

See **paybox** skill. Do not confuse with `mp mcp` (local CLI) or Cheshire `mcp-server` (Pump + REST proxies).

## Cheshire Terminal mcp-server

Monorepo `mcp-server/` also exposes MoonPay REST tools (`get_moonpay_*`) and a PayBox client proxy (`get_paybox_*` / `set_paybox_session`). Configure `MOONPAY_PUB_KEY` and optional `PAYBOX_ACCESS_TOKEN` per `mcp-server/.env.example`. Entry skill: **moonpay**.

## Related skills

- **moonpay** — Pack entry + Cheshire wiring.
- **paybox** — PayBox official MCP + proxy.
- **moonpay-auth** — Login and wallet setup.
- **moonpay-discover-tokens** — Search and analyze tokens.
- **moonpay-swap-tokens** — Swap tokens.
- **moonpay-skills-index** — Full list.
