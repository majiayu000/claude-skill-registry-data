---
name: check-a-live-model
description: The agent reads the scores a running model has given against what those records went on to do, and runs a proposed replacement beside the live one on the same traffic so the two can be compared. Use it when running `ref/mkt/lead-scoring-model`.
license: CC-BY-4.0
metadata:
  agent: analytics
  agent-version: "1"
---

# Check a live model

## What it does

The agent reads the scores a running model has given against what those
records went on to do, and runs a proposed replacement beside the live
one on the same traffic so the two can be compared.

## Where it happens

The agent does this in two activities across one reference process. Each
one names the activity as that process words it.

- **Read How the Model Has Scored**
  - `ref/mkt/lead-scoring-model`, activity 2 -
    [Maintain Lead Scoring Model](../../../../processes/marketing/lead-scoring-model.md)
- **Run It Beside the Live Model**
  - `ref/mkt/lead-scoring-model`, activity 12 -
    [Maintain Lead Scoring Model](../../../../processes/marketing/lead-scoring-model.md)

## What to record

Every report with every line attributed to its source, delivered on the
cadence the process sets. A missing source appears in the report as
missing.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
