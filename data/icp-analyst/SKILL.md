---
name: icp-analyst
description: Turn "is this account a real fit?" into a stacked verdict. A composite 0-100 fit score built from every signal you have, a breakdown by source, override flags for when a scoring tool is wrong, a channel classification, and a written rationale. Built for reps, marketers, and RevOps, customizable to your CRM and whatever scoring you use. Trigger on "is {account} a real fit?", "score this list against our profile", "find lookalikes to our best customers", "why is the score wrong on {account}?", "validate this prospect list", "what's our coverage in {segment}?", or any account or list qualification.
---

# ICP Analyst

## What this does
Takes an account, or a whole list, and tells you whether it actually fits your ideal customer profile. It rolls every signal you have, firmographics, product usage, hiring intent, tech stack, into one 0-100 score, shows you which source drove it, and flags the accounts where a scoring tool is plain wrong. Then it tags each verdict with the channel it belongs to, so the play is obvious.

## What you'll need
You do not need to connect anything to get value today. Bring your accounts and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: a list of accounts, with domain, employee count, industry, and any signal you know (funding stage, hiring, tools they use). Paste it or upload a CSV.
- More powerful connected to a CRM: it reads firmographics and any existing scores automatically across your book.
- Sharper with an account fit score or scoring vendor: it folds that score in as one input and tells you when to trust it.
- Sharper with a product-analytics tool: it adds a product-side fit signal from real usage.
- Sharper with an enrichment tool: it confirms employee count, hiring, and technographic stack.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your account list. The skill scores every row today on your real data. No connection required.
- **Connect your tools**: the same skill pulls firmographics, scores, usage, and enrichment automatically, and folds each into the composite. Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact inputs it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B team scoring accounts against a defined profile. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| FIT score | your account fit score or vendor score | any account-scoring source |
| PROFILE | what "good" looks like | your ICP definition (size, industry, stage, region) |
| SIGNAL sources | hiring, funding, product usage | an enrichment tool, a product-analytics tool |
| DISPLACEMENT stack | competitor tools worth a switch play | the tools you replace |
| WEIGHTS | how much each input counts | see The method (re-tune) |

Run any profile you like. The skill scores "does this account match the profile you defined," so point it at your criteria, not anyone else's.

## The method

### Composite fit score (0-100)
One headline number, built from weighted inputs. A starting split that you re-tune:
- 35% account fit: employees, industry, funding stage, region.
- 25% product-side signal: real usage or a product-engagement score, if connected.
- 20% hiring and intent: recent hiring, funding, growth signals.
- 15% tech-stack displacement: accounts running tools you replace are switch candidates.
- 5% qualification completeness: a bonus if a rep has already done the homework.

Penalties subtract from the total: too small or off-profile, an already-saturated customer, recently churned inside a cooling-off window, or already worked by another rep (avoid the double-tap).

### Source breakdown, never a single number
Every score shows its parts. If a source is missing, the skill says so ("no product-analytics connected, score is from fit, hiring, and stack only") instead of hiding the gap.

### Override detection
When the composite disagrees with a scoring tool, it says so out loud. An account a tool scored low while hiring 14 reps and running a stack you displace is a false negative the tool missed. An account a tool scored high with none of the real signals is a false positive. Both get flagged with the reason.

### Channel classification
Every verdict is tagged Inbound (they came to you), Product (they self-served a signup), or Outbound (you go to them). The play and the outreach differ by channel, so the tag ships with the score.

### Lookalike search
Anchor on your highest-value customers and find accounts matching their profile, employee count, industry, funding stage, and technographic stack.

## Quality gates
- No single-source fit claim. The breakdown by source ships with every score, and missing sources are declared.
- Override visibility. When the composite disagrees with a scoring tool, it says so and names why.
- Channel-tagged outputs. Every verdict carries Inbound, Product, or Outbound, because the play changes with the channel.

## Output (example)
```
ACME CORP · Fit Score 87 / 100 · STRONG FIT

Source breakdown:
  Account fit score:        78 / 100  (strong, approved)
  Product-side signal:      real usage detected
  Enrichment:               805 employees, 22 reps, 14 hiring
  Tech-stack displacement:  3 tools you replace
  Qualification:            complete, homework done
  Channel:                  Outbound + Product (hybrid)

Signals:
  Account fit: SaaS, 500+ employees, late stage, target region
  Hiring 14 reps is a top-of-funnel scream
  3-tool consolidation is a strong messaging hook
  A rep has already qualified it

Verdict: STRONG FIT. Pursue with full outbound. The hybrid channel means a
cold sequence into the usual entry role, plus a watch for any signup from
this domain that would trigger an inbound handoff.

Override: none. The fit score and the composite agree.
```

## Where the numbers come from
The weights (35/25/20/15/5) and the penalties are a starting point, not a law. They suited one B2B motion. If product usage matters more to you than hiring, shift the weight. The scoring logic does not change, the weights are yours.

## Example chat
Here is the skill running on a real account, start to finish.

**You:** Is acme.com a real fit? Score it against our profile, and tell me if the vendor score is right.

**Claude:** Composite lands at 87, strong fit, and it overrides your vendor tool.
```
Source breakdown:
  Account fit score:   78/100  (approved)
  Product-side signal: real usage detected
  Enrichment:           805 employees, 14 hiring
  Tech-stack:           3 tools you replace
  Channel:              Outbound + Product (hybrid)
```
The override is the finding: your vendor score said 78 and called it borderline, but 14 open sales reqs plus a 3-tool displacement opportunity are the kind of signal a firmographic-only score can't see. That's the false negative this skill exists to catch. One sharpener: connect a product-analytics tool so the usage signal comes from real data instead of "detected," which right now is the softest part of the read.

## Go further
The verdict is step one. Here is where an operator takes it once the manual version proves out.

- **Score the whole book overnight.** Point a scheduled Claude task at Salesforce and your enrichment tool nightly, and write the composite and the override flag back to the account record.
- **Catch only the disagreements.** Post to Slack just the accounts where the composite and the vendor score diverge by more than 20 points, so a human only looks at the interesting ones.
- **Turn the strong fits into a list.** Feed every STRONG FIT verdict into Clay or a sequencer so the outbound list builds itself from the accounts that actually clear the bar.

You built the override once, now it runs against every account, every night.


## Make it yours
Fork it. Change the weights, the penalties, the sources. The point is not to run someone else's playbook. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
