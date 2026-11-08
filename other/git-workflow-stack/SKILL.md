---
name: git-workflow-stack
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load when pieces of work follow one another or more than two branches already stand on one base — chained branching from the previous one, the PR base, merging bottom-up, re-merging main on an actual conflict. One conflict — pattern git-workflow-merge.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-stack.md · 6ee2f61fb0fb · правится надстройкой, не здесь -->

# A stack of PRs from one base

Pattern of the rule `git-workflow`. What must be true — the law
`docs/constitution/delivery.md`. Resolving one conflict — pattern `git-workflow-merge`,
opening one PR — `git-workflow-pr`.

**The calls here are given with the GitHub client.** A tree on another host reads them as the
form and takes the command from its own client: field and subcommand names differ between
clients, and what is asked is one. The match is named by the edition of the delivery rule laid
out in that tree.

## When to use

- More than two branches are created from one base, and all wait for a merge.
- Several works were done in one session, and they lie in the tree unpublished.
- It is decided in which order to hand the accumulated over to the owner.

## A chain: branch from the previous one, not from the epic branch

A stack from one base is what to avoid. Works that go one after another branch one after
another:

```bash
# the first work of the chain — from the epic branch, as usual
git checkout -b <КЛЮЧ>-<номер>-<slug> <ветка эпика>

# each next one — from the previous branch, not from the epic branch
git checkout -b <КЛЮЧ>-<следующий>-<slug> <КЛЮЧ>-<номер>-<slug>
```

A chain lives inside one epic: every branch of it stands, directly or through its neighbours, on
the epic branch, and the lowest request of the chain has that branch as its base.

The previous edit then lies in the common ancestor, and two different changes of one file never
have to be reconciled at all. The divergence surfaces at branching — at the one who has both
edits as their own and at hand — not at the merge, at the owner, who has neither.

From the epic branch the first work of the chain and any work that does not touch the previous
one: a chain is about neighbouring works, not about all in a row.

## A chain PR stands on the previous branch

```bash
gh pr create --base <предыдущая ветка> --title '[<КЛЮЧ>-<номер>] <что сделано>' --body-file <файл>
```

Neither the main branch nor the epic branch is set as the base here: the review then shows the own
edit mixed with all under it.

**The base of the heir is retargeted by hand, by the same motion that merges the lower one.** The
host does it itself only when the merged branch is deleted; a branch is usually left after the
merge, and then the heir keeps standing on it — the upper PR merges into the neighbour and not into
the epic branch. A chain of nine went through this: the base moved by itself in none of the nine.

```bash
# right after the lower PR is merged — the base of the heir moves to where the lower one stood
gh api repos/<владелец>/<дерево>/pulls/<номер наследника> -X PATCH -f base=<основание нижней>
```

From the browser the same is done by editing the PR heading, where the base stands as a dropdown.
The miss turns red nowhere: the PR looks merged, and the work is not where it was meant to go.

**The `Closes` line of a chain PR is read by nobody at the host.** The host closes a task only
on a merge into the default branch; a chain PR merges into the neighbour, and the task stays
open with the column lagging the work. Which of the two the tree has — a pipeline of its own that
closes the task on such a merge, or the hand — stands in the PR body by the sample of the pattern
`git-workflow-pr-body`. The tasks of a chain are asked after every merge, not assumed closed:

```bash
# right after a merge — the task of the merged PR, then the rest of the chain
gh issue view <номер> --json state --jq .state
# still open — closed by hand, with a comment naming the PR that merged
gh issue comment <номер> --body 'Влита в ветку <основание> — PR #<номер PR>.'
gh issue close <номер> --reason completed
```

This is the cleanup step after the last merge of the chain: the branches are listed, the tasks
of the chain are asked, and what is still open is closed with the comment. A task closed in
silence, without the PR named, cannot be told from one closed by mistake.

The merge order stands in every PR body as the line "stands on #<number>, merge after it": the
owner merges by the list, and branch kinship is invisible in the list.

**The tree's pipeline is checked for whether it listens to a PR with such a base.** The host
sends the PR event with a base filter, and a tree that left only the main branch in the filter
gives neither the chain nor a single task of an epic any run at all: the PR stands green-and-empty, and there is nothing to
bring the event back — neither a new commit nor reclosing the PR changes the base. This is asked
before the chain is created: from the pipeline settings, not from the PR page, where a missing
run looks the same as waiting for one.

```bash
# the whole chain order — bottom-up
gh pr list --state open --json number,headRefName,baseRefName \
    --jq '.[] | "\(.number)\t\(.headRefName)\tна \(.baseRefName)"'
```

## What is not done in a chain

- **The lower branch's history is not rewritten.** Neither `rebase` nor a force push: the upper
  one's tip becomes reachable from its base, and the host closes the upper PR as merged — though
  main has none of its edits. A lagging lower one is fixed by merging main into it and onward
  upward.
- **A chain is not merged from the middle.** One merged out of order drags along everything
  under it — and the review of that work never happens.
- **A branch whose base was merged past it is looked for by hand.** The host counts the lower
  branch merged, closes its PR and offers nothing about the upper ones: their edits are in main,
  their own commits on top are not, and nobody is told. Such a branch is alive only while
  somebody remembers it — two pieces of work stayed in branches like that and were found by a
  list of branches, not by a list of PRs. After a merge out of order the branches of the chain
  are listed and each is either rebased onto main anew or closed by word.
- **Ready branches are not hoarded.** A chain does not cancel that the unit of work is a merged
  PR: it only makes safe the length that has piled up anyway.

## The unit of work is a merged PR, not an open one

An open draft is not work: its merge button is locked, main has none of its edits, and the work
queue is not shortened by it. Eighteen open drafts and not one merged is zero done, however much
time went into them.

Hence the order: one work is brought to the merge, then the next is taken. Not the other way
round.

## The price of a stack grows quadratically

Branches of one base that append to the same texts bring each other down at every merge: the
first merged makes the rest stale, the second merged — all but two, and so to the end. Opening
all at once, the executor assigns themselves about half the square of their number in merges of
main — and they do them, while a person presses the merges at their own pace.

This is counted before opening, not after: closing surplus PRs is cheaper than keeping them, but
the time spent on their bodies is gone by then.

## Main is merged in on an actual conflict, not on a schedule

A lagging branch and a conflicting one are different things. A lagging one the host merges
itself: edits of different places in one file are reconciled without a person. Only the one
where both sides touched the same lines conflicts.

So after someone else's merge, main is merged not into all open branches but into those the host
said conflict. This is asked with one call for the whole stack:

```bash
gh pr list --state open --json number,headRefName,mergeable \
    --jq '.[] | select(.mergeable == "CONFLICTING") | "\(.number)\t\(.headRefName)"'
```

The answer `UNKNOWN` means the host is still counting, not that there is no conflict: the call
is repeated after a few seconds. Merging "just in case" is that very quadratic price, and it is
paid for a state that most often is not there.

## A stack without PRs lags silently

The call above knows only open PRs. A stack of local branches has no PRs at all: there is
nothing to ask about it, and it lags whole — many branches, one tip, and that is the one usually
looked at.

The price grows with time. While there are no PRs, main's tip is merged into the lowest branch,
and then each next one absorbs the previous by one merge. After opening, the same edit costs as
many updated PRs as there are branches in the stack — and until then the delivery guard will not
let a single one open: it demands main's tip as an ancestor of the branch.

The sign is read offline, one command per branch:

```bash
for br in $(git branch --format='%(refname:short)' --list '<КЛЮЧ>-*'); do
    git merge-base --is-ancestor origin/<главная> "$br" || echo "$br отстала"
done
```

A stack of forty-one branches lagged eighteen commits at once that way, and not one PR from it
would have opened.

## An index everyone appends to is declared a union

The list of closed works, the spec table of contents, the task list — files where every branch
adds a line at the end. They conflict out of nothing on every branch of the stack, and their
resolution is one: both sides are needed whole. This is declared once, in `.gitattributes`:

```
docs/archive/README.md merge=union
```

The union is set only on indexes where an edit is always an addition. On text that gets
rewritten it leaves both versions in the file.

**The union of sides does not clear the mergeability mark, and main must not be merged in by
it.** The host counts mergeability by its own technique and does not read merge settings: a
branch that touched a unioned index is marked conflicting all the same. A stack asked from it
answers "conflicting" whole, and merging by that answer is the same merging into all branches
as without the union: the section on an actual conflict tells to merge main in on the fact, and
the host names that fact for every branch of the stack. Fifteen PRs stood like that at once in
one session. Checked with one command: the same merge without the driver gives a conflict
marker, with the driver it goes clean — so the mark is held by the index, not by the edit.

**An index every branch of the stack appends to is removed from the stack, not unioned.** The
union fixes the symptom: there is no conflict, there is a mark, merging is still needed. This is
asked before the branches are created: does the index answer a question that a directory walk
does not close. If not — it is removed, and the stack's overlap drops to the real shared files.

## The merge order is set in advance and named to the owner

The order is counted before the PRs open — by who edits which files:

```bash
for b in $(git branch --list '<префикс>-*' --format='%(refname:short)'); do
    git diff --name-only origin/main...$b
done | sort | uniq -c | sort -rn | head
```

Branches editing the same file go one after another: parted by someone else's merges, they will
gather a conflict where in a row there would be none. The order is named to the owner in the PR
body — they press the buttons, and they do not know the branch kinship.

## A wave of branches is checked by a trial merge

A branch lying unmerged next to its neighbours is green on its own: lint, tests, builds and
audits it passes alone. It collides with them on what no check sees on a single branch — the
same next free scenario number, the same newly created file, the same edited mark line. After
the merge the first two are fixed already in main and cost a separate work.

```bash
git fetch origin
git checkout -b probe-merge origin/main
for b in <ветка-1> <ветка-2> <ветка-3>; do git merge --no-edit "origin/$b" || break; done
npm run check:all
git checkout - && git branch -D probe-merge
```

The trial branch is deleted, and the findings and the merge order are written where the epic
plan lives: a trial merge answers "what will collide", it does not replace the handover.

## Common misses

- All PRs opened at once because the branches were ready. A branch's readiness does not say it
  is time to hand it over: as much is handed over as the owner has time to merge.
- Main merged into all open branches after every foreign merge. Half of these merges changed
  nothing: the branches did not conflict, and their mergeability was not asked.
- The state of the stack derived from one's own tree, not asked from the host. Locally merged
  main says nothing about mergeability: between the merge and the owner's look main moves ahead.
- The stack handed over without an order. The owner merges in list order, that is, by number —
  and two branches of one file land on each other exactly when a third stood between them.
- Time spent on PR bodies instead of bringing the first to the merge. The body is needed by
  whoever reads the PR; a PR whose turn comes in a day has no reader today.
