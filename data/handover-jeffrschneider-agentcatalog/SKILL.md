---
name: handover
description: Gives a finished piece of work to every agent and function that has to act on it, and takes back from each one what it is going to change as a result, so nothing settled is left sitting with the agent that made it. Use it when running `ref/mkt/analyze-customer-base` and 7 other reference processes.
license: CC-BY-4.0
metadata:
  agent: audience-manager
  agent-version: "1"
---

# Handover

## What it does

Gives a finished piece of work to every agent and function that has to
act on it, and takes back from each one what it is going to change as a
result, so nothing settled is left sitting with the agent that made it.

## Where it happens

The agent does this in eight activities across eight reference
processes. Each one names the activity as that process words it.

- **Hand over the Findings**
  - `ref/mkt/analyze-customer-base`, activity 17 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
- **Hand over the Map**
  - `ref/mkt/map-buyer-journey`, activity 17 -
    [Map Buyer Journey](../../../../processes/marketing/map-buyer-journey.md)
- **Hand over the Model**
  - `ref/mkt/lead-scoring-model`, activity 14 -
    [Maintain Lead Scoring Model](../../../../processes/marketing/lead-scoring-model.md)
- **Hand over the Persona**
  - `ref/mkt/buyer-persona`, activity 18 -
    [Develop Buyer Persona](../../../../processes/marketing/buyer-persona.md)
- **Hand over the Profile**
  - `ref/mkt/ideal-customer-profile`, activity 15 -
    [Define Ideal Customer Profile](../../../../processes/marketing/ideal-customer-profile.md)
- **Hand over the Segments**
  - `ref/mkt/segment-the-market`, activity 16 -
    [Segment the Market](../../../../processes/marketing/segment-the-market.md)
- **Hand the Strategy to the Work that Follows**
  - `ref/mkt/develop-marketing-strategy`, activity 15 -
    [Develop Marketing Strategy](../../../../processes/marketing/develop-marketing-strategy.md)
- **Tell Every Function What It Has**
  - `ref/mkt/set-marketing-budget`, activity 14 -
    [Set Marketing Budget](../../../../processes/marketing/set-marketing-budget.md)

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
