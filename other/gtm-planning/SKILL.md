---
name: gtm-planning
description: Turn "what's the plan" into a GTM plan you can defend, verdict-first. Names the two or three bets, the motions behind each, the targets, the capacity math that says whether the number is reachable, and the risks that would break it. Built for B2B GTM leaders, customizable to your model and stage. Trigger on "build our GTM plan", "plan the quarter", "is this number reachable", "what are our bets", "annual GTM planning", "do we have the capacity", or any planning cycle.
---

# GTM Planning

## What this does
Takes your target and your constraints and structures the plan behind them. It forces the plan down to the two or three bets that actually matter, names the motion behind each, sets the targets, runs the capacity math that tells you whether the number is even reachable with the team you have, and lists the risks that would break it. It leads with the verdict: reachable, reachable-if, or not with this capacity.

## What you'll need
You do not need to connect anything to get value today. Bring your target and your team and the skill runs now. Connect the tools below and it pulls the history automatically and grounds the math.

- Works today with: the target, the team you have or plan to hire, your average deal size, your win rate, and your sales cycle. Paste them or upload a simple sheet.
- More powerful connected to a CRM: it reads your real win rate, deal size, and cycle instead of using estimates, so the capacity math is grounded.
- Sharper with a product-analytics tool: adds real funnel conversion so the top-of-funnel target is not a guess.
- Sharper with a data-enrichment source: sizes the addressable market so the bets are checked against reality, not hope.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the numbers you give it today and gets more powerful as you connect tools. It never invents a rate it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste your target, team, and historical rates. The skill runs the full plan and capacity math today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls your real win rate, deal size, and cycle so the math is grounded, not estimated. Same output, less effort, sharper.
- **Just exploring**: no numbers yet? Get the framework, the capacity formula, and a worked example on sample inputs, so you can see the shape before you fill it in.

Every run ends with the one thing that would make the next run sharper, a number to confirm or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org planning a quarter or a year against a revenue target. Set these to your model:

| Set this | What it is | Default / Example |
|---|---|---|
| PERIOD | the planning window | quarter, half, fiscal year |
| TARGET | the number to hit | new ARR, net revenue, logos |
| MOTIONS | how you go to market | inbound, outbound, partner, expansion |
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| WIN_RATE | close rate by motion | your trailing-quarter actual |
| DEAL_SIZE | average deal | your trailing-quarter actual |
| CYCLE | average days to close | your trailing-quarter actual |
| CAPACITY | reps x ramped productivity | heads x per-rep number, ramp-adjusted |
| BET_LIMIT | how many bets to allow | 3 (a plan with 7 bets has none) |

Set the rates from your own history. Borrowed benchmarks are the fastest way to plan a number you cannot hit.

## The method

### Verdict first
The plan opens with the call: REACHABLE, REACHABLE_IF, or NOT_WITH_THIS_CAPACITY. Everything under it is the evidence. A leader should get the answer in the first line and the reasoning in the rest. No burying the gap on slide 14.

### Two or three bets
The plan is forced down to a BET_LIMIT of two or three bets, each a specific way you intend to hit the number: a segment, a motion, a product line, a geography. A plan that lists everything commits to nothing. Each bet gets a target and an owner.

### Motion per bet
Each bet names the motion that delivers it and the few activities that motion depends on. Outbound bet, it names the account count and the touch model. Expansion bet, it names the base and the trigger. The motion is how the bet actually happens.

### Capacity math
The hard check. Ramped-rep capacity times productivity is compared to the target. Working from the target backward through WIN_RATE, DEAL_SIZE, and CYCLE gives the pipeline and the activity the plan requires, then that is checked against the heads and ramp you actually have. If the math does not close, the verdict is REACHABLE_IF and the gap is named in heads, pipeline, or rate.

### Risks that break it
Three to five risks, each with the assumption it threatens and an early signal that it is going wrong. Ramp slower than modeled, win rate reverts, a bet under-delivers. Risks are tied to the number, not a generic list.

## Quality gates
- The plan opens with the verdict, never with context.
- Bets are capped at BET_LIMIT, each with a target and an owner.
- Capacity math is shown working backward from the target, not asserted.
- Every rate used is labeled as actual or estimate, and estimates are flagged.
- Each risk names the assumption it threatens and the signal to watch.

## Output (example)
```
GTM PLAN · Q_ · target $4.0M new ARR
VERDICT: REACHABLE_IF (short ~1.5 ramped reps, or +8pts win rate)

The bets:
  1. Mid-market outbound      target $2.0M   owner: Sales lead
  2. Install-base expansion   target $1.4M   owner: CS lead
  3. Partner-sourced          target $0.6M   owner: Partnerships

Capacity math (backward from target):
  $4.0M / $40K deal = 100 deals
  100 deals / 25% win = 400 qualified opps needed
  Current ramped capacity covers ~330 opps
  Gap: ~70 opps = ~1.5 reps or an 8-pt win-rate lift

Top risks:
  1. New-hire ramp slips a month -> watch week-6 pipeline per rep
  2. Expansion trigger softer than modeled -> watch base usage trend
  3. Partner motion is unproven -> watch first sourced opp by week 4
```

## Where the numbers come from
The deal size, win rate, and BET_LIMIT here are illustrative, not benchmarks. The capacity formula is real and the one thing you should not skip: target divided by deal size, divided by win rate, gives the opps you need, checked against ramped heads. Feed it your own rates. The framework does not change. The plan is yours.

## Example chat
**You:** Build the Q3 plan, target is $4M new ARR, here's our team and historical rates.

**Claude:** Verdict: REACHABLE_IF, short about 1.5 ramped reps or 8 points of win rate.
```
$4.0M / $40K deal = 100 deals
100 deals / 25% win = 400 qualified opps needed
Current ramped capacity covers ~330 opps
Gap: ~70 opps
```
Three bets: mid-market outbound ($2.0M), install-base expansion ($1.4M), partner-sourced ($0.6M). The gap sits entirely in outbound capacity, not the other two bets, so that's where the hiring conversation actually needs to happen.
One sharpener: connect your CRM so win rate and deal size come from your actual trailing quarter instead of the estimate you gave me.

## Go further
The plan works from the numbers you paste in. Here is where it stops going stale the week after you present it.

- **Recompute the gap as the quarter moves.** A scheduled Claude task reruns the capacity math weekly against live Salesforce pipeline, so the verdict updates before the QBR instead of at it.
- **Ground the rates in real history.** Connect Snowflake or your warehouse so win rate and cycle length pull from actual closed-won data by motion, not a single quarter's estimate.
- **Watch the named risk signals.** Wire Slack alerts to the specific signals named in each risk (new-hire ramp, base usage trend, first sourced partner opp) so a slipping bet surfaces in week 4, not at quarter-end.

The plan stops being a slide and starts being a number you can watch move.

## Make it yours
Fork it. Change the bets, the rates, the risk list. The point is not to present someone else's plan. It is to defend yours, verdict-first, so the room argues about the gap instead of the format. Built by an operator. Customize it, break it, make it better.
