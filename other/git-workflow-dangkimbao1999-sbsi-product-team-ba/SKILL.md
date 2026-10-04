---
name: git-workflow
description: Git branching, worktree isolation, commit safety, commit mechanism, and PR workflow. Use when committing, creating worktrees/branches, pushing, creating PRs, rebasing, or merging.
---

# Git Workflow — Detailed Procedure

## 1. Start from a worktree, never primary main

```
EnterWorktree(name: "feat-my-feature")
```

This creates a branch named `worktree-feat-my-feature`; the
`worktree-post-enter.sh` hook renames it to `feat/my-feature` automatically.
Naming convention: `feat/`, `fix/`, `chore/`, `refactor/`, `docs/`, `test/`,
`ci/`.

<If your project has a setup script (dependency install, .env generation),
name it here and note it should run right after EnterWorktree.>

## 2. Make your changes

Follow `.claude/rules/tdd.md` — RED before GREEN. Follow
`.claude/rules/working-style.md` — surgical, minimal changes.

## 3. Typecheck before every commit

<Fill in your project's actual typecheck/lint command.>

## 4. Commit — the 5-step mechanism

1. `git status` — see all untracked/modified files.
2. `git diff` (staged + unstaged) — see what will actually be committed.
3. `git log --oneline -10` — match the repo's existing commit message style.
4. Stage **specific files by name** (never `git add -A` / `git add .`).
5. Commit with a message that explains *why*, not just *what*:

```bash
git commit -m "$(cat <<'EOF2'
<one-line summary of why this change>

Author: Claude Code <noreply@anthropic.com>
EOF2
)"
```

Never use `--no-verify`. If a pre-commit hook fails, fix the underlying
issue and retry — don't skip the hook.

## 5. Rebase on origin/main before pushing

```bash
git fetch origin main
git rebase origin/main
```

Resolve conflicts by understanding both sides' intent — never blindly
`--theirs` or `--ours` without reading the conflicting hunks.

## 6. Push and open a PR — draft by default

```bash
git push -u origin <branch>
gh pr create --draft --title "..." --body "..."
```

The `pr-draft-default.sh` hook blocks non-draft `gh pr create`. See
`.claude/rules/git-workflow.md` for the promotion-to-ready flow
(`gh pr ready`, requires explicit human consent).

## 7. After merge — tear down immediately

```
ExitWorktree(action: "remove", discard_changes: true)
```

`discard_changes: true` is correct for squash-merges (the default): the
merge rewrote history, so the local branch's HEAD sha no longer matches
what's on `main`, even though the content is identical. Use `false` only if
your project merges via a plain merge commit (branch HEAD is preserved).

Never run raw `git worktree remove` or `git worktree add` — always the
`EnterWorktree` / `ExitWorktree` tools, so hook-driven session state (serial
worktree/PR tracking) stays consistent.

## Conflict recovery

If `ExitWorktree` refuses because of "unmerged commits" and you know the PR
was squash-merged, that's the `discard_changes` flag you need — see step 7.
If you're not sure the PR actually merged, run `gh pr view --json state`
first before forcing anything.
