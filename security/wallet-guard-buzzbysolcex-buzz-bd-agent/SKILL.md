---
name: wallet-guard
description: >
  Transaction governance layer for crypto wallet operations.
  3-state evaluation: BLOCK / WARN / ALLOW with receipt.
  Schema-frozen with AION (Aldo/CODÉ). Checks token score,
  deployer identity, liquidity depth, and contract security
  before any wallet interaction proceeds.
tags: [crypto, security, wallet, governance, agent]
---

# Wallet Guard — Buzz BD Agent

> 3-state adapter: BLOCK / WARN / ALLOW
> Schema-frozen with AION (3 locked schemas)
> API: POST https://api.buzzbd.ai/api/guard/evaluate

## When to Use

- Before any token swap or transfer
- Evaluating unknown contracts before interaction
- Agent-to-agent transaction governance
- Protecting wallets from rug pulls, honeypots, drain attacks

## 3-State Decision Engine

| State     | When                                                    | What Happens                                                  |
| --------- | ------------------------------------------------------- | ------------------------------------------------------------- |
| **BLOCK** | Score < 30 OR honeypot detected OR deployer blacklisted | Transaction rejected. Receipt logged. Alert sent to War Room. |
| **WARN**  | Score 30-69 OR missing security data OR CTO_FLAG active | Transaction paused. Human approval required via Telegram.     |
| **ALLOW** | Score >= 70 AND security clean AND identity verified    | Transaction proceeds. Receipt logged with full audit trail.   |

## Locked Schemas (Frozen with Aldo/AION)

### BuzzEvaluateRequestV1

```json
{
  "token_address": "0x...",
  "chain": "base",
  "action": "swap|transfer|approve",
  "amount_usd": 100.0,
  "requester": "agent_id"
}
```

### WalletGuardNormalizedRequestV1

```json
{
  "token_address": "0x...",
  "chain": "base",
  "action": "swap",
  "amount_usd": 100.0,
  "buzz_score": 78,
  "security_flags": [],
  "deployer_identity": { "verified": true, "ens": "dev.eth" },
  "liquidity_usd": 12400000,
  "honeypot_check": false
}
```

### WalletGuardEvaluateResponseV1

```json
{
  "decision": "ALLOW",
  "score": 78,
  "reasons": [
    "Score above threshold",
    "Identity verified",
    "Liquidity sufficient"
  ],
  "warnings": [],
  "receipt_id": "WG-2026-04-05-001",
  "evaluated_at": "2026-04-05T08:00:00Z"
}
```

## Usage

### Via Claude Code

```
/guard 0x6982508145454Ce325dDbE47a25d4ec3d2311933 swap 100
```

### Via API

```bash
curl -X POST https://api.buzzbd.ai/api/guard/evaluate \
  -H "Content-Type: application/json" \
  -d '{"token_address":"0x...","chain":"base","action":"swap","amount_usd":100}'
```

## Trust Gate Integration

Wallet Guard respects the 5-level trust system:

- Level 0 (FULL_APPROVAL): ALL transactions require Ogie's approval
- Level 1-2: BLOCK auto-rejects, WARN/ALLOW need approval
- Level 3: Only BLOCK needs approval
- Level 4 (AUTO_85): Score >= 85 auto-allows, rest need approval

Current trust level: **0 — FULL_APPROVAL** (earning autonomy)

## Security Rules

- NEVER auto-approve transactions at trust level 0
- ANY complaint → instant trust reset to Level 0
- Receipts are immutable (append-only audit table)
- Graceful fallback if AION API unreachable (defaults to WARN)
- Private keys NEVER logged, printed, committed, or transmitted
