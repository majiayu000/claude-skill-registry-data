---
name: git-commit
description: >
  Draft conventional commit messages, commit local changes, push to main on origin,
  merge branches into main, and clean/prune git worktrees and stale local branches.
  Use when the user asks to commit, push to main, merge and commit, clean worktrees,
  prune worktrees, delete merged/stale branches, or mentions "/commit", "git commit",
  or "ship to main".
argument-hint: "[message|commit|push-main|merge|worktrees|branches] [paths...]"
user-invocable: true
allowed-tools: Bash, Read, Grep
---

# Git Commit (Project Aegis)

End-to-end git commit workflow for **cmano-clone**. Trunk is **`main`** (see [`.graphite_repo_config`](../../.graphite_repo_config)).

**Result vocabulary (use in operator output):** `READY` (draft ready), `COMPLETE` (commit/push/cleanup done), `FAIL` (hook/push/conflict stopped), `BLOCKED` (needs explicit user decision, e.g. force-push or dirty worktree loss).

## When to use which path

| User intent | Path |
|-------------|------|
| Draft or refine a message only | [Phase 1](#phase-1--commit-message) |
| Commit locally (any branch) | [Phase 2](#phase-2--local-commit) |
| Land on remote `main` (direct trunk) | [Phase 3](#phase-3--commit-and-push-main) |
| Merge a branch into `main`, then push | [Phase 4](#phase-4--merge-and-commit) |
| Remove stale worktrees / branches | [Phase 5](#phase-5--worktree-and-branch-cleanup) |

**Graphite stacks:** If the current branch is Graphite-tracked (`gt log short` shows it in a stack), use `gt submit` / `gt sync` instead of raw `git push` — see [graphite-github-substitute-plan.md](../../docs/engineering/graphite-github-substitute-plan.md). This skill's push-to-main path is for **direct trunk work on `main`** or when the user explicitly requests trunk push.

## Hard rules

- **Only commit or push when the user explicitly asks** (this skill invocation counts as explicit).
- **NEVER** update git config.
- **NEVER** `--force`, `--hard`, or force-push to `main`/`master` unless the user explicitly requests it — warn first; verdict **BLOCKED** until they confirm.
- **NEVER** skip hooks (`--no-verify`, `--no-gpg-sign`) unless the user explicitly requests it.
- **NEVER** commit secrets (`.env`, credentials, keys, tokens).
- **NEVER** use interactive git (`-i` flags: rebase -i, add -i).
- **NEVER** amend unless: user asked to amend, HEAD commit is yours and unpushed, and hook did not reject the prior commit.
- If a hook rejects a commit, **fix and create a new commit** — do not amend a failed commit; report **FAIL**.
- Before commit/submit on code changes: run GitNexus `detect_changes()` (see [AGENTS.md](../../AGENTS.md)).
- Before running `git commit` / `git push` / destructive worktree remove: present the planned message, staged paths (or branch list), and ask **"May I write this commit / proceed?"** when the user has not already given a clear execute intent (e.g. bare `/git-commit` with uncommitted work = execute intent; ambiguous multi-path cleanup = ask first).

---

## Phase 0 — Parse intent

Map the user phrase to a mode from `argument-hint`:

| Mode | Triggers |
|------|----------|
| `message` | "draft message", "suggest commit message" |
| `commit` | "commit", "/commit", "/git-commit" |
| `push-main` | "push main", "ship to main" |
| `merge` | "merge and commit", "merge into main" |
| `worktrees` | "clean worktrees", "prune worktrees" |
| `branches` | "delete merged branches", "prune stale branches" |

If intent is ambiguous, list the modes and ask which to run. Do not default to force-delete.

---

## Phase 1 — Commit message

Analyze changes, then produce a conventional commit message (do not commit unless the user also asked to commit).

### Gather context (run in parallel)

```bash
git status
git diff
git diff --staged
git log -5 --oneline
```

Use staged diff when something is staged; otherwise use working-tree diff.

### Message format

```
<type>[optional scope]: <description>

[optional body — why, not what]

[optional footer: Closes #123, BREAKING CHANGE: ...]
```

| Type | Use for |
|------|---------|
| `feat` | New behavior |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Tests only |
| `refactor` | Restructure, no behavior change |
| `perf` | Performance |
| `build` / `ci` | Build or CI |
| `chore` | Maintenance |
| `qa` | QA gauntlet / test-ops artifacts |

**Style:** imperative, present tense, ≤72 chars in subject, one logical change per commit.

### Scope hints (this repo)

- `data` — ProjectAegis.Data / catalog
- `sim` — ProjectAegis.Sim
- `delegation` — ProjectAegis.Delegation*
- `unity` — unity/ProjectAegis
- `production` — production/ sprint docs
- `gauntlet` / `qa` — production/qa/gauntlet
- `ci` — Buildkite / GitHub Actions

Present the draft message. Verdict **READY** when the message is drafted and no commit was requested.

---

## Phase 2 — Local commit

### Checklist

```
- [ ] git status + diff reviewed
- [ ] No secrets in diff
- [ ] GitNexus detect_changes() run (code changes)
- [ ] Message drafted (Phase 1)
- [ ] User asked to commit (or skill invoked for commit)
```

### Stage and commit

```bash
# Stage explicit paths only — avoid git add -A unless user wants everything
git add path/to/changed/files

git commit -m "$(cat <<'EOF'
type(scope): short description

Optional body explaining why.
EOF
)"
```

Verify:

```bash
git status
git log -1 --stat
```

Verdict **COMPLETE** on success; **FAIL** if hooks reject (then fix and new commit).

---

## Phase 3 — Commit and push main

Direct trunk landing: work happens on **`main`**, commit locally, push to **`origin/main`**.

### Preconditions

```bash
git branch --show-current    # must be main (or user approved committing on main)
git fetch origin
git status                   # warn if behind/ahead of origin/main
```

If not on `main`:

```bash
git checkout main
git pull --ff-only origin main   # stop if merge required and user didn't ask to merge
```

### Workflow

1. Complete [Phase 2](#phase-2--local-commit) on `main`.
2. Push:

```bash
git push origin main
```

3. Confirm:

```bash
git status
git log origin/main -1 --oneline
```

**Do not** `git push --force` to `main`. If push is rejected (non-fast-forward), stop with **FAIL** / **BLOCKED** — user must merge/rebase explicitly.

---

## Phase 4 — Merge and commit

Merge another branch into `main`, commit the merge, push to remote.

### Identify branches

```bash
git branch --show-current
git branch -a
git log --oneline main..OTHER_BRANCH
git log --oneline OTHER_BRANCH..main
```

Confirm with the user which branch merges into `main` if ambiguous.

### Merge workflow

```bash
git fetch origin
git checkout main
git pull --ff-only origin main

git merge OTHER_BRANCH -m "$(cat <<'EOF'
merge(scope): integrate OTHER_BRANCH into main

Brief summary of what the merged work delivers.
EOF
)"
```

If merge conflicts:

1. List conflicted files: `git diff --name-only --diff-filter=U`
2. Resolve in working tree.
3. `git add` resolved files.
4. `git commit` (no `-i`); reuse merge message if Git opened one.

Push after successful merge:

```bash
git push origin main
```

### Graphite alternative

When merging stack work prefer Graphite merge order (bottom PR first) and `gt sync` after merge — not manual merge — unless user explicitly wants a local merge commit.

Verdict **COMPLETE** after push; **BLOCKED** if conflicts need user choices.

---

## Phase 5 — Worktree and branch cleanup

Project worktrees often live under **`.worktrees/`**.

### Inspect

```bash
git worktree list
git branch -vv
git fetch origin --prune
```

### Safe worktree prune (recommended order)

```bash
git worktree prune

# Remove a specific secondary worktree (never the primary checkout)
git worktree remove .worktrees/NAME
# git worktree remove --force ...  # only if user confirms dirty tree loss
```

### Local branch cleanup (merged / stale)

Safe delete criteria (all must hold as applicable):

1. Not `main` / `master` / current branch.
2. **Merged** into `origin/main` (`git branch --merged origin/main`), **or**
3. Upstream is **gone**, **or**
4. Upstream exists and local is **0 ahead** (no unique commits), **or**
5. No upstream and tip is ancestor of current/`origin/main`.

```bash
git branch -d branch/name          # prefer -d
# git branch -D branch/name        # only if classified stale and -d refuses; confirm with user if unsure
```

**Never** remove the primary checkout worktree (repo root).

Bulk cleanup: process nested + standalone trees if both exist; do not run concurrent writers on the same `.git`.

Verdict **COMPLETE** when only intended branches/worktrees remain; list what was kept and why.

---

## Quick reference

| Task | Command / section |
|------|-------------------|
| Draft message | Phase 1 — parallel `status`, `diff`, `log` |
| Commit | Phase 2 — HEREDOC `git commit -m` |
| Push main | Phase 3 — `git push origin main` |
| Merge to main | Phase 4 |
| Worktrees | Phase 5 — `git worktree remove` + `prune` |
| Stale branches | Phase 5 — merged / gone / 0-ahead only |
| Graphite PR | `gt submit --stack --no-interactive` |

---

## Follow-Up Actions

After a successful commit or submit:

- `/sprint-status` — confirm sprint story status if production docs changed
- Graphite: `gt submit` / `gt sync` for stacked work (prefer over raw push)
- GitNexus: re-run `detect_changes` / re-analyze if code landed
- `/skill-test static git-commit` — re-validate this skill after edits
- Next skill with static failures: `/skill-test static all` then `/skill-improve [name]`

---

## Related docs

- [Graphite workflow](../../docs/engineering/graphite-github-substitute-plan.md)
- [AGENTS.md — GitNexus detect_changes](../../AGENTS.md)
