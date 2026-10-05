---
name: tokenomist-burn-buyback
description: Check token burn and buyback activity. Use when analyzing deflationary mechanisms — burns, buybacks, and net inflation.
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

# Skill: Burn & Buyback

Check token burn and buyback activity.

## When to use

When you need to analyze deflationary mechanisms — how many tokens have been permanently burned or bought back from the market.

## Commands

### Burns

List all tokens with burns:
```bash
tok burn list --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--token-id <ids>` | Filter by token IDs (comma-separated) |
| `--page <number>` | Page number |
| `--page-size <number>` | Items per page |

```bash
tok burn list --token-id aptos,stellar --output json
```

Get burn events for a specific token:
```bash
tok burn detail <tokenId> --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--start <date>` | Start date (YYYY-MM-DD) |
| `--end <date>` | End date (YYYY-MM-DD) |

```bash
tok burn detail aptos --start 2024-01-01 --end 2024-12-31 --output json
```

### Buybacks

List all tokens with buybacks:
```bash
tok buyback list --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--token-id <ids>` | Filter by token IDs (comma-separated) |
| `--page <number>` | Page number |
| `--page-size <number>` | Items per page |

```bash
tok buyback list --token-id aave --output json
```

Get buyback events for a specific token:
```bash
tok buyback detail <tokenId> --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--start <date>` | Start date (YYYY-MM-DD) |
| `--end <date>` | End date (YYYY-MM-DD) |

```bash
tok buyback detail aave --start 2024-01-01 --end 2024-12-31 --output json
```

## Key output fields

**Burn list:**
- `totalBurnAmount` — total tokens burned for this token

**Burn detail:**
- `burns[].burnDate` — when the burn happened
- `burns[].amount` — tokens burned
- `burns[].burnType` — type of burn event
- `burns[].metadata.burnReasons` — why tokens were burned

**Buyback list:**
- `totalBuybackAmount` — total tokens bought back

**Buyback detail:**
- `buybacks[].buybackDate` — when the buyback happened
- `buybacks[].tokenAmount` — tokens bought back
- `buybacks[].value` — USD value of buyback
- `buybacks[].spentAmount` / `spentUnit` — what was spent (e.g. USDC)

## Analysis workflow

1. List tokens with burns: `tok burn list --output json`
2. Compare `totalBurnAmount` across tokens to find most deflationary projects
3. Drill into a token: `tok burn detail <id> --output json`
4. Cross-reference with emissions from `tok emission weekly <id>` to calculate net inflation

## Domain Context

- A sequential buyback + burn is a **single** deflationary event, not two. Counting both would double-count the supply reduction.
- Burns from **locked** supply don't reduce circulating supply — they reduce future potential supply instead.
- The `startDate`/`endDate` filters on burn/buyback detail commands filter by **last activity date**, not the event date range. This is an API quirk — the filters determine which tokens to include based on when they last had activity.

## Workflow

- Cross-reference with `tok emission weekly <id>` to calculate net inflation: if burns exceed emissions, the token is net deflationary.
- Use `tok token list --output json` to check `hasBurn`/`hasBuyback` fields before querying detail commands (these fields are only visible in JSON output, not table mode).
- Compare `totalBurnAmount` across tokens to find the most deflationary projects.
