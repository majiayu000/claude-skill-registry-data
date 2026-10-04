---
name: prospecting-analyst
description: Turn "which leads should I work?" into a lead-by-lead work plan. Per-lead status (never-touched, engaged-not-replied, gone-cold, hot), days-dark per lead, last-touch quality, a re-engagement ranker, and a recommended next action for every lead. Built for SDRs and full-cycle reps, customizable to your CRM and your outreach tool. Trigger on "which leads should I work?", "who haven't I touched?", "show me cold leads", "hot leads to follow up on", "who's gone dark?", "re-engagement candidates", or any lead-level work-assignment question.
---

# Prospecting Analyst

## What this does
Reads your leads and hands you a ranked work plan for the day. It sorts every lead into a clear status, hot, cold, never-touched, or replied-but-dropped, tells you how many days each one has been dark, and names the next move for each. The point is to open your list and know exactly what to work first, not to guess.

## What you'll need
You do not need to connect anything to get value today. Bring your leads and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: a list of your leads, with name, company, last activity date, and any engagement you know about (opens, clicks, replies). Paste it or upload a CSV.
- More powerful connected to a CRM: it reads status and last-touch automatically across your whole book.
- Sharper with an email or sequencing tool: it sees opens, clicks, replies, and enrollment, so hot-vs-cold is real, not a guess.
- Sharper with an account fit score: it ranks never-touched leads by fit instead of alphabetically.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a signal it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your lead list. The skill runs the full analysis today on your real leads. No connection required.
- **Connect your tools**: the same skill pulls status, last-touch, and engagement automatically, so hot-vs-cold reflects reality across both your CRM and your outreach tool. Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a rep working a lead list against a CRM and an outreach tool. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| OUTREACH tool | where opens, clicks, replies live | your email or sequencing tool |
| STATUS field | lead or contact status | Lead.Status, a custom stage |
| ACTIVITY field | where last-touch lives | LastActivityDate, task and event dates |
| FIT score | how you rank a fresh lead | your account fit score, or blank |
| HOT_DAYS | recent-reply window that means work now | 7 (re-tune) |
| COLD_DAYS | no-touch days that mean gone cold | 30 (re-tune) |

Run any status model you like. The skill classifies "where is this lead in my motion," so point it at your fields, not anyone else's.

## The method

### Per-lead status (4 states)
Every lead gets exactly one: HOT, ENGAGED, COLD, NEVER_TOUCHED.
- HOT: replied, clicked, or asked for a meeting inside HOT_DAYS. Work today.
- ENGAGED: in an active sequence or touched recently, but no reply yet.
- COLD: engaged historically, now dark past COLD_DAYS. A re-engagement candidate.
- NEVER_TOUCHED: no outreach yet. Start fresh, ranked by fit.

### Two-source status, never one
A lead that replied in your outreach tool but shows a stale last-touch in the CRM is HOT, not COLD. Status reads both sources and takes the freshest signal. If only one source is connected, it says so and works from what it has.

### Re-engagement ranker
Cold leads are scored by fit, time since last touch, and how deeply they engaged before going dark. A lead who replied warmly and then went quiet outranks one who only ever opened an email.

### Re-engagement candidates name the trigger
Not "follow up with this lead." Instead, "replied positively earlier this quarter, no contact since, a recent role change or funding round is a fresh reason to reopen." The trigger is the reason to reach out now.

### Next-action recommender
Every lead carries a specific motion: reply now, book the meeting, run a re-engage touch, or start a fresh sequence. Hot leads decay, so the list sorts by urgency, a reply from six days ago is more urgent than one from two days ago.

## Quality gates
- No HOT or COLD call from a single source when two are connected. The freshest signal wins.
- Re-engagement candidates name the trigger, never just "follow up."
- Hot leads are sorted by decay, oldest reply first, because reply rates fall every day you wait.
- The most expensive miss, a reply you never followed up, is surfaced first.

## Output (example)
```
LEAD WORK PLAN · 47 leads, ranked by priority

HOT · work today (5)
  1. Contact @ Acme Corp     replied "interested" 2d ago, no follow-up
  2. Contact @ Vertex        booked a meeting 1d ago, prep it
  3. Contact @ Blend Labs    opened 4 emails in 3d, no reply yet
  4. Contact @ Northwind     clicked pricing yesterday
  5. Contact @ Halo Freight  replied "send more info" 5d ago, no follow-up

RE-ENGAGE · work this week (12 ranked)
  1. Contact @ Summit        warm reply last quarter, role change is a fresh trigger
  2. Contact @ Meridian      engaged, then went dark, new funding round
  ...

COLD · when the hot queue is clear (8)
  ...

NEVER TOUCHED · start fresh (22), sorted by fit
  1. Contact @ Anvil (fit 91, signal: hiring 14 reps)
  2. Contact @ Beacon (fit 88, signal: recent raise)
  ...

Most expensive miss this week:
  Acme Corp (#1) replied 2 days ago. Every day of delay costs reply rate.

Recommended order:
  1. Reply to Acme now (under 2 minutes)
  2. Prep the Vertex meeting
  3. Run the re-engage touch for Summit and Meridian
  4. Start 5 fresh sequences from the top of never-touched
```

## Where the numbers come from
HOT_DAYS (7) and COLD_DAYS (30) are defaults, not laws. They suited a fast outbound motion. If your cycle runs slower, raise them. The status logic does not change, the thresholds are yours.

## Example chat

**You:** Here's my lead export, 47 leads, mix of never-touched and stuff I ran a sequence on a while back. Who do I work today?

**Claude:** Sorted all 47. Five are hot and none have a follow-up logged yet.
```
LEAD WORK PLAN · 47 leads, ranked by priority

HOT · work today (5)
  1. Contact @ Acme Corp     replied "interested" 2d ago, no follow-up
  2. Contact @ Vertex        booked a meeting 1d ago, prep it

RE-ENGAGE · work this week (12 ranked)
  1. Contact @ Summit        warm reply last quarter, role change is a fresh trigger

Most expensive miss this week:
  Acme Corp (#1) replied 2 days ago. Every day of delay costs reply rate.
```
Worth flagging: Acme replied in your outreach tool, but their CRM record still shows no activity. Reading only the CRM would have put them in Cold. That two-source check is why they landed in Hot instead.

**You:** Why is Summit worth re-engaging and not just "follow up sometime"?

**Claude:** Because there's a trigger: Summit replied warmly last quarter, went dark, and just had a role change on the account. That's a real reason to reopen the conversation now, not a guess. Sharpener: connect your fit score and I'll rank the never-touched pile (22 of your 47) by who's worth working first instead of alphabetically.

## Go further
The read is step one. Here is where an operator takes it once the manual version proves out.

- **Score every lead nightly.** Run this as a scheduled Claude task against your sequencer and CRM so the work plan is waiting before the morning stand-up.
- **Alert on the expensive miss.** DM the rep in Slack the moment a hot reply crosses 24 hours with no follow-up, instead of waiting for the next manual pull.
- **Feed the never-touched list to enrichment.** Route the fit-ranked never-touched pile into Clay so outreach starts with the right contact info already filled in.

You built the ranking once; now it watches the clock for you.

## Make it yours
Fork it. Change the states, the thresholds, the fields. The point is not to run someone else's playbook. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
