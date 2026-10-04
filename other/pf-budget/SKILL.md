---
name: pf-budget
version: 1.0.0
description: Build a personal budget from income and expenses using the 50/30/20 rule or a zero-based plan.
author: matrixx0070
tags: [budget, personal-finance, cash-flow, 50-30-20, zero-based]
capabilities: []
---

## When to use

Use this when the owner wants a clear monthly plan for where their money goes — starting a budget, resetting after lifestyle change, or fixing a "money disappears" feeling. Works for irregular income too (budget from a conservative baseline month).

**Not for:** investment selection, tax filing, debt-strategy sequencing (see pf-debt-payoff), or telling the owner what they *should* value. You structure their choices; you do not moralize spending.

This skill provides education and structure, not individualized financial advice. For decisions with real stakes, recommend a licensed financial planner.

## Method

1. Gather net (take-home) monthly income. Decision point — is income irregular? Use the lowest of the last 3 months as the planning baseline.
2. List fixed expenses (rent, utilities, insurance, minimum debt payments) and variable expenses (food, transport, fun).
3. Decision point — pick a method: **50/30/20** (50% needs, 30% wants, 20% savings/debt) for simplicity, or **zero-based** (every dollar assigned until income minus outflows = 0) for tight control or irregular income.
4. Categorize each expense as need, want, or savings/debt. Sum each bucket.
5. Compare actual buckets to targets. Flag any bucket over target with the gap amount.
6. Decision point — is the plan negative (outflows > income)? Cut from wants first, then renegotiate fixed costs; never zero out savings entirely.
7. Set one automation: move the savings amount out on payday before it can be spent.

## Example

Net income $4,000. 50/30/20 targets: needs $2,000, wants $1,200, savings/debt $800. Actual: needs $2,300 (rent-heavy, +$300 over), wants $1,400 (+$200 over), savings $300 (-$500 short). Fix: trim wants by $200 (dining), redirect to savings → savings $500. Needs stay high; flag rent as >30% of income and revisit at lease renewal.

## Pitfalls

- Budgeting from gross income instead of take-home — you plan money you never receive.
- Forgetting irregular annual costs (insurance, gifts, car registration). Divide them by 12 and reserve monthly.
- Setting wants to $0. Unrealistic budgets get abandoned; leave breathing room.
- Never reviewing. A budget is a monthly loop, not a one-time document.

## Output format

```
PERSONAL BUDGET — [owner] — [month]
Method: [50/30/20 | zero-based]

NET INCOME: $[x]

NEEDS      $[actual] / target $[t]   [OK | OVER +$x]
WANTS      $[actual] / target $[t]   [OK | OVER +$x]
SAVINGS    $[actual] / target $[t]   [OK | SHORT -$x]

ADJUSTMENTS
- [move $x from [cat] to [cat] — reason]

AUTOMATION: transfer $[savings] on payday.
Next: track for one month, then we reconcile actuals.
```

## Reference

Educational rules-of-thumb below — general working knowledge, not individualized advice. Numbers are round anchors, not thresholds anyone must hit.

### The 50/30/20 breakdown

A widely taught starting split of **take-home (net) pay**:

| Bucket | Target | What lives here |
|--------|--------|-----------------|
| **Needs** | 50% | Rent/mortgage, utilities, groceries, insurance, transport to work, minimum debt payments, basic phone/internet |
| **Wants** | 30% | Dining out, streaming, hobbies, travel, upgrades, gifts, subscriptions beyond the basics |
| **Savings/debt** | 20% | Emergency fund, retirement contributions, extra debt paydown above minimums, other goals |

The line between "need" and "want" is judgment: basic groceries are a need, premium delivery is a want; a reliable car is a need, a luxury trim is a want. When needs run above ~50-55%, the usual pressure points are housing (aim to keep rent/mortgage under ~30% of gross where the market allows) and transport.

Alternatives worth knowing: **zero-based budgeting** (assign every dollar a job until income − allocations = 0; strong for irregular income and tight control), **pay-yourself-first** (automate savings off the top, spend the rest freely), and **envelope/category caps** (hard limits per variable category, good for overspending in one area).

### Emergency-fund targets

A cash buffer held **separately** from the checking account, sized to monthly *essential* expenses (needs, not total spending):

| Situation | Common target |
|-----------|---------------|
| Starter buffer (while paying high-interest debt) | $1,000 or 1 month |
| Stable dual income, secure jobs | 3 months |
| Single income or one dependent household | 4-6 months |
| Variable/commission income, self-employed, sole earner | 6-12 months |

Build order most educators suggest: small starter buffer → employer retirement match → high-interest debt → full emergency fund → additional goals. Keep the fund in a liquid, low-risk place (high-yield savings, money market) so a shock never forces high-interest borrowing.

### Common category benchmarks (of gross income)

Rough ceilings used for sanity checks, not rules: housing ≤ ~28-30%, transport ≤ ~10-15%, food ≤ ~10-15%, total debt payments ≤ ~36% (the classic debt-to-income guideline lenders use). Persistently blowing one benchmark is the signal to renegotiate that fixed cost or restructure, not to zero out savings.

### Sinking funds (the "irregular expense" fix)

Annual and lumpy costs wreck monthly budgets when they hit all at once. Convert each to a monthly reserve: `annual cost ÷ 12`. Common ones: insurance premiums, car registration/repairs, holidays and gifts, medical, annual subscriptions, property tax. Setting aside these amounts every month turns a "surprise" $1,200 bill into a planned $100/month.

### Handling irregular income

Budget from a **conservative baseline** (e.g., the lowest of the last 3-6 months). In high months, top up the emergency fund and pre-fund sinking funds rather than inflating lifestyle. A "buffer month" — living on last month's income — smooths the volatility once you can build one month ahead.

### Quick reference: how to read overspending

- Over on **wants** → trim discretionary first; usually the fastest lever.
- Over on **needs** → structural; revisit housing/transport at renewal, not by skipping meals.
- Short on **savings** → automate it *before* discretionary spend clears, don't rely on "whatever's left."
