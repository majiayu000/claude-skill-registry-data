---
name: delivery-monitoring
description: Reads what has been delivered so far against the settings the buy was switched on with, such as how often one person has been shown an ad against the cap that was set, and whether the split still holds and every variant is still running. Use it when running `ref/mkt/display-retargeting` and `ref/mkt/test-ad-creative`.
license: CC-BY-4.0
metadata:
  agent: buy-check
  agent-version: "1"
---

# Delivery monitoring

## What it does

Reads what has been delivered so far against the settings the buy was
switched on with, such as how often one person has been shown an ad
against the cap that was set, and whether the split still holds and
every variant is still running.

## Where it happens

The agent does this in two activities across two reference processes.
Each one names the activity as that process words it.

- **Check the Caps Are Holding**
  - `ref/mkt/display-retargeting`, activity 14 -
    [Run Display Retargeting Campaign](../../../../processes/marketing/display-retargeting.md)
- **Watch Delivery**
  - `ref/mkt/test-ad-creative`, activity 14 -
    [Test Ad Creative](../../../../processes/marketing/test-ad-creative.md)

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
