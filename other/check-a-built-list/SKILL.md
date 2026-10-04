---
name: check-a-built-list
description: The agent reads a sample of a list back against the rule it was built from, and reports how much of it the receiving system could match. Use it when running `ref/mkt/target-audience-segment`.
license: CC-BY-4.0
metadata:
  agent: analytics
  agent-version: "1"
---

# Check a built list

## What it does

The agent reads a sample of a list back against the rule it was built
from, and reports how much of it the receiving system could match.

## Where it happens

The agent does this in two activities across one reference process. Each
one names the activity as that process words it.

- **Check the Built List**
  - `ref/mkt/target-audience-segment`, activity 10 -
    [Build Target Audience Segment](../../../../processes/marketing/target-audience-segment.md)
- **Confirm the Match**
  - `ref/mkt/target-audience-segment`, activity 14 -
    [Build Target Audience Segment](../../../../processes/marketing/target-audience-segment.md)

## What to record

Every report with every line attributed to its source, delivered on the
cadence the process sets. A missing source appears in the report as
missing.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
