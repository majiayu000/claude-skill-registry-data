---
name: dwlf
description: >
  Interact with DWLF (dwlf.co.uk), a market analysis platform for crypto and stocks.
  Use for: market data, price charts, technical indicators (EMA, RSI, DSS, S/R, trendlines,
  candlestick patterns, SMC), strategies (visual signal builder), backtesting, custom events,
  trade signals, portfolio tracking, watchlists, trade journaling, chart annotations,
  trade plans, position sizing, and academy content.
  Trigger on: market analysis, trading signals, backtests, portfolio, DWLF, chart indicators,
  support/resistance, strategy builder, trade journal, watchlist, chart annotations, trade plans,
  position sizing, how's BTC, how's the market.
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins: ["curl", "jq"]
  minis:
    originalSource: "https://clawskills.sh/skills/andywilliams-dwlf"
    convertedAt: "2026-10-31T22:10:50.050Z"
    license: "Unknown"
---

# DWLF — Market Analysis Platform

API base: `https://api.dwlf.co.uk/v2`

## Auth

Use API key auth. Check `TOOLS.md` for the key. Header:
```
Authorization: ApiKey dwlf_sk_...
```

Helper script: `scripts/dwlf-api.sh`

## Quick Start

```bash
# Generic GET request
./scripts/dwlf-api.sh GET /market-data/BTC-USD

# With query params
./scripts/dwlf-api.sh GET "/events?symbol=BTC-USD&limit=10"

# POST request
./scripts/dwlf-api.sh POST /visual-backtests '{"strategyId":"...","symbol":"BTC-USD"}'
```

## Annotation Examples

```bash
# Create a horizontal line annotation at a key support level
./scripts/dwlf-api.sh POST /annotations '{
  "symbol": "BTC-USD",
  "timeframe": "1d",
  "type": "hline",
  "data": { "price": 95000, "color": "#00ff00", "label": "Key Support", "lineStyle": "solid", "lineWidth": 2, "showPrice": true },
  "origin": "ai"
}'

# Create a text annotation on chart
./scripts/dwlf-api.sh POST /annotations '{
  "symbol": "ETH-USD",
  "timeframe": "4h",
  "type": "text",
  "data": { "text": "Breakout zone", "price": 3800, "time": "2025-06-01T00:00:00Z", "color": "#ffaa00", "fontSize": 14 },
  "origin": "ai"
}'

# Bulk create multiple annotations
./scripts/dwlf-api.sh POST /annotations/bulk '{
  "annotations": [
    { "symbol": "BTC-USD", "timeframe": "1d", "type": "hline", "data": { "price": 100000, "color": "#ff0000", "label": "Resistance" }, "origin": "ai" },
    { "symbol": "BTC-USD", "timeframe": "1d", "type": "hline", "data": { "price": 92000, "color": "#00ff00", "label": "Support" }, "origin": "ai" }
  ]
}'

# List annotations for a symbol
./scripts/dwlf-api.sh GET "/annotations?symbol=BTC-USD&timeframe=1d"

# Update an annotation (merges data — only changes specified fields)
./scripts/dwlf-api.sh PUT /annotations/abc123 '{ "data": { "color": "#ff0000" } }'
```

## Trade Plan & Position Sizing Examples

```bash
# Calculate position size
./scripts/dwlf-api.sh POST /tools/position-size '{
  "accountSize": 10000,
  "riskPercent": 2,
  "entryPrice": 95000,
  "stopLoss": 93000,
  "symbol": "BTC-USD"
}'

# Create a trade plan
./scripts/dwlf-api.sh POST /trade-plans '{
  "symbol": "BTC-USD",
  "direction": "long",
  "entryPrice": 95000,
  "stopLoss": 93000,
  "takeProfit": 100000,
  "notes": "Bounce off key support with RSI divergence"
}'
```

## Symbol Format

- Crypto: `BTC-USD`, `ETH-USD`, `SOL-USD` (always with `-USD` suffix)
- Stocks/ETFs: `TSLA`, `NVDA`, `META`, `MARA`, `RIOT`
- Forex: `GBP-USD`, `EUR-USD`

If user says "BTC" → use `BTC-USD`. If "TSLA" → use `TSLA`.

## Core Endpoints

### Market Data
| Method | Path | Description |
|--------|------|-------------|
| GET | `/market-data/{symbol}?interval=1d&limit=50` | OHLCV candles |
| GET | `/market-data/symbols` | List all tracked symbols |
| GET | `/support-resistance/{symbol}` | S/R levels with scores |
| GET | `/chart-indicators/{symbol}?interval=1d` | All indicators (RSI, EMA, MACD, etc.) |
| GET | `/trendlines/{symbol}` | Auto-detected trendlines |
| GET | `/events?symbol={symbol}&limit=20` | System events (breakouts) |
| GET | `/events?type=custom_event&scope=user&symbol={symbol}&days=30` | User's custom events (wcl, dss, reversals etc.) |

### Chart Annotations
| Method | Path | Description |
|--------|------|-------------|
| GET | `/annotations?symbol={symbol}&timeframe={tf}` | List annotations |
| POST | `/annotations` | Create annotation (hline, text, trendline, rectangle, channel) |
| PUT | `/annotations/{annotationId}` | Update annotation (merges data fields) |
| DELETE | `/annotations/{annotationId}` | Delete annotation |
| POST | `/annotations/bulk` | Bulk create annotations |

### Trade Plans
| Method | Path | Description |
|--------|------|-------------|
| GET | `/trade-plans` | List trade plans |
| GET | `/trade-plans/{planId}` | Get trade plan |
| POST | `/trade-plans` | Create trade plan |
| PUT | `/trade-plans/{planId}` | Update trade plan |
| DELETE | `/trade-plans/{planId}` | Delete trade plan |
| POST | `/trade-plans/{planId}/duplicate` | Duplicate trade plan |

### Position Sizing
| Method | Path | Description |
|--------|------|-------------|
| POST | `/tools/position-size` | Calculate position size from risk params |

### User Settings
| Method | Path | Description |
|--------|------|-------------|
| GET | `/user/settings` | Get user settings |
| PUT | `/user/settings` | Update user settings |
| DELETE | `/user/settings/{settingKey}` | Delete a setting |

### Strategies & Signals
| Method | Path | Description |
|--------|------|-------------|
| GET | `/visual-strategies` | List user's strategies |
| GET | `/visual-strategies/{id}` | Strategy details |
| POST | `/visual-strategies` | Create strategy |
| PUT | `/visual-strategies/{id}` | Update strategy |
| GET | `/user/trade-signals/active` | Active trade signals |
| GET | `/user/trade-signals/recent?limit=20` | Recent signals |
| GET | `/user/trade-signals/stats` | Signal performance stats |
| GET | `/user/trade-signals/symbol/{symbol}` | Signals for a symbol |

### Backtesting
| Method | Path | Description |
|--------|------|-------------|
| POST | `/backtests` | Trigger backtest (async) |
| GET | `/backtests` | List backtests |
| GET | `/backtests/summary` | Backtest summary |
| GET | `/backtests/{requestId}` | Get backtest status |
| GET | `/backtests/{requestId}/results` | Get backtest results |
| DELETE | `/backtests/{requestId}` | Delete a backtest |

Backtests are async — POST triggers, then poll GET until `status: "completed"`.
- Body: `{ strategyId, symbols: ["BTC-USD"], startDate: "2025-01-01", endDate: "2026-01-30" }`
- Note: `symbols` is an **array**, not `symbol` (singular).

### Portfolio & Trades
| Method | Path | Description |
|--------|------|-------------|
| GET | `/portfolios` | List portfolios |
| GET | `/portfolios/{id}` | Portfolio details + holdings |
| GET | `/trades?status=open` | List trades |
| POST | `/trades` | Log a new trade |
| PUT | `/trades/{id}` | Update trade |
| GET | `/trade-plans` | List trade plans |

### Watchlist
| Method | Path | Description |
|--------|------|-------------|
| GET | `/watchlist` | Get watchlist |
| POST | `/watchlist` | Add symbol (`{"symbol":"BTC-USD"}`) |
| DELETE | `/watchlist/{symbol}` | Remove symbol |

### Custom Events
| Method | Path | Description |
|--------|------|-------------|
| GET | `/custom-events` | List custom events |
| POST | `/custom-events` | Create custom event |
| GET | `/custom-events/{id}` | Event details |

### Custom Event Symbol Activation
| Method | Path | Description |
|--------|------|-------------|
| POST | `/custom-event-symbols/:eventId/enable-all` | Bulk activate symbols for an event |
| POST | `/custom-event-symbols/:eventId/disable-all` | Bulk deactivate symbols for an event |
| GET | `/custom-event-symbols/event/:eventId` | Get active symbols for an event |
| GET | `/custom-event-symbols` | List all event-symbol associations |

### Strategy Symbol Activation
| Method | Path | Description |
|--------|------|-------------|
| POST | `/strategy-symbols/:strategyId/enable-all` | Bulk activate symbols for a strategy |
| POST | `/strategy-symbols/:strategyId/disable-all` | Bulk deactivate symbols for a strategy |
| GET | `/strategy-symbols/strategy/:strategyId` | Get active symbols for a strategy |
| GET | `/strategy-symbols` | List all strategy-symbol associations |

### AI Summaries
| Method | Path | Description |
|--------|------|-------------|
| GET | `/ai/dashboard` | Full account overview: watchlist, signals, trades, portfolios, strategies, events |
| GET | `/ai/symbol-brief/{symbol}` | Single-symbol snapshot: price, candles, indicators, S/R, events, signals |
| GET | `/ai/strategy-performance` | All strategies with signal stats, win rate, P&L breakdowns |

> 💡 **Use these first!** The AI summary endpoints are pre-aggregated for AI consumption. When a user asks "how's BTC?" or "what's going on?", hit these before making multiple individual calls.

### Evaluations
| Method | Path | Description |
|--------|------|-------------|
| POST | `/evaluations` | Trigger evaluation run |
| GET | `/evaluations/{id}` | Get evaluation results |

## Symbol Activation (Required After Creation)

> ⚠️ **IMPORTANT:** Creating a custom event or strategy does **NOT** automatically activate it for any symbols. After creation, you **MUST** ask the user which symbols to activate it for, then call the enable endpoint. Without this step, the event/strategy will **not fire or generate signals**.

### Workflow: Custom Events
1. Create the event → `POST /custom-events`
2. Compile the event → `POST /custom-events/{id}/compile`
3. **Ask the user** which symbols to activate for
4. **Activate symbols** → `POST /custom-event-symbols/{eventId}/enable-all` with `{ "symbols": ["BTC-USD", "ETH-USD"] }`

### Workflow: Strategies
1. Create the strategy → `POST /visual-strategies`
2. Compile the strategy → `POST /visual-strategies/{id}/compile`
3. **Ask the user** which symbols to activate for
4. **Activate symbols** → `POST /strategy-symbols/{strategyId}/enable-all` with `{ "symbols": ["BTC-USD", "ETH-USD"] }`

### Editing Events or Strategies

> ⚠️ **Any update to a custom event or strategy requires recompilation!**
> The evaluator runs the **compiled** output, not the visual graph. If you update nodes, edges, conditions, or parameters without recompiling, the changes have **no effect**.

- After editing an event: `POST /custom-events/{id}/compile`
- After editing a strategy: `POST /visual-strategies/{id}/compile`

Always recompile immediately after any `PUT` update call.

### Checking Active Symbols
- Event symbols: `GET /custom-event-symbols/event/{eventId}`
- Strategy symbols: `GET /strategy-symbols/strategy/{strategyId}`
- All activations: `GET /custom-event-symbols` and `GET /strategy-symbols` (query: `?activeOnly=true`)

### Deactivating Symbols
- Event: `POST /custom-event-symbols/{eventId}/disable-all` with `{ "symbols": [...] }`
- Strategy: `POST /strategy-symbols/{strategyId}/disable-all` with `{ "symbols": [...] }`

## Response Formatting

When presenting data to users:

**Market overview:** Show price, % change, key S/R levels, and any recent events.

**Signals:** Show symbol, direction, entry, stop loss, confidence score, strategy name.

**S/R levels:** Sort by score (strongest first), show level and touch count.

**Backtests:** Show trade count, win rate, total return, Sharpe ratio, best/worst trades.

## Available Indicators

EMA (multiple periods), SMA, RSI, MACD, Bollinger Bands, DSS (Double Smoothed Stochastic),
Stochastic RSI, ATR, ADX, OBV, Volume Profile, Ichimoku Cloud, Fibonacci Retracement,
Support/Resistance, Trendlines, Candlestick Patterns, SMC (Order Blocks, FVGs, BOS/ChoCH).

## Academy

DWLF Academy is a CDN-hosted collection of educational content (15 tracks, 60+ lessons) covering indicators, events, strategies, charting, and more. No auth required.

Use academy tools to read lesson content and understand DWLF concepts:
- `dwlf_list_academy_tracks` — browse all tracks and lessons
- `dwlf_search_academy` — search by keyword
- `dwlf_get_academy_lesson` — read a specific lesson (markdown)

When a user asks "how does X work in DWLF?" or "what is DSS?", check the academy first — it likely has a lesson explaining it.

## Detailed Reference

- **API endpoints** (params, response shapes): read `references/api-endpoints.md`
- **Strategy builder** (node types, edge wiring, examples): read `references/strategy-builder.md`
