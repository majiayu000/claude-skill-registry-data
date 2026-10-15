---
name: aster-trading
description: Aster DEX trading skill for futures, spot, and market data via MCP tools
keywords: trading, crypto, DeFi, perpetuals, futures, spot, Aster DEX, market data, orders, positions, leverage
---

# Aster DEX Trading Skill

Aster DEX is a next-generation perpetual futures and spot exchange backed by YZi Labs. This skill provides trading capabilities through the `aster` MCP server.

## Available MCP Tools

### Market Data (no auth required)
| Tool | Description |
|------|-------------|
| `ping` | Test Aster API connectivity |
| `get_ticker` | 24h ticker / latest price for a futures symbol |
| `get_order_book` | Order book depth (bids/asks) |
| `get_klines` | Candlestick/K-line data (1m, 5m, 1h, 4h, 1d) |
| `get_funding_rate` | Current funding rate and mark price |
| `get_funding_info` | Funding rate configuration |
| `get_exchange_info` | Exchange rules and contract specifications |
| `get_spot_ticker` | 24h spot ticker |
| `get_spot_price` | Latest spot price |
| `get_spot_order_book` | Spot order book depth |
| `get_spot_klines` | Spot candlestick data |
| `get_spot_exchange_info` | Spot trading rules |

### Account (requires configured account)
| Tool | Description |
|------|-------------|
| `get_balance` | Futures account balance |
| `get_positions` | Open positions (optionally filtered by symbol) |
| `get_account_info` | Account info with position summary |
| `get_account_v4` | Full account info (assets + positions) |
| `get_income` | PnL and fee flow (TRANSFER, REALIZED_PNL, FUNDING_FEE, COMMISSION) |
| `get_commission_rate` | Trading fee rate for a symbol |
| `get_leverage_bracket` | Leverage tier brackets |
| `get_spot_account` | Spot account balances (free/locked) |

### Futures Orders
| Tool | Description |
|------|-------------|
| `create_order` | Place order (LIMIT, MARKET, STOP, STOP_MARKET) |
| `cancel_order` | Cancel by order_id or client_order_id |
| `cancel_all_orders` | Cancel all open orders for a symbol |
| `get_order` | Query single order |
| `get_open_orders` | List current open orders |
| `get_all_orders` | Order history |
| `get_my_trades` | Trade/fill history |

### Spot Orders
| Tool | Description |
|------|-------------|
| `create_spot_order` | Place spot order |
| `cancel_spot_order` | Cancel spot order |
| `cancel_spot_all_orders` | Cancel all spot orders for a symbol |
| `get_spot_order` | Query spot order |
| `get_spot_open_orders` | List open spot orders |
| `get_spot_all_orders` | Spot order history |
| `get_spot_my_trades` | Spot trade history |
| `get_spot_transaction_history` | Spot transaction flow |
| `get_spot_commission_rate` | Spot fee rate |

### Position & Risk Management
| Tool | Description |
|------|-------------|
| `set_leverage` | Set leverage multiplier for a symbol |
| `set_margin_mode` | Set ISOLATED or CROSSED margin |
| `transfer_funds` | Transfer between spot and futures (type 1=spot->futures, 2=futures->spot) |
| `transfer_spot_futures` | Spot-futures transfer (SPOT_FUTURE or FUTURE_SPOT) |

### System
| Tool | Description |
|------|-------------|
| `get_server_info` | MCP server info, configured accounts, tool count |

## Setup

API keys are managed exclusively through the encrypted config:

```bash
# Configure HMAC account
aster-mcp config

# Configure EIP-712 (V3) account
aster-mcp config --account-id main --auth-type v3

# List configured accounts
aster-mcp list

# Test connectivity
aster-mcp test main
```

Keys are stored with Fernet encryption in `~/.config/aster-mcp/`.

## Risk & Safety Rules

**CRITICAL: These rules are mandatory for all trading operations.**

1. **User confirmation required**: ALWAYS confirm with the user before placing ANY order. Display the full order details (symbol, side, type, quantity, price, leverage) and ask for explicit approval.

2. **Position size disclosure**: Before executing, show:
   - Position size in USD equivalent
   - Current leverage setting
   - Estimated liquidation price (if available)
   - Current account balance and margin usage

3. **Leverage warnings**:
   - Aster supports up to 1,001x leverage
   - For leverage > 10x: note elevated risk
   - For leverage > 20x: display explicit warning about liquidation risk
   - For leverage > 50x: strongly advise against unless user is experienced
   - For leverage > 100x: refuse unless user explicitly confirms understanding of extreme risk

4. **Never auto-execute**: No order placement without user seeing a preview and confirming.

5. **Rate limits**: Respect Aster API rate limits. If receiving 429 responses, back off and inform the user.

## Security Constraints

- API keys are managed ONLY through `aster-mcp config` (Fernet encrypted)
- NEVER log, display, or output full API keys or secrets
- NEVER commit credentials to git
- NEVER store API keys in plain text files
- Config directory: `~/.config/aster-mcp/` (encrypted)

## Common Workflows

### Check a price
```
1. Call get_ticker with symbol="BTCUSDT"
2. Display: last price, 24h change %, 24h volume
```

### Place a limit buy order
```
1. Call get_ticker to show current price
2. Call get_balance to show available margin
3. Present order preview: symbol, side=BUY, type=LIMIT, quantity, price
4. Wait for user confirmation
5. Call create_order with confirmed parameters
6. Display order result (orderId, status, filled quantity)
```

### Close a position
```
1. Call get_positions to show open positions
2. Identify the position to close
3. Create a closing order (opposite side, reduce_only=true)
4. Wait for user confirmation
5. Execute and display result
```

### Check portfolio
```
1. Call get_balance for margin/PnL overview
2. Call get_positions for open positions
3. Call get_open_orders for pending orders
4. Present consolidated portfolio view
```

## Symbol Format

Symbols accept both formats and are normalized internally:
- `BTCUSDT` or `BTC/USDT` -> `BTCUSDT`
- `ETHUSDT` or `ETH/USDT` -> `ETHUSDT`

## API Base URLs

| Type | URL |
|------|-----|
| Futures REST | `https://fapi.asterdex.com` |
| Spot REST | `https://sapi.asterdex.com` |
| WebSocket | `wss://fstream.asterdex.com` |

## ML-Informed Trading Patterns

### Signal Generation Workflow
```
1. Fetch candles: get_klines(symbol, interval="1h", limit=500)
2. Calculate indicators: RSI, MACD, Bollinger Bands, ATR
3. Run ML model: feature engineering → prediction → confidence score
4. Generate signal: BUY/SELL/HOLD with confidence (0.0-1.0)
5. Position sizing: Kelly criterion or fixed fractional (see finance-ml skill)
6. Risk check: get_balance() + get_positions() → verify margin availability
7. Present to user with full details (MANDATORY confirmation)
8. Execute if confirmed: create_order(...)
```

### Key Technical Indicators for Crypto
| Indicator | Bullish Signal | Bearish Signal |
|-----------|---------------|----------------|
| RSI(14) | Below 30 (oversold) | Above 70 (overbought) |
| MACD | Signal line crossover up | Signal line crossover down |
| Bollinger Bands | Price touches lower band | Price touches upper band |
| Funding Rate | Negative (shorts paying) | Very positive (longs paying) |
| Volume | Increasing on uptrend | Increasing on downtrend |

### Risk Management Integration
- Always check funding rate before entering perpetual positions
- Use ATR-based stop losses: stop = entry ± (ATR × multiplier)
- Maximum position size: never risk more than 2% of account per trade
- Correlation check: don't hold multiple highly correlated positions

### Cross-References
- **finance-ml** skill: ML models, feature engineering, risk metrics, backtesting
- **FINANCE_ML_STACK.md**: Comprehensive financial ML reference
