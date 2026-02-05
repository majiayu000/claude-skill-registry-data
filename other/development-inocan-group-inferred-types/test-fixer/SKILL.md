---
name: test-fixer
description: Fix failing tests based on failure reports, verify fixes, and iterate until all tests pass. This skill should be used after test-executor generates failure reports, providing systematic debugging and fixing strategies that work with any framework or language.
---

# Test Fixer Skill

## Purpose

Systematically fix failing tests by analyzing failure reports, diagnosing root causes, implementing fixes, and verifying corrections. Works universally with any testing framework, language, or project structure through generic debugging strategies.

## When to Use This Skill

Use this skill when:

- `test-executor` has generated a failure report (test-failures.md)
- Tests are failing and need fixes
- Need systematic approach to debugging test failures
- Want to iterate on fixes until tests pass
- Need to understand and resolve test failure patterns

## Fixing Workflow

### Phase 1: Read and Understand Failures

1. **Read Failure Report**
   - Locate test-failures.md
   - Review summary statistics
   - Identify number and types of failures
   - Prioritize fixes (critical → non-critical)

2. **Analyze Failure Patterns**
   - Are failures related? (common root cause)
   - Are failures independent?
   - Which failure to fix first?

3. **Categorize by Type**
   - Timeout errors
   - Assertion failures
   - Connection errors
   - Authentication errors
   - Data errors
   - Environment issues

### Phase 2: Diagnose Root Cause

For each failing test:

1. **Read Error Message Carefully**
   - Extract key information
   - Identify line numbers and files
   - Understand what was expected vs actual

2. **Locate Relevant Code**
   - Find test file
   - Find implementation code being tested
   - Read both test and implementation

3. **Reproduce Locally (if possible)**
   - Run single failing test
   - Observe behavior
   - Add debug logging if needed

4. **Identify Root Cause**
   - Is test correct and implementation wrong?
   - Is test incorrect and implementation right?
   - Is environment/setup the issue?
   - Is test flaky/timing-dependent?

### Phase 3: Implement Fix

1. **Choose Fix Strategy**
   - Fix implementation code
   - Fix test code
   - Fix environment/configuration
   - Fix test data/fixtures

2. **Implement Fix**
   - Make minimal change to fix issue
   - Don't over-engineer
   - Maintain code style consistency
   - Add comments if fix is non-obvious

3. **Local Verification**
   - Run fixed test locally
   - Verify it passes consistently
   - Check no regressions in related tests

### Phase 4: Verify and Iterate

1. **Re-run Test**
   - Use `test-executor` to re-run
   - Or run test command directly
   - Capture results

2. **If Test Passes:**
   - Mark test as fixed
   - Update test-failures.md or create test-fixes.md
   - Move to next failing test

3. **If Test Still Fails:**
   - Analyze new error (may be different)
   - Refine diagnosis
   - Implement additional fix
   - Iterate

4. **Once All Tests Pass:**
   - Update implementation plan
   - Document any significant changes
   - Ready for next phase or completion

## Debugging Strategies by Failure Type

### 1. Timeout Errors

**Symptom:**
```
Error: Timeout waiting for element to appear
Error: Request timeout after 30000ms
```

**Common Causes:**
- Service not running
- Service too slow
- Incorrect wait condition
- Element never appears (wrong selector)

**Diagnostic Steps:**
1. Verify all services are running
2. Manually test the operation (browser, curl, etc.)
3. Check response times in service logs
4. Verify selectors/conditions are correct

**Fix Strategies:**
- Start missing services
- Optimize slow queries/operations
- Increase timeout (if legitimately slow)
- Fix incorrect wait conditions
- Use better selectors (E2E tests)

**Example Fix:**
```typescript
// Before: Too short timeout
await page.waitForSelector('.success-message', { timeout: 1000 });

// After: Reasonable timeout
await page.waitForSelector('.success-message', { timeout: 5000 });
```

### 2. Assertion Failures

**Symptom:**
```
Expected: 200
Received: 404

AssertionError: expected 'success' to equal 'error'
```

**Common Causes:**
- Logic error in implementation
- Incorrect test expectations
- Data fixtures incorrect
- API contract mismatch

**Diagnostic Steps:**
1. Understand what test expects
2. Understand what implementation returns
3. Determine which is correct
4. Check data flowing through system

**Fix Strategies:**
- Fix implementation logic (if test is correct)
- Fix test expectations (if implementation is correct)
- Fix data fixtures
- Align API contract

**Example Fix (Implementation Error):**
```csharp
// Before: Wrong status code
return NotFound(); // 404

// After: Correct status code
return Ok(result); // 200
```

**Example Fix (Test Error):**
```typescript
// Before: Wrong expectation
expect(response.status).toBe(404);

// After: Correct expectation
expect(response.status).toBe(200);
```

### 3. Connection Errors

**Symptom:**
```
Error: connect ECONNREFUSED 127.0.0.1:5001
Error: getaddrinfo ENOTFOUND localhost
```

**Common Causes:**
- Service not running
- Wrong port or URL
- Firewall blocking connection
- Service crashed

**Diagnostic Steps:**
1. Check if service process is running
2. Verify port matches configuration
3. Test connection manually (curl, browser)
4. Check service logs for crashes

**Fix Strategies:**
- Start the service
- Fix port/URL in configuration
- Restart crashed service
- Check firewall rules

**Example Fix:**
```typescript
// Before: Wrong port
const API_URL = 'http://localhost:3000';

// After: Correct port
const API_URL = 'http://localhost:5001';
```

### 4. Authentication Errors

**Symptom:**
```
Error: 401 Unauthorized
Error: 403 Forbidden
Error: Invalid token
```

**Common Causes:**
- Missing authentication header
- Expired token
- Wrong credentials
- Incorrect auth flow

**Diagnostic Steps:**
1. Check if token is being sent
2. Verify token is valid
3. Check token hasn't expired
4. Verify auth flow is correct

**Fix Strategies:**
- Add authentication header
- Refresh/regenerate token
- Use correct credentials
- Fix auth flow logic

**Example Fix:**
```typescript
// Before: Missing auth header
const response = await fetch('/api/forms');

// After: Include auth header
const response = await fetch('/api/forms', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### 5. Data Errors

**Symptom:**
```
TypeError: Cannot read property 'name' of undefined
NullReferenceException: Object reference not set
```

**Common Causes:**
- Missing data in response
- Null/undefined values
- Wrong data shape
- Database empty/wrong state

**Diagnostic Steps:**
1. Log actual data being received
2. Check database state
3. Verify API response structure
4. Check data fixtures

**Fix Strategies:**
- Add null checks
- Fix data fixtures
- Ensure database has required data
- Fix API to return correct shape

**Example Fix:**
```typescript
// Before: No null check
const userName = user.name.toUpperCase();

// After: Safe null check
const userName = user?.name?.toUpperCase() ?? 'Unknown';
```

### 6. Environment / Configuration Issues

**Symptom:**
```
Error: Missing environment variable
Error: Configuration not found
Error: Module not found
```

**Common Causes:**
- Missing .env file
- Missing dependencies
- Wrong configuration
- Environment variables not set

**Diagnostic Steps:**
1. Check .env file exists
2. Verify dependencies installed
3. Check configuration files
4. Verify environment variables

**Fix Strategies:**
- Create .env file
- Install dependencies
- Fix configuration
- Set environment variables

**Example Fix:**
```bash
# Create missing .env file
cp .env.example .env

# Install missing dependencies
npm install

# Set environment variable
export DATABASE_URL="postgresql://localhost:5432/db"
```

## Systematic Debugging Approach

### The 5 Whys Technique

Ask "why" repeatedly to find root cause:

**Example:**
1. **Why did test fail?** → API returned 500
2. **Why did API return 500?** → Database query failed
3. **Why did query fail?** → Connection string wrong
4. **Why is connection string wrong?** → .env file missing
5. **Why is .env file missing?** → Not in .gitignore, not documented

**Root cause:** Missing .env file
**Fix:** Create .env file and document in README

### Rubber Duck Debugging

Explain the failure out loud (or in comments):

```
# What should happen:
# 1. User clicks submit
# 2. Form data is sent to API
# 3. API validates and saves to DB
# 4. API returns 200 with submission ID
# 5. UI shows success message

# What actually happens:
# 1-2: OK
# 3: API validation fails ← Problem here!
# 4-5: Never reached

# Why does validation fail?
# - Required field "email" is missing
# - Frontend not sending email field ← Root cause!
```

### Binary Search Debugging

For complex failures, narrow down:

1. **Add logging at midpoint of flow**
2. **Run test**
3. **Check logs**
4. **If before midpoint:** Search first half
5. **If after midpoint:** Search second half
6. **Repeat** until issue found

### Comparative Debugging

Compare working vs failing:

- Working test vs failing test (what's different?)
- Working environment vs failing environment
- Previous commit (working) vs current commit (failing)

## Fixing Multiple Related Failures

### Pattern Recognition

If multiple tests fail similarly:

**Example:**
```
Test A: Expected 200, got 500
Test B: Expected 200, got 500
Test C: Expected 200, got 500
```

**Pattern:** All tests hitting same endpoint fail
**Root cause:** Likely in shared code (endpoint implementation)
**Fix:** Fix endpoint once, all tests should pass

### Dependency Fixing

Fix failures in dependency order:

**Example:**
```
Test A: Create user (fails)
Test B: Login as user (fails - depends on A)
Test C: User updates profile (fails - depends on A, B)
```

**Fix order:** A → B → C
- Fix Test A first
- Tests B and C may pass automatically

### Batch Fixing

For independent failures:
- Fix multiple in parallel (if team)
- Fix in order of priority/severity
- Re-run all tests together at end

## Verification

### Single Test Verification

```bash
# Run only the fixed test
npm test -- specific-test.spec.ts
dotnet test --filter TestName
pytest tests/test_specific.py::test_function
```

### Regression Check

After fixing, ensure no new failures:

```bash
# Run full test suite
npm test
dotnet test
pytest
```

### Multiple Runs (Flaky Tests)

If test seems flaky:

```bash
# Run multiple times to verify stability
for i in {1..5}; do npm test; done
```

If still flaky, fix the flakiness (timing issues, race conditions, etc.)

## Documenting Fixes

### In Code Comments

For non-obvious fixes:

```typescript
// Fix: Added timeout to wait for async operation to complete
// Issue: Test was checking result before operation finished
await new Promise(resolve => setTimeout(resolve, 100));
```

### In test-fixes.md

Create report of fixes:

```markdown
# Test Fixes Report

**Date:** [Date]

## Fixed Tests

### Test: User can submit form
**Issue:** Timeout waiting for success message
**Root Cause:** Service startup slow in CI environment
**Fix:** Increased timeout from 1s to 5s
**File:** `tests/e2e/form-submission.spec.ts:42`

### Test: API validates SIRET
**Issue:** Validation always failed
**Root Cause:** Wrong validation logic (bug in implementation)
**Fix:** Corrected Luhn algorithm in ValidationService
**File:** `src/services/ValidationService.cs:67`
```

### In Implementation Plan

Update plan with any significant changes:

```markdown
- [x] Phase 4: Testing (100%)
  **Note:** Fixed timeout issues in E2E tests, fixed SIRET validation bug
```

## Iteration with test-executor

### Fix Loop

```
1. test-executor runs tests → test-failures.md
2. test-fixer fixes failures
3. test-executor re-runs tests
   → If all pass: Done!
   → If still failures: Go to step 2
```

### Incremental Progress

Track progress across iterations:

```markdown
# Test Failure Report - Iteration 1
- Failed: 10/15 tests

# Test Failure Report - Iteration 2
- Failed: 3/15 tests (7 fixed!)

# Test Failure Report - Iteration 3
- Failed: 0/15 tests (All passing! ✅)
```

## Tips for Effective Test Fixing

1. **Read Error Messages Carefully**: They often tell you exactly what's wrong
2. **Start Simple**: Check obvious things first (services running, config correct)
3. **One Fix at a Time**: Don't change multiple things simultaneously
4. **Verify Locally**: Run test locally before marking fixed
5. **Consider Root Cause**: Fix the cause, not just the symptom
6. **Document Non-Obvious Fixes**: Help future developers
7. **Check for Regressions**: Ensure fix doesn't break other tests
8. **Ask for Help**: If stuck, consult user or team
9. **Take Breaks**: Fresh eyes spot issues faster
10. **Learn Patterns**: Similar failures often have similar fixes

## Common Mistakes to Avoid

❌ **Changing Tests to Match Bugs**: Fix implementation, not tests
❌ **Adding Arbitrary Delays**: Understand why timing is an issue
❌ **Ignoring Flaky Tests**: Fix flakiness, don't just retry
❌ **Skipping Verification**: Always re-run test after fix
❌ **Fixing Symptoms**: Find and fix root cause
❌ **Over-Complicating**: Simple fixes are usually best

## Bundled Resources

- `references/debugging-strategies.md` - Universal debugging strategies
- `references/common-test-failures.md` - Common failures and solutions
