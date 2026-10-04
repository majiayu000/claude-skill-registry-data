---
name: pre-launch-buy-check
description: Reads a buy or a change to a buy as it is configured, before any money is spent, and scores it against the plan line it was placed on and the terms it was bought under. Use it when running `ref/mkt/account-based-play` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: buy-check
  agent-version: "1"
---

# Pre launch buy check

## What it does

Reads a buy or a change to a buy as it is configured, before any money
is spent, and scores it against the plan line it was placed on and the
terms it was bought under. Every failure it reports names the plan line
or the rule behind it.

## Where it happens

The agent does this in three activities across four reference processes.
Each one names the activity as that process words it.

- **Check the Buy Before It Runs**
  - `ref/mkt/account-based-play`, activity 12 -
    [Run Account-Based Play](../../../../processes/marketing/account-based-play.md)
- **Check the Buy Before Switch-On**
  - `ref/mkt/display-retargeting`, activity 12 -
    [Run Display Retargeting Campaign](../../../../processes/marketing/display-retargeting.md)
  - `ref/mkt/traffic-ad-creative`, activity 14 -
    [Traffic Ad Creative](../../../../processes/marketing/traffic-ad-creative.md)
- **Check the Move against the Rules**
  - `ref/mkt/reallocate-media-spend`, activity 7 -
    [Reallocate Media Spend](../../../../processes/marketing/reallocate-media-spend.md)

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
