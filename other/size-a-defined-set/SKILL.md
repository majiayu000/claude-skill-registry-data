---
name: size-a-defined-set
description: The agent counts a set that somebody has already defined and puts the volume and the money against it, saying which system each figure came from. Use it when running `ref/mkt/analyze-customer-base`, `ref/mkt/target-audience-segment` and `ref/mkt/verify-ad-placement`.
license: CC-BY-4.0
metadata:
  agent: analytics
  agent-version: "1"
---

# Size a defined set

## What it does

The agent counts a set that somebody has already defined and puts the
volume and the money against it, saying which system each figure came
from.

## Where it happens

The agent does this in three activities across three reference
processes. Each one names the activity as that process words it.

- **Size Each Group**
  - `ref/mkt/analyze-customer-base`, activity 12 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
- **Size What It Cost**
  - `ref/mkt/verify-ad-placement`, activity 8 -
    [Verify Ad Placement Quality](../../../../processes/marketing/verify-ad-placement.md)
- **Size the Segment**
  - `ref/mkt/target-audience-segment`, activity 6 -
    [Build Target Audience Segment](../../../../processes/marketing/target-audience-segment.md)

## What to record

Every report with every line attributed to its source, delivered on the
cadence the process sets. A missing source appears in the report as
missing.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
