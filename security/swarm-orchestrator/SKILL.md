---
description: Orchestrate multi-bot trading swarms on Pump.fun with persona-driven agents
---

# Swarm Orchestrator

Manage multi-bot trading swarms with agent personas, epistemological memory, and cross-bot event routing.

## Prerequisites

- SolanaOS core installed
- `TELEGRAM_BOT_TOKEN` for Telegram gateway (optional)
- `HELIUS_RPC_URL` configured

## Quick Start

```bash
# Start the swarm orchestrator
npm run swarm

# Start SolanaOS agent orchestrator
npm run claw
npm run claw:dev  # with hot reload
```

## Agent Roles

| Role | Description | Auto-Actions |
|------|-------------|-------------|
| `sniper` | Snipe new token launches | Monitor → Buy on launch |
| `monitor` | On-chain event watcher | Observe → Alert |
| `fee-claimer` | Claim creator fees | Check → Claim automatically |
| `analyst` | Price/curve analysis | Observe → Report |
| `momentum` | Momentum-based trading | RSI+EMA → Execute |
| `graduation` | Target near-graduation tokens | Monitor progress → Buy |
| `market-maker` | Provide liquidity | Buy/sell oscillation |
| `launcher` | Create new tokens | Build → Launch |
| `channel-feed` | Telegram channel updates | Events → Post |
| `outsider` | Call tracking + leaderboards | Track → Score |

## Persona Assignment

Every agent can be born with one of 43+ DeFi personas:

```bash
# Via Telegram
/spawn analyst --persona whale-watcher
/spawn sniper --persona alpha-leak-detector
/personas                    # Browse all personas
/personas trading            # Filter by category
```

### Persona Categories

| Category | Count | Examples |
|----------|-------|---------|
| 🪙 Crypto | 6 | Whale Watcher, Alpha Detector |
| 🏦 DeFi | 14 | Yield Farmer, Flash Loan Analyst |
| 📈 Trading | 5 | Pump SDK Expert, MEV Researcher |
| 🔒 Security | 6 | Smart Contract Auditor |
| 📚 Education | 2 | DeFi Mentor |

## Event Bus

All bots communicate through a pub/sub event bus:

| Event | Source | Description |
|-------|--------|-------------|
| `token:launch` | websocket-server | New token detected |
| `token:graduation` | monitor | Token completed bonding curve |
| `trade:buy` / `trade:sell` | swarm-bot | Trade executed |
| `alert:whale` | monitor | Large transaction detected |
| `fee:claim` | fee-claimer | Fee claimed successfully |
| `call:new` | outsiders-bot | New call registered |

## Memory System

Each agent gets its own ClawVault with 3-tier epistemological memory:

- **KNOWN** (60s TTL) — live market data
- **LEARNED** (7d TTL) — validated patterns
- **INFERRED** (3d TTL) — hypotheses

```bash
/memory <agent-id>     # View agent's memory
/agents                # List agents with memory stats
/health                # Collective memory overview
```

## Telegram Commands

| Command | Description |
|---------|-------------|
| `/spawn <role> [--persona <id>]` | Spawn agent |
| `/stop <id>` | Stop an agent |
| `/agents` | List active agents |
| `/personas [query]` | Browse personas |
| `/memory <id>` | View agent memory |
| `/health` | Swarm health dashboard |
| `/price <mint>` | Token price |
| `/quote <mint> <sol>` | Buy/sell quote |
| `/curve <mint>` | Bonding curve state |
| `/events` | Recent event stream |

## Bot Manager

The bot manager handles lifecycle for sub-bots:

```typescript
import { BotManager, EventBus } from "solanaos";

const eventBus = new EventBus(5000);
const manager = new BotManager(eventBus);

await manager.start("telegram-bot");
await manager.start("swarm-bot");

manager.startHealthChecks();

// Route events
eventBus.on("alert:whale", (event) => {
  console.log("Whale detected:", event.data);
});
```
