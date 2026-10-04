---
name: "ATR — Average True Range Volatility Meter"
description: "Use when measuring volatility with ATR, setting ATR-based stop-losses, calculating position sizes by risk tolerance, or comparing volatility across timeframes."
version: "2.0.1"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["atr", "volatility", "trading", "crypto", "stocks", "technical-analysis", "finance", "risk-management"]
---

# ATR — Average True Range Volatility Meter

Measure market volatility using Average True Range. Calculate ATR-based stop-losses, position sizes, and compare volatility across different timeframes and assets.

## Commands

### calculate
Calculate ATR from price data with True Range breakdown.
```bash
bash scripts/script.sh calculate 14
```

### interpret
Interpret an ATR value relative to price for volatility assessment.
```bash
bash scripts/script.sh interpret 2.45 150.00
```

### stoploss
Calculate ATR-based stop-loss levels using ATR multiples.
```bash
bash scripts/script.sh stoploss 2.45 150.00 long 2.0
```

### position-size
Calculate position size based on ATR and risk parameters.
```bash
bash scripts/script.sh position-size 2.45 10000 2.0 2.0
```

### compare
Compare ATR volatility across different periods and contexts.
```bash
bash scripts/script.sh compare
```

### help
Show all commands.
```bash
bash scripts/script.sh help
```

## Output
- ATR values with True Range component breakdown
- Volatility classification (low/medium/high/extreme)
- Stop-loss price levels and distance
- Position size in units and dollar amount

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
