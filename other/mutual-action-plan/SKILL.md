---
name: mutual-action-plan
description: Turn "let's stay in touch" into a dated plan to signature that you and the champion own together. Lays out every milestone from today to signed, with an owner and a date on each, plus the exit criteria that say the deal is real. Written to send, so the buyer can react to something concrete. Built for B2B sales teams, customizable to your process and your CRM. Trigger on "build a mutual action plan", "close plan", "MAP for this deal", "path to signature", "what are the next steps", or any late-stage deal you need to drive.
---

# Mutual Action Plan

## What this does
Builds the plan that gets a deal from today to signed, jointly, with your champion. It lays out the milestones between here and signature, puts a name and a date on each one, and states the exit criteria that prove the deal is actually moving. It writes the whole thing as something you can send, so the buyer commits to real steps instead of vague enthusiasm.

## What you'll need
You do not need to connect anything to get value today. Bring what you know about the deal and the skill runs now. Connect the tools below and it grounds the plan in the real close date and the real committee.

- Works today with: the deal basics you can paste, the target close date, the steps you know are coming (legal, security, procurement), and who is involved. The skill turns them into a dated, owned plan.
- More powerful connected to a CRM: it reads the close date, the stage, and the contact roles, so the plan lines up with the deal the pipeline already believes in.
- Sharper connected to a meeting or email tool: it pulls what the champion already agreed to, so the plan reflects commitments, not hopes.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the deal facts you give it today and gets sharper as you connect tools. It never invents a milestone the buyer never agreed to. A step with no owner or no date is a gap the plan surfaces, not one it papers over.

- **Bring your data**: paste the deal, the close date, and the steps you know. The skill returns the full milestone plan, owners, dates, and exit criteria, written to send. No connection required.
- **Connect your tools**: the same skill reads the close date and roles from the deal and the champion's agreements from the calls. Same plan, grounded in what is real.
- **Just exploring**: no live deal? Get the milestone structure, the owner-and-date discipline, and a worked example on a sample deal, so you can see the shape before you send one.

Every run ends with the one milestone that has no owner or no date yet, because that is the one that slips the deal.

## Customize this for yourself
This was built for a B2B SaaS org running a committee sale. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| CLOSE field | the target signature date | Opportunity.CloseDate |
| STAGE field | the opportunity stage | Opportunity.StageName |
| MILESTONE set | your standard path to signed | eval, business case, legal, security, procurement, sign |
| ROLES | who owns which step | AE, champion, EB, legal, IT, procurement |
| EXIT criteria | what proves each step is done | your definition of done per stage |
| BUFFER days | slack before the close date | 5 (re-tune to your cycle) |

Build the plan around your real buying process, not a generic template. The skill puts a name and a date on every step and shows you the ones you left blank.

## The method

### Backward from the signature date
Start at the target close date and work backward, placing each milestone so the whole chain lands on time with a buffer. If the steps do not fit before the date, the date is the fiction, and the plan shows it now instead of at quarter end.

### An owner and a date on every line
Every milestone has exactly one owner and one date. "The team will handle legal" is not a plan. "Champion sends the agreement to legal by the 14th" is. A line with a missing owner or date is flagged, because that is where deals stall.

### Exit criteria, not activities
Each milestone states what proves it is done, not just that it happened. "Security review complete" is an activity. "Security signs off in writing, no open items" is an exit criterion. The plan tracks the criteria.

### Shared, not sent one way
The plan is built with the champion and owned by both sides. Half the milestones belong to the buyer. That shared ownership is the test: a champion who will not take a single dated step is telling you the deal is not real yet.

### Written to send
The output is drafted as something the buyer reads, reacts to, and edits. Concrete steps give them something to push back on, and the pushback is where you learn what the deal actually needs.

## Quality gates
- No milestone without one owner and one date. Blanks are flagged, not hidden.
- At least one buyer-owned step early, as a live test that the champion will act.
- Exit criteria are written as proof of done, never as "in progress."
- The chain fits before the close date with a buffer, or the date is flagged as at risk.

## Output (example)
```
MUTUAL ACTION PLAN · illustrative deal · target sign: end of quarter
#  Milestone                     Owner        Date     Exit criteria
1  Confirm success criteria      AE + champ   day 0    Written, both agree
2  Business case to committee    Champion     day 5    On the committee agenda
3  Security review               IT / vendor  day 12   Signed off, no open items
4  Legal + redlines              Legal        day 20   Redlines resolved
5  Procurement + PO              Procurement  day 26   PO issued
6  Signature                     EB           day 30   Contract signed

Flags:
  - Milestone 2 owner is the champion. If they will not take it, the deal is not real.
  - No date yet on procurement contact. Get the name before milestone 3.
```

## Where the inputs come from
The owner-and-date rule, the exit-criteria discipline, and the backward-from-signature build are the defaults that keep a close plan honest. The milestone set and the buffer are yours. If your process has more gates, add them. The discipline does not change: every line owned, every line dated, every line with a definition of done. The plan is yours.

## Example chat
Here is the skill running on a real deal, start to finish.

**You:** Build the MAP for Acme. Target close is end of quarter, and we're heading into security review next.

**Claude:** Backward-planned from the sign date, buyer-owned steps flagged.
```
2  Business case to committee    Champion     day 5    On the committee agenda
3  Security review               IT / vendor  day 12   Signed off, no open items

Flags:
  - Milestone 2 owner is the champion. If they won't take it, the deal isn't real.
```
The catch worth naming: milestone 2 is the test, not a formality. It's the first buyer-owned step, and it's early on purpose, if the champion won't commit to a dated action this soon, that's a live signal the deal is softer than the stage says, weeks before it would show up in a forecast call. One sharpener: connect your CRM so the close date and stage come from the real opportunity instead of the number you typed in.

## Go further
The plan is step one. Here is where an operator takes it once the manual version proves out.

- **Send it and track opens.** Drop the MAP into a doc or email tool that reports when the champion opens and edits it, so you know if it's being used or ignored.
- **Flag slipping milestones automatically.** Wire a scheduled Claude task to check each dated milestone against today and post to Slack the moment one goes overdue.
- **Roll the pattern up across the pipeline.** Pull every open MAP from Salesforce and report which champions are missing their buyer-owned steps this week, so a sales leader sees the soft deals before the forecast call.

You built the plan once, now the slippage gets caught in real time.


## Make it yours
Fork it. Change the milestones, the roles, the buffer. The point is not to send someone else's close plan. It is to build a dated path to signature that your champion will actually co-own, and to find the blank line before it costs you the quarter. Built by an operator. Customize it, break it, make it better.
