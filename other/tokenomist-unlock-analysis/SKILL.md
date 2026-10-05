---
name: tokenomist-unlock-analysis
description: Analyze token unlock events — upcoming unlocks, historical events, and allocation breakdowns. Use when checking unlock impact on market cap or reviewing unlock schedules.
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

# Skill: Unlock Analysis

Analyze token unlock events — upcoming unlocks, historical events, and allocation breakdowns.

## When to use

When you need to check upcoming token unlocks, assess unlock impact on market cap, or review historical unlock events for a specific token.

## Commands

### List all unlock events (grouped by token)
```bash
tok unlock list --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--min-market-cap <value>` | Minimum market cap |
| `--min-released-percentage <value>` | Minimum released percentage |
| `--min-unlock-date <date>` | Min unlock date (YYYY-MM-DD) |
| `--max-unlock-date <date>` | Max unlock date (YYYY-MM-DD) |
| `--min-total-unlock-amount <value>` | Minimum total unlock amount |
| `--min-value-to-market-cap <value>` | Min value-to-market-cap ratio |
| `--standard-allocation <names>` | Filter by allocation (comma-separated) |
| `--page <number>` | Page number |
| `--page-size <number>` | Items per page |

```bash
tok unlock list --min-market-cap 1000000 --min-unlock-date 2025-01-01 --max-unlock-date 2025-12-31
tok unlock list --min-value-to-market-cap 0.01 --standard-allocation "privateInvestors,founderTeam"
```

Available `--standard-allocation` values: `community`, `founderTeam`, `privateInvestors`, `publicInvestors`, `others`, `reserve` (comma-separated for multiple).

### Get upcoming unlocks (next event per token)
```bash
tok unlock upcoming --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--start <date>` | Start date (YYYY-MM-DD) |
| `--end <date>` | End date (YYYY-MM-DD) |
| `--standard-allocation <names>` | Filter by allocation (comma-separated) |
| `--min-market-cap <value>` | Minimum market cap |
| `--min-released-percentage <value>` | Minimum released percentage |
| `--min-total-unlock-amount <value>` | Minimum total unlock amount |
| `--min-value-to-market-cap <value>` | Min value-to-market-cap ratio |
| `--page <number>` | Page number |
| `--page-size <number>` | Items per page |

```bash
tok unlock upcoming --min-market-cap 5000000 --min-value-to-market-cap 0.01 --output json
```

### Get unlock events for a specific token
```bash
tok unlock events <tokenId> --output json
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
tok unlock events solana --start 2025-01-01 --end 2025-12-31 --output json
```

## Key output fields

**unlock list / upcoming:**
- `tokenName`, `tokenSymbol` — token identification
- `marketCap` — current market cap
- `releasedPercentage` — how much of total supply has been released

**unlock events:**
- `unlockDate` — when the unlock happens
- `cliffUnlocks.cliffAmount` — number of tokens unlocking
- `cliffUnlocks.cliffValue` — USD value of the unlock
- `cliffUnlocks.valueToMarketCap` — unlock value as % of market cap
- `cliffUnlocks.allocationBreakdown` — which allocations are unlocking

## Analysis workflow

1. Run `tok unlock upcoming --output json` to find tokens with large upcoming unlocks
2. Filter by `valueToMarketCap` to identify potentially market-moving events
3. Drill into specific tokens with `tok unlock events <id> --output json`
4. Check allocation breakdown to understand who is receiving tokens (investors, team, community, etc.)

## Domain Context

- **Unlocked does not mean circulating.** Tokenomist tracks release schedules (when tokens become available), not on-chain transfers. Tokens can be unlocked but still held by the team, locked in DeFi, or otherwise not on the open market.
- Schedules may include assumptions — the allocation breakdown can help assess confidence in the schedule.
- `valueToMarketCap` is a key metric: unlocks representing >1% of market cap may be market-moving events.

## Workflow

- Use `tok token list --output json` first to find the token ID if you don't know it.
- Chain with `tok emission daily <id>` for a complete unlock + emission picture.
- Cross-reference with `tok allocation detail <id>` to understand which groups (team, investors, community) are unlocking.
- Use `tok fundraising detail <id>` to see what price investors paid — compare with current price to assess sell pressure.

## Output Size

The `unlock list` command can return hundreds of events. Use date and market cap filters to narrow results: `--min-market-cap`, `--min-unlock-date`, `--max-unlock-date`.
