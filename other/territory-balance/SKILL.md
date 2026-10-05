---
name: territory-balance
description: 'Carves accounts into sales territories that are fair on opportunity, not just account count, and flags coverage gaps and overloaded reps before the quarter starts. Use when: territory planning, territory design, carve territories, rebalance accounts, sales capacity planning, quota fairness, coverage model, account assignment.'
---

# Territory Balance (EVEN Framework)

Territories split by alphabet, zip code, or headcount look fair on a slide but drift out of balance within weeks. Territory Balance scores every account for near-term potential, then assigns accounts so each rep carries a comparable share of opportunity and a workload they can actually cover.

## Core Principle

**Balance opportunity and effort, not account count.** Ten enterprise logos and ten small businesses are not the same book.

## The EVEN Framework

| Letter | Step | The Question |
|---|---|---|
| **E** | Estimate | What is each account worth in the next 12 months? (whitespace × propensity) |
| **V** | Visit load | How many touches does each account need at its tier? |
| **E** | Equalize | Which assignment keeps every rep within ±10% of the mean potential and capacity? |
| **N** | Nudge | Which exceptions (existing relationships, language, time zone) justify breaking balance? |

**Account potential** = whitespace ($) × propensity (0-1), where propensity blends fit, intent, and engagement.

**Rep load** = Σ(touches per account per month) ÷ rep capacity (touches per month). Target 0.75-0.9.

## Process

1. **Score accounts** - compute potential; tier into A (top 20% of potential), B (next 30%), C (rest)
2. **Set touch norms** - e.g. A = 8/month, B = 3/month, C = 1/month (pooled or digital-led)
3. **Assign greedily** - hand out accounts in descending potential to the rep with the lowest current potential who still has capacity
4. **Apply exceptions** - keep existing relationships where the account is mid-cycle; log every exception
5. **Check balance** - report each rep's potential share and load; iterate until all fall in band
6. **Publish** - territory list, balance table, and exception log

## Output

Save to `outputs/territory-balance-[period]-[YYYY-MM-DD].md`

| Artifact | Description |
|---|---|
| **Assignment table** | Account, tier, potential, owner |
| **Balance table** | Rep, total potential, share vs mean, load |
| **Exception log** | Every manual override with its reason |

## Tips

1. **Publish the math** - reps accept territories they can audit
2. **Cap exceptions** - more than 10% of accounts overridden means the model is wrong
3. **Revisit mid-year** - propensity drifts; rebalance C-tier freely, A-tier rarely

## Pairs With

- **abm-playbook** - A-tier accounts become ABM target lists
- **signal-radar** - intent signals feed propensity
- **revenue-forecasting** - consumes territory potential as a capacity input
