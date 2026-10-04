---
name: run-intake
description: Takes in what a piece of work has to settle, who it is for and when it is due, and names the standing documents it has to sit inside at the versions in force, so everything built afterwards cites the same versions. Use it when running `ref/mkt/buyer-persona` and 4 other reference processes.
license: CC-BY-4.0
metadata:
  agent: audience-manager
  agent-version: "1"
---

# Run intake

## What it does

Takes in what a piece of work has to settle, who it is for and when it
is due, and names the standing documents it has to sit inside at the
versions in force, so everything built afterwards cites the same
versions.

## Where it happens

The agent does this in six activities across five reference processes.
Each one names the activity as that process words it.

- **Open the Cycle**
  - `ref/mkt/contact-database-hygiene`, activity 1 -
    [Cleanse Contact Database](../../../../processes/marketing/contact-database-hygiene.md)
- **Quote the Account Profile**
  - `ref/mkt/buyer-persona`, activity 2 -
    [Develop Buyer Persona](../../../../processes/marketing/buyer-persona.md)
- **Read the Standards in Force**
  - `ref/mkt/product-positioning`, activity 2 -
    [Develop Product Positioning](../../../../processes/marketing/product-positioning.md)
- **Take in the Segment**
  - `ref/mkt/buyer-persona`, activity 1 -
    [Develop Buyer Persona](../../../../processes/marketing/buyer-persona.md)
- **Take in the Segment and the Goal**
  - `ref/mkt/nurture-sequence`, activity 1 -
    [Build Nurture Sequence](../../../../processes/marketing/nurture-sequence.md)
- **Take in the Targeting Need**
  - `ref/mkt/target-audience-segment`, activity 1 -
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
