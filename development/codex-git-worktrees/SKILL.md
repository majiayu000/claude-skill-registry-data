---
name: codex-git-worktrees
description: Use when implementation needs isolation from the current workspace; creates git worktrees with safe directory selection and baseline verification.
load_priority: on-demand
---

## TL;DR
Create isolated workspace: detect directory → verify gitignored → create worktree → install deps → verify tests pass. Use `$worktree` or `$isolate` to activate. Pairs with `$finish` for cleanup.

# Git Worktrees

## Activation

1. Activate on `$codex-git-worktrees`, `$worktree`, or `$isolate`.
2. Activate before executing implementation plans that need isolation.
3. Activate when `codex-subagent-execution` starts (recommended prereq).
4. Activate when user asks for parallel development branches.

**Announce at start:** "I'm using codex-git-worktrees to set up an isolated workspace."

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
# Check in priority order (cross-platform)
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative

# PowerShell (Windows)
Test-Path .worktrees
Test-Path worktrees
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check Project Config

```bash
# Check .codex/context/genome.md or project README for worktree preferences
grep -i "worktree" .codex/context/genome.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### 3. Ask User

If no directory exists and no config preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. worktrees/ (project-local, visible)

Which would you prefer?
```

## Safety Verification

### For Project-Local Directories

**MUST verify directory is ignored before creating worktree:**

```bash
# Bash/macOS/Linux
git check-ignore -q .worktrees 2>/dev/null
echo $?  # 0 = ignored (safe), 1 = NOT ignored (fix needed)
```

```powershell
# PowerShell (Windows)
git check-ignore -q .worktrees 2>$null
$LASTEXITCODE  # 0 = ignored (safe), 1 = NOT ignored (fix needed)
```

**If NOT ignored:**

Fix immediately:
1. Add to `.gitignore`
2. Commit the change
3. Proceed with worktree creation

```bash
# Bash
echo ".worktrees/" >> .gitignore
git add .gitignore
git commit -m "chore: add .worktrees to gitignore"
```

```powershell
# PowerShell
Add-Content .gitignore ".worktrees/"
git add .gitignore
git commit -m "chore: add .worktrees to gitignore"
```

**Why critical:** Prevents accidentally committing worktree contents to repository.

## Creation Steps

### 1. Detect Project

```bash
# Bash
project=$(basename "$(git rev-parse --show-toplevel)")
echo "Project: $project"
```

```powershell
# PowerShell
$project = Split-Path (git rev-parse --show-toplevel) -Leaf
Write-Output "Project: $project"
```

### 2. Create Worktree

```bash
# Create worktree with new branch
git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"
cd ".worktrees/$BRANCH_NAME"
```

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then pip install -e .; fi
```

```powershell
# PowerShell equivalents
if (Test-Path package.json) { npm install }
if (Test-Path requirements.txt) { pip install -r requirements.txt }
if (Test-Path pyproject.toml) { pip install -e . }
if (Test-Path Cargo.toml) { cargo build }
if (Test-Path go.mod) { go mod download }
if (Test-Path *.csproj) { dotnet restore }
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean:

```bash
# Use project-appropriate command
npm test / python -m pytest / cargo test / go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.
**If tests pass:** Report ready.

### 5. Report Location

```
Worktree ready at <full-path>
Branch: <branch-name>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Finishing a Branch

When work is complete, present options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
```

### Option 1: Merge Locally
```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
# Verify tests
git branch -d <feature-branch>
git worktree remove <worktree-path>
```

### Option 2: Push and Create PR
```bash
git push -u origin <feature-branch>
# Create PR via gh/git platform
```
Keep worktree for follow-up work.

### Option 3: Keep As-Is
Report: "Branch preserved at <path>."

### Option 4: Discard
**Confirm first** with typed confirmation.
```bash
git checkout <base-branch>
git branch -D <feature-branch>
git worktree remove <worktree-path>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check config → Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Skip ignore verification | Worktree tracked in git | Always `git check-ignore` first |
| Assume directory location | Inconsistency with project | Follow priority: existing > config > ask |
| Proceed with failing tests | Can't distinguish new vs old bugs | Report failures, get permission |
| Hardcode setup commands | Breaks on different projects | Auto-detect from project files |
| No test baseline | Don't know if worktree is clean | Always run tests after setup |

## Red Flags — Never Do

- Create worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip git config check

## CodexAI Integration

### With Subagent Execution
```
$worktree → create isolated branch → $sdd → execute plan → $finish
```

### With Git Autopilot
```bash
# Auto-commit within worktree
python codex-git-autopilot/scripts/auto_commit.py --project-root <worktree-path>
```

### With Quality Gate
```bash
# Verify before merging back
python codex-execution-quality-gate/scripts/auto_gate.py --mode full --project-root <worktree-path>
```

## Related Skills

- **`codex-subagent-execution`** — Execute plan tasks within isolated worktree
- **`codex-git-autopilot`** — Commit automation within worktree
- **`codex-execution-quality-gate`** — Verify before merge/PR
- **`codex-plan-writer`** — Creates the plan to execute in worktree
