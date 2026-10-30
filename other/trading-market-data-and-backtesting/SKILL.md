---
name: trading-market-data-and-backtesting
description: Use when Ruby/Rails applications build or maintain market data (OHLCV candles, instrument master, symbol/session calendars) or run backtests and replay-driven simulations — data integrity, gap detection, timezone discipline, look-ahead-bias prevention, deterministic replay, fees/slippage realism, and out-of-sample evaluation.
license: MIT
---

# Market Data and Backtesting Integrity

## Purpose

Treat market data and backtests as measurement infrastructure: the numbers they produce are only as trustworthy as the data contracts and simulation assumptions behind them.

A backtest can be mathematically correct and still be a lie — a forward-filled gap, a timezone-shifted session boundary, an indicator computed on the close of the bar it trades, or a fill at a price nobody could have gotten. This skill makes the data contracts explicit (OHLCV, calendars, timezones, event time), keeps simulation honest (look-ahead, fees, slippage, latency), and keeps evaluation disciplined (determinism, out-of-sample separation).

Core flow:

```
define the data contract (OHLCV, instrument, calendar)
-> validate integrity (gaps, alignment, sessions, timezones)
-> compute indicators on event-time data with explicit windows
-> simulate execution with fees, slippage, and realistic fills
-> prevent look-ahead at every boundary
-> replay deterministically with pinned inputs
-> evaluate out-of-sample and report honestly
```

Compose this skill with:

- trading-execution-safety for live execution boundaries;
- ruby-financial-data-integrity for PnL and fee arithmetic;
- rails-external-stream-ingestion for live market feed consumption;
- rails-database-engineering for historical data storage and queries;
- ruby-tdd-refactoring for indicator/regression tests;
- rails-observability for data-quality telemetry.

This skill owns data and simulation integrity. It does not own strategy design advice ("what should I trade?"), execution safety, or general performance engineering.

## Activate when

- building or validating OHLCV/candle stores, instrument masters, or symbol metadata;
- detecting and repairing candle gaps, misaligned timeframes, or session calendar errors;
- handling exchange timezones, session boundaries, or day-rollover logic;
- implementing indicators that must match historical windows exactly;
- building backtest engines, replay harnesses, or calibration runs;
- preventing look-ahead bias or data leakage in features/signals;
- modeling fees, slippage, latency, or partial fills in simulation;
- comparing backtest results with live behavior;
- designing out-of-sample, walk-forward, or holdout evaluation;
- making replay deterministic and testable.

Do not activate for live order placement (execution safety owns that) or for ledger accounting of realized trades. Activate when data integrity or simulation fidelity is the boundary being changed.

## Repository inspection

Inspect:

1. the data sources: vendor APIs, dumps, or a live feed; their documented and observed contracts;
2. the OHLCV schema: timestamp semantics (bar open/close, epoch unit, timezone), deduplication keys;
3. instrument master: symbol changes, corporate actions, expiries, tick/lot sizes;
4. session calendars: which exchange, which days, holidays, half-days, and how they are stored;
5. gap-handling logic that exists (or does not): detection, repair, forward-fill policies;
6. indicator implementations and their window/alignment conventions;
7. the backtest engine's fill model: at what price, with what fees/slippage, when relative to the signal;
8. what the backtest "knows" at each step — the as-of discipline in the code;
9. determinism: seeded randomness, ordered inputs, pinned dependencies;
10. evaluation splits: train/validation/test boundaries and leakage risks;
11. tests for indicators (against known references) and for gaps/sessions;
12. timezone storage and conversion points throughout the pipeline.

Do not assume vendor timestamps are UTC, that candles are contiguous, that "close" means the same thing across sources, or that a backtest that ran green is unbiased. Verify the data contract, then verify the simulation against it.

## Decision rules

1. Classify the change: market data integrity; indicators and alignment; backtest execution realism; or replay and evaluation. Load the matching reference below before changing that boundary.
2. Pin the data contract first: timestamp meaning, timezone, deduplication key, session calendar — then build on it.
3. Treat gaps as first-class facts: detect, classify, and repair deliberately; a silently forward-filled series is a bias generator.
4. Compute every indicator from event-time windows with explicit boundaries; never let "the current bar's close" participate in a signal that trades at that close.
5. Simulate with pessimistic execution: fees, slippage, latency, and constraints on fills at the bar's extreme prices.
6. Make replay deterministic: same inputs and seed produce byte-identical results, and that property is tested.
7. Keep evaluation honest: out-of-sample separation, no tuning on the test set, and results reported with their assumptions.

## Critical invariants

- Never let a backtest observe data beyond the simulated decision time.
- Never silently forward-fill or interpolate a gap without recording it.
- Never compare or convert timestamps without knowing their timezone and bar-boundary convention.
- Never fill a simulated order at a price that required knowing the future (the bar's extreme on an intrabar signal).
- Never tune on the holdout set; the holdout is spent once.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change stores, validates, or repairs candles, instruments, sessions, or timezones | [references/market-data-integrity.md](references/market-data-integrity.md) | OHLCV contract; Candle gaps; Timeframe alignment; Session calendars and timezones; Instrument master | `event-envelope` |
| a change computes indicators or builds the backtest's as-of discipline | [references/indicators-and-lookahead.md](references/indicators-and-lookahead.md) | Window and alignment conventions; Look-ahead bias; Data leakage; Feature/signal boundaries | `message-handler-boundary` |
| a change simulates fills, fees, or slippage, or compares backtest with live behavior | [references/simulation-and-evaluation.md](references/simulation-and-evaluation.md) | Fill models; Fees and slippage; Live/backtest parity; Deterministic replay; Out-of-sample evaluation | `regression-test` |

## Reference example

An as-of join that cannot see the future — the discipline every backtest needs at its core:

```ruby
# app/services/backtest/as_of_series.rb
class AsOfSeries
  def initialize(bars)
    @bars = bars.sort_by(&:timestamp)   # event time, UTC, bar-open convention documented
  end

  # Everything known strictly before `time`: no partial bar, no future leak.
  def known_at(time)
    index = @bars.bsearch_index { |bar| bar.timestamp >= time } || @bars.length
    @bars[0...index]
  end
end

class Backtest
  def step(time)
    history = @series.known_at(time)            # decision data: past only
    signal = strategy.decide(history)           # indicator windows over completed bars
    return if signal.none?

    fill_price = @fills.fill_price_for(signal)  # next bar's open, plus slippage — not this close
    ledger.record(signal, fill_price)            # fees included, exact arithmetic
  end
end
```

The three look-ahead guards in one frame: `known_at` excludes the current partial bar, the strategy trades on completed bars only, and the fill price comes from the *next* bar with slippage and fees.

## Agent review checklist

- [ ] timestamp semantics documented (epoch unit, timezone, bar-open vs bar-close)
- [ ] deduplication key enforced for candles and instruments
- [ ] gaps detected, classified, repaired, and recorded
- [ ] timeframe alignment explicit (no mixed boundaries in one series)
- [ ] session calendar applied, holidays respected, day-rollover correct
- [ ] indicators tested against known reference values
- [ ] no signal consumes the bar it trades
- [ ] features and metadata use as-of joins, not whole-history joins
- [ ] fills use realistic prices (next open, not the extreme)
- [ ] fees and slippage modeled and stated in results
- [ ] replay deterministic under fixed inputs and seed, and tested
- [ ] out-of-sample separation enforced; holdout used once
- [ ] live/backtest divergence tracked and explained, not explained away

## Anti-patterns

- comparing epoch seconds with epoch milliseconds;
- storing timestamps in local time, or converting with the wrong zone;
- forward-filling gaps silently and forgetting they existed;
- mixing 09:15 and 09:30 bar boundaries in one aligned series;
- computing the signal on the bar's close and filling at that same close;
- a "sharpe" from an in-sample tune reported as out-of-sample performance;
- fills at the bar's high/low for limit orders with no queue/fill model;
- fees modeled "later";
- deterministic-until-random: an unseeded shuffle in the data pipeline;
- survivorship-biased instrument lists (today's symbols applied to past dates);
- tuning parameters against the test set because validation "wasn't enough";
- one giant backtest run reported without its assumptions;
- live behavior that differs from the backtest in data, timing, or costs with no parity report.

## Verification

For data integrity:

`load series -> gap scan -> session check -> timezone round-trip -> schema contract holds`

For look-ahead:

`step at time T -> all inputs strictly before T -> signal reproducible from history alone`

For simulation:

`signal at T -> fill at T+1 open with fees and slippage -> PnL from exact arithmetic`

For determinism:

`same inputs + seed -> byte-identical results -> asserted in CI`

For evaluation:

`train/validation boundaries enforced -> holdout evaluated once -> assumptions reported`

Report data quality findings, the fill model, the leakage defenses, determinism evidence, and the evaluation protocol.

## Source foundation

- ISO 8601 time representations: https://www.iso.org/iso-8601-date-and-time-format.html
- IANA Time Zone Database: https://www.iana.org/time-zones
- Rails Active Support time zones: https://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html
- pandas as-of merge semantics (as-of join reference behavior): https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html
- Repository skills: trading-execution-safety, ruby-financial-data-integrity, rails-external-stream-ingestion, rails-database-engineering, ruby-tdd-refactoring, rails-observability

## Market data and backtesting changes

For candle, instrument, calendar, indicator, backtest, and replay changes:

- pin the OHLCV contract (timestamp meaning, unit, timezone, dedup key) before building on the data;
- validate gaps and session coverage on load, and record every repair decision in the dataset's metadata;
- align timeframes explicitly and keep series with different boundaries separate;
- resolve session calendars per exchange (holidays, half-days) and test day-rollover at the boundary dates;
- compute indicators from event-time windows of completed bars with tested reference values;
- enforce as-of discipline at every join and signal boundary; the current bar's close never trades at itself;
- fill simulated orders at the next bar's open (or a modeled intrabar price) with fees and slippage included;
- keep replay deterministic with pinned inputs, seeded randomness, and a byte-identical test;
- separate out-of-sample data before tuning, spend the holdout once, and report results with their assumptions;
- track live/backtest divergence with a parity report rather than explaining it away.
