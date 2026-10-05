---
name: solanaos
description: Full SolanaOS operator skill — install the runtime, query Solana blockchain data via SolanaTracker RPC, manage wallets, run OODA trading loops, configure multi-venue strategies (spot + Hyperliquid + Aster perps), control BitAxe mining fleets, pair Seeker devices, and interact with the SolanaOS Hub. Use when asked about SolanaOS installation, Solana wallet balances, token research, trading strategy, OODA loops, gateway setup, Telegram bot configuration, mining fleet management, or any SolanaOS runtime operation.
---

# SolanaOS — The Solana Computer

Autonomous operator runtime for Solana trading, research, wallets, and hardware control.

**Repo**: [github.com/x402agent/SolanaOS](https://github.com/x402agent/SolanaOS)
**Hub**: [seeker.solanaos.net](https://seeker.solanaos.net)
**Souls**: [souls.solanaos.net](https://souls.solanaos.net)
**Docs**: [solanaos.net](https://solanaos.net)

## Install

```bash
npx solanaos-cli install
# or
git clone https://github.com/x402agent/SolanaOS.git && cd solanaos && make build
```

After install: `solanaos daemon` starts everything.

## Solana Blockchain Queries

SolanaOS uses SolanaTracker RPC + Datastream for real-time data. No Python script needed — queries are built into the Go binary.

### Wallet & Balance

```bash
solanaos solana wallet              # agent wallet address + SOL balance
solanaos solana balance <pubkey>    # any wallet balance
solanaos solana health              # RPC health check
```

### Token Research

```bash
solanaos solana research <mint>     # deep research: price, holders, liquidity, chart
solanaos solana trending            # trending tokens from SolanaTracker
```

Via Telegram: `/wallet`, `/trending`, `/research <mint>`

### On-Chain Registry

```bash
solanaos solana register            # register agent on-chain (devnet NFT)
solanaos solana registry            # view registered agents
```

## Trading — OODA Loop

The OODA loop (Observe → Orient → Decide → Act) runs autonomously:

```bash
solanaos ooda --sim                 # paper trading (simulated)
solanaos ooda --live                # live trading (real SOL)
solanaos ooda --interval 30         # custom interval in seconds
```

### Multi-Venue Strategy

Three venues with one shared risk engine:

| Venue | Use case |
| --- | --- |
| **Solana Spot** | Pump.fun launches, meme rotations, breakout continuation |
| **Hyperliquid Perps** | Liquid directional expression, funding dislocations |
| **Aster Perps** | Solana-native perp exposure, shared wallet context |

### Key Strategy Parameters

```bash
# Via Telegram /set command:
/set rsi_period 14
/set stop_loss 7
/set take_profit 25
/set position_size 10
```

| Parameter | Default | Range |
| --- | --- | --- |
| `rsi_period` | 14 | 5–30 |
| `rsi_overbought` | 72 | 60–90 |
| `rsi_oversold` | 28 | 10–40 |
| `ema_fast` | 9 | 3–20 |
| `ema_slow` | 21 | 10–100 |
| `stop_loss` | 7% | 1–50% |
| `take_profit` | 25% | 1–500% |
| `position_size` | 10% | 1–50% |

### Confidence Model

Trades scored 0.00–1.00: trend structure (0.25), momentum (0.20), liquidity (0.20), participation (0.15), execution risk (0.20). Entry requires ≥0.60 confidence.

### Drawdown Cascade

| Drawdown | Action |
| --- | --- |
| 5% | Reduce weakest exposure, block high-risk entries |
| 8% | Close all perps, spot-only mode |
| 12% | Full halt until review |

## Gateway & Seeker

```bash
solanaos gateway start              # start gateway API (port 18790)
solanaos gateway setup-code         # print QR for Seeker pairing
```

Pair at [seeker.solanaos.net/dashboard](https://seeker.solanaos.net/dashboard) or scan the QR code with the Android app.

## Telegram Bot

Auto-registers commands on daemon start. Key commands:

| Command | What |
| --- | --- |
| `/status` | Full agent status |
| `/wallet` | Address + SOL balance |
| `/trending` | Trending tokens |
| `/ooda` | Trigger OODA cycle |
| `/strategy` | Show parameters |
| `/memory` | Honcho peer card + facts |
| `/recall <query>` | AI memory retrieval |
| `/miner` | BitAxe fleet status |

## Memory — Honcho v3

Three memory layers:
1. **Local Vault** (`~/.solanaos/memory/`) — decisions, lessons, trades, research
2. **Honcho v3** — cross-session dialectic memory with user modeling
3. **Convex** — cloud persistence for Hub + Android sync

```bash
# Telegram commands:
/memory                     # show peer card + known facts
/recall <query>             # AI-powered memory retrieval
/remember <fact>            # save durable fact
/honcho_status              # bridge config
```

## BitAxe Mining (MawdAxe)

```bash
# In .env:
BITAXE_HOST=192.168.1.42
BITAXE_ENABLED=true
```

Fleet dashboard: [seeker.solanaos.net/mining](https://seeker.solanaos.net/mining)

## Chrome Extension

Load `chrome-extension/` folder unpacked in `chrome://extensions`. Tabs: Wallet, Seeker, Miner, Chat, Tools.

## Minimum .env

```bash
SOLANA_TRACKER_API_KEY=your-key
OPENROUTER_API_KEY=sk-or-v1-...
TELEGRAM_BOT_TOKEN=your-token
TELEGRAM_ID=your-chat-id
HONCHO_ENABLED=true
HONCHO_API_KEY=hch-v3-...
```

## Hub Pages

| Page | URL |
| --- | --- |
| Launch | [solanaos.net](https://solanaos.net) |
| Dashboard | [seeker.solanaos.net/dashboard](https://seeker.solanaos.net/dashboard) |
| Mining | [seeker.solanaos.net/mining](https://seeker.solanaos.net/mining) |
| Strategy Builder | [seeker.solanaos.net/strategy](https://seeker.solanaos.net/strategy) |
| Skill Creator | [seeker.solanaos.net/create](https://seeker.solanaos.net/create) |
| Skills | [seeker.solanaos.net/skills](https://seeker.solanaos.net/skills) |
| Souls | [souls.solanaos.net](https://souls.solanaos.net) |

## Setup Guides

| Guide | URL |
| --- | --- |
| Gateway | [/setup/gateway](https://seeker.solanaos.net/setup/gateway) |
| Telegram | [/setup/telegram](https://seeker.solanaos.net/setup/telegram) |
| Metaplex Agent | [/setup/metaplex](https://seeker.solanaos.net/setup/metaplex) |
| BitAxe Mining | [/setup/mining](https://seeker.solanaos.net/setup/mining) |
| Chrome Extension | [/setup/extension](https://seeker.solanaos.net/setup/extension) |

---

*SolanaOS · Built by SolanaOS Labs · MIT License · Powered by Go · Built on Solana*
