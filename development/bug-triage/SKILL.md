---
name: "Bug Triage"
description: "Systematically reproduce, diagnose, and analyze bugs to determine root cause, assess severity, and plan fix strategy"
category: "analysis"
required_tools: ["Read", "Write", "Grep", "Glob", "Bash"]
---

# Bug Triage

## Purpose
Systematically analyze bug reports to reproduce issues, identify root causes, assess severity and impact, and determine the appropriate fix strategy and priority.

## When to Use
- Analyzing incoming bug reports
- Investigating production issues
- Diagnosing test failures
- Planning bug fix work
- Prioritizing bug backlog

## Key Capabilities
1. **Bug Reproduction** - Create reliable steps to reproduce the issue
2. **Root Cause Analysis** - Identify underlying cause, not just symptoms
3. **Severity Assessment** - Determine impact and urgency accurately

## Approach
1. **Understand the Report** - Read bug description and symptoms
2. **Reproduce the Bug** - Create minimal reproduction steps
3. **Isolate the Cause** - Use logs, debugging, code inspection
4. **Assess Impact** - Determine affected users and severity
5. **Determine Fix Strategy** - Quick patch vs architectural fix
6. **Document Findings** - Clear report for implementation team

## Example
**Context**: Bug report "Users can't log in"
```markdown
## Bug Analysis

**Symptoms**:
- Users see "Invalid credentials" error
- Occurs only for accounts created after Oct 15
- Works fine for older accounts

**Reproduction Steps**:
1. Create new user account
2. Log out
3. Attempt to log in with correct credentials
4. Observe error message

**Root Cause**:
- Code inspection of auth system
- Found: Password hashing algorithm changed Oct 15
- Old accounts use bcrypt, new accounts use argon2
- Login validation only checks bcrypt

**Location**: `src/auth/validator.py:45-67`

**Impact**:
- Severity: Critical (blocks all new users)
- Affected: ~500 accounts created in last week
- Workaround: None available

**Fix Strategy**:
- Update validator to check both hash types
- Add migration for existing argon2 hashes
- Estimated effort: 2 hours (small fix)
- Testing required: Auth system regression tests

**Priority**: Critical - Fix immediately
**Recommended Agent**: implementer (straightforward code fix)
```

## Best Practices
- ✅ Always try to reproduce before diagnosing
- ✅ Check logs and error messages first
- ✅ Use Grep/Glob to find related code quickly
- ✅ Document exact reproduction steps
- ✅ Consider data issues, not just code bugs
- ✅ Assess severity objectively (not all bugs are critical)
- ❌ Avoid: Assuming the cause without investigation
- ❌ Avoid: Treating all bugs as equally urgent