---
name: token-scoring
description: 4-category composite token scoring engine (11 factors, max 100) for exchange listing intelligence — evaluates market metrics, safety audits, social signals, and quality indicators with dual-gate verification. Supports Solana, Base, BSC, and Stacks (SIP-010).
author: buzzbysolcex
author_agent: Ionic Nova (Buzz BD Agent)
user-invocable: true
arguments: doctor | run | run --address <contract> --chain <chain>
entry: token-scoring/token-scoring.ts
requires: [wallet, settings]
tags: [read-only, infrastructure, l2]
---

# Token Scoring

## What it does

Scores any token across Solana, Base, BSC, or Stacks on a 0-100 composite scale using 4 scoring categories with 11 weighted factors. Data sources: DexScreener (market data, pairs), CoinGecko (project metadata, supply data), RugCheck (contract safety audits), and Hiro API (Stacks SIP-010 tokens). Applies dual-gate verification where fundamentals (safety + holder + quality factors, max 70) and market (social + market factors, max 30) must each independently clear 60% before a token can advance. Auto-classifies tokens as HOT (85+), QUALIFIED (70-84), WATCH (50-69), or SKIP (<50).

## Scoring Categories (4 categories, 11 factors, max 100 points)

### Market (30 points max)

| Factor     | Max | How it's scored                                                    |
| ---------- | --- | ------------------------------------------------------------------ |
| market_cap | 10  | Tiered by MCap range ($100K-$50M = full marks, penalizes extremes) |
| liquidity  | 10  | Liquidity-to-MCap ratio (3%+ with $100K+ liq = full marks)         |
| volume     | 10  | Volume-to-MCap ratio (10%+ = full marks)                           |

### Safety (30 points max)

| Factor          | Max | How it's scored                                                   |
| --------------- | --- | ----------------------------------------------------------------- |
| contract_safety | 15  | RugCheck verdict + score (Good/80+ = full, Warning = 10, <30 = 2) |
| holder_dist     | 15  | Circulating/total supply ratio from CoinGecko (80%+ = full)       |

### Social (20 points max)

| Factor          | Max | How it's scored                                                              |
| --------------- | --- | ---------------------------------------------------------------------------- |
| team_identity   | 10  | CoinGecko project listing as proxy for team visibility (listed = 6, not = 3) |
| social_presence | 10  | CoinGecko project listing as proxy for community (listed = 6, not = 3)       |

### Quality (20 points max)

| Factor           | Max | How it's scored                                                 |
| ---------------- | --- | --------------------------------------------------------------- |
| token_age        | 5   | Days since pair creation (90d+ = 5, 30d+ = 4, 7d+ = 3, <1d = 1) |
| deployer_history | 5   | Default 3/5. Pump.fun tokens receive -10 composite penalty      |
| web_footprint    | 5   | CoinGecko listing = 4, not listed = 2                           |
| momentum         | 5   | 24h price change direction (positive = 4, negative = 2)         |

## Honest Limitations

- **team_identity** and **social_presence** use CoinGecko listing as a proxy for team/community presence. Not a direct social metrics analysis. Tokens not on CoinGecko score 3/10.
- **deployer_history** uses a default score of 3/5 without deep on-chain deployer wallet analysis. Pump.fun tokens get a composite penalty.
- **momentum** is a binary check on 24h price direction, not RSI/MACD technical analysis.
- **holder_dist** estimates from circulating/total supply ratio, not individual wallet analysis.
- Stacks SIP-010 support is basic — uses Hiro API for token existence and DexScreener for market data if available.

## Dual-Gate Verification

Both gates must pass independently:

- **Fundamentals gate** (safety + holder + quality): score >= 42/70 (60%)
- **Market gate** (social + market): score >= 18/30 (60%)

If either gate fails, classification is capped at WATCH regardless of composite score.

## Supported Chains

- **Solana** — Full support (DexScreener + RugCheck + CoinGecko)
- **Base** — Full support (DexScreener + CoinGecko)
- **BSC** — Full support (DexScreener + CoinGecko)
- **Stacks** — Basic SIP-010 support (Hiro API + DexScreener where available)

## Why agents need it

Any agent evaluating tokens for trading, listing, or portfolio decisions needs systematic due diligence beyond price action. This skill replaces narrative-driven evaluation with data-backed composite scoring. The dual-gate prevents tokens with inflated social metrics but poor fundamentals from passing, and vice versa.

## Safety notes

- This skill is READ-ONLY. It never writes to chain or moves funds.
- All data is pulled from public APIs (DexScreener, CoinGecko, RugCheck, Hiro).
- No wallet funds required for execution.
- Scores are informational — not financial advice.

## Commands

### doctor

Checks API connectivity to all data sources and reports readiness.

```bash
bun run token-scoring/token-scoring.ts doctor
```

### run

Scores a token by contract address. Pulls data from all sources, computes composite score, applies dual-gate, and returns classification.

```bash
bun run token-scoring/token-scoring.ts run --address <contract_address> --chain <solana|base|bsc|stacks>
```

Without arguments, scores the top trending token from DexScreener:

```bash
bun run token-scoring/token-scoring.ts run
```

## Output contract

All outputs are JSON to stdout.

```json
{
  "status": "success | error | blocked",
  "action": "review score and classification for trading/listing decision",
  "data": {
    "address": "contract address",
    "chain": "solana",
    "composite_score": 67,
    "classification": "watch",
    "dual_gate": {
      "pass": true,
      "fundamentals": { "score": 45, "max": 70, "threshold": 42, "pass": true },
      "market": { "score": 22, "max": 30, "threshold": 18, "pass": true }
    },
    "components": {
      "safety": { "score": 15, "max": 15 },
      "holder_dist": { "score": 10, "max": 15 },
      "market_cap": { "score": 10, "max": 10 },
      "liquidity": { "score": 8, "max": 10 },
      "volume": { "score": 5, "max": 10 },
      "team_identity": { "score": 6, "max": 10 },
      "social_presence": { "score": 6, "max": 10 },
      "token_age": { "score": 4, "max": 5 },
      "deployer_history": { "score": 3, "max": 5 },
      "web_footprint": { "score": 4, "max": 5 },
      "momentum": { "score": 4, "max": 5 }
    },
    "flags": ["pump_fun_detected", "low_liquidity"],
    "verdict": "PROCEED | MONITOR | REJECT"
  },
  "error": null
}
```

## Known constraints

- DexScreener free tier: 300 requests/min (sufficient for scoring)
- CoinGecko free tier: 30 requests/min (rate-limited internally)
- RugCheck may return 400 for non-Solana tokens (graceful degradation)
- Scores are point-in-time snapshots — re-score after 24h for stability check
- Pump.fun tokens auto-penalized (-10 points) due to low-mcap rug risk
