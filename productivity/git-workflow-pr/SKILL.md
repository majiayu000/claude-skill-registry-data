---
name: git-workflow-pr
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load for opening a PR and everything around it — title format, draft and leaving it, reading the PR state, the checklist. The link to the task, reviewer, labels and the body sample — pattern git-workflow-pr-body; creating the task and committing — git-workflow-commit.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-pr.github.md · 39043493a1e3 · правится надстройкой, не здесь -->

# The PR

Pattern of the rule `git-workflow`. What must be true — the law
`docs/constitution/delivery.md`. Creating the task, the branch and the commit — pattern
`git-workflow-commit`.

## When to use

- A PR is opened from a finished branch.
- The title, body or labels of an already open PR are edited.
- The draft is lifted, and the work is handed over for review.
- The PR state is read before anything is said about it to the owner.

## The task number stands in its title and in the PR title

One form for both — `[<КЛЮЧ>-<номер>] <текст>`. The number stands in the title itself, not only
in the body: the PR list shows no bodies, and in the task list the number otherwise has to be
found by eye in the left column. The branch name carries the same number —
`<КЛЮЧ>-<номер>-<короткий-slug>` — so task, branch and PR read as one.

The task says what is wrong; the PR, under the same number, says what was done:

```
задача  [<КЛЮЧ>-86] Пустой MAIL_OWNER — письма владельцу не уходят молча
PR      [<КЛЮЧ>-86] Письмо владельцу с незаполненным адресом попадает в логи

задача  [<КЛЮЧ>-101] Вернуть оверлей загрузки таблицы и включить stylelint гейтом
PR      [<КЛЮЧ>-101] Stylelint включён гейтом

задача  [<КЛЮЧ>-212] Сайт не собирается: компонентам кита проставлен префикс приложения вместо своего
PR      [<КЛЮЧ>-212] Виджет переписки зовёт кит его собственными именами
```

The infinitive of the task does not carry into the PR title: "fix" becomes "fixed", "restore" —
"restored", "add" — "added".

The number in the title must match the branch number: the delivery guard checks them before the
command is sent, and the queue audit — on every open PR.

Type and scope — `fix(site):`, `docs(common):` — do not go into the PR title: that is the commit
subject format, and `commitlint` checks it there. In the PR list it takes room and adds nothing:
the kind of edit and the area are already visible by the labels.

## A draft where a run is waited for, ready where it is not

A code edit is handed to a person by an open PR: a pushed branch is shown to them nowhere. An
open PR reads as an invitation to merge, so unfinished work opens it as a draft — the host locks
a draft's merge button itself.

**Which bases the pipeline wakes for is read from its file, not from memory.** That one line decides
which of the two orders applies, and taking the wrong one means either waiting for a run that never
comes or handing over unchecked work as finished:

```bash
# the bases the checks wake for; nothing printed means every base
sed -n '/^on:/,/^[a-z]/p' .github/workflows/<файл конвейера>
```

A base the pipeline wakes for — the PR opens as a draft, and the draft is lifted on the green run:

```bash
GH_TOKEN="$TOKEN" gh pr create --draft --base <ветка эпика> --title '[<КЛЮЧ>-86] …' --body-file тело.md
```

A base it does not wake for — nothing to wait for, and the PR opens without the draft key. The push
gate is then the only blocking check behind the work, green before the branch is sent:

```bash
GH_TOKEN="$TOKEN" gh pr create --base <ветка эпика> --title '[<КЛЮЧ>-86] …' --body-file тело.md
```

**The base is the epic branch, and it is named by the command.** Without `--base` the host takes
the repository's default branch: the request then carries the task past the epic, and the epic
branch stays a copy nobody merges. The epic's own request is the only one based on the main branch,
and it opens when the last folder of its tasks is taken apart.

Before `gh pr create --base <ветка>` the base is checked on the host by `git ls-remote --heads origin
<ветка>`. An empty answer means the base was merged and removed: the request then takes the next
branch up the chain as its base, not the removed one.

Everything waiting for a pipeline run, a rework or an answer goes as a draft, and the question is
asked in the PR itself: a person reads the PR, not the session's conversation.

The draft is lifted by a separate call, and that is the very turn in which the executor says the
solution is ready:

```bash
GH_TOKEN="$TOKEN" gh pr ready 86
```

Before the lifting the executor's silence means "not ready yet", after — "may be merged".
Lifting the draft and asking to merge go in one turn: a lifted draft nobody told the person about
waits for review just like one not lifted. A PR opened without the draft key needs no such call,
and the request to merge goes in the turn that opened it.

## The link to the task and the body

The `Closes #<номер>` line, the reviewer, the assignee and the labels set by the opening call,
the four sections of the body and how the task closes when the base is not the main branch —
pattern `git-workflow-pr-body`. The pattern was split out of this one by the length limit.

## The PR state is read, not guessed

The calls that set the reviewer, labels and assignee answer with a zero code even when they did
nothing: GitHub silently drops a review request on the PR author. So after them the PR is reread:

```bash
# Keys in Latin letters: `jq` cannot parse an unquoted Cyrillic key and fails on it
$GH api "repos/$REPO/pulls/321" \
    --jq '{author: .user.login, reviewers: [.requested_reviewers[].login], labels: [.labels[].name]}'
```

The author here is `<бот>`. If it turned out to be the owner, the PR will have no reviewer at
all: the author cannot be made the reviewer, and no refusal comes for such a request. The owner
is told what was read, not what was ordered.

A discrepancy read has an assigned action: a PR's author cannot be changed, so it is closed and
opened anew with the machine account's token — carrying over the body, labels, reviewer and
assignee. The number changes, and links to the old one are rewritten in the same turn. A fork
brought to the owner here means the delivery order was read and not carried out.

The account one had to push from does not carry into this call: push and PR authorship are
chosen separately, and `GH_TOKEN` for publishing is always the bot's token.

It is reread by time too, not only after calls that silently did nothing: the PR state is read
before anything is said about it. Between "the run is green" and the next phrase the owner has
time to merge the PR, and everything said about it after that is about yesterday. That is how
the owner was offered to merge what they had merged an hour earlier.

The state is read before a push into a branch that has a PR too. A merged PR means the branch is
no longer on the server: the push will not update it but create it anew, and the contribution
stays outside the main branch. The push answer says this with a new-branch mark instead of a list
of commits — otherwise it looks exactly like a successful push.

**After a push that carries a merge of the base, the PR's count is matched against the comparison
of the branches.** The host counts the commits and files of a PR from the base commit it stored
when the PR opened or was last retargeted, and a push does not always move it. The base merged into
the branch then shows inside the PR as its own work: a PR with 30 commits of its own read as 153
with 371 files, while the comparison of the same branches answered 30 at the same minute. The count
is asked from both sides:

```bash
$GH api "repos/$REPO/pulls/321" --jq '{base: .base.sha[0:9], commits: .commits, files: .changed_files}'
$GH api "repos/$REPO/compare/<база>...<ветка>" --jq '{ahead: .ahead_by, behind: .behind_by}'
```

`commits` other than `ahead` is cured by setting the same base again — the host recounts the PR in
the same answer:

```bash
$GH api -X PATCH "repos/$REPO/pulls/321" -f base=<база> --jq '{base: .base.sha[0:9], commits: .commits}'
```

**The run's outcome is read by a separate call, not by the wait's return code.** The client
command that waits for the run's end returns zero on red too: it waited for the end, not for
success. Read as an outcome, this zero makes green what fell, and what was said to the owner
about a green run turns out to be about a red one. The run's state and conclusion are asked by
their own call — the same one that reads the PR state.

An open PR means the task awaits review — the column is moved in the same motion:

```bash
npm run task:move -- 86 in-review
```

This is not written as bare GraphQL by project, item and field option ids: the command knows
them itself, and a query assembled from memory silently sets the wrong column — the board has no
refusal for that.

## Answering under remarks

Remarks arrive on a PR in three places: a comment on a line, the text of a review and a comment in
the conversation. All three are read at once, before the first edit:

```bash
gh api repos/<владелец>/<репозиторий>/pulls/<номер>/comments --paginate \
    --jq '.[] | {id, user: .user.login, path, body}'
gh api repos/<владелец>/<репозиторий>/pulls/<номер>/reviews --paginate \
    --jq '.[] | select(.body != "") | {id, user: .user.login, body}'
gh api repos/<владелец>/<репозиторий>/issues/<номер>/comments --paginate \
    --jq '.[] | {id, user: .user.login, body}'
```

The person is asked by the asking tool whether to answer under them, in the turn the remarks were
read. The answer holds for this PR. Silence is not a yes: a message on the host stays there, and
it goes out under an account the person answers for.

After a yes every remark gets its own answer, once the edit has reached the host: a commit named
before the push does not exist for the reader yet.

```bash
gh api -X POST repos/<владелец>/<репозиторий>/pulls/<номер>/comments/<id>/replies \
    -F body=@ответ.md
```

The text of a review has no thread of its own, so the answer to it goes into the PR conversation:

```bash
gh api -X POST repos/<владелец>/<репозиторий>/issues/<номер>/comments -F body=@ответ.md
```

An answer is written in the owner's language and names one of two things: the commit that closes
the remark, or why the remark is declined. The count of answers is compared with the count of
remarks read at the start: a remark left without one is a remark the person checks again by hand.

## What is checked before the PR is published

There are no checks on the PR itself: the rollout starts with a push into the main branch, and
before the merge nobody runs anything. Linters, unit tests and hook scenarios are taken by the
push gate — below is what it does not know.

1. **The base is merged into this branch** — for a task branch that is the epic branch, for an epic branch the main one: `git fetch origin && git merge origin/<база>`.
   Base freshness is not inherited between branches of one session: the second and the third
   are taken after their own `fetch`, not from the ref under the first. While work goes on, main
   moves ahead — most often by the same executor's own PR. Everything checked below is checked
   from this base: a PR from a diverged branch shows the reviewer the edit mixed with someone
   else's. Order and conflict resolution — pattern `git-workflow-merge`.
2. **The branch holds only the edit it was created for** — `git diff main...HEAD --stat`. A
   foreign domain in the file list means the edit has spread, and it must be brought back within
   its bounds.
3. **No mock, no substituted response, no debug line** — `git diff main...HEAD` is read whole,
   not by file names. They go to production silently and corrupt real data.
4. **The document goes in the same commit.** `docs-guard` names the pair, but it does not know
   the domain spec and an edit of its behaviour — that stays with the author.
5. **Text and layout checks are green** — those the tree created in `tools/`: scenarios against
   tests, paths in documents, lib layout, duplicates and classes without a rule. Which ones
   exist here — the rule's `implementation.md`.
6. **All applications of the tree build** — `nx build` for each. The push gate does not run the
   build: it is longer than anything it can do between the command and the push.
7. **Visible text is entered in all translation locales** — by the dictionary completeness test,
   if the tree is translated.
8. **A layout edit is confirmed by a measurement**, not by a look, and captured on a narrow
   screen — pattern `browser-verification-measure`.
9. **A markup edit of the public site is checked on the production build in all translation
   locales** — the search visibility rule of the tree that has one.
10. **The PR body is assembled by the sample** — starts with the line `Closes #<номер>`, carries
    the sections "What was done", "What confirms it" and "Remaining step", and labels, reviewer
    and assignee are set. By this moment the remaining step section says no steps are left: the
    draft is lifted after the folder is taken apart, not before.
11. **The PR title carries the task number and names it done:** `[<КЛЮЧ>-<номер>] <Что сделано>`,
    with the same number as the task and the branch name. The infinitive of the task does not
    carry into it, nor do the commit type and scope.
12. **The work queue matches** — `npm run check:board`. The task is on the board, with an
    assignee and the number in the title; one PR per task, and it closes the task whole.
13. **The PR state is read, not derived from return codes** — author `<бот>`, reviewer — the
    owner, labels the same as on the task, the commit count equal to `ahead_by` of the branch
    comparison. The owner is told what was read.
14. **The set is taken from the pipeline file, not assembled from memory.** The push gate is
    narrower by design: it stands between the command and the push, and everything longer than
    seconds is taken out of it. What the pipeline runs is written in its file — that list is
    repeated locally; a green gate is not completeness of the set.
15. **The set is revised after merging the main branch in.** It is chosen by what the branch now
    carries, not by what the author edited. A branch that touched no line of the showcase runs
    the showcase snapshots: since the merge the pipeline runs them on its code, and the red
    comes to its PR.

Where the pipeline wakes for this base, the list is about lifting the draft: the PR opens as a
draft earlier, while work goes on, and the person is shown what exists together with what is
still missing. Items 1–15 are then passed before `gh pr ready`, and an unmet item means the draft
is not lifted — not that the PR does not open.

Where it does not wake, the same list is about opening: there is no second state to hold the work
in, so an unmet item means the PR does not open yet. Item 1 changes with it — no run is asked for,
and its place is taken by the push gate, green before the sending.

Right after publishing the task is moved to review — `npm run task:move -- <номер>
in-review` — and `npm run check:board` is run once more: before the PR opens it does not judge
the column, after the opening it sees the discrepancy.

What was done by reasoning and what was done by measurement are told apart plainly in the PR
body: the unchecked named as checked, the reviewer takes as checked.

**The "What confirms it" section names what was not run too.** A list of one run cannot be told from
the full set, and by it the reviewer decides what need not be rechecked. The price of a mistake here
is trust in the section: once read as complete, from then on it is rechecked whole.

## Common misses

Misses about creating the task, the branch and the commit — pattern
`git-workflow-commit`; about the link line, the labels and the body — `git-workflow-pr-body`.

- A PR opened without a reviewer: it never reaches the owner's inbox at all, and the queue stands
  while looking as if it works. That is how sixteen PRs waited for a review nobody had requested.
