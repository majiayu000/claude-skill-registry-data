---
name: business-case
description: Turn a champion's enthusiasm into a one-page business case the buying committee can approve. Frames the cost of the problem, the change you enable, the value model, and the risk of doing nothing, in the buyer's own numbers. Built for B2B sales teams, customizable to your value drivers and your CRM. Trigger on "build a business case", "ROI narrative", "justify the spend", "one-pager for the committee", "cost of doing nothing", or any deal that has to clear a budget holder.
---

# Business Case

## What this does
Writes the one-page business case that a champion carries into a committee and a budget holder approves. It states what the problem costs today, the change you enable, a value model in the buyer's own numbers, and the risk of doing nothing. It is built to be defended by someone who is not you, in a room you are not in.

## What you'll need
You do not need to connect anything to get value today. Bring the numbers you gathered in discovery and the skill runs now. Connect the tools below and it pulls the pain metrics and the deal context for you.

- Works today with: the problem the buyer stated, the pain metrics you captured (hours, dollars, headcount, churn), and the price of your solution. Paste them and the skill builds the case.
- More powerful connected to a meeting or transcription tool: it pulls the buyer's own quantified pain from discovery, so the value model is built on their numbers, not yours.
- Sharper connected to a CRM: it reads the deal size, the stage, and the qualification fields, so the case matches the deal the pipeline already holds.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the numbers you give it today and gets sharper as you connect tools. It never presents a made-up figure as real. Every number is labeled as the buyer's, a stated assumption, or illustrative, so the case survives scrutiny.

- **Bring your data**: paste the stated pain, the metrics, and the price. The skill returns the one-page case, the value model, and the cost of inaction today. No connection required.
- **Connect your tools**: the same skill pulls the buyer's quantified pain from the calls and the deal context from the CRM. Same case, built on their numbers.
- **Just exploring**: no deal yet? Get the one-page structure, the value-model math, and a worked example on sample numbers, so you can see the shape before you build one.

Every run ends with the one assumption the whole case rests on, so you can go confirm it before the committee does.

## Customize this for yourself
This was built for a B2B SaaS org selling into a buying committee. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| VALUE drivers | how your product creates value | time saved, revenue gained, cost avoided, risk reduced |
| PAIN metrics | the units you quantify in | hours, dollars, headcount, churn rate |
| PRICE input | your cost to the buyer | list price, expected deal size |
| DEAL fields | where deal context lives | Amount, StageName, qualification fields |
| HORIZON | the payback window you show | 12 months (re-tune to your buyer) |
| ASSUMPTION log | where you list every input | shown on the page, not hidden |

Build the case on the buyer's value drivers, not your feature list. The skill labels every number so the committee trusts the page.

## The method

### The cost of the problem
Start with what the status quo costs today, in the buyer's numbers. Not what your product does, what the problem does. If the buyer gave you "roughly 6 hours a week per rep," that becomes the annualized cost of doing nothing. No stated pain, no case.

### The change you enable
State plainly what is different after they buy: the workflow that goes away, the time that comes back, the revenue that stops leaking. One paragraph, concrete, in their language, no adjectives.

### The value model
Show the math. Cost of the problem, minus the price of the solution, over the horizon, equals the value. Keep it simple enough that the champion can defend every line without you. Label each input as the buyer's number, a stated assumption, or illustrative. An illustrative example: "~6 hrs/wk x 20 reps x loaded rate" makes the assumption visible so the committee can test it, not swallow it.

### The risk of doing nothing
Name what happens if they defer: the pain compounds, the cost keeps running, the quarter they wanted to fix passes. Doing nothing is a decision with a price. The case shows that price.

### One page, one owner
It fits on one page because a champion has to carry it into a room and defend it fast. Anything that will not fit is a leave-behind, not the case. The page is built to be forwarded and defended without you present.

## Quality gates
- Every number is labeled: the buyer's, a stated assumption, or illustrative. Nothing invented as real.
- The value model math is shown, not asserted, and simple enough to defend without you.
- The cost of doing nothing is quantified, not just described.
- The case fits on one page, and the single load-bearing assumption is called out.

## Output (example)
```
BUSINESS CASE · illustrative deal · one page

The problem, today
  ~6 hrs/wk/rep lost to manual prospecting. At 20 reps, that is roughly
  6,000 hours a year not spent selling. [buyer's number: 6 hrs; assumption: 20 reps]

The change
  Reps stop building lists by hand. That time returns to selling.

The value (12-month horizon)
  Cost of problem:   ~6,000 hrs/yr x loaded rate   [illustrative]
  Cost of solution:  annual price                   [list price]
  Net:               value over 12 months, payback inside the year

The risk of doing nothing
  The 6 hours keep leaking every week. The ramp problem repeats next
  cohort. The quarter you wanted to fix passes unfixed.

Load-bearing assumption: the 20-rep count. Confirm before committee.
```

## Where the inputs come from
The number-labeling rule, the shown-not-asserted math, and the one-page limit are the defaults that let a champion defend the case without you. The value drivers and the horizon are yours. If your buyer thinks in risk reduction, not time saved, model that. The discipline does not change: every number sourced, every assumption visible. The case is yours.

## Example chat
**You:** My champion needs to take this to their VP. Build the business case. Here's what I got in discovery: about 6 hrs/wk per rep lost to manual prospecting, 20 reps.

**Claude:** One page, built to be defended without you in the room.
```
The problem, today
  ~6 hrs/wk/rep lost to manual prospecting. At 20 reps, that is roughly
  6,000 hours a year not spent selling. [buyer's number: 6 hrs; assumption: 20 reps]

The value (12-month horizon)
  Cost of problem:   ~6,000 hrs/yr x loaded rate   [illustrative]
  Cost of solution:  annual price                   [list price]
  Net:               value over 12 months, payback inside the year

Load-bearing assumption: the 20-rep count. Confirm before committee.
```
The part that actually protects your champion: every number is labeled as theirs, an assumption, or illustrative. When the committee pokes at the math, they're not defending a black box, they're defending exactly one number, the rep count, and you told them that upfront.

**You:** Should I include the loaded rate calculation?

**Claude:** Only if you have it as a real number, otherwise leave it illustrative and let the champion fill in their own comp data. A rep's actual loaded rate is something the finance person in the room will know better than you do. One sharpener: get the buyer to confirm the 20-rep count before the committee meeting, that's the single assumption the whole case rests on.

## Go further
Building one case by hand proves your champion can defend it. Here's the version that scales across every deal.

- **Pull the pain metrics from the call automatically.** Connect Gong or your meeting tool so the discovery numbers feed the value model directly instead of you re-typing them from notes.
- **Match the case to the deal in flight.** Wire Salesforce deal size and stage into the template so the case's price and horizon always match what's actually in the pipeline.
- **Generate it the moment discovery closes.** Set a scheduled Claude task that drafts the one-pager the day a deal enters the Validation stage, so the case exists before the champion has to ask for it.

A defensible case built once by hand becomes a habit the pipeline expects at every deal.

## Make it yours
Fork it. Change the value drivers, the horizon, the math. The point is not to hand over someone else's ROI deck. It is to build a one-pager your champion can defend in a room you are not in, with numbers the committee cannot pick apart. Built by an operator. Customize it, break it, make it better.
