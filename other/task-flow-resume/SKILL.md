---
name: task-flow-resume
kind: pattern
rule: task-flow
description: Pattern of rule task-flow. Load when returning to unfinished work in a new session. What is already in the context, what not to ask the owner, how to edit "Where we stand", how to record a decision along the way and a stage revision. Not for starting work — that is pattern task-flow-start.
---
<!-- rt-kit v0.34.0 · patterns/task-flow-resume.md · 74da4459cfe6 · правится надстройкой, не здесь -->

# Returning to unfinished work

Pattern of the rule `task-flow`. What must be true meanwhile — the law
`docs/constitution/work-conduct.md`.

**Requires:** `hooks/task-context-load.sh`

## When to use

- A session is begun on a branch `<КЛЮЧ>-*`, and work in it was already going.
- The work is interrupted — it has to be left so that the next session picks it up without the
  owner.

## What has already come into the context

The hook `task-context-load.sh` gave the plan and the progress whole at session start, and the grill
of the request — by path. They need not be re-read as files; `grill.md` is read when a decision
whose reason is unclear surfaces in the progress.

The warning `РАБОТА БЕЗ ПАПКИ ЗАДАЧИ` came — the work went past the folder. The folder is assembled
from the template, and `progress.md` is filled by what is seen in the tree and in the branch
history, not by questioning the owner.

`РАБОТА ЗАКРЫВАЕТСЯ` came — the branch itself took the folder apart before the PR, and it is not
assembled again: the work state is read at the PR and in the session handover. A code edit after
review remarks became needed — the folder is restored for the time of the edit, and the taking-apart
is repeated by the same commit.

## A stage sign is checked by a run, not by a list made by reading

What is counted by eye diverges from what is there. Reading the check, the executor counted four
exits by skip, and there were five — the fifth lay behind a separate function inside the database
client wrapper and did not get into the list. It was found by a run, and what saved the work was
exactly the plan line that demanded checking every case by a command.

Hence the form of the sign: it names a command and what in its output means "matches" — not a list
gathered by reading. A list is good for knowing where to look; a stage is closed by command output.

## What not to do

- **Do not ask the owner about what is recorded.** That is what all of this is for.
- **Do not start over what is marked done.** The mark stands in the progress; doubt about it is
  checked by the tree — a build, tests, reading the file — not by a question.
- **Do not re-derive the recorded from the code.** The ban on questions does not cover this: a
  decision derived from the code and served as a finding costs more than a spare question. The owner
  is offered to accept anew what they already accepted, and a list of options sounds more convincing
  than a record they do not see. Before deriving, the grill, the progress and the plan are searched.
- **Do not edit the plan.** The result is checked against it; a revision goes as an entry in the
  progress.

## Entry from a session handover

The handover was written by a past session and lies outside the tree. It is read as an assignment —
and the work is taken up past the rule: the state is not checked, the rule is not loaded, the
numbers are taken on trust. The entry from a handover differs from an ordinary session in one thing:
everything written in it is checked against the tree, because it was written yesterday.

The order is short, four steps:

1. **The work-conduct rule and this pattern — as the first move**, before the first line to the
   owner.
2. **The branch and the work state are read in the tree**, not in the handover: `git branch
   --show-current` and the state line in the progress. Diverged from the handover — the tree is
   right.
3. **The numbers from the handover are recounted** on the current commit. The estimate "twice as
   much work" was never confirmed by a recount.
4. **The next step is taken from the progress**, not from the handover's section about it: the
   progress is committed, the handover is not, and they manage to diverge within one session.

What is not in the handover and never will be: the owner's words — they are in the grill; decisions
with reasons — they are in the progress; the plan — it is on disk. The handover retells, it does not
replace.

## Entering the session: the state line is checked against the tree

Check "Where we stand" against the tree. The record describes the day it was made:

```bash
git status --short
git log --oneline origin/main..HEAD
```

Diverged — "Where we stand" is fixed at once, before the work: the next session will trust the
record, not the tree. The state line is fixed together with it: the guard reads it, and left over
from the past session it either refuses a lawful edit or lets through work that has not yet reached
the code edit.

## State `этап-идёт`: the stage is done and marked in the progress

The "Where we stand" section is **rewritten**, not appended — it is the first thing the next session
reads, and the only thing that survives trimming by size:

```markdown
## Where we stand

- **State:** `этап-идёт`
- **Stage:** 3 of 6 — the guard and the startup hook
- **Done:** the law is created, the task folder and the sample are written
- **Next step:** the scenarios of both hooks, then wiring them into the settings
- **Uncommitted:** everything, the branch has no commits yet
- **Waiting for the owner:** nothing
- **PR:** not opened yet
```

The PR line is mandatory from the minute the stages are over: between opening the PR and the merge a
day or more passes, and that is where a session breaks off most often. Without it the next session
reads "the last stage, all green" and learns of the open PR only from the branch history or from the
owner — exactly the retelling all of this was set up to cancel:

```markdown
- **PR:** #1396, ждёт разбора · отвечено 3 замечания из 5 · не сделано: снятие черновика
```

The waiting line carries the owner's standing word about a stop, quoted in « », when they gave
one. The exit guard reads their word from this line, not a retelling; a line without a quote
releases nothing. The quote holds until the owner cancels it, and the line is rewritten then.

```markdown
- **Waiting for the owner:** «эпик чата пока откладываем» — сказано вчера, работа стоит до его слова.
```

With the PR opened the state becomes `работа-отдана`, and its mandatory action is different — the
next task, not waiting for review. By that minute there is nothing left to declare it with on disk:
the progress left with the folder, and the tail of the work is led by pattern `task-flow-close`.

A decision taken along the way — with the reason and with what the alternative was:

```markdown
- **2026-08-07. Гард судит по путям правки, а не по замыслу задачи.** Оценку «меняет ли
  поведение» назначал бы тот, кому она мешает. Альтернатива — строка в замысле — отвергнута.
```

A stage revision — to the same place, not by editing the plan:

```markdown
- **2026-08-07. Этап 4 заменён: роли заводятся обе, а не одна.** Владелец решил при разборе;
  прежний этап в замысле оставлен видимым.
```

A new request of the owner inside the same task goes into the grill, not only into the progress.
The grill leaves for the archive, the progress only when it holds decisions. The request is quoted
verbatim under "The owner request"; under "Decisions" goes the answer, or the line "closed by
assumption: <what is taken>" when the question was not put. Otherwise the archive keeps the first
answer while the code carries the second.

The session entry marks what was done and what confirms it:

```markdown
### 2026-08-07

- 28 сценариев в наборе, `bash .claude/hooks/tests/run.sh` — все наборы зелёные.
- Доэтапное, не этой работы: сверка очереди перечисляет шесть закрытых задач вне борды.
```

**Next move:** the marked stage gives way to the next in the same turn. The stages are over — the
same turn runs the suite, merges the agreement, brings the texts up to date and takes the task
folder apart; the PR opens behind work already cleaned up.

## State `работа-отдана`: the next task is taken by the same move

The task is closed, the PR is open and waits for the owner — the session does not end on it. What is
handed in for review waits for a person, not a machine: while the epic is not over, its next task is
taken at once, by the same move with which the previous one went to review.

Taken, not chosen: the order was assigned at planning and lies in the epic plan. A choice offered to
the owner under an assigned order is a request to assign it anew.

Work outside an epic has no plan with an order, and the next is taken from the work queue — by the
same move and with the same ban on choosing aloud. The queue is asked by a command, not by memory of
what the executor created themselves. An empty queue is a statement about the tree, and it is backed
by command output.

```bash
# what is assigned next — read in the epic plan, not asked
# the state of the tasks — in the work queue: the plan does not know what is closed
```

Only the window fill limit stops the session — then comes the handover, pattern `task-flow-handoff`.
A finished epic is never a reason to stop. Work is taken outside it — from the work queue — and the
owner is told in the same turn that it is the epic that ended, not one of its tasks. It is named
together with the taken work, not instead of it.

**Next move:** an action is done on the next task — a task, a branch or a folder is created. The
turn ends after it, not after words about it.

## Common misses

- **A session that ended in nothing is recorded too.** Otherwise the next one walks the same road:
  "we tried this — it did not work, because" costs one line and saves a whole session.
- **The uncommitted is named outright.** Work lives in the tree for weeks; the line "what lies
  unsaved and why" is the only thing that makes it visible while there is no PR.
- **Confirmation is command output or a measurement, not a retelling.** "Checked, it works" a
  session later cannot be told from "it seemed to work".
- **A number from the handover and from "Where we stand" is recounted before it gets into any new
  text.** Not only before splitting the work. Carried into the grill or the progress, it is read by
  the next sessions as a measurement and checked by nobody else. The handover describes the day it
  was written, lies outside the tree, and no check reads it. A count taken unrecounted diverged from
  the tree by eight and was found by a counting script, not by reading. The estimate "twice as much
  work as the previous" costs the same — on the current commit the volumes were almost equal. A
  recount costs one command, and the text gets its own number.
- **Pre-existing red is kept apart from one's own.** Red found along the way and not made by this
  work is marked as such at once: otherwise the next session takes it for its own breakage.
- **An analysis written by this session does not become a requirement for it.** The record explains
  the mechanism, and it is carried out by the same thing as the previous one — the attention of
  whoever leads the turn. One turn after the record the mechanism repeated in the same form. So an
  analysis ends not with text but with what came out of it: an edit of a resource, a guard or a
  proposal with an address. A session that appended an analysis and returned to work unchanged pays
  for it twice.
- **A findings count written as a word goes stale by the next paragraph.** The count grows by
  sessions, and the word stays put. "Seven" stood over eight listed ones up to the summary itself
  and would have gone further — into the report and into the epic plan. Either a list without a
  number is written, or a number counted in the same turn as the summary.
- **A red suite on a branch that touched not one line of code is asked of the neighbouring sessions
  before one's own edit.** The stand for the runs is one per machine. A neighbouring session that
  raised it for itself drops someone else's suite, and the failure looks like a broken environment.
  Read so, it sends a second session to the same place — to fix what never broke. The order is the
  reverse: first the neighbouring sessions and the busy ports are read, and only then one's own
  edit.
