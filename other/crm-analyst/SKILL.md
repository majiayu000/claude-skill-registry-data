---
name: crm-analyst
description: Turn "what's happening with this account?" into a structured read straight from your CRM. A real-activity audit across every source, a qualification-vs-stage gap check, a one-screen account summary, and a risk verdict on the deal. Built for any sales team, customizable to your CRM and your sales process. Trigger on "analyze this account", "what's happening with this deal", "is this opp healthy", "what's stuck in my pipeline", "deal autopsy on this closed-lost", "where am I missing qualification coverage", "prep me for this account", or any account, opp, or pipeline diagnostic.
---

# CRM Analyst

## What this does
Reads a single account or deal out of your CRM and gives a straight, structured read: current state, when it was last actually touched, whether the rep did the qualification work the stage claims, and one risk verdict on the deal. It is the sixty-second account summary that tells you what to do next, and the "is the rep BS-ing this deal" check that a single CRM field misses.

## What you'll need
You do not need to connect anything to get value today. Bring an account or deal export and the skill runs now. Connect your CRM and it pulls the same data automatically, across the whole pipeline.

- Works today with: a CRM export for the account or opp, with stage, amount, close date, last-activity dates, the qualification fields, and the contacts on the record. Paste it or upload a CSV.
- More powerful connected to a CRM: it reads all of the above automatically, and audits activity across every source, not one field.
- Sharper with an enrichment tool: adds firmographic and buying-committee context. Deepline is one generic example.
- Sharper with a meeting or email tool: tightens the last-touch and champion-drop checks.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload the account or opp export. The skill runs the full read today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the record automatically and audits activity across every source, so a deal never looks dead just because one field is blank. Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to map or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running a staged pipeline. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| STAGE field | the opportunity stage | your stage field |
| AMOUNT field | current and forecasted value | amount, ARR, contract value |
| QUALIFICATION fields | your methodology's fields | MEDDIC, BANT, your custom framework |
| ACTIVITY sources | every place a "last touch" lives | account, opp, task, event dates |
| CONTACT ROLES | how you see who is on a deal | your contact-role object |
| DARK_DAYS | no-activity days that mean at risk | 14 (re-tune to your cycle) |
| STUCK_DAYS | days in one stage that mean stuck | 21 (re-tune) |

Run any methodology you like. The skill checks "is this account qualified for the stage it claims," so point it at your qualification fields, not anyone else's.

## The method

### Multi-source activity check
Days dark is today minus the most recent touch across ALL your activity sources: the account record, the opp record, completed tasks, and logged events. Never a single field. This solves the classic CRM bug where the opp-level last-activity date is blank because reps log emails and meetings at the account or contact level, so a live deal gets falsely flagged as dead. The skill takes the max across sources and shows the dates.

### Account summary (one screen)
Current state, owner, value, days in current stage, last real activity, and the single risk flag. The read a rep or leader needs before walking into a meeting, on one screen.

### Qualification-vs-stage gap
If a deal claims a late stage but the qualification fields for that stage are empty, flag it and name the exact field that is missing. This is the sandbagging detector. It is only as good as the fields you map.

### Deal-risk verdict
One verdict per open opp: HEALTHY, MOMENTUM, AT_RISK, SLIP_RISK, STUCK, STALE, CHAMPION_DROP, GHOST. GHOST needs every activity source cold and the dates to prove it. CHAMPION_DROP means the main contact has gone quiet. AT_RISK means single-threaded.

### Account context
Pull the firmographic and buying-committee context that lives on the record: decision maker, tech stack, hiring or expansion signals. An optional enrichment tool fills what the CRM does not carry.

## Quality gates
- No GHOST verdict without showing the activity dates, across every source, that prove it.
- Qualification gaps surface field by field, named, never "incomplete."
- The activity check reads every source, never one field. A single-field read systematically misses real activity.
- Never report a field the export does not contain. A missing field is a prompt, not a guess.

## Output (example)
```
ACME CORP · Customer · CSM: owner

Verdict: REACH_OUT (renewal-defence read)
  Last activity: TODAY (account level) - 6 email replies + meeting in 1h
  Days in current stage: 12d (late stage)
  Qualification: 4/4 complete - problems, leverage, decision dynamics, next steps
  Fit-score check: score looks low, but real usage present -> false negative

The qualification read
  PROBLEMS: inbox plateau, no signal on adoption depth
  LEVERAGE: multi-team rollout across Sales, RevOps, CS
  DECISION DYNAMICS: CFO signs, RevOps lead champions
  NEXT STEPS: finalize commercial terms by the 15th

Tech stack: email, CRM, an outbound tool
Decision maker: the CFO
Signal: hiring 14 reps at this account - expansion

Next move: the meeting today. Late stage means commercial close is the gate.
```

## Where the numbers come from
DARK_DAYS (14) and STUCK_DAYS (21) are defaults, not laws. They suited a mid-market SaaS cycle. If your deals run longer, raise them. The multi-source activity rule is not a threshold, it is the correct way to read a CRM, and it does not change. The thresholds are yours.

## Example chat
Here is the skill running on a real account before a rep walks into a meeting.

**You:** Give me the read on Acme Corp before my call in an hour.

**Claude:** Read's done, and the fit score on this account is wrong.
```
Verdict: REACH_OUT (renewal-defence read)
  Last activity: TODAY (account level), 6 email replies + meeting in 1h
  Fit-score check: score looks low, but real usage present ->
  false negative
```
The fit score was pulling from a single stale field, but checking activity across every source, account, opp, tasks, and events, shows this account is very much alive. That's the classic bug where an opp-level date sits blank because reps log the real activity elsewhere, so a live deal gets falsely flagged as dead. One sharpener: connect a meeting tool so the last-touch and champion checks tighten beyond what's logged in the CRM.

**You:** Check qualification against the stage it claims.

**Claude:** Ran it. 4 of 4 fields complete, this one's not being sandbagged.
```
PROBLEMS: inbox plateau, no signal on adoption depth
LEVERAGE: multi-team rollout across Sales, RevOps, CS
DECISION DYNAMICS: CFO signs, RevOps lead champions
NEXT STEPS: finalize commercial terms by the 15th
```
Late stage and full qualification agree here, which is the opposite of what usually triggers a flag. The gap check exists to catch the deal that claims Stage 4 with an empty decision-dynamics field, this one earns its stage. One sharpener: connect an enrichment tool so the tech-stack and hiring-signal context refreshes automatically instead of going stale between calls.

## Go further
The read is step one. Here's where an operator takes it once the manual version proves out.

- **Run the read on the whole pipeline, not one account.** Point a scheduled Claude task at Salesforce nightly and flag every deal that just moved from HEALTHY to AT_RISK or STUCK.
- **Kill sandbagging before the forecast call.** Post any qualification-vs-stage gap straight to the manager's Slack the moment a rep advances a stage without the fields to back it.
- **Feed the false-negative catch upstream.** Wire the fit-score correction back into your scoring model's exception list so the same account doesn't get mis-scored again next cycle.

You built the read once; now it runs itself.


## Make it yours
Fork it. Change the states, the thresholds, the qualification fields. The point is not to run someone else's playbook. It is to read your own pipeline the way you actually sell, faster. Built by an operator. Customize it, break it, make it better.
