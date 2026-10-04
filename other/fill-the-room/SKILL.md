---
name: fill-the-room
description: The agent decides who is invited and how many have to come, sends the ask, chases and confirms the replies, works the waitlist, and watches the pace against the target week by week. Use it when running `ref/mkt/advisory-board` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: event-manager
  agent-version: "1"
---

# Fill the room

## What it does

The agent decides who is invited and how many have to come, sends the
ask, chases and confirms the replies, works the waitlist, and watches
the pace against the target week by week.

## Where it happens

The agent does this in five activities across four reference processes.
Each one names the activity as that process words it.

- **Build the Invitation List**
  - `ref/mkt/field-event`, activity 5 -
    [Host Field Event](../../../../processes/marketing/field-event.md)
- **Invite the Members**
  - `ref/mkt/advisory-board`, activity 4 -
    [Convene Customer Advisory Board](../../../../processes/marketing/advisory-board.md)
- **Invite the Press and the Analysts**
  - `ref/mkt/user-conference`, activity 11 -
    [Host User Conference](../../../../processes/marketing/user-conference.md)
- **Watch the Registrations**
  - `ref/mkt/user-conference`, activity 9 -
    [Host User Conference](../../../../processes/marketing/user-conference.md)
- **Work the Registration List**
  - `ref/mkt/field-event`, activity 10 -
    [Host Field Event](../../../../processes/marketing/field-event.md)
  - `ref/mkt/webinar`, activity 9 -
    [Produce Webinar](../../../../processes/marketing/webinar.md)

## What to record

The event plan lands at a version and says what the event has to
deliver, what each agent owes, and when each piece is due. The deadline
list lands at a version, and a dated record goes in each time a piece
lands or slips. The agent leaves the CONVENED and DONE records of the
briefing, the roll-calls, the approvals and the debrief. The invitation
and attendance record says who was invited, who registered and who came.
Every call made on the day is recorded with the time it was made and the
reason for it. The report after the event sets what happened beside what
the event was asked to do, and it goes out on its date whether or not
every source answered.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
