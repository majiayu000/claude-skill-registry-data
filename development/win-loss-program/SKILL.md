---
name: win-loss-program
description: Turn scattered closed deals into a win/loss program that changes what you ship and what you say. Picks who to interview, gives you the question guide, codes themes across deals so a pattern beats a single anecdote, and turns the pattern into a specific messaging or product change. Built for B2B GTM, product, and RevOps leaders, customizable to your motion and your CRM. Trigger on "start a win-loss program", "why are we losing deals", "run win-loss interviews", "what patterns are in our closed-lost", "who should I interview", or any win/loss or closed-deal analysis.
---

# Win-Loss Program Builder

## What this does
Stands up a repeatable win/loss program instead of a one-off post-mortem. It chooses which won and lost deals to interview and why, hands you the question guide that gets past "price," codes the answers into themes across many deals so you act on a pattern and not the loudest anecdote, and turns that pattern into a named change to the message or the product.

## What you'll need
You do not need to connect anything to get value today. Bring a list of recent closed deals and the skill runs now. Connect the tools below and it selects the interview slate and pulls the deal context automatically.

- Works today with: a list of recently won and lost deals, with segment, deal size, competitor if known, and the stated reason. Paste it or upload a CSV.
- More powerful connected to a CRM: it reads closed-won and closed-lost with stage history and loss reasons so the sample is not cherry-picked.
- Sharper with a call-recording or meeting tool: it mines what buyers actually said, not just the field a rep typed.
- Sharper with a survey or feedback tool: it folds structured buyer responses into the same theme coding.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the list you give it today and gets more powerful as you connect tools. It never invents a loss reason it cannot see. A blank reason is a prompt to interview, not a guess.

- **Bring your data**: paste or upload your closed deals. The skill builds the slate and the guide today on your real deals. No connection required.
- **Connect your tools**: the same skill pulls closed-won and closed-lost with history and call context automatically, so the sample and the themes are grounded, not anecdotal.
- **Just exploring**: no data yet? Get the framework, the question guide, and a worked example on sample deals, so you can see the shape before you feed it.

Every run ends with the one input that would make the next round sharper, a loss-reason field to add or a source to connect.

## Customize this for yourself
This was built for a B2B SaaS org running competitive, committee-driven deals. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| SCOPE | which deals qualify | closed in the last 1 to 2 quarters |
| MIX | won-to-lost interview split | roughly half and half, plus no-decisions |
| SAMPLE | how many interviews per round | 10 to 20 to see a pattern |
| SELECTION | who to prioritize | by segment, deal size, competitor, reason |
| INTERVIEWER | who runs them | a neutral third party, never the deal rep |
| THEMES | the coding buckets | product gap, message, price, trust, timing |
| PATTERN_BAR | when a theme becomes a finding | a theme across 3+ independent deals |
| OWNER | who acts on each finding | PMM for message, product for gaps |

Run any theme taxonomy you like. The skill codes across deals and requires a pattern before it recommends a change, so point it at your buckets, not anyone else's.

## The method

### Who to interview
Do not only interview losses, and do not let reps pick. Build a slate across MIX so you learn from wins, losses, and no-decisions, because a no-decision is a loss to the status quo and it teaches the most. Prioritize by SELECTION so the sample spans segments and competitors, not just the three deals someone remembers. Use a neutral INTERVIEWER, because buyers do not tell the rep who lost them the real reason.

### The question guide
Get past the stated reason. "Price" is almost never the reason, it is the reason that is polite to say. Ask what they were solving, who else was in the room, what nearly changed their mind, and what the winner did that you did not. Ask the same core questions every time so answers are comparable across deals. Open questions first, then probe, never lead.

### Coding themes across deals
Tag every interview into THEMES, then count across the sample. One buyer saying the onboarding scared them is an anecdote. Five saying it is a finding. A theme is only a finding when it clears PATTERN_BAR across independent deals, so a single loud loss cannot set the roadmap. Show the theme counts and the deals behind each.

### From pattern to change
Every finding gets an owner and a specific change, not a discussion. A message theme goes to PMM as a positioning or objection-handling change. A product theme goes to product as a gap with the deals it cost. A trust or proof theme becomes a case study or a security page. The program has failed if it produces a deck nobody acts on, so each finding ends as a named change with an owner and a date.

## Quality gates
- Interviews are run by a neutral party, never the rep who owned the deal.
- Wins and no-decisions are in the sample, not only losses.
- No theme becomes a finding until it clears the pattern bar across independent deals.
- "Price" is probed, never accepted at face value as the real reason.
- Every finding ends with a named owner and a specific change, not a summary slide.

## Output (example)
```
WIN-LOSS PROGRAM · 14 interviews · illustrative
Sample:  6 lost · 5 won · 3 no-decision · mix of segments and 2 competitors

Themes (count across independent deals):
  Product gap: integration missing      5 deals   FINDING
  Message: value story unclear early     4 deals   FINDING
  Trust: no proof at our size            3 deals   FINDING
  Price stated as reason                 4 deals   probe showed it was fit, not price

Changes:
  1. Integration gap -> Product. Costed 5 deals this quarter. Roadmap review.
  2. Value story -> PMM. Rewrite the first-call narrative, ship objection guide.
  3. Proof gap -> PMM. Publish 2 case studies in the losing segment.
```

## Where the numbers come from
SAMPLE (10 to 20), PATTERN_BAR (3+ deals), and the MIX split are defaults, not laws. They suited a mid-market competitive motion. If your deal volume is lower, run smaller rounds more often and let patterns build over time. The coding logic does not change. The thresholds are yours.

## Example chat

**You:** We've closed 14 deals this quarter, can you build a win-loss round?

**Claude:** Built the slate and the guide.
```
Sample: 6 lost, 5 won, 3 no-decision, mix of segments and 2 competitors
Themes: Product gap (integration missing) - 5 deals - FINDING
        Message: value story unclear early - 4 deals - FINDING
        Price stated as reason - 4 deals - probe showed it was fit, not price
```
Key insight: "price" showed up in 4 deals as the stated reason, but the probe questions revealed it was actually a fit mismatch dressed up as price, that is the whole reason to run structured interviews instead of trusting the CRM's closed-lost field. One sharpener: connect a call-recording tool so the coding is grounded in what buyers actually said, not a rep's summary of the call.

## Go further
The round is coded. Here is where an operator takes it once the manual version proves out.

- **Pull the sample without manual CRM digging.** A scheduled Claude task pulls closed-won and closed-lost from Salesforce every quarter and proposes the interview slate automatically, mixed across segments and competitors.
- **Mine the calls you already have.** Run past discovery and closing calls through Gong to pre-code themes before a single interview is booked, so live conversations go deeper instead of covering ground you already have.
- **Turn findings into tracked work.** Push each finding with its owner and deadline straight into a task tool or Slack channel for PMM and product, so "the value story is unclear" does not die in a deck.

The interviews find the pattern; the automation is what makes sure it turns into a shipped change.


## Make it yours
Fork it. Change the themes, the sample, the owners. The point is not to run someone else's win-loss deck. It is to run yours, coded across deals and ending in a change someone actually ships. Built by an operator. Customize it, break it, make it better.
