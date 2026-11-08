---
name: git-workflow-commit
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load for creating a task and a branch, commit and push — the creation command with all four steps, moving the column, merging two tasks into one, working as the machine account, skipping the document requirement. Opening a PR — pattern git-workflow-pr.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-commit.github.md · fae1cad32185 · правится надстройкой, не здесь -->

# Task, branch and commit

Pattern of the rule `git-workflow`. What must be true meanwhile — the law
`docs/constitution/delivery.md`.

## When to use

- A task is being created, and the edit starts from it.
- A branch is being created for a task.
- A commit or a push is being prepared.
- The work moved to the next step, and the task moves to another column of the board.

## First the task on the board, then the branch

Creation is four steps: the issue, the number in its title, adding to the board, the first
column. The board is not bound to the repository — its `projectsV2` is empty — so the third step
does not happen by itself, and without it the task is visible neither in the work queue nor to
the owner: two tasks stood that way for a month.

All four steps are done by one tree command, not by hand: splitting them means forgetting the
third.

**A command that does not exist is not replaced by client calls in the pattern.** A tree that
takes the package for the first time gets the check files, but not the entries about them in its
manifest: the layout edits resources, and the consumer's manifest does not belong to it. Two ways
from here: create the command in the same turn, or repeat all its steps by name from the list
above. A bypass by client calls looks like execution up to the last step of the list: it is
forgotten first, because the previous ones have already given a visible result. So a card stood
outside the columns for the whole work — two commits and two closed stages.

**The local branches of this task are read before a new one is created.** The board does not see
branches, and a task whose work lies finished in a local branch looks open to everyone: the column
is moved by hand, there is no PR, and the branch is visible only on the machine where it was
created. So a second branch was created under one number, with its own task folder and its own
plan — that is, the work was planned a second time, and the owner had to choose between the two.

```bash
git branch --list '<КЛЮЧ>-<номер>-*'
```

One line of answer means the work is already started: its state is read in the progress of its
folder, not created anew. An empty answer speaks only about this machine — a branch created on
another and not handed to the host is invisible from here too.

**The work queue is asked before the task is created, not after.** What one's own audit found
feels new, and that feeling is the only thing behind the decision to create a task: the creation
command answers for its calls and knows nothing about the queue's contents. It is asked by a search
over the topic words, together with what was closed in the last month: a defect closed and back
again is the same work, not a new one. A duplicate costs a lot — the whole work goes through it,
and merging two tasks into one afterwards is done by hand.

```bash
/opt/homebrew/bin/gh issue list --state all --limit 200 --search '<слова темы>' \
    --json number,title,state
```


```bash
npm run task:new -- --epic-of <номер эпика> --title 'Письма владельцу не уходят молча' \
    --label bug --label area:api --slug mail-owner-silence < описание.md
```

The body is read from standard input, `--slug` is optional and goes only into the hint with the
branch name. The epic is named by `--epic-of`, and the command writes the line about it into the
body itself and prints the branch line from the branch of the epic; work outside an epic goes by
`--outside-epic '<слово владельца>'`, and without either of the two the call is refused before the
card is created. The epic itself is created by the same command with `--epic`. Author and assignee — the machine account; the command reads the token itself, from
a file outside the repository.

A task created under an epic that has closed since is taken outside the epic, not by reviving
the epic branch. The delivery guard reads the epic from the line in the task body, and for a closed
epic it demands a branch in the remote that nobody will send again. The line about the epic is
replaced in the body by `Работа вне эпика — <слово владельца>`, the shape `--outside-epic` writes,
and only then is the branch created.

The script under this command is created by the project — the package does not ship it. What it
does by `gh` calls:

```bash
gh issue create --title '[<КЛЮЧ>-<номер>] …' --label bug --assignee <бот> --body-file -
gh issue edit <номер> --title '[<КЛЮЧ>-<номер>] …'   # the number is known only after creation
gh project item-add <номер борды> --owner <владелец> --url <адрес issue>
```

The last step is the one that gets forgotten: without it the task is created, but it is not in the
queue.

Creation ends not with the command's output but with the work queue's answer. The command asks
it itself and prints what it read — presence on the board, the column, the assignee; absence ends
it with a non-zero code. That answer goes into the comment, the PR body and the plan, not the
printed number: the number says "the call went through", not "the task is visible to whoever
works on it".

Creations that go one after another are checked not by the last one but by an audit of the whole
queue: their miss is shared, and by one task it is invisible. Sixteen tasks in a row printed a
number, and not one reached the queue so that the owner saw it.

A task created from the text of a document names a check in the tree in its body. A quote is
never the ground: a document speaks of intent, goes stale silently and stays true on the face of
it, while a task is created for what is in the tree now. The body holds the file and the symbol
where the miss is visible, or the command output that shows it. Neither found — the task is not
created, and the document line is edited in the turn that read it.

The task title says what is wrong, not what to do: the PR turns it into the done later. The number
is not written into the title by hand — it is known only after creation, and the command appends
it itself.

What to check the work queue with:

```bash
npm run check:board
```

It looks only at what is open: the tasks on the board, the number and the assignee of every open
task, and for every open PR — the number in the title, the `Closes` line, the open task behind it
and that there is no second PR with the same number. It does not judge the branch name: an open PR
cannot have it renamed.

Closed tasks the audit does not look for on the board, and there is no need to add them there
after the fact: a closed task leaves the queue by merge, and the board has no column for it. Of a
closed task the audit remembers only one thing — its folder in `docs/tasks/`.

## Two tasks fixed by one edit

If it turned out along the way that the edit closes the neighbouring task too — that is one task,
not two. They can be merged while the edit has not reached the main branch:

```bash
GH=/opt/homebrew/bin/gh
# what the absorbing task lacked is appended to its body
$GH api -X PATCH repos/<владелец>/<репозиторий>/issues/<поглотившая> -f body="$(cat тело.md)"
# the absorbed one is erased with its number — two lines about one work are worse than a numbering gap
$GH api graphql -f query='mutation { deleteIssue(input: {issueId: "<node-id>"})
    { repository { name } } }'
```

Deletion is irreversible and takes away the `Closes #<номер>` links from other bodies with it — so
the absorbing task is edited first, and only then the absorbed one is erased. After the merge
there is no absorbing: the branch went in, and it is reverted whole.

## The branch is created by a separate call

The main branch guard parses the command text and looks at the branch at launch, so a compound
command is rejected whole — the branch does not exist in it yet:

```bash
✗ git checkout -b <КЛЮЧ>-85-guest-token && git commit -m 'feat(<область>): …'
✓ git checkout -b <КЛЮЧ>-85-guest-token
✓ git commit -F -
```

The base is the epic branch, not the main branch — `git checkout -b <КЛЮЧ>-85-guest-token
<ветка эпика>`. From the main branch only the epic branch itself is taken: a task branched from it
carries into it what the epic has not finished.

The name — `<КЛЮЧ>-<номер задачи>-<короткий-slug>`, the slug in lowercase Latin letters joined by
hyphens. The delivery guard parses it on the spot and refuses a miss in the form before the first
commit, and by the number it asks the board: the task must exist, be open, stand in the queue and
have an assignee.

A name without a number (`feat/…`, `fix/…`) is legitimate while the branch lives locally — for a
trial and an analysis. No PR opens from it: an edit that reaches the main branch starts with a
task.

**A local branch that continues an open PR under another name is tied to the PR's branch before
the first push.** Otherwise it has no upstream: the push goes nowhere by itself, and the turn-exit
guard counts every commit as not handed over while all of them already stand in the PR. The tie
and the push name the PR's branch:

```bash
git branch --set-upstream-to=origin/<ветка PR>
git push origin HEAD:<ветка PR>
git rev-list --count @{u}..HEAD   # 0 — everything is on the host
```

## The task column moves together with the work

Branch created — the task is no longer in `📋 Backlog` but in progress. PR opened — it awaits
review. Both moves are done by one command, as a second call right after the one that caused it:

```bash
npm run task:move -- 86 in-progress   # right after git checkout -b <КЛЮЧ>-86-…
npm run task:move -- 86 in-review     # right after gh pr create
```

The columns under their own names: `backlog`, `in-progress`, `in-review`, and also `new`,
`ready`, `done` and `deployed`, which the work does not pass through — a closed task leaves the
queue by merge. The command edits the board as the bot, reads the token itself and prints from
where to where it moved; it accepts neither tasks off the board nor an unknown column.

The move is not put off for later: the work queue is read between steps, not after them. A task
with an open PR stood in `📋 Backlog` until the audit itself — all that time it looked untouched,
and nobody was waiting to review it.

## The commit is signed by the bot

The token is read into a variable and not printed; author and committer are set by variables of
the same command. `git config` will not do — the config is shared with the main tree and would
rewrite the signature to the owner:

```bash
TOKEN=$(tr -d '\n' < ~/.config/<дерево>-bot-token)

GIT_AUTHOR_NAME="<бот>" GIT_AUTHOR_EMAIL="<номер>+<бот>@users.noreply.github.com" \
GIT_COMMITTER_NAME="<бот>" GIT_COMMITTER_EMAIL="<номер>+<бот>@users.noreply.github.com" \
    git commit -F -
```

The subject — `type(scope): description`. Types: `feat`, `fix`, `refactor`, `docs`, `style`,
`test`, `chore`, `perf`. Scopes: `site`, `admin`, `api`, `common`, `proto`, `deploy`. A full stop
at the end of the subject is not accepted; the length — up to 150 characters. The letter case is checked as well, by the `subject-case` rule of the commit check: a word in capitals, such as a file name, can trip it, so the allowed case is read in the commit check settings before the subject is written.

```
feat(<область>): availability calendar with season prices
fix(<область>): reject overlapping booking dates
chore(deploy): docker-compose for vps
```

## The files of one's own work are named one by one

The working tree is one, and there can be several works in it: someone else's uncommitted folder,
a draft left behind, an edit of a neighbouring session. A directory added whole takes them along,
and what this work never asked for leaves for the main branch.

```bash
git add docs/tasks/<КЛЮЧ>-<номер>-<slug>/plan.md docs/tasks/<КЛЮЧ>-<номер>-<slug>/progress.md
git diff --cached --name-only     # what actually got into the index
```

Checking the index after adding is not enough: a foreign file added once becomes tracked and goes
on silently — the next `git add` no longer asks about it.

## The document goes in the same commit

`docs-guard` demands the pair and names it itself. The bypass — a line in the body, the reason
is mandatory:

```
Docs-skip: правка только в тестах хука, зеркала у него нет
```

The guard looks for the `Docs-skip` line in the command text only. A message read from a file by
`git commit -F <file>` is invisible to it and the commit is refused; the body goes inside the command,
as in `git commit -F -` with the text after it.

## Common misses

- **An amend goes through the same hooks as a commit.** The flag that skips the commit hooks is not
  used for any edit, a one-letter typo in the subject included. The gate before a push does not
  read commit messages, so a message the hook never saw reaches the host unchecked. A commit that
  skipped the hooks is redone without the flag before the push.
- **An audit right after adding answers "no" when the card already stands.** The work queue gives
  out a new item not in the same second it was created, and the last step reads it by the next
  call. The answer to this is to reread the whole queue, not to create the card a second time: two
  records about one task are removed only by an administrator. The creation command itself needs
  an edit here: the state is read right after the mutation, without a retry, and a false refusal
  here costs more than a delay.
- `gh` in the user's shell is substituted — call `/opt/homebrew/bin/gh` directly.
- A directory added whole with someone else's uncommitted work next to it: a foreign task folder
  left for the main branch and became tracked.
- `git add` with several paths adds nothing if even one path does not exist: the command breaks
  off whole at the first miss instead of skipping it. The next `git commit --amend` then carries
  into the commit everything left in the index — so a file deletion belonging to a neighbouring
  branch went into the commit. The commit contents are read by `git show --stat` right after it,
  not at PR review.
- The index contents are read by `git diff --cached --stat` **before** the commit, not only by
  `git show --stat` after it. Tree commands put files into the index themselves: `npm run
  task:new` adds the task folder, and everything lying next to it goes along — so a temporary
  diagnostics directory ended up in the index.
- `gh project` with `--owner` answers `unknown owner type`: the board owner is another account,
  and the edit goes only through GraphQL.
- A created task is not taken onto the board by itself: the repository is not linked to it, and
  adding goes by a separate call. Two tasks stayed outside the work queue that way — which is why
  all four steps are done by `npm run task:new`, not by hand.
- The assignee of a task is not set by itself either at creation through the web or at adding to
  the board: of ninety-nine open tasks it stood on two.
- A task created through the web, past the command, does not reach the board and is not refused
  by the guard — it looks at the command, not at the task. Only the queue audit catches this.
- The task column does not move by itself either from creating a branch or from opening a PR: the
  board does not see the branch at all, and the link to the PR fills only the host's field of
  linked PRs. The audit does not catch taking into work either — the branch is invisible to it
  too.
- `gh api graphql --paginate` on a query of board items goes into repeating the first page: the
  cursor is taken from the answer by hand, and completeness is checked against
  `items(first: 1) { totalCount }`.
- Two commits chained in one call: a commit refused by the message check leaves its files in the
  index, and the next `git commit` takes them under its own subject. One commit is one call, and
  its outcome is read before the next; a swallowed one is split by `git reset --soft HEAD~1` and two
  commits anew.
- The push set listed by hand without the package defaults: the tree profile extends the package
  one through the default function, and sourced alone it calls an undefined function. The error
  goes to a stream nobody reads, and the list loses lint, unit tests, the build and the spec audit
  with a zero exit. The defaults are sourced first, and the line count is compared with the last
  push before the run.
- The owner's edit takes neither the token nor the variables — they are only for machine work.
- A commit into the branch of a merged PR reaches no one: the host deleted the branch, and a push
  creates it anew with an answer `new branch`. The delivery guard refuses such a push and names the
  merged PR. The commit moves to a new branch from the fresh base by `git cherry-pick`.

## The closing columns in this tree

The section above says the work does not pass through `done` and `deployed`. Here it does, and
by no hand: a merged edit closes its task, the board rule «Item closed» moves the card to Done,
and the rollout moves the closed ones on to Deployed.

- **A task closes on the merge of its PR — into main by the host, into any other branch by the
  pipeline `close-epic-tasks.yml`.** The host reads `Closes #…` only on a merge into the default
  branch; the pipeline reads the same line on a merge into an epic or a chain branch and closes
  the task with a comment naming the PR and the branch. So «closed» here means «merged into the
  epic branch», and the epic's own progress grows as its tasks land.
- **Deployed is set by the rollout, its last step, not by a merge.** After a successful rollout
  `tools/board-deployed.mjs` moves every card in Done with a closed task — except a task of an
  epic still open: that one reached the epic branch, and main only with the epic. The dry run on
  this machine names what would move today: `node tools/board-deployed.mjs --dry-run`.
- **Neither column is moved by hand.** `task:move` accepts both names, and that is for a repair
  after a miss, not for the order of work.
