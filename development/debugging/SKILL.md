---
name: debugging
description: Auto-triggered debugging skill for bug/issue diagnosis and fix. Runs systematic root cause analysis, unit tests, deep tracing, and implements fixes.
---

# Comprehensive Debugging Skill

Expert debugging workflow for diagnosing and fixing issues in the Supplier Management System codebase. Auto-triggers when bug/issue-related keywords are detected.

## Auto-Trigger Keywords

The skill activates when messages contain:
- **Bug/Issue**: "bug", "issue", "problem", "error", "broken", "not working"
- **Failures**: "failed", "failure", "crash", "exception", "error"
- **Unexpected Behavior**: "unexpected", "should be", "not as expected", "wrong"
- **Performance**: "slow", "timeout", "performance", "hangs"
- **Data Integrity**: "corruption", "mismatch", "incorrect data", "balance wrong"
- **Concurrency**: "race condition", "concurrent", "lock", "conflict"

## Debugging Workflow (7 Phases)

### Phase 1: Symptom Collection & Reproduction ✓

**Objective**: Understand what's broken and make it happen consistently

1. **Gather Symptom Information**
   - What is the user experiencing?
   - When did it start happening?
   - Is it reproducible or intermittent?
   - Any error messages or log entries?
   - Affected components/modules?

2. **Ask Clarifying Questions**
   - What steps lead to the issue?
   - What was expected vs. what happened?
   - Can you reproduce it on demand?
   - Does it happen in all contexts or specific scenarios?
   - Any recent changes before issue appeared?

3. **Document Reproduction Steps**
   - Create minimal steps to recreate issue
   - Identify scope (single feature, multiple features, system-wide?)
   - Note any prerequisites or state

**Tools Used**: Conversation/question analysis, User descriptions

---

### Phase 2: Environment & Context Analysis ✓

**Objective**: Understand the system state and context

1. **Review Recent Code Changes**
   ```bash
   git log --oneline -20
   git diff HEAD~5 -- relevant/files
   ```
   - Find commits that might have introduced issue
   - Check blame history for modified functions

2. **Examine System State**
   - Check CONFIG settings and defaults
   - Review relevant sheet structure and data
   - Look for related cached data state
   - Check user permissions and environment

3. **Review Related Documentation**
   - Check CLAUDE.md "Gotchas & Known Issues" section
   - Review module responsibilities in CLAUDE.md
   - Look for documented limitations
   - Check for architectural constraints

4. **Check Git History for Similar Issues**
   ```bash
   git log --all --oneline | grep -i "fix"
   git log --all --oneline | grep -i "bug"
   git show <commit-hash>  # Review fix approach
   ```

**Tools Used**: Bash (git commands), Read (documentation)

---

### Phase 3: Unit Test Execution & Analysis ✓

**Objective**: Identify scope and validate assumptions

1. **Locate Relevant Test Files**
   - Test.CacheManager.gs
   - Test.InvoiceManager.gs
   - Test.PaymentManager.gs
   - Test.Integration.gs
   - Test.MasterDatabase.gs

2. **Run Targeted Unit Tests**
   ```bash
   # From Script Editor, run relevant test function
   runPaymentManagerTests()
   runCacheManagerTests()
   testInvoiceManager()
   ```

3. **Analyze Test Results**
   - Which tests pass/fail?
   - Do failures match reported issue?
   - Are there error messages in Logger?
   - Check test coverage of affected code

4. **Document Test Gaps**
   - Is the bug scenario covered by tests?
   - What test would prevent this issue?
   - Create new test case for bug scenario

**Tools Used**: Bash (running tests), Logger analysis, Test file reading

---

### Phase 4: Integration Testing ✓

**Objective**: Understand how modules interact

1. **Review Integration Test Suite**
   - Read Test.Integration.gs
   - Run relevant integration scenarios
   - Check for cross-module failures

2. **Trace Data Flow Through Modules**
   - Entry point (onEdit, batch operation, menu click)
   - Which modules process the data?
   - What's the expected data transformation?
   - Check cache updates after each step

3. **Verify Assumptions**
   - Does invoice get created correctly?
   - Is cache synchronized after payment?
   - Are balances calculated after updates?
   - Are audit logs recorded?

**Tools Used**: Read (integration test analysis), Bash (test execution), Logger

---

### Phase 5: Root Cause Analysis & Deep Trace ✓

**Objective**: Find the exact cause of the issue

1. **Code Inspection of Suspected Module**
   - Read the primary module file
   - Check function that handles reported scenario
   - Look for edge cases not handled
   - Check error handling (try-catch blocks)

2. **Deep Trace Analysis**
   - Follow execution path step-by-step
   - Add console logging to critical points:
     ```javascript
     Logger.log(`[MODULE] Function called with: ${JSON.stringify(data)}`);
     Logger.log(`[MODULE] Cache state: ${JSON.stringify(cache)}`);
     Logger.log(`[MODULE] Result: ${JSON.stringify(result)}`);
     ```
   - Trace data transformations
   - Check variable states at decision points

3. **Common Bug Patterns** (check these first)
   - **Cache Invalidation Timing**: Payment cache updated BEFORE PaymentLog write?
   - **Formula vs Values**: Storing formula strings instead of evaluated values?
   - **Lock Scope Issues**: Lock released too early or held too long?
   - **User Resolution**: Session.getActiveUser() vs UserResolver.getCurrentUser()?
   - **Master Database Mode**: Simple trigger accessing other spreadsheet?
   - **Edge Cases**: Boundary conditions (zero amounts, negative balances)?
   - **Null/Undefined**: Unhandled null values or missing fields?
   - **Type Mismatches**: String vs number, date formatting issues?
   - **Concurrent Access**: Race conditions without proper locking?

4. **Hypothesis Testing**
   - Form specific hypothesis: "Bug occurs because..."
   - Write test case to prove/disprove
   - Add logging to validate hypothesis
   - Trace execution with real data

**Tools Used**: Read (code inspection), Edit (add logging), Bash (run tests), Grep (search patterns)

---

### Phase 6: Fix Implementation ✓

**Objective**: Implement minimal, targeted fix

1. **Design the Fix**
   - What's the smallest change to resolve?
   - Does it align with module responsibilities?
   - Will it break existing functionality?
   - Are there other similar issues?

2. **Implement Fix**
   - Apply minimal change to source file
   - Keep changes focused on root cause
   - Add defensive code if needed
   - Include explanatory comments

3. **Example Fix Patterns**
   ```javascript
   // ❌ BAD: Timing issue
   PaymentCache.clear();  // Cache cleared
   paymentLog.appendRow(...);  // Data added after clear

   // ✅ GOOD: Correct ordering
   paymentLog.appendRow(...);  // Write data first
   PaymentCache.clear();  // Then invalidate cache
   ```

4. **Add Logging for Future Debugging**
   - Log state changes
   - Log error conditions
   - Include context in log messages
   - Use consistent prefixes: `[MODULE] message`

**Tools Used**: Read (understand current code), Edit (implement fix)

---

### Phase 7: Verification & Regression Testing ✓

**Objective**: Prove fix works and doesn't break anything

1. **Test the Specific Bug Scenario**
   - Run reproduction steps
   - Verify issue is gone
   - Check edge cases still work
   - Confirm expected behavior restored

2. **Run Full Test Suite**
   ```bash
   # Run all related tests
   runAllPaymentManagerTests()
   runAllCacheManagerTests()
   runAllInvoiceManagerTests()
   runIntegrationTests()
   ```
   - All tests must pass
   - No new test failures
   - Performance not degraded

3. **Integration Testing**
   - Test with batch operations
   - Test with concurrent edits
   - Test with Master Database mode (if applicable)
   - Test data integrity end-to-end

4. **Create Prevention Test Case**
   - Add test case that would catch this bug
   - Ensure test fails without fix
   - Ensure test passes with fix
   - Document what it prevents

5. **Review for Side Effects**
   - Does fix affect other modules?
   - Are there performance implications?
   - Does caching still work correctly?
   - Are audit logs still recorded?

**Tools Used**: Bash (test execution), Logger (verification), Read (test review)

---

## Investigation Checklist

When starting investigation, verify:

- [ ] Issue is reproducible
- [ ] Reproduction steps documented
- [ ] Recent code changes reviewed (git log)
- [ ] Relevant test files identified
- [ ] Unit tests run and analyzed
- [ ] Integration tests run and analyzed
- [ ] Known gotchas reviewed (CLAUDE.md)
- [ ] Similar past issues checked
- [ ] Root cause identified with evidence
- [ ] Minimal fix designed and implemented
- [ ] Fix tested and verified
- [ ] Full test suite passes
- [ ] Prevention test case added
- [ ] No side effects identified

## Common Issues & Solutions

### Cache Synchronization Issues
**Symptom**: Balance wrong, invoice data stale, payment not applied

**Investigation**:
```bash
git log --oneline | grep -i "cache"
# Find recent cache-related changes
grep -n "updateInvoiceInCache\|PaymentCache.clear\|invalidate" PaymentManager.gs
# Check cache update order
```

**Common Cause**: Cache cleared before sheet write, or updated before SUMIFS formula recalculates

**Fix Pattern**: Always write sheet first, then clear/invalidate cache

### Trigger Context Issues
**Symptom**: Works manually, fails in trigger; "Cannot access other spreadsheets"

**Investigation**:
- Check if accessing Master Database
- Check CONFIG.masterDatabase.connectionMode
- Check trigger type in Script Editor

**Fix Pattern**: Use installable trigger instead of simple trigger for Master Database mode

### User Resolution Issues
**Symptom**: Wrong user recorded, "default@google.com" showing up

**Investigation**:
- Check UserResolver usage in code
- Verify fallback chain works
- Check trigger context

**Fix Pattern**: Use `UserResolver.getCurrentUser()` instead of `Session.getActiveUser()`

### Balance Calculation Issues
**Symptom**: Balance doesn't match, off by payment amount

**Investigation**:
- Check _calculateTransactionImpact logic
- Verify payment type handling
- Check invoice state transitions

**Fix Pattern**: Trace through calculation, verify all payment types handled correctly

### Concurrency Issues
**Symptom**: Intermittent duplicates, race conditions, "Unable to acquire lock"

**Investigation**:
- Check lock scope in PaymentManager
- Verify critical section is protected
- Check batch operation locking

**Fix Pattern**: Ensure locks cover entire critical section, not just part of it

## Deep Trace Logging Template

When adding debugging logs:

```javascript
/**
 * Deep trace for [issue description]
 * Related to: [component/feature]
 * Test case: [reproduction steps]
 */
function debugFunction(data) {
  Logger.log(`[MODULE] Function entry: data=${JSON.stringify(data)}`);

  try {
    const step1 = calculateSomething(data);
    Logger.log(`[MODULE] After step1: result=${JSON.stringify(step1)}`);

    const step2 = updateCache(step1);
    Logger.log(`[MODULE] After step2 (cache): result=${JSON.stringify(step2)}`);
    Logger.log(`[MODULE] Cache state: ${JSON.stringify(CacheManager.getInvoiceData())}`);

    return { success: true, data: step2 };
  } catch (error) {
    Logger.log(`[MODULE] ERROR: ${error.message}`);
    Logger.log(`[MODULE] Stack: ${error.stack}`);
    throw error;
  }
}
```

## Tools Available

- **Read** - Examine source and test files
- **Edit** - Implement fixes and add logging
- **Bash** - Run tests and git commands
- **Grep** - Search for patterns and related code
- **Glob** - Find test files and related modules

## Output Format

For each bug investigation, provide:

1. **Symptom Analysis** - What's broken and under what conditions
2. **Environment Context** - Recent changes, affected modules, state
3. **Test Results** - Unit and integration test findings
4. **Root Cause** - Why the bug occurs with specific evidence
5. **Fix Implementation** - Minimal code change with explanation
6. **Verification** - Testing approach and results
7. **Prevention** - Test case or safeguard to prevent recurrence

## Key Principles

- **Systematic Approach** - Follow phases in order, don't skip steps
- **Evidence-Based** - Use test results, logs, and code evidence
- **Minimal Changes** - Fix root cause, not symptoms
- **Test-First** - Write test for bug before implementing fix
- **Documentation** - Document what went wrong and how to prevent it
- **Prevention** - Always add test case to catch this bug in future

## Related Testing Functions

From codebase (run from Script Editor):
- `runPaymentManagerTests()` - All payment tests
- `runCacheManagerTests()` - All cache tests
- `testInvoiceManager()` - Invoice functionality
- `runIntegrationTests()` - Multi-module scenarios
- `testMasterDatabaseConnection()` - Master DB validation
