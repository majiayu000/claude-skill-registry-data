---
name: fno-options-analysis
description: |
  Indian F&O analysis for NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY, SENSEX and stock derivatives: lot
  sizes, holiday-adjusted expiry calendar (NIFTY Tuesday weekly, SENSEX Thursday weekly), option-chain
  reading (OI walls, change in OI, PCR, max pain, ATM straddle, IV skew), India VIX and expected move,
  Black-Scholes Greeks and IV, futures OI buildup, margins, F&O ban, physical settlement and SEBI's
  2024–26 rule changes. options.py computes all of it from numbers or an NSE option-chain CSV.

  Use when the user asks about option chains, PCR, max pain, OI data, India VIX, IV, Greeks, "what is
  NIFTY's expected move", "when is the next expiry", lot sizes, long/short buildup, F&O ban, margin or
  expiry-day rules.
---

# F&O and Option-Chain Analysis (India)

## Contract basics (verified 31 Oct 2026)

| Underlying | Exchange | Lot | Expiries | Notes |
|---|---|---|---|---|
| NIFTY | NSE | 65 | **Weekly Tuesday** + monthly (last Tue) | Among the most traded option contracts globally |
| BANKNIFTY | NSE | 30 | Monthly (last Tue) | No weeklies since Nov 2024 |
| FINNIFTY | NSE | 60 | Monthly (last Tue) | |
| MIDCPNIFTY | NSE | 120 | Monthly (last Tue) | |
| NIFTYNXT50 | NSE | 25 | Monthly (last Tue) | |
| SENSEX | BSE | 20 | **Weekly Thursday** + monthly (last Thu) | |
| BANKEX | BSE | 30 | Monthly (last Thu) | |
| Stock F&O | NSE | varies | Monthly (last Tue) | **Physically settled**, European style |

Index options are European and cash-settled. If an expiry day is a holiday, expiry moves to the
**previous** trading day. 2026 had several Tuesday holidays: 3 Mar, 31 Mar, 14 Apr, 20 Oct, 10 Nov and 24 Nov.

```bash
python3 scripts/options.py expiries NIFTY --count 6          # holiday-adjusted, flags monthly
python3 scripts/options.py lots
```

## Toolkit

```bash
python3 scripts/options.py greeks --spot 23050 --strike 23200 --type CE --iv 14 --expiry 2026-11-03 --lot-size 65
python3 scripts/options.py iv --spot 23050 --strike 23200 --type CE --premium 85 --days 3
python3 scripts/options.py move --spot 23050 --iv 15.3 --days 1          # India VIX → daily 1σ
python3 scripts/options.py chain nifty_chain.csv --spot 23050            # NSE CSV download or simple CSV
python3 scripts/options.py buildup --price-change 1.4 --oi-change 9      # futures OI interpretation
```

- Time uses calendar days to 15:30 IST on expiry. Use `--expiry` for the exact date.
- `--rate` defaults to 6%; pass the current 91-day T-bill yield for precision.
- Chain input: NSE's option-chain page "Download (.csv)", whose columns mirror around STRIKE, or a
  simple CSV with `strike, call_oi, put_oi, call_chg_oi, put_chg_oi, call_ltp, put_ltp, call_iv, put_iv`.
  Broker MCPs that expose chains (Dhan with its Data API, Fyers, the Upstox skill) can be saved to that format.

## Reading the option chain

| Metric | How to read it | Caveats |
|---|---|---|
| **Call OI wall** (max call OI strike) | Writers expect price to stay below it, so it acts as resistance into expiry | Walls migrate intraday; read *change* in OI |
| **Put OI wall** | Support | Same caveat |
| **Change in OI** | Fresh writing shows where conviction is today | Writing vs buying can't be separated from OI alone; use price |
| **PCR (OI)** | >1 means more puts written (supportive); <0.7 call-heavy (bearish lean) | Contrarian at extremes (>1.5 crowded bullish, <0.6 washed out) |
| **Max pain** | Strike where option buyers' total intrinsic value is lowest | Weak magnet; matters most in the last 1–2 sessions |
| **ATM straddle** | Premium sum ≈ market's expected move to expiry | Use alongside IV and VIX |
| **IV / skew** | OTM put IV above OTM call IV is normal (crash protection). Rising skew means fear | Compare to its own history, not to other underlyings |

Combine chain levels with chart levels (`technical-analysis`). A call wall at a round number that is
also a Fib extension and prior resistance is a strong cap.

## India VIX and expected move

India VIX is NIFTY's 30-day implied volatility, annualised on a calendar-day basis.

```
1σ move over N days ≈ Spot × VIX% × √(N/365)
VIX 15.3, NIFTY 23,050, 1 day → ±185 pts (±0.80%); 7 days → ±488 pts
```

| VIX | Regime | Implication |
|---|---|---|
| < 12 | Complacent | Options cheap. Favour debit spreads and long options over naked selling |
| 12–18 | Normal | Both sides workable |
| 18–25 | Elevated | Rich premiums. Defined-risk credit spreads, smaller size |
| > 25 | Fear | Gap risk is extreme. Cut size and avoid naked shorts |

Spikes before the Budget, RBI policy, elections and US Fed meetings usually unwind afterwards (IV crush).

## Greeks (per unit; multiply by lot size)

- **Delta** is the ₹ change per 1-point move, roughly the probability of expiring in the money.
- **Gamma** is delta's sensitivity. It **explodes on expiry day** for ATM strikes, which is why
  Tuesday/Thursday expiries swing wildly.
- **Theta** is daily decay. It accelerates in the last week, and weekly options lose most of their time
  value in the final 2–3 sessions.
- **Vega** is the ₹ change per 1 vol point. It matters around events.

## Futures OI buildup

| Price | OI | Read |
|---|---|---|
| ↑ | ↑ | Long buildup (bullish) |
| ↓ | ↑ | Short buildup (bearish) |
| ↑ | ↓ | Short covering (bullish, often short-lived) |
| ↓ | ↓ | Long unwinding (bearish, often short-lived) |

Exchanges and brokers publish daily buildup lists. Rollover % and cost of carry near monthly expiry
show whether positions are carried forward. **Participant-wise OI** (FII, DII, Pro, Client), published
daily by NSE, shows FII index-futures long/short ratios, which are a positioning gauge.

## Rules that change P&L (SEBI 2024–26)

- Contract value is at least ₹15 lakh at introduction, and lot sizes are revised periodically.
- One weekly index expiry per exchange (NIFTY Tue, SENSEX Thu).
- Option premium is collected upfront from buyers.
- **Expiry day:** an extra 2% ELM on short options, and no calendar-spread margin benefit.
- Intraday position-limit monitoring. OI and the F&O ban have been measured on **delta-based**
  (future-equivalent) OI since Dec 2025. MWPL is reviewed quarterly.
- Pre-open session for current-month futures (09:00–09:08) since Dec 2025.
- **STT from 1 Apr 2026:** futures 0.05% (sell), options 0.15% of premium (sell), and exercised options
  0.15% of intrinsic value. Selling an ITM option before expiry and letting it exercise now cost similar
  STT, so the old "STT trap" is mostly gone.
- **Stock F&O physical settlement:** ITM positions at expiry become delivery or receipt of shares.
  Brokers ramp margins from about 4 sessions before expiry and may square off. Close or roll early.
- **F&O ban:** at more than 95% of MWPL, positions can only be reduced until OI falls below 80%.
- **Retail API algos** need a registered app and a static IP (from 1 Apr 2026).

## Risk reality

SEBI's studies found that **about 91% of individual F&O traders lost money in FY25** (aggregate
losses ≈ ₹1.06 lakh crore), and about 88% in FY26. Mention this when a beginner asks about F&O, and
steer them toward defined-risk structures, small size, and the `position-sizing` rules.

## Output

```
NIFTY [spot] | VIX [x] | next expiry [date, weekday] ([n] sessions)
Chain: PCR x.xx ([read]) | max pain ₹.. | call wall .. | put wall .. | ATM straddle .. → range ..–..
Fresh writing: calls at .., puts at ..
Expected move (1σ): ±.. to expiry
Read: [range/bias], levels that would change it: ..
```
