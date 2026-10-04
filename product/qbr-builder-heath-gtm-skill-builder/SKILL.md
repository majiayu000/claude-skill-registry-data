---
name: qbr-builder
description: Turn account data into a QBR that earns the renewal. It builds the value-delivered story, adoption against the goals they signed up for, the open risks stated plainly, the forward roadmap, and the expansion ask, then hands you a deck outline. Built for B2B customer success teams, customizable to your CRM and product analytics. Trigger on "build a QBR", "prep the business review", "quarterly review for this account", "what do I show the customer", "value story for the renewal", or any account-review prep.
---

# QBR Builder

## What this does
Takes what you know about an account and builds the quarterly business review the buyer actually wants: proof of value delivered, adoption measured against the goals they bought for, the risks named before they name them, a roadmap that shows you are looking ahead, and an expansion ask tied to an outcome. It ends with a slide-by-slide outline you can drop into a deck.

## What you'll need
You do not need to connect anything to get value today. Bring what you know about the account and the skill runs now. Connect the tools below and it pulls the rest and adds signals you cannot paste by hand.

- Works today with: the account's stated goals at purchase, what you delivered this quarter, current usage or adoption notes, open issues, and the renewal date. Paste it or upload a doc.
- More powerful connected to a CRM: it reads the account record, renewal date, ARR, and open cases automatically.
- Sharper with a product-analytics tool: pulls real adoption against the goals instead of your estimate.
- Sharper with a support or ticketing tool: surfaces the open risks you may have forgotten.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste the goals, the wins, the usage, the open issues. The skill builds the full QBR today on your real account. No connection required.
- **Connect your tools**: the same skill pulls adoption, cases, and renewal data automatically and adds signals you cannot paste by hand. Same output, less effort, sharper.
- **Just exploring**: no account yet? Get the framework, the exact inputs it reads, and a worked example on a sample account, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next QBR sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running quarterly reviews on named accounts. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| GOALS source | where the customer's stated goals live | onboarding notes, success plan, order form |
| ADOPTION source | where usage lives | product analytics, a usage export |
| VALUE metrics | how this customer defines a win | hours saved, tickets deflected, cycle time |
| RISK source | where open issues live | support tickets, escalations, CSM notes |
| RENEWAL field | the renewal date and ARR | Account.RenewalDate, Account.ARR |
| EXPANSION target | the next product, seat, or tier | modules, seat bands, usage tiers |

Point it at the goals this customer actually stated. A QBR that measures against your goals instead of theirs is a pitch, not a review.

## The method

### Value-delivered story
Lead with outcomes, not features. Tie every win to a goal the customer stated at purchase. If a win has no goal behind it, mark it a bonus, not the headline. If a stated goal has no win yet, say so; the honesty buys the room.

### Adoption vs goals
Show adoption against the goals, not adoption in the abstract. "You wanted the whole revenue team live; 6 of 9 seats are active weekly" beats any raw number. Name the gap and whose it is to close.

### Open risks, stated first
List the risks before the buyer does: unadopted seats, an open escalation, a quiet champion, a contract term that no longer fits. Naming a risk yourself turns it from an ambush into a plan.

### The roadmap
Two lanes: what the customer will do next quarter, and what your product is shipping that they should care about. Each item has an owner and a date. A roadmap with no owners is a wish list.

### The expansion ask
Exactly one primary ask, tied to an outcome they already value. "You saved this much time on one team; the next team is not yet on it" is an ask. "Do you want to buy more" is not. Only make it if the value story earned it.

### Deck outline
Output a slide-by-slide outline: title, executive summary, goals recap, value delivered, adoption, risks and mitigations, roadmap, the ask, next steps. Ready to build, not to guess.

## Quality gates
- No win claimed without the goal it maps to. Bonus wins are labeled bonus.
- Every adoption number shows its source, or is marked an estimate.
- Risks appear even when the quarter went well. A QBR with zero risks is a QBR that stopped looking.
- One expansion ask, not five. Make it only if the value story earns it.

## Output (example)
```
QBR · sample account · renewal in 74 days
GOAL (stated)            RESULT              ADOPTION
Cut onboarding time      ~30% faster (est)   6/9 seats weekly
Standardize outreach     Live, 1 team        1 of 3 teams
Report on pipeline       Not started         0 seats

Open risks:
  1. Champion quiet 26 days. Single-threaded.
  2. 3 seats never activated since launch.
  3. Reporting goal untouched; renewal talks to reference it.

Expansion ask:
  One team proved the outreach win. The other two teams are not on it yet.

Deck outline: 9 slides. Value story leads, ask on slide 8, next steps close.
```

## Where the numbers come from
The adoption counts, the time-saved figures, and any percentage come from the data you paste or the tools you connect. Nothing in the example above is a real customer number; it is illustrative. When the skill cannot see a number, it marks it an estimate and tells you which input would make it real.

## Example chat

**You:** Build the QBR for this account. Renewal's in 74 days. They wanted faster onboarding, standardized outreach, and pipeline reporting. Onboarding's about 30% faster, outreach is live on one team, reporting never started.

**Claude:** Built it. The reporting goal is the thing you need to name before they do.
```
QBR · sample account · renewal in 74 days
GOAL (stated)            RESULT              ADOPTION
Cut onboarding time      ~30% faster (est)   6/9 seats weekly
Standardize outreach     Live, 1 team        1 of 3 teams
Report on pipeline       Not started         0 seats

Open risks:
  1. Champion quiet 26 days. Single-threaded.
  2. Reporting goal untouched; renewal talks to reference it.

Expansion ask:
  One team proved the outreach win. The other two teams are not on it yet.
```
I put the reporting miss in the risks section instead of leaving it out. A QBR with zero risks reads as a QBR that stopped looking, and the buyer will bring it up if you don't.

**You:** Should the expansion ask lead with the reporting gap or the outreach win?

**Claude:** The outreach win, it's proven value they already believe. Leading with the gap turns the ask into an apology. Sharpener: connect your product-analytics tool and I'll pull the actual weekly-active count instead of the "6/9 seats" estimate, so the adoption story is exact, not rounded.

## Go further
The manual read earns the room. Here is the version that keeps earning it every quarter.

- **Auto-build the deck a week before every renewal.** Point a scheduled Claude task at Salesforce renewal dates so the outline is ready before the CSM has to ask for it.
- **Pull adoption live, not from memory.** Connect Amplitude so the adoption-vs-goals table updates itself instead of a CSM estimating "about 30% faster."
- **Push the risk list to the account owner automatically.** Send the open-risks section to Slack the moment it's built, so the exec sponsor sees it before the call, not during it.

The QBR argues itself before you ever open the deck.

## Make it yours
Fork it. Change the sections, the value metrics, the order of the deck. The point is not to run someone else's business review. It is to run yours, faster, and walk in with the renewal already half-closed. Built by an operator. Customize it, break it, make it better.
