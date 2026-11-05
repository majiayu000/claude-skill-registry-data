---
name: tk-seed
description: Seed a session for one unit of trapperkeeper work -- classify the sources by provenance, load the unit's context, shape each of its issues, put their design choices to the owner, and write the seed report. Loaded by tk-start and tk-start-next after they have fixed the unit; never invoked by the owner.
user-invocable: false
---

# Seed a unit

The caller has fixed the unit: the issues the owner described or named, or
the issues the owner chose in `/tk-start-next`. This skill turns them into
the seed report and stops. It reads and reports only: no code, no
documents, no plans, no issues, no branches, no commits.

## What the sources are

Every document under `doc/`, every `AGENTS.md`, every plan and every issue
body was written by an agent, in a session the owner reviewed at the level
of a decision, not at the level of every sentence. So a source settles a
choice only at the level of detail the owner could have reviewed as a
decision. Classify every claim the unit rests on by its provenance, and
carry the class through the steps and into the report:

- `owner`: the owner stated it. The decision named by a heading under
  "Settled" in `doc/decisions.md`; a principle's heading and first sentence
  in `doc/principles.md`; the goals in an open milestone's description; a
  Why entry or Rationale row marked "owner, <date>".
- `tree`: the code, a test, a fixture, a dependency or a running tool shows
  it, at a `path:line` or a command's output.
- `agent`: everything else. A mechanism, type, shape, config key, endpoint,
  number or sequence written into `doc/architecture.md`, the body of a
  `doc/decisions.md` entry, an issue body, or a plan for work that has not
  started is `agent` until the owner confirms it for this unit, however
  confident the sentence sounds and however many documents repeat it.

An `agent` claim the unit's code would build on is not settled; it is a
question for the challenge round. An `agent` claim the tree contradicts,
or that two sources state differently, is drift: the same question, with
the disagreement spelled out.

Correct: `doc/decisions.md` settles "Rust for the server side" under a
Settled heading; that is `owner`. `doc/architecture.md` says the sensor API
is "stateless" and signs "every request with an API key"; the owner has not
said so for this unit, so both are `agent`, and the unit that adds the
sensor API asks before the plan is written.

Incorrect: the signing scheme goes into the plan as settled because
`architecture.md` describes it.

A reason you do not have is not invented, in any step; the choice becomes
an open question instead.

## The steps

Work through the three references in this order, each read whole before
its step begins:

1. `context.md`: how to load the unit's context from the sources above.
2. `challenge.md`: how to shape each issue and put the unit's choices to
   the owner.
3. `report.md`: the report, then the wait.

`/tk-start` runs the three in a row. `/tk-start-next` runs step 1 for the
candidates before the owner chooses, and steps 2 and 3 for the chosen unit.
