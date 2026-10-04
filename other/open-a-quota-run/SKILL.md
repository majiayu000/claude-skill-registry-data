---
name: open-a-quota-run
description: Takes the map and its carrying numbers with the target the set has to reach, and gets the over-assignment fixed as a figure by a named person before any number is drafted. Use it when running `ref/rev/model-the-territories` and `ref/rev/set-the-quotas`.
license: CC-BY-4.0
metadata:
  agent: quota-setter
  agent-version: "1"
---

# Open a quota run

## What it does

Takes the map and its carrying numbers with the target the set has to
reach, and gets the over-assignment fixed as a figure by a named person
before any number is drafted. A total nobody signed is not one.

## Where it happens

The agent does this in three activities across two reference processes.
Each one names the activity as that process words it.

- **Hand the Map to Quota Setting**
  - `ref/rev/model-the-territories`, activity 15 -
    [Model the Territories](../../../../processes/revenue-operations/model-the-territories.md)
- **Set the Over-Assignment**
  - `ref/rev/set-the-quotas`, activity 2 -
    [Set the Quotas](../../../../processes/revenue-operations/set-the-quotas.md)
- **Take in the Map and the Number**
  - `ref/rev/set-the-quotas`, activity 1 -
    [Set the Quotas](../../../../processes/revenue-operations/set-the-quotas.md)

## What to record

Per run: the over-assignment as a figure with who decided it and why, a
draft on every patch naming the carrying figure and the curve behind it,
and the capacity test and the history test attached to each number.
Every number further from history than the stated distance carries the
reason for the difference beside it. The roll-up states the sum, the
target and the distance between them as an amount, and any adjustment
records what moved, on which patch, and by how much. Ramped numbers name
the written rule that produced them and the dates they cover. The signed
set names the person who signed it and the hour, and a quota changed
afterwards is a new version saying what moved and who decided it, with
the version it replaces left where it was.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
