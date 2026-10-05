---
name: git-worktrees
description: "Use when starting feature work that needs isolation from the current workspace, before executing an implementation plan, or when creating, listing, merging, or cleaning up git worktrees. Covers directory selection and gitignore safety, creation with project setup and a clean test baseline, merging back to main, and teardown of stale worktrees and branches."
---

# Git Worktrees

Worktrees create isolated workspaces that share one repository, so you can work on several branches
at once without switching. This skill covers the full lifecycle: choose a location → create → set up
and verify → merge back → tear down.

**Core principle:** systematic directory selection + safety verification = reliable isolation.

## 1. Choose the worktree directory

Follow this priority order. Do not assume a location.

```bash
ls -d .worktrees 2>/dev/null     # preferred (hidden, project-local)
ls -d worktrees 2>/dev/null      # alternative
```

1. **An existing directory wins.** If both exist, use `.worktrees/`.
2. **Otherwise check the project's agent instructions:**
   `grep -i "worktree.*director" GEMINI.md 2>/dev/null` — if a preference is stated, use it without asking.
3. **Otherwise ask**, offering both conventions:
   - `.worktrees/` — project-local and hidden
   - a sibling `../<repo>_worktrees/` — keeps the repo directory clean

Resolve the sibling path with:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"
WT_BASE="$(dirname "$REPO_ROOT")/${REPO_NAME}_worktrees"
```

## 2. Verify safety before creating

For a **project-local** directory (`.worktrees/` or `worktrees/`), confirm it is ignored first:

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If it is not ignored:** add it to `.gitignore` and commit that change before proceeding.
Otherwise worktree contents get tracked and pollute `git status`.

A sibling directory outside the repo needs no such check.

## 3. Create the worktree

```bash
# New branch
git worktree add "<path>/<name>" -b "<branch>" main

# Existing branch
git worktree add "<path>/<name>" "<branch>"
```

A `wt/<name>` branch prefix keeps worktree branches easy to spot, though any convention works as
long as the project is consistent.

## 4. Set up and verify a clean baseline

Auto-detect the project type rather than hardcoding commands:

```bash
[ -f package.json ]     && npm install
[ -f Cargo.toml ]       && cargo build
[ -f pyproject.toml ]   && uv sync
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f go.mod ]           && go mod download
```

Then run the project's test command. **If tests fail, report the failures and ask** whether to
proceed — a dirty baseline makes new bugs indistinguishable from pre-existing ones. If they pass,
report the path, the test count, and that the worktree is ready.

## 5. Merge back to main

```bash
git checkout main
git merge <branch> --no-edit
```

**On conflicts:** read both sides and keep all non-overlapping changes. Where two branches touched
different sections of the same document, combine both sides rather than picking one.

**After merging**, either tear down (below) or reset the worktree to keep working in it:

```bash
git -C "<path>/<name>" reset --hard main
```

## 6. List and tear down

```bash
git worktree list
```

Use `scripts/wt_cleanup.sh` — the manual sequence is error-prone (stale directories, leftover
metadata, force-removal needed for untracked files):

```bash
bash scripts/wt_cleanup.sh <name>                   # keep the branch
bash scripts/wt_cleanup.sh <name> --delete-branch   # after a merge
```

Manual equivalent:

1. `git worktree remove --force "<path>/<name>"` — force is needed if untracked files exist
2. `rm -rf "<path>/<name>"` if a stale directory remains
3. `git worktree prune`
4. `git branch -D <branch>` — only if merged

## Optional: paired terminal sessions

If your setup uses a terminal multiplexer, pairing each worktree with a session keeps parallel work
navigable. With `tmx2` and a `ge_<name>` session prefix:

```bash
tmx2 new-session -d -s "ge_<name>" -c "<path>/<name>"   # create, alongside step 3
tmx2 ls                                                  # list sessions
tmx2 kill-session -t "ge_<name>"                        # kill, before step 6
```

Cross-reference `git worktree list` against `tmx2 ls` to spot orphaned sessions (session alive,
worktree gone) and unpaired worktrees. Adapt to `tmux`/`screen` as needed — this section is a
convenience, not part of the core lifecycle.

## Common pitfalls

| Problem | Cause | Fix |
|---|---|---|
| `already exists` on worktree add | Stale directory from a previous removal | `rm -rf` the directory, `git worktree prune`, retry |
| `branch already exists` on `-b` | Branch survived cleanup | `git branch -D <branch>`, retry |
| `contains modified or untracked files` | Normal — worktrees accumulate artifacts | Use `--force` on `git worktree remove` |
| Worktree contents show in `git status` | Directory was never gitignored | Add to `.gitignore` and commit; see step 2 |
| Can't tell new bugs from old | Skipped the baseline test run | Always verify a clean baseline in step 4 |
| Session dies after worktree removal | Removing the directory kills the session's cwd | Recreate the session, or kill it first |

## Red flags

**Never** create a project-local worktree without verifying it is ignored, skip the baseline test
run, proceed past failing tests without asking, or assume a directory location when it is ambiguous.

## Integration

| Skill | Relationship |
|---|---|
| `executing-plans`, `subagent-driven-development` | The work that happens inside the worktree |
| `finishing-a-development-branch` | Completes the work before teardown |
| `writing-plans` | Produces the plan the worktree isolates work for |
