---
name: whiteboard-defense
description: "Use when a person wants to be questioned about a system they shipped, says \"defend <feature>\" or \"whiteboard me on <subsystem>\", or wants to be ready to explain and defend a design to anyone who pulls them aside. Hard questions on the system and on its stack, open-book. Produces a defense report: the gaps, the reading that closes them, and the architecture leads the questions turned up. Not a review of the code, not a test of the person, not a quiz on names and lines, and it changes nothing in the repository."
---

# Whiteboard defense

**The goal is readiness**: anyone can pull the person aside and ask how a system they
shipped works and why it is built that way, and they can answer and defend it. The session
is the study, the questions are its curriculum, the code is the textbook. It ends when the
person says so.

**Open-book.** The person goes and reads before answering: the code, the plan, the board,
the stack's documentation. What is tested is the model they come back with, not recall.
Function names, line numbers and implementation detail are out of scope; where a guarantee
holds and why it holds there is in scope.

## Scope

**One subsystem or feature per session**, named by the person. Before the first question,
read it: its code, its history, and its documents in the data home through the `aiview`
skill. Build the answer key from that reading and keep it out of chat.

**A resuming session reads the previous report first** and does not re-ask what was
defended solid.

## Two tracks

**The system.** In the order a sceptical reviewer pushes:

1. **Shape**: the parts and what each owns.
2. **Flow**: one real request or event start to finish, where state lives, who changes it.
3. **Decisions**: why this and not the obvious alternative, and what was given up.
4. **Failure**: what breaks first under load, bad input or a dependency outage, and how it would be found out.
5. **Change**: where the cut goes if a requirement changed, and what must not be touched.

**The stack.** What the languages, frameworks, runtimes and stores the system rests on
offer at a senior level, used by the system or not: the runtime's concurrency model, the
store's isolation and locking, the framework's lifecycle, the features an experienced
engineer on this stack reaches for. Every stack question is tied to a place in the system
where the answer would matter. When the person answers "we don't use that", the follow-up
is "should you, here?"; the answer either way is learned. Research the stack question from
the official source before asking it, as the `interview` skill researches a claim.

## The questions

- **One question per message**, as the `interview` skill asks its decisions, then the
  follow-ups a sceptic would make: the timeout, the second retry, the concurrent write,
  the deploy halfway through.
- **No question answerable from one file.** Every question tests a connection: two parts of
  the system, or the system and a property of the stack. Name the connection to yourself
  before asking; without one, drop the question.
- **Advanced only.** The level is a staff engineer interviewing for their own team: a
  question the person could fail, that a correct answer needs the stack's semantics for and
  not its API. Never a definition, a module's name restated, a "what does X do", or a
  question whose answer is in the question. If the answer comes back solid at once, the
  next question goes deeper on the same connection until it does not.
- **Check the answer against the reading**, then say what the code says where it differs.
  An answer is marked *solid*, *vague*, *wrong*, or *inherited*: a decision the code holds
  that no person made, which is the first kind to learn, since it will be asked anyway.
- **The mark ends the message; the next question waits.** After a mark the person may
  ask back, contest it, or go and read; the discussion runs until they say "next" or ask
  for the next question. A mark revised in that discussion is revised in the report. The
  next question is never asked in the message that marks.
- **No edits to the repository.** A question is never proved by rewriting the code, and a
  lead is never followed in-session.

## The report

**`YYYY-MM-DD-<subsystem>.defense.report.md` through the `aiview` skill**, kind `report`,
tags = subsystem + defense, written as each answer lands. In this order:

- **Readiness**: per layer of the system track and per stack topic, solid, vague, wrong or
  inherited, with the count of each.
- **Gaps**: each question not defended solid, what the person said, what the code says, and
  the reading that closes it: the files, the document, the stack's source.
- **Inherited decisions**: what the code decided without the person, where, and the
  alternative it silently rejected.
- **Improvement leads**: a stack feature or design the system does not use, the place it
  would apply, the trade-off. Leads, not findings: one that is worth pursuing goes through
  the `brainstorm` or `write-plan` skill like any other change.
- **Log**: every question, the answer as given, the mark.

**Close in chat** with the readiness line and what the next session should start from.
