---
name: market-breadth
description: |
  Market-wide breadth for Indian equities: how many NSE/BSE stocks are actually joining the index's
  move. From a folder of stock CSVs (NIFTY 50/500, midcap or smallcap constituents), a yfinance symbol
  list, or an exchange advances/declines file, breadth.py reports % of stocks above 20/50/200 DMA,
  the uptrend ratio, advances/declines with an A/D line and divergence against NIFTY, new 52-week
  highs/lows, the McClellan oscillator and summation index, breadth thrusts, sector participation
  and a 0–100 health score. Works offline from CSV.

  Use when the user asks: "is this rally broad-based", "market breadth", "advance decline ratio",
  "how many stocks are above the 200 DMA", "is NIFTY being carried by a few heavyweights", "are
  midcaps and smallcaps participating", "McClellan oscillator for NSE", "breadth thrust", "new highs
  vs new lows", or wants breadth context alongside the market regime.
---

# Market Breadth (India)

The index tells you where a few large weights went. Breadth tells you what the typical stock did.
A NIFTY high made by five heavyweights while most stocks slide is a weaker market than the chart shows.

## 1. Run it

```bash
python3 scripts/breadth.py status --csv-dir nifty500/ --benchmark-csv "NIFTY 50.csv" --members ind_nifty500list.csv
python3 scripts/breadth.py status --csv-dir nifty500/ --universe-file ind_nifty50list.csv --benchmark-csv nifty.csv
python3 scripts/breadth.py status --ad-csv nse_adv_dec.csv          # exchange counts, no stock files
python3 scripts/breadth.py status --universe-file ind_nifty500list.csv --save-dir nifty500/   # yfinance
python3 scripts/breadth.py history --csv-dir nifty500/ --sessions 60 --out breadth.csv --json
```
Stock CSVs are daily OHLCV, one per stock, file stem = symbol (`RELIANCE.csv`, `.NS` is stripped),
from `../technical-analysis/scripts/ta.py fetch`, a broker export, or `--save-dir` (caches the Yahoo
download: ~500 requests for NIFTY 500). Rows with blank or null prices are skipped. `--pattern`
filters the folder; `--universe-file` restricts it to a constituent list, so one NIFTY 500 folder
gives NIFTY 50, NIFTY 500 and midcap breadth. `--members` (symbol,sector, or the Industry column of a
niftyindices list) adds sector participation. Also: `--as-of DATE` (replay), `--hl-window 252`,
`--div-window 20`, `--div-min-pct 1.0`, `--benchmark NAME` (yfinance; NIFTY by default when fetching).

## 2. Getting the data

- **Constituents:** niftyindices.com, each index page, "Index Constituent" CSV (for example
  `ind_nifty500list.csv`, with Company Name, Industry and Symbol columns). Pass it straight to
  `--universe-file` or `--members`.
- **Exchange-wide A/D (`--ad-csv`):** NSE and BSE show daily advances, declines and unchanged counts,
  and 52-week high/low lists, on their market-data pages. nseindia.com blocks scripts, so copy the
  numbers by hand or find them with WebSearch in market-wrap reports, citing the source. Columns:
  `Date,Advances,Declines[,Unchanged,New 52W Highs,New 52W Lows,NIFTY 50]`. Any case or spacing
  works, and the index column feeds the divergence check. This mode gives A/D, McClellan, thrust and
  highs/lows but no DMA participation (that needs per-stock prices).

## 3. What it measures

| Metric | Definition in breadth.py |
|---|---|
| % above 20/50/200 DMA | Stocks with close > N-day SMA ÷ stocks with ≥ N bars. Change over 5 and 20 sessions in points |
| Uptrend ratio | % of stocks with close > 50 DMA > 200 DMA (stocks with ≥ 200 bars) |
| Advance / decline | Close vs that stock's previous close; equal = unchanged. A/D line = running sum of A − D (read its slope, not its level) |
| Divergence | Over `--div-window` sessions: index up ≥ 1% while the A/D line falls = **bearish**; index down ≥ 1% while it rises = **bullish** |
| New 52w highs/lows | Today's high above every high of the prior 251 sessions (lows mirrored). Only stocks with 252 bars count |
| McClellan | RANA = 1000 × (A − D)/(A + D). Oscillator = EMA19(RANA) − EMA39(RANA) (smoothing 0.10/0.05, SMA-seeded). Summation = running sum of the oscillator from the first value |
| Breadth thrust | 10-session EMA of A/(A + D) closes above 0.615 having been below 0.40 within the previous 10 sessions (Zweig's thresholds). "Armed" = below 0.40 recently, window still open |
| Sector participation | A sector participates when ≥ 50% of its members are above their 50 DMA |
| Circuit suspects | Zero-range bar (high = low) with a move ≥ 1.9%: probably locked at a price band |

Ratio adjustment lets a 50-stock list and exchange-wide counts share one McClellan scale. The summation
level depends on where the data starts, so read its direction and zero crossings.

## 4. Health score (0–100)

| Component | Weight | Scaling |
|---|---|---|
| Participation | 25 | 0.2 × %>20 DMA + 0.4 × %>50 DMA + 0.4 × %>200 DMA |
| Uptrend ratio | 15 | 10% → 0, 60% → 100 |
| Participation trend | 10 | 20-session change in %>50 DMA: −25 pts → 0, +25 → 100 |
| A/D line | 15 | 20-session (A − D)/(A + D): −0.25 → 0, +0.25 → 100 |
| McClellan | 10 | oscillator −100 → 0, +100 → 100 |
| Highs vs lows | 15 | 10-session new highs ÷ (highs + lows); none of either = 50 |
| Sectors | 10 | % of sectors participating |

Missing components (no members, short history, `--ad-csv`) are dropped and the rest re-weighted.
"Coverage" shows how much weight was scored, and under 50% the read is A/D-only. Labels: 75+ Broad
participation, 60–74 Healthy, 40–59 Mixed, 25–39 Narrow / weak, below 25 Very weak. The scalings
are judgement calls, not fitted values, so compare a universe with its own history (`history`).

## 5. Reading breadth in India

- **Index vs broad market.** The top six names (HDFC Bank, ICICI Bank, Reliance, Infosys, Bharti
  Airtel, L&T) are about 40% of NIFTY 50, so heavyweight-led rallies are common (2018: smallcaps fell
  hard while NIFTY made highs). Run one folder three ways: NIFTY 50, NIFTY 500, midcap/smallcap lists.
  NIFTY near highs with NIFTY 500 %>50 DMA under 40% and falling, or a bearish A/D divergence, is a
  narrowing market; the script flags an index above its 50 DMA with under 40% of stocks above theirs.
- **Survivorship bias.** Today's constituent list omits stocks dropped after falling and includes
  ones added after rallying, so past breadth looks stronger than it was. Treat long `history` as rough.
- **Circuit-locked stocks.** A stock frozen at its 5/10/20% band counts as an advance or decline
  but nobody could trade it. Clusters of lower circuits in SME, ASM/GSM or small names exaggerate
  declines, so check the circuit-suspect line before reading a washout.
- **F&O ban names** (open interest above 95% of the market-wide limit) still trade in cash and stay
  in the counts. Their sharp moves are stock events, not breadth.
- **How many stocks.** Each stock is 100/N points: 2 points in NIFTY 50, 0.2 in NIFTY 500. Use 100+
  for stable percentages and 200–500 for McClellan and thrust, or use `--ad-csv` exchange counts.
  Ten stocks give a sketch, not a signal.

## 6. How other skills use this

- **`market-regime`** sets the exposure ceiling; breadth adjusts within it. Confirmed uptrend with a
  score under 40 or a bearish divergence: act one notch lower (fewer, smaller new positions). In a
  Correction or Rally attempt, count a thrust as supporting evidence for a follow-through day. Score
  60+ with %>50 DMA rising backs the uptrend.
- **`market-pulse`:** the "Breadth" line quotes exchange A/D for the day, NIFTY 500 %>50/200 DMA, the
  score and label, and any divergence or thrust. Don't infer breadth from index points.
- **`india-market-analyst`:** put the breadth label next to the regime in the context line. In a
  narrow market, prefer leaders in participating sectors and cut size in small caps.
- **`breakout-planner`:** in a narrow tape (under 40% above the 50 DMA) demand stronger relative strength.
- **`sector-rotation`** has per-sector member breadth (its `breadth` sub-command); this is the market view.

## Caveats

- Stale or suspended stocks (no bar on the last date) are excluded and listed. Use split-adjusted
  daily bars after 15:30 IST: a raw split looks like a crash, a partial day distorts A/D.
- Thresholds (0.40/0.615 thrust, 19/39 McClellan, 52-week window) are US-born conventions applied to
  Indian data. Replay past turns with `--as-of` (Mar 2020, mid-2022, early 2025) before you rely on them.

## Output

```
Breadth: [universe, N stocks / exchange A/D] to [date] | score s/100 [label] (coverage c%)
%>20/50/200 DMA a/b/c (20-session change) | uptrend u% | A/D adv/dec, 20s net, divergence [flag]
NH/NL today and 10s | McClellan osc, summation trend | thrust [state] | sectors k/m participating
Read: [one line] | Regime fit: [how it shifts the market-regime exposure ceiling]
```

_Educational analysis, not investment advice. Data: [sources + timestamps]._
