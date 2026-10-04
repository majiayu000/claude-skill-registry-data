---
name: success-plan
description: Turn a customer's stated goals into a success plan that predicts the renewal. It sets time-to-value milestones, names an owner on both sides for each, and picks the leading indicators that tell you a year early whether this account renews. Built for B2B customer success teams, customizable to your CRM and product analytics. Trigger on "build a success plan", "onboarding plan for this account", "what are the milestones", "how do I know they'll renew", "time-to-value plan", or any post-sale planning.
---

# Success Plan

## What this does
Takes the goals a customer stated when they bought and turns them into a plan that drives to value: milestones with dates, an owner on your side and theirs for each one, and the leading indicators that predict the renewal long before the renewal date. The output is a working plan, not a wish list.

## What you'll need
You do not need to connect anything to get value today. Bring the customer's goals and the skill runs now. Connect the tools below and it pulls the rest and adds signals you cannot paste by hand.

- Works today with: the customer's stated goals, the buying context, who the users and sponsor are, the start date, and the renewal date. Paste it or upload the sales-to-CS handoff.
- More powerful connected to a CRM: it reads the account, contacts, ARR, and renewal date automatically.
- Sharper with a product-analytics tool: turns milestones into measured events instead of checkboxes.
- Sharper with a meeting or email tool: tracks whether the owners are actually meeting the plan.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste the goals and the handoff notes. The skill builds the full plan today on your real account. No connection required.
- **Connect your tools**: the same skill pulls contacts, usage, and dates automatically and adds signals you cannot paste by hand. Same plan, less effort, sharper.
- **Just exploring**: no account yet? Get the framework, the exact inputs it reads, and a worked example on a sample account, so you can see the shape before you feed it.

Every run ends with the one thing that would make the plan sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org onboarding named accounts to a renewal. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| GOALS source | where the stated goals live | order form, handoff, discovery notes |
| ADOPTION source | where usage lives | product analytics, a usage export |
| FIRST_VALUE | the first real outcome that matters | first live workflow, first report shipped |
| TTV target | days to first value you aim for | 30 (re-tune to your product) |
| INDICATOR set | the leading signals you trust | weekly active seats, key-feature use, sponsor engaged |
| OWNERS model | how you name both-side owners | CSM + customer champion per milestone |
| RENEWAL field | the renewal date and ARR | Account.RenewalDate, Account.ARR |

Build the plan around the goals this customer stated, not a template. A generic plan renews no one.

## The method

### Goal translation
Turn each stated goal into a measurable outcome. "Improve efficiency" becomes "one team running the core workflow live by day 30." A goal you cannot measure is a goal you cannot prove at renewal.

### Time-to-value milestones
Sequence the outcomes: first value fast, then breadth, then depth. Each milestone has a date anchored to the start, not to "someday." The first-value milestone is the one that matters most; protect its date.

### Owners on both sides
Every milestone names a your-side owner and a customer-side owner. A milestone with no customer owner is a task you will do alone and they will not value. Escalate any milestone that has no owner on their side.

### Leading indicators that predict renewal
Pick the few signals that move before the renewal does: weekly active seats trending up, the key feature in real use, the sponsor still engaged, a second use case emerging. These are the early-warning system. Lagging signals like the renewal date itself tell you too late.

### The renewal thesis
State, in one line, why this account renews if the plan holds, and what would break it. Revisit it every review. If you cannot write the thesis, the plan is not done.

## Quality gates
- Every goal is measurable, or it is flagged and sent back for a metric.
- Every milestone has a date and an owner on both sides.
- Leading indicators are named and trackable, not vague "engagement."
- The plan states its renewal thesis and the single biggest risk to it.

## Output (example)
```
SUCCESS PLAN · sample account · start day 0, renewal day 365
MILESTONE               TARGET   YOUR OWNER   THEIR OWNER   INDICATOR
Kickoff + goals agreed  Day 3    CSM          Sponsor       plan signed
First workflow live     Day 30   CSM          Champion      1 team active
Full team adopted       Day 75   CSM          Champion      8/9 seats weekly
Second use case         Day 120  CSM          Sponsor       new workflow live
Value review            Day 180  CSM          Sponsor       outcome measured

Leading indicators: weekly active seats, key-feature use, sponsor engaged.
Renewal thesis: renews if the second team adopts and the sponsor stays engaged.
Biggest risk: single-threaded on one champion.
```

## Where the numbers come from
The day targets, seat counts, and indicators come from the data you paste or the tools you connect. Nothing above is a real customer number; it is illustrative. When the skill cannot measure a milestone, it marks it a checkpoint and names the input that would make it measured.

## Example chat

**You:** New account just signed. Here's the sales-to-CS handoff notes, build the success plan.

**Claude:** Here's the plan, built off the stated goals.
```
MILESTONE               TARGET   YOUR OWNER  THEIR OWNER  INDICATOR
Kickoff + goals agreed  Day 3    CSM         Sponsor      plan signed
First workflow live     Day 30   CSM         Champion     1 team active
Full team adopted       Day 75   CSM         Champion     7/8 seats weekly

Renewal thesis: renews if the second team adopts by day 120.
Biggest risk: single-threaded on one champion, no second contact named yet.
```
Key insight: the handoff notes never named a customer-side owner for "full team adopted," that's the milestone most likely to slip since nobody but the CSM is accountable for it. One sharpener: connect product analytics so "1 team active" is a measured event instead of a checkbox the CSM self-reports.

## Go further
The plan is drafted. Here is where an operator takes it once the manual version proves out.

- **Turn milestones into measured events.** Wire product analytics (Amplitude) so "first workflow live" fires automatically off real usage, and the plan updates itself instead of waiting on a CSM check-in.
- **Watch the renewal thesis, not just the renewal date.** A scheduled Claude task re-reads the leading indicators weekly and flags the account in Salesforce the moment the sponsor goes quiet.
- **Route the risk to a human before it's a save.** If the single-threaded flag trips, have Slack DM the CSM's manager automatically, so the second-contact gap gets worked while there's still runway.

The plan predicts the renewal; the automation is what keeps the prediction honest.


## Make it yours
Fork it. Change the milestones, the time-to-value target, the indicators you trust. The point is not to run someone else's onboarding. It is to run yours, and to see the renewal coming a year out. Built by an operator. Customize it, break it, make it better.
