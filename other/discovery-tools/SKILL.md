---
name: discovery-tools
description: How SCOUT finds, filters, and structures high-signal Solana memecoin leads from pump.fun, gmgn.ai, Photon, Axiom, and social sources. Produces the standard LEAD block.
---

# Discovery Tools

## Primary Surfaces
- pump.fun
- gmgn.ai
- Photon / Axiom
- Solscan recent deployments
- High-signal X and Telegram channels

## Mandatory Output Schema
```
LEAD-ID: SOL-YYYYMMDD-NNN
Mint: <full address>
Source: <URL or tx signature>
Age: <minutes>
Initial Liquidity: <SOL or USD>
Mint Authority (visible): <status>
Early Signals: ...
Why this lead: <1–2 precise sentences>
Hand-off to RISK: YES
UTC Timestamp: <ISO>
```

## Never
- Recommend buy size or urgency
- Clear risk yourself
- Surface leads without a verifiable mint and source
