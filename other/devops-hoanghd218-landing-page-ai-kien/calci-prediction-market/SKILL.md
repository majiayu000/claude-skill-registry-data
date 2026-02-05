---
name: calci-prediction-market
description: Context and working knowledge for Calci’s prediction-market domain, which is powered by Kalshi. Use this skill whenever the user asks about Calci prediction markets, Kalshi markets, tickers, order books, pricing, settlement, or the Kalshi API/WebSocket.
allowed-tools: Read, Grep, Glob
---
# Calci Prediction Market (Kalshi)

Calci’s prediction-market layer is built on **Kalshi**. This skill provides the domain model, trading mechanics, and API conventions you need to reason about Calci/Kalshi data and to explain it clearly to users.

## Core Mental Model

1. **Binary event contracts**  
   - Every tradable contract is **Yes/No** on a real‑world outcome.  
   - A winning side pays **$1**, losing side pays **$0**.  
   - Prices between **$0.01–$0.99** represent implied probability.

2. **Implied probability**  
   - If a Yes contract trades at **$0.74**, the market implies ~**74%** chance of Yes.  
   - No price is complementary (roughly **1 − Yes**, ignoring fees/spread).

3. **Fully collateralized**  
   - Users pay maximum loss up‑front. No margin/leverage.  
   - You can never lose more than you spend on contracts.

## Data Hierarchy (Kalshi → Calci)

Kalshi uses a strict hierarchy:

- **Series** → template for recurring markets (shared rules/settlement).  
- **Event** → specific instance within a series (a real‑world occurrence).  
- **Market** → single binary contract within an event (one Yes/No outcome).

Calci mirrors these objects. When you see “market” in Calci UI, clarify whether it’s an **event page** (container) or a **specific market outcome** (binary leg).

## Market Objects: What Fields Mean

When interpreting Calci/Kalshi market JSON:

- **ticker**: unique identifier (string).  
- **event_ticker / series_ticker**: parent identifiers.  
- **title / subtitle**: human‑readable question and clarification.  
- **yes_bid / yes_ask** (cents) and *_dollars*: best prices to buy/sell Yes.  
- **no_bid / no_ask**: best prices to buy/sell No.  
- **last_price**: last traded Yes price.  
- **volume / volume_24h / open_interest**: activity and outstanding contracts.  
- **open_time / close_time / expiration_time**: lifecycle timestamps.  
- **status**: initialized, active/open, closed, settled.  
- **result / settlement_value**: set after resolution.

## Trading Mechanics to Explain

- **Order book** on both Yes and No sides.  
- **Quick/market order** crosses current spread for immediate fill.  
- **Limit order** rests at a chosen price; may add liquidity.  
- **Closing a position** = taking the opposite side later (sell Yes or buy No).  
- **Mutually exclusive events** contain multiple markets where at most one can settle Yes.

Fees on Kalshi are **variable/quadratic**, roughly a percent of potential profit; maker orders may be discounted.

## Settlement & Resolution

- Each series defines **official settlement sources** and rules.  
- Markets usually close before the strike/decision time, then settle after confirmation.  
- Some markets can resolve early if `can_close_early` is true.

When asked “how does this resolve?”, reference the series rules and settlement source, then restate in plain language.

## API Conventions You Should Use

Public data (no auth needed):

- `GET /series`  
- `GET /events` (events include their markets)  
- `GET /markets`  
- `GET /market/{ticker}`  
- `GET /market/orderbook`  
- `GET /market/candlesticks`  
- `GET /market/trades`  
- `GET /exchange/status`

Trading/account (auth required):

- `POST /orders`, `DELETE /orders/{id}`, `GET /orders/{id}`  
- `POST /order-groups` and related order‑group endpoints  
- `GET /portfolio/balance`, `GET /portfolio/positions`, `GET /portfolio/fills`

Auth uses an API key id plus RSA signature headers:

- `KALSHI-ACCESS-KEY`  
- `KALSHI-ACCESS-TIMESTAMP`  
- `KALSHI-ACCESS-SIGNATURE`

Real‑time updates arrive via **WebSocket** subscriptions to tickers.

## How to Apply This Skill When Answering

1. **Map Calci terms → Kalshi terms** if the user is vague.  
2. **Always distinguish Series/Event/Market** and restate which level you’re discussing.  
3. **Convert price to probability** explicitly when helpful.  
4. **Explain both sides (Yes/No) and spreads** when discussing pricing or order books.  
5. **Cite rules + settlement source** for resolution questions.  
6. **Stay neutral**: describe mechanics and risks; don’t give financial advice.

## Examples

- “This Calci market is a Kalshi **market ticker**. It’s a binary contract paying $1 if Yes. At $0.62, the market implies ~62% Yes probability.”
- “The event is **mutually exclusive**, so each candidate outcome is a separate market. Exactly one can settle Yes.”
- “To get real‑time prices, subscribe to the market tickers on the Kalshi WebSocket; Calci mirrors those updates.”

For more detail, see [reference.md](reference.md).

