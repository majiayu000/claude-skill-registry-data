---
name: tdd-guard-workflow
description: Use when implementing features or fixes in projects with tdd-guard installed. This skill guides the RED-GREEN-REFACTOR cycle with proper test registration, preventing common TDD violations like writing code before tests or implementing multiple tests simultaneously. Invoke when tdd-guard blocks an edit or when starting TDD work.
---

# TDD Guard Workflow

## Overview

This skill provides the workflow for Test-Driven Development when tdd-guard is enforcing TDD discipline. tdd-guard is a CLI tool that integrates with Claude Code hooks to block code changes that violate TDD principles.

**Important:** For comprehensive TDD principles and rationale, invoke the `superpowers:test-driven-development` skill. This skill focuses specifically on the tdd-guard integration workflow.

## What "One Test" Means

**A "test" is a single `it()` or `test()` block** — not a `describe()` suite.

```typescript
// This is ONE test:
it('should return true for valid input', () => { ... });

// This is also ONE test:
test('handles empty array', () => { ... });

// This is a TEST SUITE (contains multiple tests):
describe('MyFunction', () => {
  it('test 1', () => { ... });  // ← one test
  it('test 2', () => { ... });  // ← another test
});
```

**Why one test at a time?**

1. **Forces minimal implementation** — With only one failing test, you write only the code needed to pass that test. No speculative coding.
2. **Creates tight feedback loops** — You know immediately if each piece of code works.
3. **Prevents over-engineering** — You can't write code for tests that don't exist yet.
4. **Makes debugging trivial** — If a test fails, you know exactly which change caused it.

**The guard enforces this because:**

- Writing multiple tests at once tempts you to implement everything at once
- "Batch" implementation leads to larger changes that are harder to debug
- It's the smallest unit of work that proves progress

## Prerequisites Check

Before starting TDD work, verify tdd-guard reporter is installed in the package where tests run:

```bash
# Check if tdd-guard-vitest is installed
npm list tdd-guard-vitest

# If not installed, add it
npm install --save-dev tdd-guard-vitest
```

Verify vitest.config.ts includes the reporter with correct project root path:

```typescript
import { defineConfig } from 'vitest/config';
import { VitestReporter } from 'tdd-guard-vitest';
import { resolve } from 'path';

export default defineConfig({
  test: {
    reporters: ['default', new VitestReporter(resolve(__dirname, '../..'))],
    // ... other config
  },
});
```

**Critical:** The path argument to `VitestReporter` must resolve to the repository root, not the package directory. In monorepos, use `resolve(__dirname, '../..')` or similar to reach the repo root.

## The RED-GREEN-REFACTOR Cycle

### Phase 1: RED - Write ONE Failing Test

1. Write exactly **ONE `it()` or `test()` block** that describes the desired behavior
2. The test file must be valid (no syntax errors)
3. Run the test to register the failure with tdd-guard:

```bash
pnpm test -- path/to/test.test.ts
```

4. Verify the test fails for the expected reason (missing feature, not typo)
5. Only after the test run completes can edits to production code proceed

**What tdd-guard will BLOCK:**

| Scenario | Why Blocked |
|----------|-------------|
| Adding 2+ `it()` blocks at once | Multiple test addition violation |
| Editing production code with no failing test | Premature implementation |
| Adding `it()` while another is still failing | Must pass current test first |
| Adding test that passes immediately | Not a valid RED state (test should fail) |

**What tdd-guard ALLOWS:**

| Scenario | Why Allowed |
|----------|-------------|
| Adding/modifying `describe()` structure | `describe()` is organization, not a test |
| Adding helper functions in test file | Test infrastructure, not assertions |
| Adding ONE new `it()` block | Valid RED phase |
| Fixing typos in existing tests | Not adding new behavior |

### Phase 2: GREEN - Implement Minimal Code

1. Write the **minimum** code to make the test pass
2. If tdd-guard blocks with "over-implementation violation":
   - Create an empty stub first (e.g., empty method body)
   - Run tests to see the next specific failure
   - Add only what's needed to address that failure
3. Run tests to verify GREEN state:

```bash
pnpm test -- path/to/test.test.ts
```

4. All tests must pass before proceeding

### Phase 3: REFACTOR (Optional)

1. Clean up code while keeping tests green
2. Run tests after each refactoring change
3. Do not add new behavior during refactoring

### Repeat

Return to Phase 1 for the next test.

## Common Scenarios

### Scenario: Adding a New Method

```
1. RED:   Write test calling the new method
2. RUN:   Execute test → fails with "method doesn't exist"
3. GREEN: Add empty method stub: `myMethod(): void {}`
4. RUN:   Execute test → fails with specific assertion
5. GREEN: Implement minimal logic to pass assertion
6. RUN:   Execute test → passes
7. REPEAT for next behavior
```

### Scenario: Adding Caching

```
1. RED:   Write test verifying cached results (fewer calls on repeat)
2. RUN:   Execute test → fails (no caching exists)
3. GREEN: Add cache data structure
4. GREEN: Add cache lookup at method start
5. GREEN: Add cache storage before returns
6. RUN:   Execute test → passes
```

## Troubleshooting

See `references/troubleshooting.md` for common error messages and solutions.

## Quick Reference

| Phase | Action | Verify |
|-------|--------|--------|
| RED | Write ONE failing test | Test fails for expected reason |
| RUN | Execute test suite | Failure registered with tdd-guard |
| GREEN | Minimal implementation | Test passes |
| REFACTOR | Clean up (optional) | Tests still pass |
