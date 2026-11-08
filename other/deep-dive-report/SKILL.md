---
name: deep-dive-report
description: Write a financial and operations deep dive for a small business that has shared its real numbers — P&L, revenue by line, staff costs, operating metrics — comparing them against sector benchmarks, naming each gap with inline arithmetic the owner can check on a calculator, and ending in a prioritised action plan sorted by ease x impact. Includes the minimum data to request and the key metrics per sector (restaurant, auto repair, medical billing, fitness, retail, franchise). Use when a client hands over financials and wants to know where the money is, or for a keep / revamp / close decision.
---

# Deep dive report (from the client's own numbers)

The high-touch report: the owner has shared their actual numbers. Every estimate uses *their*
numbers, not conservative public-data floors. That is the whole difference from an outside-in report.

## What to ask the client for

Minimum viable set:
- **P&L**, the last 2-3 years, with as much line detail as they have (revenue, COGS, labour by
  category, rent, marketing, software, other overhead)
- **Revenue**, monthly or annual, ideally by service line or location
- **Staff**: headcount by role, fully-loaded cost per category if available
- **The sector's key operating metrics** (below)

| Sector | Key metrics |
|---|---|
| Restaurant | weekly covers, average check, beverage attach rate, food cost %, labour %, prime cost |
| Auto repair | bay count, daily car count, average repair order, technician efficiency %, labour rate |
| Medical billing | net collection rate, first-pass denial rate, days in A/R, claims per FTE, clearinghouse cost per claim |
| Fitness | monthly members, churn, revenue per member, class fill rate, cost per acquisition |
| Retail | revenue per sq ft, inventory turns, gross margin %, top SKUs |
| Franchise | actual vs the FDD's Item 19, royalty rate, marketing fund %, comp to system average |

## Rules for the draft

- **No benchmark ranges for their dollars.** "$X at your current $Y revenue", not "$X-$Z depending on
  revenue".
- **Name each gap explicitly, with its source**: "Your labour cost is 34.2%. The trade-association
  benchmark for your format is 28-32%. That 2.2-point gap on $Y revenue is $Z a year."
- **Show the arithmetic inline.** The owner should be able to verify every figure with a calculator.
- **Lead with the biggest lever**, not a tour of the business.
- **Use the trade's own metric names** where they're sharper (`trade-vocabulary`), and plain words
  everywhere else (`copy-voice`).
- **Benchmarks are cited**, from a trade association, a published industry study or a government
  series (`federal-labor-data`). Never a number that "sounds right".

## Structure

```
## Executive snapshot
  - the single biggest finding, in their own numbers
  - total upside across findings (a range is fine here, labelled)
  - the one thing to do first
## [Operating sections, by sector]
  - each: benchmark -> their number -> gap -> dollar impact -> specific action
  - competitor context where it's public or they shared it
## Prioritised action plan
  - 5-8 actions; each: what / why / time to implement / $ impact
  - sorted by ease x impact; at least 3 doable in under 2 hours
## Questions for you
  - gaps where their answer changes the call, framed "If X, then A. If Y, then B."
```

**For a strategic decision** (keep / revamp / close a location or line): open with the data you still
need, lay out the options side by side with the same benchmarks, and let the arithmetic carry the
recommendation.

## Deliverable checklist

- [ ] Every dollar figure uses their real revenue, not a benchmark range
- [ ] Each gap is stated with its arithmetic and its benchmark's source
- [ ] The snapshot opens with the highest-impact finding
- [ ] The action plan has 5+ actions with time estimates; 3+ quick wins under 2 hours
- [ ] The PDF renders untruncated (deep dives run long)
- [ ] The client's financials stay private: no copies in shared folders, repos or prompts beyond the job
