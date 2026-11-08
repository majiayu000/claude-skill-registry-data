---
name: git-workflow-pr-body
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load when the PR body is written or edited — the Closes line and how the task closes when the base is not the main branch, reviewer, assignee and labels by the opening call, the four sections of the body. Opening the PR itself — pattern git-workflow-pr.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-pr-body.github.md · 7139273899d8 · правится надстройкой, не здесь -->

# The PR body and the link to the task

Pattern of the rule `git-workflow`. What must be true — the law
`docs/constitution/delivery.md`. Opening the PR, the draft and its state — pattern
`git-workflow-pr`; a chain of branches — `git-workflow-stack`.

## When to use

- The body of a PR is written or rewritten — at the opening, after a merge into the branch, in
  the turn that lifts the draft.
- The base of the PR is an epic branch or the previous branch of a chain, and it has to be said
  how the task closes.
- Reviewer, assignee and labels are set on an already open PR.

## The PR is attached to the task

The body starts with the link line — by it the board fills the linked PRs field, and by it the task
closes on the merge. The number in it is the branch's, copied rather than recalled; a tree that
named the sample of the line in its profile, `RT_PULL_CLOSES_LINE`, gets the opening refused by the
delivery guard without it. Reviewer,
assignee and labels are set by the same command, and a PR does not open without them:

```bash
GH_TOKEN="$TOKEN" gh pr create --title '[<КЛЮЧ>-86] Письмо владельцу с незаполненным адресом попадает в логи' \
    --base <ветка эпика> --body-file <файл с телом> \
    --reviewer <владелец> --assignee <бот> --label bug --label area:api
```

**The title stands first in the call, and the body comes in by a file.** The delivery guard reads
the title out of the command text and takes the first match of the short key: a body passed as a
line in the same call may itself hold a word after that key — a quoted command, a label, a run
line — and it becomes the title in the guard's eyes. The refusal then says the title does not
start with the task number while the real title is right, and the mistake is looked for where
there is none. A body in a file leaves the call one title and nothing else to match.

The reviewer is always the owner: without a review request the PR does not show in their queue.
The assignee is the same account the machine work goes from. Labels are taken from the task
whole — both the kind of edit and all its areas; they are read from the task, not picked from
memory:

```bash
/opt/homebrew/bin/gh issue view 86 --json labels --jq '.labels | map(.name) | join(",")'
```

The line `Closes #<номер>` is mandatory: without it the PR is not attached to the task, and the
queue audit finds this. It also means the task closes whole — half a task is not rolled out by
one PR: work that does not fit one branch is split into tasks before the branch is created.

**The host reads the line only on a merge into the default branch.** A PR into an epic branch or
into the previous branch of a chain merges, and its task stays open: two chain PRs promised a
closing this way, and the board column lagged the work until a person noticed. So the body of a
PR with such a base says how the task closes, and the tree decides which of the two it is:

- the tree closes such tasks by a pipeline of its own on the merge of a PR — the `Closes` line
  stays, and the body names the pipeline; where it is named for this tree is said by the
  override next to this pattern;
- the tree has no such pipeline — the body names the task in words, «Задача #86 закрывается
  рукой после слияния череды», and the cleanup step after the merge closes it with a comment
  naming the PR: pattern `git-workflow-stack`.

The queue audit reads the `Closes` line as the link between the PR and the task on every base;
a PR without it is named a divergence whichever way the task closes.

A refusal about an exceeded query-language quota (`API rate limit already exceeded`) creates no
PR at all; the opening then goes by a REST call — `$GH api -X POST "repos/$REPO/pulls" -f head=… -f
base=… -f title=… -F body=@<файл>` — and labels and reviewer are set after it. The text of such
a refusal reads as temporary, but the account's quota is not exhausted — it equals zero: there
is nothing to wait for.

On an already open PR the same is set by three REST calls. `gh pr edit` will not do here: it
queries Projects (classic) cards, gets a refusal about a removed API and never reaches the edit.

```bash
GH=/opt/homebrew/bin/gh
REPO=<владелец>/<репозиторий>

$GH api -X POST "repos/$REPO/issues/205/labels" -f 'labels[]=bug' -f 'labels[]=area:api'
$GH api -X POST "repos/$REPO/issues/205/assignees" -f 'assignees[]=<бот>'
$GH api -X POST "repos/$REPO/pulls/205/requested_reviewers" -f 'reviewers[]=<владелец>'
```

The same call edits the body itself: `-f body=` rewrites it whole, so the line
`Closes #<номер>` is written anew together with the rest of the text.

```bash
$GH api -X PATCH "repos/$REPO/pulls/205" -f body="$(cat тело.md)"
```

The body is reread whenever something merged into the branch after publishing: the PR states
things about the tree, and the tree has changed since.

## PR body sample

Six sections, and one order between them: the link line, what was done, the points, the goal, what
confirms it, the remaining step. A section with nothing to say says so in words — an empty heading
and a removed heading read alike and mean different things.

The table of points comes from the reply of the role `product-strategist`: a sign not run is
written as not run, and its point as not reached. The table of the goal comes from the reply of the
role `goal-critic`. Both go in word for word, and the critic reads the finished body against the
replies.

```markdown
Closes #86

## Что сделано

- <правка, названная тем, что она меняет для читателя, а не тем, какие файлы задела>

## Точки

| Точка | Признак | Результат |
| --- | --- | --- |
| <изменение, которое увидит человек> | <команда, страница или число> | <вывод признака: достигнута или промах> |

## Цель

| Слова владельца | Что показывает результат | Итог |
| --- | --- | --- |
| <дословная цитата> | <что видно в результате> | <выполнено или нет> |

## Чем подтверждено

- <проверка>: <её вывод одной строкой>
- Не гонялось: <что в набор не вошло и почему>

## Оставшийся шаг

Папка задачи разобрана коммитом `<sha>` — за работой убрано. Осталось дождаться прогона и снять
черновик; до этого кнопка слияния заблокирована хостингом.
```

With a base other than the main branch the link line carries the way the task closes — one of
the two, by the tree's decision:

```markdown
Closes #86 — задача закрывается конвейером дерева при слиянии в ветку эпика.
```

```markdown
Задача #86 — закрывается рукой после слияния череды, с комментарием со ссылкой на этот PR.
```

The "Remaining step" section stands last and is rewritten by the same call as the rest of the
body — in the turn that lifts the draft:

```markdown
## Оставшийся шаг

Не осталось: прогон зелёный, черновик снят. Можно вливать.
```

It stands there because the merge decision is made on that page, not in the conversation: what
was said to the owner aloud lives until the next reply, and the body lies right by the button.
One does not cancel the other — the order of both messages to the owner is described by the
pattern for closing work.

There is nothing to check the body by machine: no audit reads it, and the host asks only about
the title. The sample is held by whoever writes the body — like the words said aloud.

## Common misses

- A second `Closes` line in one PR no longer closes a task: two tasks in one branch roll back
  only together. Either it is one task — and the second is absorbed — or two branches.
- Half a task that left by its own PR is a miss too: the body of such a PR starts with the words
  `Часть #<номер>` instead of `Closes`, and the task stays open. Work that does not fit one
  branch is split into tasks before the branch is created.
- Labels set by the PR title, not read from the task: the area is lost, and the board does not
  show that the edit touched the site too.
- The task closed not in full, but the labels carried over whole: the task stays open, and the
  PR body says so instead of implying it by a `Closes` line.
- A `Closes` line in a PR whose base is not the main branch, in a tree without a closing pipeline:
  the task looks attached and stays open after the merge. The body names the task in words, and
  the cleanup step closes it by hand.
- Labels read with `join(",")` and split by a shell expansion: zsh does not split an unquoted
  `${L//,/ }` into words, the REST call gets the whole line as one label, and the host creates a
  label with that name. Each label goes as its own `-f 'labels[]=…'`, or is read one per line with
  `--jq '.labels[].name'`.

## How a task of an epic closes in this tree

The `Closes #<номер>` line stays in every PR body here, whatever the base. A merge into `main` is
read by the host; a merge into an epic branch or a chain branch is read by this tree's own pipeline
`.github/workflows/close-epic-tasks.yml`: it closes the task with a comment naming the PR and the
branch. The body of such a PR says so by the first sample of the section «PR body sample» — «задача
закрывается конвейером дерева при слиянии в ветку эпика». The hand closes nothing here: a task
still open after such a merge is a red run of that pipeline, and it is read by its output.
