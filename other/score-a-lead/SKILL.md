---
name: score-a-lead
description: Scores a lead against the model currently in force and records the inputs that produced the score. Use it when running `ref/mkt/lead-routing`.
license: CC-BY-4.0
metadata:
  agent: lead-scorer
  agent-version: "1"
---

# Score a lead

## What it does

Scores a lead against the model currently in force and records the
inputs that produced the score.

## Where it happens

The agent does this in one activity across one reference process. Each
one names the activity as that process words it.

- **Score**
  - `ref/mkt/lead-routing`, activity 3 -
    [Route Inbound Lead](../../../../processes/marketing/lead-routing.md)

## What to record

Per lead: the merged record with each filled field naming its source,
the score with the model version and the inputs it was computed from,
and the assignment with the reason. Any auditor can replay any decision
from what it left behind.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
