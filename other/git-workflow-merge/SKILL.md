---
name: git-workflow-merge
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load when the base of a branch is merged into it and a conflict is resolved — the merge order, handling by file kind, checking what was appended against the work queue, re-reading the body of the open request. Branch and commit — pattern git-workflow-commit.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-merge.md · 5ceb1171ded8 · правится надстройкой, не здесь -->

# Merging the base of a branch into it

Pattern of the rule `git-workflow`. What must be true — the law
`docs/constitution/delivery.md`.

**The calls here are given with the GitHub client.** A tree on another host reads them as the
form and takes the command from its own client: field and subcommand names differ between
clients, and what is asked is one. The match is named by the edition of the delivery rule laid
out in that tree.

## When to use

- The PR is marked conflicting, and it must be brought back to a mergeable state.
- The base of the branch moved ahead, and the branch must be caught up before the checks: for a
  task branch the base is the branch of its epic, for an epic branch the main one.
- The main branch moved ahead, and the whole epic must be caught up: the main branch is merged
  into the epic branch, and the epic branch into the branches of its unfinished tasks.
- A commit is carried over by a cherry-pick.

## Order

```bash
git fetch origin
GIT_AUTHOR_NAME="<бот>" GIT_AUTHOR_EMAIL="<номер>+<бот>@users.noreply.github.com" \
GIT_COMMITTER_NAME="<бот>" GIT_COMMITTER_EMAIL="<номер>+<бот>@users.noreply.github.com" \
    git merge origin/<база> --no-edit
git diff --name-only --diff-filter=U     # what ended up in conflict
```

The signature stands in the command itself: that command creates the merge commit, not a
separate `git commit`, and there is nothing to change its signature with later — a merge that
left with a person's signature is refused at push and fixed by rebasing onto the main branch.

The conflict list is read whole before the first resolution: the file kind decides the
technique, and different files of one merge are resolved differently.

| What ended up in conflict          | How it is resolved                                                                 |
| ---------------------------------- | ---------------------------------------------------------------------------------- |
| code                               | the `git-workflow` rule's pitfall about a deletion side; after — `npm run check:dupes` |
| a build from a description         | rebuilt from the description after the description is resolved: a generator writes the lines of such a file, and sides joined by hand give a file it would never output |
| a spec in `docs/specs/`            | by keeping both sides, if both appended; a section removed by one side stays removed — rule `spec-driven`; after — `npm run check:specs` |
| a rule's companion next to the rule | by keeping both sides — the same two additions to one table; after — `npm run check:specs` |
| the table of working-copy assignments | by the base's side whole. The owner fills it in the main branch, and a session does not write it: the branch's side can only be an older copy. After — the reading the session start prints |
| the work list (`docs/BACKLOG.md`)  | by the selection sign — pattern `doc-style-sweep`                                  |

## A commit is carried over by a cherry-pick

The branch the commit was meant to leave with is gone: merged, removed by the host or created
under the wrong task. The commit itself is intact and lies in the fallen-off branch.

```bash
GIT_COMMITTER_NAME="<бот>" GIT_COMMITTER_EMAIL="<номер>+<бот>@users.noreply.github.com" \
    git cherry-pick <sha>
```

The signature variables stand on the carry-over command itself. A cherry-pick keeps the commit's
author and sets as committer whoever calls it — that is, a person; the check set before a push
reads the committer, and this is then fixed by a rebase, not by editing one commit.

The fallen-off branch is removed on both sides in the same turn — otherwise it stands in the
list as unclosed work.

## What the branch appended is seen only from the divergence point

A conflict marker shows the place, not the edit: the branch's side in it is its addition
together with everything that lay in the file before it.

```bash
git diff "$(git merge-base origin/main HEAD)" HEAD -- docs/BACKLOG.md
```

## What the branch appended is checked against the work queue, not carried over by default

The section the branch appended to the work list usually already stands as a task by merge
time: a branch lives for weeks, and a defect noticed along the way is created as a task at once.
Carrying it over a second time means creating a second record of one work.

```bash
/opt/homebrew/bin/gh issue list --state all --limit 400 --search '<слова из раздела>' \
    --json number,title,state
```

The task carries the same content — the branch's side is not carried over:

```bash
git checkout --theirs docs/BACKLOG.md && git add docs/BACKLOG.md
```

In a merge `--theirs` is the merged-in base and `--ours` is the branch standing on it; in a rebase
the sides swap. The wrong side taken erases work silently.

## Checks after the resolution

**A conflict in a laid-out file that executes is resolved by the same call that found it.**
Markers in a guard's body are a syntax error, not a text discrepancy: the branch falls, the
dispatcher returns its code as a refusal, and there will be no next shell call — with it every
other door named in that guard's declaration is refused too. An executable file is recognised by
the line `# rt-hook:` in its header; a deferred "I'll fix it later" here means a session there is
nothing to continue with.

A conflict in texts does not touch the code, and a green build says nothing about it:

```bash
grep -rn '^<<<<<<< \|^>>>>>>> ' --exclude-dir=node_modules --exclude-dir=.git .
npm run check:docs && npm run check:specs && npm run check:dupes && npm run check:board
bash .claude/hooks/tests/run.sh       # if the conflict touched the hooks
```

A merge without conflicts is not exempt: two branches can declare the same value apart, and the
merge joins them silently — the duplicate check turns red only at the push. After every merge of the
base, a conflict-free one included, the duplicate and the styles checks run (`npm run check:dupes`
and `npm run check:styles`), and the value moves to its one shared place; no line goes into the
known list.

**After a merge of the base, the migrations it brought are read.** Those that set the rights of a
role are opened. A branch migration that writes a role's full set of rights drops any right the base
added meanwhile; git sees two different files and marks no conflict, and the fall shows later as a
failing test on the count of rights, easy to take for a test error. The lost right returns by a new
migration of the branch.

The merge commit is signed by the bot the same way as any other — pattern
`git-workflow-commit`. After the push the state is read from the PR itself, not from one's own
tree — more on this in pattern `git-workflow-pr`:

```bash
/opt/homebrew/bin/gh pr view <номер> --json mergeable,mergeStateStatus
```

## The body of the open PR is reread after the merge

The PR described the tree on the day it was written. Merging the main branch changes what it
states: the body said both defects were entered in `docs/BACKLOG.md`, and by then the main
branch had taken that list apart. The body is edited by a REST call — `gh pr edit` in this
repository refuses about Projects (classic) and never reaches the edit:

```bash
/opt/homebrew/bin/gh api -X PATCH repos/<владелец>/<репозиторий>/pulls/<номер> -f body="$(cat тело.md)"
```

## The task of a merged PR is asked, not assumed closed

The host closes the task by the `Closes` line only when the base is the default branch. A PR
merged into an epic branch or into the previous branch of a chain leaves its task open unless the
tree closes it by a pipeline of its own — and the column of the board lags the work until then.
After every known merge with such a base the task's state is asked by a command; one still open
is closed by hand with a comment naming the PR — the calls are in the pattern
`git-workflow-stack`.

```bash
gh issue view <номер> --json state --jq .state
```

## A green run ages together with the main branch

A run speaks about the base it went on. While it goes and the PR awaits review, the main branch
lives its own life, and the local ref is silent about it: it describes the day it was pulled.
Before a PR is called ready to merge, the lag is asked from the host:

```bash
/opt/homebrew/bin/gh api repos/<владелец>/<репозиторий>/compare/<главная>...<ветка> --jq .behind_by
```

Zero — the PR is ready. Above zero — main is merged in, the check set is revised by what the
branch now carries, and the run goes anew: green steps of the past run mean nothing after the
merge.

## Other people's task folders arrive with the main branch

A merge of the main branch carries everything merged into it — including the task folders of
neighbouring works, if those went into main not taken apart. In one's own branch they look like
one's own: they lie in the same directory, named in the same order, and there is nobody to take
them apart from here.

The merge button is pressed by a person, and where they do it there are no hooks: the guard
watching the folder's taking apart does not reach that path. So the work queue audit is run
right after merging main, not before the push:

```bash
npm run check:board
```

It names a folder with no open task — that is the arrived foreign one. It is not taken apart by
one's own hand: it is removed by whoever's work it is, in their own branch.

## Common misses

- "Keep both sides" applied to all files alike: in a spec it is right, in code and in the work
  list it is not.
- **A merge carries edits of files, not edits of an application.** A function switched on by one
  line in the root of one application stays off in the second application of the tree: nobody
  touched that root, so there is no conflict, and an optional dependency is allowed to be absent, so
  no check turns red. After the merge the diff of the merged-in roots and shared layers is read for
  every application of the tree: each added line is either carried over or named in the report as
  not needed there.
- The merge command taken without the signature variables: the merge commit is signed by a
  person, and the push set refuses it — at the step where all checks are already green. This is
  fixed by rewriting the branch, not by editing one commit: conflict resolutions usually already
  lie behind the merge.
- The branch's side carried over without a check against the work queue: one work became two
  records.
- After the resolution the build was run, and the text checks were not: the build cannot see a
  conflict in them.
- The PR body left as it was: the reviewer reads a statement about a tree that no longer exists.
- The PR called ready by a green run: the steps went from a base that is no longer in the main
  branch.
- A section removed by the main branch came back by "keeping both sides": the spec has two
  copies of one paragraph, and the removed one reads as in force.
- A cherry-pick taken without the committer variable: the commit's author is the old one, the committer is a person, and the check set refuses the push.
- The merge left with a person's signature: there were no variables in the merge command, and
  the line about the signature lies below the command and is read only after the commit.
