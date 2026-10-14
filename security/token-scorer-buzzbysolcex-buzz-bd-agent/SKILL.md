---
name: token-scorer
description: >
  Score any crypto token using Buzz's 11-rule scoring engine.
  Zero LLM cost — pure rule-based analysis across liquidity, volume,
  security, deployer identity, and market dynamics. Pulls from
  DexScreener API + on-chain data. Returns 0-100 score with
  COLD/WARM/HOT classification and actionable breakdown.
tags: [crypto, defi, scoring, token, security, analysis]
---

# Token Scorer — Buzz BD Agent

> 11 permanent rules. Zero LLM cost. Real-time scoring.
> API: https://api.buzzbd.ai/api/score/{address}
> Free widget: https://buzzbd.ai/score

## When to Use

- Evaluating a token for listing potential
- Quick safety check before interaction
- Pipeline screening for BD outreach
- Hackathon demos requiring token intelligence

## Scoring Rules (v2_8rules + 3 new)

| #   | Rule                     | Type    | What It Catches                                       |
| --- | ------------------------ | ------- | ----------------------------------------------------- |
| 1   | FDV Gap Penalty          | Penalty | FDV/mcap divergence > 5x = inflated valuation         |
| 2   | Stablecoin Exclusion     | Filter  | Stablecoins auto-excluded (not listing candidates)    |
| 3   | Ghost Token Exclusion    | Filter  | No real on-chain activity = dead project              |
| 4   | Contradictory Audit Hold | Hold    | Conflicting security data = needs manual review       |
| 5   | Security Penalty         | Penalty | Flagged by Go+ Security / Token Sniffer / Honeypot.is |
| 6   | Liquidity Cross-Ref      | Verify  | Liquidity vs volume sanity check                      |
| 7   | Age Bonus                | Bonus   | Token age > 90 days = maturity signal                 |
| 8   | Volume Threshold         | Filter  | Minimum 24h volume required                           |
| 9   | GHOST_VOLUME             | Penalty | Fake volume detection (wash trading patterns)         |
| 10  | CTO_FLAG                 | Flag    | Community takeover indicator (original team left)     |
| 11  | VOLUME_LIQUIDITY_RATIO   | Penalty | Suspicious volume/liquidity ratio > 10x               |

## Score Bands

| Range  | Classification | Action                              |
| ------ | -------------- | ----------------------------------- |
| 85-100 | HOT            | BD screening pipeline activated     |
| 70-84  | WARM           | Monitor, potential future candidate |
| 50-69  | COLD           | Low priority, log and archive       |
| 0-49   | REJECTED       | Auto-filtered, do not pursue        |

## Usage

### Via API (x402 micropayment — $0.01 USDC on Base)

```bash
curl https://api.buzzbd.ai/api/score/0x...contractAddress
```

### Via Claude Code

```
/score PEPE
/score 0x6982508145454Ce325dDbE47a25d4ec3d2311933
```

### Via Free Widget

Visit https://buzzbd.ai/score — paste contract address, get instant score.

### Via npm CLI

```bash
npx @buzzbd/scorer --token PEPE --chain ethereum
```

## Response Format

```json
{
  "token": "PEPE",
  "address": "0x6982...",
  "chain": "ethereum",
  "score": 78,
  "classification": "WARM",
  "breakdown": {
    "liquidity": { "score": 85, "value": "$12.4M" },
    "volume_24h": { "score": 72, "value": "$45.2M" },
    "security": { "score": 90, "penalties": [] },
    "deployer": { "score": 65, "identity": "ANON" },
    "age_days": 412,
    "fdv_gap": 1.2
  },
  "flags": [],
  "rules_triggered": ["AGE_BONUS"],
  "scored_at": "2026-04-05T08:00:00Z",
  "llm_cost": "$0.00"
}
```

## Architecture Notes

- Scoring engine is 100% rule-based (zero LLM inference)
- Data pulled from DexScreener API (free tier)
- Identity verification via ATV (x402, $0.01/call)
- Results cached 1 hour in SQLite
- On-chain proof: ScoreStorage v2 on Base mainnet
- 482-token public leaderboard at buzzbd.ai/scores
