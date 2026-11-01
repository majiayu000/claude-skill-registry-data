---
name: thread-reader
description: "Reads a thread of emails or messages and answers the question that starts most disputes: what did we actually agree. Separates what was decided from what was proposed and never answered, tracks who was on the thread at each point since a decision made after somebody dropped off is a decision they never saw, finds the requests that were never replied to, and flags anything that quietly accepted scope, cost or time. Trigger on \"read this thread\", \"what did we agree on this\", \"go through this email chain\", \"did we ever answer this\", \"thread-reader\", or a chain of correspondence handed over. Carries no contract terms; whether something is binding comes from the agreement. `draft-email` writes one message; this reads a chain of them. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Thread Reader"
  summary: "Read an email or message thread for what was actually decided"
  discipline: "practice-contracts"
  tags: "Review, Project Management"
---

# Thread Reader

Every dispute starts with two people remembering the same thread differently.
They are both reading it honestly. Threads branch, people get added and dropped,
a question three messages up is never answered, and the last message reads as
agreement to whichever proposal the reader had in mind.

## Scope and limits — read first

**What this does.** Reads the chain in order and reports what was decided, what
was proposed and never answered, what was asked and never replied to, and who
was present for each. Flags anything that accepted scope, cost or time.

**What this does not do.**

- **It carries no contract terms.** Whether an email binds anybody comes from
  the agreement, and it varies. Point at `contract-review` and
  `construction-attorney`.
- It does not decide who is right.
- It does not write the reply. `/draft-email` does, and this is what it should
  be given.
- It does not resolve a dispute. `dispute-advisor` finds the next required step.
- It does not replace the Architect of Record.

**What you need before starting.** The thread, complete, with headers: who,
when, and who was copied on each message. Anything that happened outside it —
a call, a meeting — that the thread refers to.

## Workflow

### Step 1. Establish the shape of the thread before reading it

- How many messages, over what period? A thread spanning months is several
  conversations sharing a subject line.
- Who is on it, and **does the recipient list change?** Note every point where
  somebody is added or dropped.
- Are there branches: forwards, replies that went to a subset, a separate thread
  that merged in?
- Does it reference anything outside itself: a call, a meeting, an attachment, a
  drawing revision?
- Is the subject line still describing what the thread is about? It usually
  stops being accurate a third of the way down.

**A decision made after somebody dropped off is a decision they never saw**, and
that is the most common source of the "we agreed this" argument.

### Step 2. Walk it in order and log every move

| # | Date | From | To | Kind | What |
|---|---|---|---|---|---|

`Kind` is one of:

- **Proposal.** Somebody suggested something.
- **Question.** Somebody asked something.
- **Answer.** A reply to a specific question.
- **Decision.** Somebody with authority said do it.
- **Acknowledgement.** Received, nothing more.
- **Noise.** Thanks, scheduling, out of office.

Work forward, never backward. Reading a thread from the last message is how the
last message becomes the summary.

### Step 3. Match the questions to the answers

The pass that produces the finding:

| Question | Asked by, when | Answered? | By whom |
|---|---|---|---|

**Report the unanswered count first.** In a long thread it is usually two or
three, and one of them is the reason the thread is still open.

An answer that arrived but addressed a different question is `not answered` and
gets said so.

### Step 4. Separate what was decided from what was assumed

| Item | Decided / Proposed only / Assumed by silence |
|---|---|

- **Decided.** Someone with the authority said so, and it can be quoted.
- **Proposed only.** Suggested, never confirmed. Somebody is probably acting on
  it.
- **Assumed by silence.** Proposed, not objected to, and now being treated as
  agreed. **This is the category that causes disputes** and it is worth naming
  every instance.

For each, quote the sentence it rests on. A decision nobody can quote is a
decision nobody made.

### Step 5. Flag what was given away

Read the thread again looking only for these:

- Any imperative from your side: provide, proceed, go ahead, revise, install.
- Any approval word: approved, accepted, fine, no objection, looks good.
- Anything about cost or time said casually.
- Anything accepting scope without an instrument. Point at
  `/draft-additional-services`.
- Anything that should have been an RFI response, an ASI, or a formal
  instruction rather than an email. Point at `/draft-email`.

Quote each with its date and author.

### Step 6. Report

- Unanswered questions, first, with who asked and when.
- Decided / proposed only / assumed by silence, with a quote against each.
- Everything given away, quoted.
- Every point where the recipient list changed, and what was decided after.
- What the thread references that is not in it, and has to be found.
- What is still open, and who owes the next message.

### Step 7. Save, if asked

Ask whether to write the reading to a file and where. Keep it where the thread
touches scope, money or time.

## Rules

- **Read forward, never from the last message.**
- Track the recipient list at every point and note who dropped off.
- **Report unanswered questions before anything else.**
- Every decision carries a quotable sentence, or it is not a decision.
- Name every item assumed by silence.
- Quote every approval word and every imperative from your own side.
- Never say whether something binds. Name the agreement and the party who reads
  it.

## Anti-patterns

- Summarising from the last message.
- Treating no objection as agreement without naming it as such.
- Missing that somebody was dropped from the thread before the decision.
- Reporting a decision nobody can quote.
- Ignoring a question three messages up because the thread moved on.
- Reading the subject line as the subject.
- Deciding who is right.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
