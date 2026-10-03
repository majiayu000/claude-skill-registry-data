---
name: solana-token-research
description: Research a Solana token or daily hot-token set using market structure, liquidity and AMM reserves, directional wallet flows, source-of-funds tracing, holder normalization, MEV/bot filtering, KOL evidence, and explicit trade triggers. Use when Codex is asked to investigate a Solana token, explain a volume or market-cap spike, identify buyers or sellers, assess market-maker or manipulation claims, rank hot tokens, build monitoring rules, or produce an evidence-backed Crypto research report for X/Twitter.
---

# Solana Token Research

Produce an evidence-backed snapshot before giving a narrative or trade view.

## Start

1. Resolve the exact mint address and reject symbol-only identification.
2. Record the snapshot timestamp, timezone, data source, pair address, quote asset and pool venue.
3. Use GMGN market/token/holder/portfolio/track capabilities when available. Supplement gaps with Solana RPC, DEX pool data and current public sources.
4. Read [references/evidence-framework.md](references/evidence-framework.md) before attributing wallets, market makers, insiders or KOLs.
5. Read [references/report-schema.md](references/report-schema.md) when producing a ranking, spreadsheet, monitor or publishable report.

## Research workflow

### 1. Market structure

- Collect price, market cap, FDV, liquidity, holders and volume for 5m, 15m, 1h, 6h and 24h windows when available.
- Compare liquidity growth with price and volume growth. Flag price expansion without matching liquidity.
- Split the move into accumulation, markup, acceleration, distribution and stabilization phases when the chart supports them.
- Identify support, reclaim, confirmation, prior-high and invalidation levels.

### 2. Pool and execution evidence

- Inspect the dominant pool, its token/SOL reserves, liquidity concentration and reserve changes across the event.
- Estimate the quote-side capital required for the observed price displacement using the AMM curve. State assumptions.
- Distinguish gross turnover from directional net flow.
- Flag shallow liquidity, concentrated LP ownership, removable liquidity and abnormal slippage.

### 3. Wallet flows

- Rank net buyers and net sellers over the event window; include trade count, amount, average entry, remaining balance and realized behavior.
- Trace the immediate source of funds. Classify it as CEX withdrawal, bridge inflow, internal token rotation, wallet transfer or unknown.
- Score wallet quality from repeated history, not one well-timed trade.
- Separate directional holders from sandwich bots, bundlers, arbitrageurs and same-block round trips.
- Treat market-maker attribution as a hypothesis unless repeated two-sided quoting, inventory behavior and counterparty structure support it.

### 4. Holder structure

- Normalize DEX vaults, pool authorities, CEX custody, bridges, burn addresses and program accounts before calculating private concentration.
- Report adjusted private Top 10, related-wallet clusters, creator/dev holdings, profitable supply, trapped supply and holder-duration distribution.
- Compare price direction with holder-count direction. Explain whether the pattern suggests accumulation, dispersion or noise.

### 5. Narrative and social evidence

- Search current X/Twitter and official project channels when the move may be news-driven.
- Map a KOL only with public identity evidence or a reliable labeled-wallet source.
- Explain why the account matters: audience, prior calls, project role, wallet performance or information access.
- Separate confirmed announcements, credible rumors and engagement-only chatter.

### 6. Decision model

Score 0–100 using:

- Market and liquidity quality: 20
- Directional capital quality: 25
- Flow persistence: 15
- Adjusted holder structure: 15
- Narrative and social confirmation: 10
- Execution safety: 15

Cap the score at 45 for critical unresolved risks such as unverifiable mint identity, removable liquidity, extreme private concentration, active creator dumping or predominantly bot-generated volume.

Do not output a binary buy call alone. Provide:

- base case, bull case and bear case
- entry confirmation conditions
- invalidation conditions
- monitoring metrics and alert thresholds
- evidence that would change the conclusion

## Output rules

- Lead with the conclusion and confidence level.
- Label facts as observed, labeled by a provider, or inferred.
- Include full mint and relevant wallet addresses in a copyable appendix.
- Include timestamps and methodology caveats.
- Never expose API keys, cookies, private keys or unredacted personal data.
- Do not execute trades unless the user separately and explicitly authorizes financial execution.
- State that the research is not investment advice.
