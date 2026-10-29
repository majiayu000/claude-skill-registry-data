---
name: using-git-spice
description: Stack-aware Git workflows. Use when creating or adopting stacked branches, changing stack commits or dependencies, rebasing onto trunk, updating dependent PRs, splitting work into a stack, or choosing git-spice scope.
---

# Using git-spice

Use `git-spice`; `gs` is Ghostscript.

## Read the stack

A tracked branch records its base. Trunk is the integration branch. Choose the
smallest scope that covers the requested work:

| Scope | Branches affected |
| --- | --- |
| `branch` | Current branch |
| `upstack` | Current branch and descendants |
| `downstack` | Current branch and ancestors |
| `stack` | All connected branches |
| `repo` | All tracked branches |

`(needs restack)` marks a stale branch. Start by inspecting the working tree and
current branch; preserve unrelated changes, stage only intended files, and run
branch-sensitive commands from a checked-out branch.

Check whether git-spice has initialized the repository before any other
git-spice command:

```bash
git show-ref --verify --quiet refs/spice/data
```

If initialized, inspect with `git-spice log short` or
`git-spice log short --all`. Use `git-spice log long` to include each branch's
commits. The log tree shows branch base and position; there is no `branch info`
command.

To adopt an untracked Orca worktree branch against its known base, run:

```bash
git-spice branch track --base=<base> --no-prompt
```

Continue only when the log shows the intended stack and bases.

## Initialize when needed

If `refs/spice/data` is absent, resolve trunk and remote from Git state or ask
the user, then initialize explicitly:

```bash
git-spice repo init --trunk=<trunk> --remote=<remote> --no-prompt
```

`--reset` is destructive. Run it only when the user requested that reset and
the target is verified. Initialization is complete when git-spice commands
work and the log shows the intended trunk.

## Create and change branches

Config prepends `prateek/` to names passed to `branch create`. Remove that
prefix from the requested name and pass the bare name:

```bash
git add <specific-files>
git-spice branch create <bare-name> -m "<message>" --no-prompt
```

With nothing staged, add `--no-commit`. Use `-t <base>` when another branch is
the intended base. Split and rename commands require full `prateek/...` names.

Commit on the layer that owns the change so descendants remain aligned:

```bash
git add <specific-files>
git-spice commit create -m "<message>" --no-prompt
```

Before amending, verify the checked-out branch owns its top commit:

```bash
git add <specific-files>
git-spice commit amend --no-edit --no-prompt
```

For a lower branch held in another worktree, amend in that worktree, then
restack skipped descendants from the worktrees that hold them. Use
`commit fixup` only when no worktree holds the owning branch. The change is
complete when the intended commit is on its owning layer and the stack log
shows no unexplained stale descendants.

For adoption chains, dependency moves, insertion, fixups, splitting,
squashing, folding, renaming, deletion, or editor-driven operations, read
[stack surgery](references/stack-surgery.md) before changing stack shape.

When designing layers for work that should become a stack, read
[stack design](references/stack-design.md) first.

## Submit only when asked

Submission changes remote state. Submit only on the user's explicit request.
Read [change requests](references/change-requests.md) for authentication,
previews, submission metadata, merging, and remote failure recovery.

Run one submit at a time. Before submitting, and when a submit runs past about
60 seconds, read [slow pushes](references/change-requests.md#slow-pushes).

Submit an unsubmitted base first. From a higher layer, submit bottom-up:

```bash
git-spice downstack submit --fill --no-prompt
```

Use `--update-only` when updating existing change requests. Config creates
drafts; use `--no-draft` when the user requested ready-for-review status.
Preview with `--dry-run`, inspect the result, then run the same command without
it only when the preview matches the request.

If a branch needs restacking or is outdated, restack the intended scope, verify
the marker is gone, then retry. `--force` force-pushes and bypasses safety
checks; use it only with explicit user intent, a verified remote, and a pinned
base. Submission is complete when the requested change requests reflect the
intended stack and status.

## Sync after trunk changes

After trunk changes or a parent merges, sync forge state and inspect the stack:

```bash
git-spice repo sync --no-prompt
git-spice log short
```

Sync advances trunk even when another worktree holds it; direct
`git fetch origin master:master` cannot. Config restacks descendants of
branches sync merges or deletes. A trunk-only advance still needs a restack:

```bash
git-spice upstack restack --no-prompt
git-spice stack restack --no-prompt
```

Sync skips branches held by another worktree. Restack skipped branches from
the worktrees that hold them. For a squash-merge SHA mismatch, confirm the
merge, delete the merged branch, then restack descendants. Sync is complete
when the log reflects the updated trunk and has no unexplained stale branches.

## Continue or abort a conflict

When an operation stops on conflicts, resolve them, stage only resolved files,
and continue through git-spice:

```bash
git add <resolved-files>
git-spice rebase continue --no-edit --no-prompt
```

Use `git-spice rebase abort` when the user wants to abandon the resolution.
The operation is complete when git-spice finishes and the log shows the
intended branch relationships.

Run git-spice separately from long tests. The requested work is done when the
operation succeeded, only intended changes were included, and no unexplained
stale branches remain.

## Operating rules

- In headless runs, supply required values and `--no-prompt`; suppress editors
  with `-m`, `--no-edit`, or `--fill`.
- On tracked branches, use git-spice for commits, restacks, `onto`, and submits
  so it can keep branch relationships and descendants aligned.
- Keep local commits separate from remote submission. Submit or merge only
  when requested.
- Keep hooks and safety checks enabled unless the user requests a bypass.
- For an ambiguous request such as “clean up this stack,” inspect and ask
  before restacking, deleting, submitting, or rewriting history.
- Run delete scopes or `repo init --reset` only after the user requests that
  destructive result and you verify the targets.
