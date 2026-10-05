---
name: solana-market-data
description: Fetch and structure live market data for any Solana mint — price, liquidity, volume, bonding-curve progress, and multi-DEX depth.
---

# Solana Market Data

## Preferred Sources
- Jupiter quote / price endpoints (via tools/jupiter_quote.py)
- gmgn.ai
- Solscan
- Photon / Axiom

## Output Schema
```
MINT: ...
UTC: ...
Price SOL / USD: ...
Liquidity: ...
Volume 1h: ...
Bonding Curve: ... % (or graduated)
Holders (approx): ...
Sources: [list]
```
