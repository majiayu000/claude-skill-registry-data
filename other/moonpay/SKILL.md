---
name: moonpay
description: Entry-point for MoonPay CLI, PayBox agent vault, and Cheshire mcp-server MoonPay/PayBox tools. Use for fiat on-ramp, wallets, swaps, x402, PayBox MCP, or moonpay-* skill discovery.
---

# What you can build with MoonPay Skills

**Live catalog:** https://cheshireterminal.ai/skills/moonpay  
**API:** https://cheshireterminal.ai/api/skills/moonpay · raw `SKILL.md` at `/api/skills/moonpay/SKILL.md`

Upstream: [moonpay/skills](https://github.com/moonpay/skills) · agent integrations: https://agents.moonpay.com

## Overview

MoonPay Skills are modular capabilities you add to your AI agent via the command line or a plugin marketplace. Each skill maps to a specific onchain action — from swapping tokens to funding prediction markets to accepting crypto payments. Mix and match skills to automate complex workflows without writing infrastructure from scratch.

> **Note:** You don't need to install every skill. Each skill works independently — install only what your workflow needs and add more as you go.

> **Tip:** New to MoonPay CLI? Get set up first with [MoonPay CLI for AI agents](https://support.moonpay.com/en/articles/586583-moonpay-cli-for-ai-agents) before installing skills. In this hub, start with `moonpay-auth`.

## Key benefits

- **Broad agent compatibility** — works with Claude Code, Cursor, Windsurf, Codex, and 40+ other agents
- **Composable by design** — combine skills into multi-step pipelines for research, trading, safety checks, and more
- **One-line install** — add any skill in seconds with `npx skills add`

## Install

### Install all skills

```bash
npx skills add moonpay/skills
```

### Install a specific skill

```bash
npx skills add moonpay/skills --skill moonpay-swap-tokens
```

### Install globally across all projects

```bash
npx skills add moonpay/skills --global
```

> **Note:** Global installation (`--global`) makes skills available across all your projects. Omit the flag to install skills for the current project only.

### Install via Claude Code plugin marketplace

```
/plugin marketplace add moonpay/skills
/plugin install moonpay-skills
```

> **Note:** Full source and documentation are available on [GitHub](https://github.com/moonpay/skills). To explore agent-specific integrations, visit https://agents.moonpay.com.

### Cheshire hub install

This monorepo already vendors the pack under `skills/` (and `.agents/skills/`). Rebuild the public catalog with:

```bash
node skills/scripts/build-catalog.mjs
```

Browse: https://cheshireterminal.ai/skills/moonpay

## Load order (Cheshire)

1. **Auth first:** `moonpay-auth` — install `@moonpay/cli` (`mp`), login/verify, local wallets.
2. **MCP planes:**
   - **MoonPay CLI MCP:** `mp mcp` (see `moonpay-mcp`)
   - **PayBox official MCP:** `https://api.paybox.sh/mcp` (OAuth 2.1 + PKCE; see `paybox`)
   - **Cheshire mcp-server proxy:** monorepo `mcp-server/` tools `get_moonpay_*` + `get_paybox_*`
3. Load a focused skill from `moonpay-skills-index` for the task.

## Trade and automate

| What you want | Skills to use |
| --- | --- |
| Swap tokens on Solana, Ethereum, Base, or Polygon | `moonpay-swap-tokens` |
| Buy crypto with a credit card or bank transfer | `moonpay-buy-crypto` |
| DCA into any token on a recurring schedule | `moonpay-trading-automation` |
| Full fiat → DCA loop via virtual account | `moonpay-virtual-account` + `moonpay-trading-automation` |
| Get notified when a token hits your price | `moonpay-price-alerts` |
| Check and track your portfolio | `moonpay-check-wallet` |
| Export trade history for tax or reporting | `moonpay-export-data` |

## Trade prediction markets

> **Note:** Polymarket settles on Polygon (USDC.e), Kalshi on Solana, and Myriad on BNB Chain (USDT/USD1). Make sure your wallet is funded on the correct chain before trading.

| What you want | Skills to use |
| --- | --- |
| Trade on Polymarket or Kalshi | `moonpay-prediction-market` |
| Fund a Polymarket wallet (USDC.e + POL) | `moonpay-fund-polymarket` |
| Find arbitrage across Polymarket and Kalshi | `moonpay-scout` |
| Trade prediction markets on BNB Chain | `myriad-prediction-markets` |
| Use real-time sports data as trading signals | `shipp-sports-data` + `moonpay-prediction-market` |

## Research before you buy

| What you want | Skills to use |
| --- | --- |
| Research any token (fundamentals, price, sentiment, news) | `messari-token-research` |
| Surface trending narratives and momentum assets | `messari-alpha-scout` |
| Track VC funding rounds and M&A activity | `messari-funding-intel` |
| Generate a long-form research report on any topic | `messari-deep-research` |
| Search trending tokens and check risk | `moonpay-discover-tokens` |
| Query live on-chain data (wallet activity, DEX volume) | `dune-analytics` |
| Get token prices, balances, and transactions | `allium-onchain-data` |

## Stay safe

> **Note:** If you're new to on-chain trading, we recommend running `maiat-token-safety` before any swap. It takes seconds and catches the most common token risks automatically.

| What you want | Skills to use |
| --- | --- |
| Check a token for honeypots, rug pulls, and high-tax traps | `maiat-token-safety` |
| Verify an agent's trust score before transacting | `maiat-trust-check` |
| Get adversarial verification on any trade decision | `thoughtproof-reasoning-check` |

## Pay for things

| What you want | Skills to use |
| --- | --- |
| Make micropayments to x402-protected APIs | `moonpay-x402` |
| Browse and pay for hundreds of premium APIs without API keys | `corbits-marketplace` |
| Accept crypto deposits from any chain (auto-converts to stablecoin) | `moonpay-deposit` |
| On-ramp fiat to stablecoin (and off-ramp back) | `moonpay-virtual-account` |

## Build products

| What you want | Skills to use |
| --- | --- |
| Add crypto checkout to any Shopify store | `moonpay-commerce` |
| Sign transactions with a Ledger hardware wallet | `moonpay-hardware-wallet` |
| Expose all MoonPay tools as an MCP server | `moonpay-mcp` |

> **Tip:** Want to see these skills combined into a real workflow? See [Use case: The autonomous trader](https://support.moonpay.com/en/articles/629134-use-case-the-autonomous-trader) or [Use case: Research-to-trade pipeline](https://support.moonpay.com/en/articles/629133-use-case-research-to-trade-pipeline) for end-to-end examples.

## Skill combinations that work well together

These multi-skill pipelines cover common end-to-end workflows.

> **Important:** Multi-skill pipelines that include `moonpay-swap-tokens` or `moonpay-trading-automation` execute real transactions. Review each proposed trade before confirming execution.

| Workflow | Skills |
| --- | --- |
| Morning research brief → trade | `messari-alpha-scout` + `messari-token-research` + `maiat-token-safety` + `moonpay-swap-tokens` |
| Sports game → prediction market position | `shipp-sports-data` + `moonpay-prediction-market` + `moonpay-scout` |
| Fiat in → DCA on autopilot | `moonpay-virtual-account` + `moonpay-trading-automation` + `moonpay-price-alerts` |
| Find, verify, buy memecoin | `moonpay-discover-tokens` + `maiat-token-safety` + `thoughtproof-reasoning-check` + `moonpay-swap-tokens` |
| Cross-chain arb scanner | `moonpay-scout` + `moonpay-fund-polymarket` + `myriad-prediction-markets` |
| Full portfolio dashboard | `moonpay-check-wallet` + `dune-analytics` + `allium-onchain-data` + `moonpay-export-data` |

## Cheshire Terminal mcp-server integration

The package `@pump-fun/mcp-server` (repo `mcp-server/`) exposes:

| Tool family | Purpose | Auth |
|-------------|---------|------|
| `get_moonpay_status` / `get_moonpay_currencies` / `get_moonpay_buy_quote` / `get_moonpay_buy_url` | MoonPay REST catalog + buy widget URLs | `MOONPAY_PUB_KEY` (optional `MOONPAY_SECRET_KEY` to sign URLs) |
| `get_moonpay_cli_connect` | How to run `mp mcp` | none |
| `get_paybox_connect` / `set_paybox_session` / `clear_paybox_session` | PayBox session proxy | OAuth bearer |
| `get_paybox_health` / `get_paybox_oauth_metadata` | Public PayBox API health + discovery | none |
| `list_paybox_mcp_tools` / `call_paybox_mcp_tool` | Proxy official PayBox tools | session / `PAYBOX_ACCESS_TOKEN` |

Env (see `mcp-server/.env.example`):

```bash
MOONPAY_PUB_KEY=pk_test_...   # or pk_live_...
# MOONPAY_SECRET_KEY=sk_...   # optional HMAC for buy.moonpay.com
# PAYBOX_ACCESS_TOKEN=...     # optional; prefer set_paybox_session after OAuth
```

## Non-negotiable rules

- Never print, export, or log wallet private keys, seed phrases, or PayBox client secrets.
- `mp wallet export` is interactive-only — agents must not attempt secret extraction.
- Fiat checkout and card payments complete in the user's browser / passkey flow — do not claim funds moved until the user confirms or on-chain verification succeeds.
- Mutating PayBox tools require explicit user intent and `confirm=true` on the Cheshire proxy.
- Prefer **PayBox** for agent-scoped vault/signing; prefer **MoonPay CLI** for local non-custodial wallets; prefer **mcp-server REST tools** for quotes/widget links without a full CLI session.

## Related skills

- `moonpay-skills-index` — full skill list
- `moonpay-auth`, `moonpay-mcp`, `moonpay-buy-crypto`, `moonpay-swap-tokens`, `moonpay-x402`
- `paybox` — PayBox connector and Cheshire proxy
