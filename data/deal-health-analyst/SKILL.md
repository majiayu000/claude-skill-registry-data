---
name: deal-health-analyst
description: Turn "is this deal real?" into a deal-by-deal risk verdict. An 8-state risk taxonomy, a qualification-vs-stage gap check, multi-thread coverage, days-dark per deal, and a commit-creep watch. Built for B2B sales teams, customizable to your CRM and your sales process. Trigger on "how are my deals", "which deals are stuck", "what's at risk this month", "is the rep sandbagging", "multi-thread check", or any open-deal diagnostic.
---

# Deal-Health Analyst

## What this does
Reads your open opportunities and gives each one a straight verdict: healthy, slipping, stuck, or dead. It checks whether a deal has real activity behind it, whether the rep actually qualified it, and whether they are talking to more than one person. Then it names the next move on the deals that need one.

## What you'll need
You do not need to connect anything to get value today. Bring your deals and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: a list of your open deals, with stage, amount, close date, last activity date, and the contacts on each. Paste it or upload a CSV.
- More powerful connected to a CRM: it reads all of the above automatically, across the whole pipeline.
- Sharper with a meeting or email tool: tightens the multi-thread and gone-dark checks.
- Sharper with a product-analytics tool: adds usage momentum on trials.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your list (a deal export, a stage CSV). The skill runs the full analysis today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the data automatically and adds signals you cannot paste by hand (live activity, product usage, history). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running a staged pipeline. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| STAGE field | the opportunity stage | Opportunity.StageName |
| FORECAST field | commit / best-case category | ForecastCategoryName |
| QUALIFICATION fields | your methodology's fields | MEDDIC, BANT, your custom fields |
| ACTIVITY sources | where "last touch" lives | Account, Opportunity, Task, Event dates |
| CONTACT ROLES | how you see who is on a deal | OpportunityContactRole |
| DARK_DAYS | no-activity days that mean at risk | 14 (re-tune to your cycle) |
| STUCK_DAYS | days in one stage that mean stuck | 21 (re-tune) |

Run any methodology you like. The skill checks "is this deal qualified for the stage it claims," so point it at your qualification fields, not anyone else's.

## The method

### Deal-risk verdict (8 states)
Every open deal gets exactly one: HEALTHY, MOMENTUM, AT_RISK, SLIP_RISK, STUCK, STALE, CHAMPION_DROP, GHOST.
- GHOST: no activity across any activity source for DARK_DAYS or more. Must show the source dates that prove it.
- STUCK: same stage past STUCK_DAYS with no forward step.
- SLIP_RISK: close date inside the period, but activity or qualification is thin.
- CHAMPION_DROP: your main contact has gone quiet, no touches in 30 days.
- AT_RISK: single-threaded, fewer than 2 contacts engaged in 30 days.
- MOMENTUM and HEALTHY: real activity, multi-threaded, qualified for stage.

### Activity check (multi-source)
Days dark is today minus the most recent touch across ALL your activity sources, not one. A deal is GHOST only if every source is cold. Show the dates.

### Qualification-vs-stage gap
If a deal claims a late stage but the qualification fields for that stage are empty, flag it and name the exact field that is missing. This is the "is the rep sandbagging" check. It is only as good as the fields you map.

### Multi-thread check
Fewer than 2 contacts engaged in 30 days is single-thread risk. One champion is one point of failure.

### Commit-creep watch
Flag deals that quietly moved from Commit to Best Case in the trailing two weeks. That movement is the forecast telling on itself.

## Quality gates
- No GHOST verdict without showing the activity dates that prove it.
- Qualification gaps surface field by field, named, never "incomplete."
- Forecast accuracy is trailing-quarter, never trailing-week. Small samples lie.

## Output (example)
```
ACTIVE DEAL HEALTH · 7 open opps
Account     Stage / ARR    Risk      Days-Dark   Why
Acme Corp   Sol Val/$45K   HEALTHY   2           Multi-thread + qualified
Vertex      Prop/$67K      SLIP      12          Champion went quiet
Blend Labs  Sol Val/$28K   STUCK     23          No next step set
Northwind   Eval/$112K     GHOST     47          Zero activity, all sources

Next moves:
  1. Vertex. Re-engage the champion. The deal has no second thread.
  2. Blend Labs. Add the missing next step before the next review.
  3. Northwind. Declare it lost or run one final outreach this week.
```

## Where the numbers come from
DARK_DAYS (14), STUCK_DAYS (21), and the multi-thread cutoff (2 contacts in 30 days) are defaults, not laws. They suited a mid-market SaaS cycle. If your deals run longer, raise them. The logic does not change. The thresholds are yours.

## Example chat
Here is the skill running on a real pipeline export, start to finish.

**You:** Run deal health on my pipeline, here's the export. [pastes CSV]

**Claude:** Scored all 7 against the 8-state taxonomy.
```
Account     Stage / ARR    Risk      Days-Dark   Why
Northwind   Eval/$112K     GHOST     47          Zero activity, all sources
Vertex      Prop/$67K      SLIP      12          Champion went quiet
```
The catch: Northwind has been sitting in your Best Case column for a month with zero activity across every source. That is not a slipping deal, it is a dead one still counted in forecast.

**You:** Is Vertex sandbagged or actually healthy?

**Claude:** Checked the qualification-vs-stage gap: Vertex claims Proposal but the decision-dynamics field is empty, no named economic buyer. That is a real gap, not paperwork. The deal should not be this far along without it. One sharpener: connect a meeting tool so days-dark counts actual call activity, not just CRM-logged touches.

## Go further
The read is step one. Here is where an operator takes it once the manual version proves out.

- **Run this before every forecast call.** Schedule a Claude task to score the full pipeline every Thursday and post the GHOST and STUCK deals to the sales leader's Slack DM.
- **Catch commit-creep in real time.** Connect Salesforce field-history tracking so any deal moving from Commit to Best Case triggers an alert the same day, not two weeks later.
- **Tighten the multi-thread check.** Connect Gong or your email tool so days-dark and contacts-engaged pull from real conversation data instead of manually logged activity.

The read is only as good as its refresh rate. Automate the refresh.

## Make it yours
Fork it. Change the states, the thresholds, the fields. The point is not to run someone else's playbook. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
