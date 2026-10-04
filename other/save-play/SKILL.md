---
name: save-play
description: Turn an at-risk account into a churn-save play. It diagnoses the real reason behind the risk (not the stated one), lays out the commercial and non-commercial levers you can pull, and builds a multi-touch save sequence with owners and dates. Built for B2B customer success teams, customizable to your CRM and product analytics. Trigger on "this account is going to churn", "build a save play", "why are they leaving", "at-risk renewal", "how do I keep this account", or any retention rescue.
---

# Save Play

## What this does
Takes an at-risk account and builds the play to save it: the real reason it is slipping (which is rarely the reason first given), the levers you can actually pull (commercial and not), and a multi-touch sequence with owners and dates so the save is a plan, not a hope. It is honest about when an account is not savable, so you spend your effort where it pays.

## What you'll need
You do not need to connect anything to get value today. Bring what you know about the account and the skill runs now. Connect the tools below and it pulls the rest and adds signals you cannot paste by hand.

- Works today with: the risk signal you saw, the account's history, who the sponsor and users are, usage trend, open issues, and the renewal date. Paste it or upload your notes.
- More powerful connected to a CRM: it reads the account, ARR, renewal date, contacts, and open cases automatically.
- Sharper with a product-analytics tool: shows whether usage is actually falling, and where it fell off first.
- Sharper with a support or ticketing tool: surfaces the unresolved pain the customer may not be naming.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste the risk signal and the history. The skill builds the full save play today on your real account. No connection required.
- **Connect your tools**: the same skill pulls usage, cases, and dates automatically and adds signals you cannot paste by hand. Same play, less effort, sharper.
- **Just exploring**: no account yet? Get the framework, the exact inputs it reads, and a worked example on a sample account, so you can see the shape before you feed it.

Every run ends with the one input that would sharpen the diagnosis, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org saving at-risk renewals. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| RISK signals | what flagged the account | usage drop, quiet sponsor, escalation, non-renewal notice |
| USAGE source | where adoption lives | product analytics, a usage export |
| SUPPORT source | where unresolved pain lives | ticketing tool, escalation log |
| COMMERCIAL levers | what you can offer | discount, term change, right-size, pause |
| NON-COMMERCIAL levers | what you can do without price | exec sponsor, re-onboarding, new use case, roadmap commit |
| RENEWAL field | the renewal date and ARR | Account.RenewalDate, Account.ARR |
| SAVE window | days you have to work the play | 60 (re-tune to your notice period) |

Diagnose before you discount. A price cut aimed at a product problem loses the money and the account both.

## The method

### Diagnose the real reason
The stated reason ("too expensive") is usually a symptom. Trace it to the root: low adoption, a lost champion, an unresolved escalation, a use case that never landed, a reorg, a competitor. Show the evidence, usage trend, ticket history, sponsor activity, that points to the real cause. Fix the wrong reason and you lose the account anyway.

### Match levers to the cause
Commercial levers (discount, shorter term, right-sizing seats, a pause) fix commercial problems. Non-commercial levers (an executive sponsor, re-onboarding, a new use case, a roadmap commitment, a success plan reset) fix value and relationship problems. Most saves need the non-commercial lever first; the discount alone rarely holds.

### Build the multi-touch sequence
A save is a sequence, not a single call. Space the touches across the save window: an acknowledgment, a working session on the real issue, a value or plan reset, an executive touch, the commercial conversation last. Each touch has an owner, a date, and a goal. One heroic email saves nothing.

### Set the exit criteria
Name what "saved" looks like (renewed, re-engaged, a signed plan) and what "not savable" looks like (no sponsor will engage, the decision is made above your line). Call it early. Effort spent on a dead account is effort stolen from a savable one.

### Escalate deliberately
Say when to pull in a leader or an executive sponsor, and for what. Escalation is a lever, not a panic button. Use it on the touch where a peer-level voice changes the room.

## Quality gates
- The diagnosis names a root cause with evidence, never just the stated reason.
- Commercial levers are matched to commercial causes, not thrown at value problems.
- The sequence has owners and dates on every touch, and the commercial ask comes last.
- The play states its exit criteria, including when to stop. Not every account is savable.

## Output (example)
```
SAVE PLAY · sample account · renewal in 52 days
Stated reason:   "too expensive"
Real reason:     adoption fell after the champion left; usage down sharply
Evidence:        weekly seats dropped by half, sponsor quiet 40 days, 1 open escalation

Levers:
  Non-commercial (first): new exec sponsor intro, re-onboard the team, reset the plan
  Commercial (last):      right-size seats to actual usage, hold the rate

Save sequence (52-day window):
  1. Day 0   CSM      acknowledge, book a working session
  2. Day 5   CSM      resolve the open escalation
  3. Day 14  CSM+Lead re-onboarding + plan reset with the new sponsor
  4. Day 30  Exec     executive-to-executive value check
  5. Day 45  CSM      commercial conversation, right-size to usage

Exit criteria: saved = signed plan + renewal. Not savable = no sponsor engages by day 20.
```

## Where the numbers come from
The usage drops, day counts, and any figure come from the data you paste or the tools you connect. Nothing above is a real customer number; it is illustrative. When the skill cannot see whether usage actually fell, it marks the diagnosis provisional and names the input, a usage export or ticket history, that would confirm it.

## Example chat

**You:** This account says we're too expensive and they're not renewing. Build the save play. Here's what I know: champion left two months ago, usage has been dropping.

**Claude:** Built it, but the stated reason isn't the real one.
```
SAVE PLAY · sample account · renewal in 52 days
Stated reason:   "too expensive"
Real reason:     adoption fell after the champion left; usage down sharply
Evidence:        weekly seats dropped by half, sponsor quiet 40 days

Levers:
  Non-commercial (first): new exec sponsor intro, re-onboard the team
  Commercial (last):      right-size seats to actual usage, hold the rate

Save sequence (52-day window):
  1. Day 0   CSM      acknowledge, book a working session
  5. Day 45  CSM      commercial conversation, right-size to usage
```
Caught the trap: "too expensive" almost always shows up when adoption drops, not the other way around. If I'd taken it at face value, the play would've opened with a discount and lost the account and the margin both.

**You:** What tells us this account isn't actually savable, versus just needs work?

**Claude:** The exit criteria in the plan: if no sponsor engages by day 20, that's the "not savable" line, not a vibe call, a dated checkpoint. Sharpener: connect your product-analytics tool and I'll confirm the usage drop is real instead of working from the note you pasted, so the diagnosis stops being provisional.

## Go further
The diagnosis proves the account is worth the effort. Here is the version that catches it earlier and runs itself.

- **Flag the risk signal automatically.** Connect your product-analytics tool so a usage drop past a set threshold opens a save play in Salesforce before the customer says a word.
- **Route the sequence to real owners with real dates.** Push the multi-touch plan into Salesforce tasks so "Day 5, resolve the open escalation" shows up as an assignment, not a line in a doc.
- **Watch the exit criteria, not just the start.** Schedule a Claude task to check the day-20 checkpoint and alert the CSM lead the moment an account crosses from savable to not.

The account gets diagnosed correctly before anyone reaches for the discount.

## Make it yours
Fork it. Change the risk signals, the levers, the sequence, the save window. The point is not to run someone else's retention script. It is to save the accounts worth saving, for the right reason, and to walk away fast from the ones that are gone. Built by an operator. Customize it, break it, make it better.
