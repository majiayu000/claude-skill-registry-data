---
name: macro-regime
description: |
  Structural (6–24 month) macro regime for Indian equities from monthly cross-asset lines: equal
  weight or smallcap vs NIFTY (broadening), size, NIFTY Bank leadership, cyclicals vs defensives,
  NIFTY vs gold in rupees, India 10-year G-sec and the yield curve (10y minus T-bill or repo),
  USD/INR, Brent, the US 10-year and India VIX. Each line gets a 6- vs 12-month crossover state
  and its last turn. Output: a regime label (Broadening, Narrow, Inflationary squeeze, Easing,
  Risk-off, Transitional) with evidence, an "N of M turned" count, tilts and what would flip it.
  macro.py works offline from CSVs.

  Use when the user asks: "what is the macro regime", "is the market broadening or narrowing",
  "are smallcaps leading", "is the yield curve inverted in India", "how do crude and the rupee
  affect the market", "is RBI easing helping stocks", "equity vs gold", "should I tilt to
  defensives this year", "big-picture positioning", or before a quarterly allocation review.
---

# Macro Regime (India)

**Not the same as `market-regime`.** That skill reads NIFTY's daily tape (distribution days,
follow-through) over a horizon of weeks and sets the exposure ceiling. This one works on month-end
data over 6–24 months. It asks which kind of market India is in (who leads, and whether crude, the
rupee and rates are helping or hurting) and changes only a few times per cycle. Use it for the
quarterly allocation tilt, then let the faster skills time entries inside it.

## Commands

```bash
python3 scripts/macro.py series                                    # file names, tickers, sources
python3 scripts/macro.py status --csv-dir macro_data/              # label, evidence, table, tilts
python3 scripts/macro.py status --csv-dir yields/ --fetch --json   # CSVs for yields, Yahoo for the rest
python3 scripts/macro.py history --csv-dir macro_data/ --months 36
python3 scripts/macro.py component curve --csv-dir macro_data/     # one gauge month by month
```
Flags: `--as-of YYYY-MM[-DD]` (replay), `--closed-months` (drop the month in progress), `--fast 6`,
`--slow 12`, `--recent 3` (turn window), `--band-pct 0.25` / `--band-bp 5` (dead band),
`--ticker KEY=TICKER`, `--period 10y`, `--json` (strict JSON). Loader helpers are shared with
`../technical-analysis/scripts/ta.py`. Errors print one `error:` line and exit 2.

## Inputs: one CSV per series, any subset

A date column plus a close/price/yield column is enough. Daily, weekly or monthly rows all work
(the last value of each month is used). Null rows are skipped. Investing.com exports (MM/DD/YYYY,
"Price" column) are detected from the whole file. Name each file after the series key or label
(`series` lists the aliases).

| Key | Series | Yahoo | Status | Where else |
|---|---|---|---|---|
| NIFTY, BANK | NIFTY 50, NIFTY Bank | ^NSEI, ^NSEBANK | confirmed | niftyindices.com historical data |
| SMALLCAP, MIDCAP | Smallcap 250, Midcap 150 | NIFTYSMLCAP250.NS, NIFTYMIDCAP150.NS | confirmed | niftyindices.com |
| EQUALWEIGHT | NIFTY50 Equal Weight | — | csv-only | niftyindices.com strategy indices |
| FMCG, PHARMA / METAL, REALTY, PSUBANK | defensive / cyclical baskets | ^CNXFMCG ... ^CNXPSUBANK | confirmed | niftyindices.com |
| GOLD | GOLDBEES (gold in ₹) | GOLDBEES.NS | unconfirmed | broker history, MCX or IBJA prices |
| IN10Y | India 10-year G-sec yield | — | csv-only | RBI DBIE, CCIL/FBIL, Investing.com export |
| SHORT | 91-day T-bill or repo rate | — | csv-only | RBI DBIE, FBIL; a repo file needs only change dates |
| USDINR | USD/INR | INR=X (or USDINR=X) | unconfirmed | RBI/FBIL reference rate |
| BRENT | Brent crude | BZ=F | unconfirmed | EIA, Investing.com |
| US10Y | US 10-year | ^TNX | unconfirmed | FRED DGS10 |
| VIX | India VIX | ^INDIAVIX | unconfirmed | nseindia.com historical VIX |

"Confirmed" means daily history was served in this pack's 2026-10-31 Yahoo probe (shared with
`sector-rotation`). "Unconfirmed" tickers are the usual symbols, but Yahoo rate-limited (HTTP 429)
the 2026-11-12 check, so they were not verified. Use `--ticker` or a CSV if one fails. G-sec yields
are not on Yahoo. `--fetch` (or no `--csv-dir`) needs `pip install yfinance`.

## Method

1. Month-end values. One missing month is bridged; a longer hole drops older data (with a warning).
   A repo series is carried forward between policy changes. Ten lines: price ratios (concentration, size, banks, cyclical/defensive baskets, NIFTY/gold) and
   levels (10-year, USD/INR, Brent, US 10-year, VIX). Baskets are equal-weight after rebasing to
   100. Without equal weight, smallcap/NIFTY becomes the concentration line and midcap/NIFTY the
   size line, so no ratio is counted twice.
2. State = 6-month SMA vs 12-month SMA of the line, with a dead band (0.25% for ratios, 5bp for
   yields). A **turn** is a change of direction, dated by the month it happened. A fitted 6-month
   slope labels the trend as running or fading (for example "rising, fading"). 6- and 12-month
   changes are shown in % (or bp for yields).
3. Curve = 10y minus the short rate, with the same crossover (steepening/flattening; bull or bear
   from the 10y direction), plus an **inversion flag** with the start month.
4. Transition count: "N of M components turned in the last 3 months". 0 = stable, under 25% =
   isolated, 25–50% = rotation building, 50% or more = broad transition. It is a tally, not a
   probability. The month in progress is flagged as provisional.

## Regime labels (the first one that matches is the headline; others are listed as "also matching")

| Label | Rule | Tends to favour / hurt (tendencies, not predictions) |
|---|---|---|
| Inflationary squeeze | ≥2 of Brent, USD/INR, 10y rising, none falling | IT and pharma exporters, upstream oil, gold, short debt / OMCs, paints, aviation, NBFCs, realty |
| Risk-off / contraction | ≥3 equity ratios falling incl. NIFTY/gold (cyc/def if no gold); 2 if VIX ≥22 | FMCG, pharma, gold, cash / smallcaps, PSU banks, metals, leverage |
| Broadening risk-on | concentration/size rising, none falling, ≥60% of equity ratios rising | mid/small caps, capex, PSU banks, metals / defensives, gold weight |
| Narrow / concentrated | breadth pair falling, none rising | heavyweights, large-cap quality / small-cap breakouts |
| Easing tailwind | 10y falling + a backer (steepening curve, crude down, US yields down, firmer rupee); not crude and rupee both up | banks, NBFCs, realty, autos, gilt duration |
| Transitional / mixed | none of the above | balance; use the faster skills |

The squeeze ranks first because crude feeds India's current account, the rupee and CPI together,
and that combination has repeatedly kept RBI tight. "What would change the label" flips one gauge
at a time and lists the flips that alter the headline, nearest crossover first.

## Reading the components in India

- **Breadth and size:** equal weight or smallcap rising against NIFTY means money is spreading out
  (retail/SIP flows, domestic cyclicals). A narrow tape means FII money is sitting in the
  heavyweights. Smallcap/NIFTY tends to turn before the index does, in both directions.
- **NIFTY Bank / NIFTY:** credit growth and the rate cycle. PSU banks lead in capex upcycles.
  Private banks lead when FIIs return.
- **Cyclicals vs defensives:** metals, realty and PSU banks track the capex/PSU cycle and global
  metals. FMCG and pharma lead when rural demand or global growth is weak.
- **NIFTY / gold:** gold is the Indian household's hedge, and rupee depreciation lifts it twice.
  Gold winning for months is a warning about risk appetite, not just a bullion trade.
- **10-year and curve:** read with the RBI cycle. Cuts usually show up as bull steepening (the
  short rate falls faster). An inverted 10y–T-bill curve is rare in India and usually comes from
  liquidity squeezes (advance-tax outflows, defending the rupee), so check the cause.
- **USD/INR:** a weaker rupee usually comes with FII outflows (see `fii-dii-flows`). It helps IT and
  pharma earnings but raises imported inflation.
- **Brent:** India imports about 85% of its crude, so rising crude hurts the current account, the
  rupee, OMC margins and inflation together. Falling crude is a quiet tailwind.
- **US 10-year:** rising US yields pull FPI debt and equity money back home, pressuring the rupee
  and Indian valuations.
- **India VIX:** the level is banded like `market-regime` (13/17/22/30). The trend matters more here.

## How it sits with the other skills

`macro-regime` (quarters) → `market-regime` (weeks, exposure ceiling) → `market-breadth` and
`sector-rotation` (which stocks and sectors) → `fii-dii-flows` (who is buying). Use the label to set
the tilt and the faster skills to time it. When the two regimes disagree (squeeze here, confirmed
uptrend there), size down rather than pick one. Feed the tilts into `portfolio-review`.

## Limits

- Few regime shifts per decade, so each past example is one data point. The rules are judgement,
  not fitted. Ratios can trend for years (smallcap/NIFTY fell through 2018–20), so a state is
  context, not a timing signal.
- The 6/12-month averages lag by design: a turn is confirmed months after the price low or high.
- Yahoo index history can be short or patchy, and the G-sec, equal-weight and repo series are
  CSV-only. Under 5 components the coverage is graded "thin"; say so when you quote the label.
- Baskets are fixed (FMCG+Pharma vs Metal+Realty+PSU Bank). Supply DEFENSIVE.csv or CYCLICAL.csv
  to use your own series.

## Output

```
Regime: [label] | coverage m/10 ([grade]) | month [YYYY-MM] (data to [date])
For/against: [legs] | Transition: N of M turned in the last 3 months | table | tilts | would change
```
_Educational analysis, not investment advice. Data: [files/tickers + month-end dates]._
