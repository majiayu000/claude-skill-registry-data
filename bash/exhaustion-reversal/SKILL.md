---
name: exhaustion-reversal
description: |
  When a move on NSE/BSE has run out of buyers or sellers. exhaustion.py scores a vertical run-up
  0-100 (stretch above the 20/50/200 DMA, acceleration, run length, range/volume blow-off, late
  gaps, upper-circuit streaks, price-band cuts), labels it extended, climax or reversal confirmed,
  and plans the exit: scale out and trail with a GTT if you hold, or short only via stock futures or
  puts on F&O names after a trigger, sized in lots. Also finds selling-exhaustion hammers for long
  entries, judges whether a stock failed to react to news, and scans a universe with F&O tags.

  Use when the user asks: "is this stock parabolic", "has the rally topped", "my stock hit upper
  circuit five days running, should I sell", "how do I book profit on a multibagger", "can I short
  this", "short a stock that ran up 80%", "capitulation or hammer setup", "selling exhaustion",
  "results were good but the stock fell, what does it mean", or wants a blow-off top scan.
---

# Exhaustion & Reversal (NSE/BSE)

`momentum-scanner` finds stocks as they start to move. This skill takes the same stocks weeks later,
when the move is old and steep, and asks whether it is ending. For most Indian retail traders the
answer matters as a **holder**: how much to sell into strength and where to trail the rest. Shorting
is the exception, and only possible in F&O stocks.

## Commands

```bash
python3 scripts/exhaustion.py climax --csv data/KAYNES.csv              # one stock: factors + stage
python3 scripts/exhaustion.py climax --csv-dir data/ --min-score 40     # ranked table
python3 scripts/exhaustion.py plan --csv data/KAYNES.csv --qty 120 --avg-price 4100
python3 scripts/exhaustion.py plan --csv-dir data/ --symbol KAYNES --side short --fno-list fo_mktlots.csv \
    --ban-list fo_secban.csv --margin-per-lot 210000 --capital 1500000 --risk-pct 1 --put-premium 120 --put-strike 5000
python3 scripts/exhaustion.py washout --csv-dir data/ --days 3 --capital 500000 --show-rejects
python3 scripts/exhaustion.py reaction --csv data/INFY.csv --date 2026-10-16 --news bullish --after-close \
    --crowding long --benchmark-csv nifty.csv
python3 scripts/exhaustion.py scan --csv-dir data/ --fno-list fo_mktlots.csv --bands bands.csv
```
Universe flags match `momentum.py`: `--csv-dir` + `--pattern`, `--csv` (repeatable), `--symbols`
(yfinance), `--as-of`, `--min-turnover-cr` (5), `--bands` (`SYMBOL,band`, 0 for F&O), `--tick`,
`--json`. `--fno-list` takes one symbol per line, `SYMBOL,LOT` or NSE `fo_mktlots.csv` (lots are read
from it). Blank or zero candles are skipped; bad input exits 2 with one `error:` line.

## `climax`: the parabolic score

The high of the move is the highest high in the last 15 sessions (`--lookback`). Points:

| Factor | Max | Full marks at |
|---|---|---|
| Stretch | 25 | high 6+ ATR over the 20 DMA (10), 50%+ over the 50 DMA (10), 120%+ over the 200 DMA (5) |
| Acceleration | 15 | last 5 sessions running 3x the 20-day daily pace, with 10%+ in those 5 |
| Run | 25 | +50% in 10 / +80% in 20 / +150% in 60 sessions (15), 8 up days (6) and 6 up weeks (4) in a row |
| Blow-off | 30 | widest bar 3x ATR and volume 4x the 50-day average, each the biggest in 60 sessions, gap-ups in the last 5 sessions, and a peak day that closes in its lower part (reversal bar). Or 6 points per consecutive upper-circuit close (5 locked closes = 30): whichever is higher |
| Band cut | 5 | the exchange narrowed the price band during the run (or the stock sits in a 2%/5% band) |

Why these: stretch and run size say how far price has left value; acceleration and up-day streaks
catch the vertical last leg; the blow-off bar is where late buyers and short-covering arrive at
once. Banded small caps can't print a blow-off bar (they lock), so the circuit streak stands in.

**Stage:** under 40 not extended, 40-64 extended, 65+ climax, and **reversal confirmed** once any of
these happens after the high: a close below the previous session's low, a close below the 10 EMA,
or a lower high (a bounce that fails under the peak, then a close under the pullback low). The date
of the first is printed. Until then the output lists tomorrow's levels to watch.

## `plan`

**Holder (default `--side hold`).** Sell a slice into strength: 25% when extended, 40% at a climax,
50% once confirmed (`--sell-pct`). Trail the rest one tick under the prior day's low (climax or a
circuit streak) or on a close below the 10 EMA (extended), as a **GTT single SELL** with a limit 1-2%
under the trigger. GTTs fire on LTP and send a limit, so a gap below the limit stays unfilled;
plain SL orders expire at 15:30. On a locked upper circuit, selling into the buy queue fills at once,
which is the best liquidity a pumped stock will offer. In a 2%/5% band a lower-circuit lock blocks
every exit. See `trailing-stops` and `stop-loss-strategies` for the general mechanics.

**Short (`--side short` or `both`).** Refused for a non-F&O stock: cash shorts are intraday (MIS)
only, an undelivered short goes to the exchange auction with a penalty, and there is no future or
put to hold overnight. Also refused in the F&O ban (OI above 95% of MWPL: reduce-only) and below
score 40 (`--force`). Otherwise: entry only after a trigger, a trade below the climax-day low or a
failed bounce, never into strength. Stop is 0.5% above the climax high (`--stop-buffer-pct`). Targets
are the 10 EMA, 20 EMA and 50 DMA with their R multiple. Size with `--capital --risk-pct` in whole
lots (`--lot`, or from `--fno-list`). Margin is `--margin-per-lot` from your broker, else 25% of
contract value, capped at 50% of capital. `--put-premium/--put-strike` prices a long put as the
defined-risk route (see `fno-options-analysis`, `options-strategies`). Every short plan prints the
warnings: no ceiling on loss, squeeze into expiry and MWPL, gap-through stops, physical settlement.

## `washout`: selling exhaustion for a long entry

A bar in the last 3 sessions (`--days`) that is the low of the last five and:
a pullback of 8-40% from the 40-session high over 3+ sessions; a prior uptrend (+25% into the high,
a rising 200 DMA, or a name on your `--quality` list); a wick of 50%+ of the bar and a close in
the top 40%; range ≥ 0.75 ATR; volume ≥ the 50-day average. Score: context 20, depth 15, undercut of
an earlier pivot low then a close back above it 25, wick 15, close 10, volume 15, +5 when a
lower-circuit streak just ended. Entry one tick over the bar's high, stop one tick under its low
(NSE ticks), targets the 20 EMA and the prior high, status pending / triggered / failed.

## `reaction`: did the news work?

Day 1 is the news date, or the next session with `--after-close`. Moves are measured in ATRs with
the news (net of `--benchmark-csv` if given) over `--sessions` (3). **Failed** if day 1 closes
against the news in the worst 35% of its range on 1.5x+ volume, or if after 2-3 sessions price is
0.5+ ATR the wrong way and through the news-day low (high, for bad news). **Confirmed** if 0.5+ ATR
the right way and holding the news-day midpoint. Otherwise **inconclusive**. The rule that fired is
printed. `--crowding long|short|none` adds a gate: crowded side + failed reaction + broken level = a
contrarian setup. Judge crowding from `fii-dii-flows` (participant OI), the stock's OI vs MWPL, and
MTF/delivery build-up.

## `scan`

Climax scores ≥ 40 and washout bars, ranked, illiquid names filtered (listed with the reason), each
tagged with its short route: futures/puts, F&O ban, or none overnight.

## Reading it in India

- **Operator small caps and SME stocks** rise in circuit streaks on thin delivery, no news. The
  queue that locked them up becomes the queue that locks them down. Sell into the circuit; never
  short them (you can't overnight, and intraday is usually blocked).
- **ASM/GSM and band cuts.** After sharp run-ups exchanges move stocks into surveillance, cut the
  band 20 → 10 → 5 → 2% and demand 100% margin. Leverage leaves and the run often ends. Check the
  NSE/BSE surveillance lists and series (EQ vs BE).
- **Results-day spikes** gap 10-20% in F&O names. A spike that closes near its low on record
  volume is a reversal bar; `reaction` tells you whether good results were sold.
- **Why shorting strength is dangerous:** parabolic stocks go further than anyone expects, F&O
  names have no circuit, MWPL squeezes force covering, and futures are marked to market daily.
  The defined-risk way is a put or bear put spread, after confirmation.

## Workflow

1. `climax` on what you hold (or `scan`). Under 40: let `trailing-stops` handle it.
2. Extended or climax: `plan` → sell the slice, set the GTT. Confirmed: sell the bigger slice.
3. Short only F&O names, after the trigger, sized by `position-sizing` rules, 1% risk or less.
4. `washout` entries: size with `position-sizing` (`../position-sizing/scripts/risk.py`).
5. Run the `trading-discipline` gate (`../trading-discipline/scripts/discipline.py`) first.

Limits: daily bars only (no intraday triggers or live circuit status); bands are inferred unless
`--bands` is given; F&O status, lots, ban and margin are only what you pass; the score is a
description of the tape, not a probability that the top is in.

_Educational analysis, not investment advice._
