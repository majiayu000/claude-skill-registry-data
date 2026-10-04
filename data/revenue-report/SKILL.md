---
name: revenue-report
description: Turn raw revenue data into a weekly or monthly wrap-up that drives action, not another dashboard screenshot. Position vs plan, what moved, the risks worth naming, and the specific next moves. Built for B2B revenue teams, customizable to your data and your cadence. Trigger on "write the revenue report", "how did we do this month", "revenue wrap-up", "are we on plan", "monthly number", or any revenue-recap request.
---

# Revenue Report

## What this does
Takes your revenue numbers and writes the recap a leader actually reads: where you stand against plan, what moved since last time, the two or three risks that matter, and the exact next moves. It is a report that ends in decisions, not a chart with no verdict.

## What you'll need
You do not need to connect anything to get value today. Bring your numbers and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: your revenue figures for the period, with a plan or target to measure against, and last period's numbers for the delta. Paste it or upload a CSV.
- More powerful connected to a CRM: it reads closed and committed revenue automatically, deal by deal.
- Sharper with a BI tool or a sheet: pulls the plan, the trend, and the prior periods without a copy-paste.
- Sharper with a billing or finance source: separates new, expansion, and churn cleanly.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your figures (an export, a plan-vs-actual sheet). The skill writes the full recap today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the numbers automatically and adds signals you cannot paste by hand (live pipeline, trend history, segment splits). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org reporting on a recurring-revenue number. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CADENCE | how often you report | weekly, monthly |
| METRIC | the headline number | new ARR, net new ARR, bookings, MRR |
| PLAN source | where the target lives | a BI tool, a plan sheet, a quota field |
| SEGMENTS | how you cut the number | new business, expansion, churn, by region |
| PACING basis | how you read mid-period | linear, or your historical shape |
| PRIOR periods | how far back the trend runs | trailing 3 to 6 periods |
| VARIANCE flag | gap to plan worth naming | +/- 10% (re-tune to your business) |

Report on any metric you like. The skill measures position against your plan and explains the movement, so point it at your number, not anyone else's.

## The method

### Position vs plan
State the headline number, the target, and the gap, in that order. Ahead, on, or behind, with the percentage. If the period is not over, show pacing: where the number sits versus where a normal period would have it by now. Never call a mid-period number a miss without a pacing basis.

### What moved
Compare to last period and name the drivers. Did new business carry it, did expansion, did churn drag it down? Attribute the change to a cause you can see in the data, not a vibe. If you cannot see the cause, say so.

### The risks
Two or three, not ten. A risk is something that threatens the next period's number: thin pipeline, a slipping large deal, a churn spike, a segment falling behind. Each risk gets a size, so the reader knows what is at stake.

### The next moves
Every report ends in moves, each one owned and specific. "Chase the three deals inside the period" beats "improve pipeline." A recap with no moves is a screenshot.

## Quality gates
- No "miss" or "beat" on a mid-period number without a stated pacing basis.
- Every driver ties to a number you can show, never an unsourced claim.
- Risks are sized. A risk with no magnitude is a worry, not a risk.
- Next moves are owned. An action with no owner does not happen.

## Output (example)
```
REVENUE REPORT · Month to date
Headline      New ARR $420K vs $500K plan  ·  84%, behind
Pacing        On track for ~$465K at current run rate
Moved         +18% vs last month, carried by expansion ($140K)
              New business flat, churn steady

Risks
  1. Two deals worth ~$90K slipped past the close date. Period-defining.
  2. New-business pipeline for next month is thin, ~0.8x coverage.

Next moves
  1. Sales lead: pull the two slipped deals into a same-week decision.
  2. Marketing: name the source of next month's pipeline gap by Friday.
```
(Figures illustrative.)

## Where the numbers come from
The variance flag (+/- 10%) and the trailing-period window are defaults, not laws. They suited a monthly SaaS cadence. If your business is lumpier, widen the flag. If you report weekly, shorten the window. The logic does not change. The thresholds are yours.

## Example chat

**You:** Write this month's revenue report. Here's the CSV, $420K against a $500K plan.

**Claude:** Written. You're behind on the headline, but the pacing math says it's not as bad as the raw percentage looks.
```
REVENUE REPORT · Month to date
Headline      New ARR $420K vs $500K plan  ·  84%, behind
Pacing        On track for ~$465K at current run rate
Moved         +18% vs last month, carried by expansion ($140K)

Risks
  1. Two deals worth ~$90K slipped past the close date. Period-defining.

Next moves
  1. Sales lead: pull the two slipped deals into a same-week decision.
```
Worth naming: I didn't call this a "miss" outright, because the period isn't over. Pacing says you land near $465K at the current run rate, that's a different conversation than 84% sounds like.

**You:** Why did you call out expansion specifically instead of just "revenue grew"?

**Claude:** Because "revenue grew" doesn't tell your lead what to do next. Expansion carried the month while new business stayed flat, that's a different set of next moves, protect the expansion motion, go fix new-business pipeline, than if new business had carried it. Sharpener: connect your CRM and I'll pull the two slipped deals by name instead of just the dollar total, so the next move has an owner attached.

## Go further
The recap earns a read. Here is the version that writes itself every period.

- **Run it every Monday morning automatically.** Schedule a Claude task against your BI export so the report is in your leader's inbox before the pipeline review starts.
- **Name the slipped deals, not just the total.** Connect Salesforce so the risks section lists the actual opportunities and owners instead of a dollar figure.
- **Post it where the team already looks.** Send the finished report to Slack instead of a doc nobody opens until the next meeting.

The report shows up with the next move attached before anyone has to ask for it.

## Make it yours
Fork it. Change the metric, the segments, the cadence. The point is not to run someone else's report. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
