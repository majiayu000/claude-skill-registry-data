---
name: dv360-pacing-and-optimization
description: Diagnose and fix pacing, and run the optimization loop in DV360. Use when the user asks about pacing, under-delivery, over-delivery, spend is behind or ahead, a campaign that will not spend its budget, impression loss, even vs ASAP vs ahead pacing, daily vs flight pacing, how to optimize a campaign, why a line item is underpacing, or how to reallocate budget. Covers the pacing math (even daily target, expected spend to date, pacing index) and the ordered fix trees for under and over-delivery.
---

# DV360 pacing and optimization

Keep spend on track to the flight and steer it toward the KPI. This skill encodes pacing settings, the pacing math, ordered fix trees for under-delivery and over-delivery, and the daily optimization loop. A pacing problem is almost always a delivery constraint upstream, so the discipline is to read the impression loss breakdown before touching bids.

For shared definitions (CPM, win rate, the KPI math) see the `programmatic-foundations` skill. This skill ships a `pacing_calculator.py` helper for the arithmetic.

## When to use this skill

Use when the user wants to:

- Diagnose under-delivery (spend behind) or over-delivery (spend ahead, or budget gone too fast).
- Choose or change a pacing setting (ASAP, even, ahead of schedule; daily vs flight; amount vs impressions).
- Compute even daily target, expected spend to date, or a pacing index.
- Read the impression loss breakdown and decide what to fix.
- Run an optimization cadence over a flight.

Boundary with sibling skills:

- For pulling and scheduling the underlying reports and metric definitions, use `dv360-reporting`. This skill reads the numbers; that skill produces them.
- For deep no-delivery, low-win-rate, viewability, and creative-disapproval playbooks, hand off to `dv360-troubleshooting`. This skill orders the likely causes; that skill is the exhaustive runbook.
- If a fix is "loosen the frequency cap" or "relax brand safety or viewability," make the change with `dv360-frequency-and-brand-safety`, which owns those controls.

## Quick reference

| Symptom | First check | Likely fix |
| --- | --- | --- |
| Spend behind flight | Impression loss breakdown | Raise bid or budget, widen targeting, loosen the binding filter |
| Spend gone too early | Pacing setting and bid | Switch ASAP to even, lower bid, tighten audience or cap |
| Pacing index < 1.0 | Expected vs actual spend | Diagnose the loss category, then act |
| Lost to auctions / below min bid | Bid vs floor, win rate | Raise bid or bid strategy target |
| Lost to budget / pacing | Daily cap, flight budget | Raise daily cap or reallocate budget |
| Lost to frequency | Frequency cap | Loosen cap (in `dv360-frequency-and-brand-safety`) |
| Lost to viewability / brand safety | Viewability threshold, exclusions | Relax the control to the KPI level |
| Lost to no eligible creative | Creative status and specs | Fix or add a compatible creative |

## Pacing settings

Set pacing at the insertion order and the line item. The IO budget caps the combined line item spend regardless of individual line item budgets, the same way it caps frequency.

- **Pacing type:**
  - **Even** spends a steady amount each day, scaling to daily inventory availability. The default for most flighted delivery.
  - **ASAP** spends as fast as inventory allows (roughly an order of magnitude faster than even). Use to capture limited or time-sensitive inventory, or to recover a badly behind flight, knowing it front-loads spend.
  - **Ahead of schedule** targets up to about 120% of the even daily amount to finish the budget before inventory or competition tightens late in the flight.
- **Pacing period:** daily (spend the daily amount each day) or flight (spend the whole budget across the flight). Daily gives smoother control; flight gives the system more room.
- **Budget unit:** amount or impressions. An IO and its line items must use the same unit.

## Pacing math

Run the numbers before adjusting anything; "behind" is only meaningful against an expected position. The `pacing_calculator.py` script computes all of these from a budget, flight dates, an as-of date, and spend to date.

- **Even daily target** = remaining budget / remaining days. At flight start this equals total budget / total flight days. Recomputing on remaining budget and days is what lands the flight exactly on budget after a slow or fast stretch.
- **Expected spend to date** = even daily target at flight start times days elapsed. Where even pacing would have you today.
- **Pacing index** = actual spend / expected spend to date. 1.0 is on pace, below 1.0 is behind (under-delivery), above 1.0 is ahead (over-delivery). Treat roughly 0.95 to 1.05 as on pace and investigate outside that band.
- **Projected end-of-flight spend** = current daily run rate times total flight days. If this lands below budget, you will under-deliver unless the daily target rises.

Count flight days inclusive of both the start and end date, because that is how the flight is booked.

## Under-delivery: ordered causes and fixes

Work top down. Each cause is roughly ordered from most common and cheapest to fix, to least. Confirm the cause in the impression loss breakdown before acting, so you fix the binding constraint and not a symptom.

1. **Budget or daily cap too low.** A daily cap below the even daily target throttles delivery. Raise the daily cap or reallocate budget from an underperforming line item.
2. **Bid too low / losing auctions.** Lost-to-auction or below-minimum-bid loss means you are priced out. Raise the bid or the bid strategy target (see `dv360-bid-strategy`).
3. **Targeting too narrow.** A small audience or tight geo/device/contextual filter starves the line item. Broaden the most restrictive dimension.
4. **Frequency cap too tight.** Frequency-limited loss means the cap is exhausting available users. Loosen it in `dv360-frequency-and-brand-safety`.
5. **Viewability or brand-safety filters too strict.** High predicted-viewability targeting or aggressive exclusions cut the eligible pool. Relax the control to the KPI level, not below it.
6. **Deal not delivering.** A PMP or Programmatic Guaranteed deal can under-supply. Check deal status and inventory in `dv360-deals-and-inventory`.
7. **Creative disapproved or missing.** No-eligible-creative loss means the line item cannot serve. Fix the disapproval or add a compatible creative.

## Over-delivery: causes and fixes

1. **ASAP pacing front-loading spend.** Switch to even (or ahead) so the budget lasts the flight.
2. **Bid too high.** Winning expensive impressions burns budget fast. Lower the bid or bid strategy target.
3. **Audience too broad.** A wide pool plus a healthy bid over-delivers. Tighten targeting.
4. **Frequency cap too loose.** Spending repeatedly on the same users. Tighten the cap.

## Optimization workflow

1. **Monitor pacing vs flight and performance vs KPI together.** Pacing is the rate of spend toward budget; performance is the value from impressions bought. They are different questions; a line item can pace perfectly and miss the KPI, or hit the KPI while underpacing. Read both.
2. **Compute the pacing index** with the script. If outside 0.95 to 1.05, treat it as a delivery problem to diagnose, not a number to force.
3. **Read the impression loss breakdown** to see where impressions are lost: auctions, below minimum bid, budget or pacing, frequency, viewability, brand safety, or no eligible creative. This names the binding constraint.
4. **Segment by dimension** (exchange, device, app or URL, geo, creative) to find where the loss or the underperformance concentrates, rather than adjusting the whole line item blindly.
5. **Act on one lever at a time:** bid, budget reallocation, targeting, or creative. Changing several at once makes the next read uninterpretable.
6. **Re-check after the system settles.** Optimization-view data can lag (it can take up to about three days to populate after setup), and bid strategies relearn after a change, so do not stack changes faster than you can read their effect.

Cadence: daily in week one while delivery stabilizes, then a few times a week through the middle of the flight, then watch more closely near the end when the remaining-days math makes each day's target swing harder.

## Decision rules and thresholds

- **Pacing index bands:** below 0.95 is behind, above 1.05 is ahead, between is on pace. The further from 1.0 and the later in the flight, the more urgent, because fewer remaining days mean a larger daily correction.
- **Recovering a behind flight:** prefer raising the bid or daily cap and loosening the single binding filter over switching to ASAP, because ASAP front-loads and can over-correct. Use ASAP only when inventory is genuinely scarce or time-boxed.
- **One change per read.** Adjust a single lever, let it settle, re-read. This keeps cause and effect legible and protects bid-strategy learning.
- **Fix the named loss category, not a guess.** If loss is dominated by below-minimum-bid, more budget will not help; the bid is the constraint. If loss is budget or pacing, a higher bid wastes money; raise the cap or reallocate.

## Reference material

- `scripts/pacing_calculator.py`: computes even daily spend, expected spend to date, pacing index, projected end-of-flight spend, and the recommended new daily spend to finish exactly on budget. Run it with `--help` for usage. Use it whenever the user gives a budget, flight dates, and spend to date.

## Templates and examples

**Underpacing line item, mid-flight.** A $30,000 line item runs 2026-06-01 to 2026-06-30. On 2026-06-10, $8,000 is spent. Run:

```
python3 scripts/pacing_calculator.py --budget 30000 --start 2026-06-01 --end 2026-06-30 --as-of 2026-06-10 --spend 8000
```

Output: even daily target $1,000, expected to date $10,000, pacing index 0.80 (behind), projected end-of-flight $24,000, recommended new daily $1,100 for the remaining 20 days. The line item is behind and would leave $6,000 unspent. Next step: read the impression loss breakdown. If loss is dominated by lost-to-auction, raise the bid; if by budget or pacing, raise the daily cap toward the new $1,100 target; if by frequency or viewability, loosen that control in `dv360-frequency-and-brand-safety`.

**Over-delivering insertion order.** Budget is spending at a 1.30 pacing index four days in, set to ASAP. The deal it targets is not scarce. Fix: switch the IO to even pacing so the budget lasts the flight, and lower the bid if the index stays high after the change. Re-read after the system settles before any further change.

**Even-paced but underperforming.** Pacing index 1.00 but cost per action is above the KPI. Pacing is fine, so do not touch budget. Segment by exchange and creative, find where the bad outcomes concentrate, and act on bid or creative there. This is a performance problem, handed in part to `dv360-bid-strategy`.

## Common pitfalls

- Reacting to "behind" without computing expected spend. Early in a flight a low absolute spend can still be on pace. Run the index first.
- Reading pacing and ignoring performance, or the reverse. They answer different questions; check both.
- Changing bid, budget, and targeting at once, then being unable to tell what worked. One lever per read.
- Throwing budget at a line item whose loss is below-minimum-bid. Wrong constraint; raise the bid.
- Switching to ASAP to recover a behind flight and then over-delivering early. Prefer bid, cap, and a single filter loosen first.
- Re-tuning faster than data populates or a bid strategy relearns, churning without signal.

## Sources

- Set budgets and control your pacing: https://support.google.com/displayvideo/answer/3114676 (as of June 2026)
- Use the Optimization view: https://support.google.com/displayvideo/answer/7563784 (as of June 2026)
- Difference between performance and pacing: https://support.google.com/displayvideo/answer/2697800 (as of June 2026)
- Monitor impression loss: https://support.google.com/displayvideo/answer/3103324 (as of June 2026)
