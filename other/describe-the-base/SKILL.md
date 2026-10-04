---
name: describe-the-base
description: "The agent describes the customer base as it stands and as it has changed: how many there are, where the revenue sits and how concentrated it is, who arrived and who left over time, and what has moved since the previous read. Use it when running `ref/mkt/analyze-customer-base`."
license: CC-BY-4.0
metadata:
  agent: analytics
  agent-version: "1"
---

# Describe the base

## What it does

The agent describes the customer base as it stands and as it has
changed: how many there are, where the revenue sits and how concentrated
it is, who arrived and who left over time, and what has moved since the
previous read.

## Where it happens

The agent does this in three activities across one reference process.
Each one names the activity as that process words it.

- **Compare with the Last Read**
  - `ref/mkt/analyze-customer-base`, activity 13 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
- **Describe Who Bought**
  - `ref/mkt/analyze-customer-base`, activity 7 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
- **Read the Base over Time**
  - `ref/mkt/analyze-customer-base`, activity 11 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)

## What to record

Every report with every line attributed to its source, delivered on the
cadence the process sets. A missing source appears in the report as
missing.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
