---
name: price-a-tier-set
description: "Says what each tier costs the company before anybody is told they hold it: the margin, the discount, the funds and the support hours behind the promise. Use it when running `ref/prt/set-a-partner-tier`."
license: CC-BY-4.0
metadata:
  agent: margin-keeper
  agent-version: "1"
---

# Price a tier set

## What it does

Says what each tier costs the company before anybody is told they hold
it: the margin, the discount, the funds and the support hours behind the
promise. It then sets each tier's discount against the margin floor at
the volume that tier assumes and names the shortfall where there is one.

## Where it happens

The agent does this in two activities across one reference process. Each
one names the activity as that process words it.

- **Check the Margin Holds**
  - `ref/prt/set-a-partner-tier`, activity 8 -
    [Set a Partner Tier](../../../../processes/partners/set-a-partner-tier.md)
- **Price What Each Tier Costs**
  - `ref/prt/set-a-partner-tier`, activity 7 -
    [Set a Partner Tier](../../../../processes/partners/set-a-partner-tier.md)

## What to record

The priced tier table at a version, naming the rules version it was
priced against, the volume each tier assumes, and the margin, discount,
fund and support hours each one carries. The margin test per tier,
naming the floor it was set against and the shortfall where there is
one, with the name of whoever accepted a shortfall in writing. Per
partner, the discount in force and the date it started. Per system
changed, what it was set to and the date it took effect. For a
relationship ending, the settlement line by line: what was earned, what
was paid, what is recovered, and what is still open. For a performance
round, what the company owed each partner set against what was actually
delivered, with each difference settled or marked open.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
