---
name: explain
description: List every question still waiting on the user, each explained in plain terms, in a numbered format they can answer inline by quoting it. Use when the user types /explain or asks to see the open questions again.
disable-model-invocation: true
argument-hint: "[optional topic to narrow the list]"
---

# explain

List every question still waiting on the user's answer, each explained in plain
words, laid out so they can copy the reply, type their answer under each item and
send it back.

If arguments were given (`$ARGUMENTS`), list only the open questions about that topic.

## Gather

Collect every open item from this conversation, including what came before any
summary:

- questions you asked that have not been answered, or were only partly answered;
- decisions you are waiting on (approvals, choices between options, "should I…?");
- actions you offered that the user has neither taken up nor turned down;
- blockers that only the user can clear (logins, credentials, access, a ruling).

Leave out anything already answered, dropped, or that you can decide yourself.
Before listing an item as unanswered, check the user's later messages.
If a work-state list or plan file records pending decisions, include those too.

## Write

For each item:

1. **A short title** in plain words.
2. **What it is:** one or two sentences, no jargon. Say what the thing is and
   where it came from, in terms someone who wasn't watching would follow. Name
   files only when that helps them decide.
3. **Why it matters:** what happens, or stays blocked, until they answer.
4. **Options**, if there are any: lettered, with your recommendation first and
   marked *(recommended)*, plus one line on why.
5. **An empty answer line** for them to fill in.

Order the items by urgency: blockers first, then decisions, then offers.

## Format

Use exactly this shape, so a reply that quotes it lines up item by item:

```
### 1. <title>
<What it is.> <Why it matters.>
- a) <option> *(recommended)*: <why>
- b) <option>
> **Answer:**

### 2. <title>
…
```

End with one line telling them they can answer just the numbers they care about,
for example "1: a, 3: skip", and that anything left unanswered stays open.

If nothing is open, say so in one line.

Don't act on any item while you are listing. This command only asks.
