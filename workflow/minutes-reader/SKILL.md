---
name: minutes-reader
description: "Reads minutes written by somebody else — a contractor, a client, a project manager, a consultant — for the thing that matters and gets skipped: what they recorded about you. Minutes become the record if nobody objects within the period the contract or the covering note sets, so an action assigned to you that you did not accept, or a decision recorded that was not made, hardens into fact by silence. Trigger on \"read these minutes\", \"the contractor sent minutes\", \"do we need to correct these\", \"did we agree to that\", \"minutes-reader\", or minutes received from anybody else. Carries no contract terms; the objection period comes from the agreement or the minutes themselves. `meeting-notes-cleaner` turns your own raw notes into actions; this reads somebody else's finished document. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Minutes Reader"
  summary: "Read somebody else's minutes for what they recorded about you"
  discipline: "practice-contracts"
  tags: "Review, Project Management"
---

# Minutes Reader

Minutes written by somebody else are a claim about what happened, and in most
contracts they become the record if nobody objects in time. The person who
writes them is not being dishonest. They are writing what they heard, from
their side, with their actions phrased carefully.

The cost of not reading them is that an action you never accepted becomes yours,
and it takes weeks to find out.

## Scope and limits — read first

**What this does.** Reads minutes received from somebody else against what
actually happened, finds the objection period, and produces the list of
corrections worth making.

**What this does not do.**

- **It carries no contract terms.** Whether minutes become the record, and in
  what period, comes from the agreement or from the minutes' own covering note.
- It does not process your own notes. `meeting-notes-cleaner` does that.
- It does not write the correction. `/draft-email` does, and this is what it
  should be given.
- It does not decide who is right about what was said.
- It does not replace the Architect of Record.

**What you need before starting.** The minutes. Your own note of the meeting, if
there is one, and who attended for you. The agreement's provision on minutes, if
there is one. Previous minutes from the same series.

## Workflow

### Step 1. Find the clock before reading the content

- Who wrote them, and when were they issued?
- **Is there a stated objection period?** In the covering note, in the minutes'
  own header, or in the agreement. Point at `contract-review`.
- If none is stated, is there a series convention: corrections raised at the
  next meeting, or in writing beforehand?
- When is the next meeting?

**A period that has already passed changes what this exercise is for.** Say so
immediately, and say what can still be done: a note on the record at the next
meeting is weaker than a correction in time, and it is not nothing.

### Step 2. Read your own name first

Not front to back. Go through and find every place your practice appears:

| # | Item | What it says about us | Kind |
|---|---|---|---|

`Kind` is one of:

- **Action assigned to us.** With or without a date.
- **Decision attributed to us.** Something we are recorded as having decided or
  agreed.
- **Statement attributed to us.** Something we are recorded as having said.
- **Omission.** Something we said or asked that is not there.

**The omissions are as consequential as the errors** and they are harder to see,
because a missing item does not appear anywhere.

### Step 3. Check each against what happened

| # | Minutes say | What happened | Correction needed? |
|---|---|---|---|

Three kinds of discrepancy, and they are not equal:

- **Wrong.** It did not happen that way.
- **Incomplete.** It happened but the condition, the caveat or the "subject to"
  is missing. This is the most common and the most consequential, because a
  qualified agreement recorded unqualified is an unqualified agreement.
- **Not ours.** An action assigned to us that belongs to somebody else.

Where you have no note of your own, say so. A correction offered against memory
alone is weaker, and knowing that before sending it is worth something.

### Step 4. Read the actions column as a whole

- How many actions are assigned to you compared to everyone else? A
  systematically lopsided list is worth noticing across a series rather than in
  one set.
- Do any carry a date you did not agree?
- Are any carried over from previous minutes and still assigned to you? Point at
  `project-tracker`.
- Is anything assigned to "the design team" without a name, which means you?

### Step 5. Decide what is worth correcting

Not everything is. Sort:

| # | Discrepancy | Correct it | Let it stand | Why |
|---|---|---|---|---|

Correct anything touching scope, cost, time, responsibility, or a decision
attributed to you that was not made. Let stand anything about tone, emphasis, or
a detail with no consequence — a practice that corrects every set of minutes is
a practice nobody reads corrections from.

Report both counts. **Correcting three things gets three things corrected;
correcting thirty gets none.**

### Step 6. Report

- The objection period and whether it has passed, first.
- Everything recorded about you, by kind.
- Discrepancies, split into wrong, incomplete, and not ours.
- Omissions.
- What to correct and what to let stand, with counts.
- Whether you have your own note to correct against.

Then point at `/draft-email` for the correction, and say it should go to
whoever issued the minutes with the meeting reference and the item numbers.

### Step 7. Save

Ask where. Keep the reading with the minutes. Where a correction was sent, keep
that too: the pair is the record.

## Rules

- **Find the objection period before reading the content**, and say if it has
  passed.
- Read for your own name first, not front to back.
- Treat an incomplete record as a discrepancy, not as a detail.
- Look for omissions as well as errors.
- Say plainly when there is no note of your own to correct against.
- Sort into correct and let stand, and report both counts.
- Never argue about what was said. Record the difference.

## Anti-patterns

- Filing minutes unread.
- Reading front to back and stopping halfway.
- Letting an unqualified record of a qualified agreement stand.
- Correcting everything.
- Missing an action assigned to "the design team".
- Objecting after the period without saying that is what it is.
- Accepting an action with a date nobody agreed.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
