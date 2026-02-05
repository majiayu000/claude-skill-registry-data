---
name: pre-commit-check
description: Pre-commit validation checklist before staging and committing code. Use BEFORE every git commit to ensure code quality, tests pass, and documentation is updated. Triggers on "commit", "stage changes", "ready to commit", or when completing a feature or fix.
---

# Pre-Commit Checklist

Run through this checklist before every commit.

## Required Checks

### 1. Build Verification
```bash
npm run build
```
- [ ] Build completes without errors
- [ ] No new warnings introduced

### 2. Test Suite
```bash
npm test
```
- [ ] All tests pass
- [ ] No skipped tests that should run
- [ ] Coverage not decreased (if tracked)

### 3. Linting (if configured)
```bash
npm run lint
```
- [ ] No linting errors
- [ ] No new warnings

## Context Updates

### 4. ConPort Documentation
- [ ] Log any decisions made during this work (`mcp__conport__log_decision`)
- [ ] Update progress entries to DONE (`mcp__conport__update_progress`)
- [ ] Log any new patterns discovered (`mcp__conport__log_system_pattern`)
- [ ] Link related items (`mcp__conport__link_conport_items`)

### 5. Serena Memory
- [ ] Document architectural learnings if applicable (`write_memory`)

## Code Review

### 6. Self-Review
- [ ] Changes match the task requirements
- [ ] No debug code left behind (console.log, debugger statements)
- [ ] No commented-out code without explanation
- [ ] No hardcoded values that should be configurable

### 7. Automated Reviews (for significant changes)

Launch these sub-agents in parallel for comprehensive review:

**Code Quality Review:**
```
Task(subagent_type="pr-review-toolkit:code-reviewer", prompt="Review unstaged changes for code quality, bugs, and adherence to project conventions")
```

**Security Review (when changes involve):**
- User input handling, file uploads, URL processing
- API keys, authentication, authorization
- Data sanitization or validation
- External API calls or network requests

```
Task(subagent_type="security-pro:security-auditor", prompt="Review changes for security vulnerabilities, OWASP compliance, and secure coding practices")
```

**Frontend Security (for UI changes):**
```
Task(subagent_type="frontend-mobile-security:frontend-security-coder", prompt="Review frontend changes for XSS prevention, output sanitization, and client-side security")
```

**Backend Security (for API/service changes):**
```
Task(subagent_type="backend-api-security:backend-security-coder", prompt="Review backend changes for input validation, authentication security, and API security")
```

**Architecture Review (for structural changes):**
```
Task(subagent_type="code-review-ai:architect-review", prompt="Review changes for architectural integrity, patterns adherence, and maintainability")
```

- [ ] Address all high-priority findings before committing

## Commit

### 8. Stage and Commit
```bash
git add -A
git status  # Review staged files
git commit -m "type: descriptive message"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `docs:` - Documentation only
- `test:` - Adding/updating tests
- `chore:` - Maintenance tasks
