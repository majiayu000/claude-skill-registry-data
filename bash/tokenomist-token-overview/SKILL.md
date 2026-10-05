---
name: tokenomist-token-overview
description: Get a summary list of all tracked tokens with market data and supply info. Use when browsing tokens, comparing market caps, or finding which tokens have fundraising/burn/buyback data.
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

# Skill: Token Overview

Get a summary list of all tracked tokens with market data and supply info.

## When to use

When you need to browse all available tokens, compare market caps, or find which tokens have fundraising/burn/buyback data.

## Commands

### List all tokens
```bash
tok token list --output json
```

Options:
| Option | Description |
|--------|-------------|
| `--token-id <ids>` | Filter by token IDs (comma-separated) |

### Search tokens
```bash
tok token search <query> --output json
```

## Output fields

| Field | Description |
|-------|-------------|
| `id` | Token ID (use in other commands) |
| `name` | Token name |
| `symbol` | Ticker symbol |
| `marketCap` | Current market cap (USD), null if unavailable |
| `circulatingSupply` | Circulating supply |
| `totalLockedAmount` | Tokens still locked |
| `unlockedAmount` | Tokens already unlocked |
| `hasStandardAllocation` | Whether allocation data exists |
| `hasFundraising` | Whether fundraising data exists |
| `hasBurn` | Whether burn data exists |
| `hasBuyback` | Whether buyback data exists |

## Examples

List all tokens as a table:
```bash
tok token list
```

Filter by specific tokens:
```bash
tok token list --token-id solana,aptos --output json
```

Search by name or symbol:
```bash
tok token search bitcoin --output json
```

Export to CSV:
```bash
tok token list --output csv > tokens.csv
```

## Domain Context

- Token IDs (the `id` field) are the primary identifier used across all commands. Use `token list` to discover them.
- `circulatingSupply` and `unlockedAmount` are different concepts — unlocked tokens may not be circulating (they could be held by the team, locked in DeFi protocols, or otherwise not trading on exchanges).
- Fields like `hasStandardAllocation`, `hasFundraising`, `hasBurn`, `hasBuyback` indicate which data types are available. Check these before querying detail commands to avoid empty results.

## Workflow

- **Start here** to find token slugs before using other commands.
- Use the ID in: `tok unlock events <id>`, `tok emission daily <id>`, `tok allocation detail <id>`, etc.
- Check `has*` boolean fields (visible in `--output json`) to know which data types exist for a token before querying.

## Output Size

The `token list` command returns all tracked tokens (~200+). Use `--output json` and filter programmatically for large datasets.
