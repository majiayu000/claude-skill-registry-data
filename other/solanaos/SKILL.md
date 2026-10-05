---
name: solanaos
description: >
  Complete SolanaOS agent skill — install, configure, and operate the autonomous
  Solana trading runtime with Honcho v3 epistemological memory, multi-venue perp
  trading (Hyperliquid + Aster), on-chain intelligence with USD pricing, Telegram
  bot, gateway API, Tailscale mesh, hardware integration, and cross-session recall.
  Use when asked to install SolanaOS, query Solana blockchain data, manage wallets,
  run OODA trading loops, configure strategies, control BitAxe mining fleets, pair
  Seeker devices, or operate any SolanaOS runtime surface.
license: MIT
metadata:
  solanaos:
    version: 2.0.0
    author: 8BIT Labs
    category: solana-crypto
    venues: [solana-spot, hyperliquid, aster]
    requires_bins: [go, git, curl]
    requires_env: [SOLANA_TRACKER_API_KEY, TELEGRAM_BOT_TOKEN]
---

# SolanaOS — Complete Agent Skill

> Give this file to any AI agent (Claude, Codex, GPT-4, DeepSolana, Hermes, etc.)
> to fully install, configure, and operate SolanaOS in one shot.

```text
   _____       __                        ____  _____
  / ___/____  / /___ _____  ____ _     / __ \/ ___/
  \__ \/ __ \/ / __ `/ __ \/ __ `/    / / / /\__ \
 ___/ / /_/ / / /_/ / / / / /_/ /    / /_/ /___/ /
/____/\____/_/\__,_/_/ /_/\__,_/     \____//____/
                S O L A N A O S
```

## What You Are Installing

**SolanaOS** — an autonomous Solana trading and operator runtime by 8BIT Labs.

One ~10MB Go binary (`solanaos`) that combines:

- **OODA trading loop** — RSI + EMA + ATR across Solana spot, Hyperliquid perps, Aster perps
- **Honcho v3 memory** — persistent cross-session reasoning (KNOWN/LEARNED/INFERRED)
- **On-chain intelligence** — wallets, token research, whale detection, USD pricing
- **Telegram bot** — 60+ commands + natural language trading
- **Gateway API** — memory, trading, sessions, chat on port 18790
- **Tailscale mesh** — cross-device access without port forwarding
- **Hardware** — Arduino Modulino I2C on Orin Nano, RPi, RISC-V
- **80+ skills** — auto-injected into LLM context
- **SolanaOS Hub** — [seeker.solanaos.net](https://seeker.solanaos.net)

### Links

| | |
| --- | --- |
| Repo | [github.com/x402agent/SolanaOS](https://github.com/x402agent/SolanaOS) |
| Hub | [seeker.solanaos.net](https://seeker.solanaos.net) |
| Souls | [souls.solanaos.net](https://souls.solanaos.net) |
| Docs | [go.solanaos.net](https://go.solanaos.net) |
| npm | [solanaos-cli](https://www.npmjs.com/package/solanaos-cli) |
| Launch | [solanaos.net](https://solanaos.net) |

---

## Install

```bash
git clone https://github.com/x402agent/SolanaOS solanaos
cd solanaos
```

### Minimum `.env`

```bash
SOLANA_TRACKER_API_KEY=your-key
SOLANA_TRACKER_RPC_URL=https://rpc-mainnet.solanatracker.io/?api_key=your-key
SOLANA_TRACKER_WSS_URL=wss://rpc-mainnet.solanatracker.io/?api_key=your-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_ID=123456789
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-your-key
OPENROUTER_MODEL=minimax/minimax-m2.7

# Recommended
HONCHO_ENABLED=true
HONCHO_API_KEY=hch-v3-your-key
HONCHO_SESSION_STRATEGY=per-chat
HONCHO_DIALECTIC_ENABLED=true
HELIUS_API_KEY=your-helius-key

# Optional perps
# HYPERLIQUID_PRIVATE_KEY=0x...
# ASTER_API_KEY=your-key
```

### Build & Run

```bash
make build
./build/solanaos onboard
./build/solanaos daemon
```

Or npm: `npx solanaos-cli install`

### Verify

```bash
solanaos status && solanaos solana wallet && solanaos pet
```

---

## On-Chain Intelligence

| Source | Tier | Freshness |
|--------|------|-----------|
| SolanaTracker RPC | **KNOWN** | < 60s |
| SolanaTracker Datastream | **KNOWN** | Real-time WSS |
| Helius DAS | **KNOWN** | < 60s |
| Jupiter + SolanaTracker Swap | **KNOWN** | < 30s |
| Hyperliquid / Aster | **KNOWN** | < 10s |
| Honcho conclusions | **LEARNED** | Persistent |

### Commands

```
/wallet                     SOL balance + token portfolio + USD
/trending                   Trending via SolanaTracker Datastream
/research <mint>            Deep research with risk scoring (0.0-1.0)
/buy <token> <sol>          Buy via Jupiter + SolanaTracker swap
/sell <token> <amount|%>    Sell (supports "50%", "all")
```

### Natural Language Spot Trading

```
buy 0.5 SOL worth of BONK       → executes buy
ape into WIF with 1 sol         → executes buy
sell all my BONK                 → executes sell
dump half my WIF                → executes sell 50%
yolo 2 sol into PENGU           → executes buy
snipe that new token with 0.1   → executes buy
should I buy BONK?              → NOT executed (question filtered)
research this token             → NOT executed (analysis only)
```

---

## Perpetual Trading

### Hyperliquid

```
/hl                              Account overview
/hl_positions                    Open positions + PnL
/hl_open BTC long 0.01 5x       Open position
/hl_close BTC                   Close position
long BTC on HL with 5x          Natural language
short ETH 3x                    Natural language
```

### Aster (Solana-native)

```
/aster                           Account summary
/aster_positions                 Open positions
/aster_open SOL long             Open position
/aster_close SOL                 Close position
long SOL on aster                Natural language
```

---

## Memory (Honcho v3)

Three tiers: **KNOWN** (API data, expires), **LEARNED** (trade patterns, persistent), **INFERRED** (correlations, held loosely).

```
/memory                          Status + peer card
/recall <query>                  AI-powered recall via PeerChat dialectic
/remember <fact>                 Save durable conclusion
/ask_memory <question>           Ask about yourself
/forget <query>                  Delete matching memories
/dream                           Trigger memory consolidation
/profile                         Synthesized operator profile
/card                            Peer card biographical facts
/honcho_conclusions [query]      Trading conclusions
```

### Gateway Memory API

```bash
POST /memory/recall              Natural language query
POST /memory/context             Session context for LLM injection
GET  /memory/profile/{peerID}    Operator profile
POST /memory/dream/{peerID}      Trigger consolidation
POST /chat                       Natural language gateway
```

---

## Strategy & OODA

```
OBSERVE → wallet, prices, funding, OI, holders
ORIENT  → RSI/EMA/ATR scoring, confidence model
DECIDE  → venue selection, risk caps, drawdown cascade
ACT     → Jupiter swap / HL order / Aster order
LEARN   → persist to Honcho, feed auto-optimizer
```

```
/strategy                        Show all parameters
/set rsi_period 12               Update live
/set stop_loss 5                 Persists to config
```

### Drawdown Cascade

| Drawdown | Action |
|----------|--------|
| 5% | Reduce weakest, block Pump.fun |
| 8% | Close perps, spot-only |
| 12% | Full halt |

---

## Surfaces

| Surface | How |
|---------|-----|
| Terminal | `solanaos daemon` |
| Telegram | Auto-connected, 60+ commands |
| Chrome | Load `chrome-extension/` unpacked |
| Seeker | Scan QR from `gateway setup-code` |
| Hub | [seeker.solanaos.net](https://seeker.solanaos.net) |
| Mining | [seeker.solanaos.net/mining](https://seeker.solanaos.net/mining) |
| Strategy | [seeker.solanaos.net/strategy](https://seeker.solanaos.net/strategy) |
| Skills | [seeker.solanaos.net/skills](https://seeker.solanaos.net/skills) |
| Souls | [souls.solanaos.net](https://souls.solanaos.net) |

---

## Key Files

| File | Purpose |
|------|---------|
| `main.go` | CLI entrypoint |
| `SOUL.md` | Agent identity |
| `strategy.md` | Multi-venue strategy v2.0 |
| `skill.md` | This file |
| `pkg/daemon/` | Daemon orchestrator |
| `pkg/agent/` | OODA loop + compression + routing + insights |
| `pkg/honcho/` | Honcho v3 client |
| `pkg/solana/` | SolanaTracker + Jupiter + swap |
| `pkg/hyperliquid/` | HL perps |
| `pkg/aster/` | Aster perps |
| `pkg/trading/` | Unified trading engine |
| `pkg/blockchain/` | On-chain queries with USD pricing |
| `pkg/memory/` | Epistemological vault + adapter |
| `pkg/acp/` | VS Code/Cursor editor integration |
| `pkg/tailscale/` | Mesh networking |
| `nanohub/` | Hub frontend + Convex backend |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 7777/18790 in use | `lsof -i :7777` → kill |
| Telegram 409 | `pkill -f "solanaos"` → restart |
| Wallet not found | `solanaos onboard` |
| Honcho empty | Needs messages to reason about — keep chatting |
| Perps empty | Set `HYPERLIQUID_PRIVATE_KEY` or `ASTER_API_KEY` |
| Build fails | `go mod tidy && make build` |

---

## One-Shot Agent Prompt

```
Read skill.md in the solanaos project root.
Follow every step. My .env values are:
  SOLANA_TRACKER_API_KEY=...
  TELEGRAM_BOT_TOKEN=...
  TELEGRAM_ID=...
  OPENROUTER_API_KEY=...
  HONCHO_API_KEY=...
Complete the full installation.
After install: solanaos status && solanaos solana wallet && solanaos pet
```

---

*SolanaOS v2.0.0 · 8BIT Labs · MIT*
*github.com/x402agent/SolanaOS · seeker.solanaos.net · go.solanaos.net*
