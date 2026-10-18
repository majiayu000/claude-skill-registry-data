---
name: worktree-isolation-pattern
last_updated: 2026-05-17
description: "The exact git worktree create, detect, and clean pattern for Beamix workers: detect-or-create from main-repo-root, child worktree commands, branch naming conventions (feat/fix/chore), atomic commits, and .worktrees/ gitignore enforcement."
tags: [git, beamix-specific, workflow, workers]
source: beamix-authored 2026-05-16
risk: low
---

# Worktree Isolation Pattern

## Quick reference

> Every code worker creates a fresh worktree under `MAIN_REPO/.worktrees/<slug>`. Never edit main repo. Never edit another worker's worktree.

## When to use

- Any code worker (backend-engineer, frontend-engineer, database-engineer, etc.) starting a new task
- CTO creating a worktree on behalf of a worker via Task
- Debugging "file not found" or "wrong branch" errors in a worker session
- Authoring a new worker agent file that needs the worktree operating procedure

## When NOT to use

- For non-code workers (technical-writer, researcher — no worktree needed)
- For QA-Lead (QA-Lead reads, does not create worktrees)

## Step 1: Detect current context

Run this before any `git worktree add` command. You may already be inside a worktree.

```bash
git worktree list
# Output example when INSIDE a worktree:
# /Users/adamks/VibeCoding/Beamix                      abc1234 [main]
# /Users/adamks/VibeCoding/Beamix/.worktrees/ceo-1-xxx  def5678 [ceo-1-xxx]

# The FIRST line is always the main repo root
# If there is more than one line, you are inside a worktree
pwd  # confirm current directory
```

## Step 2: Get the main repo root

```bash
MAIN_REPO=$(git worktree list | head -1 | awk '{print $1}')
echo "Main repo: $MAIN_REPO"
```

## Step 3: Create the task worktree from main repo root

Never run `git worktree add` from inside a worktree path. Always reference `$MAIN_REPO`.

```bash
TASK_SLUG="scan-rate-limit"  # matches Linear ticket slug
BRANCH_PREFIX="feat"          # or "fix" or "chore"

git -C "$MAIN_REPO" worktree add \
  "$MAIN_REPO/.worktrees/$TASK_SLUG" \
  -b "$BRANCH_PREFIX/$TASK_SLUG"

# Verify
ls "$MAIN_REPO/.worktrees/$TASK_SLUG"
```

## Branch naming

```
feat/<task-slug>     — new feature or addition
fix/<task-slug>      — bug fix
chore/<task-slug>    — cleanup, dependency update, refactoring
test/<task-slug>     — test-only changes (test-engineer, qa-engineer)
```

Slug format: lowercase, hyphens, matches the Linear ticket slug. Example: `feat/scan-rate-limit` for BMX-101.

## Step 4: Work in the task worktree

All file reads and writes happen inside `$MAIN_REPO/.worktrees/$TASK_SLUG/`, not in the main repo.

```bash
cd "$MAIN_REPO/.worktrees/$TASK_SLUG"

# Now implement the task
# Edit files, run type checks, etc.

# Type check (per-file — faster than full monorepo check)
pnpm -F @beamix/web exec tsc --noEmit apps/web/src/app/api/scan/route.ts

# Lint
pnpm -F @beamix/web lint --max-warnings 0
```

## Step 5: Atomic conventional commits

One logical change per commit. Follow Conventional Commits format.

```bash
git add apps/web/src/app/api/scan/start/route.ts
git commit -m "feat(api): add rate-limit middleware to free scan endpoint (BMX-101)"
```

Scopes: `api`, `ui`, `db`, `auth`, `billing`, `agent`, `infra`, `test`

Multi-file changes: one commit if the changes are logically inseparable. Split if independently revertable.

## Step 6: Run diagnostics before return

```bash
# TypeScript diagnostics on ALL edited files
# (mcp__ide__getDiagnostics if available, otherwise tsc per file)

# Run relevant tests
pnpm -F @beamix/web test -- --testPathPattern="scan"

# If tests don't exist for the changed area, flag in return JSON
```

## Step 7: Return JSON and signal completion

Do NOT clean up the worktree yourself. CTO/QA-Lead needs to inspect it. Return:

```json
{
  "status": "COMPLETE",
  "agent": "backend-engineer",
  "branch": "feat/scan-rate-limit",
  "worktree": "/Users/adamks/VibeCoding/Beamix/.worktrees/scan-rate-limit",
  "files_changed": [
    "apps/web/src/app/api/scan/start/route.ts",
    "apps/web/src/lib/rate-limit.ts"
  ],
  "commits": ["feat(api): add rate-limit middleware (BMX-101)"],
  "summary": "Added per-IP rate limiting to /api/scan/start. Free tier capped at 3 scans per 24h via Redis-backed middleware.",
  "decisions_made": [],
  "blockers": [],
  "needs_followup": []
}
```

## Cleanup (after QA-Lead PASS and merge)

CTO or devops-engineer cleans the worktree after the PR is merged:

```bash
git -C "$MAIN_REPO" worktree remove "$MAIN_REPO/.worktrees/$TASK_SLUG"
git -C "$MAIN_REPO" branch -d "feat/$TASK_SLUG"
```

## .worktrees/ gitignore

Confirm this line is in `$MAIN_REPO/.gitignore`:

```
.worktrees/
```

If it is missing, add it before creating any worktree. Worktrees should never be committed.

## Parallel workers (CTO dispatch)

When CTO spawns multiple workers in parallel (Task calls), each gets its own worktree:

```
.worktrees/scan-rate-limit/    ← backend-engineer
.worktrees/scan-rate-limit-test/  ← test-engineer
```

Workers never share a worktree. If two workers need to see each other's output, CTO mediates — passes the prior worker's return JSON as input to the next worker's brief.

## Auto-fix rules (worker deviation rules)

Workers handle these without returning BLOCKED:
1. **TypeScript type errors** in files they authored — fix immediately
2. **Missing imports** — auto-add
3. **Unused imports** — auto-remove

Everything else (architectural mismatch, missing spec clarity, scope expansion) → return `PARTIAL` with `needs_followup`. CTO decides.

## See also

- `using-git-worktrees` — [[using-git-worktrees]]
- `qa-gate-protocol` — [[qa-gate-protocol]]
- `finishing-a-development-branch` — [[finishing-a-development-branch]]

## Anti-patterns

- Running `git worktree add` from inside a worktree path (creates nested worktree, confuses git)
- Committing to `main` or another worker's branch
- Using `git add -A` without reviewing the diff (can accidentally stage unrelated changes)
- Cleaning the worktree before QA-Lead has reviewed it
- Not returning `worktree` path in JSON (QA-Lead cannot inspect without it)
- Multiple workers sharing one worktree (state interference)
- Task slug not matching Linear ticket slug (makes correlation hard)
