---
name: worksession
description: Use at the start of any work session, especially when multiple Claude Code terminals may be open. Creates an isolated git worktree (or branch fallback), prevents conflicts from parallel sessions. Also use when asked to "start a session", "new branch", or "ws".
---

# Work Session

Isolated git worktrees for parallel Claude Code terminals. One worktree per session, PR at the end.

## Start of Session

Run these steps in order:

1. **Fetch latest and check state:**
   ```
   git fetch origin
   git status
   git branch --show-current
   ```

2. **CRITICAL: Check if another session is already on a ws/ branch:**
   - If already on a `ws/` branch that THIS terminal created: continue working
   - If on a `ws/` branch that ANOTHER terminal created: **DO NOT use it.** Switch to main first.
   - If on `main`: proceed to create a new session
   - Run `git branch` to see all local branches. If there are stale `ws/` branches, delete them.

3. **Ask the user** (one question):
   > "What are you working on? (short description for the branch name)"

4. **Create isolated worktree session:**

   First, try the worktree approach (preferred):
   ```bash
   git checkout main
   git pull origin main
   
   # Create worktree in sibling directory
   BRANCH="ws/<description>-<MMDD>-<HHMM>"
   WORKTREE_DIR="../worktrees/<description>-<MMDD>-<HHMM>"
   
   git worktree add "$WORKTREE_DIR" -b "$BRANCH"
   ```
   
   Then set up the worktree:
   ```bash
   cd "$WORKTREE_DIR"
   
   # Copy environment files (not tracked by git)
   cp "../ZAO OS V1/.env.local" .env.local 2>/dev/null
   
   # Install dependencies (uses npm cache, fast)
   npm install --prefer-offline
   ```

   **NO FALLBACK.** Per doc 459 + ADR-001 + `feedback_workspace_worktrees.md`, the worktree IS the only valid path. If `git worktree add` fails:
   - Diagnose the cause (disk space, permissions, locked branch, missing parent dir)
   - Fix it
   - Retry the worktree command
   - Do NOT fall back to a branch in the shared checkout — branch-only sessions caused multiple wrong-branch incidents (2026-04-19 push to main, 2026-04-20 mid-session branch flips). Doc 459.

   **Better path:** the user should launch new Claude Code sessions via the `zsesh` shell alias (`~/.zshrc`) which runs `claude --worktree ws/<desc>-<stamp>` automatically. Use this skill only when the user is ALREADY inside a Claude session and needs to spin up another worktree from there.

   - Format: `ws/fractal-fixes-0406-1423`
   - Always branch from latest `main`
   - Prefix `ws/` makes session branches identifiable
   - **NEVER reuse another session's branch.** Always create a fresh one.

5. **Board pickup (build-dispatch consumer):** check the cowork tracker for queued build asks and offer to start one:
   ```bash
   ~/bin/zao-tracker search "[build]" --status todo --limit 5 2>/dev/null || true
   ```
   If any `[build]` or P1 rows exist, list them and ask Zaal: "Pick one up this session?" This is the pickup side of ZOE's build-dispatch - Zaal TGs ZOE a build ask, ZOE puts it on the board, the next worksession offers it. Skip silently if the tracker env is not loaded.

6. **Confirm:**
   > "Session `ws/<name>` created at `../worktrees/<name>/`. Ready to work."

## End of Session (PR Workflow)

When the user says "ship", "done", "pr", "wrap up", or work is complete:

1. Stage and commit any remaining changes
2. **Merge main into your branch before pushing** (prevents CI failures from stale base):
   ```bash
   git fetch origin main
   git merge origin/main --no-edit
   # If conflicts, resolve them before pushing
   ```
3. **CRITICAL: Check if branch already has a merged PR before pushing:**
   ```bash
   MERGED=$(gh pr list --state merged --head "ws/<name>" --json number --jq '.[0].number' 2>/dev/null)
   if [ -n "$MERGED" ] && [ "$MERGED" != "null" ]; then
     echo "WARNING: PR #$MERGED already merged for this branch!"
     echo "Creating new branch instead..."
     # Cherry-pick commits to a new branch from latest main
     git checkout main && git pull origin main
     NEW_BRANCH="ws/<name>-2"
     git checkout -b "$NEW_BRANCH"
     git cherry-pick <commits>
     git push -u origin "$NEW_BRANCH"
     gh pr create  # new PR
   fi
   ```
4. Push the session branch: `git push -u origin ws/<name>`
5. Create PR to `main` using `gh pr create`
6. Report the PR URL
7. **Clean up after merge:**
   - Delete the remote branch after PR is merged: `git push origin --delete ws/<name>`
   - Delete the local branch: `git branch -D ws/<name>`
   - Remove the worktree: `git worktree remove "../worktrees/<name>"`
   
   Do NOT auto-delete - the user merges PRs themselves. Just remind them:
   > "PR created. After you merge, I'll clean up the branch."

## Rules

- **NEVER reuse another terminal's branch.** Each session gets a FRESH branch from main.
- **Never commit directly to `main`** from a work session
- **Never push to someone else's branch** - always your own `ws/` branch
- **Always pull main before branching** - stale bases cause merge conflicts
- **Always merge main before creating PRs** - prevents CI failures from being behind
- If the branch already exists on remote, append a counter: `ws/fix-0406-1423-2`
- **Always create a PR** as the finishing step - Zaal merges himself
- **Always clean up** stale local and remote branches at start/end of sessions
- Keep worktree count to 3-5 max (each needs ~1.2GB for node_modules)
- Use `git worktree list` to see active worktrees

## Branch Hygiene (Run Periodically)

When starting a session, clean up stale branches:
```bash
# Delete local branches that are already merged to main
git branch --merged main | grep -v main | xargs git branch -d

# Check for remote branches with no unmerged work
git fetch --prune
```

## When NOT to Use

- Quick one-line fixes where the user says "just push to main"
- When the user explicitly says to work on an existing branch
- Research-only sessions (no code changes - no isolation needed)

## Worktree Directory Layout

```
~/Documents/
  ZAO OS V1/                          # Main checkout (stays on main)
  worktrees/
    feature-auth-0411-1000/           # Isolated session
    fix-search-0411-1430/             # Another session
```
