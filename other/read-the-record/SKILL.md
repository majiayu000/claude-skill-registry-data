---
name: read-the-record
description: "Reads the organization's own record of its customers and says what is in it: who bought, who stayed, who left, when each one arrived, and what each one pays today. Use it when running `ref/mkt/analyze-customer-base` and 3 other reference processes."
license: CC-BY-4.0
metadata:
  agent: forecaster
  agent-version: "1"
---

# Read the record

## What it does

Reads the organization's own record of its customers and says what is in
it: who bought, who stayed, who left, when each one arrived, and what
each one pays today.

## Where it happens

The agent does this in three activities across four reference processes.
Each one names the activity as that process words it.

- **Read the Affected Customers**
  - `ref/mkt/pricing-change`, activity 2 -
    [Launch Pricing Change](../../../../processes/marketing/pricing-change.md)
- **Read the Base over Time**
  - `ref/mkt/analyze-customer-base`, activity 11 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
- **Read the Customer Record**
  - `ref/mkt/ideal-customer-profile`, activity 2 -
    [Define Ideal Customer Profile](../../../../processes/marketing/ideal-customer-profile.md)
  - `ref/mkt/segment-the-market`, activity 3 -
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
