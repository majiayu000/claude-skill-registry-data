---
name: task-flow-close
kind: pattern
rule: task-flow
description: Pattern of rule task-flow. Load when bringing work to readiness — merging the product agreement into the domain spec, bringing the domain texts up to date with what was done, opening the PR as a draft or ready by its base and leaving draft.
---
<!-- rt-kit v0.34.0 · patterns/task-flow-close.md · 4b1f2d58f71f · правится надстройкой, не здесь -->

# Closing the work

Pattern of the rule `task-flow`. What must be true meanwhile — the law
`docs/constitution/work-conduct.md`.

## When to use

- The stages of the plan are closed.
- `npm run check:specs` listed the agreement in its "time to merge" section.
- The spec is measured for length before the merge and right after it: one already over the limit is
  split by a commit of its own first, one that has grown is split by the same commit.
- The domain texts are up to date, and `product-strategist` reviews the work against its points.
- The gate suite is run whole — after the merge and the texts, not before them.
- The task folder is taken apart, and the PR opens — a draft or ready, by the base.
- The run on the head is green, and the draft is lifted from the PR.

Taking the folder itself apart is not here — that is pattern `task-flow-archive`. It stands between
the suite run and opening the PR: the PR opens behind work already cleaned up.

**The run stands after merging the agreement and bringing the texts up to date, not before them.**
Both steps cost minutes, and the run costs the session window. A session that spent it on the run
hit the fill threshold on four binding lines, and there was nothing left to write them with. The
second argument is stronger than the first — a run that goes after the merge checks the merge
itself; going before it, it looks at a state of the tree that will not reach main.

## State `этапы-кончились`: the agreement merges into the domain spec

By one of the last commits of the branch, before the PR opens. By then the code is written, so the
`file:symbol` bindings are known — the rule enters the domain spec checkable at once.

```bash
npm run check:specs   # the "time to merge" section names the ready directories
```

**The spec is measured for length before the merge, and again in the same turn after it.** Merging
is a known move that grows a spec. One merge took it to 572 lines against a limit of 500, and the
executor learned of it from the push guard's refusal — after the commit. One that has grown is split
into subdomains right here, not on the push.

A spec grows by direct edits too, and a measure taken only after the merge leaves that excess to
every next merge: one domain spec stood at 885 lines and its scenarios at 1293 before any of nine
waiting agreements. So the measure goes first: a spec already over the limit is split by a commit
of its own, and the agreement merges after it. The same holds for a rule or a scenario added to a
spec directly, with no agreement: the room is measured before the edit, not learned from the push
set after the work.

The order of the move:

- the rules from `proposed/<фича>/spec.md` are appended to the domain's `spec.md`, into its
  sections;
- the scenarios move to the domain's `scenarios.md` **with their old numbers**: test titles refer to
  them, and renumbering breaks the audit;
- scenarios whose promise the work rewrote are edited in place: the number stays, the text is new,
  the test title is edited by the same commit. Work that removes a technique rewrites a written
  promise more often than it adds a new one, and a list naming one append does not name this edit at
  all;
- the bindings from `proposed/<фича>/implementation.md` are appended to the domain's
  `implementation.md` and set on the code that now exists;
- the laws the feature declared in its header are appended to the header of the domain spec;
- the `proposed/<фича>/` directory is deleted, and the line about the feature is removed from the
  "proposed, not yet rolled out" section of `docs/specs/README.md`;
- the domain did not exist yet — `proposed/` is replaced by a full spec, and the domain gets a row
  in the table of `docs/specs/README.md`.

The work went in several tasks — the merge goes in the last of them. Which one is last is seen in
the epic plan; a closed epic leaves for the archive or is deleted.

```bash
npm run check:specs   # after the merge: the bindings are in place, no scenario is lost
```

**Next move:** after the merged agreement, in the same turn, come the domain texts — the rules,
patterns and sections the work touched.

## State `этапы-кончились`: the domain texts are brought up to what was done

Only what was written before the code goes into the spec. The other texts — rules, patterns,
application laws — nobody re-reads after the edit, and they go on describing the old tree. The next
reader takes them for true.

What to re-read is taken from the plan section that names what the work touches: the specs, laws and
rules along its footprint stand there. What surfaced along the way is added. The whole constitution
and all the rules need not be read.

| Kind of text | What is done with it |
| --- | --- |
| the domain spec and its subdomains | a new feature gets a rule, a scenario and a binding; what is now included leaves "What is not included" |
| a rule and its `implementation.md` | a new statement with a `file:symbol` binding; a lifted one leaves together with its binding line |
| a pattern | code that diverged from the tree is fixed; a new technique is appended as a section |
| an application law and a general law | **the file is not edited**: the owner gets the text of the article, the work goes on without it |
| the product overview document | a new feature is appended as a line; the line about a lifted one is edited |

What is stale lies most often in four places, and all four are read whole:

- **"What of the law is not here" in a rule.** The spec audit does not read this section, so an
  untruth lives there as long as it likes;
- **"What is not included" in a domain spec.** A task boundary was written there, and the task is
  long closed;
- **"Where it lives" in a rule.** Files move, the paths in the table stay;
- **A statement of a companion about what the tree does not have.** Written before the subject
  exists, it lives on words about emptiness, and nobody rereads it once the subject appears.

```bash
# where the rule and the specs speak of what the work touched
grep -rn -i "<слово работы>" <каталог правил>/*/SKILL.md docs/specs/*/spec.md
# the section nothing audits — read whole by eye
grep -rn -A3 "What of the law is not here" <каталог правил>/<правило>/SKILL.md
# the companions: statements about emptiness and counts, checked by nothing
grep -rn -iE "(нет|ни одного|пока|всего|записей) [0-9]*" <каталог правил>/*/implementation.md
```

**A law is not edited in the branch.** An article of a law is an agreement with the owner, and the
owner changes it. The work diverged from it — the ready-made text of the article is written: into
the progress and into the PR body. The law file is edited after the answer, an application law too.

What was done at this step is written into the PR body: what was re-read, what was changed, and if
nothing was changed — why. The form of the section — pattern `git-workflow-pr-body`. The body fits
the host's length limit — Azure DevOps takes 4000 characters — so the report is one line per text.

**The role `product-strategist` reviews the work while the folder still lies here.** It runs the sign
of each point in the plan and tries to prove the miss. A proved miss is fixed now or named in the PR
body next to the table of points. Before the PR of an epic the same call judges the milestone.

**The role `goal-critic` compares the result with the owner's words in the same state.** It gets the
words verbatim and the result, without the plan or an account of the work. A session calls it before
saying the work is done. Its reply is not reworded: a disagreement goes under it as a session line.

**Next move:** the updated texts are committed, and in the same turn the task folder is taken apart
— by the last commit of the branch, pattern `task-flow-archive`.

## State `папка-разобрана`: the work is handed in by a PR

The folder is taken apart and pushed, the work is cleaned up behind — and the PR opens. Whether it
opens as a draft is decided by the bases the pipeline wakes for: where a run comes, a draft, and it
is lifted on the green; where none comes, the PR opens ready and the push gate is the check behind
it. From this minute the work waits for the owner, not for the machine, and the session does not end
on it: the next task is taken by the same move, pattern `task-flow-resume`.

**Readiness is measured by what is told, not by what has passed.** A check the executor cannot pass
for a reason outside the work — a refused permission, an unreachable environment, a key held by a
person — does not cancel readiness: it goes into "Not run" and into "Remaining step" with the
reason. Silence about it reads as passed.

There is no state on disk any more — the progress left with the folder. This is the price of the
cleanup standing before the PR. The tail — open the PR, wait for the run, lift the draft, ask to
merge, and without a run the first and the last of those — is held by this pattern, not by a line in
a file. The guard counts the work
handed in by the branch history: a folder removed by its commit is the sign.

### The section on the remaining step is written in the PR body, not appended later

It stands there from the minute of opening. Saying it aloud is not enough, and the requirement does
not hold on that alone. A message lives until the next message, and the merge decision is taken on
the PR page — there is no conversation there at all. The owner merges as soon as they see green, and
a PR opened without the section goes into main before the section is appended. That is how a task
folder once went unsorted while the run was going. The section stands last and says exactly one
thing: is anything left before the merge.

```markdown
## Оставшийся шаг

Папка задачи разобрана коммитом `<sha>` — за работой убрано. Осталось дождаться прогона и снять
черновик; до этого кнопка слияния заблокирована хостингом.
```

The draft is lifted — the section is rewritten by the same call that edits the body:

```markdown
## Оставшийся шаг

Не осталось: прогон зелёный, черновик снят. Можно вливать.
```

Where the pipeline does not wake for this base, the PR opens with the section already in this
second form: nothing is left to wait for, and the check standing behind it is the push gate.

```markdown
## Оставшийся шаг

Не осталось: набор проверок перед push зелёный, CI на эту базу не ходит. Можно вливать.
```

The section heading and the words of both samples are written in the language of the PR, not the
language of the pattern. The heading is named by the tree in its profile, `RT_PULL_BODY_SECTION`,
and is taken from there, not from the samples above. What is carried over whole is the order of
thoughts, not the words. The same holds for the messages to the owner below: they are samples of
**what** is said, not of which words.

The section is neither left empty nor removed altogether: a missing section and "no steps left" read
the same and mean different things. The full sample of a PR body — in the pattern for creating a
commit and a PR, if the tree laid it out.

Where the tree laid out the delivery guard, it reads the body straight from the opening command —
passed as an argument or as a file — and refuses the call together with everything else that does
not match. It judges the section by the heading the profile names; unnamed, the section is not
judged at all. Without the guard the section is held only by whoever writes the body.
The work queue audit still does not read the body: the miss is caught at the minute of opening, that
is, where one call still fixes it.

An open PR is re-read by the account that will merge it, not by the one that opened it. The host's
answer to the author says only that the call went through: the right to open and the visibility of
what was opened are different things, and the second is checked only from the reader's side. An
invisible PR gives itself away by nothing — it is in the answer to its author, it carries labels,
and the owner's review queue is simply empty.

The difference between the section and the spoken word is one, and it is all. The owner reads a
message only if they return to the conversation, and the section they see where they look when
pressing the button.

### The messages to the owner, and the run between them

Where the pipeline wakes for this base both are mandatory, and the order between them is one.
Neither replaces the other: the first says the work is handed in and what it waits for, the second
— that it is ready. Where no run comes, there is nothing between them, and they are written as one.

Right after the PR opens:

```
PR #<номер> открыт черновиком, папка задачи уже разобрана — за работой убрано. Жду прогона:
пока он идёт, о работе известно только то, что она запушена. Как закончится — сниму черновик и
попрошу тебя влить. Следующая задача уже взята: #<номер>, ветка <имя ветки>.
```

Где CI на эту базу не просыпается, оба сообщения складываются в одно — его пишут тем же ходом,
каким открыли PR:

```
PR #<номер> открыт и готов к слиянию: набор проверок перед push зелёный, папка задачи разобрана.
CI на PR в ветку эпика у нас не ходит — влей его, пожалуйста. Следующая задача уже взята:
#<номер>, ветка <имя ветки>.
```

The last line names what is taken, not an intent to take, and that is no figure of speech. A sample
that ends with a promise is carried out as a promise: the session says the last line and ends the
turn on it. The message looks complete, and nobody sees the emptiness behind it, neither the owner
nor the session itself. A sample that ends with the number of a created branch cannot be carried out
so: while there is no branch, there is nothing to write the line with. The incident analysis —
`2026-08-16-next-task-said-not-taken.md`.

The run is green, the draft is lifted:

```
PR #<номер> готов к слиянию: прогон зелёный, черновик снят. Влей его, пожалуйста.
```

The draft is lifted before the second message, not after it. The owner, having read the request to
merge, goes to press the button — on a draft it is locked, and the turn comes back to the executor
for nothing.

The run is red — the message is the same in form, but speaks of the red and of what is being done
about it; there is no request to merge in it. The request sounds once and only when the work is
ready whole: said ahead of time, it stops meaning anything, and the owner returns to the old way —
merging by a green page.

Between the two messages the executor does not wait: the work is handed in for review, and the next
task is taken by the same move. They return to the PR by the turn that reads the end of the run.

### An edit after remarks goes without a plan on disk

The review returned remarks, or the run went red — it is fixed in the same branch. The plan is no
longer there, and the folder is not assembled again: the progress guard lets the edit through on the
sign from the branch history. What exactly is fixed is taken from the remark, not from the plan.

A merge left in the working copy is either pushed in the same turn or not made — otherwise the owner
sees the old state and decides by it.

**Next move:** the run is green and there are no remarks — the draft is lifted, and the owner is
told the work is ready. Where no run comes, the same move follows the fix itself.

## State `задачи-эпика-кончились`: the epic is handed in by a request into the main branch

Every task of the epic is merged into its branch and every folder is taken apart — only then does
the epic branch get a request of its own, and its base is the main branch. Until that minute the
branch is not offered to a person at all: the merge button on it means the whole epic, and there is
nothing to press it for while a task is still being written.

Before opening, three things are checked by a command rather than by memory:

```bash
gh pr list --base <ветка эпика> --state open      # no task of the epic is left unmerged
git ls-tree -r --name-only HEAD -- docs/tasks/    # no folder of a task of this epic is left
git fetch origin && git merge origin/main         # the main branch is merged into the epic branch
```

A folder left in the epic branch reaches the main branch with it: what one branch needed becomes the
tree's for good. A foreign folder, arrived with a merge of the main branch, is not touched.

The body is written the same way as a task's, and its "Что сделано" is the list of the tasks by
number: the reviewer opens one page instead of five. The plan of the epic stays in the tree — it
outlives the branch.

**Next move:** the request is open as a draft, the run is awaited, the draft is lifted, and the
owner is asked to merge — by the number, in one turn.

## Common misses

- **The texts are edited before the folder is taken apart:** the list lies in the plan, which the
  taking-apart deletes.
- **A decisions entry repeating a rule's article word for word is no reason next to it.** It leaves
  whole even if the section empties; a reason the article lacks is appended to it.
- **The PR body stays older than the taking-apart.** The taking-apart is the last commit of the
  branch and makes untrue everything the body promised to do before the merge; it is edited in the
  same turn.
- **A rule statement is lifted together with its binding line.** The link goes by text, and either
  half alone reddens the spec audit.
- **The section "What of the law is not here" is read by eye, grep does not help here.** The word
  to search for is not the one expected, and the untruth is not where the theme word leads.
- **"Audited" cannot be said without opening the file.** The rule is read whole: a stale statement
  stands among true ones and differs by nothing.
- **The merge is not done after the merge into main:** main then holds a "proposed, not rolled out" section with what has worked for a month.
- **Scenario numbers are not renumbered at the merge.** The id is the key of the link to the tests.
- **"What is not included" is read whole after the merge, not appended to.** The feature's
  boundaries land next to the domain's, and the line "this section does not exist yet" becomes a lie
  by the very work that merges it. The spec audit does not look there.
- **One's own line of the work queue audit is found by name** — by the task number and the branch
  name: the audit answers for the whole tree.
- **The pair "size label — line in the epic plan" breaks from both sides.** A task on the trail of a
  closed one inherits the label without the line about sessions, and a closed epic takes the line
  away from everyone who carries it.
- **A rule without a binding does not enter the domain spec.** Nothing carries it out, so it is an
  intent, and its place is the domain's open questions.
