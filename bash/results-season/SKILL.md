---
name: results-season
description: |
  Reads the price reaction to quarterly results on NSE/BSE stocks. Picks the right reaction session
  from the announcement time (same day for pre-market/market-hours, next NSE session for after-hours,
  weekend or holiday releases), measures gap, close, close location, volume vs 50-day, ATR-normalised
  move, 1-20 session follow-through and gap fill, grades it 0-100 (A-D) with visible weights, watches
  weekly bars for a post-results drift entry or a failed reaction, ranks many events, and lists
  positions whose results fall inside a holding window. results.py works offline from CSVs.

  Use when the user asks: "how did X react to results", "was that a good results reaction", "should
  I buy after the results gap", "post-earnings drift setup in X", "rank this quarter's results
  reactions", "did the gap fill", "which of my holdings report before I exit", "results calendar
  check", or plans a swing trade during results season.
---

# Results Season (NSE/BSE)

`fundamental-screening` reads the numbers. This skill reads the market's verdict on them. The
reaction (how far, on how much volume, where it closed, and whether it held) is more objective
than a headline beat or miss, especially in India, where consensus estimates are not freely available.

## Commands

```bash
# One stock: reaction metrics, then the score (adds factor table and a plain-English read)
python3 scripts/results.py reaction --csv tcs.csv --date 2026-10-09 --timing post-market
python3 scripts/results.py score --symbol HDFCBANK --date 18-Oct-2026 --timing 14:20
# Weekly drift watch after a strong gap-up: pullback that holds the gap-day low, then a breakout
python3 scripts/results.py drift --csv dixon.csv --date 2026-07-24 --timing post-market
# Many events: symbol,date,timing CSV (+ optional file column); CSVs named SYMBOL.csv
python3 scripts/results.py scan --events q2.csv --csv-dir data/ --top 10
# Positions with results inside a holding window (feeds trading-discipline's event check)
python3 scripts/results.py calendar-check --events q2.csv --from 2026-11-02 --to 2026-11-13 --symbols TCS,INFY
```
Inputs follow `technical-analysis` (`--csv`, `--candles`, `--symbol`). Dates are ISO (2026-10-31) or
NSE style (31-Oct-2026); a numeric date that could be DD/MM or MM/DD is refused, never guessed.
`--timing` is pre-market, market-hours, post-market, or the filing time (16:05, read as IST). Every
command takes `--json`. Bad input exits 2 with one `error:` line. Use 220+ daily bars for the 200-DMA.

## Which session is the reaction?

| Announced | Reaction session |
|---|---|
| Before 09:15 on a trading day | Same day: the open is the verdict |
| 09:15–15:30 | Same day. The open came before the news, so read the close, not the gap |
| 15:00–15:30 | Same day, flagged: NSE's close is the volume-weighted price of the last 30 minutes, so part of the move lands next session |
| After 15:30, or a weekend/holiday | Next NSE session (holiday list from `../fno-options-analysis/scripts/options.py`) |

Some companies hold results board meetings on Saturdays, and those react on Monday. Muhurat or
special sessions in the data are skipped and flagged. Use `--reaction-date` to override.

## Reading `reaction` and `score`

`reaction` reports gap %, reaction-day return, close location (0 = low, 1 = high), volume ÷ the
prior 50 sessions, ATR(14) as of the day before, follow-through at +1/3/5/10/20 sessions (vs the
reaction close and vs the pre-results close, and whether the reaction-day low held), and whether
the gap filled.

| Factor | Weight | Full marks | Why |
|---|---|---|---|
| Reaction size | 35 | close ≥ +3 ATR vs pre-results close | ATR scales the move to the stock's usual noise; the close is what the market kept |
| Volume expansion | 20 | 4× the 50-day average (1× = 0) | Funds re-rating a stock can't hide their size |
| Close strength | 15 | closed at the day's high | A faded gap means holders used the news to sell |
| Trend position | 20 | above 200-DMA (7), above 50-DMA (6), at the pre-results 52-week high (7, zero at −10%) | Gaps into new highs meet no trapped sellers |
| Fresh surprise | 10 | ≤ +10% in the 60 sessions before results (zero at +40%) | A big run-up often means the news was already priced in |

Volume, trend and fresh surprise are context, so they are multiplied by a **gate**: 0 for a flat or
negative close and 1 from +1 ATR up. A stock in a perfect uptrend that does nothing on results earns
little. Missing data (no volume, under 200 bars) drops that factor and rescales the total to 100.
Grades: **A ≥80, B ≥60, C ≥40, D below**. The score is long-biased. A strong negative reaction is a D
with a bearish read.

## Reading `drift`

Runs only after a strong gap-up: gap or close ≥ `--min-gap-pct` (4%) with a green close. Weeks
start after the reaction week.
- **Failed:** any daily close below the gap-day low. The reaction was rejected, so drop it.
- **Pullback-set:** the first red weekly candle whose low stays above the gap-day low. The trigger is
  that week's high, and the stop is its low minus `--stop-buffer-pct` (0.5%). Further red weeks
  extend the pullback and lower the trigger. A week that dips under the gap-day low intraday but
  closes above it is noted as a shakeout.
- **Triggered / stopped:** the later breakout above the trigger (a gap above it fills at the open),
  then the stop check. Reports R so far. **Expired:** no entry within `--max-weeks` (12).

Feed the trigger and stop to `../breakout-planner/scripts/breakout.py plan --pivot .. --stop ..` for
ticks, size and GTT orders.

## India context

- **Deadlines (SEBI LODR Reg 33(3)):** Q1–Q3 results within 45 days of quarter end (14 Aug, 14 Nov,
  14 Feb). Q4 comes with the audited annual results within 60 days of the FY end (30 May).
  `calendar-check` prints the season deadline and flags positions with no known date.
- **Notice (Reg 29):** the board meeting to approve results must be intimated at least 2 working
  days ahead, excluding the intimation and meeting days. This has applied since the 17-May-2024
  amendment; it was 5 days before that. Exchange board-meeting lists therefore cover only the next
  few days. Re-check them during long holds.
- **Timing (Sch III Part A):** the outcome must be filed within 30 minutes of the meeting ending, so
  results can land mid-session as well as after 15:30. Use the filing timestamp.
- **F&O stocks:** implied volatility builds into results and collapses after (IV crush). Option
  buyers can be right on direction and still lose. Compare the IV-implied move from
  `fno-options-analysis` with the realised ATR move here.
- **Non-F&O stocks** have 5/10/20% price bands. A results-day upper circuit means buyers may not have
  been filled. A lower circuit traps holders, and stops do not fill. The script flags closes pinned
  at a band.
- **No free consensus.** Judge the numbers by YoY growth first (seasonality), then QoQ, plus margins
  and management commentary (`fundamental-screening`). The reaction shows how they compared with
  what the market expected.

## How it connects

- `india-market-analyst`: avoid fresh swing entries just before results. Run `calendar-check` before
  any multi-day plan.
- `trading-discipline`: an INSIDE row from `calendar-check` means the gate gets `--event yes`.
- `momentum-scanner`: a grade-A gap out of a quiet base is an episodic pivot candidate.
- `breakout-planner`: a pivot within ~5 sessions of results is a coin toss. After the event, the
  drift trigger is a cleaner pivot.
- `trailing-stops`: manage a triggered drift trade (breakeven at 1R).

## Limits

These are daily bars only: no intraday order of events, no delivery %, no option IV. Reactions to
other news on the same day (block deals, index inclusion, market-wide gaps) look like results
reactions, so check the NIFTY move that day. Thresholds are conventions, not fitted parameters.

_Educational analysis, not investment advice._
