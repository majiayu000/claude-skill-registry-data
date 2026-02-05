---
name: fix-issue
description: Debug and fix bugs by reproducing issues, identifying root causes, implementing fixes, and validating without regressions. Use when debugging reported bugs, investigating test failures, or resolving production issues requiring root cause analysis.
acceptance:
  - bug_reproduced: "Bug successfully reproduced with failing test"
  - root_cause_identified: "Root cause clearly identified and documented"
  - fix_applied: "Minimal fix applied addressing root cause"
  - tests_passing: "Bug test now passes, all existing tests pass"
  - no_regressions: "No regressions introduced by fix"
  - edge_cases_tested: "Edge cases identified and tested"
inputs:
  issue_id:
    type: string
    required: true
    description: "Issue/bug identifier (e.g., bug-login-email, issue-42)"
    validation: "Must be valid issue identifier"
  severity:
    type: enum
    required: false
    description: "Issue severity: critical, high, medium, low"
    default: "medium"
  reproduction_confirmed:
    type: boolean
    required: false
    description: "Whether reproduction is confirmed"
    default: false
outputs:
  fix_complete:
    type: boolean
    description: "Whether bug fix is complete"
  bug_test_passes:
    type: boolean
    description: "Whether the new bug test passes"
  all_tests_pass:
    type: boolean
    description: "Whether all tests pass (no regressions)"
  regression_count:
    type: number
    description: "Number of regressions introduced (should be 0)"
  edge_case_tests_added:
    type: number
    description: "Number of edge case tests added"
  files_modified:
    type: array
    description: "List of files modified during fix"
  root_cause_location:
    type: string
    description: "File and line where root cause was identified"
telemetry:
  emit: "skill.fix-issue.completed"
  track:
    - issue_id
    - severity
    - reproduction_confirmed
    - root_cause_identified
    - duration_ms
    - files_modified_count
    - tests_added
    - tests_passed
    - regression_count
---

# Fix Issue Skill

## Purpose

Debug and fix bugs, issues, or failing tests through systematic reproduction, root cause analysis, minimal fixes, and comprehensive validation.

**Core Principle:** Always write failing test first, fix with minimal changes, validate with full test suite.

## Prerequisites

- Clear issue description or failing test
- Access to relevant code and logs
- Test framework configured

---

## Workflow

### 1. Understand Issue

**Parse issue description:**
- **What** is broken?
- **When** does it happen? (always/sometimes/specific condition)
- **Where** does it occur? (component/file/endpoint)
- **Expected** vs **Actual** behavior
- **Impact** severity (critical/high/medium/low)

**Load context:**
- Related task/story files (if applicable)
- Recent commits (if regression suspected)
- Error logs and stack traces

**Example Analysis:**
```
Issue: "Login fails when email contains + symbol"

Analysis:
- What: Login endpoint rejects valid emails with + symbol
- When: Always for emails like "user+tag@example.com"
- Where: POST /api/auth/login
- Expected: Email accepted, login succeeds
- Actual: Returns 400 "Invalid email format"
- Impact: Medium (blocks some users)
```

---

### 2. Reproduce Issue

**Create failing test** that demonstrates the bug:

```typescript
describe('[Bug Fix] Login with + symbol in email', () => {
  it('should accept email addresses with + symbol', async () => {
    await User.create({
      email: 'user+tag@example.com',
      password: await bcrypt.hash('SecurePass123!', 12)
    });

    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'user+tag@example.com',
        password: 'SecurePass123!'
      });

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('token');
  });
});
```

**Run test** and verify it fails with expected error.

**Document reproduction steps** for future reference.

---

### 3. Identify Root Cause

**Trace execution path:**
- Use debugger or add temporary logging
- Follow request through middleware → controller → service → database
- Identify exact line/function causing issue

**For the email example:**
```
POST /api/auth/login
  ↓ auth.controller.ts:login()
  ↓ loginSchema.safeParse(req.body)  ← Validation fails here
  ↓ z.string().email()  ← Too strict, rejects + symbol
```

**Document root cause:**
```markdown
**Root Cause:**
- Location: src/schemas/auth.schema.ts:5
- Issue: z.string().email() rejects valid RFC 5322 emails with + symbol
- Why wrong: + symbol is valid in email local part
- Impact: Users with + in email cannot log in
```

**See:** `references/debugging-techniques.md` for common debugging approaches

---

### 4. Implement Fix

**Make minimal change** to fix the issue:

```typescript
// src/schemas/auth.schema.ts

// Custom email regex that allows + symbol (RFC 5322 compliant)
const EMAIL_REGEX = /^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

export const loginSchema = z.object({
  email: z.string().regex(EMAIL_REGEX, 'Invalid email format'),
  password: z.string().min(1, 'Password is required'),
});
```

**Guidelines:**
- Fix ONLY the bug (no refactoring unrelated code)
- Keep change focused and simple
- Add comment explaining why fix is needed
- Avoid over-engineering

---

### 5. Validate Fix

**Run tests in order:**

1. **Failing test** (should now pass)
   ```bash
   npm test -- --testNamePattern="Login with \\+ symbol"
   ```

2. **Related tests** (no regressions)
   ```bash
   npm test auth
   ```

3. **Full test suite** (no unexpected failures)
   ```bash
   npm test
   ```

4. **Manual testing** (if applicable)

**Verify:**
- ✅ Bug test passes
- ✅ All existing tests pass
- ✅ No regressions introduced

---

### 6. Add Edge Case Tests

**Identify related edge cases** that could have similar issues:

```typescript
describe('[Bug Fix] Email validation edge cases', () => {
  it('should accept email with multiple + symbols', async () => { /* ... */ });
  it('should accept email with dots in local part', async () => { /* ... */ });
  it('should accept email with hyphen in domain', async () => { /* ... */ });
  it('should reject email without @ symbol', async () => { /* ... */ });
  it('should reject email without domain extension', async () => { /* ... */ });
});
```

**Run edge case tests** and verify all pass.

---

### 7. Clean Up and Document

**Clean up:**
- Remove debug logging
- Remove commented code
- Ensure code is production-ready

**Document fix:**

Update task file with bug fix record:
```markdown
## Bug Fixes

### Fix: Email validation rejects + symbol

**Date:** 2025-01-15
**Root Cause:** Zod's email() validator too strict
**Changes:** Custom RFC 5322-compliant regex
**Impact:** Users with + in email can now log in
**Tests:** 6 new tests, all passing, no regressions

**Files Changed:**
- src/schemas/auth.schema.ts (3 lines)
- src/__tests__/integration/auth.integration.test.ts (60 lines)
```

**Commit:**
```bash
git commit -m "fix: allow + symbol in email addresses

- Replaced Zod email() with RFC 5322-compliant regex
- Added test for + symbol in email
- Added 5 edge case tests

Fixes: Email validation incorrectly rejected valid emails
Tests: 6 new tests, all passing, no regressions"
```

---

### 8. Present Summary

```markdown
✅ Bug Fixed: Email validation rejects + symbol

**Root Cause:** src/schemas/auth.schema.ts:5 - Zod email() validator too strict
**Fix:** Custom RFC 5322-compliant regex allowing + symbol
**Impact:** Users with + in email can now log in

**Validation:**
- ✅ Bug test passes
- ✅ All existing tests pass (no regressions)
- ✅ 5 edge case tests added, all pass

**Files Changed:**
- Modified: src/schemas/auth.schema.ts (+3 lines)
- Added tests: src/__tests__/integration/auth.integration.test.ts (+60 lines, 6 tests)

**Status:** Committed, task file updated, ready for review
```

---

## Common Scenarios

### Cannot Reproduce Issue

If test doesn't fail as expected:
1. Verify test setup matches reported conditions
2. Check environment differences (dev vs production)
3. Request more information: exact inputs, error messages, logs
4. Document unable to reproduce, ask for clarification

**See:** `references/error-scenarios.md`

### Fix Introduces Regression

If existing tests fail after fix:
1. Analyze which tests broke and why
2. Refine fix to handle both bug and existing cases
3. Never sacrifice existing functionality for bug fix
4. Consider if breaking change is intentional and justified

**See:** `references/error-scenarios.md`

### Issue is Complex (Multiple Root Causes)

If issue has multiple contributing factors:
1. Fix most critical cause first
2. Create separate tests for each cause
3. Fix and validate each cause independently
4. Document all root causes and fixes

---

## Best Practices

1. **Always write failing test first** - Proves bug exists, prevents regressions
2. **Make minimal changes** - Don't refactor unrelated code
3. **Check for regressions** - Run full test suite after fix
4. **Document root cause** - Explain why, not just what changed
5. **Add edge case tests** - One bug often indicates others nearby

---

## Reference Files

- `references/common-patterns.md` - Common bug patterns and fixes
- `references/debugging-techniques.md` - Systematic debugging approaches
- `references/error-scenarios.md` - Handling complex debugging scenarios
- `references/test-examples.md` - Comprehensive test examples

---

## When to Escalate

- Cannot reproduce after multiple attempts with different approaches
- Root cause requires architecture changes
- Fix requires breaking changes affecting multiple systems
- Security vulnerability requiring coordinated disclosure
- Performance issue requiring profiling tools not available

---

*Part of BMAD Enhanced Development Suite*
