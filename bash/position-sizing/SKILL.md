---
name: position-sizing
description: |
  Position sizing for Indian equity and F&O trades: fixed-fractional risk sizing with round-trip
  costs included, ATR-based stops, F&O lot rounding and margin checks, MTF/intraday leverage
  adjustment, gap-through-stop and circuit risk, Kelly from a trade journal, and portfolio limits.
  risk.py also covers R:R, trailing stops and journal statistics.

  Use when the user asks: "how many shares should I buy", "position size for X", "how many lots of
  NIFTY", "how much to invest", "risk per trade", "can I afford one lot", "Kelly criterion", "what's my
  win rate / expectancy", or any capital-allocation question.
---

# Position Sizing

Sizing decides survival. Risk a small, fixed fraction of capital per trade so that a losing streak,
which will happen, is survivable.

## Calculator

```bash
# Equity, structure stop
python3 scripts/risk.py size --capital 500000 --risk-pct 1 --entry 1450 --stop 1410
# Equity, ATR stop + gap-risk check for a midcap
python3 scripts/risk.py size --capital 500000 --risk-pct 1 --entry 1450 --atr 28 --atr-mult 2 --cap midcap
# NIFTY futures: lot rounding + margin
python3 scripts/risk.py size --capital 800000 --risk-pct 1 --entry 24950 --stop 24800 --lot-size 65 \
    --margin-per-lot 165000 --cost-pct 0.06
# MTF at 3x
python3 scripts/risk.py size --capital 300000 --risk-pct 1 --entry 820 --stop 790 --leverage 3
# Win rate / payoff / Kelly from your journal (date,symbol,side,entry,exit,stop,qty,charges | or pnl)
python3 scripts/risk.py journal trades.csv
```

`--cost-pct` is the round-trip cost as % of entry. Use about 0.25 for delivery, 0.05 for intraday,
and 0.06 for index futures, or compute it exactly with `trading-costs`. Get margin per lot from the
broker's margin calculator or the MCP margin tool, because SPAN changes daily.

## Method 1: fixed fractional (default)

```
Risk budget = Capital × Risk%            (÷ leverage when using MTF/MIS margin)
Units       = Budget ÷ (|Entry − Stop| + cost per unit)
F&O         = floor(Units ÷ lot size) lots
```

| Situation | Risk % per trade |
|---|---|
| Normal swing/positional, no leverage | 0.5–1% (max 2%) |
| New or unproven setup | 0.25–0.5% |
| With MTF/MIS leverage | base risk ÷ leverage (see below) |
| F&O beginners | 0.5%, and only defined-risk structures |
| Total open risk across all positions | ≤ 6% |

**Why divide by leverage?** The loss at the stop doesn't depend on leverage. But leverage lets a
position grow beyond your cash, so a gap through the stop or a margin call hurts far more.
`risk.py --leverage` therefore divides the risk budget by the leverage as a deliberate safety
haircut. Pass `--leverage 1` if you want the plain calculation.

**Example:** capital ₹10 lakh, 2% risk, entry ₹1,800, stop ₹1,700. Without costs that is 200 shares.
With 0.25% round-trip costs, risk per share is ₹104.5, so 191 shares. That is ₹3.44 lakh, 34% of
capital, which breaches the 20% single-stock cap, so cap at about 111 shares unless the user accepts
the concentration.

## Method 2: ATR-based stop distance

```
Stop = Entry − ATR(14) × k         k: 1.5 (calm, ADX<20) | 2.0 (normal) | 2.5 (volatile, ADX>30)
```
Volatile stocks automatically get smaller size. Get ATR from `ta.py summary`.

## Method 3: Kelly (needs 30+ trades of history)

```
Kelly% = W − (1 − W) / R      W = win rate, R = avg win / avg loss
```
Kelly gives the fraction of capital to **risk** per trade, not to invest. Use at most half-Kelly and
never more than 2%. `risk.py journal` computes W, R, profit factor, drawdown and Kelly from a CSV.

## F&O specifics

- **One lot is the minimum unit.** At end-October 2026 levels, one NIFTY lot (65 × ~23,050) is about
  ₹15 lakh notional and one BANKNIFTY lot (30 × ~54,700) about ₹16.4 lakh. If one lot at a sensible
  stop risks more than 1–2% of capital, the answer is **don't trade futures**. Use a defined-risk option spread, or trade the cash stock instead.
- **Option buying:** the premium is the maximum loss. Size so that total premium at risk ≤ risk
  budget, or use a premium stop (for example, exit at −40%) and size on that.
- **Option selling:** size on max loss (spreads) or a stress move (naked; 2–3× the expected move).
  Never size on margin alone.
- **Margin headroom:** keep used margin ≤ 50% of capital. With `--margin-per-lot`, `risk.py size` caps
  lots at that limit automatically (`--max-margin-pct` changes it). Margins rise on volatility spikes, on expiry
  day (+2% ELM on shorts), and for stock F&O in expiry week (physical delivery).
- **50:50 rule:** at least half of F&O margin must be cash or cash-equivalent.

## Indian risk overlays (always check)

1. **Gap-through-stop.** `--cap largecap|midcap|smallcap` (3/5/10%) or `--gap-pct` shows the loss
   if price gaps beyond the stop. Results, global sell-offs and regulatory news gap Indian stocks
   overnight.
2. **Circuits.** In stocks with 5% or 10% bands, a lower circuit can last days, and the stop never fills.
   Cut size so a two-day circuit run (2 × band) stays tolerable.
3. **Liquidity.** Keep the position below about 1% of the stock's average daily traded value. SME and
   illiquid small caps need far smaller sizes.
4. **Correlation.** Three private banks are effectively one position. Apply the sector limit.

## Portfolio limits (hard)

| Constraint | Limit |
|---|---|
| Single stock | ≤ 20% of capital (≤ 10% small caps) |
| Single sector | ≤ 35% |
| Total open risk (sum of stop distances) | ≤ 6% |
| Correlated names in one sector | ≤ 3 |
| F&O margin used | ≤ 50% of capital |

## Output

```
Position: N shares / L lots (qty Q)
Entry ₹E | Stop ₹S (x% away, method) | Value ₹V (y% of capital) | Margin ₹M
Risk if stopped: ₹R (r% incl. costs) | Gap-through loss: ₹G (g%)
Notes: [caps applied, lot too big, leverage adjustment, liquidity]
```
