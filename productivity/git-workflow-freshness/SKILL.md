---
name: git-workflow-freshness
kind: pattern
rule: git-workflow
description: Pattern of rule git-workflow. Load before a push, when taking a task and after every known merge — reading all your open PRs at once, telling lag apart from a conflict in files, checking the local head against the hosting.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-freshness.md · d4d8e242afb8 · правится надстройкой, не здесь -->

# Freshness of open PRs

Pattern of the rule `git-workflow`. What must be true — the law
`docs/constitution/delivery.md`. Resolving one conflict — pattern `git-workflow-merge`, a chain
of branches from one base — `git-workflow-stack`.

## When to use

Three places, and in each the reading is mandatory:

- before a push — main's tip may have moved while the work went on;
- when taking a new task — the earlier PRs stayed open and will not remind of themselves;
- after every merge that became known — it made all the others lag at once.

## What is read

By one command over all one's own open PRs, not the one whose branch is checked out now:

```bash
/opt/homebrew/bin/gh pr list --author '<машинная запись>' --state open \
    --json number,headRefName,isDraft,mergeable,mergeStateStatus,statusCheckRollup
```

| Field                | What it says                                                                      |
| -------------------- | --------------------------------------------------------------------------------- |
| `mergeable`          | `MERGEABLE` — the button can be pressed; `CONFLICTING` — it cannot; `UNKNOWN` — not counted yet |
| `mergeStateStatus`   | `BEHIND` — lags behind main; `DIRTY` — a dispute in files; `BLOCKED` — awaits review |
| `isDraft`            | a draft: the host locks the merge button whatever the run's colour                |
| `statusCheckRollup`  | the run on the tip: an empty list means no run at all, not "green"                |

`UNKNOWN` means "not counted yet" and reads as "ask again in a few seconds", not as "no
conflicts".

## A dispute in files is told apart from lag

The host's mark says one thing — "cannot press". What exactly to fix is answered by a tree
merge, and it answers offline:

```bash
git fetch origin
git merge-tree "$(git merge-base origin/main <ветка>)" origin/main <ветка> | grep -c '^<<<<<<<'
```

Zero — the branch merely lags, and merging main in cures it. Above zero — a dispute in files,
and each is resolved by file kind: pattern `git-workflow-merge`.

## What is done with what was found

| Found                                  | What is done                                                       |
| -------------------------------------- | ------------------------------------------------------------------ |
| lagging, no dispute                    | main is merged into the branch and pushed in the same turn         |
| a dispute in files                     | resolution by file kind, then a push                               |
| no run on the tip                      | the tip is rerun or waited for — neither one has a colour          |
| a draft with a green run               | the draft is lifted — its merge button is locked                   |
| the PR opened by a person, not by the machine | it can no longer get a reviewer: it is created anew by the machine account |

Within one branch the order is one: merge main in → run the gate set → push → reread the state
from the host. Rereading is part of the work, not a report on it.

## The local tip is checked against the one on the host

A branch caught up in the working tree and not pushed does not count as work: a person sees the
old state.

```bash
git rev-parse HEAD
/opt/homebrew/bin/gh pr view <номер> --json headRefOid --jq .headRefOid
```

Diverged — the push is not done, and that is the first thing fixed.

## Common misses

- The PR state read from memory of the previous turn: between turns a person merged a neighbouring work.
- `UNKNOWN` read as "no conflicts" — the host was still counting.
- The PR of the current branch was read, and the abandoned ones stayed lagging: all one's own open ones are asked.
- Main merged in the working tree and not pushed: from outside that is "nothing done".
- Lag was cured by resolving a conflict: there was no dispute in files at all, a merge would have sufficed.
- A dispute resolved by choosing one side whole: the file kind decides the technique, and its sides differ.
- The catch-up round started at a person's shout, not on its own: by that minute all PRs had already lagged.
