---
name: revenue-reporting
description: Turn revenue reporting from a rear-view mirror into an operating rhythm. It narrates where you are against target, decomposes the variance by channel, reads your forecast for where you land, then adds an action layer of hot leads and deals to work now. Built for GTM teams reporting on ARR and bookings, customizable to your sheet and your metrics. Trigger on "weekly revenue wrap-up", "monthly revenue report", "how are we pacing", "revenue position", "forecast confidence", "run the weekly report", or any ARR, bookings, pipeline, or channel-performance review.
---

# Revenue Reporting

## What this does
Reports the number, then tells you what to do about it. It leads with total ARR against target, splits the gap into the channels and sub-channels driving it, compares what has closed to what is forecast to where you need to land, and closes with an action layer: the hot leads and the deals that need a push this week. It turns a backward-looking wrap-up into the rhythm the team actually runs on.

## What you'll need
You do not need to connect anything to get value today. Bring your numbers and the skill runs now. Connect the tools below and it pulls them automatically and keeps the report current without re-pasting.

- Works today with: your revenue summary. Paste or upload the rows that hold total ARR, channel ARR, bookings, targets, and the forecast. A summary export or CSV is enough.
- More powerful connected to a spreadsheet or BI tool: it reads every summary tab automatically and reconciles row counts.
- Sharper with a CRM: it pulls the open pipeline and the deals behind the forecast so the action layer names real accounts.
- Sharper with a product-analytics tool: it adds usage momentum to the hot-leads list.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your summary (an ARR export, a bookings CSV). The skill runs the full wrap-up today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the sheet and pipeline automatically and keeps the report live (pacing, forecast, action layer) without re-pasting. Same output, less effort, sharper.
- **Just exploring**: no numbers yet? Get the framework, the exact cells it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org reporting ARR across a direct-sales and a self-serve channel. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| SOURCE | where your numbers live | a summary sheet, a BI export, a CSV |
| TOP_METRIC | your headline number | Total ARR, MRR, net revenue |
| CHANNELS | how you split the business | Direct Sales vs Self-Serve, New vs Expansion |
| TARGET / FORECAST / CURRENT | the three numbers you never blur | committed goal / team commitment / what has closed |
| VARIANCE_FLAG | the gap that earns a red flag | 10% of target (yellow at 5-10%) |
| ACTION source | where the hot leads and deals come from | your CRM, a pipeline export |
| CADENCE | how often the report runs | weekly pacing, monthly retrospective, quarterly review |

Point it at your metrics and your channels, not anyone else's. The skill narrates position and variance, whatever your revenue model is.

## The method

### The accuracy contract
Revenue reporting is where a wrong number costs the most, so accuracy is not optional.
- Every number traces to a specific cell. If you cannot point to a row, say "data unavailable" instead of guessing.
- Verify the period first, always. Read the "as of" and "period covered" dates, echo them at the top, and stop if they do not match what was asked.
- Read the forecast the sheet already computes. Never run your own pacing math on top of a number the source already calculated.
- Never narrate an error cell. Skip it or note "data unavailable," never print the glyph.
- Never mix a monthly and a quarterly period in the same section. Crossing streams produces wrong numbers that look right.

### Revenue-position analysis (five steps)
1. **Headline.** Lead with the top metric against target: above, below, or on target, in both dollars and percent.
2. **Break down by channel.** Which channel is driving the gap or the surplus.
3. **Drill into the driver.** For the channel with the biggest variance, analyze the sub-channel breakdown (new business vs churn, upgrade vs reactivation).
4. **Forecast comparison.** Current vs Forecast vs Target: are you tracking to close the gap by period end.
5. **Forward outlook.** What the forecast says about where you land, quantified.

### The three definitions (never blur these)
Target is the committed goal. Forecast is what the team commits to based on current visibility. Current is what has actually closed as of the date. "We are at X" is ambiguous, always say which.

### Variance flagging
Flag any metric where variance exceeds VARIANCE_FLAG of target. Color it: green on or above target, yellow in the 5-10% watch zone, red past 10%.

### The action layer
A report nobody acts on is a rear-view mirror. Close every wrap-up with what to do now: the hot leads worth a touch this week, and the open deals whose forecast the number depends on. This is what turns reporting into an operating rhythm rather than a recap.

## Quality gates
- Period verification runs before analysis, every time. No exceptions.
- Every headline number is traceable to a source cell, or it is not reported.
- Forecast is read from the source, never recalculated.
- Variance is flagged by the same thresholds every time, so this week compares to last week.

## Output (example)
```
REVENUE WRAP-UP · as of Apr 30 · period: April · cadence: Monthly

Headline: April closed 4.9% under the Total ARR target, driven almost
entirely by Direct Sales. Self-Serve held the line.

Metric        Current   Target    Variance ($)   Variance (%)
Total ARR     $8.50M    $8.94M    -$440K         -4.9%   (yellow)
DS ARR        $4.54M    $5.00M    -$460K         -9.2%   (yellow)
SS ARR        $3.96M    $3.93M    +$30K          +0.6%   (green)

Driver: DS churn ran well above plan; new business landed light.
Offsetting: expansion came in near 2x target, reactivation added upside.

Forecast: on the current forecast, next period closes within 2% of target
if the two slip-risk deals below hold.

ACTION LAYER
  Hot leads: 3 accounts replied or engaged this week, no follow-up yet.
  Deals to work: 2 slip-risk deals the forecast depends on. Push both before period end.
```

## Where the numbers come from
The 10% variance flag (yellow at 5-10%) and the monthly cadence are defaults, not laws. They suited a mid-market SaaS reporting rhythm. If your business runs tighter or looser, move them. The logic does not change. The thresholds are yours.

## Example chat

**You:** Run the wrap-up. Here's the ARR summary sheet, as of April 30th.

**Claude:** Verified the period first, then ran it. Direct Sales is where the gap is coming from, self-serve is fine.
```
REVENUE WRAP-UP · as of Apr 30 · period: April · cadence: Monthly
Metric        Current   Target    Variance ($)   Variance (%)
Total ARR     $8.50M    $8.94M    -$440K         -4.9%   (yellow)
DS ARR        $4.54M    $5.00M    -$460K         -9.2%   (yellow)
SS ARR        $3.96M    $3.93M    +$30K          +0.6%   (green)

ACTION LAYER
  Hot leads: 3 accounts replied or engaged this week, no follow-up yet.
  Deals to work: 2 slip-risk deals the forecast depends on.
```
Caught one thing before I ran the numbers: I checked the "as of" date on the sheet against what you asked for. They matched, so I didn't stop. If they hadn't, I'd have flagged it instead of reporting a number from the wrong period.

**You:** Is the forecast in here your math or the sheet's?

**Claude:** The sheet's. This skill never runs its own pacing math on top of a number the source already calculated, it reads the forecast the sheet computes and reports it straight. Sharpener: connect your CRM and the action layer will name the two slip-risk deals by account instead of just counting them.

## Go further
The wrap-up proves the rhythm is worth keeping. Here is the version that keeps the rhythm without you touching it.

- **Run this every Monday without touching it.** Schedule a Claude task against your BI export so the wrap-up is written and posted before the pipeline review starts.
- **Name the hot leads and slip-risk deals live.** Connect Salesforce so the action layer lists real accounts and owners instead of a count.
- **Flag variance the moment it crosses the line.** Wire the yellow and red thresholds to a Slack alert so a channel gap gets noticed the day it happens, not at the next report.

The number shows up with its own explanation attached, every time, on the same schedule.

## Make it yours
Fork it. Change the metrics, the channels, the flags, the cadence. The point is not to run someone else's report. It is to run yours, so the number arrives with the next move already attached. Built by an operator. Customize it, break it, make it better.
