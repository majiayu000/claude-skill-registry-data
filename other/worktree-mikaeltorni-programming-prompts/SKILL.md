---
name: worktree
description: >-
  v1.0.8 — Edit Git projects in a sibling .worktrees project/task checkout,
  commit there, merge each Feature into the live default branch, and reapply
  its consumers. Never push unless requested.
---

# Git worktree isolation and delivery

When isolation applies, use one linked worktree and one matching branch per
project for every Feature, repair, and documentation commit. Do not create a
new worktree or branch for each capability sentence.

## Establish the task checkout

Read the project's `AGENTS.md` and `CLAUDE.md` first. Read-only
inspection may precede isolation; the first repository mutation is
`git worktree add`. Use the existing repository and history, not `git
init` or a history rewrite. Explain the limitation if there is no Git
repository. An explicit request to edit the current checkout overrides
isolation.

Resolve the **physical live checkout** first. If already in a linked
worktree, recover it from `git worktree list --porcelain` and the common
Git directory. Let `PROJECT` be that live checkout's basename, never an
agent, model, account, or linked-worktree name. Use the external sibling
layout:

```text
<project-parent>/.worktrees/<project>/<project>_<type>-<feature>
branch: <type>/<project>_<feature>
```

`TYPE` is a conventional commit type, and `FEATURE` is one descriptive
task slug. Use the **same bytes** for PROJECT, TYPE, and FEATURE in both
names. Pick FEATURE once and use its literal value in the branch as well as
the directory: a leaf ending `_feat-converter` requires branch
`feat/app_converter` for project `app`; `feat/app_temperature-converter`
does not match. The leaf separator after TYPE is `-`, while the branch uses
`/` before PROJECT and `_` before FEATURE. Construct both names from the
same variables below; do not hand-type a different leaf or branch later.
Verify both expanded strings before `git worktree add`. For `/home/mk/projects/widget`, `TYPE=fix` and `FEATURE=parser`
produce `/home/mk/projects/.worktrees/widget/widget_fix-parser` and
`fix/widget_parser`. The store must not sit inside the live repository.
Resolve the store physically before creating it; a symlink must not
redirect it inside the repository. On collision, add a unique suffix
to FEATURE and recompute both names; never reuse or delete another
task's checkout or branch.

```bash
REPO="/home/mk/projects/widget"  # physical live checkout
TYPE="fix"
FEATURE="parser"
PARENT="$(dirname "$REPO")"
PROJECT="$(basename "$REPO")"
WT="$PARENT/.worktrees/$PROJECT/${PROJECT}_${TYPE}-${FEATURE}"
BRANCH="$TYPE/${PROJECT}_${FEATURE}"
git -C "$REPO" worktree add -b "$BRANCH" "$WT"
cd "$WT"
pwd -P
git branch --show-current
```

Compare the printed physical path and branch with `WT` and `BRANCH`
before editing. Keep that same checkout and branch for every Feature,
repair, and documentation commit; a new `docs/...` branch would break
the directory-to-branch identity. Before **every edit and commit**,
verify `pwd -P` is inside the external project group and the current
branch is the task branch. Use the full worktree path for edits,
README files, and scratch output. A shell `cd` does not persist into
later tool calls. Check status afterward and inspect the project group
for misplaced files; recover only this task's files without overwriting
user work in the live checkout. For multiple repositories, establish
this layout separately from each live project.

The external `<project-parent>/.worktrees/<project>/` group holds registered
worktrees only. Put scratch files and recovered drafts inside this task's
checkout under `tmp/`, never in a second unregistered directory or loose file
beside it. If a write accidentally landed in the live checkout, compare it with
the task copy and move only this task's draft into the task checkout (or its
`tmp/` recovery directory), then commit and merge the intended deliverable.
Before delivery, inspect the project group for this task's stray recovery files;
preserve other tasks and user work.

## Deliver each completed Feature

The commits skill owns Feature boundaries. For each completed Feature
or focused repair:

1. Verify and commit in the task worktree. Confirm its `HEAD` advanced
   and the worktree is clean.
2. Confirm the live checkout is on its actual default branch from
   repository metadata or project instructions; preserve unrelated
   live changes. Merge with `git merge --no-ff "$BRANCH"`. Resolve
   conflicts without discarding user work.
3. Confirm the task `HEAD` is an ancestor of live `HEAD` with
   `git merge-base --is-ancestor`, then inspect live status.
4. Reapply through the project's installer, skill selector, or narrow
   reload and verify the consumer and relevant logs. For static
   content without an installed consumer, verify the merged file.
   Follow Linux desktop rules when applicable.

Return to this same worktree for the next Feature. Every later commit,
including a docs-only correction, gets its own merge and reapplication.
Include README and other documentation edits in this same worktree's
commits and merges. Inspect both checkouts for uncommitted source or
documentation; a working live-only README does not complete delivery.
Create documentation in the task worktree from the start. If a README was
accidentally drafted as an untracked file in the live checkout, move that
content into the task worktree and remove only that misplaced draft before
merging. Do not commit the live copy merely to clear a merge obstruction:
the README's introducing commit must originate on the task branch.

Report completion only when the live default branch contains the work
and consumers are current. Never push, publish, add remotes, or rewrite
history without an explicit request.
