---
name: cargo-triage
kind: rule
law: work-conduct
description: A rule under the "Law on work conduct". Take it when the cargo that arrived in the intake is sorted out — incident analyses and proposals from trees. It names what the cargo is read by and when a record gets the marks of a fix and of a release. The pattern is cargo-triage-mark.
---

# Sorting out the arrived cargo — how it is arranged here

A rule under the law `docs/constitution/work-conduct.md`. The law says that work is conducted so
that its state outlives a session; here — how that is held for someone else's work that arrived as
cargo. One's own work goes by the rule `task-flow` under the same law, and one continues the
other: taking a report into work creates a task, and that flow starts from a task.

**Requires:** `.claude/hooks/cargo-mark-guard.sh`

## What it is called here

| In the law                                | Here                                                                             |
| ----------------------------------------- | ---------------------------------------------------------------------------------- |
| work somebody else spoke about            | cargo: an incident analysis and a proposal that arrived in the intake from a tree |
| the state of work that outlived a session | the state of a cargo record: new, in work, done, released                         |
| a mark about what was done                | a call of the mark command — it moves records and writes the fix and the version  |
| what the cargo is taken by                | a call of the read command — it signs in as a service pair and gives the records with their keys |
| the place where the state is read         | the read command's answer; the same is shown to a person by the intake's admin panel |
| the answer to "what it was fixed by"      | the fix: a rule's article, a guard, a check, a code edit                          |
| the answer to "where to look for the fix" | the release version: the string the tree named the release by                     |

## Where it lives

In this tree — the table in `implementation.md` next to it: the intake address, what the mark
command is called and how the states are named in its arguments. Paths live there, not here: the
rule travels between repositories, while the intake address and the command name are each tree's
own.

## Flow

The flow of one cargo record from arrival to release: where every mark is set and what is done
before it.

```mermaid
flowchart TD
    A[A cargo record arrived in the intake] --> B[The read command takes the records: filtered by "new", in arrival order]
    B --> C{There will be work on the record}
    C -->|No| D[The record goes into the quarantine, and the move carries the reason]
    C -->|Yes| E[A task is created, and in the same turn the record moves to "in work"]
    E --> F[The work goes the usual way: a branch, a task folder, a plan]
    F --> G{The edit is merged into the main branch}
    G -->|No| F
    G -->|Yes| H[The record moves to "done", and the fix travels with the move]
    H --> I{The edition with the fix is published}
    I -->|No| I
    I -->|Yes| J[Whoever publishes moves the record to "released" and names the version]
```

## How the law applies here

- **The cargo is taken from the intake by a command, not by eye in the admin panel.** The cargo is
  sorted out by the executor, and what they cannot read they do not sort out: while the reading was
  open to one person, over two hundred records stood as new, and there was nothing to mark them
  with — the mark command knew only what still lay on the tree's disk. The admin panel stays with
  the person and answers a different question: how the cargo looks as a whole.
- **Cargo is not created in the work queue.** A digest speaks of the team's working habits, and in
  an open work queue that is laid out for all to see. The records created by the former order will
  not go anywhere from the queue, but new ones are not created there.
- **Cargo standing in the queue from former times is not judged as a task.** It has no title with a
  number, no assignee and no place on the board, and will have none: the queue audit printed three
  lines per such record — eighteen lines for seven records — and a real discrepancy could not be
  read among them. Cargo is recognised by a label the tree names itself: each has its own, and an
  invented default would match nothing and silently switch the sifting off. What is sifted out the
  audit names by a number — a silent sifting is indistinguishable from an audit whose label is
  named with a typo.
- **Sorting out starts with what is not sorted out.** The list is narrowed by a filter on the state
  "new" and goes in arrival order. Without the filter what is sorted out and what is untouched
  stand mixed together — the very state the states were started to get away from.
- **What is already sorted out is asked of the intake rather than recalled.** The state outlives a
  session, the executor's memory does not: having sorted out the cargo today, tomorrow one starts
  from nothing. It is asked by the same read the cargo is taken by — a second call with a different
  filter, not a query to the storage.
- **A record found disputable goes into the quarantine, and the move carries the reason.** The
  quarantine is a fifth state of the intake: into it a record goes from "new" and returns only
  there, by the word of a person. Left in "new", such a record is taken apart anew every sorting
  out; marked "in work", it lies — no work by it is going. The move without the reason is refused
  row by row: a state with no answer to "what makes it disputable" costs the next sorting out the
  same reading.
- **A record of the quarantine is not taken into work by the executor's own decision.** It is
  returned into "new" by the word of a person, and only after that it becomes work. Taken straight
  from the quarantine, it would skip the very comparison with the agreement it was quarantined by.
- **To take a report into work means to create a task for it.** The mark "in work" without a task
  says somebody took the record and stays silent about where that work goes; a task without the
  mark leaves the record among what is not sorted out, and the next session sorts it out anew.
- **The task and the mark go in one turn.** A deferred mark is not set: between creating the task
  and the next step a day passes, and by that day the executor remembers the task, not the cargo
  record.
- **One edit — one task, however many cargo records called for it.** Records fixed together are
  marked in one batch and by one task: what is split is what would have to be rolled back apart.
- **"Done" is set when the edit is merged into the main branch.** Not when the request is opened
  and not when the run is green: before the merge the edit is not in the tree, and the mark asserts
  that it is.
- **The move to "done" goes by the work state `влито`, not by the executor's memory.** That is the
  only work state where the merge has already happened while the turn about the task is still
  going: the closing stands before the merge, and a mark there would assert what is not in the main
  branch, while after the turn nobody remembers the task. In one sorting out forty-six records hung
  that way — the edits in the main branch, the state as before.
- **The fix travels with the move to "done".** It answers "what by", not "where": a rule's article,
  a guard, a check, a code edit. A link to the task answers "where", and it does not count as a
  fix. Without the text the move is refused line by line — a list would again show a state with no
  answer to "what by".
- **A neighbouring tree's record is closed by the edition's publisher, not by its sender.** The
  sender does not know about the release: the edit enters the package not at their place, and
  nobody owns a neighbour's token — and without a second path foreign records stand in "new" even
  when they have long lain in an edition. That path goes only forward and only over the last two
  steps: "in work" means work taken by a tree, and the tree sets it. A record on closing is named
  by a sign from the read, not by the sender's key: a key is unique in its own tree, not in the
  intake.
- **"Released" is set by whoever publishes the edition, and by the same motion as the
  publication.** They have the version at hand; a release deferred to the next session is marked
  from memory or not marked at all.
- **Between "done" and "released" stands an edition.** A consumer gets the fix only after a layout
  at their place, and the two states are kept apart for exactly that.
- **Both sides of the sorting out go by commands, and they are closed differently.** The reading is
  closed by a service account's sign-in: all the cargo about the resources has to be sorted out,
  and several trees send it. The mark is closed by one's own tree's token: nobody has the right to
  move a neighbour's states, and a leaked token still opens nobody's reading.
- **The service account's pair lies outside the repository.** By the same technique as the tree
  token: laid into the tree, it travels into the history and into every copy of it, and there is
  nothing to revoke it from there with.
- **A key is written down in full and travels into the description of the past together with the
  grill of the request.** The task folder is sorted out before the request is opened, and the mark
  is set after the merge: by that minute the key lives only in the archive. Written down as eight
  characters, it stays that way there — the mark command accepts a full one and answers a short one
  with "the tree has no such record", and restoring it takes matching it against a read of the
  intake.
- **The mark's key is taken from that same read rather than computed from a file on the disk.**
  Computed from one's own disk, it finds only what still lies there: a removed analysis file and a
  rewritten proposal text are never marked, and the record about them hangs as new until somebody
  notices it by eye.
- **The records of a whole sorting out travel in one batch.** The command accepts several records
  per call, and a call per record would cost as much as the sorting out itself.
- **The command's answer is read, not assumed.** It names how many records were moved, how many
  already stood in the named state and which lines were refused. A refused line means the record
  stayed where it was, and it is sorted out by the reason of the refusal, not by repeating the same
  call.
- **The release version is named by one number, without the package name.** The column names the
  version of the same package as the record itself — a name repeated a second time in it adds
  nothing, and the forms of that repetition diverge silently: `rt-agent-kit@0.17.0` and
  `@rt-tools/agent-kit 0.17.0` stood in the intake next to each other and both meant one release.
  The intake cannot refuse this — every tree chooses the version's form for itself, and a shared
  ban would refuse a neighbour's records; the article is held by a sample in the pattern, which is
  where the string is taken from.
- **Sorting out the cargo and gathering the proposals are two different steps.** The gathering
  divides what came in into what repeated and what was one-off and decides what becomes an edit;
  the sorting out marks the state of every record. The gathering is called once every few days over
  a stretch, the sorting out every time work is taken.
- **A proposal is compared with the spec about its resource before it becomes work.** The spec is
  found by the entry command, not by memory: the memory of a session ends with the session, and the
  next sorting out of the same record judges by the complaint text again.
- **The outcomes of the comparison are three, and they are named in advance.** The spec is right —
  the proposal is disputable and does not become work. The spec is wrong — it is corrected, and the
  behaviour after it. The spec is silent — the question goes to the person, and their word says
  which of the other two this becomes. A list written after the fact is assigned by whoever it suits.
- **The move of a proposal into work names the spec it was compared with.** Without it the move says
  "this is taken" and stays silent about what the proposal was judged against: the comparison then
  lives one session. The mark command refuses such a move before the network; an analysis is not
  asked for a spec — there is nothing to compare it with.

## An incident analysis: what is in it and where it lives

An incident is a session in which the executor did the wrong thing, the rules layer did not refuse
it, and the owner paid with a session. No fixable code is left after such a session, and without a
record it ends in an apology in the correspondence: by the next day the mechanism of the miss is
retold smoothed over — the conclusions stay, and a rule is not derived from conclusions.

- **The analysis lives in the intake, and on the tree's disk only until the send.** A draft is
  written as a file into a directory outside the history — a settings key names it — travels away
  by the send command and is removed in the same turn. Two copies of one record diverge silently:
  an edit is read in the intake, while on the disk stays the one written that day, and which of
  them is right is visible from nowhere.
- **The record is made in the same session the incident happened in.** Deferred by a day, it is
  written from a memory of the conclusions rather than of the mechanism.
- **The analysis names the mechanism step by step, not an appraisal of the executor.** What was
  taken for granted, where it came from, what confirmed it — a sequence that can be repeated. From
  the appraisal "was inattentive" no rule is derived.
- **The analysis names what was available before the miss.** The files, the commands and what had
  already been read where the answer lay: from here it is visible whether this is a miss or a lack
  of data.
- **The analysis names what it was caught by.** Which check fired, which stayed silent, which fired
  late.
- **The analysis names what of this went into the rules layer.** A proposal or an edit of a law, a
  rule, a pattern. A record without that line is a complaint, not an analysis.
- **The record's name names the miss, not the task.** `<year>-<month>-<day>-<short name>`: the task
  will close, and the miss will repeat on another. The intake takes that same name as the record's
  key.
- **A defect in the code is not closed by an incident analysis.** It has a spec, and the spec
  explains it.
- **An analysis has no edits after the fact.** A record is edited only if it described what
  happened wrongly; one that travelled into the intake all the more so: there it is already
  somebody else's work.

## What of the law is not here

That the cargo was sorted out is invisible to a machine, and there will be no check for it: the
executor has no sign of "read and decided". The decision "there will be no work on this record"
leaves no trace at all, and a read call without a sorting out is no different from a call after one.

**Handing over work is another matter, and a guard judges it.** It leaves a trace, and a
machine-readable one: the task folder's sample demands that the keys of the cargo records be named
in full in the grill of the request. The cargo mark guard reads them from there and does not let
out a turn that handed over the work on a record while the record's state in the intake is not
moved. One moment is judged, not every turn: a guard asking for a mark on every turn would refuse
the work itself. A dry run does not count as a mark — it leaves no trace outward.

Taking work on the guard does not judge, and that is not a concession: the state "in work" is set
on its own record by the tree it belongs to, and a foreign record is moved only by the publisher's
closing — it accepts "done" and "released", because "in work" speaks of work a tree conducts. The
cargo arrives from neighbours, and demanding a mark for taking a foreign record would be demanding
the impossible. Handing over work has no such fork: both paths lead to "done".

The rest is held by two things, and both are visible in the intake itself. The first is a record
whose edit is merged while the state is as before: it names the skipped step itself as soon as the
list is looked at with a filter. The second is the number of records in "new": a growing one means
the sorting out is not going at all.

A record there will be no work on goes into the quarantine, and nothing checks that it went there:
the decision is the executor's, and a record left in "new" is indistinguishable from one nobody has
reached yet. What the quarantine gives is the state itself and the reason at it — the next sorting
out sees the record taken apart and does not read it a second time.

## Patterns

- `cargo-triage-mark` — the ready-made calls: a dry run, a mark in a batch, the fix and the release
  version, sorting out a refused line.

## Pitfalls

- **A mark deferred "for later" is not set.** Between the decision and the next turn a day passes,
  and by that day only the intake remembers the cargo record. It is marked in the same turn as the
  decision.
- **A dry run does not count as a mark.** It shows what would have travelled and leaves no trace
  outward: the record stays in its former state, and the executor leaves with a feeling of having
  done it.
- **"Done" on an open request is a mark about what is not in the tree.** Between the opening and
  the merge a day and more pass, and a request is also closed without a merge.
- **A fix written as a retelling of the analysis answers the wrong question.** The cargo record
  already carries what was wrong; the mark says what was done about it — and it is read exactly to
  understand whether it is worth fixing at one's own place.
- **The command's answer with zero moved reads as a refusal, not as a success.** The line "moved 0,
  already stood 3" means this sorting out moved nothing: either the records were marked earlier, or
  the keys were named wrongly.
