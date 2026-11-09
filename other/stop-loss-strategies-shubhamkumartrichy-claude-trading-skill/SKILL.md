---
name: stop-loss-strategies
description: |
  Initial stop-loss placement and execution for NSE/BSE stocks and F&O: structure, ATR, S/R and
  moving-average stops with buffers, plus Indian execution realities — SL vs SL-M vs GTT, DAY validity
  of stop orders, gap and circuit risk, closing-basis stops on a 30-minute VWAP close, stop-hunting
  around round numbers and OI strikes, and option premium vs underlying stops.

  Use when the user asks: "where should I put my stop-loss", "stop for X", "how do I protect this
  trade", "GTT or SL order", "my stop didn't trigger / got skipped", "stop on my option", or anything
  about initial stop placement for Indian equity or F&O trades.
---

# Stop-Loss Strategies

Decide the stop before entry. It caps loss when the trade thesis is wrong. It is not a price
prediction.

## 1. Where (method)

| Method | Best for | Long-side rule |
|---|---|---|
| **Structure** (preferred) | Swing trades with clear swings | Below the swing low that invalidates the idea − buffer |
| ATR | No clean structure, volatile names | Entry − 1.5–2.5 × ATR(14) |
| S/R | Ranges, well-tested levels (≥2 touches) | Below support × (1 − buffer) |
| Moving average | Trend-following | Daily close below SMA20 (fast), SMA50 (medium), SMA200 (positional) |

**Buffers:** 0.5% for large caps, 1% for mid/small caps, and 1.5–2% for illiquid names (under about
₹5 crore daily value). Don't place the stop exactly at round numbers (₹1,000, NIFTY 24,500) or at the
biggest put-OI strike. Those are where everyone else's stops sit and where stop-hunting wicks reach.
Go beyond them.

Get levels and ATR from `ta.py summary`. It prints ATR stops and the structure stop with buffer.

## 2. Validation

- [ ] At least 1 ATR from entry (otherwise it sits inside daily noise).
- [ ] Wider than the typical overnight gap (`ta.py summary` prints 60-day gap statistics).
- [ ] The resulting size keeps risk ≤ 1–2% of capital (`risk.py size`).
- [ ] R:R ≥ 1.5–2 after costs (`risk.py rr`).
- [ ] It sits beyond a real technical level, not at a convenient round number.

## 3. How (Indian execution mechanics)

- **SL orders are DAY orders.** A stop-loss order for a delivery (CNC) holding expires at 15:30. For a
  stop that lives across days, place a **GTT** (good-till-triggered; Zerodha, Groww, Upstox, Dhan and
  others support it), or re-enter the SL every morning.
- **GTT on trigger places a LIMIT order.** If the stock gaps below both trigger and limit, it won't
  fill. Set the GTT limit 1–2% below the trigger in volatile names, and watch results days manually.
- **SL (stop-limit)** needs a limit beyond the trigger, for example trigger ₹980 and limit ₹975. A
  zero-gap SL often fails to fill in fast moves.
- **SL-M (stop-market)** is blocked by many brokers for options and illiquid contracts, and has
  caused freak fills. Prefer SL-limit.
- **Closing-basis stops** use the daily close, which on NSE is the VWAP of 15:00–15:30. Check near
  15:20–15:25 and exit in the closing session if the stop is breached. The post-close session
  (15:40–16:00) trades only at the official close.
- **Circuits.** In a lower circuit there are no buyers, so no stop executes. For band-limited stocks,
  size smaller instead of trusting the stop.
- **MIS positions** auto-square around 15:15–15:25 regardless of your stop, often for a fee. Exit
  yourself first.

## 4. F&O stops

- **Futures:** stop on the underlying or futures chart with the same methods. Use SL-limit with a
  buffer. Freeze-quantity limits apply to large orders.
- **Long options:** stop on the **underlying level** that invalidates the view, not a fixed premium %,
  because premium moves are non-linear and theta erodes it. Add a time stop: exit if the move hasn't
  happened within N sessions.
- **Short options:** define the exit as underlying crossing a level, or premium reaching 1.5–2× the
  credit. Use hedges (spreads) so the worst case is capped even if the stop fails on a gap.
- Illiquid strikes have wide spreads. Market stops there can fill far away.

## 5. Hard rules

1. Max loss per trade is 1–2% of capital (≤1% with leverage).
2. **Never widen a stop.** Only tighten it or leave it.
3. When the closing-basis stop is breached, exit in the closing session or at the next open. Don't wait
   for "one more day".
4. Set the stop before entry. Don't move it on emotion after entry.
5. Put the stop in the system (GTT or SL). A mental stop plus an alert is acceptable only if you will
   actually watch the market.

## Output

```
Stop: ₹S (method: structure below swing low ₹L dd-mmm − 0.5% buffer)
Distance: ₹d (x% | y ATR) | wider than 60-day max gap? yes/no
Execution: GTT trigger ₹S, limit ₹S−b (or SL trigger/limit for today), closing-basis check at 15:25
Validation: size ok (risk r%) | R:R after costs z
```
