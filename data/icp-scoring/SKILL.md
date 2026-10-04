---
name: icp-scoring
description: Turn a pile of accounts into a stack-ranked priority list with a reason on every row. A layered score (gates first, then an evidence-weighted base rank over the signals you actually have, then bounded boosts for product usage and buyer intent) that stays fair across channels and never scores a blank field as a zero. Built for B2B GTM teams, customizable to your signals and your ICP. Trigger on "score these accounts", "rank by fit", "composite ICP score", "stack-rank my list", "who should I work first", "prioritize these leads", or any multi-signal account qualification.
---

# ICP Scoring

## What this does
Reads a list of accounts and gives each one a fit score and a rank, with the reasoning spelled out per account: what pushed it up, what held it back, and what you could not see. It blends many signals into one number without letting the signal you happen to have the most of drown out the ones you have less of. The output is a stack rank you can work top-down, plus a short "why this score" on every row.

## What you'll need
You do not need to connect anything to get value today. Bring your accounts and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: a list of accounts and whatever signals you already have (domain, size, tech stack, recent hiring, website CTA, product usage, buyer intent). Paste it or upload a CSV.
- More powerful connected to a CRM: it reads your account fields automatically, across the whole list.
- Sharper with enrichment tools: fills the gaps (firmographics, technographics, hiring, contacts) so more signals are present per account.
- Sharper with a product-analytics tool: adds live usage as a boost on accounts already in your product.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a signal it cannot see. A missing signal is renormalized out of the math, never scored as a zero.

- **Bring your data**: paste or upload your list. The skill runs the full score today on your real signals. No connection required.
- **Connect your tools**: the same skill pulls firmographics, usage, and intent automatically and fills the gaps you could not paste. Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact signals it reads, and a worked example on sample accounts, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper: a signal to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org scoring accounts across mixed acquisition channels. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| SIGNAL LIBRARY | the signals you score on | size band, tech stack, hiring, website CTA, usage, intent |
| GATES | hard caps applied before ranking | email-stack fairness, ICP disqualifier, no-sales-motion |
| WEIGHTS | how much each signal counts | evidence-weighted, renormalized over the signals that are filled |
| ESCALATORS | bounded additive boosts on top of the base rank | product usage +6 / +12, buyer intent +8 / +15 |
| TIERS | the score bands | Hot >=80 / Warm 65-79 / Watch 50-64 / DQ <50 |
| STRIKE_BAND | the action cutoff (work these first) | >=90 |

Score on the signals you actually have. The skill does not care whose weights they are; point it at your ICP evidence, not anyone else's.

## The method

### Score modes (pick by lifecycle, never by channel)
Three modes read one signal library: NEW-BUSINESS (accounts you have not sold), EXPANSION (current customers), WIN-BACK (churned accounts). Mode is chosen by commercial state. Channel segments an account inside a mode, it never picks the mode and it is never a scoring input.

### Layer 0: gates
Hard caps applied before any ranking. Examples: an email-stack fairness multiplier so an account on a provider that fits your motion is not penalized against one that does not; an ICP disqualifier cap when a hard "not our fit" signal is present; a "no sales-motion fingerprint" cap. Gates answer yes/no questions from the cheapest source first. A DNS MX lookup for the email stack costs nothing and covers every domain, so it beats a paid field.

### Layer 1: base rank, renormalized over the signals you have
score = SUM(weight x value x filled) / SUM(weight x filled). Only the signals actually present count toward the denominator, so a missing enrichment field is never scored as a zero. A Coverage stamp caps the score and says so when too little is filled. This is the channel-fair core: every account is ranked on its own present signals, and the highest-fill signal cannot dominate the rest.

### Layer 2: escalators (bounded, additive)
Product usage and buyer intent add points on top. They add, they never multiply, because multiplying saturates the ceiling and buries the base rank. Example bands: product usage +6 for a foothold, +12 for real depth; buyer intent +8 for one in-market person, +15 for two or more. Disqualified accounts get their boosts capped low so a gate is never bought back by usage.

### Reasoning per account ("why this score")
Every row ships with its evidence in order: the live escalators first (usage, intent, the outreach hook), then the fit case (tech-stack match, hiring, a displaceable competitor, a talk-to-sales CTA), then the qualifiers, then the caveats stated plainly (disqualifier cap, coverage cap, unknown-stack haircut). A score is never delivered without its evidence.

## Quality gates
- No score without its per-component reasoning. Every row explains itself.
- Missing signals are renormalized out, never scored as zero.
- A Coverage stamp rides on every account; a thin account is flagged, not silently ranked next to a fully-enriched one.
- Weights change only through a pre-registered lift test, never a hunch. A new signal enters at weight zero, shadow-scores, earns its weight, then gets promoted.
- Recompute a handful of scores by hand every run; they must match the machine.

## Output (example)
```
ICP STACK RANK - 8 accounts
Account      Score  Tier    Why
Acme Corp    92     Hot     CRM in stack + hiring 3 sales roles + demo CTA; 12 weekly users
Vertex       78     Warm    Right size + hiring; no product usage yet
Blend Labs   64     Watch   Fits size band; thin coverage (2 of 6 signals)
Northwind    38     DQ      Disqualifier cap: not our motion

Work first (>=90 strike band):
  1. Acme Corp. Product foothold plus in-market this week. Lead with the usage hook.
```

## Where the numbers come from
The weights, the +6 / +12 escalator bands, and the tier cutoffs (Hot / Warm / Watch / DQ) are defaults from one team's win/loss backtest, not laws. They fit that team's motion. If your ICP is different, re-fit them on your own closed cohort. The layering logic (gate, renormalize over filled, add bounded boosts) is the part that carries over; the exact numbers are yours to earn.

## Example chat
Here is the skill running on a real list, start to finish.

**You:** Score this list of 8 accounts and give me a stack rank I can work top-down.

**Claude:** Ranked, gated, and every row has its reasoning.
```
Account      Score  Tier    Why
Acme Corp    92     Hot     CRM in stack + hiring 3 sales roles + demo CTA; 12 weekly users
Northwind    38     DQ      Disqualifier cap: not our motion
```
The thing worth catching: Blend Labs scored 64 on 2 of 6 signals filled, which is the coverage cap doing its job, a thin account never gets to hide next to a fully-enriched one at the same score. One sharpener: connect an enrichment tool so accounts like Blend Labs get scored on their real signals instead of getting capped by what's missing.

## Go further
The rank is step one. Here is where an operator takes it once the manual version proves out.

- **Rescore the pipeline nightly.** Point a scheduled Claude task at Salesforce and your enrichment stack, and write the score, tier, and reasoning back to each account record every night.
- **Alert on the strike band only.** Send a Slack DM to the account owner the moment an account crosses the >=90 strike threshold, so the hottest accounts get worked same-day.
- **Backtest the weights on a real cohort.** Pull closed-won and closed-lost from Snowflake or Salesforce quarterly and re-fit the escalator bands against what actually converted, instead of leaving them frozen at launch defaults.

You built the rank once, now it stays current without anyone re-running it by hand.


## Make it yours
Fork it. Change the signals, the weights, the escalators, the tiers. The point is not to run someone else's scoring model. It is to run yours, faster, with the reasoning attached so a rep trusts the rank. Built by an operator. Customize it, break it, make it better.
