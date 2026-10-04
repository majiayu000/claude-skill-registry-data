---
name: size-a-market
description: Says how many buyers or accounts of a given shape exist and how much money sits with them. Use it when running `ref/mkt/ideal-customer-profile`, `ref/mkt/segment-the-market` and `ref/mkt/size-market-opportunity`.
license: CC-BY-4.0
metadata:
  agent: forecaster
  agent-version: "1"
---

# Size a market

## What it does

Says how many buyers or accounts of a given shape exist and how much
money sits with them. It picks the counting method and says why, sets
the price and frequency assumptions with the source of each one, runs
the count through each method, and explains where the methods disagree.

## Where it happens

The agent does this in seven activities across three reference
processes. Each one names the activity as that process words it.

- **Choose the Sizing Method**
  - `ref/mkt/size-market-opportunity`, activity 3 -
    [Size Market Opportunity](../../../../processes/marketing/size-market-opportunity.md)
- **Compute the Size Each Way**
  - `ref/mkt/size-market-opportunity`, activity 7 -
    [Size Market Opportunity](../../../../processes/marketing/size-market-opportunity.md)
- **Count the Buyers**
  - `ref/mkt/size-market-opportunity`, activity 5 -
    [Size Market Opportunity](../../../../processes/marketing/size-market-opportunity.md)
- **Reconcile the Methods**
  - `ref/mkt/size-market-opportunity`, activity 8 -
    [Size Market Opportunity](../../../../processes/marketing/size-market-opportunity.md)
- **Set the Rate Assumptions**
  - `ref/mkt/size-market-opportunity`, activity 6 -
    [Size Market Opportunity](../../../../processes/marketing/size-market-opportunity.md)
- **Size Each Candidate Market**
  - `ref/mkt/ideal-customer-profile`, activity 10 -
    [Define Ideal Customer Profile](../../../../processes/marketing/ideal-customer-profile.md)
- **Size Each Segment**
  - `ref/mkt/segment-the-market`, activity 9 -
    [Segment the Market](../../../../processes/marketing/segment-the-market.md)

## What to record

Every model at a version, saying which data it was fit on, over what
period, and which records it left out and why. Every prediction with the
model version that produced it and the inputs it was computed from, so
somebody can run it again and see whether the answer still holds. Every
assumption written beside the number it drives, naming where the
assumption came from and how far the number moves when the assumption
moves. A back-test result whenever the agent says a profile would have
picked the right customers, showing what the profile would have selected
and what actually happened to those accounts. A list of every rate it
could not source, marked unsourced, carried into the report.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
