---
name: crypto-research
description: Deep-dive research report on a specific cryptocurrency before trading or investing. Always trigger immediately when the user's message starts with "cr" followed by a coin name or ticker. Also trigger on "research [coin]", "due diligence [coin]", "is [coin] worth buying", or any request for a structured breakdown of a specific crypto asset. Always verify current market, team, tokenomics, and project facts before responding; never answer from memory.
version: 1.1.0
---

# Crypto Research

## Intent

Produce structured cryptocurrency due diligence with source-aware research, risks, tokenomics, listings, and practical caveats.

## Do Not Use When

- Do not use for investment advice, guaranteed returns, trade signals, or unsourced project claims.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

Generate a structured due diligence report on a specific cryptocurrency. This is a research tool for project quality and risk review, not a buy or sell recommendation engine.

## Trigger When

- The user starts with `cr` followed by a coin name or ticker
- The user asks for research, due diligence, or a full breakdown of a specific crypto asset
- The user asks whether a coin looks credible, risky, overvalued, or worth further review

Examples:

```text
cr ONDO
cr Solana
cr Sui
cr ai16z
```

## Workflow

1. Verify current facts before writing, especially price, supply, listings, team status, and recent news.
2. Gather enough source-backed information for each report section.
3. Mark unverifiable fields as `—` or `Not found` instead of guessing.
4. Write the report in the required format with a mandatory `Red Flags` section.
5. End with a research-only disclaimer and source list.

## Research Areas

Always cover:

1. Project overview and differentiators
2. Tokenomics and unlock risk
3. Team and backer credibility
4. Exchange listings and liquidity context
5. Price action and market context
6. Roadmap and development activity
7. Adoption signals and traction metrics
8. Red flags and green flags
9. Summary scorecard

## Search Guidance

Verify current information for:

- project overview and use case
- tokenomics, supply, and vesting schedule
- team and founder background
- roadmap and milestones
- current price and chart context
- exchange listings
- recent news
- risks, criticism, and controversies
- audit and security status
- market data from sources such as CoinGecko or CoinMarketCap

If search snippets are insufficient, open direct source pages for cleaner data.

## Report Format

Use this structure:

```markdown
# [Coin Name] ($TICKER) Research Report
*Generated [Month DD, YYYY] | Data as of [YYYY-MM-DD HH:MM UTC]*

## TL;DR

## Project Overview

## Tokenomics

## Team & Backers

## Exchange Listings

## Recent Price Action

## Roadmap & Development

## Use Case & Adoption

## Red Flags

## Green Flags

## Summary Scorecard

## Sources
```

## Rules

- Verify current facts before writing
- Use reliable and current sources
- Never fabricate missing data
- Keep language direct and factual
- Include a `Red Flags` section every time
- Do not provide financial advice
- Remove or mark any claim that cannot be sourced
- Avoid crypto hype language and marketing copy

## Scoring Guidance

Use this fixed rubric so every report scores the same way and reports stay comparable over time. Score each area 1 to 5 with a one-line justification tied to a sourced fact:

| Area | 5 looks like | 1 looks like |
| --- | --- | --- |
| Fundamentals | Working product with real usage | Whitepaper-only or vaporware |
| Tokenomics | High float, modest emissions, aligned vesting | Low float, heavy unlocks ahead, insider-skewed allocation |
| Team | Public, credible track record, relevant backers | Anonymous or unverifiable, no notable backers |
| Liquidity | Tier 1 exchange listings, deep books | DEX-only or thin Tier 3 books |
| Development | Active repos and shipped milestones | Stale repos, slipped roadmap |
| Risk (inverted) | Few open risks | Multiple red flags below |

The scorecard summarizes quality and risk; it is never a trading signal. Do not output an overall buy-strength number.

## Red Flag Screen

Run these checks explicitly every time and report findings, including clean results:

- **Unlock risk**: cliff or large vesting events in the next 6 months; insider share above ~40%
- **Centralization**: admin keys or upgradeable contracts without timelock, top-10 wallets holding an outsized supply share, single-sequencer or single-validator dependence
- **Suspicious emissions**: rewards funded mostly by new token issuance, APYs that only work while price rises
- **Governance theater**: a DAO where the team or foundation controls quorum, or governance that has never overturned a team proposal
- **Classic scam markers**: forked code with renamed branding, fake or unverifiable audit claims, paid-influencer-heavy promotion, team that has rugged before

A clean screen is a Green Flag entry; a partial screen (data unavailable) must be stated, not skipped.

## Compare Mode

When the user gives two assets (`cr ONDO vs CFG` or similar):

- run the same rubric on both and present the scorecards side by side in one table
- compare on the dimensions that actually differ; skip near-identical rows with a one-line note
- state which asset the evidence favors for the user's stated context, while keeping the research-only framing
- if one asset is far less documented, say the comparison is asymmetric rather than padding the weaker side

## Validation Checklist

- [ ] Current price and market data are source-backed
- [ ] Tokenomics and unlock risk are addressed
- [ ] Team and backers are verified or marked unknown
- [ ] Red flags are explicit and not omitted
- [ ] Sources are included for all major populated sections
- [ ] Output stays research-only and avoids financial advice

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A coin or token name and the kind of due diligence you want.

Example prompts:

- `Use crypto-research to do due diligence on Solana with risks, catalysts, and red flags.`
- `Research this coin and tell me whether the tokenomics and adoption story actually hold up.`
- `Show me an example prompt for a full crypto research brief.`

