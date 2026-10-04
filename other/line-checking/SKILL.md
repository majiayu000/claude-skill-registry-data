---
name: line-checking
description: Sets each billed line against the order it came from and the delivery that was recorded, and works the money out again from the agreed rates, fees, taxes and discounts. Use it when running `ref/mkt/reconcile-media-spend`.
license: CC-BY-4.0
metadata:
  agent: spend-reconciler
  agent-version: "1"
---

# Line checking

## What it does

Sets each billed line against the order it came from and the delivery
that was recorded, and works the money out again from the agreed rates,
fees, taxes and discounts. Every line comes out of this with a verdict
that cites the term it was checked against.

## Where it happens

The agent does this in two activities across one reference process. Each
one names the activity as that process words it.

- **Check the Rates and Fees**
  - `ref/mkt/reconcile-media-spend`, activity 6 -
    [Reconcile Media Spend](../../../../processes/marketing/reconcile-media-spend.md)
- **Match the Invoice Lines**
  - `ref/mkt/reconcile-media-spend`, activity 5 -
    [Reconcile Media Spend](../../../../processes/marketing/reconcile-media-spend.md)

## What to record

The reconciliation for the period at a version, one row per line: what
was ordered, what ran, what was billed, the difference, and the amount
at stake. Against every unmatched line, the question that went to the
issuer, the date it went, the answer that came back, and what that
answer settled. A line still open on the day the period closes is
recorded as open, with its age and its amount. A credit is recorded
against the line it settles, so the next period is checked against a
figure that already accounts for it.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
