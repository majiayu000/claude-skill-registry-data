---
name: task-flow-handoff
kind: pattern
rule: turn-conduct
description: Pattern of rule turn-conduct. Load when the session runs into window fill — choosing the stopping point, writing the progress, the shape of the handover and what the owner does with it. Not for returning to work in a new session — that is pattern task-flow-resume.
---
<!-- rt-kit v0.34.0 · patterns/task-flow-handoff.md · f754b3f8ed1e · правится надстройкой, не здесь -->

# Closing a session on window fill

Pattern of the rule `turn-conduct`. What must be true meanwhile — the law
`docs/constitution/work-conduct.md`.

## When to use

- A reminder about window fill has come.
- The work does not fit into the session, and this became visible in advance.
- The session is interrupted for any other reason: the owner leaves, the machine is busy.

## What happens at the thresholds

| Fill | What the guard does | What the session does |
| --- | --- | --- |
| below the first threshold | stays silent | works |
| the first threshold and above | a reminder at every next step of five percent | picks a stopping point and brings the current step to it |
| the second threshold and above | refuses everything but the task folder, the handover and the delivery commands | closes |

The thresholds are watched by the window-fill guard; it takes the window size from the tree's
setting — it cannot be derived from the session record. The room between the thresholds is what the
session closes on: write up the progress, write the handover, commit and open the PR if the work is
finished.

## The stopping point

The logical point is not "where the reminder caught us" but a state from which the next session goes
on without redoing anything:

- a stage of the plan is closed whole, not by half;
- what was done is checked — the run passed, the build built, the measurement taken;
- what was checked is committed: uncommitted work does not survive the break;
- what was begun and dropped is named in the progress outright, with the reason.

An unclosed stage is a lawful point too, if the progress records exactly what of it is done and what
confirms it. There is one unlawful point: an edit about which nothing is recorded.

## The session closes with a handover, and the work state does not change

The cleanup of this step — main, the merged branches and the record of the handover itself — is done
by the `next-session` command: it walks the step whole and names the path to the handover in its
last line. Below is what must come out of it; the order is the same whether it is called by the
command or by hand.

### The progress

The "Where we stand" section is rewritten, the decisions along the way and the session entry are
appended. The form — pattern `task-flow-resume`.

### The commit

What was checked is committed at once, not stored up until the end of the task. The work is finished
— a PR opens: pattern `git-workflow-pr`.

### The handover

It is placed as the section `## Handover of the session` in the task's progress — the same file where "Where
we stand" stands. It is committed and goes into the branch, so the handover survives a move to
another machine: work broken off by window fill is picked up where it goes on. The executor commits
and pushes the section, in the same turn as the rest of the work record.

The section is one: a second compaction rewrites the previous one rather than adding a second — two
truths about one piece of work in one file are worse than one stale truth. The headings inside it go
at the third level, so as not to clash with the sections of the progress itself.

Work without a task folder — a detached head, a branch without a created task — has nowhere to put
the section, and the handover leaves as a file outside the tree; the directory is named by the
profile:

```bash
mkdir -p <каталог передачи>
# the file — <каталог передачи>/<ветка>.md
```

This is a fallback, not a second lawful place: a branch with a task folder gets no such file at all,
and the reading side does not look at it once it has found the section.

**The handover draft is written by a hook, not by hand.** Before context compaction it puts what is
on disk at the same address: the branch, the work state, the next step, what is uncommitted, the
commits above main. Compaction comes even when there is nobody to remind — at night or in the middle
of a long turn — and without the hook the session lost the handover whole at that moment.

**The handover is read by a hook too, not by a person.** At startup it puts it into the context
whole, together with the turn map. Nobody has to paste it by hand — neither after compaction, nor
after a break, nor after clearing. Written and not read, a handover equals an unwritten one: the
next session knows nothing of it and starts from a blank — that is, from what it was written to
prevent.

Hence the requirement on the text: the handover is written for a machine that feeds it in without
sorting, and for a session that reads it as its first line. Addressing the owner in it — "ask them
how the trial ended" — is writing into a void: by the time it is read the owner is not yet in the
conversation.

What the hook writes is the lower bound, not a finished handover. An executor closing the session by
the rule writes over it: they know what is not on disk — how the trial ended, why this path was
chosen, what the owner said along the way. The file is one, the last entry wins.

Inside — ready text for pasting into the new session, without asking the owner for details:

```markdown
Work: <KEY>-<number> "<task name>". Working tree — <full path>, branch
<KEY>-<number>-<slug> (created, in progress).
PR: #<number>, open, waiting for the owner's review. The freshness of its base is left out on
purpose — it goes stale; the new session asks the hosting about it first thing.

The progress and the plan arrive at session start through the hook — no need to re-read them
as files. The grill of the owner's request lies in the task folder and is read when the reason
for a decision is unclear.

Done: stages 1–3 of the plan are closed and committed.
Next step: stage 4 — <what exactly>.

What to keep in mind in this session:

- the rules review of <KEY>-<number> was started in the background and has not returned —
  write the findings to `<plan name>-findings.md` next to the epic plan;
- the stands are already up, raised by the owner; do not raise your own;
- the dependencies of this tree lag behind the main branch — when the build fails on a
  foreign error, install dependencies first;
- <anything else that is neither in the rules nor in the progress>.
```

The third section is "Epic" — the position table. Work outside an epic does not carry this section:
a table of one row repeats the "Work" section and reads as an epic of one task.

```markdown
### Epic <number> — <the capability named by the plan>

| #   | Task                              | State       |
| --- | --------------------------------- | ----------- |
| 1   | <KEY>-<number> — <what it does>   | closed      |
| 2   | **<KEY>-<number> — <what it does>** | in progress |
| 3   | <KEY>-<number> — <what it does>   | ahead       |
```

Three columns, a row per task. The heading names the epic number and the capability — the one
written in the plan, not retold anew. `#` is the place in order: the actual one for closed tasks,
the one assigned by the plan for future ones. `Task` — the number and what it does, in the same
words as the plan. `State` — "closed", "in progress" or "ahead"; the row of the current task is
highlighted whole.

The set is taken from the epic plan, and the state from the work queue: the plan does not know what
is closed, and the queue does not know the order. A task added to the epic after planning stands in
the queue and in the table, but not in the plan — the discrepancy is named aloud, not smoothed over.

The sections are fixed, and their order is the same:

1. **Work** — the task number, its name, the working tree by full path, the branch and its state;
   for handed-in work — the number of the open PR and what it waits for.
2. **Where to look** — what comes by the hook itself, and what is read as needed.
3. **Epic** — the position table; work outside an epic has no such section.
4. **Done and the next step** — one line each; the details are already in the progress.
5. **What to keep in mind** — the particulars of this session that are neither in the rules nor in
   the progress. Raised stands, lagging dependencies, other people's processes on ports, open
   questions to the owner, a review launched in the background and not returned.

**A review launched in the background and not returned by the session's end is named by a line in
"What to keep in mind".** The role answers into the conversation, gone by the next session. An
answer that came after closing is read by nobody, and the findings are lost whole, together with
what the review was launched for. There is no trace on disk either — the findings file is written by
the executor from the answer, and there was no answer yet. The line names the task the review runs
on and the file to write the returned findings to: without the second, the next session knows it
waits for something and does not know where to put it. The review gets no section of its own — in a
session that did not launch one, the section would stand empty.

### The path to the owner

The last action of the session is to name to the owner the path to the handover, so they can put the
text into a new session with one paste. Retelling the content of the handover in the reply is not
needed: the owner will read it anyway, and the room for it is already spent.

## Common misses

- **The session closes at the second threshold instead of starting a new stage on it.** The reminder
  at the first one is already the signal to pick a point, not to work on until refused.
- **The handover is written as a retelling of the conversation.** What goes into it is what is
  neither in the progress nor in the rules: the tree, the branch, the state of the stands.
  Everything else the next session reads by itself.
- **A statement about the state of the work is taken in the same turn, not recalled.** The task's
  parent, its column, the open PR, the merged branch, the raised stands live outside the session and
  change without it. The handover is read first and not disputed: the session carries out its
  instruction rather than checking it. Plausibility is no confirmation — "the branch is not merged,
  so there is no parent either" is an inference, not a measurement. Nothing to ask with — then it is
  written as a question: "the parent is not checked, check before the PR".
- **The work state does not move into the handover.** Done work is marked in the progress — by one
  entry; the handover retells it but does not replace it and is not committed into the tree.
- **The handover records a state that lives for hours.** Lag behind main, the course of the run and
  "checks green" the new session reads as true today. What goes into the handover is what does not
  change without the executor: the tree, the branch, the PR number, what is not committed.
- **The uncommitted is not named.** Work lives in the tree for weeks, and the line "what lies
  unsaved and why" is the only thing that makes it visible.
- **A session that ended in nothing writes a handover too.** "We tried this — it did not work,
  because" is its result; without the record the next session repeats the same path.
