---
name: bugfixforever
description: State-of-the-art procedure for fixing bugs in software projects. Use this skill when a bug has been detected or declared by the user, agent, or another skill (not during early-stage work in progress). Enforces a disciplined test-driven approach - understand, reproduce experimentally, write failing tests, fix the code, and clean up.
---

# BugFixForever (BFF)

## Overview

This skill guides a reliable, test-driven procedure for fixing bugs in software projects. The approach emphasizes experimental reproduction, comprehensive test coverage at appropriate abstraction levels, and clean commits.

## When to Use This Skill

Activate this skill when:
- A user reports a bug or issue in the system
- An agent detects unexpected behavior or failures
- Another skill identifies a problem that needs fixing
- Do NOT interrupt early-stage work in progress for minor issues

## The BFF Workflow

Follow these phases in order. Do not skip ahead to fixing code before establishing reproducibility and test coverage.

### Phase 1: Understand the Bug

Gather context about the bug's behavior:
- What is the expected behavior vs. actual behavior?
- When does it occur? What triggers it?
- What is the impact? (User-facing, data corruption, performance, etc.)
- What has changed recently that might be related?
- Is this reproducible consistently or intermittent?

Review relevant code, recent commits, and existing tests to build mental model of where the bug likely exists.

### Phase 2: Experimentally Reproduce the Bug

Prove the bug exists through experimentation. All experimental code must live on the filesystem - do NOT write one-off scripts directly into stdin of a scripting language.

**Acceptable reproduction methods:**
- Run the software normally (web server, CLI, etc.)
- Run existing tests to confirm failures
- Write temporary test files to isolate the issue
- Use a web browser and developer tools to reproduce user-facing issues
- Tail logs and add temporary logging statements
- Run the same test multiple times for intermittent issues
- Manipulate mocks/stubs to isolate components

**Code inspection & debugging techniques:**
- Add temporary logging/print statements to trace execution flow
- Use debuggers with breakpoints to step through code
- Add strategic assertions to catch bad state earlier
- Temporary console.log/print statements in production code (to be removed in cleanup phase)

**System-level tools (when appropriate):**
- System call tracing (strace, dtrace) for low-level issues
- Performance profiling tools for performance bugs
- Container/process inspection (docker logs, ps, top)
- Network analysis tools

**Important:** Create reusable files for all experimental code. Temporary test files, debugging scripts, and reproduction cases should be saved to the filesystem, not executed as one-liners.

Continue experimentation until the bug's behavior is proven and understood mechanistically.

### Phase 3: Write Failing Tests

Once reproduction is confirmed, write one or more declarative tests into the project's test suites that fail because the bug exists.

**The Drill-Down Approach:**

For user-facing bugs or integration issues:
1. **Start at the top**: Write an E2E or integration test that captures the user-visible symptom
2. **Drill down**: Write a unit test that captures the root cause at the component/function level

For internal bugs discovered during development:
- A focused unit test may be sufficient

**Test quality criteria:**
- Tests should be declarative and clearly document what behavior is expected
- Tests should fail reliably when the bug exists
- Tests should be placed in appropriate test suites (not temporary files)
- Choose abstraction level that matches the bug's nature

Run the new tests to confirm they fail with clear, expected error messages.

### Phase 4: Fix the Bug

Only after failing tests are in place, modify the production code to fix the bug.

**Fix principles:**
- Make the minimal change necessary to fix the root cause
- Preserve existing functionality (don't introduce regressions)
- Follow existing code patterns and conventions
- Consider edge cases and similar bugs that might exist

Run the new tests to confirm they now pass. Run the full test suite to ensure no regressions.

### Phase 5: Cleanup and Commit

Remove all temporary artifacts and prepare a clean commit:

**Cleanup tasks:**
- Delete temporary test files, debugging scripts, and experimental code
- Remove temporary logging/print/console.log statements added during reproduction
- Remove extraneous comments added during debugging
- Update or remove outdated documentation affected by the fix

**Commit preparation:**
Use the `no-more-commitment-issues` skill to ensure commit hygiene:
- Clear, concise commit message explaining what was fixed and why
- Only include files relevant to the fix and its tests
- No debug statements, temporal language, or cruft

## Examples

### Example 1: User-facing bug in web application

**User report:** "When I click 'Save' on the profile page, nothing happens."

**Phase 1:** Understand - profile save button should update user data but appears non-functional

**Phase 2:** Reproduce experimentally:
```bash
# Run dev server
pnpm run dev

# Open browser, navigate to profile page, reproduce issue
# Check browser console - see "TypeError: Cannot read property 'id' of undefined"
# Add temporary console.log in src/components/Profile.tsx to trace data flow
```

**Phase 3:** Write failing tests (drill-down approach):
```typescript
// E2E test capturing user-facing symptom
test('user can save profile changes', async ({ page }) => {
  // ... test fails
});

// Unit test capturing root cause
test('ProfileService.save handles missing user ID', () => {
  // ... test fails
});
```

**Phase 4:** Fix - add null check in ProfileService.save()

**Phase 5:** Remove temporary console.log, commit with no-more-commitment-issues skill

### Example 2: Intermittent test failure

**Agent observation:** "Tests are flaky - UserAuthTest sometimes fails."

**Phase 1:** Understand - race condition suspected in authentication flow

**Phase 2:** Reproduce experimentally:
```bash
# Create temporary script to run test 100 times
# File: debug/test_flakiness.sh
for i in {1..100}; do
  npm test -- UserAuthTest
done

# Add temporary logging to trace async timing issues
```

**Phase 3:** Write failing test that reliably exposes race condition

**Phase 4:** Fix - add proper async/await handling

**Phase 5:** Delete debug/test_flakiness.sh and temporary logging, commit

## Key Principles

1. **Filesystem-first**: All experimental code lives in files, not stdin one-liners
2. **Drill-down testing**: Start with high-level tests for user impact, drill to unit tests for root cause
3. **Prove before fixing**: Never fix code until bug is reproducible and tests are written
4. **Clean commits**: Remove all temporary artifacts before committing
