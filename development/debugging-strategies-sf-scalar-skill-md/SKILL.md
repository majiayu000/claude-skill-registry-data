---
name: debugging-strategies
description: When isolating and fixing unpredictable or complex software bugs.
version: 2.0.0
category: dev-tools
tags: [dev-tools, debugging, troubleshooting]
skill_type: debugging
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1400
dangerous: false
requires_review: false
security_level: safe
dependencies: []
triggers: [bug, debug, error, failing test, reproduction]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: false }
  shell: { execute: true }
input_requirements: [failing code or test, reproducible scenario]
output_contract: [failing test, root cause identified, fix minimal]
failure_conditions: [cannot reproduce bug, test passes but bug exists, no hypothesis formed]
last_updated: 2026-05-15
---

# Debugging Strategies

## Purpose
"Guess and check" programming wastes hours. This skill replaces randomness with the scientific method: reproduce the bug reliably, isolate the failing component via binary search, formulate testable hypotheses, and apply minimal fixes. The goal is deterministic bug resolution, not random fixes that seem to work.

## When to use
- Investigating a defect reported in production
- Facing a failing test with no obvious root cause
- Understanding unfamiliar or undocumented legacy code
- Debugging intermittent failures (flaky tests)

## When NOT to use
- Performance optimization (use Caching Strategies or Database Query Optimization)
- Code review (use Code Review Guidelines)
- Architecture decisions (different concern)

## Inputs required
- Failing code, test, or end-to-end scenario
- Ability to reproduce the failure
- Source code and execution environment

## Workflow
1. **Reproduce the Bug**: Consistently replicate the failure state. If you CANNOT reproduce it, STOP (get more details). Write a failing test.
2. **Isolate the Subsystem**: Use binary search (comment out code halves, use `git bisect`, add logging) to locate the exact module causing the issue
3. **Formulate Hypothesis**: Propose WHY the failure is happening based on logs, stack traces, and code inspection
4. **Test Hypothesis**: Add targeted logging or step through debugger to verify assumptions about state/variables at runtime
5. **Apply Minimal Fix**: Change ONLY what's necessary to make the test pass (single line if possible)
6. **Verify Fix**: Confirm the failing test now passes, and no other tests break
7. **Add Regression Test**: Ensure this bug never reoccurs

## Rules
- MUST establish a reproducible test BEFORE changing code
- MUST only change one variable or line at a time during hypothesis testing
- MUST NOT apply multiple changes simultaneously (makes diagnosis impossible)
- MUST use binary search for isolation (comment out halves, not random guessing)
- MUST formulate a hypothesis before adding logging or changes
- MUST keep the fix minimal (change only what caused the bug)

## Anti-patterns
- **Shotgun Debugging**: Randomly changing configuration or code until things "seem to work"
- **Blaming the Compiler**: Assuming the language/framework is broken before checking your code
- **Adding Debug Code**: Adding excessive logging everywhere instead of targeted logging
- **Not Isolating**: Staring at code trying to reason about it instead of actually testing
- **Fixing Symptoms**: "Fixing" the error message instead of fixing the root cause
- **Multiple Changes**: Changing 5 things at once, then one works, but you don't know which

## Failure conditions
- Bug cannot be reproduced
- Test passes but bug still exists in production
- No hypothesis formed before debugging
- Fix applied without verification test
- Multiple changes applied simultaneously

## Validation checklist
- [ ] Failing test or scenario created and reproducible
- [ ] Bug can be consistently reproduced every time
- [ ] Subsystem isolated (know which file/function is failing)
- [ ] Hypothesis is specific (not "something is wrong")
- [ ] Targeted logging/breakpoints confirm hypothesis
- [ ] Fix is minimal (only necessary changes)
- [ ] Failing test now passes
- [ ] No other tests broken
- [ ] Regression test added
- [ ] Root cause documented in code comments or commit

## Output format
- **Failing test**: Automated test that reproduces the bug
- **Minimal fix**: Code change addressing root cause only
- **Regression test**: Test ensuring bug never reoccurs
- **Documentation**: Comment explaining root cause and why fix works

## Security considerations
- Debug logging MUST NOT leak sensitive data (credentials, PII)
- Breakpoint debugging MUST NOT be left in production code
- Temporary logging MUST be removed before commit
- Hypothesis testing MUST NOT modify production data

## Agent execution notes
- Agent MAY: Add failing tests, add targeted logging, apply minimal fixes, use git bisect
- Agent MUST NEVER: Make multiple changes simultaneously, apply fixes without tests, leave debug code
- Agent MUST ASK: Before running expensive operations, before modifying production-like data
- Agent MUST VALIDATE: Failing test reproduces bug, fix is minimal, regression test present

## Example

**❌ Anti-pattern (Shotgun debugging, multiple changes, no hypothesis):**
```javascript
// User reports: "Login sometimes fails"
// Response: randomly change stuff

// Change 1: Remove cache (wild guess)
Cache.clear();

// Change 2: Increase timeout (wild guess)
timeout = 5000;

// Change 3: Retry login (wild guess)
retry();

// Change 4: Restart server
process.restart();

// "It works now!" - but which change fixed it?
```

**✅ Correct pattern (Systematic, hypothesis-driven, minimal fix):**
```javascript
// User reports: "Login sometimes fails with 'Session token invalid'"

// 1. Create failing test
test('login should succeed with valid credentials', async () => {
  const user = await login('user@test.com', 'password');
  expect(user).toBeDefined();
});

// 2. Run test 10 times - fails randomly - good, reproducible
for (let i = 0; i < 10; i++) {
  npm test; // Run failing test
}

// 3. Isolate subsystem with logging
function validateToken(token) {
  console.log('Token:', token, 'Expires:', token.expiresAt, 'Now:', Date.now());
  if (token.expiresAt < Date.now()) {
    throw new Error('Token expired');
  }
}

// 4. Hypothesis: Token generation race condition in parallel requests
// 5. Test: Run login twice simultaneously
Promise.all([login(...), login(...)]);
// Confirm: Second request gets token from first request but with different expiresAt

// 6. Minimal fix: Add mutex to token generation
const mutex = new Mutex();
async function generateToken() {
  return mutex.runExclusive(async () => {
    return createToken();
  });
}

// 7. Verify: Failing test now passes 100 times
// 8. Add regression test
test('concurrent logins should not fail', async () => {
  const results = await Promise.all([
    login('user@test.com', 'password'),
    login('user@test.com', 'password')
  ]);
  expect(results.every(r => r)).toBe(true);
});
```
