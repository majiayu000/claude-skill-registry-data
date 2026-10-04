---
name: close-the-run
description: Sets what the run actually landed beside what was asked for, and writes down what to repeat and what to change next cycle. Use it when running `ref/mkt/advisory-board` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: advocacy-manager
  agent-version: "1"
---

# Close the run

## What it does

Sets what the run actually landed beside what was asked for, and writes
down what to repeat and what to change next cycle.

## Where it happens

The agent does this in two activities across four reference processes.
Each one names the activity as that process words it.

- **Record What Was Learned**
  - `ref/mkt/advisory-board`, activity 16 -
    [Convene Customer Advisory Board](../../../../processes/marketing/advisory-board.md)
  - `ref/mkt/customer-case-study`, activity 21 -
    [Produce Customer Case Study](../../../../processes/marketing/customer-case-study.md)
  - `ref/mkt/customer-reference`, activity 15 -
    [Recruit Customer Reference](../../../../processes/marketing/customer-reference.md)
  - `ref/mkt/customer-reviews`, activity 16 -
    [Solicit Customer Reviews](../../../../processes/marketing/customer-reviews.md)
- **Report against the Goal**
  - `ref/mkt/customer-reviews`, activity 15 -
    [Solicit Customer Reviews](../../../../processes/marketing/customer-reviews.md)

## What to record

For each ask, it records the customer, what was asked for, who asked,
the date, and the answer that came back. An agreement records its terms
in the customer's own words: what may be used, in which channels, under
which name and title, and until when, together with the approval the use
rests on. A refusal records the reason the customer gave and the date
they may be asked again. Beside those, it keeps a standing list of which
customers are available for which kind of ask, current as of a date, so
that no run plans around a customer who never agreed to it.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
