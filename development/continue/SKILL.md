---
name: continue
description: Pick up unfinished work from where the last session left off
argument-hint: "[task description or context]"
---

# Continue

Reconstruct context from the last session and continue unfinished work. Use when a previous session ended mid-task due to context limits, interruption, or session timeout.

**DO NOT STOP UNTIL THE RECONSTRUCTED TASK IS COMPLETE.**

## Arguments

- `$ARGUMENTS` - Optional context about what was being done. If empty, reconstruct from git state.

## Phase 1: Reconstruct Context (Parallel)

Launch **four agents** in parallel to gather all state simultaneously:

**Agent 1 — Git State:**
```bash
git status
git branch --show-current
git stash list
BASE_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
echo "BASE_BRANCH=$BASE_BRANCH"
if [ -n "$BASE_BRANCH" ]; then
  git fetch -q origin "$BASE_BRANCH"
  git log --oneline "origin/$BASE_BRANCH"..HEAD 2>/dev/null || git log --oneline -10
  git diff --stat "origin/$BASE_BRANCH"...HEAD 2>/dev/null
else
  git log --oneline -10
fi
```

**Agent 2 — Uncommitted Work:**
```bash
git diff --stat
git diff --cached --stat
git diff
git diff --cached
```

**Agent 3 — Recent Changes:**
```bash
git log --oneline -10 --all
```

**Agent 4 — Failing State:**

Run the project's test/build/lint commands to find what's currently broken:
```bash
if [ -f 'composer.json' ]; then composer test 2>&1 | tail -30; fi
if [ -f 'build.gradle' ] || [ -f 'build.gradle.kts' ]; then ./gradlew test 2>&1 | tail -30; fi
if [ -f 'package.json' ]; then npm test 2>&1 | tail -30; fi
if [ -f 'Cargo.toml' ]; then cargo test 2>&1 | tail -30; fi
if [ -f 'go.mod' ]; then go test ./... 2>&1 | tail -30; fi
```

## Phase 2: Diagnose What's Unfinished

From Phase 1 results, determine:

1. **Branch state** — Are we on a feature branch? How far ahead of base?
2. **Uncommitted changes** — Is there work in progress that needs committing?
3. **Stashed work** — Is there stashed work that needs popping?
4. **Test/build state** — Are tests passing? Is the build clean?
5. **Incomplete patterns** — Are there TODO markers, placeholder code, empty test bodies, or unimplemented methods?

Search for incomplete markers:
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX\|PLACEHOLDER\|NotImplemented\|throw.*not.*implement" --include="*.php" --include="*.kt" --include="*.java" --include="*.ts" --include="*.js" --include="*.rs" --include="*.go" --include="*.py" . 2>/dev/null | grep -v node_modules | grep -v vendor | head -20
```

If `$ARGUMENTS` is provided, use it to narrow focus. Otherwise, infer the task from:
- Branch name (e.g., `feat/add-auth` tells you what was being built)
- Commit messages (what's already been done)
- Uncommitted changes (what's in progress)
- Failing tests (what's broken)

## Phase 3: Plan Remaining Work

Based on the diagnosis, create a plan:

1. List what's already done (from commits and code state)
2. List what's remaining (from failures, TODOs, uncommitted work)
3. Prioritize: fix broken things first, then complete unfinished work

## Phase 4: Execute

Based on complexity of remaining work:

**If simple (1-2 files, clear fix):**
Fix directly, verify, commit.

**If moderate (multiple files, one domain):**
Launch an **architect** agent to complete the work, then verify.

**If complex (cross-cutting, multiple domains):**
Invoke the **consolidation** skill (`Skill(skill="skills:consolidation", args="...")`) with the remaining work plan. You become the conductor and dispatch the planner → verifier → parallel architects → consolidator → reviewer → verifier cycle.

## Phase 5: Verify & Commit

1. Run full test suite — all tests must pass
2. Run lint — must be clean
3. Run build — must succeed
4. Commit any remaining changes:

```
Skill(skill="skills:commit-all")
```

## Phase 6: Report

```
## Continuation Summary

- **Picked up from:** <branch name, last commit>
- **State found:** <clean/dirty/failing>
- **Work completed:**
  - <item 1>
  - <item 2>
- **Tests:** pass
- **Build:** pass
- **Commits created:** N
```

## Hard Rules

1. **DO NOT ASK what was being done** if it can be inferred from git state — just continue
2. **DO NOT START OVER** — build on existing work, don't redo it
3. **FIX EVERYTHING** — if tests are failing, fix them regardless of whether they're "yours"
4. **COMMIT INCREMENTALLY** — don't accumulate a huge uncommitted diff
5. **VERIFY BEFORE REPORTING** — run tests/build/lint before claiming completion
