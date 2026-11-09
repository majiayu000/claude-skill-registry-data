---
name: multi-timeframe-analysis
description: |
  Three-screen multi-timeframe analysis for NSE/BSE stocks and indices: weekly (or monthly) sets the
  bias, daily finds the setup, and 75-minute / 15-minute bars time the entry, with a 6-factor
  confluence score that sets position size. Uses ta.py mtf to resample daily data into weekly and
  monthly views automatically.

  Use when the user asks: "weekly vs daily trend", "multi-timeframe check", "higher timeframe view",
  "3-screen analysis", "is the daily setup aligned with weekly", "what's the bigger trend on X", or
  wants a quality score for a setup.
---

# Multi-Timeframe Analysis

Higher timeframes decide direction; lower timeframes refine timing. Trading against the weekly trend
needs a much stronger reason than trading with it.

## The three screens (Indian session adaptation)

| Screen | Positional / swing | Short-term swing | Intraday |
|---|---|---|---|
| 1 — Bias | Monthly + **weekly** | Weekly | Daily |
| 2 — Setup | **Daily** | Daily / 125-min | 75-min |
| 3 — Entry | 75-min / 60-min | 15-min | 5-min / 3-min |

The NSE session is 375 minutes (09:15–15:30). **75-minute candles** divide it into exactly five
bars, and **125-minute** into three, so many Indian traders use them instead of 1h/4h, which leave a
stub bar. Most Indian charting tools (Kite, TradingView, Groww) offer custom intervals.

## Run it

```bash
python3 ../technical-analysis/scripts/ta.py mtf --symbol HDFCBANK      # or --csv / --candles
python3 ../technical-analysis/scripts/ta.py mtf --csv nifty.csv --json
```

The script builds weekly and monthly bars from daily data, using ISO weeks for Monday–Friday
sessions. The current week is partial until Friday's close. For each timeframe it gives structure,
the indicator dashboard and a bias. It then scores a long and a short setup. For screen 3, fetch
intraday candles from the broker MCP, or with `ta.py summary --symbol X --interval 15m --period 1mo`.

## Screen 1 — weekly bias
- Swing structure (HH/HL or LH/LL) and price vs 20- and 50-week SMA.
- Weekly RSI above or below 50; weekly MACD histogram direction.
- Major horizontal levels with multiple weekly touches and the 52-week range.
- Verdict: **bullish / bearish / neutral**. Neutral weekly means smaller size or range tactics only.

## Screen 2 — daily setup (in the weekly direction)
- Uptrend: look for pullbacks to SMA20/50, prior breakout levels, or Fib 38.2–61.8% on declining
  volume. Downtrend: the mirror image.
- Patterns: flags, bases, double bottoms or tops, breakouts with volume and rising delivery %.
- Verdict: setup present / no setup / counter-trend (risky).

## Screen 3 — entry timing
- Wait for the lower timeframe to turn in your direction: a reversal candle at the level, a 75-min
  close back above VWAP or EMA20, an RSI hook from 40, or a MACD cross.
- The stop goes beyond the lower-timeframe swing, which tightens risk and improves R:R.
- Avoid entries in the first 15 minutes (pre-open imbalance) and the last 30 minutes (closing-VWAP
  window) unless that is your method.

## Confluence score (1 point each; the script computes it)

| Factor | |
|---|---|
| Weekly trend agrees with direction | +1 |
| Daily shows a valid setup (pullback to MA/level in trend) | +1 |
| Daily RSI supports (rising 40–70 for longs) | +1 |
| Daily MACD histogram improving | +1 |
| Clear S/R within ~2 ATR for stop or target | +1 |
| Volume confirms (up-day expansion or quiet pullback) | +1 |

| Score | Action |
|---|---|
| 5–6 | Strong: full planned size |
| 4 | Good: full size |
| 3 | Marginal: half size |
| 2 | Weak: skip or paper trade |
| 0–1 | No trade |

The score is mechanical. Sanity-check it visually and override with stated reasons.

## Common mistakes
- Fighting the weekly trend because the daily RSI is oversold.
- Using one timeframe only, or switching timeframes until one agrees.
- Ignoring the index: on big index days most large caps move with NIFTY. Check NIFTY's weekly bias
  as screen 0.
- Treating a partial current week as a completed weekly candle.
