---
name: review
description: |
  Code reviewer that reads diffs, catches bugs, auto-fixes safe issues, and asks
  about ambiguous ones. Checks for SOLID violations, security issues, performance
  problems, and test coverage gaps. Auto-commits fixes as atomic commits.
  Use when: "review this", "check my code", "code review", "review the diff",
  or before shipping any code.
---

# /review — Code Reviewer

Your senior engineer who catches what you missed.

## When to Use

- Before opening a PR
- After implementing a feature
- When you want a second opinion on code quality
- Before `/ship`

## Process

### Step 1: Read Context

- Check if a plan exists (`docs/plans/*.md`) — use it for intent
- Read the git diff (`git diff main...HEAD` or staged changes)
- Identify the scope: which files changed, what's the intent

### Step 2: Analyze the Diff

Check for:

**Critical (auto-block)**
- Hardcoded secrets, API keys, tokens
- SQL injection, XSS, command injection
- Broken error handling (swallowed exceptions)
- Race conditions in concurrent code

**High (flag for review)**
- Missing input validation
- N+1 queries
- Unbounded loops or memory allocation
- Missing tests for new logic

**Medium (suggest improvement)**
- SOLID violations
- Dead code or unused imports
- Inconsistent naming
- Missing error messages

**Low (note)**
- Style inconsistencies
- TODO/FIXME without issue reference
- Overly complex expressions

### Step 3: Auto-Fix Safe Issues

If confidence > 95% and the fix is mechanical:
- Remove unused imports
- Fix obvious typos in strings
- Add missing `await`
- Fix incorrect null checks

Commit each fix atomically:
```
fix(review): {description of fix}
```

### Step 4: Report

For issues that need human judgment:
```
## Review Summary

### Auto-Fixed (2)
- ✅ Removed unused import `lodash` in src/utils.ts
- ✅ Added missing `await` in src/api.ts:42

### Needs Decision (1)
- ⚠️ Race condition in src/queue.ts:88 — two workers can claim same job
  Suggested fix: Add optimistic locking. Apply? [y/n]

### Notes (1)
- 💡 Consider extracting src/handlers.ts:120-145 into a helper
```

## Chaining

- **Before**: `/plan` (reads plan for intent context)
- **After**: `/qa` (review findings inform test priorities), `/ship` (blocks ship if critical issues remain)
