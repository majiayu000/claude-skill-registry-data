---
name: code-review
description: Enforces systematic multi-axis code review (correctness, readability, architecture, security, performance) with severity ratings and actionable findings. Use before merging, before declaring done, or when explicitly asked to review code. Unlike code-collaborate-qa (conversational Q&A), this is a structured process with checklists.
---

# Code Review (Structured Multi-Axis)

## Problem it solves

Code review without structure misses issues. Reviewers focus on nitpicks (naming, formatting) and skip hard questions (correctness, security, architecture). This causes:
- Shallow reviews that miss real bugs
- Inconsistent review quality across sessions
- Security issues overlooked because the reviewer wasn't looking for them
- Review comments without actionable evidence or severity
- No systematic coverage of all quality dimensions

## Protocol

### 1. Before reviewing

Read the entire diff or file first. Do not comment during the first pass. Build mental model of:
- What does this code do?
- What was it supposed to do? (check the spec or requirements)
- What's the scope of the change?

### 2. Multi-axis review checklist

Review each axis in order. Do not skip axes. For each finding, assign a severity.

#### Severity levels

| Level | Meaning | Action |
|-------|---------|--------|
| **Critical** | Bug, security vulnerability, or data loss risk | Must fix before merge |
| **High** | Significant correctness, performance, or maintainability issue | Should fix before merge |
| **Medium** | Minor issue, code smell, or improvement opportunity | Fix or file a follow-up |
| **Low** | Nitpick, style preference, or suggestion | Optional |

#### Axis 1: Correctness

- Does the code do what the spec requires?
- Are there edge cases not handled? (null, empty, boundary, concurrent access)
- Are error paths handled? (exceptions, error returns, fallbacks)
- Are there race conditions or state corruption risks?
- Do calculations look correct? (off-by-one, overflow, type coercion)
- Are assumptions validated? (input validation, preconditions, invariants)

#### Axis 2: Readability & Maintainability

- Is the intent clear without comments? (self-documenting code)
- Are names precise? (functions named for what they do, variables for what they hold)
- Is the code too long? (function >50 lines, file >500 lines — consider splitting)
- Are there unnecessary abstractions? (YAGNI violations)
- Would a new team member understand this in one pass?

#### Axis 3: Architecture

- Does this follow the project's existing patterns? (see follow-existing-patterns)
- Does it introduce new dependencies? Are they justified?
- Is the change at the right level of abstraction?
- Does it respect layering? (presentation -> business -> data, no circular deps)
- Is it testable? (can you unit test this without mocking the world?)

#### Axis 4: Security

- Are inputs sanitized? (injection risks: SQL, command, XSS, path traversal)
- Are secrets handled safely? (no hardcoded keys, no logging of sensitive data)
- Are permissions checked? (authorization boundaries respected)
- Is there risk of denial of service? (unbounded loops, large allocations, no timeouts)
- Does it follow the principle of least privilege?

#### Axis 5: Performance

- Are there N+1 queries or redundant computations?
- Are there obvious performance bottlenecks? (nested loops over large data, synchronous I/O in hot path)
- Is there premature optimization that complicates the code?
- Are resources released properly? (connections, file handles, memory)

### 3. Write the review report

Format each finding as:

```
**Severity**: [Critical|High|Medium|Low]
**File**: path/to/file:line
**Issue**: One-line description of the problem
**Evidence**: Why this is a problem (include relevant code context)
**Suggestion**: How to fix it (specific, actionable)
```

### 4. Summarize

After all findings:
- **Verdict**: Approve / Changes requested / Blocked
- **Critical blockers**: 0-N items that must be resolved
- **Summary**: 2-3 sentence overall assessment

## Detection triggers

Activate when:
- User says "review this code", "code review", or "CR"
- Before merging a PR or branch
- Before declaring a task done (as final quality gate)
- After implementation completes and tests pass
- User shares a diff or code snippet for feedback

## When NOT to use

- Quick prototyping or exploratory code
- User explicitly asks for conversational Q&A (use code-collaborate-qa instead)
- Code that is explicitly marked as temporary or throwaway
- User asks for a specific axis only (e.g., "just check security")

## Cross-references

- **spec-driven-development** — The spec is the review baseline. Review checks if the implementation matches the spec.

- **test-driven-development** — Review checks that tests exist, follow TDD principles, and cover the right cases.

- **code-collaborate-qa** — Use for conversational Q&A about code. Use code-review for a structured multi-axis review.

- **security-best-practices** — Integrate security review findings. For deep security review, load this skill alongside.

- **follow-existing-patterns** — The architecture axis checks that new code matches the project's existing patterns.

- **receiving-code-review** — When receiving review feedback, use receiving-code-review to respond properly instead of blindly agreeing.

- **anti-premature-termination** — Code review is a completion gate. Do not declare done until review findings are resolved.
- **git-workflow-conventional-commits** — Review should verify commit messages follow conventional format and commits are atomic.
