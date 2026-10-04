---
name: list-build
description: Runs the rule against the contact database and produces the list itself with its counts, applying the consent rules as it goes, whether what comes out is the people to contact, the pool an advertisement may target, or the list of people who must never be shown it. Use it when running `ref/mkt/account-based-play` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: audience-manager
  agent-version: "1"
---

# List build

## What it does

Runs the rule against the contact database and produces the list itself
with its counts, applying the consent rules as it goes, whether what
comes out is the people to contact, the pool an advertisement may
target, or the list of people who must never be shown it.

## Where it happens

The agent does this in five activities across four reference processes.
Each one names the activity as that process words it.

- **Build the Audience Pools**
  - `ref/mkt/display-retargeting`, activity 7 -
    [Run Display Retargeting Campaign](../../../../processes/marketing/display-retargeting.md)
- **Build the Contact Set**
  - `ref/mkt/account-based-play`, activity 5 -
    [Run Account-Based Play](../../../../processes/marketing/account-based-play.md)
- **Build the Invitation Audience**
  - `ref/mkt/webinar`, activity 7 -
    [Produce Webinar](../../../../processes/marketing/webinar.md)
- **Build the Suppression List**
  - `ref/mkt/display-retargeting`, activity 5 -
    [Run Display Retargeting Campaign](../../../../processes/marketing/display-retargeting.md)
- **Size the Segment**
  - `ref/mkt/target-audience-segment`, activity 6 -
    [Build Target Audience Segment](../../../../processes/marketing/target-audience-segment.md)

## What to record

Each program at a version, naming the entry condition, every step, every
wait, the condition on every branch, and every exit. The hygiene cycle's
scope at a version, saying which records it covers and what it has to
fix in them. The rule that settles which program takes a contact who
qualifies for two, with the date it was decided and who decided it. A
dated account of the database between cycles: how many records there
are, how many are complete enough to use, and how many may be contacted.
The CONVENED and DONE records of everything it convenes. The go record
for a program, naming the version that started sending and who said go.
The standing readout at the cadence the process sets, and the decision
it made after reading it.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
