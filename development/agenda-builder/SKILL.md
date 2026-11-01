---
name: agenda-builder
description: "Builds an agenda for any project meeting from the decisions it has to produce rather than from the topics somebody wants to raise. Establishes who has to be there for each decision and whether they are coming, what has to be sent in advance for a decision to be possible, and what is being discussed with nobody present who can decide it — which is how a meeting produces a follow-up meeting. Trigger on \"agenda for tomorrow\", \"what should we cover in this meeting\", \"build the agenda\", \"prep for the client meeting\", \"agenda-builder\", or a meeting coming up with nothing prepared. Carries no meeting formats and no standard agendas; the items come from what this project actually needs settled. `meeting-notes-cleaner` handles what comes out of the meeting; this handles what goes in. It does not replace the principal or the Architect of Record."
license: MIT
metadata:
  title: "Agenda Builder"
  summary: "Build the agenda around what has to be decided, not what to talk about"
  discipline: "practice-contracts"
  tags: "Project Management, Documentation"
---

# Agenda Builder

An agenda listing topics produces a meeting about those topics. An agenda
listing decisions produces decisions, or it produces the discovery that the
person who can make one is not in the room, which is worth knowing beforehand.

## Scope and limits — read first

**What this does.** Builds the agenda backwards from the decisions the meeting
has to produce. Checks that the decider for each is attending and that whatever
they need has been sent. Names what is being discussed with nobody present who
can settle it.

**What this does not do.**

- **It carries no standard agenda and no format.** Items come from what this
  project needs settled now. A recurring agenda that never changes is a meeting
  nobody prepares for.
- It does not run the meeting or take the notes. `meeting-notes-cleaner` takes
  what comes out.
- It does not track the actions afterwards. `project-tracker` does.
- It does not decide anything.
- It does not replace the principal or the Architect of Record.

**What you need before starting.** What kind of meeting, when, how long, who is
invited. What is open on the project. What was left over from last time.

## Workflow

### Step 1. Establish what the meeting is for and who is coming

Ask, in one message:

> 1. What kind of meeting: client, design team, consultant coordination, site,
>    authority, internal?
> 2. When, how long, and in person or not?
> 3. Who is invited, and **who has authority to decide what?** Point at
>    `stakeholder-map`.
> 4. What was left open at the last one? Point at `meeting-notes-cleaner` and
>    `project-tracker`.
> 5. What is blocking work right now?
> 6. Is anything being sent in advance, and by when?

Question 3 is the one that changes the agenda. A client meeting where the person
who signs is not coming is a different meeting and should be a shorter one.

### Step 2. List the decisions, not the topics

| # | The decision, as a question | Who decides | Attending? | Blocks what |
|---|---|---|---|---|

Write each as a question with an answer somebody can give in the room. "Discuss
the facade" is a topic. "Do we go with the brick or the panel, given the cost
difference" is a decision.

**Where the decider is not attending, mark it and say so up front.** That item
either comes off the agenda or the meeting waits, and finding out in the room
costs everybody the hour.

Order by what is blocking most, not by what is easiest or by what happened
chronologically.

### Step 3. Say what has to be sent in advance for each

A decision is not possible without the thing it rests on:

| # | Decision | Needs to be sent | By whom | By when | Sent? |
|---|---|---|---|---|---|

Drawings, options, a cost, a code answer, a sample, a report. Send it far enough
ahead to be read, and say so; material handed out in the room is material
nobody has read.

**Anything not sent by the deadline comes off the agenda.** Say that in the
agenda itself.

### Step 4. Separate the three other kinds of item

Not everything in a meeting is a decision, and mixing them is what makes
meetings long:

- **For information.** Say it in the agenda in writing instead, and put fifteen
  minutes back.
- **For discussion, no decision yet.** Legitimate, and say what it is building
  toward and when the decision comes.
- **Carried over.** From last time, with why it did not resolve. **An item
  carried over twice is an item with a problem that is not about the item.**

Report the carried-over count. A meeting mostly made of them has a structural
problem, usually that the decider is never there.

### Step 5. Time it honestly, and cut

Put a length against each item and add it up. It will exceed the meeting.

Then cut, deliberately, and say what was cut and why:

- Information items go into the agenda text.
- Items whose decider is absent come off.
- Items whose material was not sent come off.
- Items that are not blocking anything go to next time.

**A meeting agenda that fits is the whole product of this exercise.**

### Step 6. Report and write the agenda

The agenda itself, in the order decided, with:

- Each item as a question, with who decides and how long.
- What was sent in advance and when.
- What is for information, marked, and not scheduled.
- What was cut and why, at the bottom, so nobody thinks it was forgotten.
- Any item whose decider is not attending, flagged at the top.

Then ask where to write it, and point at `meeting-notes-cleaner` for afterwards.

## Rules

- **Every item is a question somebody can answer in the room.**
- Name the decider for each, and flag every one who is not attending.
- Say what has to be sent, by whom, and by when.
- Anything not sent comes off the agenda.
- Put information items in writing, not on the agenda.
- Time every item, add it up, and cut until it fits.
- Report the carried-over count.

## Anti-patterns

- An agenda of topics.
- The same recurring agenda every week.
- Handing out material in the room.
- Scheduling a decision whose decider is not coming.
- An agenda that does not fit in the meeting.
- Fifteen minutes of updates that could have been three lines of text.
- Carrying an item over three times without asking why.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
