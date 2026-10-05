---
name: code-coverage
description: "Analyzes test coverage, identifies untested code paths, and generates tests for the most critical uncovered areas. Use to improve test coverage before releases."
argument-hint: "[file, module, or 'all']"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Test Coverage Analysis

## Detect Test Setup
!`ls package.json jest.config.* vitest.config.* .nycrc* .c8rc* .coveragerc* setup.cfg pyproject.toml tox.ini 2>/dev/null`
!`cat package.json 2>/dev/null | grep -E "jest|vitest|c8|nyc|istanbul|coverage" | head -5`

---

## Process

### Step 1: Run Coverage (if configured)
Attempt to run the project's coverage command:

| Ecosystem | Coverage Command |
|-----------|-----------------|
| npm (Jest) | `npx jest --coverage --json 2>/dev/null` |
| npm (Vitest) | `npx vitest run --coverage 2>/dev/null` |
| npm (c8) | `npx c8 report --reporter=json 2>/dev/null` |
| Python (pytest) | `python -m pytest --cov --cov-report=json 2>/dev/null` |
| Go | `go test -coverprofile=coverage.out ./... 2>/dev/null && go tool cover -func=coverage.out` |
| Rust | `cargo tarpaulin --out json 2>/dev/null` |

If coverage tools aren't configured, proceed with static analysis.

### Step 2: Static Analysis (if no coverage tool)
For the target file(s):
1. Identify all public functions, methods, and classes
2. Search for corresponding test files
3. For each function, check if there's a test that calls it
4. Map which code paths (branches, error handlers) have test coverage

### Step 3: Coverage Report

#### Summary
| Metric | Value |
|--------|-------|
| Line coverage | XX% |
| Branch coverage | XX% |
| Function coverage | XX% |
| Uncovered files | X |

#### Uncovered Critical Code
List the most important uncovered code, prioritized by:
1. **Business logic** — core features and workflows
2. **Error handling** — catch blocks, error paths, edge cases
3. **Security-sensitive** — auth, input validation, data access
4. **Complex logic** — functions with high cyclomatic complexity

For each uncovered area:
- File path and line numbers
- What the code does
- Why it's important to test
- Suggested test cases

### Step 4: Generate Missing Tests
For the top 5 most critical uncovered areas, generate test code following the project's test patterns (same structure as `/write-tests`).

### Step 5: Coverage Improvement Plan

| Priority | File | Current | Target | Tests Needed |
|----------|------|---------|--------|-------------|
| 1 | ... | XX% | 80%+ | ... |
| 2 | ... | XX% | 80%+ | ... |

---

## Rules
- Focus on meaningful coverage, not 100% — test behavior, not implementation
- Prioritize business logic and error paths over boilerplate
- Don't generate tests just to increase numbers — each test should validate something valuable
- Respect existing test patterns and conventions
