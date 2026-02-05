---
name: self-reviewing-code
description: Self-review checklist before marking PR ready - catch clarity, correctness, and maintainability issues with fresh eyes
---

# Self-Reviewing Code

## Purpose

Review your own PR with beginner-mind before marking ready. Step back and catch assumptions, missing edge cases, unclear code.

**Core insight:** You're too close to the code. Review as if seeing it for the first time.

## Pre-Review

```bash
just check-all    # Automated checks
gh pr checks      # CI status
```

## Self-Review Checklist

**Before marking ready:**

- [ ] Re-read original issue - ALL criteria met?
- [ ] Review diff - code clear and maintainable?
- [ ] Edge cases covered in tests?
- [ ] Documentation updated?
- [ ] `just check-all` passes?
- [ ] CI green?

## Software Laws

Apply these industry-standard principles:

- **Postel's Law** - Liberal input acceptance, conservative output
- **Hyrum's Law** - All observable behavior becomes API contract
- **Kernighan's Law** - Simple code over clever code
- **Leaky Abstractions** - Understand when abstractions leak
- **DRY** - Single source of truth, no duplication
- **YAGNI** - Add only when actually needed

## Review Questions

**Clarity:**
- Would this make sense to someone unfamiliar?
- Variable/function names descriptive?
- Complex logic commented with "why"?

**Correctness:**
- Tests cover edge cases?
- Error conditions handled?
- Could this fail in production?

**Maintainability:**
- Code DRY?
- Functions single-responsibility?
- Future changes easy?

**Performance:**
- Obvious performance issues?
- Database queries efficient?

**Security:**
- Inputs validated?
- Sensitive data handled properly?
- No injection vulnerabilities?

## Common Issues

- Leftover debugging code (`console.log`, `print`)
- Commented-out code
- TODOs that should be issues
- Magic numbers without constants
- Missing null/undefined checks
- Hardcoded values that should be config

## Fresh Eyes Technique

1. Walk away 15+ minutes
2. Come back, review as if someone else wrote it
3. Read diff line by line
4. Question every decision

**Ask:** "Would I approve this reviewing someone else's code?"
