---
name: improve
description: Review and improve code — fix bugs, harden security, optimize performance, improve readability and maintainability
argument-hint: "[cycles=1]"
---

# Improve

Iterative improvement cycles that review code across multiple dimensions and fix everything found. Goes beyond bug-fixing — actively improves performance, security, readability, and maintainability.

**This is not just a review. It finds issues AND fixes them.**

## Arguments

- `$ARGUMENTS` - Number of improvement cycles (default: 1)

Parse cycles from arguments:
- `/improve` -> 1 cycle
- `/improve 3` -> 3 cycles

## Workflow

For each cycle (1 to N):

### Step 1: Gather Context

Collect the base branch, the commit history, the changed files and the full diff in one Bash call:

```bash
BASE_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
: "${BASE_BRANCH:?no base branch found: ask the user which branch to compare against}"
git fetch -q origin "$BASE_BRANCH"
echo "BASE_BRANCH=$BASE_BRANCH"
git log --oneline "origin/$BASE_BRANCH"..HEAD
git diff --stat "origin/$BASE_BRANCH"...HEAD
git diff "origin/$BASE_BRANCH"...HEAD
```

### Step 2: Parallel Review (6 dimensions)

Launch six **reviewer** agents in parallel, each focused on a different dimension. Every agent receives the full diff and file list from Step 1.

**Agent A — Security:**
- Injection vulnerabilities (SQL, command, XSS, CSRF)
- Authentication and authorization gaps
- Data exposure risks (logging secrets, overly broad API responses)
- Resource leaks and denial-of-service vectors
- Missing input validation at system boundaries

**Agent B — Performance:**
- N+1 queries, missing indexes, unnecessary round-trips
- Redundant allocations, unbounded collections, missing pagination
- Blocking I/O in async paths, missing caching opportunities
- Algorithmic complexity (O(n^2) or worse that could be O(n) or O(1))
- Memory-inefficient patterns (copying where referencing suffices)

**Agent C — Correctness:**
- Logic errors and unhandled edge cases
- Error handling gaps (swallowed exceptions, missing fallbacks)
- Race conditions and concurrency issues
- Off-by-one errors, null/nil handling, type coercion bugs

**Agent D — Readability:**
- Unclear naming (variables, functions, classes that don't express intent)
- Complex control flow that could be simplified (deep nesting, long methods)
- Misleading comments, or comments that narrate what the code already says
- Magic numbers and strings that should be constants/enums
- Dead code, unused imports, commented-out blocks

**Agent E — Maintainability:**
- DRY violations (duplicated logic across files)
- Tight coupling between modules that should be independent
- Missing abstractions or unnecessary abstractions
- Inconsistent patterns within the same codebase
- Public API surface that's too broad (exposing internals)

**Agent F — Testing:**
- Missing test coverage for new/changed code paths
- Inadequate edge case testing
- Flaky test patterns (timing dependencies, shared state)
- Tests that test the mock instead of the code
- Missing regression tests for bug fixes

Each agent outputs a prioritized list of issues with `file:line` references and severity (critical / warning / suggestion). For performance and readability issues, include the **improvement** not just the problem — describe what the better version looks like.

### Step 3: Merge & Prioritize

Combine findings from all six agents into a single prioritized list. Remove duplicates. Group by severity:
1. Critical (bugs, security vulnerabilities, data loss risks)
2. Warnings (performance problems, maintainability issues, missing tests)
3. Suggestions (readability improvements, style, minor optimizations)

### Step 4: Parallel Fixes (Consolidation Pattern)

Partition the issue list into groups by area/theme. Use the **consolidation pattern** — launch each fix group as a parallel agent in its own worktree. Agents can freely edit overlapping files; the consolidator handles merges.

Before launching them, record BASE: the SHA `git rev-parse HEAD` prints in this checkout. Give each group's `architect` agent the checkout's absolute path as the repo, BASE, its own branch and an absolute worktree path (explicit worktree mode: the architect follows its Worktree BASE protocol). Prompt the consolidator with this checkout as the integration worktree, BASE, and merge as the integration mode.

**Per worktree agent:**
1. Verify each assigned issue is valid (not a false positive)
2. Fix confirmed issues — don't just patch, *improve*:
   - For performance issues: implement the faster approach, not a band-aid
   - For readability issues: restructure the code, don't just add comments
   - For maintainability issues: extract proper abstractions, remove duplication
   - For security issues: implement defense in depth, not a single check
3. Ensure fixes don't introduce regressions
4. Commit all changes before finishing

**After all worktree agents complete**, launch the **consolidator** agent (`subagent_type: "consolidator"`) to merge all branches and resolve any overlapping edits.

### Step 5: Verify

Launch a **verifier** agent (`subagent_type: "verifier"`) in post-verification mode to confirm tests pass and lint is clean. If it fails, fix and re-verify.

### Step 6: Commit

After all fixes pass verification, delegate to `skills:commit`:

```
Skill(skill="skills:commit", args="refactor(<scope>): improve [summary of what was improved]")
```

Use `refactor` for structural improvements, `fix` for bug fixes, `perf` for performance — or `skills:commit-all` if the changes span multiple types.

### Step 7: Next Cycle (if cycles > 1)

If more cycles remain, return to Step 1 with a raised severity floor:
- **Cycle 1**: fix critical + warning + suggestion
- **Cycle 2**: fix critical + warning only
- **Cycle 3+**: fix critical only

Track what was already addressed to avoid re-fixing. This naturally converges — each cycle finds fewer issues as the bar rises.

## Cycle Summary

After all cycles, report:

```
## Improvement Summary

### Cycle 1
- Security: X issues found, Y fixed
- Performance: X issues found, Y fixed
- Correctness: X issues found, Y fixed
- Readability: X issues found, Y fixed
- Maintainability: X issues found, Y fixed
- Testing: X issues found, Y fixed
- Remaining: Z

### Final State
- Total issues fixed: N
- Remaining issues: M (with explanation if any)
- Commits created: K
```

## Exit Conditions

Stop early if:
- No issues found (code is clean)
- Same issue persists after a fix attempt (escalate to user)
- Only minor suggestions remain (no critical/warnings)

## Test Failure Policy

There is no such thing as a "pre-existing" test failure. If any test fails, fix it. The task always completes with completely passing tests.

## Notes

- Each cycle raises the severity floor so iteration naturally converges in 2-3 passes
- Don't fix the same issue twice — track what's been addressed
