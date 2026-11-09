---
name: options-strategies
description: |
  Choosing, sizing and managing option strategies on NIFTY, BANKNIFTY, SENSEX and stock options in
  India: a view × volatility selection matrix, defined-risk structures (spreads, iron condors,
  butterflies, calendars), covered calls and protective puts, expiry-day (Tuesday/Thursday) behaviour,
  adjustments, margin benefits of hedging, and event playbooks (Budget, RBI, results). options.py
  payoff computes max profit/loss, breakevens, probability of profit and position Greeks.

  Use when the user asks: "which option strategy", "sell a straddle/strangle", "iron condor for this
  week", "bull call spread on X", "hedge my portfolio with puts", "covered call on my holdings",
  "adjust my position", or wants a payoff/breakeven for a multi-leg trade.
---

# Options Strategies (India)

Pick the structure from **view × volatility × capital**, then size it on **maximum loss**.

## Payoff calculator

```bash
# Leg = SIDE,TYPE,STRIKE,PREMIUM[,LOTS]   (TYPE = CE | PE | FUT)
python3 ../fno-options-analysis/scripts/options.py payoff --underlying NIFTY --spot 23050 \
    --leg S,CE,23500,48 --leg B,CE,23700,20 --leg S,PE,22600,52 --leg B,PE,22400,24 \
    --iv 15 --expiry 2026-11-03
python3 ../fno-options-analysis/scripts/options.py payoff --lot-size 250 --spot 1400 \
    --leg B,FUT,1400 --leg B,PE,1360,22                 # stock protective put (lot size from contract file)
```
Output: net credit or debit, max profit and loss (detects unlimited), expiry breakevens, lognormal
probability of profit, and position Greeks. **Margin is not modelled.** Use the broker's basket margin
calculator or the MCP margin tool. Hedged structures get large SPAN benefits.

## Selection matrix

| View ↓ / IV → | Low IV (VIX < 13) | Normal | High IV (VIX > 18) |
|---|---|---|---|
| Strongly bullish | Long call, bull call spread | Bull call spread | Bull put spread (credit) |
| Mildly bullish | Bull call spread | Bull put spread | Bull put spread, covered call |
| Neutral / range | Calendar (long vega), butterfly | Iron condor, iron fly | Iron condor (wider wings), short strangle **hedged** |
| Mildly bearish | Bear put spread | Bear call spread | Bear call spread |
| Strongly bearish | Long put, bear put spread | Bear put spread | Bear call spread |
| Big move, unsure of direction | Long straddle/strangle (before events) | Long strangle | Avoid buying (IV crush) |
| Holding stock, want protection | Protective put / collar | Collar | Collar (sell call to fund put) |

## Indian expiry dynamics

- **Weekly NIFTY expires Tuesday; SENSEX Thursday.** Theta is steepest in the last 2–3 sessions, and
  gamma on expiry day makes ATM premiums swing 50–200% intraday.
- **Expiry-day trading ("0DTE")** has the worst risk profile for beginners. Small moves wipe out
  sellers, and buyers' premiums decay to zero within hours. The extra 2% ELM on short options raises
  margin that day.
- **Holiday-shifted expiries** (a Tuesday holiday moves expiry to Monday) shorten the week. Check
  `options.py expiries`.
- **Monthly stock options** are physically settled. Never hold ITM stock options into expiry without
  the cash or shares to settle them.

## Construction rules

1. **Defined risk by default.** Every short option gets a long hedge (a spread or condor wings) unless
   the user has substantial capital and explicitly wants naked exposure. Hedges also cut margin by
   60–80%.
2. **Strikes from data:** place short strikes beyond the 1σ expected move (`options.py move`) and beyond
   chart and OI levels. Place wings 100–300 points away on NIFTY (strike interval 50) and 300–1,000 on
   BANKNIFTY (interval 100).
3. **Liquidity:** use strikes with tight bid-ask spreads and high OI. Far-OTM weekly strikes are cheap
   for a reason.
4. **Size on max loss:** total max loss ≤ 1–2% of capital (`position-sizing`). One NIFTY iron condor
   with 200-point wings risks up to roughly ₹13,000 minus the credit, so a ₹5 lakh account should run
   at most one.
5. **Costs:** four legs means four orders each way, so ₹160 brokerage round trip plus STT on sells
   (`trading-costs`). That matters for low-credit condors.

## Management

| Situation | Action |
|---|---|
| Credit trade reaches 50–70% of max profit | Close it. The remaining reward isn't worth gamma risk |
| Short strike tested (price within ~0.5σ) | Roll the untested side closer, roll out in time, or close |
| Loss reaches 1.5–2× the credit received | Exit. Don't "adjust" a losing trade into a bigger one |
| Debit trade has lost 50% with no move | Exit. Theta keeps working against you |
| Event tomorrow (Budget, RBI, results) | Reduce or close shorts, or hedge with wings. Gaps skip adjustments |

## Event playbook

- **Union Budget (1 Feb), RBI policy (6 meetings a year), state or general elections, US Fed:** IV
  rises into the event and collapses after it. Long straddles bought just before often lose even on a
  decent move. Credit spreads sold **after** the event capture the crush.
- **Stock results:** stock option IV rises into results. Prefer defined-risk spreads, and remember the
  stock can move 5–15%.

## Disclosure

Remind users that most individual F&O traders lose money (SEBI: about 91% in FY25, about 88% in FY26),
and that strategies with high win rates often have large tail losses.

## Output

```
Strategy: [name] on [underlying] exp [date, weekday]  (view: .., IV regime: VIX ..)
Legs: SELL 1 × 23500 CE @48 | BUY 1 × 23700 CE @20 | ...
Net credit ₹.. | Max profit ₹.. | Max loss ₹.. | Breakevens .. / ..
POP ≈ ..% | Greeks Δ .. Θ ../day Vega ..
Margin: check basket calculator (hedged) | Costs ≈ ₹..
Plan: take profit at ..% | exit if .. | event risk: ..
```
