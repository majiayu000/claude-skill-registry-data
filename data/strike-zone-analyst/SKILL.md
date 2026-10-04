---
name: strike-zone-analyst
description: A funnel and account-scoring diagnostic engine for any sales org. Connect a CRM and a product-analytics tool (plus optional enrichment, community, and meeting tools). Three modes. (1) FUNNEL DIAGNOSIS finds leaky conversion gates by channel with per-stage leakage, dollarized leverage points, and cohort velocity. (2) SPRINT PLANNING enriches qualified accounts into a ranked backlog with verified buying committees. (3) SCORING AUDIT finds where your scoring model is missing real ICPs. Trigger on 'funnel diagnosis', 'diagnose the funnel', 'where are we leaking', 'why is [channel] underperforming', 'conversion by channel', 'sprint planning', 'score these accounts', 'find missed ICPs', 'audit the scoring model', or any channel-level cohort-conversion, account-prioritization, or scoring-gap question.
---

# Strike-Zone Analyst: Diagnostic + Sprint Planning + Scoring Audit

## What this does
This is your diagnostic partner for understanding a sales funnel: why it is converting or not, which accounts to work next, and where the scoring model is letting you down. A scoring dashboard tells you what is happening. This skill helps you understand why, what to do about it, and which accounts deserve the next sprint. It works across three modes that share one six-gate funnel framework, one multi-source signal stack, and the same cohort-anchored math.

## What you'll need
You do not need to connect anything to start. Bring your funnel numbers and the skill runs today. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: your funnel counts by stage and channel, with a cohort entry date per channel, plus your fit scores if you have them. Paste or upload.
- More powerful connected to a CRM: cohort dates, stages, scores, contacts, and owners, live.
- More powerful connected to a product-analytics tool: real product engagement for the Product channel.
- Sharper with ICP-qualification, community or intent, enrichment, and meeting tools.

You still need a defined channel taxonomy, a stage model, and a cohort anchor date per channel. Bring them, or map them from your CRM.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your list (a deal export, a stage CSV). The skill runs the full analysis today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the data automatically and adds signals you cannot paste by hand (live activity, product usage, history). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
| Set this | What it is | Default / Example |
|---|---|---|
| CRM connector | Where cohort dates, stages, scores, contacts live | Your CRM |
| Product-analytics connector | Where product-usage events live | Your product-analytics tool |
| ICP-qualification connector | Independent fit qualifier (optional) | Your ICP tool |
| Community/intent connector | Community + buying-committee signals (optional) | Your community tool |
| Enrichment connector | Verified contact data on top-tier accounts (optional) | Your enrichment tool |
| Channels | Your funnel entry channels | Inbound / Outbound / Product |
| Cohort anchor field per channel | The date field that marks funnel entry | A "qualified date" field per channel |
| Qualification stage | The CRM stage that equals SQL | Your "Qualification" stage |
| Discovery stage | The CRM stage that equals SQO | Your "Discovery" stage |
| New-business filter | The opportunity-type filter that excludes renewals | Opportunity type = New Business |
| Fit-score field | The model score you are auditing | Your scoring model's fit score |
| Score floor value | The value your engagement score collapses to when usage is sparse | Your model's floor score |
| Conversion benchmarks | Per-gate target conversion rates | Your trailing baseline |
| Average deal size | Used to dollarize leverage points | Your current ASP |

Swap in your own scoring model, your own selling methodology, and your own channel and stage names. The method below is written against placeholders so it does not assume any one vendor or taxonomy.

## The method

### The six funnel gates
Strike zone is the sequence of conversion gates from a new lead to closed revenue. For each cohort and channel, six gates matter:
1. Cohort created (a qualified-account date fires) to Meeting booked.
2. Meeting booked to Meeting completed (show rate).
3. Meeting completed to SQL (your Qualification stage).
4. SQL to SQO (your Discovery stage).
5. SQO to Closed Won.
6. Closed Won to average deal size and cycle time.

Each gate has a different failure mode and a different intervention. Misdiagnosing the gate wastes weeks fixing the wrong thing.

### Mode 1: Funnel Diagnosis
Default mode is conversational. Work interactively. Do not dump a full report unprompted.
1. Anchor on a channel and a cohort window. Ask what they want to diagnose.
2. Pull live data from the CRM. Always run queries. Do not analyze from memory.
3. Find the leaky gate. Compare each gate to the channel's trailing baseline and to the other channels. The leaky gate has the largest negative gap.
4. Diagnose with the pattern framework. Each leaky gate has two to four known failure modes. Identify which fits.
5. Recommend a specific action. Named: a person, a list of accounts, a process change, a target.
6. Offer the written write-up only if asked.

### Mode 2: Sprint Planning
Converts the funnel from a diagnostic into an execution backlog.
1. Define the cohort. Default: all accounts whose qualified-account date falls in the target window.
2. Multi-source enrich every account in parallel: CRM firmographics and stage, ICP-tool fit, product-analytics engagement, community signals, and enrichment contacts on the top tier only (the paid step, check credits first).
3. Compute composite scores. Tier into Hot, Warm, Watch, Disqualify.
4. Build the spreadsheet: Sprint Ranking, Top Buying Committee, Scoring Rubric, Cohort Summary, Scoring Gaps.
5. Hand off. Reps work the buying-committee tab top-down.

Cost guardrails. The enrichment tool is the only paid source. Cap spend per run unless approved.

### Mode 3: Scoring Audit
When the independent qualifier, product analytics, community signals, and CRM disagree with your scoring model, the disagreement is the finding.
- Model False-Negatives: the engagement score sits at its floor value, but product analytics show real sustained team adoption.
- Model-Missed ICPs: an independent qualifier scores a strong fit, but the model's account-fit score is low or null. A firmographic miss, not an engagement miss.

Common scoring failure modes: score-floor collapse, "no score" read as low fit, no buying-title weighting, no trend velocity, no ICP penetration ratio.

### Action format (all modes)
Every recommendation needs three parts: Who (named person or role), What (a specific change), By when (a date or sprint). If you cannot fill all three, diagnose deeper.

## Quality gates
- Use your own selling methodology consistently. Do not introduce a framework the team does not run.
- Lead with conversion, not volume.
- Cohort math, not snapshot math. Anchor the cohort by entry date and trace it forward.
- Honest caveats. If a cohort is too young or a field is not groupable, say so.
- Use the audience's own taxonomy. Keep expansion as its own motion, not a funnel channel.
- If a channel-source field is a formula field, filter on it but do not group by it.
- Filter renewals out of new-business math.
- If a query needs a field you cannot confirm exists, fail loud and ask. Never invent field names.

## Output (example)
```
STRIKE-ZONE FUNNEL DIAGNOSIS  ·  Trailing 90 days

OUTBOUND COHORT
  Meeting Set:  47
  to SQL:       16  (34%, BELOW 55% target)
  to SQO:        9  (56%, strong)
  to Closed Won: 4  (44%, strong)
  Velocity: avg 82 days meeting to close
  Diagnosis: Leakage at MEETING to SQL. Getting meetings, not qualifying them in.

LEVERAGE POINT (dollarized):
  Outbound meeting-to-SQL +10% = 5 more SQLs per quarter
  At ASP $22K that is +$110K pipeline + 2 more Closed Won
  = +$44K ARR per quarter at current win rate

WHAT MOVES THE NUMBER:
  1. Listen to 5 outbound meeting recordings, find the qualification gap
  2. Test a qualification-first meeting structure on the next 10 outbound meetings
  3. Compare Inbound vs Outbound conversion at the SQL stage to find the delta
```
Use generic placeholder names (Acme, Vertex, Northwind) and "Rep" in your own outputs. Never carry real account or person names into a shared artifact.

## Where the numbers come from
The benchmarks, target rates, the ASP, and the floor score in the example are defaults. Re-tune them to your own data. Set each gate's target from your channel's trailing baseline. Replace the ASP with your current average deal size before dollarizing. Pick a cohort window old enough that the cohort has had time to convert, and report sample size when it is young.

## Example chat

**You:** Outbound felt slow this quarter, can you diagnose the funnel?

**Claude:** Pulled the trailing 90-day cohort.
```
OUTBOUND COHORT (trailing 90 days)
  Meeting Set: 52  ->  to SQL: 19 (37%, below 55% target)
  to SQO: 11 (58%, strong)  ->  Closed Won: 5 (45%, strong)
  Leaky gate: MEETING to SQL
```
Every gate past SQL is healthy, the leak is entirely in qualification, meetings are happening but not converting into real SQLs. Key insight: this is a meeting-quality problem, not a top-of-funnel problem, so adding more outbound volume would have made the wrong number worse. One sharpener: connect the product-analytics tool so Product-channel meetings get graded on real usage instead of self-reported fit.

## Go further
The diagnosis runs once, by hand. Here is where an operator takes it once the manual version proves out.

- **Run the diagnosis every Monday, not just when it's asked.** A scheduled Claude task pulls the trailing-90 cohort from Salesforce weekly and flags the gate that moved past tolerance.
- **Catch the leak while the rep can still fix it.** Wire a Slack alert the moment a meeting-to-SQL rate on a live cohort drops below target, so coaching happens mid-quarter, not in the QBR.
- **Turn Sprint Planning into a standing queue.** Feed qualified accounts through Clay for buying-committee enrichment automatically, so the ranked backlog refreshes without a manual sprint kickoff.

The framework finds the gate; the automation keeps watching it after you look away.


## Make it yours
Fork it, plug in your connectors and thresholds, and break it against your own funnel until it tells you something true. Built by an operator. Customize it, break it, make it better.
