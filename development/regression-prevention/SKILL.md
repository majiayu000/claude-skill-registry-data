---
name: regression-prevention
description: >
  Use when making changes to existing systems to ensure those changes don't break
  existing functionality. This skill provides procedures for identifying at-risk areas,
  adding regression tests, and validating changes don't cause unintended side effects.
---

# Regression Prevention

## Overview
This skill defines how to prevent regressions - bugs introduced by changes that break previously working functionality. Systematic regression prevention saves time, maintains quality, and builds confidence in changes.

## When to Use
- Before modifying any existing code, configuration, or process
- Before upgrading dependencies, libraries, or frameworks
- Before deploying changes that affect shared components or APIs
- After fixing a bug (prevent it from coming back)
- **Don't use when:** Working on entirely new code with no existing dependencies

## Core Procedures

### Step 1: Identify At-Risk Areas
For every proposed change, determine what could break:
- **Direct Dependencies:** Files, modules, or services that use the thing being changed
- **Indirect Dependencies:** Things that depend on things that depend on what's being changed
- **Shared Components:** Libraries, utilities, or infrastructure used by multiple systems
- **Data Contracts:** APIs, database schemas, or interfaces that other systems depend on
- **Configuration:** Environment variables, feature flags, or deployment settings

### Step 2: Verify Existing Tests Cover At-Risk Areas
For each at-risk area:
- [ ] Does an existing test cover this? If yes, run it.
- [ ] If no test exists, create a regression test BEFORE making the change
- [ ] Ensure regression test fails on the current broken state (test the test)

### Step 3: Make Changes Safely
1. Check out a clean branch for the change
2. Run ALL tests for at-risk areas BEFORE changing anything
3. Make the smallest possible change that achieves the goal
4. Run tests after each small change
5. If any test fails that wasn't expected, STOP and diagnose before continuing

### Step 4: Post-Change Validation
After change is complete:
- [ ] Run FULL test suite, not just at-risk tests
- [ ] Manual smoke test of affected functionality
- [ ] Verify the original bug is fixed (if that was the goal)
- [ ] Commit regression test with clear description of what it protects

### Step 5: Document Regression Tests
```
REGRESSION TEST
===============
Bugs prevented: [what issue/s does this test protect against]
Change that introduced it: [what change could cause this regression]
Test location: [file, function, test name]
Coverage: [what specific behavior is validated]
Date created: [when this was added]
```

## Quality Checklist
- [ ] All at-risk areas identified before changes
- [ ] Existing tests cover at-risk areas OR new regression tests added
- [ ] Tests pass before changes begin
- [ ] Tests pass after changes complete
- [ ] Smoke test performed on affected functionality
- [ ] Regression test documented and committed with change

## Error Handling
- **Error:** Change breaks an existing test
  **Response:** Determine if test is correct (your change is wrong) or if change is right (test needs updating)
- **Error:** Existing tests don't cover enough to make change safely
  **Response:** Write coverage tests first, then make the change, treat as test discovery exercise
- **Error:** Full test suite takes too long to run
  **Response:** Run at-risk tests for quick feedback, queue full suite for later validation

## Cross-Team Integration
**Related Skills:** testing-strategy, test-driven-development, output-validation-checklist, edge-case-analysis
**Used By:** ALL agents modifying existing systems, especially Fixers, Refactors, Maintainers, Integration specialists