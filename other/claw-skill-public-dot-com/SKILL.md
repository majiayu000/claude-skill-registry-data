---
id: public-dot-com
name: public.com
description: Interact with your Public.com brokerage account using the Public.com API. Able to view portfolio, get stock quotes, place trades, and get account updates. To create a Public.com account head to public.com/signup.
env: ['PUBLIC_COM_SECRET', 'PUBLIC_COM_ACCOUNT_ID']
license: Apache-2.0
metadata:
  author: PublicDotCom
  source: https://github.com/PublicDotCom/claw-skill-public-dot-com
  category: "Finance"
  tags: ["investing", "stocks", "crypto", "options", "public", "finance"]
  version: "1.0"
---

# Public.com Account Manager
> **Disclaimer:** For illustrative and informational purposes only. Not investment advice or recommendations.
>
> We recommend running this skill in as isolated of an instance as possible. If possible, test the integration on a new Public account as well.

This skill allows users to interact with their Public.com brokerage account.

## Prerequisites
- **Python 3.9+** and **pip** — Required to run this skill.
- **Public.com account** — Create one at https://public.com/signup
- **Public.com API key** — Get one at https://public.com/settings/v2/api

The `publicdotcom-py` SDK is required. It will be **auto-installed** on first run, or you can install manually:
```bash
pip install publicdotcom-py
```

## Configuration

This skill uses two environment variables: `PUBLIC_COM_SECRET` (required) and `PUBLIC_COM_ACCOUNT_ID` (optional). Each is resolved from the environment:

- **Environment variable** — `PUBLIC_COM_SECRET` / `PUBLIC_COM_ACCOUNT_ID`

### API Secret (Required)
If `PUBLIC_COM_SECRET` is not set:
- Tell the user: "I need your Public.com API Secret. You can find this in your Public.com developer settings at https://public.com/settings/v2/api."
- Once provided, instruct them to set it as an environment variable: `export PUBLIC_COM_SECRET=[VALUE]`

### Default Account ID (Optional)
If the user wants to set a default account for all requests:
- Instruct them to set: `export PUBLIC_COM_ACCOUNT_ID=[VALUE]`
- This eliminates the need to specify `--account-id` on each command.

## Error Recovery

If any command exits with an error, follow these steps before giving up:

- **`PUBLIC_COM_SECRET` not set** — Ask the user for their API secret and instruct them to run `export PUBLIC_COM_SECRET=[VALUE]`, then retry.
- **`No account ID provided`** — Run `python3 scripts/get_accounts.py` to retrieve the account ID, then retry the original command with `--account-id [ID]`.
- **Authentication / 401 error** — Tell the user their API key may be expired or invalid, and direct them to https://public.com/settings/v2/api to generate a new one.
- **Network / connection error** — Ask the user to check their internet connection and retry.
- **Any other unexpected error** — Show the error message to the user and ask them how they'd like to proceed.

Never silently retry the same failing command more than once.

## Available Commands

### Check Setup
Run this automatically the **first time** the user interacts with this skill, or whenever they ask "is everything configured?", "check my setup", or "verify my API key":
1. Execute `python3 scripts/check_setup.py`
2. If it exits successfully, proceed normally.
3. If it fails, follow the printed instructions to resolve the issue before continuing.

### Get Accounts
When the user asks to "get my accounts", "list accounts", or "show my Public.com accounts":
1. Execute `python3 scripts/get_accounts.py`
2. Report the account IDs and types back to the user.
3. Remember the account IDs returned — use them automatically for any subsequent commands in the same session that require `--account-id`.

### Get Portfolio
When the user asks to "get my portfolio", "show my holdings", or "what's in my account":
1. If `PUBLIC_COM_ACCOUNT_ID` is set, execute `python3 scripts/get_portfolio.py` (no arguments needed).
2. If not set and you don't know the user's account ID, first run `get_accounts.py` to retrieve it.
3. Execute `python3 scripts/get_portfolio.py --account-id [ACCOUNT_ID]`
4. Report the portfolio summary (equity, buying power, positions) back to the user.

### Get Orders
When the user asks to "get my orders", "show my orders", "active orders", or "pending orders":
1. If `PUBLIC_COM_ACCOUNT_ID` is set, execute `python3 scripts/get_orders.py` (no arguments needed).
2. If not set and you don't know the user's account ID, first run `get_accounts.py` to retrieve it.
3. Execute `python3 scripts/get_orders.py --account-id [ACCOUNT_ID]`
4. Report the active orders with their details (symbol, side, type, status, quantity, prices) back to the user.

### Get History
When the user asks to "get my history", "show my transactions", "transaction history", "trade history", or wants to see past account activity:

**Optional parameters:**
- `--type`: Filter by transaction type (TRADE, MONEY_MOVEMENT, POSITION_ADJUSTMENT)
- `--limit`: Limit the number of transactions returned

**Examples:**

Get all transaction history:
```bash
python3 scripts/get_history.py
```

Get only trades:
```bash
python3 scripts/get_history.py --type TRADE
```

Get only money movements (deposits, withdrawals, dividends, fees):
```bash
python3 scripts/get_history.py --type MONEY_MOVEMENT
```

Get last 10 transactions:
```bash
python3 scripts/get_history.py --limit 10
```

With explicit account ID:
```bash
python3 scripts/get_history.py --account-id YOUR_ACCOUNT_ID
```

**Workflow:**
1. If `PUBLIC_COM_ACCOUNT_ID` is not set and you don't know the user's account ID, first run `get_accounts.py` to retrieve it.
2. Execute: `python3 scripts/get_history.py [OPTIONS]`
3. Report the transaction history grouped by type (Trades, Money Movements, Position Adjustments).
4. Include relevant details like symbol, quantity, net amount, fees, and timestamps.

**Transaction Types:**
- **TRADE**: Buy/sell transactions for equities, options, and crypto
- **MONEY_MOVEMENT**: Deposits, withdrawals, dividends, fees, and cash adjustments
- **POSITION_ADJUSTMENT**: Stock splits, mergers, and other position changes

### Get Quotes
When the user asks to "get a quote", "what's the price of", "check the price", or wants stock/crypto prices:

**Format:** `SYMBOL` or `SYMBOL:TYPE` (TYPE defaults to EQUITY)

**Examples:**

Single equity quote (uses default account):
```bash
python3 scripts/get_quotes.py AAPL
```

Multiple equity quotes:
```bash
python3 scripts/get_quotes.py AAPL GOOGL MSFT
```

Mixed instrument types:
```bash
python3 scripts/get_quotes.py AAPL:EQUITY BTC:CRYPTO
```

Option quote:
```bash
python3 scripts/get_quotes.py AAPL260320C00280000:OPTION
```

With explicit account ID:
```bash
python3 scripts/get_quotes.py AAPL --account-id YOUR_ACCOUNT_ID
```

**Workflow:**
1. If `PUBLIC_COM_ACCOUNT_ID` is not set and you don't know the user's account ID, first run `get_accounts.py` to retrieve it.
2. Parse the user's request for symbol(s) and type(s).
3. Execute: `python3 scripts/get_quotes.py [SYMBOLS...] [--account-id ACCOUNT_ID]`
4. Report the quote information (last price, bid, ask, volume, etc.) back to the user.

### Get Instruments
When the user asks to "list instruments", "what can I trade", "show available stocks", or wants to see tradeable instruments:

**Optional parameters:**
- `--type`: Instrument types to filter (EQUITY, OPTION, CRYPTO). Defaults to EQUITY.
- `--trading`: Trading status filter (BUY_AND_SELL, BUY_ONLY, SELL_ONLY, NOT_TRADABLE)
- `--search`: Search by symbol or name
- `--limit`: Limit number of results

**Examples:**

List all equities (default):
```bash
python3 scripts/get_instruments.py
```

List equities and crypto:
```bash
python3 scripts/get_instruments.py --type EQUITY CRYPTO
```

List only tradeable instruments:
```bash
python3 scripts/get_instruments.py --type EQUITY --trading BUY_AND_SELL
```

Search for specific instruments:
```bash
python3 scripts/get_instruments.py --search AAPL
```

Limit results:
```bash
python3 scripts/get_instruments.py --limit 50
```

**Workflow:**
1. Parse the user's request for any filters (type, trading status, search term).
2. Execute: `python3 scripts/get_instruments.py [OPTIONS]`
3. Report the available instruments with their trading status back to the user.

### Get Instrument
When the user asks to "get instrument details", "show instrument info", "what are the details for AAPL", or wants to see details for a specific instrument:

**Required parameters:**
- `--symbol`: The ticker symbol (e.g., AAPL, BTC)

**Optional parameters:**
- `--type`: Instrument type (EQUITY, OPTION, CRYPTO). Defaults to EQUITY.

**Examples:**

Get equity instrument details:
```bash
python3 scripts/get_instrument.py --symbol AAPL
```

Get crypto instrument details:
```bash
python3 scripts/get_instrument.py --symbol BTC --type CRYPTO
```

**Workflow:**
1. Parse the user's request for the symbol and optional type.
2. Execute: `python3 scripts/get_instrument.py --symbol [SYMBOL] [--type TYPE]`
3. Report the instrument details (trading status, fractional trading, option trading) back to the user.

### Get Option Expirations
**This skill CAN list all available option expiration dates for any symbol.**

When the user asks to "get option expirations", "list expirations", "show expiration dates", "when do options expire", or wants to know what option expiration dates are available for a stock:
1. Execute `python3 scripts/get_option_expirations.py [SYMBOL]`
2. Report the available expiration dates to the user.

Common user phrasings:
- "get option expirations for AAPL"
- "what are the option expiration dates for Google"
- "when do TSLA options expire"
- "show me expiration dates for SPY options"
- "list available expirations for MSFT"
- "can you get the options expirations for Apple"
- "what options dates are available for NVDA"

**Required parameters:**
- `symbol`: The underlying symbol (e.g., AAPL, GOOGL, TSLA, SPY). Convert company names to ticker symbols.

**Examples:**

```bash
python3 scripts/get_option_expirations.py AAPL
python3 scripts/get_option_expirations.py GOOGL
python3 scripts/get_option_expirations.py TSLA
python3 scripts/get_option_expirations.py SPY
```

**Common company name to symbol mappings:**
- Apple = AAPL
- Google/Alphabet = GOOGL
- Tesla = TSLA
- Microsoft = MSFT
- Amazon = AMZN
- Nvidia = NVDA
- Meta/Facebook = META

**Workflow:**
1. Extract the symbol from the user's request. Convert company names to ticker symbols.
2. Execute: `python3 scripts/get_option_expirations.py [SYMBOL]`
3. Report the available expiration dates to the user.
4. If they want to see the option chain next, use the expiration date with `get_option_chain.py`.

### Get Option Greeks
When the user asks for "option greeks", "delta", "gamma", "theta", "vega", or wants to analyze options:

**Required parameters:**
- One or more OSI option symbols (e.g., AAPL260116C00270000)

**OSI Symbol Format:**
```
AAPL260116C00270000
^^^^------^--------
|   |     |  Strike price ($270.00)
|   |     Call (C) or Put (P)
|   Expiration (Jan 16, 2026 = 260116)
Underlying symbol
```

**Examples:**

Single option:
```bash
python3 scripts/get_option_greeks.py AAPL260116C00270000
```

Multiple options (e.g., call and put at same strike):
```bash
python3 scripts/get_option_greeks.py AAPL260116C00270000 AAPL260116P00270000
```

**Workflow:**
1. Help the user construct the OSI symbol if they provide expiration, strike, and call/put separately.
2. Execute: `python3 scripts/get_option_greeks.py [OSI_SYMBOLS...]`
3. Report the greeks (Delta, Gamma, Theta, Vega, Rho, IV) back to the user with explanations if needed.

### Get Option Chain
When the user asks for "option chain", "options for AAPL", "show me calls and puts", or wants to see available options:

**Required parameters:**
- `symbol`: The underlying symbol (e.g., AAPL)

**Optional parameters:**
- `--expiration`: Expiration date (YYYY-MM-DD). If not provided, uses the nearest expiration.
- `--list-expirations`: List available expiration dates instead of fetching the chain.

**Examples:**

List available expirations:
```bash
python3 scripts/get_option_chain.py AAPL --list-expirations
```

Get option chain for nearest expiration:
```bash
python3 scripts/get_option_chain.py AAPL
```

Get option chain for specific expiration:
```bash
python3 scripts/get_option_chain.py AAPL --expiration 2026-03-20
```

**Workflow:**
1. If the user doesn't specify an expiration, first run with `--list-expirations` to show available dates.
2. Execute: `python3 scripts/get_option_chain.py [SYMBOL] [--expiration DATE]`
3. Report the calls and puts with strike prices, bid/ask, last price, volume, and open interest.

### Set Default Account
When the user asks to "set my default account" or "use account X as default":
1. Instruct the user to set: `export PUBLIC_COM_ACCOUNT_ID=[ACCOUNT_ID]`
2. Confirm to the user that future requests will use this account by default.

### Preflight Calculation
When the user asks to "estimate order cost", "preflight an order", "what would it cost to buy", "check buying power impact", or wants to see the estimated cost and account impact before placing an order:

**Required parameters:**
- `--symbol`: The ticker symbol (e.g., AAPL, BTC, or option symbol like NVDA260213P00177500)
- `--type`: EQUITY, OPTION, or CRYPTO
- `--side`: BUY or SELL
- `--order-type`: LIMIT, MARKET, STOP, or STOP_LIMIT
- `--quantity` OR `--amount`: Number of shares/contracts OR notional dollar amount

**Conditional parameters:**
- `--limit-price`: Required for LIMIT and STOP_LIMIT orders
- `--stop-price`: Required for STOP and STOP_LIMIT orders
- `--session`: CORE (default) or EXTENDED for equity orders
- `--open-close`: OPEN or CLOSE for options orders (OPEN to open a new position, CLOSE to close existing)
- `--time-in-force`: DAY (default) or GTD (Good Till Date — requires `--expiration-time YYYY-MM-DD`, max 90 days out)

**Examples:**

Equity limit buy preflight:
```bash
python3 scripts/preflight.py --symbol AAPL --type EQUITY --side BUY --order-type LIMIT --quantity 10 --limit-price 227.50
```

Equity market sell preflight:
```bash
python3 scripts/preflight.py --symbol AAPL --type EQUITY --side SELL --order-type MARKET --quantity 10
```

Crypto buy by amount preflight:
```bash
python3 scripts/preflight.py --symbol BTC --type CRYPTO --side BUY --order-type MARKET --amount 100
```

Option contract buy preflight (opening a new position):
```bash
python3 scripts/preflight.py --symbol NVDA260213P00177500 --type OPTION --side BUY --order-type LIMIT --quantity 1 --limit-price 4.00 --open-close OPEN
```

Option contract sell preflight (closing a position):
```bash
python3 scripts/preflight.py --symbol NVDA260213P00177500 --type OPTION --side SELL --order-type LIMIT --quantity 1 --limit-price 5.00 --open-close CLOSE
```

**Workflow:**
1. Gather the order parameters from the user (symbol, type, side, order type, quantity/amount, prices if needed).
2. Execute: `python3 scripts/preflight.py [OPTIONS]`
3. Report the estimated cost, buying power impact, and any fees to the user.
4. If the user wants to proceed, use the `place_order.py` script with the same parameters.

### Place Order
When the user asks to "buy", "sell", "place an order", or "trade":

**Required parameters:**
- `--symbol`: The ticker symbol (e.g., AAPL, BTC)
- `--type`: EQUITY, OPTION, or CRYPTO
- `--side`: BUY or SELL
- `--order-type`: LIMIT, MARKET, STOP, or STOP_LIMIT
- `--quantity` OR `--amount`: Number of shares OR notional dollar amount

**Conditional parameters:**
- `--limit-price`: Required for LIMIT and STOP_LIMIT orders
- `--stop-price`: Required for STOP and STOP_LIMIT orders
- `--session`: CORE (default) or EXTENDED for equity orders
- `--open-close`: OPEN or CLOSE for options orders
- `--time-in-force`: DAY (default) or GTD (Good Till Date — requires `--expiration-time YYYY-MM-DD`, max 90 days out)

**Examples:**

Buy 10 shares of AAPL at limit price $227.50:
```bash
python3 scripts/place_order.py --symbol AAPL --type EQUITY --side BUY --order-type LIMIT --quantity 10 --limit-price 227.50
```

Sell $500 worth of AAPL at market price:
```bash
python3 scripts/place_order.py --symbol AAPL --type EQUITY --side SELL --order-type MARKET --amount 500
```

Buy crypto with extended hours:
```bash
python3 scripts/place_order.py --symbol BTC --type CRYPTO --side BUY --order-type MARKET --amount 100
```

Buy with a Good-Till-Date (GTD) order (cancels automatically on the given date if not filled):
```bash
python3 scripts/place_order.py --symbol AAPL --type EQUITY --side BUY --order-type LIMIT --quantity 10 --limit-price 220.00 --time-in-force GTD --expiration-time 2026-07-01
```

**Workflow:**
1. Gather all required information from the user (symbol, side, order type, quantity/amount, prices if needed).
2. Confirm the order details with the user before executing.
3. Execute: `python3 scripts/place_order.py [OPTIONS]`
4. Report the order ID and confirmation back to the user.
5. Remind user that order placement is asynchronous. To check status later, use `get_order.py --order-id <id>`. To block until the order fills (or reaches another terminal status), use `wait_for_fill.py --order-id <id>`.

### Cancel Order
When the user asks to "cancel order", "cancel my order", or wants to cancel a specific order:

**Required parameters:**
- `--order-id`: The order ID to cancel

**Example:**
```bash
python3 scripts/cancel_order.py --order-id 345d3e58-5ba3-401a-ac89-1b756332cc94
```

With explicit account ID:
```bash
python3 scripts/cancel_order.py --order-id 345d3e58-5ba3-401a-ac89-1b756332cc94 --account-id YOUR_ACCOUNT_ID
```

**Workflow:**
1. If the user doesn't provide an order ID, first run `get_orders.py` to show them their active orders.
2. Confirm with the user which order they want to cancel.
3. Execute: `python3 scripts/cancel_order.py --order-id [ORDER_ID]`
4. Inform the user that cancellation is asynchronous - confirm by running `get_order.py --order-id <id>`.

### Get Historical Bars
When the user asks for "historical prices", "price history", "candles", "OHLC", "bars", or "what did AAPL do last week/month/year":

**Required parameters:**
- `--symbol`: Ticker symbol (e.g., AAPL, BTC, or an OSI option symbol)
- `--period`: One of DAY, WEEK, MONTH, QUARTER, HALF_YEAR, YEAR, FIVE_YEARS, YTD, SINCE_PURCHASE

**Optional parameters:**
- `--type`: EQUITY (default), CRYPTO, OPTION, or INDEX
- `--aggregation`: Bar size override (ONE_MINUTE, FIVE_MINUTES, TEN_MINUTES, FIFTEEN_MINUTES, THIRTY_MINUTES, ONE_HOUR, ONE_DAY, ONE_WEEK, ONE_MONTH, THREE_MONTHS, SIX_MONTHS, ONE_YEAR). If omitted, the server picks a sensible default for the period.
- `--purchase-date`: Required when `--period SINCE_PURCHASE`. Format YYYY-MM-DD.

**Examples:**

One year of daily bars for AAPL:
```bash
python3 scripts/get_bars.py --symbol AAPL --period YEAR
```

One month of one-day bars:
```bash
python3 scripts/get_bars.py --symbol AAPL --period MONTH --aggregation ONE_DAY
```

One week of BTC bars:
```bash
python3 scripts/get_bars.py --symbol BTC --type CRYPTO --period WEEK
```

Bars since purchase:
```bash
python3 scripts/get_bars.py --symbol AAPL --period SINCE_PURCHASE --purchase-date 2024-01-15
```

**Workflow:**
1. Parse the user's request for symbol, time window, and optional bar size.
2. Execute: `python3 scripts/get_bars.py [OPTIONS]`
3. Report the pre-market, regular-market, and after-hours bars along with the previous close and total gain/loss summary.

### Preflight Spread
When the user wants to estimate the cost of a vertical option spread before placing it:

**Required parameters:**
- `--spread-type`: One of CALL_CREDIT, CALL_DEBIT, PUT_CREDIT, PUT_DEBIT
- `--sell`: OSI symbol of the leg to sell
- `--buy`: OSI symbol of the leg to buy
- `--quantity`: Number of spread contracts
- `--limit-price`: Net debit (for DEBIT spreads) or net credit (for CREDIT spreads) as a positive value. The SDK negates credits internally.

**Optional parameters:**
- `--time-in-force`: DAY (default) or GTD

**Spread types:**
- `CALL_CREDIT` — Bear Call Spread: sell lower-strike CALL, buy higher-strike CALL (net credit)
- `CALL_DEBIT` — Bull Call Spread: buy lower-strike CALL, sell higher-strike CALL (net debit)
- `PUT_CREDIT` — Bull Put Spread: sell higher-strike PUT, buy lower-strike PUT (net credit)
- `PUT_DEBIT` — Bear Put Spread: buy higher-strike PUT, sell lower-strike PUT (net debit)

**Example:**

```bash
python3 scripts/preflight_spread.py --spread-type CALL_DEBIT \
  --sell AAPL251219C00200000 --buy AAPL251219C00190000 \
  --quantity 1 --limit-price 3.00
```

**Workflow:**
1. Help the user pick legs (use `get_option_chain.py` and `get_option_expirations.py` if needed).
2. Execute: `python3 scripts/preflight_spread.py [OPTIONS]`
3. Report estimated cost, credit/debit, fees, and buying-power impact.
4. If the user wants to proceed, use `place_spread.py` with the same parameters.

### Place Spread
When the user wants to place a vertical option spread:

Same arguments as Preflight Spread above. Uses the OSI-direct helpers added in publicdotcom-py 0.1.11 (`place_call_credit_spread`, etc.).

**Example:**

```bash
python3 scripts/place_spread.py --spread-type PUT_CREDIT \
  --sell AAPL251219P00180000 --buy AAPL251219P00170000 \
  --quantity 1 --limit-price 2.50
```

**Workflow:**
1. Confirm all spread details with the user before executing — multi-leg orders are not easily reversible.
2. Recommend running `preflight_spread.py` first.
3. Execute: `python3 scripts/place_spread.py [OPTIONS]`
4. Report the order ID and remind the user to check order status.

### Preflight Short
When the user asks to "preflight a short", "estimate a short sale", or wants to see the impact before shorting:

**Required parameters:**
- `--symbol`: Equity symbol to short
- `--quantity`: Number of shares

**Optional parameters:**
- `--order-type`: MARKET (default), LIMIT, STOP, or STOP_LIMIT
- `--limit-price`: Required for LIMIT/STOP_LIMIT
- `--stop-price`: Required for STOP/STOP_LIMIT
- `--time-in-force`: DAY (default) or GTD
- `--session`: CORE or EXTENDED

**Example:**

```bash
python3 scripts/preflight_short.py --symbol TSLA --quantity 10 --order-type LIMIT --limit-price 245.00
```

**Workflow:**
1. Execute: `python3 scripts/preflight_short.py [OPTIONS]`
2. Report estimated proceeds, fees, and buying-power impact.
3. If the user wants to proceed, use `place_short.py` with the same parameters.

### Place Short
When the user asks to "short a stock", "open a short position", or "place a short order":

Same arguments as Preflight Short above. Uses the `place_short_order` helper added in publicdotcom-py 0.1.11. The API represents short intent as SELL + openCloseIndicator=OPEN; this helper handles that automatically.

**Example:**

```bash
python3 scripts/place_short.py --symbol TSLA --quantity 10
```

**Workflow:**
1. Confirm short-sale details with the user — shorting carries unlimited theoretical risk.
2. Recommend running `preflight_short.py` first.
3. Execute: `python3 scripts/place_short.py [OPTIONS]`
4. Report the order ID and remind the user to check order status.

### Options Strategy Guidance
When the user asks about options strategies, how to automate a strategy, which strategy to use for a given scenario, or wants help constructing multi-leg options trades:

1. Read the file `options-automation-library.md` (located in the same directory as this skill) for detailed strategy context.
2. This library contains 35+ options strategies organized by category:
   - **Single-leg strategies**: Long Call, Long Put, Covered Call, Cash-Secured Put
   - **Vertical spreads**: Bull Call, Bear Call, Bull Put, Bear Put
   - **Calendar & diagonal spreads**: Long Calendar, Diagonal Spread
   - **Straddles & strangles**: Long/Short Straddle, Long/Short Strangle
   - **Complex spreads**: Iron Condor, Iron Butterfly, Broken-Wing Butterfly, Jade Lizard, Christmas Tree
   - **Synthetic positions**: Synthetic Long/Short, Synthetic Covered Call, Conversion/Reversal
   - **Income strategies**: Wheel, Poor Man's Covered Call, Ratio Spreads
   - **Advanced/quant strategies**: Box Spread, Risk Reversal, Hedged Iron Fly, Vol Arb, Calendar Strangles
   - **Event-driven workflows**: Earnings IV Crush, Pre-Market IV Expansion, Post-Earnings Drift, Macro/OPEX Gamma
3. Each strategy includes: description, use case with event examples, where the strategy breaks, API workflow steps, and code examples using the Public.com SDK.
4. Use the shared SDK helpers (Setup, Market Data, Preflight, Multi-leg order helpers) from the library when constructing code examples.
5. When recommending a strategy, always include the "Where This Strategy Breaks" context so the user understands the risks.
6. For executable trades, map the library's code patterns to the actual scripts available in this skill:
   - Single-leg orders → `preflight.py` / `place_order.py`
   - Vertical spreads (bull/bear call/put) → `preflight_spread.py` / `place_spread.py`
   - Any other 2-6 leg combination (iron condor, butterfly, straddle, strangle, calendar, diagonal, ratio, jade lizard, etc.) → `preflight_multileg.py` / `place_multileg.py`

### Get Order Status
When the user asks to "check order status", "is my order filled", "what happened to order X", or wants the current state of a specific order:

**Required parameters:**
- `--order-id`: The order ID to look up

**Example:**
```bash
python3 scripts/get_order.py --order-id 345d3e58-5ba3-401a-ac89-1b756332cc94
```

**Workflow:**
1. Execute: `python3 scripts/get_order.py --order-id [ID]`
2. Report the order's status, filled quantity, average price, and reject reason (if any).
3. Multi-leg orders also include a per-leg breakdown.

### Wait For Fill
When the user wants to "wait until my order fills", "block until filled", or wants the agent to monitor an order through to a terminal state before doing the next step:

**Required parameters:**
- `--order-id`: UUID of the order to track

**Optional parameters:**
- `--timeout`: Max seconds to wait (default 120)
- `--poll-seconds`: Polling interval (default 1.0)
- `--fill-only`: Only return success (exit code 0) on FILLED. Otherwise any terminal status (CANCELLED/REJECTED/EXPIRED/REPLACED) ends the wait.

**Exit codes:** 0 = filled, 1 = other terminal status, 2 = timed out.

**Example:**
```bash
python3 scripts/wait_for_fill.py --order-id 345d3e58-5ba3-401a-ac89-1b756332cc94 --timeout 300
```

**Workflow:**
1. After `place_order.py` / `place_spread.py` / `place_multileg.py` returns an order ID, run `wait_for_fill.py --order-id <id>` to block until terminal status.
2. Report the final status, fill quantity, and average price.

### Cancel and Replace Order
When the user wants to "modify my order", "change the limit price", "update the quantity on order X", or asks to swap an open order for one with new parameters:

**Required parameters:**
- `--order-id`: UUID of the existing order to replace
- `--order-type`: New order type (LIMIT, MARKET, STOP, STOP_LIMIT)

**Optional parameters:**
- `--quantity`: New quantity (omit to keep original)
- `--limit-price`: Required for LIMIT/STOP_LIMIT
- `--stop-price`: Required for STOP/STOP_LIMIT
- `--time-in-force`: DAY (default) or GTD (requires `--expiration-time`)
- `--expiration-time`: Required when GTD

**Example:**
```bash
python3 scripts/cancel_and_replace.py --order-id 345d3e58-5ba3-401a-ac89-1b756332cc94 \
  --order-type LIMIT --quantity 10 --limit-price 230.00
```

**Workflow:**
1. If the user doesn't know the order ID, run `get_orders.py` first.
2. Confirm the new parameters with the user.
3. Execute `cancel_and_replace.py`. The replacement gets a new order ID — report both.

### Preflight Multi-Leg
When the user wants to price a multi-leg options strategy other than a plain vertical spread (iron condor, butterfly, straddle, strangle, calendar, diagonal, ratio spread, jade lizard, etc.):

**Required parameters:**
- `--leg`: Repeat 2-6 times. Format `SYMBOL:TYPE:SIDE[:OPEN_CLOSE][:RATIO]`
  - `TYPE` = EQUITY | OPTION
  - `SIDE` = BUY | SELL
  - `OPEN_CLOSE` = OPEN | CLOSE (required for OPTION legs)
  - `RATIO` = optional integer ratio
- `--quantity`: Number of strategy units
- `--limit-price`: Net limit (positive = debit, negative = credit)

**Optional parameters:**
- `--time-in-force`: DAY (default) or GTD (requires `--expiration-time`)
- `--expiration-time`: Required when GTD

**Examples:**

Iron Condor on AAPL (sell put spread + sell call spread, $1.50 net credit):
```bash
python3 scripts/preflight_multileg.py --quantity 1 --limit-price -1.50 \
  --leg AAPL251219P00190000:OPTION:SELL:OPEN \
  --leg AAPL251219P00185000:OPTION:BUY:OPEN \
  --leg AAPL251219C00210000:OPTION:SELL:OPEN \
  --leg AAPL251219C00215000:OPTION:BUY:OPEN
```

Long Straddle on AAPL ($5.00 debit):
```bash
python3 scripts/preflight_multileg.py --quantity 1 --limit-price 5.00 \
  --leg AAPL251219C00200000:OPTION:BUY:OPEN \
  --leg AAPL251219P00200000:OPTION:BUY:OPEN
```

**Workflow:**
1. Use `get_option_chain.py` and `get_option_expirations.py` to pick strikes/expirations.
2. Execute `preflight_multileg.py` to see estimated cost, margin requirement, and buying-power impact.
3. If user proceeds, run `place_multileg.py` with the same legs.

### Place Multi-Leg
When the user is ready to place a non-vertical multi-leg options strategy:

Same arguments as Preflight Multi-Leg above. Only LIMIT orders are accepted by the API for multi-leg orders.

**Example:**
```bash
python3 scripts/place_multileg.py --quantity 1 --limit-price -1.50 \
  --leg AAPL251219P00190000:OPTION:SELL:OPEN \
  --leg AAPL251219P00185000:OPTION:BUY:OPEN \
  --leg AAPL251219C00210000:OPTION:SELL:OPEN \
  --leg AAPL251219C00215000:OPTION:BUY:OPEN
```

**Workflow:**
1. Always run `preflight_multileg.py` first with the same legs.
2. Confirm with the user.
3. Execute `place_multileg.py`. Report the order ID.
4. Optionally call `wait_for_fill.py --order-id <id>` to monitor through to terminal status.

### Flatten And Go Short
When the user wants to "reverse my position", "flip to short", "flatten my long and short it", or asks to close a long equity position and immediately open a short:

**Required parameters:**
- `--symbol`: Equity symbol
- `--short-quantity`: Number of shares to short after flattening

**Optional parameters:**
- `--order-type`: Short order type — MARKET (default), LIMIT, STOP, STOP_LIMIT
- `--limit-price` / `--stop-price`: Required for non-MARKET types
- `--time-in-force`: DAY (default) or GTD (requires `--expiration-time`)
- `--session`: CORE or EXTENDED
- `--flatten-timeout`: Seconds to wait for the flatten leg to fill (default 60)

**Important:** This is **experimental** in the SDK and **not atomic** — it's a two-order workflow (flatten the long, then short). Market conditions can move between the two fills.

**Example:**
```bash
python3 scripts/flatten_and_short.py --symbol TSLA --short-quantity 10
```

**Workflow:**
1. Warn the user about the non-atomic nature and the unlimited theoretical risk of shorting.
2. Execute the script. It reports both the flatten order (if any) and the short order.
3. The script can be skipped if the user is already flat or short — in that case it just submits the short directly.

### Watch Prices (Real-time)
When the user asks to "watch the price", "monitor a stock", "alert me when X moves", or wants a real-time stream of quote changes:

**Required parameters:**
- One or more instruments: `SYMBOL` or `SYMBOL:TYPE` (TYPE = EQUITY | OPTION | CRYPTO, defaults to EQUITY)

**Optional parameters:**
- `--poll-seconds`: SDK polling interval (0.1-60, default 2.0)
- `--max-updates`: Stop after N price changes (useful when the agent only needs a snapshot, not an open stream)

**Examples:**

Watch a single equity:
```bash
python3 scripts/watch_prices.py AAPL
```

Watch a basket with a 5-second poll:
```bash
python3 scripts/watch_prices.py AAPL GOOGL MSFT --poll-seconds 5
```

Capture 10 price changes on BTC, then exit:
```bash
python3 scripts/watch_prices.py BTC:CRYPTO --max-updates 10
```

**Workflow:**
1. Stream prints one line per detected price change (timestamp, symbol, old→new last, bid, ask, changed fields).
2. For automation-style use (set an alert and walk away), pair this with `--max-updates` plus an outer loop or with the `/schedule` skill — do not leave a long-lived stream running by default.
3. For trade triggers, the agent should read each line and decide whether to call `place_order.py`.
