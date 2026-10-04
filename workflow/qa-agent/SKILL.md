---
name: qa-agent
description: The analyst that watches your other analysts. It reads the trail your reports and workflows leave behind, then surfaces scoring blind spots, CRM hygiene gaps, and workflow drift, and turns every miss into a training signal. Built for GTM teams running any stack of reports, customizable to your process. Trigger on "run QA", "weekly QA report", "system health check", "where are our scoring blind spots", "what should we coach on this week", "audit our workflow performance", or any system-level health or feedback-loop question.
---

# QA Agent (the meta-analyst)

## What this does
Most reporting is one-shot: produce the work, ship it, move on, and nothing learns from the misses. This skill is the feedback layer that sits on top of everything else you run. It reads the audit trail your other reports and workflows leave behind, then tells you where the system is getting things wrong and what to fix first. Every override, every empty CRM field, every workflow that quietly failed becomes a signal that compounds into a sharper system next week.

## What you'll need
You do not need to connect anything to get value today. Bring the logs and outputs your reports already produce and the skill runs now. Connect the tools below and it pulls them automatically and watches more of the system.

- Works today with: any record of what your reports and workflows did. Paste or upload a log of overrides, flagged deals, workflow runs, or CRM-gap lists. A CSV of "what we scored vs what happened" is enough to start.
- More powerful connected to a CRM: it reads field-population rates and staleness across the whole book automatically.
- Sharper with a messaging tool: it posts the weekly digest and critical alerts where the team already works.
- Sharper with a code or file host: it verifies published reports still render and that shared manifests have not drifted.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your logs (overrides, workflow runs, CRM-gap exports). The skill runs the full QA pass today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the trails automatically and watches signals you cannot paste by hand (live field coverage, deploy state, message reactions). Same output, less effort, sharper.
- **Just exploring**: no logs yet? Get the framework, the exact streams it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a stream to add or a tool to connect.

## Customize this for yourself
This was built for a GTM team running several reports on a shared pipeline. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| AUDIT sources | where your reports log what they did | override logs, workflow run logs, CRM-gap exports |
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| STALE_DAYS | notes age that means the account is neglected | 180 (re-tune to your cadence) |
| HYGIENE fields | fields that must be filled to trust a record | decision maker, last activity date, your custom fields |
| SCORE sources | the scores you want to check for drift | your account fit score, product-engagement score, any model |
| DELIVERY | where the weekly digest lands | a messaging DM, a channel, email |
| CADENCE | how often the QA pass runs | weekly (a Sunday-evening digest before the Monday review) |

Point it at your logs and your fields, not anyone else's. The skill checks "is the system doing what we think it is," whatever your system is.

## The method

### Scoring accuracy
For every model you run, check whether its calls held up. When you overrode a score and marked an account as under-rated, did it become a real deal? Report the precision as a plain hit rate. Track score drift over a trailing window so you catch a model quietly getting looser or tighter. Where two of your reports disagree on the same account, one says healthy and another says the champion went dark, surface it to a calibration queue instead of picking a winner silently.

### CRM hygiene
Per owner, count the records that fail your trust bar: notes older than STALE_DAYS, a null decision maker, an opportunity with no last-activity date, a late-stage deal missing the fields that stage demands. Report the field-by-field fill rate, and the trend versus last week, so hygiene is a direction, not a one-time scold.

### Enrichment and data gaps
Where you fill data from providers, track the not-found rate per provider over time and the cost per verified field. Flag the records that came back empty three or more runs in a row, they need manual sourcing. Watch for patterns in what fails, a segment or region where one provider is consistently weak.

### Workflow performance
Per workflow, track success and failure rate over time, which connector was unavailable on a given run, and the failure-mode breakdown (connector missing, data not found, models disagreed, a validation check failed). Surface the top workflows by usage and by failure rate.

### Engagement decline
If your team gets a recurring drop of leads or actions to work, watch whether they act on it. Claim rate, first-touch rate, and follow-through rate, per person and per day. Watch streaks and catch a week-over-week decline before it becomes a habit.

### System health
Broken links to published reports must be zero, surface any immediately. Watch shared manifests for entry-count drift. Flag anyone writing to a single-owner file who should not be. Track deploy lag so a report is not stale by the time someone opens it.

## Quality gates
- No accuracy claim without the underlying calls that prove it. "82% precision" means naming the calls, not asserting a number.
- Hygiene gaps surface owner by owner and field by field, named, never "incomplete."
- Accuracy is measured over a trailing window, never a single week. Small samples lie.
- Recommendations are surgical: a named owner, a named issue, and one next move, never "improve hygiene."

## Output (example)
```
WEEKLY QA DIGEST · Week of May 25

SCORING ACCURACY
  Override precision: 82% (19 of 23 flagged accounts became real deals)
  Fit-score drift: +4 pts over trailing 30d (scoring tighter, expect recalibration)
  Deal-risk classifier: 8 of 11 flagged slip-risk deals actually slipped (73%)

CRM HYGIENE (top 3)
  1. 17 of 24 cross-rep deals incomplete for current stage (71%). No change vs last week.
  2. Rep C: 14% field-completeness (1 of 7 opps). Lowest on the team. Top coaching priority.
  3. 12 accounts with notes older than 180 days. Refresh in the next 1:1s.

DATA GAPS
  Provider A not-found rate jumped to 31% (baseline 12%). Investigate freshness.

ENGAGEMENT
  Average claim rate 67% (above 60% target). Longest streak: Rep A, 4 days at 100%.
  Concern: Rep D claim rate 23%. Onboarding check needed.

SYSTEM HEALTH
  Zero broken report links. Zero manifest violations. All green.

TOP RECOMMENDATIONS
  1. Rep C: 1:1 on field completion, the biggest team-level coaching priority.
  2. Send the under-scored-segment list back to your scoring owner to recalibrate.
  3. Investigate Provider A data freshness.
```

## Where the numbers come from
STALE_DAYS (180), the trailing window for drift, and the engagement targets are defaults, not laws. They suited a mid-market GTM cadence. If your cycle runs longer, raise them. The logic does not change. The thresholds are yours.

## Example chat

**You:** Run QA on this week's numbers. Here's the override log and the CRM export.

**Claude:** Ran the full pass. Two things worth your attention before the review.
```
SCORING ACCURACY
  Override precision: 82% (19 of 23 flagged accounts became real deals)

CRM HYGIENE (top 3)
  1. Rep C: 14% field-completeness. Lowest on the team. Top coaching priority.

TOP RECOMMENDATIONS
  1. Rep C: 1:1 on field completion.
```
The catch: two of your reports disagree on the same account, one calls it healthy, the other flags the champion as dark, so instead of picking a winner I put it in a calibration queue rather than silently trusting either one.

**You:** Good catch. Is 82% actually good or is that just a number?

**Claude:** On its own it's just a number, that's why the digest names the calls, 19 of 23 flagged accounts, not "most." Compare it week over week and you'll see whether the model is getting sharper or looser. Sharpener: connect your CRM directly and I'll pull field-population rates live instead of working off this week's export, so hygiene becomes a trend instead of a snapshot.

## Go further
The weekly pass proves where the system is lying to itself. Here is the scaled version.

- **Run it every Sunday night.** Schedule this as a Claude task so the digest lands in Slack before the Monday pipeline review, not after.
- **Watch the disagreements live.** Wire it to Salesforce and Amplitude so it flags every account where two reports disagree the moment the data updates, not once a week.
- **Track the trendline in one place.** Log each week's digest to a Snowflake table or a sheet so drift and hygiene become a chart, not a memory.

The system starts grading itself instead of waiting for you to notice the drift.

## Make it yours
Fork it. Change the streams it reads, the trust bar, the cadence. The point is not to run someone else's QA. It is to make your own system learn from itself, so next week's outputs are better than this week's. Built by an operator. Customize it, break it, make it better.
