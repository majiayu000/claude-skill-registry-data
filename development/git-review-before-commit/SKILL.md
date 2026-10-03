---
name: git-review-before-commit
description: "Review the working tree before committing to Git. Triggers on: the user asks to commit or push, a large task is complete, or a PR is about to be created. Rules: ensure `svelte-check` passes (see the verify-svelte-check skill), use `git status` to inspect all files, use `git diff` for staged and unstaged changes, classify pre-existing versus new changes, match the repo style (see `git log --oneline -10`), do not stage irrelevant files, do not commit secrets, do not amend, and do not force-push."
---

# Skill: Git review before commit

## Pre-commit checklist

Run these in parallel where independent:

```
git status
git diff --staged
git diff
git log --oneline -10
```

## Steps

### 1. Run `svelte-check` first

See `verify-svelte-check` skill. **Never** commit before type-check passes.

### 2. `git status` — full inventory

- Confirm which files are staged vs unstaged
- Spot any file NOT related to the task — investigate or revert
- Spot any unexpected untracked file (test scaffolds, temp files, `.local` files, dumps) — delete or `.gitignore`, don't commit

### 3. `git diff --staged` + `git diff`

Read all changes line by line. Classify each block:
- **Intended**: change addresses the user's request
- **Side-effect from refactor**: not directly requested but follows from the intended change
- **Pre-existing**: file was modified before this session — confirm not accidentally staged
- **Stranger**: change that doesn't fit either category. STOP, investigate.

For each stranger block:
- Revert with `git checkout -- file` if it's a scratch or accidental edit
- If legitimate, mention in commit message body

### 4. Stage intentionally

Use `git add <specific-files>` rather than `git add .` / `git add -A`. Separate un-related changes into separate commits.

### 5. Inspect recent commits for style

```
git log --oneline -10
```

Sample repo style (from this codebase):
- Short imperative subject (~50 chars)
- Lowercase first letter
- No conventional-commits like `feat:` / `fix:` unless the repo uses them — verify against git log
- Multi-paragraph body if change has nuance, blank line between subject and body

Match style. Don't introduce a "Co-authored-by … Claude / model-name" footer unless the repo convention shows one in git log.

### 6. Compose commit message

Single-line example:
```
remove dead exports and unused props from admin form components
```

Multi-line example (only if nuance can't fit on one line):
```
remove dead exports and unused props from admin form components

- drop `placeholder`/`hint` props from FormField (no call site passes them)
- drop `confirmLabel`/`cancelLabel` props from ConfirmDialog (always default)
- drop `variant` prop from Header (always 'public')
- revert recent bind:value refactor per AGENTS.md bug #4
```

### 7. Commit (separate from push)

```
git commit -m "..."
```

Do NOT push unless the user explicitly asks.

### 8. (Optional) Make a PR with `gh`

Only when user asks. Before opening:
- `git log --oneline origin/main..HEAD` to list commits in PR
- Confirm the diff still builds: `pnpm build`
- Open with `gh pr create --base main --title "..." --body "..."`
- Return the PR URL

## Forbidden actions

Per repo rules + safe defaults:
- `git commit --amend` on already-pushed commits
- `git push --force` / `--force-with-lease` without explicit user request
- `git config` modification
- Empty commits
- Skipping hooks (--no-verify)
- Interactive `-i` flag

## Secret hygiene

Inspect the diff for:
- API keys, tokens, JWT, secrets in env-style
- Absolute paths exposing username (`/Users/<name>/` / `C:\Users\...`) in source beyond what's already in repo
- Database credentials, AWS keys, private IPs
- `.env` files (they should be gitignored — verify)

If found, **don't commit**. Strip and ask user.

## Final summary

After commit, report:

```
Committed: <hash-snip> "<subject>"
Files changed: <count>
Status: clean (or: working tree clean)
```

If asked to push:
```
Pushed to <remote>:<branch>
Result: <hash-snip>..<hash-snip>  <branch> -> origin/<branch>
```