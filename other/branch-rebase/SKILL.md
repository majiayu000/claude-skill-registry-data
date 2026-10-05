---
name: branch-rebase
category: developer-experience
description: >
  Safely rebase the current branch onto its upstream target, auto-resolving trivial
  conflicts and prompting for complex ones. Use when the user says "rebase", "rebase onto
  main", "update my branch", "sync with baseline", "catch up with main", or invokes /branch-
  rebase.
codex-short-description: "Safely rebase the current branch onto its upstream target, auto-resolving trivial conflicts"
related-skills:
  - branch-resolve-conflicts
loop-eligible: false

compatibility: claude-code codex opencode
---

# Branch Rebase

Rebase the current feature branch onto its upstream target with automatic resolution of trivial conflicts.

## Invocation

```
/rebase-branch [target]
```

- `target` — branch to rebase onto. Defaults to the first of `baseline`, `main`, `master` that exists.

## Workflow

Follow every step in order. Do not skip steps. Do not push at the end.

### 1. Validate environment

```bash
git rev-parse --is-inside-work-tree
```

If not a git repo, stop and tell the user.

### 2. Detect branches

```bash
CURRENT=$(git branch --show-current)
```

If `CURRENT` is empty (detached HEAD), stop: "You are in detached HEAD state. Check out a branch first."

If a target argument was provided, use it. Otherwise detect the target:

```bash
for candidate in baseline main master; do
  if git show-ref --verify --quiet "refs/heads/$candidate" || \
     git show-ref --verify --quiet "refs/remotes/origin/$candidate"; then
    TARGET=$candidate
    break
  fi
done
```

If no target found, stop: "Could not find baseline, main, or master. Specify a target branch."

If `CURRENT` equals `TARGET`, stop: "You are already on the target branch."

### 3. Check for uncommitted changes

```bash
git status --porcelain
```

If output is non-empty, **stop immediately** and tell the user:

> You have uncommitted changes. Please commit or stash them before rebasing.

List the dirty files so they can decide. Do not proceed.

### 4. Update the target branch

```bash
git checkout $TARGET
git pull --ff-only
```

If the pull fails (e.g. diverged local target), warn the user and ask whether to continue or abort.

### 5. Return to feature branch and rebase

```bash
git checkout $CURRENT
git rebase $TARGET
```

If the rebase completes cleanly, skip to step 7.

### 6. Resolve conflicts

If the rebase stops with conflicts, read [CONFLICTS.md](CONFLICTS.md): version-only and
different-version changelog conflicts auto-resolve; everything else goes to `/branch-resolve-conflicts`
(or `git rebase --abort` if the user prefers). Repeat for each conflicting commit.

### 7. Post-rebase version bump and changelog

If the repo has a version manifest (`build.gradle(.kts)`, `pom.xml`, `package.json`, `*.csproj`) or a
changelog, read [VERSIONING.md](VERSIONING.md). The branch must end with a version distinct from the
target's and its own changelog section; any fixup is a separate `chore:` commit at the tip. Otherwise
skip to step 8.

### 8. Report success

Tell the user:

> Rebase complete. `{CURRENT}` is now based on `{TARGET}`.

If a version bump or changelog update was made, list exactly what changed:
> - Version bumped: `{OLD}` → `{NEW}` in `build.gradle`
> - New changelog section added for `{NEW}`

Then:
> **Your branch has not been pushed.** When you're ready:
> ```
> git push --force-with-lease
> ```

List any files that were auto-resolved during conflict resolution so the user can verify.

## Important rules

- **Never push.** The user decides when and how to push.
- **Never use `--force`.** Only suggest `--force-with-lease` in the final message.
- **Never amend or squash** commits during this workflow.
- If anything unexpected happens (network errors, lock files, hook failures), stop and report rather than retrying destructively.
- Prefer `git rebase --abort` over leaving the repo in a broken state.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/branch-rebase.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
