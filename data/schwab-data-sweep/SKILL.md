---
name: schwab-data-sweep
description: Collect a single Schwab MCP data snapshot (accounts, quotes, indicators, option chains) with a five-minute cache so trading agents can reuse consistent inputs. Use whenever an options persona needs fresh risk, market, or chain data before recommending trades.
---

# Schwab Data Sweep

Reliable trade proposals in this workspace start from the same broker payloads. This skill centralizes that workflow so every persona reuses the identical snapshot and cache policy.

## Inputs
- `primary_symbol` (string): Underlying or index to analyze. Prefix indices/volatility products with `$` (e.g., `$SPX`, `$VIX`, `$VIX1D`) to avoid equity substitutions.
- `additional_symbols` (list, optional): Extra tickers for quotes (e.g., the wheel watchlist or hedge ETFs). Keep the list tight to minimize MCP latency.
- `include_option_chain` (bool, default true): Fetch option chain data for `primary_symbol`.
- `indicators` (list, optional): Indicator payloads to compute. Supported values: `atr`, `rsi`, `expected_move`, `historical_volatility`.
- `force_refresh` (bool, default false): Ignore cached payloads even if they are younger than five minutes.

## Outputs
Structured dictionary stored in memory for the calling agent:
- `timestamp`: ISO string + broker timezone from `mcp__schwab__get_datetime`.
- `account`: Payload from `mcp__schwab__get_account_with_positions()`.
- `quotes`: Map of symbol → quote (from `mcp__schwab__get_quotes()`).
- `historical`: Optional OHLCV data (from `mcp__schwab__get_price_history_every_day()` for 1M window).
- `option_chain`: Optional option chain snapshot (when requested).
- `indicators`: Any computed indicators with metadata about lookback and parameters.

## Instructions
1. **Cache Check**
   - Maintain a per-symbol cache keyed by `primary_symbol` + sorted `additional_symbols`.
   - Reuse the existing snapshot when `force_refresh` is false and the cached timestamp is ≤5 minutes old.
   - When reusing, surface the original Schwab timestamp so downstream persona messaging reflects the data age.

2. **Authentication Guardrail**
   - Call `mcp__schwab__get_account_numbers()` once per session if the MCP client indicates an unauthenticated state. Abort and return a `BLOCK` flag if authentication fails.

3. **Account & Capital Snapshot**
   - Run `mcp__schwab__get_account_with_positions()` to capture net liquidity, cash, buying power, and open option positions.
   - Derive helper metrics (wheel exposure %, margin headroom, overlapping SPX structures) for persona-specific reporting, but keep raw payloads intact in the output.

4. **Market Quotes**
   - Assemble the quote request list: `{primary_symbol} ∪ additional_symbols ∪ {$VIX, $VIX1D}` when indices are relevant.
   - Use `mcp__schwab__get_quotes(symbols=...)` with `fields="QUOTE,FUNDAMENTAL"` when single-name data is required for event checks.
   - Normalize timestamps (store both the broker timezone and Eastern Time equivalent for later formatting).

5. **Historical Context**
   - Call `mcp__schwab__get_price_history_every_day(primary_symbol, period_type="MONTH", period="ONE_MONTH")` to support ATR/expected-move math.
   - Skip when the persona explicitly disables historical pulls to reduce latency.

6. **Indicator Bundle**
   - For each indicator requested, call the matching Schwab MCP function:
     - `atr` → `mcp__schwab__atr(symbol=primary_symbol, interval="DAY", length=14)`
     - `rsi` → `mcp__schwab__rsi(symbol=primary_symbol, interval="DAY", length=14)`
     - `expected_move` → `mcp__schwab__expected_move(symbol=primary_symbol, interval="DAY")`
     - `historical_volatility` → `mcp__schwab__historical_volatility(symbol=primary_symbol, period=30)`
   - Store both the numeric result and the parameters used so personas can echo them in final outputs.

7. **Option Chain Snapshot**
   - When `include_option_chain` is true, call `mcp__schwab__get_option_chain(symbol=primary_symbol, include_quotes="true", strike_count=40)`.
   - Cache the option chain alongside its Schwab timestamp; note in the output when the chain comes from outside regular trading hours.

8. **Packaging & Return**
   - Combine all payloads into the output dictionary and persist it in the cache with the broker timestamp.
   - Return the object plus a `cache_metadata` block containing: `source_timestamp`, `eastern_timestamp`, `cache_expires_at`, and `force_refresh_used` flag.

## Usage Notes
- Personas should call this skill exactly once per planning cycle, then reference the cached snapshot for prerequisite checks, sizing, and proposal outputs.
- When a user asks for “updated marks” or more than five minutes have elapsed, set `force_refresh=true`.
- If a required symbol is missing from Schwab (e.g., delisted or after-hours only), return a `FLAG` status with guidance instead of silently omitting the data.

## Examples
```yaml
# 0DTE iron condor sweep
primary_symbol: $SPX
additional_symbols: [$VIX, $VIX1D]
indicators: [atr, rsi, expected_move]
include_option_chain: true
```

```yaml
# Wheel candidate sweep for a single-name equity
primary_symbol: AAPL
additional_symbols: [$VIX]
indicators: [atr, rsi, historical_volatility]
include_option_chain: true
```
