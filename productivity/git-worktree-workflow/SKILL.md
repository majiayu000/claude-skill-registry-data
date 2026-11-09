---
name: git-worktree-workflow
description: Use when deciding whether to isolate substantial implementation work in a Git worktree, creating one with worktree-new, or safely closing one with worktree-close. Do not use for read-only research, planning, review, documentation-only changes, trivial edits, or arbitrary branch cleanup.
license: MIT
metadata:
  compatibility: Requires Git, Bash, and the repository's installed worktree-new/worktree-close helpers; ask before using manual Git worktree commands when the helpers are unavailable
---

# Git Worktree Workflow

Use this skill for the lifecycle of an isolated implementation checkout. The
helpers are local filesystem and Git operations; they do not push branches,
create pull requests, or merge code.

## Decide whether to isolate

Use a worktree when the task is substantial enough that keeping the current
checkout untouched is useful, especially for implementation, debugging, or
tests that may run for more than one session.

Do not create one for read-only research, planning, review, documentation-only
changes, or trivial edits unless the user explicitly requests isolation. If it
is unclear whether isolation is worthwhile, ask before creating it.

## Preflight

1. Confirm the current repository, branch, and working-tree state with
   `git status --short --branch`.
2. Confirm `worktree-new` and `worktree-close` resolve with `command -v`. The
   repository linker can place them in `~/.local/bin` or the directory selected
   by `AI_WORKFLOW_BIN_DIR`; make sure that directory is on `PATH`.
3. Choose a full branch name using the repository's naming convention and a
   local base ref that exists. `worktree-new` does not fetch the base ref.
4. Remember that a new worktree starts from the base ref. It does not inherit
   tracked uncommitted changes from the invoking checkout.
5. If `implement-next` will execute the task, complete this worktree setup
   first and invoke `implement-next` only from the selected checkout.
   `implement-next` executes an approved task; it does not create the branch or
   worktree itself.

Never read or print `.env` contents, credentials, private keys, or other
secrets. `worktree-new` copies ignored runtime files from the checkout where it
is invoked, while excluding common dependency, package-manager, cache, and
generated-output directories. Sensitive-looking ignored paths are skipped by
default, but ignored `.env` files are runtime inputs and may be copied without
being read or printed. Before creation, decide whether each local environment
file should be duplicated; exclude unwanted paths with
`WORKTREE_COPY_EXCLUDE` (list each known file or repository-relative prefix).

## Create and use the worktree

Run from the repository checkout whose ignored runtime files should be copied:

```bash
worktree-new BRANCH_NAME [BASE_REF] [START_WINDOW]
worktree-new feature/my-change origin/main agent
```

The default base is `origin/main` and the default start window is `agent`.
Set `AI_WORKFLOW_WORKTREE_ROOT` to an absolute directory before creating a
worktree. The helper errors if it is unset. If the directory does not exist,
the helper asks before creating it. Worktrees are grouped by repository name
and branch beneath that root. After creation, enter the exact path printed by
the helper:

```bash
cd /path/printed/by/worktree-new
git branch --show-current
```

The branch must be unique and the target path must not already exist. Make all
implementation edits in the new checkout. Do not silently switch the original
checkout to the new branch or use the same branch in multiple worktrees.

When a project needs an additional ignored directory excluded from copying, use
colon-separated repository-relative prefixes:

```bash
WORKTREE_COPY_EXCLUDE='local-cache:generated/runtime' \
  worktree-new feature/my-change origin/main agent
```

Paths are normalized and escaping or absolute prefixes are rejected. Use
`WORKTREE_COPY_ALLOW_SENSITIVE=1` only for an explicitly approved need to copy
the helper's sensitive-looking paths; do not set it as a general default.

## Close the worktree

Cleanup is destructive: it removes the worktree directory and local branch.
Only prepare or run it after the branch is merged and the user has approved
that exact cleanup, including the target path, branch, merge ref, and any
remote verification. Run it from outside the target worktree:

```bash
worktree-close /path/printed/by/worktree-new origin/main
```

`worktree-close` refuses to remove the main checkout, a detached or dirty
worktree, a worktree containing ignored files, or a worktree whose branch is
not proven merged. It may refresh a named remote. For squash- or rebase-merged
pull requests, its GitHub CLI fallback requires an authenticated `gh`, binds
the query to the selected remote's repository, and requires the merged PR head
to match the current local branch tip. Before using a remote-qualified merge
ref, inspect the active network policy: cleanup may run `git fetch --prune`,
and failed local ancestry may trigger a read-only `gh pr list` query. Request
the required network approval or escalation before invoking it when needed.

If the task requires creating, editing, commenting on, reviewing, or merging a
GitHub issue or pull request, stop and load `github-cli-workflow`. This skill
only covers local worktree lifecycle and the helper's read-only merge evidence.

Never bypass a refusal with force removal or manual branch deletion. Resolve
the reported condition, re-check the target, and obtain fresh approval if the
cleanup target or merge evidence changes.

## Handoff checklist

- Record the worktree path and branch in the task handoff.
- Run the task's validation from inside the isolated checkout.
- Leave the checkout clean before requesting cleanup.
- Keep cleanup separate from commit, push, PR, merge, or release actions.
