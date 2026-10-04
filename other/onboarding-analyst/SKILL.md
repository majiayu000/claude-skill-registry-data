---
name: onboarding-analyst
description: Turn "is this new customer going to stick?" into a first-90-day diagnostic. Day-30 / 60 / 90 activation tracking, a sales-to-success handoff quality score, champion engagement during the onboarding window, time-to-value milestone hit rate, and an early false-negative catch on customers already adopting. Built for CS leaders and CSMs, customizable to your CRM and your product-analytics tool. Trigger on "how's {account} onboarding going?", "first 90 day check on {customer}", "is {account} activating?", "time-to-value on {customer}", "handoff quality", "who's at risk in first 90 days?", or any first-90-day adoption question.
---

# Onboarding Analyst

## What this does
Watches every new customer through their first 90 days and tells you which ones are actually sticking. It checks Day-30, Day-60, and Day-90 activation against named capabilities, scores how clean the sales-to-success handoff was, tracks how fast each account hit first value, and flags the accounts a fit score wrote off while they were quietly adopting. It is the missing read between the deal closing and the renewal.

## What you'll need
You do not need to connect anything to get value today. Bring your new customers and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: a list of recently closed customers, with close date, and any activation you know (features adopted, first login, kickoff date). Paste it or upload a CSV.
- More powerful connected to a CRM: it reads close date, owner, and handoff fields automatically.
- Sharper with a product-analytics tool: it measures real activation and time-to-value instead of asking you.
- Sharper with a meeting or email tool: it confirms the kickoff happened and the CSM is actually engaged.
- Sharper with a support tool: it catches early-ticket patterns that predict a rocky start.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a milestone it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your new-customer list. The skill runs the full first-90-day diagnostic today on your real accounts. No connection required.
- **Connect your tools**: the same skill pulls activation, handoff, and engagement automatically, so milestones reflect real usage. Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact milestones it checks, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a CS team onboarding new customers off a CRM and a product-analytics tool. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot |
| PRODUCT analytics | where activation lives | a product-analytics tool |
| CLOSE date | when the clock starts | account created or contract-signed date |
| CAPABILITIES | the features that mean "activated" | your product's key actions |
| HANDOFF fields | kickoff, notes, owner transfer | your kickoff and account-notes fields |
| TTV target | your time-to-value benchmark | Day-30 activation (re-tune) |

Run any milestone model you like. The skill checks "did this customer hit the milestones you defined," so point it at your capabilities, not anyone else's.

## The method

### Day-30 / 60 / 90 milestone framework
Each checkpoint is named-capability, not a vague "good activation." A real read looks like "first capability adopted Day 12, second started Day 18, the Day-30 target capability not yet activated." You see exactly what landed and what is missing.

### Handoff quality scorer (multi-source)
Did the kickoff happen inside the first two weeks? Was the deal context actually transferred, not left as stale sales notes? Has the CSM met the customer? The score reads more than the CRM, it confirms the meeting and the notes transfer across your tools.

### Onboarding-window champion engagement
Engagement during the honeymoon period is uniquely diagnostic, different from a post-90-day champion check. A champion who goes quiet in the first 30 days is an early red flag worth more than the same silence at Day 200.

### Early false-negative catch
A customer a fit score floored while they have already adopted several capabilities in their first 30 days is a false negative. That account belongs in the expansion pipeline now, not written off.

### Time-to-value tracker
Measure the time from contract signed to first power-user threshold, and tag it against your benchmark. "Hit Day-30 activation in 18 days, top of the recent cohort" tells you more than a raw date.

## Quality gates
- Milestones are named-capability, never aggregate. You see which capability landed and which is missing, with the day.
- The handoff scorer is multi-source, not CRM-only. It confirms the kickoff meeting and the notes transfer.
- Time-to-value is benchmark-tagged, so a number always carries "fast or slow versus your cohort."

## Output (example)
```
FIRST 90 DAYS · 14 customers in the onboarding window

DAY 30 CHECK (8 past Day 30)
  OK    Acme Corp    activated Day 18 (top of cohort)
  OK    Vertex       activated Day 24 (on pace)
  WARN  Blend Labs   Day 30, zero core actions (behind)
  WARN  Northwind    Day 30, champion dark 14 days

DAY 60 CHECK (4 past Day 60)
  OK    Summit       multi-capability adopted
  WARN  Meridian     Day 60, baseline only, nothing adopted

DAY 90 CHECK (2 past Day 90)
  OK    Anvil        power usage on two capabilities
  WARN  Beacon       Day 90, fit score now healthy but no expansion in pipeline

Handoff quality:
  11 of 14 had a kickoff inside 14 days
  WARN  Blend Labs   no kickoff yet (Day 30)
  WARN  Meridian     kickoff happened but context was empty at handoff
  WARN  Northwind    account notes never updated from sales-stage notes

Early false-negatives (1):
  Beacon   fit score floored, but adopted 4 capabilities in 30 days
           should be in the expansion pipeline now

At-risk in first 90 days (3):
  1. Blend Labs   Day 30, zero adoption, no CSM meeting
  2. Northwind    champion not engaged, thin handoff
  3. Meridian     Day 60, still no capability adopted

Next moves:
  1. Emergency CSM intervention on Blend Labs this week
  2. Northwind, re-engage the champion or pivot to a backup
  3. Add Beacon to the expansion pipeline and assign coverage
  4. Handoff-completeness rate needs to hit 100 percent
```

## Where the numbers come from
The Day-30 / 60 / 90 checkpoints and the two-week kickoff window are defaults, not laws. They suited a product with a fast time-to-value. If your product takes longer to land, stretch the windows. The milestone logic does not change, the thresholds are yours.

## Example chat

**You:** Beacon is 90 days in and our fit score has them flagged low. Worth a save call or should we let it go quiet?

**Claude:** Pulled the first-90-day read on Beacon. Don't let this one go quiet.
```
DAY 90 CHECK
  Beacon   power usage on two capabilities, fit score still LOW

Early false-negative:
  Beacon   fit score floored at signup, adopted 4 capabilities in 30 days
           should have moved to expansion pipeline back on Day 30
```
The fit score never caught up to what Beacon was actually doing. That's a 60-day-old false negative sitting in the wrong bucket.

**You:** How do we stop missing this on the next cohort?

**Claude:** Two fixes. First, re-run the false-negative check at Day 30, not just Day 90, so you catch it while it's still fresh. Second, add Beacon to the expansion pipeline today with the adoption evidence attached so the AE isn't starting from zero. One sharpener: connect your product-analytics tool so activation dates come from real usage instead of the self-reported milestones you pasted in.

## Go further
The read above is a one-time pull. Here's what an operator wires up once the manual version proves the false-negative catch is real.

- **Run it every Monday, not when you remember.** A scheduled Claude task pulls the new-customer list from Salesforce and flags Day-30/60/90 misses before the CSM has to ask.
- **Catch the false negative the day it happens.** Connect a product-analytics tool so the moment a low-fit account crosses the adoption threshold, it lands in a Slack DM to the account owner instead of waiting for a quarterly review.
- **Close the loop into expansion.** Route confirmed false negatives straight into the expansion pipeline in Salesforce with the adoption evidence attached, so the AE opens the conversation with proof, not a guess.

The diagnostic is the easy part. Wiring it to run without you is what actually saves the account.

## Make it yours
Fork it. Change the milestones, the windows, the capabilities. The point is not to run someone else's playbook. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
