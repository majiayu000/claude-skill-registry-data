---
name: stock-hot
description: Hot Scanner — find the most trending and high-momentum stocks and crypto right now via AIsa API. Top gainers, losers, most active by volume, crypto highlights, news catalysts, and top 5 watchlist picks. Use when the user asks about trending stocks, what's hot, market movers, or momentum plays.
author: AIsa
version: 1.0.0
license: Apache-2.0
homepage: https://aisa.one
source: https://github.com/baofeng-tech/agent-skills-io/tree/main/targetSkills/stock-hot
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 📊
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    optionalEnv:
    - AISA_BASE_URL
    - AISA_MODEL
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 📊
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    optionalEnv:
    - AISA_BASE_URL
    - AISA_MODEL
    primaryEnv: AISA_API_KEY
---

# Hot Scanner — AIsa Edition

Scan for the most trending and high-momentum stocks and cryptocurrencies using the AIsa API.

## Usage

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/stock-hot/scripts/hot_scanner.py"
python3 "${CLAUDE_PLUGIN_ROOT}/skills/stock-hot/scripts/hot_scanner.py" --focus stocks
python3 "${CLAUDE_PLUGIN_ROOT}/skills/stock-hot/scripts/hot_scanner.py" --focus crypto
python3 "${CLAUDE_PLUGIN_ROOT}/skills/stock-hot/scripts/hot_scanner.py" --output json
```

### Arguments

- `--focus`: Filter by `stocks`, `crypto`, or `both` (default)
- `--output json`: Append structured JSON summary

## Output Sections

- **Top Stock Movers**: Gainers (>3%), losers, most active by volume
- **Crypto Highlights**: BTC price, dominance, trending coins, gainers/losers
- **News-Driven Movers**: 5-8 items with ticker mentions from last 6 hours
- **Top 5 Watchlist Picks**: With risk level assessment
- **Quick Take**: 2-3 sentence market summary

**NOT FINANCIAL ADVICE.** For informational purposes only.
