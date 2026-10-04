---
name: capacity-model
description: Turn "can we even hit this number" into a capacity model that shows the truth before the quarter does. Models ramped-rep productivity, builds the hiring plan the target requires, states the ramp assumptions plainly, and names the gap between plan and capacity so nobody discovers it in month three. Built for B2B sales and RevOps leaders, customizable to your ramp and your CRM. Trigger on "build a capacity model", "how many reps to hit the number", "what's the hiring plan", "are we capacity constrained", "model the ramp", or any capacity or headcount planning question.
---

# Capacity Modeler

## What this does
Takes your target and tells you whether the team you have, plus the team you plan to hire, can actually produce it. It models productivity per ramped rep, lays a hiring plan against the gap, states the ramp curve so partial-year hires are not counted as full heads, and surfaces the shortfall between what the plan asks and what the capacity can deliver.

## What you'll need
You do not need to connect anything to get value today. Bring your target and current headcount and the skill runs now. Connect the tools below and the productivity and ramp numbers come from your own history instead of a guess.

- Works today with: your target for the period, current rep count, planned hires with start months, average productivity per ramped rep, and a ramp length. Paste it or upload a sheet.
- More powerful connected to a CRM: it reads real per-rep productivity and cycle length instead of a blended average.
- Sharper with an HRIS or ATS: it pulls actual start dates and open reqs so the hiring plan is grounded in reality.
- Sharper with a data warehouse: it splits ramp and productivity by segment and hire source.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the numbers you give it today and gets more powerful as you connect tools. It never invents a productivity rate it cannot see. A missing input is a prompt, not a guess.

- **Bring your data**: paste your target, heads, hires, and ramp. The skill runs the full model today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls historical productivity, cycle length, and start dates automatically, so the ramp and the gap are measured, not assumed.
- **Just exploring**: no data yet? Get the framework, the exact inputs it reads, and a worked example on sample numbers, so you can see the shape before you feed it.

Every run ends with the one input that would make the next model sharper, a segment split to add or a system to connect.

## Customize this for yourself
This was built for a B2B SaaS org with a quota-carrying sales team. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| TARGET | the number to fund | new ARR for the period |
| PRODUCTIVITY | output per fully ramped rep | annual quota-attained per head |
| RAMP_MONTHS | months to full productivity | 3 to 9 by segment |
| RAMP_CURVE | output during ramp | 0 / 25 / 50 / 100 percent by stage |
| ATTAINMENT | expected attainment on quota | 70 to 90 percent, not 100 |
| ATTRITION | planned annual rep loss | 10 to 20 percent |
| HIRE_PLAN | new reqs and start months | by month, with backfills |
| LEAD_TIME | months from req to ramped | hire lag plus RAMP_MONTHS |

Run any ramp shape you like. The skill applies your curve and shows the gap, so point it at your onboarding reality, not a textbook.

## The method

### Ramped-rep productivity
Start from what a fully ramped rep actually produces at expected ATTAINMENT, not at a fantasy 100 percent. This is the unit the whole model rests on. If you have history, use the median, not the top rep, because you cannot staff a plan on your best person.

### The ramp assumptions
State the RAMP_CURVE openly. A rep who starts mid-period does not deliver a full head. Apply the curve month by month so a Q3 hire contributes a fraction, not a whole. Add LEAD_TIME so a req opened today is not producing next month. These assumptions are where optimistic plans hide, so they get shown, not buried.

### The hiring plan to hit the number
Work backward from TARGET. Subtract capacity from existing ramped reps, then fill the remainder with hires, each discounted by ramp and start month. Add backfills for ATTRITION, because a plan that ignores churn is short before it starts. The output is a req schedule with start months, not a single headcount.

### The gap between plan and capacity
Put the target next to what the modeled team can actually produce. Name the shortfall in the currency of the plan and in heads. A gap here is not a failure, it is the number you needed before the quarter to fix it, by hiring earlier, resetting the target, or accepting the miss with eyes open.

## Quality gates
- Productivity uses expected attainment and the median rep, never a 100 percent or top-rep assumption.
- Partial-year hires are discounted by the ramp curve and lead time, never counted as full heads.
- Attrition backfills are in the plan, not an afterthought.
- The gap is stated in both dollars and heads, with the month it opens.

## Output (example)
```
CAPACITY MODEL · full year · illustrative
Source                 Capacity    Note
Ramped reps (10)       $9.0M       median attainment 80%
H1 hires (4)           $2.2M       ramp-discounted, started Q1-Q2
H2 hires (3)           $0.7M       mostly still ramping at year end
Attrition backfill     -$0.6M      2 reps lost, re-ramping

Modeled capacity       $11.3M
Target                 $13.0M
Gap                    -$1.7M      opens in Q3, ~2 ramped heads short

Fix options:
  1. Pull 2 H2 reqs into Q1 so they ramp before the gap opens.
  2. Reset target to modeled capacity and flag it now, not in Q3.
  3. Hold target, accept a Q3 shortfall, and plan the story.
```

## Where the numbers come from
RAMP_MONTHS (3 to 9), ATTAINMENT (70 to 90 percent), and ATTRITION (10 to 20 percent) are defaults, not laws. They suited a mid-market SaaS team. If your onboarding is faster or your reps carry longer cycles, move them. The model logic does not change. The assumptions are yours.

## Example chat
**You:** Can we actually hit $13M this year with our current team plus planned hires?

**Claude:** Ran the model. The honest answer is no, not without a change.
```
CAPACITY MODEL · full year · illustrative
Ramped reps (10)       $9.0M       median attainment 80%
H1 hires (4)           $2.2M       ramp-discounted, started Q1-Q2
H2 hires (3)           $0.7M       mostly still ramping at year end
Attrition backfill     -$0.6M      2 reps lost, re-ramping

Modeled capacity       $11.3M
Target                 $13.0M
Gap                    -$1.7M      opens in Q3, ~2 ramped heads short
```
The number that matters isn't the $1.7M gap, it's that it opens in Q3. That's five months of runway to fix it before anyone discovers it in a missed board number.

**You:** What are the actual options?

**Claude:** Three, in order of how fast they close the gap: pull 2 H2 reqs into Q1 so they're ramped before Q3, reset the target to $11.3M and say so now, or hold the target and plan the shortfall story. One sharpener: connect your CRM's real historical productivity by rep, this run used the median attainment as a placeholder, your actual ramp curve might be faster or slower than 3 to 9 months.

## Go further
Running the model once tells you where the gap opens. Here's how to keep watching it as the year moves.

- **Recompute monthly against actuals.** Connect Salesforce to a scheduled Claude task that reruns the model against real attainment and real hire start dates each month, so the gap forecast tightens instead of staying a January guess.
- **Pull real start dates, not planned ones.** Connect your ATS or HRIS so req-to-ramped lead time reflects actual hiring speed, not the optimistic timeline in the plan.
- **Flag the gap in the board update automatically.** Feed the modeled shortfall straight into your board-update skill so the risk section never has to be reconstructed from memory the week before the meeting.

Catching the gap in month one beats explaining it in month nine.

## Make it yours
Fork it. Change the ramp curve, the attainment, the hire schedule. The point is not to run someone else's capacity math. It is to model yours, with the ramp honest and the gap named early. Built by an operator. Customize it, break it, make it better.
