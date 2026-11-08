---
name: task-flow-start
kind: pattern
rule: task-flow
description: Pattern of rule task-flow. Load at the start of work from the owner — exploration before the first question, the six mandatory questions, the product agreement, creating the task, the branch and the folder. Returning to work — pattern task-flow-resume.
---
<!-- rt-kit v0.34.0 · patterns/task-flow-start.md · 2eeef8cf00f0 · правится надстройкой, не здесь -->

# Starting the work

Pattern of the rule `task-flow`. What must be true meanwhile — the law
`docs/constitution/work-conduct.md`.

## When to use

- The owner asks for something to be done; the size of the request does not matter — a folder is
  created for any work.
- A defect noticed along the way becomes a task.

## Order

The steps below open one continuous count: a step number is one for the whole course of the work and
does not start over in the next pattern. The whole list is in the rule `task-flow`; it is also shown
to the owner at the start of work, so that after six questions what lies ahead is visible.

### State `просьба-не-разобрана`: exploration — before the first question

A question whose answer lies in the code is not put to the owner: it devalues the rest.

```
Agent(subagent_type: "Explore", prompt: "<тема просьбы>: что по ней уже есть в дереве —
  какие спеки описывают, какие законы и правила задевает, какие либы затронуты,
  есть ли готовый образец рядом. Верни находки, а не пересказ файлов.")
```

The findings go into the grill section "What is already in the tree".

The tree is not the only place where the answer lies. A decision of a past session, written nowhere,
lives only in that session's record: a search over them by the theme's word costs one command. What
is found is written into the tree in the same turn — into the epic plan if it links tasks, into the
progress if it concerns one.

Exploration that found nothing is no permission to ask: the epic plan, the archive and past sessions
are reached first, and the question names where the search went. Exploration ends with command output, not with a feeling: the root memo, `ls` of the directory at
hand, a search over the documentation and the rules.

A member added beside a list, not into it, is named at every reader of that list: each place that
walks the list knows only its members. The readers are found by a search of the list's symbol and go
into the agreement as places to touch; one the search did not return is found after the code.

Exploration over a created task ends with a reproduced symptom, not a found file: the body describes
the tree on the day of creation. Before the first edit the exploration repeats what the task
complains about; a symptom that did not reproduce closes the task as lapsed, and that is lawful.

A tree named as a sample is read as a layout whole — walking the directories two levels deep —
before questions about techniques: one folder generalised into a map leaves out its neighbours.

What was inferred is marked right in the list, together with what confirms it.

Removing an identifier that lives outside the code starts with a search for its value: a client of
the authorization server, a key, an environment variable — over the code, the environment samples
and the composition files. The plan names what uses the identifier now, not what it was created for.

**A ready-made module of the same kind is looked for before the first question** — in this tree and
in the trees recorded as samples of its layout. The one found is read whole: it closes the questions
about the structure — the source of the numbers, the rows, the screen, the storage.

The six questions are asked minus those the exploration answered; the grill gets the line "taking
such-and-such answer, here is where from". The sign is whether the answer is in the tree.

**Next move:** the findings land in the grill, and in the same turn the first of the six questions
goes to the owner. The exploration ended — the state stayed the same, so did the turn.

### State `просьба-не-разобрана`: the grill with the owner

Led by the main agent: a subagent cannot reach the owner. The command is `/grill-me`, one question
at a time, each with its recommended answer and the reason.

All six questions are closed, and those the exploration did not answer are asked:

| Question | Why |
| --- | --- |
| Does the task change the application's behaviour | the product agreement depends on it |
| Does it need an edit of a law or a rule | a law is not edited without the owner's knowledge |
| One task or several | what rolls back apart is split, and split BEFORE the branch |
| What is not part of the task | a boundary not named aloud does not exist |
| What will show that the task is closed | "it works" is no sign |
| Is there a sample the approach is taken from | exploration finds something similar, not the thing itself |

The list of six is the set of what is closed by the start of work, not a set of lines to be said. A
question the owner has already answered is marked closed together with what closed it: the answer is
sought in the documentation and in this session, the original request included. An obvious answer
closes by the line "question closed by assumption: <what is taken>": a wrong assumption costs an
edit, a question about the obvious costs a session.

**Two answers «recommended» in a row close the remaining questions by assumption.** An owner who took
the recommended option twice running has shown that the decisions are not theirs. From the second
such answer the remaining questions go into the grill as decisions — what is taken and where from —
and the owner gets the list in one line, not a menu. The guard of the conversation refuses the third
menu itself; a menu goes out again only for a question no assumption closes, and says so first.

**The streak is counted over the session record, not per task.** After two «recommended» answers at
the end of one task, the next task's questions go into its grill as decisions from the start.

The size of the work is never a ground for a question about boundaries: the owner decided it before
the work began.

The form of a question is set by the owner's settings: where a menu is required, a menu is asked,
and a free option is added to every question — a closed set has no line "wrong question".

**The framing of a handed-over text is not carried onto the current tree.** A handover, a proposals
file and a spec describe the tree they were written in; a statement about the layout is checked by a
command here — the signs of a tree that only installs the package stand on the one that writes it too.

The message with which the executor stops begins with what they wait for:

```
Стою на выборе <что решается>. Без ответа <что будет: пойду допущением таким-то / работа стоит>.
<Вопрос>
```

Under the question goes the table of the epic's position — the same as in the handover; work outside
an epic carries no table. Measurements, role findings and the list of decisions are already in the
progress and are left out of the message: a report with a question at its end drowns the question.

The answers are written into `docs/tasks/_draft-<slug>/grill.md` — the folder is still a draft,
there is no number.

```bash
mkdir -p docs/tasks/_draft-<slug>
cp docs/tasks/_template/grill.md docs/tasks/_draft-<slug>/grill.md
```

An answer chosen from a menu is written with the options it was chosen from: the label alone does
not show whether the owner took a ready option or wrote their own. A task that stands only on a
chosen option says so in its body.

**Next move:** the owner's answer is appended to the grill, and the next question follows. The
answers are over — in the same turn the work goes into the roles pipeline.

### State `разбор-закрыт`: the pipeline after the grill

There will be no more questions — from here on, the roles:

```
Workflow(name: "plan", args: "docs/tasks/_draft-<slug>")
```

Need → the points (`product-strategist`) → the product agreement (`spec-writer`) → its adversarial
review (`spec-critic`) → the plan and the breakdown (`project-manager`) → `goal-critic`. Gaps the
roles could not close return to the owner — the main agent carries them, and the route's misses.

The agreement that came out of the pipeline is checked against `grill.md` line by line before work
by it. The role writes the text without seeing the owner and can turn their answer into its
opposite: the order of stages came out reversed, and included items moved to "not included". A
critic's finding that diverges from the owner's answer is carried to the owner, not carried out in
silence. The same check holds for the executor's own decision on an open question of the agreement:
it is compared with the grill before it goes to the writer — an open question lists the owner's
answer among its variants without a mark, and is decided anew.

The turn does not end on this boundary. A closed grill looks like a finished piece — the answers are
on disk, the file is committed, there is something to report — and the report takes the place of the
agreement. It is written in the same turn, by the roles pipeline or by the executor's hand.

**Next move:** the agreement checked against the grill is committed, and in the same turn the task,
the branch and the folder are created — and if the grill produced a series, the epic is declared
first.

### State `договорённость-записана`: a series of tasks is declared an epic

The grill ended with one task — the step is skipped. Several came out, and the order between them
matters — the epic is declared here, before the first of them, and twice. As a card in the work
queue with the epic label, and as a plan next to it.

```bash
npm run task:new -- --epic --title '<Возможность, которая разрабатывается>' --slug <slug> < тело.md
```

The call puts the epic label on the card, lays a draft of the plan in the tree's directory of plans
and writes the path to it into the body: the audit reads the plan by that path, and a card without
it points into emptiness. Everything the epic cannot be created without is asked before the card is
made — an administrator alone can take a made one off the board. What the call does not write — a
file of epics, an index of plans — the tree lists as hand steps of the same commit as the plan.

The draft is filled in by hand, and three things in it are derived from nothing: the opportunity in
one phrase, the makeup of the tasks in order, and how the branches of the tasks stand. A set without
an order is no order: two tasks whose order rested on understanding went into work the other way
round, and the second was redone under the first. The assigned order holds to the end of the epic; a
revision is the owner's decision.

The cards for all the tasks are created at once, right here — by the same call with `--epic-of`, for
every row of the makeup. The issued numbers return to the same table: "take the next" answers with a
number from now on.

**Next move:** the declared epic is committed together with the task numbers, and in the same turn
its branch is taken.

### State `эпик-заведён`: the branch of the epic

```bash
git checkout -b <КЛЮЧ>-<номер эпика>-<slug> origin/main
```

The branch is taken before the first task of the epic, not with it: taken later, it leaves the first
task standing on the main branch, and the epic starts as half of itself already merged.

The plan of the epic is committed into it and the branch is pushed at once — the branches of the
tasks are taken from it, and one that exists only on the machine is a base nobody else has. The card
names the branch: the reader comes to the epic from the queue, and the queue holds no branches.

Nothing else is committed into the epic branch: it carries the plan and the merges of the tasks; an
edit made in it directly reaches the main branch unreviewed.

**Next move:** the first task of the epic is taken — the branch of the task from the branch of the
epic, and the folder.

### State `договорённость-записана`: the task, the branch, the folder

```bash
npm run task:new -- --epic-of <номер эпика> --title '<Что не так>' --slug <slug> --label area:tooling < тело.md
git checkout -b <КЛЮЧ>-<номер>-<slug> <ветка эпика>
npm run task:move -- <номер> in-progress
```

The body comes as a file and is never empty: an empty task tells nothing to the executor or the
owner, and it can be filled in later only on the owner's word.

The call writes the line about the epic into the body itself and prints the branch line with the
branch of the epic as its base: the shape of that line is read by a machine from both sides, and by
hand it comes out in a shape of its own once out of three. Work outside an epic goes by the same
call with `--outside-epic '<слово владельца>'` — a refusal without that second way out is read as
"there is no way" and gets bypassed by a call to the hosting past this command.

`task:new` renames `_draft-<slug>` to `<КЛЮЧ>-<номер>-<slug>` and fills in the plan header. The
branch is created by a second call: a compound "create and commit at once" is refused by the
main-branch guard whole.

The number is already issued — there is no draft: the folder opens straight under the branch name.
Half of all work starts this way (a past session, a noticed defect, a neighbouring task). The pitfall
"the number never comes first" does not apply: it is about not creating the task before the grill.

The other two files are written, not laid down as templates for later: an empty `plan.md` cannot be
told from a plan without stages, and the next session trusts the task folder. The template is opened
by the same move that fills it, and the layout header is stripped from the copy right there —
otherwise the guard refuses the edit, and the pitfall next to the rule explains why:

```bash
cp docs/tasks/_template/plan.md docs/tasks/<КЛЮЧ>-<номер>-<slug>/plan.md      # and written at once
cp docs/tasks/_template/progress.md docs/tasks/<КЛЮЧ>-<номер>-<slug>/progress.md
```

In the progress the first line declares the state — from this minute the guard reads it:

```markdown
- **State:** `задача-взята`
```

Until a state in which code is edited is declared, the guard refuses the edit and names the
mandatory action of the state that stands in the line.

**Next move:** having declared the state, the same turn takes up the plan starting with its header.
A created folder does not end the turn: not one written file is in it yet.

### State `задача-взята`: the plan header

The guard reads it:

```markdown
**Task:** <КЛЮЧ>-282 · **Branch:** <КЛЮЧ>-282-task-flow
**Draft:** `docs/specs/bookings/proposed/aside-header/`
**Behaviour:** changes
```

A tree with no "proposed" directory names the agreement by the domain spec itself — there it is
written straight into it, and nothing has to move at the closing of the work:

```markdown
**Spec:** `docs/specs/bookings/spec.md`
```

Work that does not touch `apps/**` and `libs/**` needs no agreement:

```markdown
**Behaviour:** unchanged — a move of the layer, invisible from outside. Подтверждено владельцем.
```

An empty reason is not accepted.

The Specs line of the footprint is filled by the command that names the spec of a resource, run on
the files of the Code line, not from memory.

**Next move:** under the header the task footprint and the stages are written, the plan is
committed, and in the same turn the first stage begins.

### State `замысел-записан`: the first stage begins in the same turn

The plan is committed — the work moves into the first stage at once, without giving up the turn. The
state line is rewritten to `этап-идёт`, and from there the work is led by the resume pattern.

```markdown
- **State:** `этап-идёт`
- **Stage:** 1 из 3 — <название первого этапа из замысла>
```

The turn does not end on this boundary. A written plan looks like a finished piece — the file is
committed, there is something to report — and the report takes the place of the work: a session
ended with "next step — such-and-such" at a window fill of about two percent. A turn ends by the
window fill limit, a guard's refusal, a question to the owner or handed-in work with the next
begun; a pattern read to the end is not among them.

**Next move:** the first stage is done in the same turn, and it is declared closed after its command
from the "Checked by" line has passed.

## Common misses

- **The number never comes first.** Until the grill ends it is not even known how many tasks come
  out of it: a task created in advance is closed after the breakdown and stays as litter in the work
  queue.
- **The grill is written to disk at once, not stored up in the conversation.** The session breaks
  off, and a grill lived through in conversation is recovered only by the owner's retelling.
- **One grill produced several tasks — the common part leaves for the epic plan.** The task folder
  dies with the merge, and the task order outlives it; the directory is named by the rule's
  companion.
- **The task is created by a command, not by four calls in a row.** The board is not bound to the
  repository, and the task gets onto it only by an explicit addition.
- **The branch slug is taken from the terminology of the agreement, not from the words of the
  request.** The agreement is written before the branch, and that is exactly where it drops the
  owner's word. The task title and the PR title can be fixed; the branch name after the PR opens —
  no longer.
