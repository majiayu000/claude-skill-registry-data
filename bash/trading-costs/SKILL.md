---
name: trading-costs
description: |
  Exact trading charges for Indian equity and F&O trades on NSE/BSE: brokerage (Zerodha, Groww,
  Angel One, Upstox, Dhan or custom), STT, exchange transaction charges, SEBI fee, stamp duty, GST,
  DP charges and MTF interest, plus breakeven price and cost-as-%-of-profit. Includes a calculator
  script with current (Oct 2026) rates, including the 1 Apr 2026 F&O STT hike.

  Use when the user asks "what are my charges", "brokerage for this trade", "breakeven price", "which
  broker is cheapest", "how much does STT cost", "is scalping worth it after charges", "MTF interest",
  or when another skill needs cost-adjusted R:R or P&L.
---

# Trading Costs (India)

Costs are the one part of a trade you know in advance. Compute them exactly, because they decide
whether small-edge strategies (scalping, frequent option trades) are viable at all.

## Calculator

```bash
python3 scripts/charges.py --segment delivery --buy 1800 --sell 1900 --qty 100 --broker zerodha
python3 scripts/charges.py --segment intraday --buy 2450 --sell 2465 --qty 200 --broker all     # compare brokers
python3 scripts/charges.py --segment options  --buy 120 --sell 150 --qty 130 --broker groww     # 2 NIFTY lots
python3 scripts/charges.py --segment futures  --buy 25000 --sell 25100 --qty 65 --exchange NSE
python3 scripts/charges.py --segment mtf --buy 500 --sell 540 --qty 400 --broker zerodha --mtf-days 20 --mtf-funded 100000
python3 scripts/charges.py ... --brokerage-pct 0.05 --brokerage-cap 20      # any other broker
python3 scripts/charges.py ... --json                                       # machine-readable
```

Options prices are **premiums per unit**, and `--qty` is in units (lots × lot size). Pass only `--buy`
or only `--sell` to price one leg. The report shows the breakeven sell price (long) and buy-back price
(short).

## Statutory charges (identical at every broker; verified 31 Oct 2026)

| Charge | Delivery | Intraday | Futures | Options |
|---|---|---|---|---|
| STT | 0.1% buy **and** sell | 0.025% sell | **0.05% sell** (was 0.02% before 1 Apr 2026) | **0.15% of premium, sell** (was 0.1%). Exercised ITM: 0.15% of intrinsic value |
| NSE transaction | 0.00307% | 0.00307% | 0.00183% | 0.03553% of premium |
| BSE transaction | 0.00375% (A/B group) | 0.00375% | 0 | 0.0325% of premium |
| SEBI fee | ₹10 / crore | ₹10 / crore | ₹10 / crore | ₹10 / crore |
| Stamp duty (buy side) | 0.015% | 0.003% | 0.002% | 0.003% |
| GST | 18% on brokerage + transaction + SEBI fee (+ DP charge) | ← | ← | ← |
| DP charge | per scrip per sell day (broker-specific, ~₹13–20 + GST) | — | — | — |

NSE also levies an IPFT (investor protection fund) charge of ₹0.01 per crore, which is negligible.
Contract notes round STT and stamp duty to the nearest rupee.

## Brokerage (per executed order, verified from official pricing pages, Oct 2026)

| Broker | Delivery | Intraday | Futures | Options | DP (pre-GST) | MTF interest |
|---|---|---|---|---|---|---|
| Zerodha | ₹0 | 0.03% or ₹20 (lower) | 0.03% or ₹20 | ₹20 flat | ₹13 | 0.04%/day |
| Groww | 0.1% or ₹20 (lower), min ₹5 | same | ₹20 flat | ₹20 flat | ₹20 | 14.95% p.a. |
| Angel One | 0.1% or ₹20, min ₹5 | same | ₹20 flat | ₹20 flat | ₹20 | 0.041%/day |
| Upstox | ₹20 flat | 0.1% or ₹20 | 0.05% or ₹20 | ₹20 flat | ₹20 | ₹20/day per ₹40k |
| Dhan | ₹0 | 0.03% or ₹20 | ₹20 flat | ₹20 flat | ₹12.5 | 12.49–15.49% p.a. (tiered) |

Brokerage in the cash segment can never exceed 2.5% of trade value (exchange cap). Introductory
offers, plans such as Upstox Plus, and NRI pricing differ. Verify on the broker's page and pass
overrides when needed.

## What the numbers mean (rules of thumb)

- **Delivery round trip ≈ 0.22–0.25%** of value before slippage, mostly STT on both sides. A swing
  trade aiming for 1% gives up about a quarter of it to costs.
- **Intraday equity ≈ 0.03%** in statutory charges plus brokerage. Percentage-capped brokerage
  (0.03% at Zerodha/Dhan, 0.1% at Groww/Angel One) scales down for small orders. Flat ₹20 brokerage
  does not: ₹40 round trip on a ₹10,000 trade is 0.4%.
- **Options:** the sell-side STT (0.15% of premium) and exchange charges (0.0355% of premium) are
  small per trade, but ₹40 brokerage per round trip on a ₹2,000 premium position is 2%. Frequent
  small option trades bleed.
- **Futures:** after the 2026 STT hike, sell-side STT alone is about ₹750 per NIFTY lot (0.05% of
  ~₹15 lakh notional at NIFTY ≈ 23,000). A long round trip breaks even only after about **14 index
  points**, so scalping for 5–10 points loses money.
- **DP charge** is per scrip per day of selling, regardless of quantity. Selling 1 share costs the same
  DP fee as selling 1,000, so avoid tiny partial exits from delivery holdings.
- **MTF interest** of 0.04%/day is about 15% a year. A 30-day MTF hold must beat ~1.2% in interest alone.
- **Hidden costs:** bid-ask spread and impact cost (large in small caps and far OTM options), auto
  square-off fees (often ₹50 + GST), call-and-trade fees, pledge/unpledge fees, demat AMC, and payment
  gateway charges.

## Tax interaction

- STT is **not deductible** from capital gains (listed equity). Brokerage, exchange fees, stamp duty and
  GST are deductible as transfer costs.
- For F&O and intraday (business income), all charges including STT are deductible expenses.
  See `indian-tax-for-traders`.

## Output

```
Charges for [trade]: ₹X total (Y% of turnover, Z% of gross P&L)
  Brokerage ₹.. | STT ₹.. | Exchange ₹.. | Stamp ₹.. | GST ₹.. | DP ₹..
Net P&L: ₹N | Breakeven: ₹B (+P pts)
Cheapest broker for this trade: … (statutory charges are the same everywhere)
```
