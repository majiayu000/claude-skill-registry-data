---
name: crypto-research-readonly
description: "Research crypto assets in a strictly read-only mode using verified network and contract identity, multi-venue price checks, liquidity and derivatives structure, tokenomics and unlocks, treasury and governance, protocol usage, on-chain evidence, smart-contract and custody risks, catalysts, technical context, and bear/base/bull scenarios. Use when the user asks which coin or token to buy, whether to hold or sell crypto, how much it may move, compares exchanges or tokens, or requests crypto market analysis. Never connect a wallet, sign a transaction, trade, transfer, bridge, approve a token, reveal a private key, or automate spending. Turkish triggers: kripto analizi, coin/token alınır mı, kontrat ve tokenomik, cüzdansız salt okunur araştırma."
---

# Crypto Research Readonly

Keep every operation read-only. Read [references/crypto-evidence.md](references/crypto-evidence.md), [references/tokenomics-checklist.md](references/tokenomics-checklist.md), and [references/risk-checklist.md](references/risk-checklist.md).

## Workflow

1. Resolve asset name, ticker, network, contract address, pair, venue, and quote currency. Stop if the symbol is ambiguous.
2. Reconcile timestamped quotes from at least two venues or one major venue plus an independent aggregator using `scripts/reconcile_quotes.py`.
3. Examine spot and derivatives liquidity, volume quality, spread, market depth when available, open interest, funding, basis, liquidations, and venue concentration.
4. Verify supply: circulating, total/max, emissions, burns, staking, insider/investor allocation, vesting and unlock calendar.
5. Evaluate protocol demand, fees/revenue where meaningful, active usage, treasury, governance, validators, bridge/oracle dependencies and upgrade control.
6. Review contract audits, exploit history, admin keys, custody, stablecoin/depeg, regulatory, listing/delisting and manipulation risks.
7. Use technical analysis only after identity and liquidity checks. Compare with BTC/ETH and the relevant sector benchmark.
8. Produce bull/base/bear scenarios, catalysts, invalidation, maximum plausible loss and confidence.

## Hard rules

- Never use ticker alone as identity.
- Never call one exchange's last trade the universal market price.
- Never treat reported volume, social sentiment, holder count, or an audit badge as proof of safety.
- Never request seed phrases, private keys, API secrets, wallet approvals, deposits, or transfers.
- Never use write-capable MCP, x402 payment, swap, mint, sniper, bot, or auto-trading tools.
- Do not provide certainty or guaranteed yield. If current execution data is incomplete, give ranked conditional setups and a quantity formula; finalize quantity once price, liquidity, budget and loss limit are known.
- Do not reject a legal high-risk crypto idea merely for volatility. Rank it on probability-weighted return, liquidity, token unlocks, catalyst quality and loss containment.

## Output

Start with identity, quote timestamp and venue dispersion. Then state action, horizon, token thesis, supply/unlock risk, usage, market structure, technical context, catalysts, bear/base/bull ranges, invalidation, custody risks and missing evidence.
