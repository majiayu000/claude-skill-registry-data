---
name: data-failover
description: >
  4-layer token data validation cascade for Buzz BD Agent.
  Ensures every piece of data touching a business decision is
  verified by 2+ independent sources. DexScreener primary,
  with Helius, Bankr, and GeckoTerminal as fallbacks.
  Valid data = long-term business.
---

# Data Failover — Token Data Validation Cascade

## Principle

Every piece of data that touches a business decision MUST be verified
by at least 2 independent sources. Unverified data = no action.

## Cascade Order

```
1. DexScreener API (FREE, primary)
   ↓ 404 / timeout / incomplete
2. Helius DAS API (FREE tier, Solana on-chain)
   ↓ rate-limited / unavailable
3. Bankr API price query (FREE, 100 msg/day shared)
   ↓ rate-limited
4. GeckoTerminal API (FREE)
   ↓ ALL fail
5. FLAG as UNVERIFIED → alert Ogie → STOP pipeline
```

## Validation Rules

| Data Point       | Primary     | Verification       | Required Match |
| ---------------- | ----------- | ------------------ | -------------- |
| Contract Address | DexScreener | Helius on-chain    | EXACT match    |
| Token Price      | DexScreener | Bankr price query  | Within 5%      |
| Market Cap       | DexScreener | GeckoTerminal      | Within 10%     |
| 24h Volume       | DexScreener | GeckoTerminal      | Within 15%     |
| LP Status        | DexScreener | Helius on-chain LP | Both confirm   |
| Token Existence  | DexScreener | Helius getAsset    | Must exist     |

## Rules

- Minimum 2 sources required for VALID data
- CA mismatch between sources → REJECT TOKEN (possible scam)
- Price variance >5% → FLAG as DISCREPANCY, use DexScreener, alert Ogie
- All sources fail → UNVERIFIED, alert Ogie, do NOT score or route
- NEVER deploy a token with unverified CA
- Bankr price check: `bankr prompt "What's the price of $TOKEN on $CHAIN?"`

## Environment Variables

```
DATA_FAILOVER_ENABLED=true
TOKEN_DATA_PRIMARY=dexscreener
TOKEN_DATA_FALLBACK_1=helius
TOKEN_DATA_FALLBACK_2=bankr
TOKEN_DATA_FALLBACK_3=geckoterminal
REQUIRE_DUAL_VERIFICATION=true
MIN_SOURCES_FOR_VALID_DATA=2
```
