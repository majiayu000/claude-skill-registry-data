---
name: code-review-skill
description: Use to review code implementations for quality, correctness, and best practices
---

# Code Review Skill

Two-phase review: First analyze and document findings, then apply approved fixes.

**Preset Configuration:**
- Focus: Code quality, correctness, best practices
- Quality Gate: No new findings for 1 iteration (review comprehensive)
- Reviewer Type: Senior Code Reviewer
- Max Iterations: 4

## When to Use

- After completing implementation of a feature
- Before creating a pull request
- When refactoring significant code
- Post-merge quality verification

## Required Information

1. **Target** - code path or git range (e.g., `src-tauri/src/calculations.rs` or `HEAD~3..HEAD`)
2. **Reference** - plan or spec the code implements

---

## Phase 1: Review (Findings Only)

### Step 1: Gather Code Context

If git range provided:
```bash
git diff --stat {BASE}..{HEAD}
git diff {BASE}..{HEAD}
```

If file path provided:
- Read the file(s)
- Identify recent changes

### Step 2: Run Tests (Baseline)

```bash
npm run test:backend
```

Note test status for review context (pass/fail). Do NOT fix yet.

### Step 3: Create Review Document

Create `_code-review.md` in project root or task folder:

```markdown
# Code Review

**Target:** {TARGET}
**Reference:** {REFERENCE}
**Started:** YYYY-MM-DD
**Status:** In Progress
**Focus:** Quality, correctness, best practices

**Baseline Test Status:** [Pass / N failures]

## Iteration 1

### Findings

[To be filled by review agent]
```

### Step 4: Execute Review Loop

For each iteration (max 4):

**Spawn Review Agent:**

```
Task tool (superpowers:code-reviewer):
  Use template from requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: {description from reference}
  PLAN_OR_REQUIREMENTS: {REFERENCE}
  BASE_SHA: {BASE or N/A}
  HEAD_SHA: {HEAD or current}

  IMPORTANT: Document findings only. Do not apply fixes.
```

**Update Review Document:** Append findings to `_code-review.md`:
```markdown
## Iteration N

### New Findings
- [Critical] Issue description - `file:line` - Suggested fix
- [Important] Issue description - `file:line` - Suggested fix
- [Minor] Issue description - `file:line` - Suggested fix

### Test Gaps
[Any missing test coverage noted]

### Coverage Assessment
[Areas reviewed / Areas remaining]
```

**Commit Review Only:**
```bash
git add _code-review.md
git commit -m "review(code): iteration N findings for {TARGET}"
```

**Quality Gate:** Exit when no new findings for 1 iteration (review is comprehensive).

### Step 5: Finalize Review Document

Update `_code-review.md` with summary:

```markdown
## Review Summary

**Status:** Ready for User Review
**Iterations:** N
**Total Findings:** X Critical, Y Important, Z Minor
**Test Status:** [Pass / Fail]

### All Findings (Consolidated)

#### Critical
1. [ ] Issue - `file:line` - Suggested fix

#### Important
1. [ ] Issue - `file:line` - Suggested fix

#### Minor
1. [ ] Issue - `file:line` - Suggested fix

### Test Gaps
- [ ] Missing test for X
- [ ] Edge case Y not covered

### Recommendation
[Ready to merge / Needs fixes / Major issues]
```

**Commit:**
```bash
git add _code-review.md
git commit -m "review(code): complete findings for {TARGET}"
```

### Step 6: Present Review for Approval

Inform user:

> **Code review complete.**
>
> Please review `_code-review.md` for findings.
>
> After your review, let me know:
> - Which findings to fix
> - Which to skip (with reason)
> - Any questions about findings

**STOP and wait for user direction.**

---

## Phase 2: Apply Approved Fixes

*Only proceed after user approval.*

### Step 7: Apply Approved Fixes

For each user-approved finding:

1. Implement the fix
2. Check the finding as addressed in `_code-review.md`: `[x]`

### Step 8: Run Tests

```bash
npm run test:backend
```

If tests fail:
- Diagnose the failure
- Fix or report to user for decision

### Step 9: Commit Changes

```bash
git add -A
git commit -m "fix: address code review findings

Addressed:
- [list of fixed issues]"
```

### Step 10: Final Assessment

Update `_code-review.md`:

```markdown
## Resolution

**Addressed:** N findings
**Skipped:** M findings (user decision)
**Test Status:** All passing
**Status:** Complete

### Applied Fixes
- Finding 1: [how resolved]
- Finding 2: [how resolved]

### Skipped Items
- Finding X: [user's reason]
```

---

## Domain-Specific Checklist

Review should verify:
- [ ] Tests pass
- [ ] No obvious bugs
- [ ] Error handling present
- [ ] No security vulnerabilities (input validation, etc.)
- [ ] Code matches plan/spec
- [ ] No scope creep (extra features not requested)
- [ ] Follows project patterns (see CLAUDE.md)

## Example

```
User: /code-review src-tauri/src/suggestions.rs against _tasks/19-feature/02-plan.md

Claude: [Executes Phase 1 - runs tests, creates _code-review.md, iterates until comprehensive]
Claude: Code review complete. Please review _code-review.md for findings.

User: Fix all Critical issues. Skip the Minor style suggestions.

Claude: [Executes Phase 2 - applies approved fixes, runs tests, commits]
```
