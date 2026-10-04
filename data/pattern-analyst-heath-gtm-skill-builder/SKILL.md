---
name: pattern-analyst
description: Your won/lost/churn pattern analyst. Connect a CRM plus a product-analytics tool, then turn retrospective data into forward-looking action. Three modes. (1) WON, win pattern recognition that feeds your ICP and lookalike search. (2) LOST, loss pattern plus competitive intel that feeds a messaging refresh. (3) CHURN, churn theme extraction plus predictive scoring (which active accounts look like recent churners?). Trigger on "why are we winning?", "why are we losing?", "closed-lost autopsy", "churn patterns", "competitive intel rollup", "who do we lose to most?", "show me lookalike candidates to {winning customer}", "predictive churn", "which active accounts look like churners?", or any portfolio-level pattern recognition.
---

# Pattern Analyst

## What this does
This skill reads your closed-won, closed-lost, and churned accounts and finds the repeating patterns inside them. It runs in three modes. WON tells you what your winning deals have in common and generates a ranked list of active accounts that look like them. LOST tells you where, how, and to whom you lose, with the objections rolled up. CHURN groups your lost customers into named themes and then scans your active book for accounts that match those themes before they leave.

## What you'll need
You do not need to connect anything to start. Bring your closed and churned deals and the skill runs today. Connect the tools below and it pulls the cohorts automatically and adds signals you cannot paste by hand.

- Works today with: exports of your closed-won, closed-lost, and churned accounts, with fields like size, industry, loss reason, and competitor. Paste or upload.
- More powerful connected to a CRM: the three cohorts and their fields, live.
- More powerful connected to a product-analytics tool: engagement decay, which powers the predictive-churn scan.
- Sharper with a conversation-intelligence tool (objections, competitive mentions) and a support tool (churn-ticket patterns).

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your list (a deal export, a stage CSV). The skill runs the full analysis today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the data automatically and adds signals you cannot paste by hand (live activity, product usage, history). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
| Set this | What it is | Default / Example |
| --- | --- | --- |
| CRM connector | Where your won/lost/churn cohorts live | Any CRM |
| Won/lost stage field | The field that marks a deal won or lost | Stage = Closed Won / Closed Lost |
| Loss reason field | Reason a deal was lost | A loss-reason field |
| Competitor field | Named competitor a deal was lost to | A competitor field |
| Churn signal | How you mark a lost customer vs a lost new deal | Type = Renewal AND Stage = Closed Lost |
| Segment fields | Account fields used for lookalike matching | Employee count, industry, tech stack, channel, primary signal |
| Activity signal | The product-analytics metric for engagement decay | 30-day active-user trend |

Map each row to the actual field name in your system. If a pattern depends on a field you do not have, the skill runs the modes it can and tells you which one it skipped and why.

## The method
### WON mode
Cohort: trailing 6 months of closed-won. Extract buying-committee shape, deal velocity, primary entry point, dominant signals, tech-stack overlap. Score active accounts against the winning pattern and rank the closest matches.
### LOST mode
Cohort: trailing 6 months of closed-lost. Competitive head-to-head by stage and deal size. Objection theme rollup from transcripts. Stage-of-loss distribution.
### CHURN mode
Cohort: trailing 12 months of churned customers. Group churns into named causes (consolidation, layoff, vendor switch, product gap, champion left, acquisition). Scan active accounts for matches to each theme and surface them with a confidence tag, ranked by risk.

## Quality gates
- Pattern extraction is statistically meaningful. The skill requires at least 5 occurrences before it calls something a pattern. Below that it returns "insufficient data, expand the window."
- Lookalike candidates are similarity-scored, with the named dimensions behind the score.
- Predictive churn calls are confidence-tagged with the evidence behind them. A low-confidence match is labeled low, not dropped.

## Output (example)
```
PATTERN ANALYSIS  ·  Q2 Lookback

WON (n=14):
  Channel: Product 57% / Inbound 29% / Outbound 14%
  Dominant signal: sales-team hiring (78% of wins)
  Top lookalikes: Account A 91%, Account B 88%, Account C 87%

LOST (n=21):
  Stage-of-loss: Solution Validation 52%
  Top reason: "no compelling differentiation vs incumbent" (n=9)
  Lost to Competitor 1: 5 (at Proposal, "team already trained")

CHURN (n=8, 12 months):
  Consolidation / layoff (n=3), acquisition (n=2), feature gap (n=2)
  PREDICTIVE WATCH:
    Account F, consolidation pattern (73%): team 22 to 14, activity -47%
    Account G, champion-left pattern (68%): champion changed jobs 21d ago
```

## Where the numbers come from
Defaults to re-tune: win/loss windows 6 months trailing, churn window 12 months, pattern floor of 5 occurrences before something is named a pattern. Lookalike and churn-match scores are built from your segment fields; add or drop dimensions to fit what predicts outcomes in your data. The activity-decay threshold flags an at-risk account; tune it to your product's normal usage rhythm. Re-tune the windows and the pattern floor first.

## Example chat

**You:** Run the churn mode on last year's losses and tell me who in the active book looks like them.

**Claude:** Grouped the churns into named themes and scanned the active book.
```
CHURN (n=8, 12 months):
  Consolidation / layoff (n=3), acquisition (n=2), feature gap (n=2)
  PREDICTIVE WATCH:
    Account F, consolidation pattern (73%): team 22 to 14, activity -47%
    Account G, champion-left pattern (68%): champion changed jobs 21d ago
```
Account G is the one worth calling today. A champion change 21 days ago is an early signal, not a lagging one, and it's a pattern we've seen precede churn twice this year.

**You:** Is that confidence score reliable with only 8 churns in the sample?

**Claude:** Good catch, that's below the 5-occurrence floor for calling something a firm pattern on its own, but consolidation clears it at n=3 within the theme. Champion-left only has n=1 backing Account G's match, so I'm labeling that one low-confidence rather than dropping it. Sharpener: connect a conversation-intelligence tool so champion-change signals get caught from call transcripts instead of relying on a manual note.

## Go further
Running this quarterly on an export proves the patterns hold. Here's the version that watches the active book continuously.

- **Scan the book every week, not once a quarter.** A scheduled Claude task reruns the predictive-churn match against Salesforce weekly and only surfaces accounts whose risk score moved.
- **Catch the champion-left pattern the day it happens.** Connect Gong or a similar conversation-intelligence tool so a champion mentioning a new role gets flagged automatically instead of waiting for the account owner to notice.
- **Feed WON mode straight into prospecting.** Push the lookalike list into Clay or your outbound tool so the accounts that score closest to your winning pattern become a working list, not a slide.

The patterns are only useful the week you'd actually act on them.

## Make it yours
Map the fields, set your windows, and decide which signals predict a win and a churn in your business. Built by an operator. Customize it, break it, make it better.
