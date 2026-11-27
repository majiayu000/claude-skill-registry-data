---
name: sync-repos
description: Use when the user asks to sync, update or pull main across their repos, to catch local checkouts up with origin, or runs /sync-repos. Fast-forward only; never discards local work.
---

# Sync repos

Brings every configured local checkout up to date with `origin/main`, safely. It only ever fast-forwards: it never rebases, resets, force-checks-out, or drops a stash, so local edits are never lost.

## Config

The repo list lives in `~/.claude/sync-repos.json`. Start from `sync-repos.example.json` next to this file:

```json
{"repos": ["~/Projects/<repo-one>", "~/Projects/<repo-two>"]}
```

If the file is missing, say so, point at the example, and stop. Expand `~` yourself; skip (and flag) any path that is not a git repo.

## Steps

Run each command as its own Bash call with `git -C <repo>`, one repo at a time.

1. Record the starting point: current branch (`git -C <repo> branch --show-current`), `git -C <repo> rev-parse --short HEAD`, and `git -C <repo> status --porcelain` (non-empty means a dirty tree).
2. `git -C <repo> fetch origin`.
3. Not on main: check whether the branch's PR was merged with `gh pr view <branch> --repo <owner/repo> --json state -q .state` (run from inside the repo if the repo name is unknown). If it says `MERGED` and the tree is clean, `git -C <repo> checkout main`. Otherwise stay on the branch and flag it.
4. On main: `git -C <repo> merge --ff-only origin/main`. If it fails (local commits on main, or a dirty file in the way), leave everything as it is and flag `ff failed`.
5. Note what came in: compare old and new sha with `git -C <repo> diff --name-only <old>..<new>` and flag lock file changes (`*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Gemfile.lock`) and new migrations (added files under any `migrations/` or `db/migrate/` directory, `--diff-filter=A`).

## Output

One table, nothing else unless something needs the user:

| repo | old sha | new sha | flags |
|---|---|---|---|
| repo-one | a1b2c3d | e4f5a6b | lock file changed, migrations added |
| repo-two | 1234567 | 1234567 | not on main (feature-x, PR open) |

Flags: `lock file changed`, `migrations added`, `dirty tree`, `not on main`, `ff failed`, `not a git repo`. Under the table, one line per flag the user should act on (for example "migrations added in repo-one: run them before starting the app").

## Never

- `git rebase`, `git reset`, `git checkout -- .`, `git stash drop`, `git clean`, or `git pull` with a merge commit.
- Switching branches on a dirty tree.
- Pushing anything.
