---
name: broker-integration
description: |
  Connect Claude to Indian brokers and use them safely: official MCP servers for Groww, Zerodha
  Kite, Dhan, Upstox, Fyers and Kotak Neo (endpoints, auth, read vs order capabilities as of Oct 2026),
  tool discovery and capability mapping, saving candles for the analysis scripts, a mandatory
  order-confirmation protocol, SEBI retail-algo/static-IP rules, and data fallbacks (yfinance, CSV).

  Use when the user asks to connect or set up Groww/Zerodha/Kite/Dhan/Upstox/Fyers/Angel One, "fetch my
  holdings/positions", "get live price", "place/modify/cancel an order", "set a GTT", "why was my order
  rejected", or when another skill needs live data.
---

# Broker Integration (India)

## Which broker does what (official MCP servers, checked Oct 2026)

| Broker | Endpoint | Auth | Can place orders? | Read access |
|---|---|---|---|---|
| **Groww** (largest by active clients, ~29% share) | `https://mcp.groww.in/mcp` | OAuth; token lasts a day | **Yes**: buy, limit and stop-loss. Sells need DDPI | Holdings, positions, P&L, candles (stocks and F&O) |
| **Zerodha Kite** | `https://mcp.kite.trade/mcp` | Kite login with 2FA | Hosted: **GTT only**. The open-source server (github.com/zerodha/kite-mcp-server) has order tools when self-hosted with your API keys | Quotes, LTP, OHLC, historical, instruments, holdings, positions, margins, MF holdings, orders and trades |
| **Dhan** | `https://mcp.dhan.co/mcp` | OAuth | **Yes**, including Super Orders | Funds, holdings, positions, order and trade book, candles. Live quotes and option chain need the Data API (₹499 + tax a month) |
| **Upstox** | `https://mcp.upstox.com/mcp` | OAuth, renewed daily | **No** (read-only). Upstox's separate Agent Skill (Python SDK) can trade | Holdings, orders, positions, MFs, funds |
| **Fyers** | `https://mcp.fyers.in/mcp` | Fyers login | No (watchlists and alerts only) | Funds, holdings, positions, orders, GTTs, option chain, history |
| **Kotak Neo** | `https://neo.kotaksecurities.com/mcp-server/mcp` | Client code + QR in app | No | Holdings, orders, positions, live prices |
| **Angel One** | No official server | — | Community servers only | Use SmartAPI directly |

Capabilities change often. After connecting, list the actual tools and trust that list over this table.

## Connect (Claude Code)

```bash
claude mcp add --transport http groww https://mcp.groww.in/mcp
claude mcp add --transport http kite  https://mcp.kite.trade/mcp
claude mcp add --transport http dhan  https://mcp.dhan.co/mcp
claude mcp add --transport http upstox https://mcp.upstox.com/mcp
# then run /mcp inside Claude Code to complete the browser login (OAuth)
```

Or commit a project `.mcp.json` (see `references/brokers.md` for more variants):

```json
{
  "mcpServers": {
    "groww": { "type": "http", "url": "https://mcp.groww.in/mcp" },
    "kite":  { "type": "http", "url": "https://mcp.kite.trade/mcp" }
  }
}
```

In Claude Desktop or claude.ai, add the URL under Settings → Connectors → Add custom connector. Older
clients can bridge with `npx mcp-remote <url>`.

## Capability map (use whatever the connected server exposes)

| Need | Kite tool | Groww tool (names as published by the community; confirm in the tool list) |
|---|---|---|
| Resolve symbol / instrument | `search_instruments` | `search_stock_and_others_symbol` |
| Live quote / depth | `get_quotes`, `get_ltp`, `get_ohlc` | `get_quotes_and_depth`, `get_ltp` |
| Candles | `get_historical_data` | `fetch_historical_candle_data` |
| Holdings / positions | `get_holdings`, `get_positions` | `get_equity_portfolio_holdings`, positions tool |
| Margins / funds | `get_margins` | margin or funds tool |
| Orders / trades | `get_orders`, `get_trades`, `get_order_history` | order book tools |
| GTT | `get_gtts`, `place_gtt_order`, `modify_gtt_order`, `delete_gtt_order` | — |

**Feeding the scripts:** write the candle response to a JSON file (the list of
`[timestamp, open, high, low, close, volume]` or a list of dicts), then run
`python3 ../technical-analysis/scripts/ta.py summary --candles candles.json --symbol X`. Compute
indicators with `ta.py`, not by eyeballing a tool's indicator output. That keeps every broker's data
consistent.

**Symbols:** always resolve F&O contracts through the instrument search. Formats differ by broker and
between weekly and monthly contracts. Kite, for example, uses `NIFTY26NOV23000CE` for monthlies and a
month-code plus day format for weeklies.

## Order protocol (mandatory)

1. **Only on an explicit request in this conversation.** Never place, modify or cancel orders from a
   loop, schedule, tip, or your own initiative.
2. **Pre-trade checks:** market open, not a holiday (`indian-market-structure`); correct exchange,
   symbol and series; quantity is a lot multiple and below the freeze limit; price inside the circuit
   band; funds and margin available; sizing within `position-sizing` limits; event risk noted.
3. **Show a ticket and wait for "yes":**
   ```
   BUY 25 TCS (NSE, EQ) | CNC | LIMIT ₹3,412.50 | DAY
   Value ₹85,312 | Est. charges ₹.. | Funds available ₹..
   Stop plan: GTT SL trigger ₹3,320 / limit ₹3,300 (separate confirmation)
   Confirm? (yes / no)
   ```
4. **LIMIT by default.** Avoid market orders in options and small caps. Use SL-limit with a buffer.
   Use GTT for stops on delivery holdings.
5. **After sending:** fetch the order status, then report the order id, status, and fill price and
   quantity. On rejection, explain the reason: margin shortfall, circuit limit, DDPI/eDIS missing for a
   sell, freeze quantity, ban-period position, product not allowed, or an expired session token.
6. **Secrets:** never ask the user to paste API secrets or TOTP seeds into chat. Self-hosted servers
   read them from environment variables. Prefer read-only connections for analysis. With Kite
   self-hosting, `EXCLUDED_TOOLS` can strip order tools.

## SEBI retail algo framework (fully in force from 1 Apr 2026)

- API orders must come from a broker-registered app with a **whitelisted static IP** tied to the client.
  Dynamic IPs are rejected.
- Strategies beyond exchange order-rate thresholds must be registered algos with exchange-issued IDs.
- How brokers apply this to hosted MCP order tools is broker-specific and not well documented. For
  self-hosted API setups (Kite Connect, Upstox API, SmartAPI, Dhan API), register the static IP first.
- In practice, MCP order tools are for **manual, confirmed, one-at-a-time orders**, not automation.

## Fallbacks when no broker is connected

- `ta.py --symbol X` uses yfinance (`pip install yfinance`). It is fine for end-of-day analysis;
  intraday quotes may be delayed.
- The user can export CSV from their charting tool or paste a screenshot of prices. Ask for the date
  and time of the data.
- NSE website reports (bhavcopy, delivery data, option chain CSV) can be downloaded manually.
  nseindia.com blocks most scripted access.
