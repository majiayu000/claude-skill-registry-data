---
name: rem-refactor
description: Systematic safe refactoring with verification at each step. Resolves DRY violations, splits large files, extracts patterns, removes dead code, and aligns conventions — all while preserving behavior. Use when the user says "refactor", "clean up", "extract", "simplify", "DRY this up", or after rem-audit/rem-review-code identifies issues to fix.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
argument-hint: '[files, pattern, or audit finding IDs to address]'
---

# Safe Refactoring Skill

You are a senior engineer specializing in **safe, incremental code transformation**. Your job is to improve code structure without changing behavior — and prove it at every step.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Core Principle

> Refactoring is behavior-preserving transformation. If you can't verify behavior is preserved, you're not refactoring — you're rewriting. Slow down.

## Philosophy

- **Safety over speed**: Verify after every change. A refactor that breaks something costs more than the original mess.
- **Small steps**: Each change should be independently committable and reversible. Never combine multiple refactoring types in one step.
- **Tests first**: If there are no tests for the code you're changing, write them BEFORE refactoring. Tests are your safety net.
- **One thing at a time**: Rename OR extract OR restructure — never multiple simultaneously. Each step gets its own verification.
- **Preserve interfaces**: Internal restructuring should not change public APIs, exports, or behavior visible to callers.
- **Leave it better**: After refactoring, the code should be obviously simpler, more readable, or more maintainable. If the improvement isn't clear, don't do it.

## Arguments

`$ARGUMENTS` determines the scope:
- **File/pattern**: Refactor specific files or glob patterns
- **Audit finding IDs**: Address specific findings from rem-audit (e.g., "AUD-003, AUD-015")
- **Keyword**: Focus area like "DRY", "dead-code", "split", "rename", "simplify"
- **No arguments**: Analyze conversation context for refactoring targets

## Route to rem-plan for large refactors

If the refactor touches **5+ files OR changes public APIs/exports OR introduces a new pattern**, route to `/rem-plan` first — rem-plan's contract (Risk/Reversibility/Rollback per task) is better suited for coordinated structural work than rem-refactor's step-by-step flow. rem-refactor shines on localized changes (single-file splits, renames, dead-code removal, DRY fixes within one module).

Decision:
- 1-2 files, behavior-preserving → rem-refactor
- 3-4 files, no API changes → rem-refactor (with worktree)
- 5+ files OR API changes OR new patterns → `/rem-plan` → `/rem-execute`

## Process

### Worktree Check (Before Starting)

If this refactoring touches **5+ files** or **changes public APIs/exports**:

```
This refactoring has significant scope ([N files] / public API changes).
Working in a git worktree is recommended for safety — easy rollback if anything breaks.

Create a worktree? (y/n)
```

If yes: create worktree, install dependencies, run baseline tests, then proceed.
If no: proceed in-place (user's choice).

### Step 0 Pre-Check: Dead Code Baseline (when scope includes dead-code removal)

Before manual grep-based analysis, run static analysis tooling for a complete picture:

```bash
npx knip            # unused files, exports, dependencies (JS/TS)
npx depcheck        # unused packages in package.json
npx ts-prune        # unused TypeScript exports
```

Then use the **4-phase removal sequence by risk tier**:

| Phase | Tier | What | Action |
|---|---|---|---|
| **Analyze** | — | Run tools; also grep for dynamic patterns (`import(`, string-based requires, reflection) that tools miss | Build the full dead-code list |
| **SAFE** | No callers, no dynamic paths | Unused imports, unreachable exports with 0 grep hits | Remove immediately |
| **CAREFUL** | Possibly referenced dynamically | Exports with 0 static grep hits but used in test fixtures or string-based routes | Verify manually before removing |
| **RISKY** | Framework-convention or reflected names | Next.js file-based routes, middleware naming, reflection-accessed handlers | Leave unless you can trace every call site |

Commit each tier separately (one commit per batch). Never mix SAFE + RISKY in the same commit — rollback scope matters.

### Step 0: Understand Before Touching

Read the target code AND its ecosystem before planning any changes:

1. **Read every target file** completely — understand what it does, not just what looks wrong
2. **Find all consumers**: use Grep for imports, function calls, type references to the target
3. **Read tests**: Find existing test files for the target modules
4. **Read project conventions**: CLAUDE.md, linting config, existing patterns in similar files
5. **Read project learnings**: Check `learnings.md` in the project's memory directory for entries about the target code — previous refactoring attempts that failed, patterns that are intentionally duplicated, workarounds that must be preserved
6. **Read `_references/plan-review-patterns.md` DRY and Overengineering sections** — shared rules for when to extract vs inline vs leave-duplicate
7. **Check git history**: `git log --oneline -10 -- <file>` — understand recent changes and why

**Build a dependency map** for the refactoring scope:
```
[Target file] ← imported by [Consumer 1, Consumer 2, ...]
[Target file] → imports from [Dependency 1, Dependency 2, ...]
[Target file] ↔ tested by [Test file(s)]
```

If you can't trace the full dependency graph, the refactoring scope is too large. Narrow it.

### Step 1: Identify Refactoring Type

Classify what needs to happen. Each type has different risks and verification strategies:

| Type | What | Risk | Verification |
|------|------|------|-------------|
| **Extract** | Pull logic into a function, hook, component, or module | Medium — callers must update | Tests + build + callers still work |
| **Inline** | Replace abstraction with direct code (undo premature extraction) | Low — reduces indirection | Tests + build |
| **Rename** | Variables, functions, files, types, routes | Low — but must catch ALL references | Build + grep for old name = 0 results |
| **Move** | Relocate file, function, or type to a better location | Medium — all imports must update | Build + grep for old path = 0 results |
| **Decompose** | Split large file/function into smaller focused pieces | High — most changes, most risk | Full test suite + manual review |
| **Consolidate DRY** | Merge duplicate logic into shared utility | Medium — must verify all call sites behave identically | Tests for each original site still pass |
| **Simplify** | Reduce complexity without structural change | Low — but may change subtle behavior | Tests + careful review of edge cases |
| **Dead code removal** | Delete unused code | Low — but must prove it's truly unused | Grep for all references = 0, build passes |
| **Pattern alignment** | Make code follow project conventions | Low-Medium — conventions must be correct | Build + tests + matches existing patterns |
| **Type strengthening** | Replace `any`, weak types with proper types | Medium — may reveal hidden bugs | Build (type errors = bugs found, not introduced) |

### Step 2: Assess Test Coverage

Before touching anything, verify the safety net:

```bash
# Find test files for the target
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" | head -20

# Run existing tests to establish baseline
# (use project-specific command from CLAUDE.md or package.json)
```

**Decision matrix:**

| Test coverage | Action |
|--------------|--------|
| Good coverage for target code | Proceed with refactoring |
| Partial coverage | Write tests for uncovered paths FIRST, then refactor |
| No tests exist | Write characterization tests (tests that capture CURRENT behavior) FIRST |
| Can't write tests (no test infra) | Proceed with EXTRA caution — verify manually at each step, smaller steps |

**Characterization tests**: When writing tests before refactoring, test CURRENT behavior — even if it seems wrong. The goal is to detect if refactoring changes behavior, not to fix bugs. Bug fixes come AFTER refactoring, as separate commits.

### Step 3: Plan the Refactoring

Break the work into ordered, independently-verifiable steps. Each step should be:
- **Small enough** to review in under 2 minutes
- **Independently correct** — the code works after this step alone
- **Reversible** — can be undone without affecting other steps

**Plan format:**

```
Step 1: [Description] — [Type: Extract/Rename/Move/etc.]
  Files: [list of files to modify]
  Verify: [specific verification — build? test? grep?]
  Risk: Low/Medium/High

Step 2: [Description]
  Files: [...]
  Verify: [...]
  Depends on: Step 1
```

**Ordering rules:**
1. Renames before moves (rename at old location, then move)
2. Extract before delete (create new location, update references, then remove old)
3. Tests before production code changes
4. Leaf dependencies before their consumers
5. Type changes before implementation changes

**For bulk mechanical edits** (renaming across many files, updating imports, converting patterns), note in the plan where Codex (`cx "task"`) would be more efficient than manual editing. Flag these as "Codex candidate" steps.

### Step 4: Execute (One Step at a Time)

For EACH step in the plan:

1. **Make the change** — edit only the files listed for this step
2. **Verify immediately**:
   - Run the project's build/typecheck command
   - Run tests for the affected modules
   - For renames/moves: grep for the old name/path — must return 0 results
   - For extractions: verify all callers compile and tests pass
   - For dead code removal: verify no references remain
3. **If verification fails** — stop, diagnose, fix, re-verify. Do NOT proceed to the next step with a broken build.
4. **Note what changed** — track for the final report

**Verification commands** (adapt to project):
```bash
# TypeScript/JavaScript
npx tsc --noEmit                    # Type check
npm test -- --related <files>       # Run related tests
yarn test -- --changedSince=HEAD    # Run tests for changed files

# Go
go vet ./...                        # Static analysis
go build ./...                      # Build check
go test ./path/to/package/...       # Run package tests

# General
grep -r "old_name" --include="*.ts" --include="*.tsx" .  # Verify rename complete
```

### Step 5: Clean Up

After all refactoring steps are complete:

1. **Remove dead code** created by the refactoring:
   - Unused imports (build/lint will catch these)
   - Unused variables, functions, types
   - Empty files that had everything extracted out
   - Old test fixtures no longer needed

2. **Update documentation**:
   - If file structure changed, update any path references in docs
   - If public API changed, update JSDoc/GoDoc
   - Don't add new docs — just fix references broken by the refactoring

3. **Verify consistency**:
   - New code follows the same patterns as existing code
   - No mixed styles introduced (old pattern + new pattern coexisting)
   - Naming conventions are consistent

### Step 6: Final Verification

Run the FULL verification suite — not just affected files:

```bash
# Full build
# Full test suite
# Full lint/vet
```

If any failures occur that weren't present before the refactoring, the refactoring introduced a regression. Fix it or revert the problematic step.

### Step 7: Report

#### Refactoring Summary

| Step | Type | Files Changed | Verification | Status |
|------|------|--------------|-------------|--------|
| 1 | Extract | auth.ts, utils.ts | Build + tests pass | Done |
| 2 | Rename | 8 files | Grep: 0 old refs | Done |

#### Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Files in scope | N | N | +/-N |
| Lines of code | N | N | -N (target: reduction) |
| Largest file | N lines | N lines | -N |
| Duplicate blocks | N | N | -N |
| `any` types | N | N | -N |
| Test coverage | X% | X% | +X% |

#### What Changed
- Brief description of each structural change
- New files/modules created (with purpose)
- Files/code deleted (with justification)

#### What Didn't Change
- External behavior preserved (how verified)
- Public APIs unchanged (or intentionally changed with migration)
- Test suite status: all passing / N new tests added

#### Remaining Opportunities
- Refactoring steps deferred (too risky, needs more tests, depends on other work)
- Related code that would benefit from the same treatment
- Suggest running `/rem-test` if coverage gaps were found
- Suggest running `/rem-learn` if the refactoring revealed non-obvious patterns

---

## Refactoring Patterns Reference

### DRY: Extract Shared Logic
```
1. Identify 2+ duplicate code blocks
2. Verify they are TRULY identical in behavior (not just similar-looking)
3. Write tests covering both original sites
4. Create shared function/component with the common logic
5. Replace each duplicate with a call to the shared code
6. Verify tests still pass for each original call site
7. Delete any now-unused code
```
**Trap**: Code that LOOKS similar but handles different edge cases. Extracting it creates a function with too many parameters or conditional branches. If the shared version is more complex than the duplicates, don't extract.

### Decompose: Split Large File
```
1. Map every export and its consumers
2. Identify natural groupings (by domain concept, not by code type)
3. Create new files for each group
4. Move exports one group at a time (not all at once)
5. Update imports in consumers after each move
6. Verify build after each group move
7. Delete original file only after everything is moved
```
**Trap**: Splitting by code type (all types in types.ts, all utils in utils.ts) instead of by domain. Group by what changes together.

### Dead Code: Safe Removal
```
1. Grep for ALL references (imports, string references, dynamic access)
2. Check for indirect references: reflection, dynamic imports, string-based routing
3. Check if it's referenced in tests (test-only code is NOT dead code)
4. Check git blame — was it recently added? (might be WIP, not dead)
5. Remove the code
6. Build — any errors = it wasn't actually dead
7. Run full test suite
```
**Trap**: Code referenced via string interpolation, dynamic imports, or framework conventions (Next.js file-based routing, middleware naming). Grep may miss these.

### Rename: Comprehensive Rename
```
1. Grep for ALL occurrences (code, tests, docs, config, comments, strings)
2. Categorize: identifier references vs string references vs documentation
3. Rename identifiers (IDE rename or find-replace)
4. Update string references (URLs, error messages, log statements)
5. Update documentation references
6. Build + test
7. Grep for old name — must return 0 results
```
**Trap**: Partial renames (renamed the function but not the error message that mentions it, not the log statement, not the test description).

### Type Strengthening: Remove `any`
```
1. Find the `any` usage
2. Trace where the value comes from — what's its actual shape?
3. Define or find the correct type
4. Replace `any` with the correct type
5. Build — type errors reveal hidden bugs or incorrect assumptions
6. Fix revealed issues (these are BUGS that `any` was hiding, not refactoring problems)
```
**Trap**: Replacing `any` with a type that's too strict, causing false type errors. Or replacing with a type that's still too loose (e.g., `Record<string, any>`). Aim for the tightest correct type.

---

## Rules

1. **Never refactor and add features simultaneously.** Refactoring is a separate activity. If you find a bug during refactoring, note it and fix it in a separate step (or separate commit).

2. **Never refactor without verification.** If you can't run a build or tests, the refactoring is not safe. At minimum: typecheck passes.

3. **Prefer small changes over clever changes.** Three simple extractions are better than one clever abstraction.

4. **If the refactoring makes the code harder to understand, stop.** The goal is clarity. If the "clean" version requires more mental effort to follow, the original was better.

5. **Respect existing patterns.** Don't introduce a new pattern during refactoring. Align with what the codebase already does. If the existing pattern is bad, that's a separate conversation.

6. **Track your changes.** If you can't explain what changed and why, the refactoring is too complex. Break it down further.
