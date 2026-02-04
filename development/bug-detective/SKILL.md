---
name: bug-detective
description: Systematic bug hunting combining Sherpa's debugging workflow, Julie's execution tracing, and Goldfish's investigation tracking. Activates for bug fixes with methodical reproduction, test capture, fix, and verification. Use when debugging errors or fixing bugs.
allowed-tools: mcp__sherpa__guide, mcp__sherpa__approach, mcp__julie__fast_search, mcp__julie__trace_call_path, mcp__julie__fast_refs, mcp__julie__fast_goto, mcp__julie__get_symbols, mcp__goldfish__recall, mcp__goldfish__checkpoint, Read, Edit, Write, Bash
---

# Bug Detective Workflow

## Purpose
Conduct **systematic, methodical bug investigations** using detective-style debugging. This workflow combines Sherpa's bug hunt phases, Julie's execution tracing, and Goldfish's investigation logging to find and fix bugs confidently.

## When to Activate
Use when the user:
- **Reports bugs**: "this is broken", "getting an error", "not working"
- **Debugs issues**: "debug this", "find the bug", "why is this failing"
- **Investigates problems**: "investigate this error", "track down this issue"
- **Unexpected behavior**: "this should work but doesn't", "weird behavior"

## The Detective Trinity

### 🕵️ Sherpa - Investigation Guidance
- 4-phase bug hunt workflow
- Detective metaphors and encouragement
- Systematic process
- Progress tracking

### 🔍 Julie - Code Investigation Tools
- Semantic error search
- Execution path tracing
- Cross-language navigation
- Reference finding

### 📝 Goldfish - Investigation Log
- Checkpoint discoveries
- Document hypotheses
- Track investigation steps
- Preserve solution

## Bug Detective Orchestration

### Session Start: Check Previous Investigations
```
1. Goldfish recall({ search: "[error/bug description]" })
   → See if similar bug investigated before
2. Learn from previous investigations
3. If same bug → Resume investigation
4. If new → Start fresh investigation
```

### Phase 1: 🔍 Reproduce & Isolate

**Sherpa Activation:**
```
approach({ workflow: "bug-hunt" })
guide() → "Phase 1: Reproduce & Isolate - Find the crime scene!"
```

**Error Discovery:**
User reports: "Getting 'Invalid token' error"

**Julie Investigation:**
```
fast_search({ query: "Invalid token", mode: "lines" })
→ Find all error message locations

fast_goto on error location
→ Jump to where error is thrown

trace_call_path({ symbol: "validateToken", direction: "upstream" })
→ See what calls this (who triggers the error?)
```

**Reproduce Reliably:**
- Identify exact steps to trigger
- Determine consistent vs intermittent
- Gather error messages and stack traces
- Understand expected vs actual behavior

**Goldfish Investigation Log:**
```
checkpoint({
  description: "Isolated 'Invalid token' error: thrown in validateToken() when refresh tokens expire, called from authenticate() middleware",
  tags: ["bug-hunt", "investigation", "phase-1", "auth"]
})
```

**Sherpa Progress:**
```
guide({ done: "reproduced bug: token validation fails with expired refresh tokens" })
→ 🕵️ "Excellent detective work! The case is taking shape..."
→ "Phase 2: Capture in Test"
```

### Phase 2: ✅ Capture in Test

**Sherpa Guidance:**
```
guide() → "Phase 2: Capture in Test - Document the crime!"
```

**Julie Pattern Search:**
```
fast_search({ query: "token validation test examples", mode: "semantic" })
→ Find similar test patterns

get_symbols({ file: "tests/auth.test.ts", mode: "structure" })
→ See existing test structure
```

**Write Failing Test:**
- Reproduce bug in test
- Verify test fails for the right reason
- Document expected behavior
- Ensure test is clear and minimal

**Run test → Fails (as expected!)**

**Goldfish Checkpoint:**
```
checkpoint({
  description: "Created failing test: 'should handle expired refresh tokens gracefully' - reproduces Invalid token error",
  tags: ["bug-hunt", "test", "phase-2", "auth"]
})
```

**Sherpa Progress:**
```
guide({ done: "wrote failing test that reproduces the expired token bug" })
→ 🎯 "Perfect! You've documented the crime. Now let's solve it!"
→ "Phase 3: Fix the Bug"
```

### Phase 3: 🔧 Fix the Bug

**Sherpa Guidance:**
```
guide() → "Phase 3: Fix - Solve the mystery!"
```

**Julie Code Understanding:**
```
get_symbols({ file: "src/auth/jwt.ts", mode: "full" })
→ Understand token validation logic

trace_call_path({ symbol: "validateToken", direction: "downstream" })
→ See what validateToken calls (jwt.verify, etc.)

fast_refs({ symbol: "refreshToken" })
→ See all refresh token usage
```

**Analysis:**
- Root cause: Not checking refresh token expiration
- Solution: Add expiration check before validation
- Impact: Minimal, isolated to validateToken

**Implement Fix:**
```typescript
// Add expiration check
if (isRefreshTokenExpired(token)) {
  throw new TokenExpiredError('Refresh token expired');
}
```

**Run test → Passes! ✅**

**Goldfish Checkpoint:**
```
checkpoint({
  description: "Fixed expired token bug: added expiration check in validateToken, test now passes",
  tags: ["bug-hunt", "fix", "phase-3", "auth", "test-pass"]
})
```

**Sherpa Progress:**
```
guide({ done: "implemented fix for expired tokens, failing test now passes" })
→ 🎉 "Case solved! The bug has been caught!"
→ "Phase 4: Verify & Prevent"
```

### Phase 4: ✅ Verify & Prevent

**Sherpa Guidance:**
```
guide() → "Phase 4: Verify - Close the case with confidence!"
```

**Verification Steps:**
1. **Run all tests** → Ensure no regressions
2. **Test manually** → Verify actual bug fixed
3. **Check edge cases** → Add more tests if needed

**Julie Impact Analysis:**
```
fast_refs({ symbol: "validateToken" })
→ See all usage points (15 locations)
→ Verify fix doesn't break anything
```

**Prevention:**
- Add tests for related scenarios
- Document the fix
- Update error messages for clarity

**Goldfish Final Checkpoint:**
```
checkpoint({
  description: "Bug hunt complete: expired token handling fixed and verified. Added 3 additional tests for edge cases. All 18 auth tests passing.",
  tags: ["bug-hunt", "complete", "phase-4", "auth", "verified"]
})
```

**Sherpa Completion:**
```
guide({ done: "verified fix across all test cases, added prevention tests, all tests green" })
→ 🌟 "Bug Hunt Complete! Detective work at its finest!"
→ Potential milestone: "🏆 Milestone: Bug Detective Mastery!"
```

## Complete Example: Race Condition Bug

```markdown
User: "Users are getting randomly logged out"

=== SESSION START ===

→ Goldfish: recall({ search: "logout session" })
  No previous investigation. New case!

=== PHASE 1: REPRODUCE & ISOLATE ===

→ Sherpa: approach({ workflow: "bug-hunt" })
  🕵️ Bug Hunt Workflow activated!

→ Sherpa: guide()
  "Phase 1: Reproduce & Isolate"

→ Julie: fast_search({ query: "logout session destroy", mode: "semantic" })
  Found: session.ts, auth-middleware.ts

→ Julie: trace_call_path({ symbol: "logout", direction: "both" })
  Execution flow:
  - logout() calls session.destroy()
  - authenticate() checks session.exists()
  - Race condition: destroy happens while checking!

→ Goldfish: checkpoint({
    description: "Isolated race condition: session.destroy() can execute during session.exists() check, causing random logouts",
    tags: ["bug-hunt", "investigation", "race-condition"]
  })

→ Sherpa: guide({ done: "found race condition between session destroy and exists check" })
  🕵️ "Aha! A race condition! Classic mystery..."

=== PHASE 2: CAPTURE IN TEST ===

→ Sherpa: guide()
  "Phase 2: Capture in Test"

→ Write test with concurrent operations:
  - Simulate logout during auth check
  - Reproduce race condition
  - Test fails (intermittently - race condition!)

→ Goldfish: checkpoint({
    description: "Created failing test: 'should handle concurrent logout during auth' - reproduces race condition",
    tags: ["bug-hunt", "test", "phase-2", "race-condition"]
  })

→ Sherpa: guide({ done: "wrote test that reproduces race condition" })
  🎯 "Documented the crime!"

=== PHASE 3: FIX THE BUG ===

→ Sherpa: guide()
  "Phase 3: Fix the Bug"

→ Julie: get_symbols({ file: "src/session.ts", mode: "full" })
  Understand session management

→ Solution: Add mutex/lock for session operations

→ Implement fix with proper locking

→ Test passes consistently! ✅

→ Goldfish: checkpoint({
    description: "Fixed race condition: added mutex for session operations, test now passes consistently",
    tags: ["bug-hunt", "fix", "phase-3", "race-condition"]
  })

→ Sherpa: guide({ done: "fixed race condition with mutex, test passes" })
  🎉 "Mystery solved!"

=== PHASE 4: VERIFY & PREVENT ===

→ Sherpa: guide()
  "Phase 4: Verify & Prevent"

→ Run full test suite → All pass ✅
→ Stress test with 100 concurrent operations → Stable! ✅

→ Julie: fast_refs({ symbol: "session" })
  Check all session usage → All safe

→ Goldfish: checkpoint({
    description: "Race condition fix verified: stress tested with 100 concurrent ops, added 5 concurrency tests, all 23 session tests pass",
    tags: ["bug-hunt", "complete", "verified", "race-condition"]
  })

→ Sherpa: guide({ done: "verified fix under stress, added prevention tests" })
  🌟 "Bug Hunt Complete! Case closed!"
```

## Investigation Techniques

### Trace Execution Paths
```
trace_call_path shows WHO calls buggy code:
- Identify entry points
- See call chain
- Understand flow
```

### Semantic Error Search
```
fast_search for error patterns:
- Find related errors
- See similar issues
- Learn from fixes
```

### Reference Analysis
```
fast_refs shows WHERE code is used:
- Impact analysis
- Breaking change detection
- Edge case discovery
```

## Goldfish Investigation Patterns

### Discovery Checkpoints
```
checkpoint({
  description: "Discovered: [finding]",
  tags: ["discovery", "hypothesis"]
})
```

### Hypothesis Checkpoints
```
checkpoint({
  description: "Hypothesis: [theory about root cause]",
  tags: ["hypothesis", "analysis"]
})
```

### Solution Checkpoints
```
checkpoint({
  description: "Solution: [fix description]",
  tags: ["solution", "fix"]
})
```

**Benefit:** Investigation trail is preserved even across context resets!

## Key Behaviors

### ✅ DO
- Recall similar bugs at start
- Follow all 4 phases systematically
- Use Julie to trace execution
- Checkpoint discoveries immediately
- Write failing test before fixing
- Verify no regressions
- Document solution clearly

### ❌ DON'T
- Jump to conclusions without reproducing
- Skip writing test (defeats the purpose!)
- Fix without understanding root cause
- Ignore similar past bugs
- Forget to checkpoint investigation steps
- Skip verification phase

## Success Criteria

Bug Detective succeeds when:
- Bug reliably reproduced
- Captured in failing test
- Root cause understood
- Fix implemented and tested
- All tests pass (including new ones)
- Investigation documented
- Prevention measures in place

## Performance

- Julie trace_call_path: ~200ms
- Julie error search: <100ms
- Goldfish checkpoint: ~10ms
- Total investigation: Depends on bug complexity

**Result:** Systematic debugging that finds root causes fast!

---

**Remember:** Every good detective documents their investigation. Sherpa guides, Julie traces, Goldfish preserves. Together, they solve the mystery!
