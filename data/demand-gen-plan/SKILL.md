---
name: demand-gen-plan
description: Turn a pipeline target into a demand-generation plan that actually maps to the number. The ICP worth spending on, the offers by funnel stage, the channel mix that reaches them, the content that earns attention, and the pipeline math worked backward from the goal so you know if the plan can even hit it. Built for B2B marketing teams, customizable to your funnel and your channels. Trigger on "build a demand gen plan", "how do we hit our pipeline number", "what's our channel mix", "plan our content", "work the funnel math backward", or any demand-generation planning question.
---

# Demand-Gen Plan

## What this does
Takes a pipeline or revenue target and builds the plan to reach it: who you are trying to reach, what you offer them at each stage of the funnel, which channels carry it, what content earns the click, and the backward math that tells you whether the budget and the conversion rates can actually produce the number. It builds the plan and stress-tests the math. It does not run the campaigns for you.

## What you'll need
You do not need to connect anything to get value today. Bring your target and the skill runs now. Connect the tools below and it grounds the funnel math in your real conversion rates instead of assumptions.

- Works today with: your pipeline or revenue target, who you sell to, your average deal size, and roughly how leads convert to deals. Paste it in.
- More powerful connected to a CRM: it reads real lead-to-opportunity and opportunity-to-won rates, so the backward math uses your history, not a guess.
- Sharper with a web-analytics tool: shows which channels and content already drive signups, so the mix leans on what works.
- Sharper with an ad platform and an email tool: ties spend and sends to sourced pipeline, so cost per opportunity is real.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the target and rates you give it today and gets more powerful as you connect tools. It never invents a conversion rate it cannot see. An assumed rate is labeled as an assumption, not passed off as fact.

- **Bring your data**: paste the target, deal size, and rough rates. The skill builds the ICP, offers, channel mix, content plan, and the full backward math today. No connection required.
- **Connect your tools**: the same skill pulls your real conversion rates and channel performance and rebuilds the math on them, so the plan is defensible, not hopeful.
- **Just exploring**: no target set yet? Get the framework, the exact inputs it reads, and a worked example, so you can see how the math forces honesty before you commit a budget.

Every run ends with the one thing that would make the next run sharper, a rate to ground or a tool to connect.

## Customize this for yourself
This was built for a B2B team owning a sourced-pipeline number across multiple channels. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| TARGET | the number the plan must hit | sourced pipeline or revenue, per quarter |
| ICP | who you spend on | your segments by fit and intent |
| STAGES | your funnel steps | visitor, lead, MQL, SQL, opportunity, won |
| CONV_RATES | how each stage converts | your rates, or assumptions flagged as such |
| CHANNELS | where you reach them | paid, organic, email, events, partners |
| DEAL_SIZE | average won deal | your ACV |
| SALES_CYCLE | time from lead to close | your cycle, to phase the plan |

The rates and dollar figures below are illustrative placeholders, not benchmarks. Replace them with your own.

## The method

### ICP (spend where it converts)
Name who the plan targets and, just as important, who it does not. A demand plan aimed at everyone converts like it. Define the segments by fit and intent, and concentrate budget on the ones most likely to become pipeline. Everything downstream inherits this choice.

### Offers by stage (match the temperature)
Each funnel stage needs an offer matched to how ready the buyer is. Top of funnel earns attention with education and proof, no ask for a meeting yet. Middle offers a reason to engage (a tool, a teardown, a comparison). Bottom makes the direct ask (demo, trial, call). One offer for the whole funnel leaks buyers at both ends.

### Channel mix (reach times fit)
Choose channels by where the ICP actually pays attention and what each channel is good at. Paid buys reach fast but costs per lead climb, organic compounds but is slow, email works the list you have, events and partners borrow trust. Weight the mix to the goal and the timeline, and note why each channel earns its slice.

### Content (the fuel)
Map content to stages and channels: what earns the top-of-funnel click, what converts the middle, what closes the bottom. Content is not a separate plan, it is the fuel the channels burn. Name the pieces and the stage each one serves so nothing gets made that no channel will use.

### Backward math (does it add up)
This is the honesty check. Start from the TARGET, divide by DEAL_SIZE for deals needed, then walk backward through CONV_RATES to the opportunities, leads, and visitors required. Compare that to what the channel mix and budget can realistically produce. If the math does not close, the skill says so and shows the gap, so you fix the plan before the quarter, not during it.

## Quality gates
- Every stage has an offer matched to buyer readiness. No single offer for the whole funnel.
- The backward math is shown end to end, from target to visitors, so the plan is falsifiable.
- Any conversion rate not read from your CRM is labeled an assumption.
- The plan states plainly whether the math closes on the given budget, and names the gap if it does not.
- All dollar and rate figures are labeled illustrative unless grounded in connected data.

## Output (example)
```
DEMAND-GEN PLAN · $2M sourced pipeline this quarter (illustrative)
ICP: two priority segments · Deal size: $25K · Cycle: ~60 days

Backward math:
  $2M / $25K            = 80 deals needed
  at 25% opp-to-won     = 320 opportunities
  at 15% SQL-to-opp     = ~2,130 SQLs
  at 40% MQL-to-SQL     = ~5,300 MQLs
  -> the mix below must produce ~5,300 MQLs. Current run rate: ~3,900. Gap: 26%.

Channel mix (weighted to the gap):
  Paid search   35%   bottom-funnel intent
  Paid social   20%   top-funnel, teardown offer
  Organic/SEO   20%   compounding, mid-funnel
  Email/nurture 15%   works the existing list
  Events        10%   borrowed trust, high-fit

Offers: top = teardown guide · mid = comparison tool · bottom = live working session.

Verdict: plan is 26% short on current rates. Close it by connecting the CRM to
confirm the real rates, then either raise paid or improve mid-funnel conversion.

Next move: connect the CRM so these rates stop being assumptions.
```

## Where the inputs come from
The target, ICP, deal size, and cycle come from you or your GTM plan. Real lead-to-opportunity and opportunity-to-won rates come from a CRM. Channel and content performance come from a web-analytics tool, an ad platform, and an email tool. Every rate not read from a connected tool is flagged as an assumption, and every dollar figure is illustrative until grounded.

## Example chat
Here is the skill running on a real target, start to finish.

**You:** Build a demand gen plan, we need $2M sourced pipeline this quarter.

**Claude:** Built the plan and ran the backward math first.
```
$2M / $25K = 80 deals needed -> ~320 opps -> ~2,130 SQLs -> ~5,300 MQLs.
Current run rate: ~3,900 MQLs. Gap: 26%.
```
The catch: the channel mix on paper looks fine, but the math underneath it is 26% short at current conversion rates. The plan as written does not hit the number.

**You:** What closes the gap, more budget or better conversion?

**Claude:** Two options: raise paid spend to buy the extra volume, or confirm whether the assumed 15% SQL-to-opp rate is actually running higher, since that one assumption is doing a lot of work in this math.
```
If SQL-to-opp is really 18%, not 15%: gap drops from 26% to 9%.
```
One sharpener: connect the CRM so these rates stop being assumptions and the plan gets rebuilt on your real history.

## Go further
The read is step one. Here is where an operator takes it once the manual version proves out.

- **Ground every rate in real data.** Connect Salesforce so lead-to-opportunity and opportunity-to-won rates pull from your actual pipeline history instead of an estimate.
- **Watch the gap close or widen in real time.** Schedule a Claude task monthly to rerun the backward math against current pipeline and alert the team if the gap grows.
- **Tie content to what's actually converting.** Connect Amplitude or your web analytics so the content plan leans on the channels and pieces already driving signups, not a guess.

A plan that does not close the math is a hope. Ground it before you commit the budget.

## Make it yours
Fork it. Change the stages, the rates, the channel weights, the definition of a win. The point is not to run a generic funnel. It is to run yours and know, before the quarter starts, whether the math can hit the number. Built by an operator. Customize it, break it, make it better.
