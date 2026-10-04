---
name: live-ad-check
description: Confirms that what is serving works for the person who sees it, which means the ads render as they should and a click reaches the page it was meant to reach. Use it when running `ref/mkt/traffic-ad-creative`.
license: CC-BY-4.0
metadata:
  agent: buy-check
  agent-version: "1"
---

# Live ad check

## What it does

Confirms that what is serving works for the person who sees it, which
means the ads render as they should and a click reaches the page it was
meant to reach.

## Where it happens

The agent does this in one activity across one reference process. Each
one names the activity as that process words it.

- **Check the Live Ads**
  - `ref/mkt/traffic-ad-creative`, activity 16 -
    [Traffic Ad Creative](../../../../processes/marketing/traffic-ad-creative.md)

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
