---
name: solana-research-brief
description: "Use when a user asks for a concise Solana token research snapshot with market, trade, and security context"
version: "1.0.0"
emoji: "🔬"
requires:
  bins: []
  env: ["BIRDEYE_API_KEY"]
  config: []
allowed-tools: []
---

# Solana Research Brief

Provide short-form token research with this structure:

1. **Metadata** — name/symbol/links
2. **Market** — price, market cap, FDV, liquidity, holders
3. **Trade** — volume, buy/sell split, wallets, price change
4. **Security** — mutability, top holder concentration, mint/freeze auth
5. **Bottom line** — 1-2 sentence risk summary

Keep output concise and decision-focused.

For CLI users, prefer:

```bash
solanaos solana research <mint>
```

For Telegram daemon users, prefer:

```text
/research <mint>
```
