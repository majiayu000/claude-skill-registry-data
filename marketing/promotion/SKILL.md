---
name: promotion
description: Runs the email, social and paid work that fills a session, an event or a place, pointed at the action the run wants somebody to take, and answers what comes back. Use it when running `ref/mkt/field-event` and 4 other reference processes.
license: CC-BY-4.0
metadata:
  agent: campaign-manager
  agent-version: "1"
---

# Promotion

## What it does

Runs the email, social and paid work that fills a session, an event or a
place, pointed at the action the run wants somebody to take, and answers
what comes back.

## Where it happens

The agent does this in five activities across five reference processes.
Each one names the activity as that process words it.

- **Promote the Conference**
  - `ref/mkt/user-conference`, activity 8 -
    [Host User Conference](../../../../processes/marketing/user-conference.md)
- **Promote the Event**
  - `ref/mkt/field-event`, activity 9 -
    [Host Field Event](../../../../processes/marketing/field-event.md)
- **Promote the Piece**
  - `ref/mkt/long-form-content`, activity 15 -
    [Produce Long-Form Content](../../../../processes/marketing/long-form-content.md)
- **Promote the Presence**
  - `ref/mkt/trade-show`, activity 10 -
    [Exhibit at Trade Show](../../../../processes/marketing/trade-show.md)
- **Promote the Session**
  - `ref/mkt/webinar`, activity 8 -
    [Produce Webinar](../../../../processes/marketing/webinar.md)

## What to record

The run's plan, the CONVENED and DONE records of everything it convenes,
the launch record naming who said go, and the final report against the
brief.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
