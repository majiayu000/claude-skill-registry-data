---
name: close-out
description: Closes a run down at the end, which means taking the advertising off, pulling the final numbers, and closing out the contacts that never answered. Use it when running `ref/mkt/social-campaign` and `ref/mkt/win-back-campaign`.
license: CC-BY-4.0
metadata:
  agent: campaign-manager
  agent-version: "1"
---

# Close out

## What it does

Closes a run down at the end, which means taking the advertising off,
pulling the final numbers, and closing out the contacts that never
answered.

## Where it happens

The agent does this in two activities across two reference processes.
Each one names the activity as that process words it.

- **Retire the Ones Who Stayed Silent**
  - `ref/mkt/win-back-campaign`, activity 18 -
    [Run Win-Back Campaign](../../../../processes/marketing/win-back-campaign.md)
- **Wrap Up**
  - `ref/mkt/social-campaign`, activity 12 -
    [Run Social Media Campaign](../../../../processes/marketing/social-campaign.md)

## What to record

The run's plan, the CONVENED and DONE records of everything it convenes,
the launch record naming who said go, and the final report against the
brief.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
