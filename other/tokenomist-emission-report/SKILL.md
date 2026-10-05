---
name: tokenomist-emission-report
description: Get daily or weekly token emission data with allocation breakdowns. Use when analyzing token inflation, comparing emission rates, or understanding supply increases.
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

# Skill: Emission Report

Get daily or weekly token emission data with allocation breakdowns.

## When to use

When you need to analyze token inflation over time, compare emission rates across periods, or understand which allocations are contributing to supply increases.

## Commands

### Daily emission
```bash
tok emission daily <tokenId> --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--start <date>` | Start date (YYYY-MM-DD) |
| `--end <date>` | End date (YYYY-MM-DD) |
| `--standard-allocation <names>` | Filter by allocation (comma-separated) |
| `--page <number>` | Page number |
| `--page-size <number>` | Items per page |

```bash
tok emission daily arbitrum --start 2024-08-01 --end 2024-08-31 --output json
tok emission daily arbitrum --standard-allocation "privateInvestors" --output json
```

Available `--standard-allocation` values: `community`, `founderTeam`, `privateInvestors`, `publicInvestors`, `others`, `reserve` (comma-separated for multiple).

### Weekly emission
```bash
tok emission weekly <tokenId> --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--start <date>` | Start date (YYYY-MM-DD) |
| `--end <date>` | End date (YYYY-MM-DD) |
| `--standard-allocation <names>` | Filter by allocation (comma-separated) |
| `--page <number>` | Page number |
| `--page-size <number>` | Items per page |

```bash
tok emission weekly arbitrum --start 2024-01-01 --end 2024-06-30 --output json
tok emission weekly arbitrum --standard-allocation "founderTeam" --output json
```

## Key output fields

| Field | Description |
|-------|-------------|
| `startDate` | Period start |
| `endDate` | Period end |
| `unlockAmount` | Tokens emitted in period |
| `unlockValue` | USD value of emitted tokens |
| `referencePrice` | Token price used for value calculation |
| `allocations` | Breakdown by allocation (name, amount, value) |
| `totalCumulativeUnlockedAmount` | Running total of all unlocked tokens |

## Analysis workflow

1. Get weekly emissions to see the trend: `tok emission weekly <id> --output json`
2. Look at `unlockAmount` over time to spot acceleration or deceleration
3. Check `allocations` to see if emissions are going to investors (sell pressure) vs community/ecosystem (growth)
4. Compare `unlockValue` against market cap from `tok token list` to assess dilution

## Domain Context

- Emission data shows **scheduled** releases per allocation. Actual on-chain supply may differ due to relocks, delays, or early releases.
- Compare `unlockValue` against market cap (from `tok token list`) to assess dilution impact.
- Emissions going to "Investor" or "Team" allocations typically represent higher sell pressure than "Community" or "Ecosystem" allocations.

## Workflow

- Combine with `tok unlock events <id>` to distinguish between cliff unlocks (large one-time events) and continuous emissions (steady daily/weekly releases).
- Chain with `tok burn detail <id>` to calculate net inflation: emissions minus burns = net new supply.
- Use `tok allocation detail <id>` to see the full allocation picture and understand where emissions are going.
