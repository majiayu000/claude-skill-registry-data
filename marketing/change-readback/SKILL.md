---
name: change-readback
description: Reads the live configuration back after an instruction was given and confirms that what is set now is what was decided, including a later reading that shows the ads have actually gone from the places they were excluded from. Use it when running `ref/mkt/reallocate-media-spend` and `ref/mkt/verify-ad-placement`.
license: CC-BY-4.0
metadata:
  agent: buy-check
  agent-version: "1"
---

# Change readback

## What it does

Reads the live configuration back after an instruction was given and
confirms that what is set now is what was decided, including a later
reading that shows the ads have actually gone from the places they were
excluded from.

## Where it happens

The agent does this in two activities across two reference processes.
Each one names the activity as that process words it.

- **Check the Change Took**
  - `ref/mkt/reallocate-media-spend`, activity 12 -
    [Reallocate Media Spend](../../../../processes/marketing/reallocate-media-spend.md)
- **Confirm the Exclusions Hold**
  - `ref/mkt/verify-ad-placement`, activity 11 -
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
