---
name: price-the-lines
description: Prices every line against the rate card at the version in force and records that version beside the price. Use it when running `ref/sls/configure-and-price`, `ref/sls/respond-to-an-rfp` and `ref/sls/work-a-churn-risk`.
license: CC-BY-4.0
metadata:
  agent: quote-builder
  agent-version: "1"
---

# Price the lines

## What it does

Prices every line against the rate card at the version in force and
records that version beside the price. Takes out what the customer
already pays for before any discount is discussed, and prices the same
way for a bid and for what a save is allowed to cost.

## Where it happens

The agent does this in four activities across three reference processes.
Each one names the activity as that process words it.

- **Net Off What Is Already Paid**
  - `ref/sls/configure-and-price`, activity 6 -
    [Configure and Price](../../../../processes/sales/configure-and-price.md)
- **Price Against the Rate Card**
  - `ref/sls/configure-and-price`, activity 5 -
    [Configure and Price](../../../../processes/sales/configure-and-price.md)
- **Price What the Save Costs**
  - `ref/sls/work-a-churn-risk`, activity 9 -
    [Work a Churn Risk](../../../../processes/sales/work-a-churn-risk.md)
- **Price the Bid**
  - `ref/sls/respond-to-an-rfp`, activity 9 -
    [Respond to an RFP](../../../../processes/sales/respond-to-an-rfp.md)

## What to record

Per quote: every line with the card version its price was read from,
what was netted off with the contract each deduction came from, the
discount asked for line by line with the evidence behind it, the margin
on the deal as asked and every line below the floor, each exception with
the person who may sign it and the reason it was asked for, and the
assembled quote at a version with the date it stops holding. When a term
is repriced smaller, the new price and its distance from the floor are
recorded beside the old one rather than replacing it.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
