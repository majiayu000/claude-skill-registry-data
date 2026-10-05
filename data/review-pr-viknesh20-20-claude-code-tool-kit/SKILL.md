---
name: review-pr
description: "Performs a comprehensive pull request code review covering correctness, security, performance, test coverage, and coding standards. Use when reviewing any code changes before merge."
argument-hint: "[branch or PR number]"
allowed-tools: Read, Grep, Glob, Bash(git diff*), Bash(git log*), Bash(git show*), Bash(gh pr*)
---

# Pull Request Code Review

## Gather Context

### Changed Files
!`git diff --name-only HEAD~1 2>/dev/null || echo "No commits to diff"`

### Diff Summary
!`git diff --stat HEAD~1 2>/dev/null || echo "No diff available"`

### Full Diff
!`git diff HEAD~1 2>/dev/null | head -500`

### Recent Commits
!`git log --oneline -10 2>/dev/null`

---

## Review Checklist

Analyze every changed file against the following categories. For each finding, provide:
- **File path and line number**
- **Severity**: Critical / High / Medium / Low
- **Description** of the issue
- **Suggested fix** with code snippet

### 1. Correctness
- Logic errors or off-by-one mistakes
- Missing null/undefined/nil checks
- Incomplete error handling
- Race conditions or concurrency issues
- Incorrect use of APIs or library functions

### 2. Security
- Input validation gaps (SQL injection, XSS, command injection, path traversal)
- Hardcoded secrets, tokens, or credentials
- Authentication/authorization bypass risks
- Insecure data handling (PII exposure, logging sensitive data)
- Missing CSRF/CORS protections where applicable

### 3. Performance
- N+1 query patterns
- Unnecessary loops or redundant computations
- Missing pagination for unbounded queries
- Blocking operations in async contexts
- Large memory allocations in hot paths
- Missing indexes for new database queries

### 4. Test Coverage
- Are new code paths covered by tests?
- Are edge cases and error paths tested?
- Are mocks appropriate and not over-mocking?
- Do test names clearly describe the scenario?

### 5. Code Quality
- Readability and naming clarity
- Unnecessary complexity that can be simplified
- Code duplication that should be extracted
- Dead code or unused imports
- Missing or misleading comments

### 6. Conventions
- Adherence to project coding standards (check CLAUDE.md)
- Consistent formatting and style
- Proper commit message format
- Documentation for public APIs

---

## Output Format

### Findings

Group findings by severity:

#### Critical (must fix before merge)
<!-- Blocking issues -->

#### High (strongly recommend fixing)
<!-- Significant issues -->

#### Medium (should fix)
<!-- Moderate issues -->

#### Low (nice to have)
<!-- Minor suggestions -->

### Summary
Provide a 2-3 sentence executive summary of the PR quality.

### Verdict
State one of:
- **GO** — Ready to merge (no critical/high issues)
- **CONDITIONAL GO** — Merge after addressing critical/high findings
- **NO-GO** — Significant issues require rework before re-review
