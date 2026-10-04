---
name: call-the-phase
description: "States which pattern the conversation is working in now: opens the session in its declared pattern, and moves it to the next phase when this one is done, with a reason attached. Use it when running `ref/gm/run-a-working-session`."
license: CC-BY-4.0
metadata:
  agent: facilitator
  agent-version: "1"
---

# Call the phase

## What it does

States which pattern the conversation is working in now: opens the
session in its declared pattern, and moves it to the next phase when
this one is done, with a reason attached. Every call is a signed message
in the record, and every call is advisory.

## Where it happens

The agent does this in two activities across one reference process. Each
one names the activity as that process words it.

- **Open the Session**
  - `ref/gm/run-a-working-session`, activity 5 -
    [Run a Working Session](../../../../processes/general-management/run-a-working-session.md)
- **Work the Agenda**
  - `ref/gm/run-a-working-session`, activity 6 -
    [Run a Working Session](../../../../processes/general-management/run-a-working-session.md)

## What to record

Its phase calls, plan statements, turn namings and departure notes, each
a signed message in the conversation's own record. It keeps no second
copy and produces no minutes document, because the record already holds
everything it did, signed, ordered and attributable - a separate minutes
document would be a weaker copy of the books.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
