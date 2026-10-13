---
name: co
description: "Commit changes with logical grouping and conventional messages, optionally push. Use when the user says 'commit', 'commits', 'save changes', or '/co', or when finished work needs committing. `/co auto` / `/co forbid` switch the session's auto-commit mode."
argument-hint: "[push] [auto|forbid] [--no-push] [--push-auto]"
---

# co — commit utility

## Arguments

Parse `$ARGUMENTS` case-insensitively, hyphens optional:

- `push` — also push after committing.
- `auto` — for the rest of the session, commit after each meaningful unit of work (feature, fix, refactor) without asking. Then commit whatever is pending now.
- `forbid` — for the rest of the session, make NO commits unless the user explicitly asks (an explicit `/co` still commits, and does not lift the mode). For try-and-error development. Set the mode, confirm in one line, and stop — commit nothing now.
- `--no-push` / `--nopush` — invoke `/push-forbid` before committing.
- `--push-auto` / `--pushauto` / `--push-ok` / `--pushok` — invoke `/push-auto` before committing.

`auto` and `forbid` are explicit user choices: apply them immediately, no confirmation question. They are session instructions like `/push-auto` / `/push-forbid`, not stored state, and are independent of the push mode. Under `auto`, still ask when unsure whether a specific file belongs in a commit.

## Execution — keep the diff out of the main context

The commit work runs in a Haiku subagent so the main session sees only a summary, never the git diff, file-selection reasoning, or message drafting.

### Step 0: Pre-check

```bash
git status --porcelain
git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "unknown"
```

- Nothing to commit, nothing ahead → report "Nothing to commit or push." and stop.
- Nothing to commit, `push` given → no subagent. Ahead: push per the Push rules below. `unknown` (no upstream): `git push -u origin $(git branch --show-current)`. Report and stop.
- Nothing to commit, N ahead, no `push` → report "Nothing to commit. N commit(s) ahead of remote — use `/co push` to push." and stop.
- Something to commit → Attempt 1.

### Attempt 1: Haiku subagent

Spawn an Agent with `model: "haiku"`. Its prompt is the Instructions section below plus the repo path, whether `push` was requested, and the session's Co-Authored-By line if the session specifies one. On success, relay its report and stop.

### Attempt 2: direct execution (last resort)

Only if the subagent failed (partial commits, conflict, any error): run `git status` and `git log --oneline` to see where it stopped, then carry out the Instructions for the remainder in this session.

## Instructions

1. **Inspect** — `git status`, `git diff --stat`.
2. **Keep junk out via `.gitignore`.** If the status shows files that must never be committed — dependencies (`node_modules/`), build output (`dist/`, `build/`, `.next/`, `out/`), logs, temp/swap files, OS files (`.DS_Store`, `Thumbs.db`), caches, coverage, env files (`.env*`), secrets (`*.pem`, `*.key`, `credentials.json`) — add the missing patterns to `.gitignore` (create it if the project has none), and `git reset HEAD <file>` anything already staged. If such a file is already in history, tell the user. IDE dirs and lockfiles are context-dependent: follow the repo's existing practice.
3. **Stray images are the exception — NEVER add image globs (`*.png` etc.) to `.gitignore`**; that can silently exclude real assets. Images in the repo root or non-content dirs are usually headless-browser or conversation leftovers: delete them if no longer needed, otherwise move them out: `LOGDIR=$(node $HOME/.claude/scripts/get-logdir.js) && mkdir -p "$LOGDIR" && mv <file> "$LOGDIR/"`.
4. **Stage selectively** — never a blind `git add .`. Only intentional, meaningful changes; skip auto-generated noise. Unsure about a file → ask.
5. **Group** — one commit when changes are small and related; separate commits for unrelated concerns (docs vs code, feature vs fix, refactor vs new behavior, config vs source). Prefer small focused commits.
6. **Commit** — conventional style (`feat:`, `fix:`, `docs:`, `refactor:`, …), HEREDOC message, ending with the Co-Authored-By line you were given, else `Co-Authored-By: Claude <noreply@anthropic.com>`:

   ```bash
   git commit -m "$(cat <<'EOF'
   feat: message here

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

7. **Push** — only if `push` was requested; see Push rules.
8. **Verify** — `git status` is clean; show `git log --oneline -n <commits made>`.

Never `git commit --amend` and never force-push without explicit user permission — always make new commits.

## Push rules

- `git rev-list --count @{upstream}..HEAD`: 0 → nothing to push. `unknown` → `git push -u origin $(git branch --show-current)`.
- Otherwise check whether the branch is actually behind **before pulling anything**: `git fetch && git rev-list --count HEAD..@{upstream}`.
- **0 (not behind) → `git push` directly. Do NOT pull.** A pull is a no-op at best; with `--rebase` it replays every local commit, flattening any merge commit on the branch and re-applying its contents as fresh work — manufacturing conflicts (typically lockfiles) where there was nothing to reconcile.
- Non-zero → `git pull --no-rebase` (regular merge; never rebase), then `git push`.

### Conflict during the pull

First re-check the behind-count. If it is 0 the pull should never have run: `git merge --abort`, plain `git push`, and treat the conflict as an artifact.

- **Haiku subagent, or a child agent in a team**: do NOT resolve. `git merge --abort`, then report the branch name and conflict details to the caller/manager, who has the full picture.
- **Main session, standalone**: `git merge --abort`, inspect incoming work with `git log --oneline HEAD..@{upstream}`, pull again to see the conflicts. Trivial (whitespace, non-overlapping) → resolve, commit, push. Overlapping logic or unclear intent → abort again and resolve deliberately with full knowledge of what was implemented before retrying.
