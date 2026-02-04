---
name: debug-root-cause-analysis
description: "Use when fixing a bug or analyzing a stack trace. Enforces systematic debugging methodology to prevent shotgun debugging and verify fixes."
author: "Claude Code Learning Flywheel Team"
allowed-tools: ["Read", "Bash", "Grep", "Glob", "Edit"]
version: 1.0.0
last_verified: "2026-01-01"
tags: ["debugging", "root-cause", "analysis", "systematic"]
related-skills: ["test-driven-workflow", "code-navigation"]
---

# Skill: Debug Root Cause Analysis

## Purpose
Prevent "Shotgun Debugging" where agents randomly change code hoping errors vanish. Enforce a scientific method approach to debugging that isolates the root cause before applying fixes, preventing introduction of new bugs while fixing old ones.

## 1. Negative Knowledge (Anti-Patterns)

| Failure Pattern | Context | Why It Fails |
| :--- | :--- | :--- |
| Shotgun Debugging | Changing multiple variables at once | Cannot isolate cause, introduces new bugs |
| Premature Fix | Applying a patch before reproducing failure | Fix is unverified, may not address root cause |
| Log Blindness | Ignoring severity levels or timestamps | Chasing symptoms, not causes |
| Assumption-Based Debugging | "I think it's X" without verification | Wastes time on wrong leads |
| Print Debugging Only | Adding console.logs without structured approach | Creates noise, hard to trace logic flow |
| Copy-Paste Solutions | Applying Stack Overflow answers without understanding | May not fit context, creates technical debt |
| Skipping Reproduction | Attempting fix without reproducing bug | Cannot verify fix works |

## 2. Verified Debugging Procedure

### The Scientific Method for Debugging

```
1. OBSERVE   → Gather evidence (logs, stack traces, user reports)
2. REPRODUCE → Create minimal reproduction case
3. HYPOTHESIZE → Form testable theories about the cause
4. TEST → Verify each hypothesis systematically
5. FIX → Apply minimal fix to root cause
6. VERIFY → Confirm fix resolves issue and doesn't break anything
7. PREVENT → Add regression test
```

### Phase 1: OBSERVE - Gather Evidence

**Collect all available information:**

```bash
# Check application logs
tail -n 100 logs/error.log

# Check recent commits that may have introduced the bug
git log --since="2 days ago" --oneline

# Check for similar errors
grep -r "ErrorMessage" logs/

# Review stack trace carefully
# Note: Line numbers, function names, timestamps
```

**Questions to answer:**
- When did the bug first appear?
- What changed recently (code, dependencies, config)?
- Is it consistent or intermittent?
- What's the exact error message and stack trace?
- What data was being processed when it failed?

### Phase 2: REPRODUCE - Create Minimal Case

**Goal:** Reliably trigger the bug with minimal setup.

```typescript
// Example: Creating a minimal reproduction test
describe('Bug Reproduction', () => {
  it('should reproduce the error when...', async () => {
    // Arrange: Set up minimal conditions
    const input = {
      userId: 'test-user',
      amount: -100  // Hypothesis: negative amounts cause crash
    };

    // Act & Assert: Verify the bug occurs
    await expect(
      processPayment(input)
    ).rejects.toThrow('Cannot process negative amount');
  });
});
```

**If you cannot reproduce:**
- Verify you have the same environment (Node version, dependencies)
- Check if it's environment-specific (production vs development)
- Look for missing configuration or state

### Phase 3: HYPOTHESIZE - Form Theories

**Generate testable hypotheses based on evidence:**

1. **Analyze the stack trace:** Start from the innermost function
2. **Check recent changes:** `git diff main...HEAD`
3. **Review data flow:** Trace how data reaches the failing code
4. **Consider edge cases:** Null values, empty arrays, special characters

**Example hypothesis formation:**
```
Stack trace shows: TypeError: Cannot read property 'id' of undefined
Location: userService.ts:45

Hypothesis 1: User object is undefined when passed to service
Hypothesis 2: User object exists but missing 'id' property
Hypothesis 3: Async race condition, user not loaded yet

Next step: Add logging at userService.ts:44 to check user object
```

### Phase 4: TEST - Verify Hypothesis

**Use the zero-context script to analyze logs:**

```bash
# Run log analysis to find patterns
python .claude/skills/debug-root-cause-analysis/scripts/analyze_logs.py \
  --log-file logs/error.log \
  --error-pattern "TypeError"
```

**Add strategic logging to test hypothesis:**

```typescript
// BEFORE (hypothesis testing)
async function getUserById(id: string) {
  console.log('[DEBUG] getUserById called with:', id);
  const user = await db.users.findOne({ id });
  console.log('[DEBUG] User found:', user);

  if (!user) {
    console.log('[DEBUG] User not found for ID:', id);
    throw new Error('User not found');
  }

  return user;
}
```

**Verify with a test:**
```typescript
it('should handle missing user gracefully', async () => {
  const result = await getUserById('nonexistent-id');
  // If this throws TypeError about 'id', hypothesis 1 is confirmed
});
```

### Phase 5: FIX - Apply Minimal Fix

**Once root cause is confirmed, apply the minimal fix:**

```typescript
// AFTER (minimal fix)
async function getUserById(id: string) {
  const user = await db.users.findOne({ id });

  if (!user) {
    throw new Error(`User not found: ${id}`);
  }

  return user;
}
```

**Principles:**
- Fix ONLY the root cause
- Don't refactor during bug fixing
- Don't add features while fixing bugs
- Keep the fix as simple as possible

### Phase 6: VERIFY - Confirm Fix

**Verification checklist:**

```bash
# 1. Run the reproduction test
npm test -- bug-reproduction.test.ts
# Expected: PASS

# 2. Run full test suite
npm test
# Expected: All tests PASS (no regressions)

# 3. Manual verification (if applicable)
npm run dev
# Test the actual user flow that triggered the bug

# 4. Check logs are clean
tail -f logs/error.log
# Expected: No errors when performing the previously failing action
```

### Phase 7: PREVENT - Add Regression Test

**Convert your reproduction case into a permanent test:**

```typescript
// tests/unit/services/UserService.test.ts
describe('UserService.getUserById', () => {
  it('should throw clear error when user not found', async () => {
    const service = new UserService(mockDb);

    await expect(
      service.getUserById('nonexistent-id')
    ).rejects.toThrow('User not found: nonexistent-id');
  });

  it('should handle null user gracefully', async () => {
    mockDb.users.findOne.mockResolvedValue(null);

    await expect(
      service.getUserById('test-id')
    ).rejects.toThrow('User not found');
  });
});
```

## 3. Zero-Context Scripts

### analyze_logs.py

Located at: `.claude/skills/debug-root-cause-analysis/scripts/analyze_logs.py`

**Purpose:** Parse error logs for frequency, patterns, and correlations.

**Usage:**
```bash
python .claude/skills/debug-root-cause-analysis/scripts/analyze_logs.py \
  --log-file logs/error.log \
  --error-pattern "TypeError|ReferenceError|null" \
  --time-range "last 24h"
```

**Output:**
```
Error Frequency Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TypeError: Cannot read property 'id': 47 occurrences
  First seen: 2026-01-01 10:23:45
  Last seen:  2026-01-01 14:32:10
  Peak time:  2026-01-01 12:00-13:00 (23 errors)

  Stack trace (most common):
    at userService.ts:45
    at authMiddleware.ts:89

ReferenceError: user is not defined: 3 occurrences
  ...
```

## 4. Debugging Workflow for Agents

### When you encounter a bug or error:

1. **Stop and Observe:**
   - Don't immediately change code
   - Read the full error message and stack trace
   - Note the file, line number, and error type

2. **Gather Context:**
   ```bash
   # What files are involved?
   grep -r "functionName" src/

   # What changed recently?
   git log --oneline -10

   # Are there logs?
   ls -la logs/ && tail logs/error.log
   ```

3. **Create Reproduction Test:**
   - Write a failing test that triggers the bug
   - Make it as minimal as possible
   - Verify it actually fails

4. **Analyze Systematically:**
   - Use the zero-context script to analyze logs
   - Add strategic logging (NOT shotgun console.logs)
   - Test one hypothesis at a time

5. **Apply Minimal Fix:**
   - Fix only the root cause
   - Don't refactor or add features
   - Keep changes minimal and focused

6. **Verify Thoroughly:**
   - Run the reproduction test
   - Run the full test suite
   - Manual verification if needed

7. **Prevent Recurrence:**
   - Convert reproduction to permanent test
   - Document the root cause in comments if complex
   - Consider if similar bugs could exist elsewhere

### Example Agent Session

```
User: "The app crashes when I try to delete a user"

Agent: "I'll debug this systematically using root cause analysis."

[OBSERVE]
Agent: Reading error logs...
Found: TypeError: Cannot read property 'posts' of undefined at deleteUser:67

[REPRODUCE]
Agent: Creating reproduction test...
Writing: tests/bugs/delete-user-crash.test.ts

[RUN TEST]
Agent: Running test to confirm reproduction...
Output: FAIL - Confirmed the crash occurs

[HYPOTHESIZE]
Agent: Stack trace shows crash at line 67 when accessing user.posts.
Hypothesis: user object is undefined before we try to access posts.
Let me check the code...

[READ CODE]
Agent: Reading userService.ts:60-70...
Found issue: deleteUser() doesn't check if user exists before accessing user.posts

[FIX]
Agent: Applying minimal fix - adding null check before accessing user.posts

[VERIFY]
Agent: Running reproduction test...
Output: PASS
Running full test suite...
Output: All tests PASS

[PREVENT]
Agent: Converting reproduction test to permanent regression test
Committing: "fix: add null check before accessing user.posts in deleteUser"
```

## 5. Failed Attempts (Negative Knowledge Evolution)

### ❌ Attempt: Debug by commenting out code
**Context:** Tried to isolate bug by commenting out sections
**Failure:** Changed program behavior, couldn't identify actual cause
**Learning:** Use logging and breakpoints, not code modification

### ❌ Attempt: Apply fix before confirming root cause
**Context:** Saw similar bug on Stack Overflow, applied their solution
**Failure:** Didn't fix our bug, introduced new edge case
**Learning:** Always verify the root cause matches before applying fixes

### ❌ Attempt: Add try-catch around everything
**Context:** Wrapped failing code in try-catch to "fix" errors
**Failure:** Silenced errors, made debugging harder, root cause unfixed
**Learning:** Fix the cause, don't suppress the symptom

### ❌ Attempt: Debug in production
**Context:** Couldn't reproduce locally, added logging to production
**Failure:** Exposed sensitive data in logs, caused performance issues
**Learning:** Reproduce locally or use proper observability tools

### ❌ Attempt: Multi-variable changes
**Context:** Changed error handling AND data validation AND logging
**Failure:** Bug disappeared but couldn't identify which change fixed it
**Learning:** Change one variable at a time, verify after each change

## 6. Common Bug Categories

### Null/Undefined Errors
- **Symptom:** TypeError: Cannot read property 'X' of undefined
- **Common causes:** Missing null checks, async race conditions
- **Fix approach:** Add null checks, ensure async operations complete

### Type Errors
- **Symptom:** Type mismatch, unexpected type coercion
- **Common causes:** Weak typing, incorrect assumptions
- **Fix approach:** Add type guards, validate inputs

### Race Conditions
- **Symptom:** Intermittent failures, works sometimes
- **Common causes:** Async operations not awaited, shared state
- **Fix approach:** Proper async/await, eliminate shared mutable state

### Off-by-One Errors
- **Symptom:** Array index out of bounds, fencepost errors
- **Common causes:** Loop conditions, array slicing
- **Fix approach:** Careful boundary analysis, add tests for edge cases

### Configuration Errors
- **Symptom:** Works locally, fails in production
- **Common causes:** Missing env vars, different configurations
- **Fix approach:** Validate configuration on startup, use same config locally

## 7. Governance
- **Token Budget:** ~495 lines (within 500 limit)
- **Dependencies:** Python 3.8+ for log analysis script
- **Pattern Origin:** Scientific Method, Systematic Debugging (Andreas Zeller)
- **Maintenance:** Update anti-patterns as new failure modes discovered
- **Verification Date:** 2026-01-01
