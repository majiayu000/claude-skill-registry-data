---
name: pr-review-standards
description: "Use when creating PRs to enforce code quality standards. Automated detection of anti-patterns, security issues, and code smells. Python 3.8+"
author: "Claude Code Learning Flywheel Team"
allowed-tools: ["Bash", "Read", "Grep", "Glob"]
version: 1.0.0
last_verified: "2026-01-01"
tags: ["code-quality", "pr", "review", "gatekeeper"]
related-skills: ["git-commit-standards"]
---

# Skill: PR Review Standards

## Purpose
Enforce code quality before human review. Transform the agent from a "coder" into a "reviewer" by catching common anti-patterns and violations.

## 1. Negative Knowledge (Anti-Patterns)
> **CRITICAL:** Fail the review if any of these are present.

| Pattern | Why It Fails | Correction |
| :--- | :--- | :--- |
| `console.log` in commits | Pollutes production logs | Use `logger.debug()` or remove |
| Hardcoded secrets | Security violation | Use `process.env` or secrets manager |
| Big PRs (>500 lines) | Unreviewable, high risk | Split into feature branches |
| Direct DB access in routes | Violates separation of concerns | Use service layer |
| Missing tests for new code | No verification of behavior | Add unit/integration tests |
| Task marker comments (TO-DO/FIX-ME) in production code | Technical debt indicator | Resolve or create issue |
| Commented-out code blocks | Code smell, use version control | Delete and rely on git history |
| Inconsistent formatting | Readability issues | Run formatter before commit |

## 2. Verified Procedure

### Pre-Review Checks
1. **Scan Diff:** Run `git diff main...HEAD` to see all changes
2. **Analyze:** Check against the "Negative Knowledge" table above
3. **Validate:** Run the static analysis script:
   ```bash
   python .claude/skills/pr-review-standards/scripts/analyze_diff.py
   ```
4. **Report:** Generate a markdown summary of blocking issues

### Review Criteria
- **Security:** No hardcoded credentials, API keys, or tokens
- **Quality:** No debug statements, commented code, or task markers
- **Size:** PR should be <500 lines (excluding generated files)
- **Tests:** New features must include tests
- **Documentation:** Public APIs must have docstrings

### Execution Flow
```
1. Agent completes feature work
2. Agent runs self-review using this skill
3. If blocking issues found:
   - Fix immediately
   - Re-run validation
4. If clean:
   - Commit changes
   - Push to branch
   - Create PR
```

## 3. Zero-Context Scripts

### analyze_diff.py
Located at: `.claude/skills/pr-review-standards/scripts/analyze_diff.py`

**Purpose:** Automated static analysis of git diff to detect anti-patterns.

**Usage:**
```bash
python .claude/skills/pr-review-standards/scripts/analyze_diff.py [--base=main]
```

**Returns:**
- Exit code 0: No blocking issues
- Exit code 1: Blocking issues found
- JSON report of all findings

## 4. Failed Attempts (Negative Knowledge Evolution)

### ❌ Attempt: Allow console.log in development
**Context:** Tried to permit console.log if guarded by environment checks
**Failure:** Still leaked to production due to misconfigured env vars
**Learning:** Zero tolerance for console.log in commits

### ❌ Attempt: Auto-fix all issues
**Context:** Script attempted to automatically fix detected issues
**Failure:** Introduced bugs by removing contextually-important code
**Learning:** Report issues, require manual review and fixing

## 5. Governance
- **Token Budget:** ~300 lines (within 500 limit)
- **Dependencies:** Git, Python 3.8+
- **Maintenance:** Update "Negative Knowledge" table as new patterns emerge
- **Verification Date:** 2026-01-01
