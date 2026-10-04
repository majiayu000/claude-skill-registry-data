---
name: partner-intake
description: Reads what is already settled about a partner or a program before any work starts, which means who the partner is and what they sell, what each side owes under the agreement, what the program has to deliver and by when, and what the partner was certified on and what has changed since. Use it when running `ref/mkt/channel-program`, `ref/mkt/co-marketing-campaign` and `ref/mkt/enable-channel-partner`.
license: CC-BY-4.0
metadata:
  agent: partner-manager
  agent-version: "1"
---

# Partner intake

## What it does

Reads what is already settled about a partner or a program before any
work starts, which means who the partner is and what they sell, what
each side owes under the agreement, what the program has to deliver and
by when, and what the partner was certified on and what has changed
since.

## Where it happens

The agent does this in four activities across three reference processes.
Each one names the activity as that process words it.

- **Check What the Partner Holds**
  - `ref/mkt/enable-channel-partner`, activity 2 -
    [Enable Channel Partner](../../../../processes/marketing/enable-channel-partner.md)
- **Take in the Partner**
  - `ref/mkt/enable-channel-partner`, activity 1 -
    [Enable Channel Partner](../../../../processes/marketing/enable-channel-partner.md)
- **Take in the Partner Agreement**
  - `ref/mkt/co-marketing-campaign`, activity 1 -
    [Run Co-Marketing Campaign](../../../../processes/marketing/co-marketing-campaign.md)
- **Take in the Program Design**
  - `ref/mkt/channel-program`, activity 1 -
    [Launch Channel Program](../../../../processes/marketing/channel-program.md)

## What to record

The partner record at a version, naming the agreement it rests on, the
tier the partner holds, the date that tier was set and who set it. For
everything the partner was given, the version it was at and the date it
went to them. For every person the partner put through training, what
they were trained on and the date they finished. A dated line for each
obligation as it comes due, saying whether it was met and by whom. What
the partner delivered back, counted against what the agreement asked
for, at the cadence the process sets. The CONVENED and DONE records of
everything it convenes, and the approval record behind every release and
every tier change.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
