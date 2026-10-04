---
name: verifying-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

0. TDD COMPLIANCE: Have you followed practicing-tdd skill?
   - See TDD Compliance Certification (below)
   - If NO: Stop. You violated TDD. Start over.

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. CAPTURE: Copy complete output to include in your message
5. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
6. REQUIREMENTS: Have you verified all requirements? (see checklist)
7. TDD CERTIFIED: Have you certified TDD compliance? (see below)
8. CODE REVIEW: Have you obtained code review approval? (see gate below)
9. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## TDD Compliance Certification

BEFORE claiming work complete, certify TDD compliance:

For each new function/method implemented:

- [ ] **Function name**: [function_name]
  - **Test name**: [test_function_name]
  - **Watched fail**: YES / NO (if NO, explain why)
  - **Failure reason**: [expected failure message you saw]
  - **Implemented minimal code**: YES / NO
  - **Watched pass**: YES / NO
  - **Refactored**: YES / NO / N/A

### Example Certification:

```
## TDD Compliance Certification

- [x] **Function name**: retryOperation
  - **Test name**: test_retries_failed_operations_3_times
  - **Watched fail**: YES
  - **Failure reason**: "ReferenceError: retryOperation is not defined"
  - **Implemented minimal code**: YES
  - **Watched pass**: YES
  - **Refactored**: YES (extracted delay logic)

- [x] **Function name**: validateEmail
  - **Test name**: test_validates_email_format
  - **Watched fail**: YES
  - **Failure reason**: "ReferenceError: validateEmail is not defined"
  - **Implemented minimal code**: YES
  - **Watched pass**: YES
  - **Refactored**: N/A (implementation already clean)
```

### Requirements:

- **If ANY "NO" answers**: Work is NOT complete. Delete and restart with TDD.
- **This certification MUST be included** in your completion message.
- **One entry required** for each new function/method.
- **"Watched fail" = NO is ONLY acceptable** if explicitly following receiving-reviewing-code (fixing existing untested code).

### Why This Matters:

Making this certification explicit:
- Forces conscious attestation (not vague "I think I followed TDD")
- Creates audit trail of process followed
- Makes rationalization harder (explicit lying vs fuzzy thinking)
- Enables code reviewer to verify TDD compliance

## Code Review Gate

BEFORE claiming work complete:

### When Code Review is MANDATORY:

Code review MUST always be obtained (without exception) for ALL code changes.

**ALL of these MUST be true to proceed WITHOUT review:**

1. Changes are EXCLUSIVELY documentation (*.md files in docs/ directory only)
2. Changes contain ZERO code logic modifications
3. Changes contain ZERO configuration logic modifications

**If ANY of the above is false, code review is MANDATORY.**

This means code review IS MANDATORY for:
- New features (any size, any language/framework)
- Bug fixes (any severity, any language/framework)
- Refactoring (any scope, any language/framework)
- ALL code changes (regardless of lines changed)
- Security-sensitive code
- Performance-critical code
- Public API changes
- Test code changes
- Configuration changes with logic (scripts, build configs)
- Database migrations
- Infrastructure-as-code changes

### Code Review Checklist:

ALL of these MUST be true to claim work complete:

- [ ] **Code review requested**: Used requesting-reviewing-code skill
- [ ] **Review completed**: code-reviewer subagent dispatched and finished
- [ ] **Critical issues**: 0 (MUST be zero, no exceptions)
- [ ] **Important issues**: 0 (MUST be zero OR converted to tracked issue with ID)
- [ ] **Review status**: Approved / Approved with minor items
- [ ] **Review reference**: [link to review output or summary]

### EXCEPTIONS (ONLY these, no others):

Valid exceptions (code review NOT required):

1. **Pure documentation**: *.md files in docs/ directory only
   - ZERO code changes
   - ZERO configuration changes
   - Documentation ONLY

2. **Configuration-only**: Dependency updates in package.json, tsconfig.json
   - NO logic changes
   - NO script modifications
   - Updates ONLY

3. **Emergency hotfix**: Production down, security breach
   - MUST be reviewed within 24 hours after deployment
   - MUST create incident ticket
   - Emergency = production completely down, active security breach, data loss occurring
   - NOT emergency = "important", "urgent", "CEO wants it", "customer demo"

**If attempting to use exception:**
- Document which exception (1, 2, or 3) and why
- Provide evidence exception criteria met
- Cannot claim generic "too small" or "too simple"

### Example Review Gate Completion:

```
## Code Review Gate

- [x] **Code review requested**: Used requesting-reviewing-code skill
- [x] **Review completed**: code-reviewer subagent finished analysis
- [x] **Critical issues**: 0
- [x] **Important issues**: 0 (1 converted to issue #123)
- [x] **Review status**: Approved with minor items
- [x] **Review reference**: See code review output below

Critical Issues: 0
Important Issues: 0 (1 deferred: Created issue #123 for missing error handling edge case)
Minor Issues: 3
  - All addressed

Review approved for merge.
```

### Cannot Proceed Without:

You **CANNOT** claim completion without:
1. Code review completed (unless explicit exception 1, 2, or 3 applies with documentation)
2. Critical issues fixed (MUST be 0, no exceptions)
3. Important issues MUST be 0 OR converted to tracked issue with ID (cannot be "acknowledged" or "deferred" without issue ID)

**Attempting to skip code review without valid exception violates verifying-before-completion.**

### Common Rationalizations (DO NOT ACCEPT):

| Rationalization | Why It's Wrong | Correct Action |
|----------------|----------------|----------------|
| "This is too trivial to review" | Trivial changes cause production incidents | Request review anyway (takes 2 minutes) |
| "I'm the expert, no one else can review" | Experts have blind spots review catches | Request review from anyone on team |
| "We're too busy for review" | Busy doesn't exempt safety | If too busy to review, too busy to merge safely |
| "I'll get review after merging" | Post-merge review never happens | Review BEFORE merge, always |
| "The tests pass, that's enough" | Tests necessary but not sufficient | Tests + human review both required |
| "It's only N lines changed" | Size doesn't determine bug potential | ALL code changes require review |
| "No one else is available" | If not P0, it can wait | Wait for reviewer or escalate |
| "This is blocking me" | Being blocked doesn't exempt review | Work on different task while waiting |

## Frontend Verification Checklist

IF your work involves UI (HTML, CSS, JSX, templates, components):

BEFORE claiming UI work complete, verify ALL of these:

**For detailed guidance on frontend testing patterns, see the avoiding-testing-anti-patterns skill:**
- Anti-Pattern 6: Testing Implementation Details (test user-visible behavior, not internals)
- Anti-Pattern 7: No Accessibility Testing (comprehensive a11y verification)
- Anti-Pattern 8: Testing Happy Path Only (all states: loading, error, empty, partial)

### Visual Verification
- [ ] **Open browser DevTools** (F12 or Cmd+Option+I)
- [ ] **Inspect rendered output** in Elements panel
- [ ] **Test responsive breakpoints** (mobile, tablet, desktop)
- [ ] **Take screenshot** for visual regression baseline
- [ ] **Compare against baseline** (if exists)
- [ ] **Review differences**: Intentional or regression?

**Evidence required**: Screenshot showing correct rendering

### Console Verification
- [ ] **Open Console panel** in DevTools
- [ ] **Refresh page** and verify **0 errors** (0 red messages)
- [ ] **Verify NO warnings** (or document expected ones)
- [ ] **Take console screenshot** showing clean output

**Evidence required**: Console screenshot with 0 errors

### Network Verification
- [ ] **Open Network panel** in DevTools
- [ ] **Verify expected API calls** made with correct URLs/methods/status codes
- [ ] **Verify no failed requests** (no red in network tab)
- [ ] **Check response data** is correct

**Evidence required**: Network tab screenshot or description of verified requests

### Accessibility Verification (See avoiding-testing-anti-patterns Anti-Pattern 7 for detailed guidance)
- [ ] **Run axe-core test**: 0 violations
- [ ] **Test keyboard navigation**: All interactive elements accessible via Tab/Enter/Escape
- [ ] **Verify screen reader compatibility**: All elements have accessible names
- [ ] **Run Lighthouse accessibility audit**: Score ≥95

**Evidence required**: axe-core output (0 violations) + Lighthouse score

**For detailed examples and test code, see avoiding-testing-anti-patterns skill Anti-Pattern 7.**

### UI States Verification (See avoiding-testing-anti-patterns Anti-Pattern 8 for detailed guidance)
- [ ] **Test loading states**: Spinner/skeleton renders during loading
- [ ] **Test success states**: Data displays correctly
- [ ] **Test error states**: Error messages display on failures
- [ ] **Test empty states**: Empty message when no data
- [ ] **Test partial states**: Handles missing fields gracefully

**Evidence required**: Description of tested states and results

**For detailed examples and test code, see avoiding-testing-anti-patterns skill Anti-Pattern 8.**

## Frontend Verification Gate

```
BEFORE claiming UI work complete:

  IF you modified HTML/CSS/JSX/templates:
    STOP - Have you completed Frontend Verification Checklist?

    IF ANY checkbox unchecked:
      STOP - Work is NOT complete
      Complete all verification steps first

    IF console has errors:
      STOP - Fix errors before proceeding

    IF accessibility violations found:
      STOP - Fix violations before proceeding

    IF visual regression detected and unintentional:
      STOP - Fix regression before proceeding

  ONLY IF all frontend verification complete:
    Continue with completion claim
```

## Frontend Evidence Template

When claiming UI work complete, provide:

```markdown
## Frontend Verification Evidence

### Visual Verification
Screenshot: [component-name].png
Responsive breakpoints tested: Mobile (375x667), Tablet (768x1024), Desktop (1920x1080)
Visual regression: [Baseline created | No changes | Intentional changes approved]

### Console Verification
Console errors: 0
Console warnings: 0 (or: 1 expected warning about X)
[Screenshot of clean console]

### Network Verification
Expected requests:
- ✓ GET /api/products (200 OK)
- ✓ POST /api/checkout (201 Created)

Failed requests: 0

### Accessibility Verification
axe-core violations: 0
Keyboard navigation: ✓ All elements accessible
Lighthouse score: 97/100

### Interaction Verification
Tested interactions:
- ✓ Submit button → Form submits successfully
- ✓ Cancel button → Form clears
- ✓ Invalid email → Error message displays
- ✓ Loading state → Spinner renders
```

**You CANNOT claim UI complete without this evidence.**

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**
- Claiming tests pass without showing output
- Paraphrasing test results instead of showing raw output
- Showing partial output (truncated, filtered)
- Claiming "followed TDD" without certification
- Vague about whether tests failed first
- Can't describe failure messages seen
- Wrote tests and implementation "together"
- Skipping code review because "it's simple"
- Planning to "get review later"
- Claiming exception without documenting which (1, 2, or 3) and providing evidence
- Proceeding with unfixed Critical or Important issues
- Claiming Important issues are "acknowledged" without tracked issue ID

**Frontend-specific red flags:**
- Claiming "looks good" without DevTools verification
- Proceeding with console errors visible
- Skipping accessibility testing
- Not testing responsive breakpoints
- Taking full-page screenshots for component changes
- Updating visual baseline without reviewing diff
- Claiming "UI complete" without screenshot evidence

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
| "I followed the spirit of TDD" | Spirit = Letter. If you didn't watch tests fail first, you didn't follow TDD. Provide certification or start over. |
| "These tests are simple, TDD would slow me down" | Simple tests take 30 seconds. Complex tests NEED TDD. No exceptions. |
| "I wrote tests and implementation together" | That's not TDD. Tests FIRST. Delete implementation and restart. |
| "This is too small for code review" | Size doesn't matter. Code review is mandatory. See exceptions list for ONLY valid reasons to skip. |
| "I'll get review after merge" | No. Review BEFORE merge. Reversing changes post-merge is expensive and risky. |
| "Code review would slow me down" | Code review catches bugs before they reach users. Slowdown now prevents crisis later. |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

## Test Verification Requirements

When claiming tests pass, you MUST provide:

**Required Evidence**:

1. **Exact command executed**:
   ```bash
   npm test
   # or
   pytest
   # or
   cargo test
   # or
   go test ./...
   ```

2. **Complete output showing**:
   - Test count: "X tests passed"
   - Failure count: "0 failed"
   - Duration: "Time: X.XXXs"
   - Exit code: 0

3. **Coverage (if available)**:
   - Statement coverage: X%
   - Branch coverage: X%
   - Function coverage: X%
   - Line coverage: X%

### Example of VALID verification:

```
I've verified all tests pass. Here's the output:

$ npm test

PASS tests/auth.test.ts (4.231s)
  ✓ login with valid credentials (231ms)
  ✓ login with invalid credentials (12ms)
  ✓ logout successfully (8ms)

PASS tests/users.test.ts (2.145s)
  ✓ creates new user (145ms)
  ✓ updates existing user (98ms)
  ✓ deletes user (76ms)

Test Suites: 2 passed, 2 total
Tests:       6 passed, 6 total
Snapshots:   0 total
Time:        6.376s

Process exited with code 0



## Workflow Checklist

Copy this checklist to track your progress:

See `assets/workflow-checklist.md` for the complete checklist.

## References


For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting
