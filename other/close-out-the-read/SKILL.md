---
name: close-out-the-read
description: The agent records what worked and what to avoid next time, and sets the date the read runs again along with what would bring it forward. Use it when running `ref/mkt/analyze-customer-base` and `ref/mkt/test-ad-creative`.
license: CC-BY-4.0
metadata:
  agent: analytics
  agent-version: "1"
---

# Close out the read

## What it does

The agent records what worked and what to avoid next time, and sets the
date the read runs again along with what would bring it forward.

## Where it happens

The agent does this in two activities across two reference processes.
Each one names the activity as that process words it.

- **Record What Was Learned**
  - `ref/mkt/analyze-customer-base`, activity 19 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
  - `ref/mkt/test-ad-creative`, activity 18 -
    [Test Ad Creative](../../../../processes/marketing/test-ad-creative.md)
- **Set the Next Read**
  - `ref/mkt/analyze-customer-base`, activity 18 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)

## What to record

Every report with every line attributed to its source, delivered on the
cadence the process sets. A missing source appears in the report as
missing.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
