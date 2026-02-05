---
name: test-watch-focused-patterns
description: Use when developing tests or refactoring test suites - run tests in watch mode with focused file patterns to get instant feedback on specific test files without running the entire suite
---

# Test Watch Mode with Focused File Patterns

## Overview

**Run tests in watch mode with file pattern filters for instant, targeted feedback during test development and refactoring.**

Instead of running the full test suite repeatedly or running tests manually after each change, watch mode with focused patterns gives you:
- Instant feedback on changes (< 1 second)
- Focus on relevant tests only
- Automatic re-runs on file changes
- Reduced cognitive load during refactoring

**Core principle:** Fast feedback loops enable confident, iterative test development.

## When to Use This Workflow

**Use test watch mode with focused patterns when:**
- Developing new test files
- Refactoring existing tests
- Debugging flaky tests
- Working on test utilities/factories
- Restructuring test organization
- Any test work requiring multiple iterations

**Don't use when:**
- Running full CI validation
- Verifying all tests pass before commit
- Initial test discovery (use full suite first)

## The Workflow

### 1. Start Watch Mode with Pattern

```bash
# Jest
npm test -- --watch --testPathPattern=user

# Vitest
npm test -- --watch --testNamePattern=user

# Mocha with nodemon
nodemon --watch src --watch test --exec "npm test -- --grep user"

# Bun
bun test --watch "**/*user*.test.ts"
```

### 2. Pattern Syntax Examples

```bash
# Single file
--testPathPattern=user.test

# Directory
--testPathPattern=services/

# Multiple patterns (Jest)
--testPathPattern="user|account|auth"

# Exclude patterns
--testPathPattern="^(?!.*integration)"
```

### 3. Interactive Commands

Most test runners provide interactive commands in watch mode:

```
p - Filter by filename pattern
t - Filter by test name pattern
a - Run all tests
f - Run only failed tests
o - Run tests related to changed files
q - Quit watch mode
```

### 4. Workflow Loop

1. Start watch mode with focused pattern
2. Make changes to test or implementation
3. Watch automatically re-runs relevant tests
4. See immediate feedback
5. Iterate quickly
6. Expand pattern or run full suite when confident

## Common Patterns

### Focus on Single File

```bash
npm test -- --watch --testPathPattern=user.test.ts
```

### Focus on Feature Directory

```bash
npm test -- --watch --testPathPattern=features/auth/
```

### Focus on Test Type

```bash
# Unit tests only
npm test -- --watch --testPathPattern="unit"

# Integration tests only
npm test -- --watch --testPathPattern="integration"
```

### Focus on Failed Tests

```bash
npm test -- --watch --onlyFailures
```

## Benefits During Refactoring

**Why this matters for test suite refactoring:**

1. **Immediate validation** - Know instantly if refactor breaks tests
2. **Reduced context switching** - No manual test runs
3. **Confidence building** - See green tests accumulate as you work
4. **Early error detection** - Catch issues before they compound
5. **Flow state** - Stay focused, get feedback without breaking concentration

## Integration with Test Development

### Test-Driven Development

```bash
# 1. Start watch on new test file
npm test -- --watch --testPathPattern=newFeature.test

# 2. Write failing test
# 3. Watch shows red
# 4. Implement feature
# 5. Watch shows green
# 6. Refactor with confidence
```

### Test Refactoring

```bash
# 1. Start watch on file being refactored
npm test -- --watch --testPathPattern=legacy.test

# 2. Extract test factory
# 3. Watch validates tests still pass
# 4. Reorganize test structure
# 5. Watch provides continuous validation
# 6. Expand to related tests gradually
```

## Troubleshooting

**Watch not triggering:**
- Check file watcher limits: `ulimit -n`
- Exclude node_modules: `--watchPathIgnorePatterns`
- Use polling mode: `--watchman=false`

**Too many tests running:**
- Narrow the pattern: `--testPathPattern=more/specific/path`
- Use test name pattern: `--testNamePattern=specific`
- Exclude directories: `--testPathIgnorePatterns`

**Tests running slowly:**
- Use `--maxWorkers=1` for debugging
- Check for expensive beforeEach/afterEach
- Consider splitting large test files

## Pro Tips

1. **Use two terminals** - One for watch mode, one for commands
2. **Start narrow, expand gradually** - Focus on one file, then directory, then full suite
3. **Combine with coverage** - `--watch --coverage` to see coverage live (may be slow)
4. **Use test name patterns for specific tests** - Faster than file patterns when debugging single test
5. **Commit with full suite** - Always run full suite before committing, even if watch passed

## Common Mistakes

**Running full suite on every change:**
- Slow feedback loop
- Wastes time on unrelated tests
- Easy to lose focus while waiting

**Not using watch mode at all:**
- Manual test runs break flow
- Higher cognitive load
- Slower iteration cycles
- More likely to forget to run tests

**Pattern too broad:**
- Runs too many tests
- Slower than focused pattern
- Defeats the purpose

**Pattern too narrow:**
- Might miss integration failures
- False confidence
- Remember to expand before committing

## The Bottom Line

**Fast feedback enables confident iteration.**

Watch mode with focused patterns makes test development feel instant. Start narrow, iterate quickly, expand gradually, validate fully before commit.

**Pattern: Focus → Iterate → Expand → Validate**
