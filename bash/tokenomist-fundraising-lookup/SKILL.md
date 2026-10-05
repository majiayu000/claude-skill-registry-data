---
name: tokenomist-fundraising-lookup
description: Look up fundraising rounds, investors, and valuation data for tokens. Use when finding who invested, at what valuation, or analyzing investor portfolios.
metadata:
  openclaw:
    requires:
      env:
        - TOKENOMIST_API_KEY
      bins:
        - tok
    primaryEnv: TOKENOMIST_API_KEY
    install:
      - kind: node
        package: "@tokenomist-ai/tokenomist-cli"
        bins: [tok]
allowed-tools: Bash(tok:*)
---

# Skill: Fundraising Lookup

Look up fundraising rounds, investors, and valuation data for tokens.

## When to use

When you need to find out who invested in a token, what valuation rounds were raised at, or what an investor's portfolio looks like.

## Commands

### Get fundraising data for a token
```bash
tok fundraising detail <tokenId> --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--funding-date-min <date>` | Min funding date (YYYY-MM-DD) |
| `--funding-date-max <date>` | Max funding date (YYYY-MM-DD) |
| `--raised-amount-min <value>` | Min raised amount |
| `--raised-amount-max <value>` | Max raised amount |

```bash
tok fundraising detail uniswap --output json
tok fundraising detail uniswap --funding-date-min 2020-01-01 --funding-date-max 2024-12-31 --raised-amount-min 1000000 --output json
```

### List all investors
```bash
tok investor list --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--start-latest-funding-date <date>` | Start date filter for latest funding (YYYY-MM-DD) |
| `--end-latest-funding-date <date>` | End date filter for latest funding (YYYY-MM-DD) |
| `--page <number>` | Page number |
| `--page-size <number>` | Items per page |

```bash
tok investor list --start-latest-funding-date 2023-01-01 --end-latest-funding-date 2024-01-01 --output json
```

### Get investor detail with portfolio
```bash
tok investor detail <investorId> --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--is-lead-investor` | Filter to rounds where investor was lead |
| `--funding-date-min <date>` | Min funding date (YYYY-MM-DD) |
| `--funding-date-max <date>` | Max funding date (YYYY-MM-DD) |
| `--raised-amount-min <value>` | Min raised amount |
| `--raised-amount-max <value>` | Max raised amount |

```bash
tok investor detail andreessen-horowitz --is-lead-investor --output json
tok investor detail andreessen-horowitz --funding-date-min 2023-01-01 --raised-amount-min 5000000 --output json
```

## Key output fields

**Token fundraising:**
- `totalAmountRaised` — total USD raised across all rounds
- `investorReleasedPercentage` — how much investor allocation has unlocked
- `fundingRounds[].fundingRound` — round name (Seed, Series A, etc.)
- `fundingRounds[].amountRaised` — USD raised in that round
- `fundingRounds[].valuation` — token valuation at that round
- `fundingRounds[].pricePerToken` — price investors paid
- `fundingRounds[].investors` — list of investors in the round

**Investor detail:**
- `fundingRounds[].tokenId` — which token they invested in
- `fundingRounds[].isLeadInvestor` — whether they led the round
- `fundingRounds[].totalAmountRaisedinThatRound` — round size

## Analysis workflow

1. Look up a token: `tok fundraising detail <id> --output json`
2. Compare `pricePerToken` across rounds to see valuation progression
3. Check `investorReleasedPercentage` — high % means most investor tokens are already unlocked (less future sell pressure)
4. Look at individual investors: `tok investor detail <id> --output json` to see their full portfolio

## Domain Context

- `pricePerToken` in early rounds vs current market price shows investor ROI — large multiples may indicate sell pressure as investors take profits.
- `investorReleasedPercentage` indicates future sell pressure — a high percentage means most investor tokens have already unlocked (less remaining overhang).
- Valuation at each round shows the project's funding trajectory.

## Workflow

- Chain with `tok investor detail <investorId>` to see an investor's full portfolio across multiple tokens.
- Cross-reference `pricePerToken` with current market data from `tok token list` to calculate investor ROI.
- Use `tok unlock events <id>` to see when remaining investor allocations will unlock.
