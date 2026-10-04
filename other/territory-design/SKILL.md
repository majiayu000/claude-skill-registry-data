---
name: territory-design
description: Turn "who owns what" into fair, balanced territories reps will not fight over. Sets the segmentation, distributes accounts, checks balance across every rep, and writes the rules for disputes and inbound before they blow up in a QBR. Built for B2B sales and RevOps leaders, customizable to your segments and your CRM. Trigger on "design territories", "carve up the patches", "are these territories fair", "balance the book", "who gets inbound", or any territory or account-assignment build.
---

# Territory Designer

## What this does
Takes your account universe and cuts it into territories that are balanced on the thing that matters, usually potential, not just account count. It picks the segmentation axis, distributes accounts across reps, runs a fairness check so no rep is handed a dead patch, and writes the dispute and inbound rules up front so ownership is decided before the deal, not during it.

## What you'll need
You do not need to connect anything to get value today. Bring your account list and the skill runs now. Connect the tools below and it balances on real potential instead of a headcount split.

- Works today with: a list of accounts with a size or potential signal (employees, revenue, tier), region or segment, and current owner if any. Paste it or upload a CSV.
- More powerful connected to a CRM: it reads owners, open pipeline, and won history so balance accounts for work already in flight.
- Sharper with an enrichment or firmographic source: it fills missing size and industry so the segmentation is not guesswork.
- Sharper with a data warehouse: it weights territories by modeled potential, not a single raw field.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the list you give it today and gets more powerful as you connect tools. It never invents an account attribute it cannot see. A blank field is a prompt, not a guess.

- **Bring your data**: paste or upload your account list. The skill runs the full carve today on your real accounts. No connection required.
- **Connect your tools**: the same skill pulls owners, pipeline, and firmographics automatically, so balance reflects real work and real potential.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample accounts, so you can see the shape before you feed it.

Every run ends with the one input that would make the next carve sharper, a potential signal to add or a source to connect.

## Customize this for yourself
This was built for a B2B SaaS org assigning named accounts to a field team. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| AXIS | how you split territories | geography, segment, industry, named |
| POTENTIAL | the balance metric | employees, revenue band, fit score |
| BALANCE_ON | what you equalize | total potential, not account count |
| TOLERANCE | allowed spread across reps | within 10 to 15 percent of the mean |
| MAX_ACCOUNTS | book size ceiling per rep | 40 to 80 by segment |
| INBOUND_RULE | how a new lead gets an owner | match on domain, then territory |
| DISPUTE_RULE | who wins a contested account | first meaningful activity wins |
| HOUSE | unassigned or held accounts | no-owner pool for round-robin |

Run any segmentation you like. The skill balances and writes the rules, so point it at your axis, not anyone else's.

## The method

### The segmentation
Pick the axis that matches how you actually sell. Geography suits high-volume field motions. Named accounts suit enterprise. Industry suits a vertical play. State the axis, then hold it consistent, because a book that is half geo and half named is a book nobody can be measured on.

### The account distribution
Assign accounts to reps against the axis, then sort by POTENTIAL so the strong and weak accounts are spread, not clumped. A territory that is all logos and no potential is a punishment. Keep each book under MAX_ACCOUNTS so coverage is real, not a name on a list.

### The balance check across reps
Sum POTENTIAL per rep and compare to the mean. Flag any book outside TOLERANCE. Balance on potential, not on account count, because 60 strong accounts and 60 dead ones are not the same job. Show the spread so the split survives the room.

### The rules for disputes and inbound
Write these before go-live. Inbound: a new lead routes by INBOUND_RULE, usually domain match to an owned account first, then territory. Disputes: name the tie-breaker, usually first meaningful activity, and the escalation path. Held and no-owner accounts go to a house pool with a claim rule. The point is that ownership is decided by policy, not by whoever shouts first.

## Quality gates
- Balance is checked on potential, never on raw account count alone.
- Every rep book is shown against the mean with the spread named, not asserted "fair."
- Inbound and dispute rules are written and dated before assignments go live.
- No account is left with two owners or none, the overlap and orphan lists are shown.

## Output (example)
```
TERRITORY DESIGN · 6 reps · illustrative
Rep        Accounts   Potential idx   vs mean   Flag
North      52         104             +4%       ok
South      48         98              -2%       ok
East       61         131             +31%      over, rebalance
West       39         71              -29%      thin, add accounts
Central    50         100             0%        ok
House      44         -               -         round-robin pool

Rules set:
  1. Inbound routes on domain match, then territory. No manual grabs.
  2. Contested account goes to first meaningful activity, RevOps breaks ties.
  3. East is 31% over the mean. Move ~8 accounts to West before launch.
```

## Where the numbers come from
TOLERANCE (10 to 15 percent), MAX_ACCOUNTS (40 to 80), and the balance metric are defaults, not laws. They suited a mid-market field team. If your reps carry fewer, larger accounts, tighten the ceiling and widen the tolerance. The fairness logic does not change. The thresholds are yours.

## Example chat

**You:** We're carving territories for next quarter. Here's the account list with employee counts and regions.

**Claude:** Carved it and ran the balance check.
```
Rep      Accounts  Potential idx  vs mean  Flag
North    52        104            +4%      ok
East     61        131            +31%     over, rebalance
West     39        71             -29%     thin, add accounts
```
East is 31% over the mean, that's not a headcount problem, it's a potential problem, moving accounts by count alone would have left East still overloaded. Key insight: balance has to run on potential, not account count, or a rep with 60 dead accounts looks equal to a rep with 60 strong ones. One sharpener: connect the CRM for open pipeline so the rebalance does not accidentally move a deal mid-cycle.

## Go further
The carve is set. Here is where an operator takes it once the manual version proves out.

- **Rebalance live instead of once a year.** A scheduled Claude task recomputes potential-per-rep monthly against Salesforce and flags any book that has drifted outside tolerance.
- **Route inbound without a human deciding.** Wire the inbound rule (domain match, then territory) directly into your lead-routing tool so a new lead never sits waiting for someone to claim it.
- **Settle disputes with a paper trail.** Log first-meaningful-activity timestamps automatically in Salesforce, so the tie-breaker rule has real evidence behind it instead of two reps' word against each other.

The carve is fair on day one; the automation is what keeps it fair in month six.


## Make it yours
Fork it. Change the axis, the balance metric, the rules. The point is not to run someone else's territory map. It is to carve yours, balanced on potential and settled before the disputes start. Built by an operator. Customize it, break it, make it better.
