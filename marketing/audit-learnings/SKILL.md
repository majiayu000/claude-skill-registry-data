---
name: audit-learnings
description: Files what the audit turned up for the next one, such as which channels and which sellers are worth checking first. Use it when running `ref/mkt/verify-ad-placement`.
license: CC-BY-4.0
metadata:
  agent: buy-check
  agent-version: "1"
---

# Audit learnings

## What it does

Files what the audit turned up for the next one, such as which channels
and which sellers are worth checking first.

## Where it happens

The agent does this in one activity across one reference process. Each
one names the activity as that process words it.

- **Record What Was Learned**
  - `ref/mkt/verify-ad-placement`, activity 15 -
    [Verify Ad Placement Quality](../../../../processes/marketing/verify-ad-placement.md)

## What to record

A verdict per item, each citing the plan line or the rule, its version,
and the campaign configuration it was read against. A pre-launch score
and a post-delivery score, each dated and each naming what it read.
Anything it could not test is recorded as untested rather than left out.
A rescore after a fix names what changed and what it ran again. Where
what ran differs from what was ordered, the difference is recorded
against the plan line it belongs to, with the figures on both sides.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
