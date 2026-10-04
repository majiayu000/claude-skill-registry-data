---
name: funnel-metrics
description: Build the funnel metrics that actually get trusted. Stage-by-stage conversion, velocity, win rate, and the single biggest leak, with every definition pinned so nobody relitigates the numbers in the meeting. Built for B2B RevOps teams, customizable to your CRM and your stage model. Trigger on "build my funnel metrics", "what's my conversion by stage", "where's the leak", "what's our win rate", "how fast do deals move", or any funnel diagnostic.
---

# Funnel Metrics

## What this does
Reads your stage data and builds the core funnel: how many deals convert from each stage to the next, how long they sit in each stage, what share of qualified deals win, and where the biggest drop-off is. Every metric ships with its definition attached, so the conversation is about the leak, not about whether the number is real.

## What you'll need
You do not need to connect anything to get value today. Bring a stage export and the skill runs now. Connect the tools below and it reads the history automatically and computes rates you cannot eyeball from a snapshot.

- Works today with: a CSV or paste of deals with stage, amount, created date, close date, stage-entry dates if you have them, and won/lost outcome.
- More powerful connected to a CRM: it reads the full deal history and stage timestamps automatically, across every cohort.
- Sharper with a data warehouse: it can build true entered-stage cohorts instead of inferring from a current snapshot.
- Sharper with a BI tool: pushes the pinned definitions into a dashboard so the whole team reads one number.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a conversion rate it cannot derive. A missing timestamp is a caveat, not a guess.

- **Bring your data**: paste or upload your stage export. The skill runs the full funnel today on your real deals. No connection required.
- **Connect your tools**: the same skill pulls stage history automatically and computes cohort-true rates you cannot eyeball (real time-in-stage, entered-stage denominators, trailing trends). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, the definitions it pins, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a timestamp to capture or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running a staged pipeline. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | a CRM (Salesforce, HubSpot, Pipedrive) |
| STAGE model | your ordered stage list | your opportunity stages |
| WIN definition | what counts as won | Closed Won, excluding no-decision |
| DENOMINATOR rule | what each rate divides by | deals that entered the stage, not all deals |
| VELOCITY basis | how you measure time-in-stage | stage-entry to next-stage-entry dates |
| COHORT window | the period you group deals by | created quarter, or entered-stage month |
| SEGMENTS | cuts you compare | segment, source, owner, product |

Pin your win definition and denominator rule before anything else. Most funnel arguments are really definition arguments in disguise.

## The method

### Stage-to-stage conversion
For each adjacent stage pair, divide deals that reached the later stage by deals that entered the earlier one. State the denominator out loud. A rate that divides by "all deals ever" and a rate that divides by "deals that entered this stage" are different numbers, and only one of them is honest about the leak.

### Time-in-stage velocity
Measure median days in each stage, not mean. One 400-day zombie deal drags a mean and hides the typical path. Use stage-entry timestamps where you have them and say so where you had to infer from close date.

### Win rate
Win rate is wins divided by resolved deals (won plus lost), with no-decisions handled explicitly and stated. Report it on a trailing window big enough to mean something, never on this week's handful.

### Leak detection
Rank the stage transitions by drop-off and name the single worst one. The biggest leak is where the funnel loses the most deals relative to what entered, not the stage with the lowest raw count. That is the one place a fix moves the whole number.

### Definition ledger
Every metric prints with its definition and denominator beside it. This is the trust layer. When someone questions a number in the room, the answer is already on the page.

## Quality gates
- Every rate shows its denominator. No naked percentages.
- Velocity is median, and the date basis is named.
- Win rate states how no-decisions were handled, every time.
- Small samples are flagged, not smoothed. A rate on nine deals says so.

## Output (example)
```
FUNNEL METRICS · created Q cohort · 620 deals
Transition            Conversion   Median days   Note
Lead -> Qualified     44%          9             denom: leads created
Qualified -> Demo     71%          6             denom: entered Qualified
Demo -> Proposal      52%          14            biggest leak
Proposal -> Won       61%          11            denom: entered Proposal

Win rate (trailing 2Q): 34% of resolved deals. No-decisions excluded, counted separately.
Biggest leak: Demo -> Proposal. Half of demoed deals never get a proposal.

Next: capture stage-entry timestamps to replace inferred velocity on 2 stages.
```
Illustrative figures. Your run reports your real numbers.

## Where the numbers come from
The cohort window, the trailing win-rate window, and the median-over-mean choice are defaults, not laws. They suited a mid-market SaaS cycle. If your deals run longer or your volume is thinner, widen the windows. The definitions are the point, and they are yours to set.

## Example chat
**You:** Where's the leak in our funnel? Here's our stage export for the quarter.

**Claude:** Ran the full funnel with the denominators pinned.
```
Transition            Conversion   Median days
Lead -> Qualified     44%          9
Demo -> Proposal      52%          14   <- biggest leak
Proposal -> Won       61%          11
```
Half of demoed deals never make it to a proposal. That's the transition worth fixing, not the stage with the lowest raw count. Win rate over the trailing 2 quarters is 34%, no-decisions counted separately so they don't quietly inflate it.
One sharpener: connect your CRM so time-in-stage uses real stage-entry timestamps instead of the two stages I had to infer from close date.

## Go further
The read works from a pasted export. Here is where the leak gets caught while it's still small.

- **Watch the leak in real time.** A scheduled Claude task rebuilds this funnel weekly from Salesforce and posts to Slack the moment the Demo-to-Proposal rate drops below its trailing average.
- **Cut it by segment automatically.** Connect a BI tool so the same pinned definitions run per segment, source, and owner without rebuilding the query each time.
- **Turn the leak into a fix.** Feed the worst transition into a coaching or deal-review skill so reps get a specific drill on the stage that's actually bleeding deals.

Once the definitions are pinned, the leak stops being an argument and starts being a fix.

## Make it yours
Fork it. Change the stages, the win definition, the denominators, the segments you cut by. The point is not to run someone else's funnel. It is to run yours with the definitions pinned, so the number survives the meeting. Built by an operator. Customize it, break it, make it better.