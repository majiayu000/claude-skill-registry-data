---
name: close-out-a-change
description: Gets the requester to agree that the change is done, and writes the record of what changed, when, and on whose word. Use it when running `ref/mkt/website-content-update`.
license: CC-BY-4.0
metadata:
  agent: web-producer
  agent-version: "1"
---

# Close out a change

## What it does

Gets the requester to agree that the change is done, and writes the
record of what changed, when, and on whose word.

## Where it happens

The agent does this in one activity across one reference process. Each
one names the activity as that process words it.

- **Close out the Change**
  - `ref/mkt/website-content-update`, activity 12 -
    [Update Website Content](../../../../processes/marketing/website-content-update.md)

## What to record

The page at a version, with the preview link that shows it. The publish
record naming the version, the time, and the person who said go. Every
redirect it set, with the address it came from and the address it now
points at. The rollback record when a page comes down, saying what is in
its place.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
