---
name: technical-analysis
description: |
  Systematic chart reading for NSE/BSE stocks and indices: trend and moving-average alignment,
  swing structure, support/resistance clusters, unfilled gaps, volume and delivery %, an indicator
  dashboard (RSI, MACD, Bollinger, ADX, Stochastic), ATR stops, circuit and gap-risk checks, and
  probabilistic scenarios. Ships a zero-dependency engine (ta.py) that reads CSV, broker-MCP candles
  or fetches via yfinance, verified against the `ta` library.

  Use when the user asks: "what's the trend on X", "support and resistance for X", "is X bullish or
  bearish", "indicators for X", "chart analysis", "volume analysis", "levels for NIFTY/BANKNIFTY", or
  any interpretation of price action on Indian equities and indices.
---

# Technical Analysis (NSE/BSE)

Read the chart systematically and report every indicator, not only the ones that agree with a
bias. Let the script do the arithmetic. Your job is interpretation and context.

## 1. Get candles

Pick the first option that works:

```bash
# A. Broker MCP: save the candle response to a JSON file, then
python3 scripts/ta.py summary --candles candles.json --symbol RELIANCE
# B. yfinance (pip install yfinance). NSE stocks auto-map to .NS; indices: NIFTY, BANKNIFTY, SENSEX, INDIAVIX, NIFTYIT …
python3 scripts/ta.py summary --symbol RELIANCE              # --exchange BSE for .BO
python3 scripts/ta.py fetch --symbol NIFTY --period 5y --out nifty.csv
# C. User/exported CSV (Date, Open, High, Low, Close, Volume, any case)
python3 scripts/ta.py summary --csv reliance.csv
```

Use at least 250 daily bars so SMA200 and 52-week levels exist. yfinance prices are split-adjusted
but not dividend-adjusted, which matches broker charts. **Check the last bar's date.** The script
warns when data is stale. Intraday bars from yfinance are limited (60 days for 15m, 730 days for 1h).

Other sub-commands: `levels`, `divergence`, `fib`, `mtf`, `indicators --rows 15`; add `--json` for raw output.

## 2. Trend

- **Structure:** higher highs and higher lows is an uptrend; lower highs and lower lows is a downtrend;
  anything else is a range. The script reports it from swing points (`--swing 5` = 5 bars each side).
- **MA alignment:** price > SMA20 > SMA50 > SMA200 is a strong uptrend, the reverse a strong downtrend,
  and mixed means transition or chop.
- **Golden or death cross** (SMA50 vs SMA200): the script reports recent crosses. It is a lagging
  confirmation, not an entry.
- **Relative strength:** compare the stock to NIFTY and to its sector index (NIFTYIT, NIFTYBANK,
  NIFTYAUTO, …). Leaders in a weak market and laggards in a strong one are different trades.

## 3. Support and resistance

- Swing-point **clusters** within ~1.5% (the script counts touches). Two or more touches is meaningful.
- **52-week high/low** and **round numbers** (₹1,000, ₹2,500; NIFTY 25,000; BANKNIFTY 55,000) act as
  magnets. Indian retail and option writers anchor heavily on round strikes.
- **Unfilled gaps:** gap-up zones act as support and gap-down zones as resistance. Overnight gaps are
  frequent because of GIFT Nifty and US cues.
- **Dynamic levels:** SMA20 (short), SMA50 (medium), SMA200 (major).
- **For indices and F&O stocks:** the largest call-OI strike tends to cap rallies and the largest put-OI
  strike tends to hold dips into expiry (see `fno-options-analysis`).

## 4. Volume and delivery

| Price | Volume | Read |
|---|---|---|
| Up | Rising | Healthy advance |
| Up | Falling | Weak rally, suspect |
| Down | Rising | Distribution, trend acceleration |
| Down | Falling | Selling exhaustion, bounce possible |
| Spike at support | — | Capitulation or absorption |
| Spike at resistance | — | Breakout attempt or distribution |

More than 1.5x the 20-day average is significant. **Delivery % is an India-specific edge.** NSE
publishes the delivery quantity as a percentage of traded quantity per stock per day (security-wise
delivery data, or the broker's "delivery %" field). A rising price with a rising delivery % means real
buyers taking delivery. A rising price with a low delivery % (below about 30% in large caps) is
intraday churn.

## 5. Indicator dashboard

The script grades each indicator bullish, bearish or neutral and counts them:

| Indicator | Bullish | Bearish | Neutral |
|---|---|---|---|
| RSI(14) | >50 and rising; rising out of <30 | <50 and falling; falling from >70 | 40–60 flat |
| MACD(12,26,9) | histogram >0 and growing | histogram <0 and growing | near zero |
| Bollinger(20,2) | %B 0.5–1 (upper half) | %B 0–0.5 | squeeze or walking the band |
| ADX(14) | >25 with +DI > −DI | >25 with −DI > +DI | <20 (no trend) |
| Stochastic(14,3,3) | %K crosses up below 20–30 | %K crosses down above 70–80 | mid-range |
| MA alignment | stacked up | stacked down | mixed |

Indicators are correlated (RSI, Stochastic and MACD all measure momentum). Five bullish signals is
not five independent confirmations. Weight structure and volume above the count.

## 6. India-specific checks (script prints these)

- **Circuit hit:** a close at the day's high or low exactly at a band (2/5/10/20%) means one-sided
  liquidity. The next day can gap again, and exits may be impossible in a lower circuit.
- **Gap statistics:** average and maximum overnight gap over 60 bars. If the stop is closer than the
  typical gap, it is decoration, not protection.
- **Event days:** quarterly results (the stock can move 5–15%), ex-dividend (mechanical price drop),
  bonus/split (check adjustment), index inclusion or exclusion, and F&O ban entry or exit.
- **Closing price is a 30-minute VWAP** (15:00–15:30) on NSE, so "closing basis" stops use that
  number, not the last tick.

## 7. Scenarios

Always give 2–3 scenarios whose probabilities sum to ~100%. Tilt toward the scenario with better
structure + volume + higher-timeframe agreement. Keep near-equal odds when evidence conflicts.

```
A — Bullish (xx%): trigger [daily close above ₹X on >1.5x volume] → targets ₹T1/₹T2; invalid below ₹S
B — Bearish (xx%): trigger [close below ₹S] → targets ₹…; invalid above ₹…
C — Range (xx%): ₹L–₹H for ~N sessions; breakout tell: [volume/delivery/ADX rising above 20]
```

## Output

Lead with the verdict and the data timestamp. Then trend, levels (nearest 2–3 each side with
touches), dashboard counts, volume and delivery, divergences, ATR and stop options, India checks, and
scenarios. Hand off to `position-sizing` and `stop-loss-strategies` when the user wants a trade plan.
