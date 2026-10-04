---
name: paid-ads-plan
description: Turn "we should run some ads" into a paid-ads plan you can hand to a buyer. Audiences, the offer per audience, the creative angles, the budget split, the metric that calls it a win, and a kill rule so you stop feeding losers. Built for B2B marketing teams, customizable to your channels and your funnel. Trigger on "build a paid ads plan", "how should we split budget", "what should the ads say", "what's our target CPL", "when do we kill a campaign", or any paid-media planning question.
---

# Paid-Ads Plan

## What this does
Takes a campaign goal and a budget and turns it into a plan a media buyer can execute: who you are targeting, what you put in front of each audience, the angles the creative should test, how the money splits, the one number that means it worked, and the rule that tells you when to shut a line off. It plans the campaign. It does not spend the money for you.

## What you'll need
You do not need to connect anything to get value today. Bring your goal and budget and the skill runs now. Connect the tools below and it pulls performance automatically and sharpens the targets with your real numbers.

- Works today with: a campaign goal, a monthly or total budget, who you sell to, and the offer you want to run. Paste it in a sentence or two.
- More powerful connected to an ad platform: it reads spend, impressions, clicks, and cost per result across your live campaigns, so the budget split and targets start from history, not guesses.
- Sharper with a web-analytics tool: closes the loop from click to signup or pipeline, so you optimize to the metric that pays, not the one that is easy.
- Sharper with a CRM: ties ad-sourced leads to real opportunities, so cost per lead becomes cost per qualified lead.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the brief you give it today and gets more powerful as you connect tools. It never invents a benchmark it cannot see. A missing number is a prompt, not a guess.

- **Bring your data**: paste the goal, budget, audience, and offer. The skill builds the full plan today. No connection required.
- **Connect your tools**: the same skill reads live spend and results and rebuilds the split and targets on your own history. Same plan, grounded in what actually converts for you.
- **Just exploring**: no campaign yet? Get the framework, the exact inputs it reads, and a worked example on sample numbers, so you can see the shape before you commit a dollar.

Every run ends with the one thing that would make the next run sharper, a target to add or a tool to connect.

## Customize this for yourself
This was built for a B2B team running paid social and search to a demo or trial. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CHANNELS | where you buy | paid search, paid social, retargeting |
| PRIMARY_GOAL | what the campaign is for | demo requests, trial starts, MQLs |
| WIN_METRIC | the number that means it worked | cost per qualified lead, pipeline per dollar |
| GUARDRAIL_METRIC | the number that caps waste | max CPL, min CTR, min landing conversion |
| BUDGET | total or monthly spend | your figure |
| KILL_WINDOW | how long a line runs before you judge it | 7 to 14 days, or a minimum spend |
| ATTRIBUTION | how you credit the click | last-touch, first-touch, your model |

The metrics below are illustrative placeholders, not benchmarks. Replace them with your own targets.

## The method

### Audiences (start narrow)
List the distinct audiences worth separate money: by segment, by intent, by stage. Cold prospecting, warm retargeting, and existing-list expansion are different buyers and should never share a budget line or a target. Name each one and why it is a real audience, not a slice you invented.

### Offer per audience
Each audience gets one offer matched to its temperature. Cold traffic rarely buys a demo on the first touch, so cold usually gets a low-friction offer (a guide, a teardown, a tool). Warm retargeting gets the direct ask. Never run the same offer to a stranger and to someone who already visited your pricing page.

### Creative angles (test the message, not just the image)
For each audience, name 2 to 4 angles to test: the pain, the outcome, the proof, the contrarian take. Angles are hypotheses about what the buyer cares about. You are buying data on which one is true. Hold the offer steady and let the angle be the variable.

### Budget split
Split the budget across audiences and angles with a bias: most of the money to the audience most likely to convert, a fixed slice reserved for testing new angles. Write the split as percentages that sum to 100, and note the reasoning so a buyer can defend it.

### Win metric and guardrail
Pick one WIN_METRIC the whole campaign is judged on, tied as close to revenue as your tools allow. Pick one GUARDRAIL_METRIC that caps waste. Clicks and impressions are diagnostics, not wins. If the only number you can see is a vanity number, say so and name the tool that would fix it.

### Kill rule
Write the rule before you launch, so you kill on evidence, not on feelings. A line dies when it passes KILL_WINDOW and misses the guardrail with enough spend to trust the read. Winners get more budget, losers get cut, and the test slice refills with new angles.

## Quality gates
- Every audience has its own offer. No shared line between cold and warm.
- The win metric is the closest thing to revenue your tools can see, and the skill names what it cannot yet see.
- The kill rule is written before launch, with a spend floor so you are not reading noise.
- Any number shown as a target is labeled illustrative unless it came from your connected data.

## Output (example)
```
PAID-ADS PLAN · Q3 demo push · $18K/mo (illustrative)
Audience          Offer              Angles                 Split   Win metric
Cold, paid social Teardown guide     Pain / Outcome / Proof  40%    CPL under target
Cold, paid search Demo (high intent) Outcome / Contrarian    30%    Cost per qualified lead
Retargeting       Book a demo        Proof / Urgency         20%    Demo booked
Test reserve      rotating           new angles              10%    signal only

Kill rule: any line past 10 days and 1.5x target CPL with >$500 spend gets cut.
Reallocate to the top performer, refill the test reserve with a fresh angle.

Next move: connect the ad platform so the split starts from your real cost-per-result,
not these placeholders.
```

## Where the inputs come from
The goal, budget, audiences, and offers come from you or your marketing plan. Spend, impressions, clicks, and cost per result come from an ad platform once connected. Click-to-signup and click-to-pipeline come from a web-analytics tool and a CRM. Every target in the plan is illustrative until it is grounded in your own connected numbers, and the skill says which is which.

## Example chat

**You:** We've got $18K a month for a demo push in Q3. Build me a plan. Selling to RevOps leads at mid-market SaaS.

**Claude:** Here's the split, with a kill rule built in before a dollar spends.
```
Audience          Offer              Angles                 Split   Win metric
Cold, paid social Teardown guide     Pain / Outcome / Proof  40%    CPL under target
Retargeting       Book a demo        Proof / Urgency         20%    Demo booked
Test reserve      rotating           new angles              10%    signal only

Kill rule: any line past 10 days and 1.5x target CPL with >$500 spend gets cut.
```
The thing to notice: cold traffic gets the low-friction offer (a guide) and retargeting gets the direct ask. Same audience, same offer would have wasted the cold budget on people who aren't ready to book.

**You:** What's our actual CPL target? I don't have a number.

**Claude:** You don't have one yet, and I flagged that as illustrative rather than guessing a benchmark. Once the ad platform is connected I can pull your real cost-per-result and set the target from your own history instead of an industry number that may not fit your funnel. Sharpener: connect the ad platform so the split and the kill rule start from your actual spend, not a placeholder.

## Go further
A plan on paper is the easy half. Here's where it becomes a system that spends the budget for you, inside guardrails you set.

- **Feed it live numbers, not a paste.** Connect the ad platform so cost-per-result updates the plan automatically, and the win metric stops being a guess.
- **Close the loop to revenue.** Wire in a web-analytics tool and the CRM so cost per lead becomes cost per qualified pipeline dollar, the number that actually matters to a buyer of this plan.
- **Let the kill rule fire itself.** A scheduled Claude task checks every line against the guardrail daily and posts to Slack the moment a line crosses 1.5x target CPL, instead of waiting for the weekly review to notice.

Plan the campaign once. Let the connectors keep it honest every day after.

## Make it yours
Fork it. Change the audiences, the split logic, the kill window, the metric that counts. The point is not to run a generic media plan. It is to run yours, with a stop-loss you wrote on purpose. Built by an operator. Customize it, break it, make it better.
