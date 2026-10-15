---
name: code-review-checklist
description: "Systematic code review with quality gates, security audit, and parallel checks. Use for structured feedback on pull requests."
context: fork
globs: []
alwaysApply: false
---

# Code Review Checklist

Systematic code review combining quality gates, security audit (OWASP Top 10), and parallel checks for comprehensive validation.

---

## Review Scope

- Review **ONLY changed files** (check diff, not entire file)
- Check related commits
- Link to related PRs/issues

---

## Automated Quality Checks (Run FIRST)

**Before any manual review, run automated checks:**

```bash
# Python
ruff check --select F,E,W,UP,B,SIM --output-format concise <files> && ruff format --check <files>

# TypeScript/JavaScript
biome check --write --unsafe <files>
```

**Block review if checks fail.** Return NEEDS_REVISION with specific violations.

---

## Review Checklist

### Correctness
- [ ] Logic is correct and complete
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] Performance acceptable

### Code Quality
- [ ] No duplication (DRY principle)
- [ ] Single responsibility functions
- [ ] Clear and descriptive naming
- [ ] Reasonable complexity (no god functions)
- [ ] Proper file sizes (<300 lines)

### Testing
- [ ] Unit tests written
- [ ] Coverage ≥80%
- [ ] Integration tests for workflows
- [ ] Edge cases tested
- [ ] Error conditions tested

### Security (OWASP Top 10)
- [ ] Input validation present
- [ ] No hardcoded secrets/credentials
- [ ] No XXE, CSRF, XSS vulnerabilities
- [ ] Authentication/authorization proper
- [ ] Sensitive data encrypted
- [ ] Rate limiting on sensitive endpoints
- [ ] Audit logging for security events

### Documentation
- [ ] Public functions documented
- [ ] Comments explain WHY not WHAT
- [ ] README/guides accurate
- [ ] API documentation complete

---

## Feedback Format

```
## Verdict: APPROVED | NEEDS_REVISION | FAILED

### Issues
- CRITICAL: X | HIGH: Y | MEDIUM: Z | LOW: W

### Details
- [CRITICAL] file.py:42 — SQL injection risk, use parameterized queries
- [HIGH] component.tsx:15 — Missing input validation
- [MEDIUM] test_utils.py:8 — Edge case not covered

### 🔍 Human Review Focus
1. [Item AI cannot fully validate — e.g., business logic correctness]
2. [Item 2 — e.g., UX flow matches requirements]
```

---

## Parallel Review Pattern

For comprehensive reviews, run 5 checks simultaneously:

| Check | Focus | Agent |
|-------|-------|-------|
| **Goal** | Does it meet requirements? | Themis |
| **Quality** | Code quality, SOLID, DRY | Themis |
| **Security** | OWASP Top 10, secrets | Themis |
| **QA** | Tests, coverage, edge cases | Themis |
| **Context** | Fits architecture, no regressions | Themis |

---

## Severity Definitions

| Level | Action | Example |
|-------|--------|---------|
| **CRITICAL** | Block merge | Security vulnerability, data loss risk |
| **HIGH** | Must fix before merge | Missing auth, broken error handling |
| **MEDIUM** | Should fix soon | Missing tests, code duplication |
| **LOW** | Nice to have | Naming, formatting, minor docs |

---

## SOLID Principles Check

- **S**ingle Responsibility: Each class/function does one thing
- **O**pen/Closed: Extensible without modification
- **L**iskov Substitution: Subtypes behave like base types
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

---

## Anti-Patterns

- ❌ Reviewing entire file instead of diff
- ❌ Approving without running tests
- ❌ Ignoring security implications
- ❌ Vague feedback ("looks good", "needs work")
- ❌ Nitpicking style over substance
