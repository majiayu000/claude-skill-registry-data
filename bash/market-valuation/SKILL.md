---
name: market-valuation
description: |
  How expensive and how frothy the Indian market is, from files you download and numbers you look
  up: NIFTY (or any NSE index) P/E, P/B and dividend-yield percentiles over 5/10/all years with a
  cheap/fair/expensive/extreme band, handling NSE's 2021 switch to consolidated P/E; earnings yield
  vs the 10-year G-sec; market cap to GDP with India reference levels; and a 0–100 froth score from
  valuation, India VIX, breadth, IPO and SME-IPO heat, SIP and demat growth, F&O activity and MTF
  leverage, mapped to a phase and a risk posture. valuation.py works offline.

  Use when the user asks: "is the market expensive", "NIFTY PE percentile", "is NIFTY overvalued",
  "are we in a bubble", "is there froth in small caps", "market cap to GDP India", "Buffett
  indicator India", "bond yield vs earnings yield", "should I slow down my buying", "is the IPO
  market too hot", or wants valuation context before adding equity exposure.
---

# Market Valuation and Froth (India)

`market-regime` says what the trend allows today. This skill says how much is already priced in and
how crowded the trade is. Rich valuations and hot behaviour lower future returns and raise the
damage when the trend breaks, but they rarely say when.

## Commands

```bash
python3 scripts/valuation.py pe --csv nifty50_pe.csv                    # percentiles, bands, basis break
python3 scripts/valuation.py pe --csv nifty50_pe.csv --since 2021-03-31 --windows 3,5 --json
python3 scripts/valuation.py yieldgap --pe 22.4 --gsec 6.55             # one-off reading
python3 scripts/valuation.py yieldgap --csv nifty50_pe.csv --yields gsec10y.csv   # + gap percentile
python3 scripts/valuation.py mcap-gdp --mcap 470 --gdp 357 --gdp-basis "FY26 provisional"
python3 scripts/valuation.py froth --inputs froth_inputs.json --as-of 2026-11-12
python3 scripts/valuation.py froth --csv nifty50_pe.csv --vix 11.5 --mtf-yoy 54 --inputs-as-of 2026-11-10
```
Common flags: `--json` (strict JSON), `--as-of DATE`, `--date-format dmy|mdy`; `pe`/`yieldgap` also take
`--since`, `--windows 5,10`, `--bands 25,75,90`, `--index "NIFTY 50"`. `froth` takes every input as a
flag (`--help` lists them with units), `--breadth-json` (output of
`../market-breadth/scripts/breadth.py status --json`), `--max-age-days 45` and `--drop-stale`. Errors
exit 2 with one `error:` line. Dates are never guessed: slash dates need a day above 12 somewhere in
the column, or `--date-format`.

## Where each number comes from

Fetch current values with WebSearch/WebFetch, cite each source and date, and never invent a missing
one. nseindia.com and niftyindices.com block scripts, so the user downloads those CSVs in a browser.

| Input | Source | Notes |
|---|---|---|
| P/E, P/B, div yield history | niftyindices.com → Reports → Historical Data → "P/E, P/B & Div Yield" (choose index and range) | Header `Index Name, Date, P/E, P/B, Div Yield %` (seen on the report page); the old NSE archive file used `Date, P/E, P/B, Div Yield`. Columns are matched by keyword, several files merge, and note rows are kept |
| 10-year G-sec yield | RBI DBIE, FBIL/CCIL benchmark, or an Investing.com "India 10Y" export (`Date, Price, …`; Price is the yield) | Percent, e.g. 6.55 |
| Market cap, GDP | BSE all-listed market cap (₹ lakh crore); MoSPI nominal GDP | Say which GDP: trailing four quarters, last fiscal year, or estimate |
| Mid/small-cap P/E | Same niftyindices report for NIFTY Midcap 150 and Smallcap 250 | Same date as the NIFTY 50 P/E |
| India VIX | NSE close | |
| IPOs | Exchange listing pages, IPO trackers | Mainboard listings in the last 3 months and their listing-day gain; SME subscription multiples |
| SIP inflow | AMFI monthly note (around the 10th) | Same month a year earlier for growth. Sep-2026 was a record ₹32,490 cr |
| New demat accounts | CDSL and NSDL monthly figures, SEBI Bulletin | Total was about 23.8 crore in Aug-2026 (press reports) |
| F&O activity | NSE Market Pulse, SEBI studies | Individual traders' premium turnover or unique-trader count, year on year |
| MTF book | NSE/BSE daily margin-trading reports; monthly CareEdge notes | NSE+BSE book was ₹1.48 lakh cr in Aug-2026 vs ₹96,000 cr a year earlier (CareEdge) |

Inputs file: JSON `{"as_of": "2026-11-10", "inputs": {"vix": 11.5, "mtf_book": {"value": 148000,
"as_of": "2026-10-31", "source": "NSE"}}}` or CSV `input,value,as_of,source`. Each input gets an
`as_of`. Components older than `--max-age-days` are flagged stale (year-ago bases, 12-month averages
and annual GDP are exempt).

## The 2021 P/E basis break

NSE Indices' press release of 23-Feb-2021 moved index P/E from trailing-four-quarter standalone to
consolidated earnings (standalone only where no consolidated figures exist), from 31-Mar-2021.
Consolidated profits include subsidiaries, so NIFTY's P/E dropped overnight (reported as roughly 40 to
33) with no price move; P/B and dividend yield were not part of the change. `pe` marks windows that
span the switch (†), takes its headline from consolidated-only history, and prints the P/E step
beside the P/B change. `--since 2021-03-31` drops the old basis everywhere. Post-switch history is
about five years (one cycle): treat percentiles as provisional and lean on P/B for long comparisons.

## What it computes

- **Percentiles:** share of observations at or below today. "Richness" flips dividend yield and yield
  gap so higher always means more expensive. Bands: cheap < 25 ≤ fair < 75 ≤ expensive < 90 ≤
  extreme. "Richer" is the share of history that was more expensive than today.
- **Yield gap:** 100 ÷ P/E − 10-year G-sec, the bond ÷ earnings-yield ratio, the P/E at which the gap
  would be zero and, with both files, its percentile. In India the gap is usually negative.
  Published "rich" thresholds conflict (about 1–3 points), so read it against its own history.
- **Market cap ÷ GDP:** bands cheap < 60, fair 60–100, elevated 100–120, expensive 120–140, extreme
  140+. References: long-period average about 75–87% (Motilal Oswal notes, rising as years are
  added); about 55% at the Mar-2020 low; 149% at the Dec-2007 peak; 130–150% in 2024–25.
- **Froth score:** sub-scores 0–100 from fixed anchors, weighted, re-normalised over what you supply,
  with coverage and confidence (high ≥ 75% of weight, low < 50%).

| Group | Components (weight) | Why |
|---|---|---|
| Valuation 40 | P/E percentile 16, yield gap 8, mcap/GDP 8, mid/small-cap P/E premium over large 8 | Most objective, but slow and it can stay high for years |
| Leverage 12 | MTF book growth year on year | Borrowed money forces selling in a fall |
| Issuance 17 | Mainboard IPO rate and listing gain 10; SME subscription 7 | Supply rises to meet demand near tops |
| Retail 18 | SIP growth 6, new demat accounts 6, F&O activity 6 | New money and speculation |
| Complacency 13 | India VIX (low scores high) 8, breadth score 5 | Calm, broad rallies get crowded |

Phases: < 20 Depressed, 20–39 Normal, 40–59 Warm, 60–79 Frothy, 80+ Euphoric. Each phase maps to a
size multiplier on the `market-regime` allowance (1.0, 1.0, 0.8, 0.5, 0.25) and to stop, IPO and
leverage guidance. This is risk management, not a market call.

## Reading it in India

- **SIP money props up multiples.** Since 2020, monthly SIPs have grown into a steady domestic bid
  that absorbs FII selling (see `fii-dii-flows`). That has kept P/E above its old averages for longer,
  so "expensive" alone has been a poor reason to sell. Watch for SIP growth stalling while valuations
  stay high.
- **Froth shows up in small caps, SME issues and leverage first.** 2007: market cap to GDP peaked
  near 149% in Dec-2007 amid an IPO rush, before the 2008 crash. 2018: the BSE Smallcap index peaked
  on 15-Jan-2018 and fell about 35% by mid-2019 while NIFTY held up. 2021: record demat openings,
  new-age tech IPOs and a retail F&O surge (SEBI studies later found about 9 in 10 individual F&O
  traders lost money). 2024: on 11-Mar-2024 the SEBI chairperson warned of froth in small and mid
  caps and their funds had to publish stress tests; SME IPOs drew hundreds of times subscription (a
  two-showroom dealer drew about 419×) and NSE capped SME listing-day prices at 90% over issue.
- **Low VIX is not safety.** India VIX at record-low levels (near 10 in 2023 and 2025) meant
  complacent option pricing, not low risk.

## How other skills use it

- `market-regime` sets the exposure ceiling; the froth phase scales new position size within it.
  Frothy plus "Uptrend under pressure" is the combination to respect most.
- `market-breadth`: feed its `status --json` to `--breadth-json`. A frothy score with narrowing
  breadth means the crowd is concentrated in fewer names.
- `fii-dii-flows`: DII absorption explains how valuations stay high despite FII selling. Absorption
  failing while the score is Frothy is a warning.
- `macro-regime`: rates and the G-sec yield move the yield gap. Check it before calling equities
  cheap or dear relative to bonds.
- `ipo-analysis`: Frothy or Euphoric means skipping listing-gain applications and SME issues.
- `position-sizing` and `trailing-stops` apply the posture: smaller risk per trade, tighter trails.

## Limits

Valuation is a poor short-term timing tool: markets stay expensive or cheap for years. Percentiles
depend on the history loaded. The froth anchors are judgement calls, not fitted values. Monthly
inputs lag by four to six weeks. Comparisons across the 2021 P/E switch are unreliable.

## Output

```
Valuation ([index], [date], source): P/E x (pctile p over [window], band), P/B y, div yield z%
Yield gap: EY e% − G-sec g% = d pp (pctile q) | Mcap/GDP r% ([band], GDP basis)
Froth: s/100 [phase] (coverage c%, confidence) | hot: [..] | cool: [..] | posture: [size ×m, stops, IPOs]
```
_Educational analysis, not investment advice. Data: [sources + dates]._
