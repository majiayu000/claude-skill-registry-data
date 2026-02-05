---
name: scode-graphite
description: For any project that contains a .git/.graphite_repo_config file, this skill should be used for creating PRs, managing git branches and otherwise all non-read-only git operations.
---

# Graphite Workflow

Use Graphite (`gt`) instead of raw git commands for branch and PR management.

## Stacked PRs/branches

Graphite supports the concept of stacked changes where one depends on another. The typical workflow is something like:

- make changes to files
- gt create -u -m 'fixed bar'
- gt submit -p -m # auto-publish (-p)
- make more changes
- gt create -u -m 'fixed baz'
- gt submit -p

At that point there are two changes pending. Depending on timing and PR success, 'fixed bar' and 'fixed baz' may both be
open still. Graphite will arrange for them to be merged automatically and in order when ready (due to the use of -m).
The -u causes gt create to create the branch with a commit containing updates to already-tracked files (-u is not
mandatory though).

At any time, `gt sync --all -f && git fetch --prune` can be used to refresh the local repo with the latest remote
changes driven by Graphite (including e.g. when Graphite rebased a PR relative to master after closing preceding diff,
or a PR has been closed and the branch deleted).

## Core Commands

- `gt log` - See current stacks/branches and their status.
- `gt create -m "message"` - Create a new branch stacked on current branch
- `gt submit -p` - Push current stack and create/update PRs
  - use `gt submit -p -m` when asked to create an auto-merging PR
- `gt sync --all -f && git fetch --prune` - Sync with trunk and restack branches (the git fetch with prune accounts for
  merged PRs and deleted branches).
- `gt checkout <branch>` - Switch to a branch
- `gt log short` - View the current stack
- `gt bottom` / `gt top` - Navigate to bottom/top of stack
- `gt up` / `gt down` - Navigate within stack
- `gt modify -u` - Modify the current branch's contents to include updates to already tracked files. Use this by default
  if you have not created new files in the session.
- `gt add <filename>` - Adds (starts tracking) files. Use this to start tracking files you have created, so that a
  subsequent `gt modify -u` picks it up. Always use this and never use `gt modify -a`, to avoid adding untracked
  unignored files the user may have in their repo.

If you need to do something with gt/git that isn't covered above, abort and tell the user why. They can choose what to
do including improving this skill.

If you are unsure what to do, err on the side of caution and tell the user about the confusion and ask for next steps
(which also gives the user a chance to improve the skill). Do not proceed when unsure without confirmation.

## Workflow

By default, never automatically create a PR or branch unless the user asks for it.

When the user asks to 'create a PR' or 'make a PR', assume the intention is to create a separate change and PR rather
than amending the existing commit. This applies regardless of whether the current branch is main or another branch.

When the user asks to 'update the PR' or 'amend the PR', assume they are asking for whatever currently active branch to
be amended (by amending the commit) and the PR updated using `gt submit`.

After being asked to create or update the PR and doing so, stop doing so for further updates unless explicitly requested
again.

1. Start from trunk (`main` or `master`). It's also fine to start from an existing branch and stack work on top of it.
   Use `gt log` to see what the current state of the repo is. Assume that when initiating work, the user is in whatever
   base state they want. So if they are in a branch, assume the intent is to stack changes on top of it (when requesting
   that a branch or PR is created; when just changing code the user may still be just intending on amending the current
   one).
2. Create stacked branches with `gt create -m "description"` (first line will become PR title, rest PR description)
3. When making changes after already being in a branch with an existing commit, use `gt modify -u` to amend the commit
   to contain the latest changes (when the user indicates to update the PR).
4. Run `gt sync --all -f && git fetch --prune` to ensure we're up-to-date with remote.
5. Run all tests/format checks/links etc (as requisted in CLAUDE.md/AGENTS.md). This should always be done before
   creating a PR or updating an PR. Fix any issues.
6. Submit the stack with `gt submit -p` (or `gt submit -p -m` if user asked for auto-merging PR). This includes after
   amending a commit.
7. If conflicts occurr during `gt sync --all -f`, bail out and ask the user to fix it.

NEVER pass the `-m` flag ('merge when ready') to `gt submit` unless the user explicitly requests an auto-merging PR.

## PR Creation

When submitting PRs with `gt submit`:

- Use `-p` to publish PRs immediately.
- Use `--no-edit` to skip editing PR descriptions
- Graphite auto-generates PR titles from branch names
- Graphite picks up the PR title and description from the commit. Make sure the commit has the right first-line (title)
  and remaining body within the guidelines below, prior to submitting.
- When a PR has been updated or created, give the user both the link to the Graphite view of the PR as well as the
  GitHub view of the PR.

## Creation of multiple PRs in a sequence

When asked to create multiple PRs, assume the intent is to create a stack of PRs (because the changes may be dependent
on each other). Do NOT switch back to main in between each change.

### Commit Message Style

Assume the first line in the commit message is the title of the PR.

For the first line, be very terse and to the point. Examples:

- "cargo update" (instead of some sentance talking about upgrading depencencies)
- "Fix bug: --foo command did not foo"
- "Add ability to bar the baz."

For the body, be more verbose and detailed when called for. For example if the change is non-obvious, explain _why_ the
change was made. Do not add low value boiler plate like listing upgraded packages from a cargo update.

Err on the side of terseness. The human will edit as needed.

### PR Description Template

The PR description should always be the same as the commit message except the first line (which is the PR title).
