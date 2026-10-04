---
name: solana-clawd
description: 'One-shot setup and operation guide for the solana-clawd agentic engine. Use when: cloning the repo, setting up MCP tools, starting the Telegram bot, deploying to Fly.io/Netlify, hatching blockchain buddies, running OODA loops, configuring voice mode (ElevenLabs + Grok), minting Metaplex agents, managing the vault, running the worker swarm, or contributing to the project. Covers all 31 MCP tools, 18 buddy species, 9 spinners, 60+ Telegram commands, 95 skills, and the full repo structure.'
metadata:
  {
    "solanaos": {
      "emoji": "\U0001F43E",
      "requires": {
        "env": ["HELIUS_API_KEY"],
        "bins": ["node", "npm"]
      }
    }
  }
---

# solana-clawd — The Agentic Engine Solana Deserves

**Repo**: [github.com/x402agent/solana-clawd](https://github.com/x402agent/solana-clawd)
**Live**: [solanaclawd.com](https://solanaclawd.com)
**npm**: `solana-clawd` (v1.6.0)
**Token**: `$CLAWD` — `8cHzQHUS2s2h8TzCmfqPKYiM4dSt4roa3n7MyRLApump`

## When to Use

- Setting up solana-clawd from scratch (clone, install, configure)
- Connecting MCP tools to Claude Desktop, Cursor, VS Code
- Starting the Telegram trading bot
- Deploying the web app or MCP server
- Hatching blockchain buddies or running spinners
- Running OODA trading loops
- Running Phoenix perpetuals through the official Solana CLAWD perps agent and bundled Vulcan skills
- Configuring voice mode (ElevenLabs + Grok)
- Minting agents on Metaplex
- Managing encrypted vault secrets
- Contributing new tools, buddies, or skills

## One-Shot Install

```bash
git clone https://github.com/x402agent/solana-clawd
cd solana-clawd
npm run setup
```

`npm run setup` is the canonical bootstrap. It installs dependencies, builds the root runtime, builds `MCP/`, builds `packages/agentwallet/`, builds the main web app, builds the Clawd Vault web app, builds the wiki app, syncs the skills catalog, and creates `.env` from `.env.example` if needed.

Minimum keys needed for live Solana data: `HELIUS_API_KEY` (free at helius.dev).

### Quick Demo (no keys needed)

```bash
npm run demo
npm run birth
npm run spinners
```

### Install As A Standalone Skill

Install only the master `solana-clawd` skill:

```bash
npx skills add x402agent/solana-clawd --path skill/solana-clawd
```

Install the full Solana-clawd skill pack from this repo:

```bash
npx skills add x402agent/solana-clawd
```

## MCP Setup

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "solana-clawd": {
      "command": "node",
      "args": ["/path/to/solana-clawd/MCP/dist/index.js"],
      "env": { "HELIUS_API_KEY": "your-key" }
    }
  }
}
```

### Cursor / VS Code

```json
{
  "solana-clawd": {
    "command": "node",
    "args": ["MCP/dist/index.js"],
    "cwd": "/path/to/solana-clawd"
  }
}
```

### Public HTTP (no install)

```json
{
  "solana-clawd": { "type": "http", "url": "https://solana-clawd.fly.dev/mcp" }
}
```

## MCP Tools (31)

| Category | Tools | Description |
|----------|-------|-------------|
| **Market Data** (8) | `solana_price`, `solana_trending`, `solana_token_info`, `solana_wallet_pnl`, `solana_search`, `solana_top_traders`, `solana_wallet_tokens`, `sol_price` | Live prices, trending, security scores, smart money, PnL |
| **Helius Onchain** (8) | `helius_account_info`, `helius_balance`, `helius_transactions`, `helius_priority_fee`, `helius_das_asset`, `helius_webhook_create`, `helius_webhook_list`, `helius_listener_setup` | RPC, DAS metadata, enhanced txs, webhooks, WebSocket |
| **Agent Fleet** (3) | `agent_spawn`, `agent_list`, `agent_stop` | Spawn research/OODA/scanner/dream agents |
| **Memory** (2) | `memory_recall`, `memory_write` | KNOWN/LEARNED/INFERRED 3-tier memory |
| **Metaplex** (6) | `metaplex_mint_agent`, `metaplex_register_identity`, `metaplex_read_agent`, `metaplex_delegate_execution`, `metaplex_verify_mint`, `metaplex_agent_wallet` | Mint AI agents as MPL Core assets |
| **Pump.fun** (8) | `pump_token_scan`, `pump_buy_quote`, `pump_sell_quote`, `pump_graduation`, `pump_market_cap`, `pump_top_tokens`, `pump_new_tokens`, `pump_cashback_info` | Bonding curve scanner, quotes, graduation |
| **Skills** (2) | `skill_list`, `skill_read` | Browse and load 95 SKILL.md files |

## Phoenix Perps: Vulcan / Rise SDK

The repo includes the full Vulcan skill pack under `vulcan-cli-master/skills` and exposes forwarding skills under `skills/vulcan-*`.

Use this loading order for Phoenix perps work:

1. `skills/vulcan/SKILL.md`
2. `vulcan-cli-master/CONTEXT.md`
3. `vulcan-cli-master/skills/INDEX.md`
4. Focused skills such as `vulcan-market-intel`, `vulcan-risk-management`, `vulcan-trade-execution`, `vulcan-twap-execution`, `vulcan-grid-trading`, or `vulcan-ta-strategy`

Official Python perps agent:

```bash
cd solana-python-agent
python perps_agent.py health
python perps_agent.py market SOL
python perps_agent.py paper-order buy SOL --notional-usdc 100
python perps_agent.py preflight
```

Safety contract:

- Paper mode is default.
- Live orders require explicit `--yes`.
- Live strategies require preflight and explicit mode selection.
- The agent never reads or prints private keys, wallet passwords, or MCP config secrets.

## Telegram Bot

```bash
# Set minimum env vars
export TELEGRAM_BOT_TOKEN=<from-botfather>
export HELIUS_API_KEY=<from-helius.dev>
export TELEGRAM_ALLOWED_CHATS=<your-chat-id>  # lock to your user

# Start
npx tsx src/telegram/index.ts
```

### Key Commands

| Category | Commands |
|----------|----------|
| **Market** | `/sol`, `/price <mint>`, `/trending`, `/token <mint>`, `/wallet <addr>`, `/market`, `/latest`, `/graduated` |
| **Research** | `/research <mint>`, `/deepresearch <mint>`, `/ooda`, `/chart <mint>`, `/trades <mint>`, `/toptraders <mint>`, `/holders <mint>` |
| **Pump.fun** | `/scan`, `/snipe`, `/stop`, `/signal`, `/grad <mint>`, `/mcap <mint>`, `/cashback <mint>` |
| **Helius** | `/balance`, `/tokens`, `/txs`, `/slot`, `/assets` |
| **AI** | `/grok <q>`, `/xsearch <q>`, `/wsearch <q>`, `/imagine <prompt>`, `/video <prompt>`, `/vision <url>` |
| **Twitter** | `/tweet <text>`, `/reply <id> <text>`, `/like <id>`, `/rt <id>`, `/tsearch <q>`, `/autotweet on` |
| **Vault** | `/vault`, `/vault store <label> <secret>`, `/vault get <id>`, `/vault lock` |
| **System** | `/status`, `/agentstate`, `/skills`, `/help`, `/watch <mint>` |

## Voice Mode

The web app at `solanaclawd.com/voice` supports two providers:

| | ElevenLabs | Grok (xAI) |
|---|---|---|
| **Agent** | Conversational AI (signed URL) | Realtime API (ephemeral tokens, server VAD) |
| **TTS** | Roger, Sarah, River, Will | Rex, Eve, Ara, Sal, Leo + speech tags |
| **Tools** | -- | Web search during conversation |

```bash
# Required env vars (web/.env)
ELEVEN_LABS_API_KEY=<elevenlabs-key>
ELEVENLABS_AGENT_ID=<agent-id>
XAI_API_KEY=<xai-key>
```

## Blockchain Buddies

18 species across 5 categories. 8 stats per buddy. 5 rarity tiers (common 60% to legendary 1%). Multi-frame ASCII sprites with 12 hat options.

```typescript
import { createBlockchainBuddy, formatBuddyCard } from 'solana-clawd/buddy'
const buddy = createBlockchainBuddy()
console.log(formatBuddyCard(buddy))
```

Species: SolDog, BONK Dog, dogwifhat, Jupiter Agg, Raydium LP, Whale, Bull, Bear, MEV Shark, Octopus, DeGod, y00t, Okay Bear, Pepe, Pump.fun, Sniper Bot, Validator, RPC Node.

## OODA Trading Loop

```bash
npx tsx examples/ooda-loop.ts
```

```
OBSERVE  -> sol_price, trending, helius_priority_fee, memory KNOWN
ORIENT   -> score candidates (trend + momentum + liquidity + participation - risk)
DECIDE   -> confidence >= 60? -> size band
ACT      -> trade_execute gated at `ask` permission
LEARN    -> write INFERRED -> Dream agent promotes to LEARNED
```

9 built-in agents: Explore, Scanner, PumpScanner, SniperBot, OODA, Dream, Analyst, Monitor, MetaplexAgent.

## Metaplex Agent Minting

```typescript
import { createAgentUmiFromEnv, mintClawdAgentFromTemplate } from 'solana-clawd/metaplex'
const umi = createAgentUmiFromEnv('solana-devnet')
const result = await mintClawdAgentFromTemplate(umi, 'trader', {
  uri: 'https://arweave.net/metadata.json',
  network: 'solana-devnet',
})
```

Templates: `explorer`, `scanner`, `trader`, `analyst`, `monitor`, `custom`.
Networks: solana-mainnet, solana-devnet, localnet, eclipse, sonic, fogo.

## Vault (AES-256-GCM)

```typescript
import { SolanaVault } from 'solana-clawd/vault'
const vault = await SolanaVault.create('passphrase')
await vault.store('api_key', 'sk-live-...', 'Helius key')
vault.lock()  // zero-fills key from memory
```

Auto-locks after 15 min. Scrypt-derived master key. Sentinel validation.

## Deploy

### Fly.io (MCP server)

```bash
cd MCP && fly launch --config fly.toml
fly secrets set HELIUS_API_KEY=key MCP_API_KEY=optional-bearer
```

### Netlify (web app)

```bash
netlify deploy --prod
# Set env: ELEVEN_LABS_API_KEY, ELEVENLABS_AGENT_ID, XAI_API_KEY
```

### Worker Swarm (iii SDK)

```bash
cd tailclawd/quickstart
iii -c iii-config.yaml      # start engine
docker compose up --build   # start 4 workers (TS + Rust + Python)
```

## Repo Structure

```
MCP/               31 MCP tools, STDIO + HTTP + SSE transport
src/               58 subsystems, 400+ files (engine, agents, telegram, buddy, pump, voice...)
web/               Next.js frontend (chat, buddies, voice) — solanaclawd.com
gateway/           Express API + Telegram bot + Birdeye WebSocket
packages/          agentwallet (encrypted Solana+EVM vault SDK)
beepboop/          macOS menu bar companion (SwiftUI, Claude vision, voice)
llm-wiki-tang/     Research knowledge base (Next.js + FastAPI + Supabase)
tailclawd/         TailClawd web UI + iii SDK worker swarm
elevenlabs-mcp-main/  ElevenLabs MCP server
formal_verification/  Lean 4 risk engine spec
skills/            95 SKILL.md knowledge documents
examples/          4 runnable demos (buddies, wallet listener, OODA, x402)
docs/              architecture.md (48KB), migration guide, risk engine spec
```

## Environment Variables

See `.env.example` (55 lines). Minimum:

```bash
HELIUS_API_KEY=              # Free at helius.dev (1M credits/month)
```

Full list by category:

| Category | Keys |
|----------|------|
| **Core** | `HELIUS_API_KEY`, `HELIUS_RPC_URL`, `SOLANA_TRACKER_API_KEY`, `BIRDEYE_API_KEY` |
| **LLM** | `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, `XAI_API_KEY` |
| **Voice** | `ELEVEN_LABS_API_KEY`, `ELEVENLABS_AGENT_ID` |
| **Telegram** | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_ALLOWED_CHATS`, `TELEGRAM_ADMIN_IDS` |
| **Wallet** | `SOLANA_PUBLIC_KEY`, `SOLANA_PRIVATE_KEY`, `VAULT_PASSPHRASE` |
| **Social** | `CONSUMER_KEY`, `SECRET_KEY`, `ACCESS_TOKEN`, `ACCESS_TOKEN_SECRET`, `BEARER_TOKEN` |
| **Deploy** | `MCP_API_KEY`, `CONVEX_URL`, `CONVEX_DEPLOY_KEY` |

## Pitfalls

- **No dotenv auto-load** — Telegram bot needs `source .env` or `set -a && source .env && set +a` before running
- **Helius free tier** — 1M credits/month, enough for dev but not high-frequency polling
- **Pump sniper** — Requires `SOLANA_PRIVATE_KEY` for live execution; signal-only mode works without
- **Voice mode** — Both ElevenLabs and xAI consume credits per request; monitor usage
- **Wiki sub-project** — `web/wiki/` has separate dependencies; excluded from main Next.js build via `eslint.dirs`
- **Node 20+** required — uses native WebSocket, `structuredClone`, other modern APIs
- **Bun compatible** but tested primarily on Node; `bun:bundle` feature gates exist in voice code

## Contributing

```bash
npm run build          # TypeScript compilation
npm run dev            # watch mode
npm run typecheck      # strict type checking
npm run mcp:build      # MCP server only
npm run demo           # test the demo
npm run birth          # test buddy hatching
npm run skills:catalog # regenerate skill manifest
```

High-impact areas: new MCP tools, buddy species, spinners, voice agent skills, Telegram commands. See `CONTRIBUTING.md`.
