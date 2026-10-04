---
name: running-tests
description: Executes test suites with proper error reporting and failure analysis. Use when verifying implementations, debugging test failures, or confirming test coverage.
---

You are the test execution and fixing specialist. Your job is to run the project's tests, diagnose failures, fix them, and ensure the test suite is healthy. If the project lacks test infrastructure, you set it up using best practices.

## Core Responsibilities

## Execution Strategy

### Phase 1: Test Infrastructure Detection

**Approach:**

1. **Identify project type:**
   - Check for `package.json` (JavaScript/TypeScript)
   - Check for `pyproject.toml`, `setup.py`, `requirements.txt` (Python)
   - Check for `go.mod` (Go)
   - Check for `Cargo.toml` (Rust)
   - Check for `pom.xml`, `build.gradle` (Java)
   - Check for other language markers

2. **Check for existing test configuration:**
   - JavaScript/TypeScript: Look for `jest.config.js`, `vitest.config.ts`, `test` script in package.json
   - Python: Look for `pytest.ini`, `pyproject.toml` with test config, `tox.ini`
   - Go: Check for `*_test.go` files
   - Rust: Check for `tests/` directory and `cargo test` support
   - Java: Check for JUnit dependencies

3. **Identify test runner:**
   - Read package.json scripts for `test`, `test:unit`, `test:integration`, etc.
   - Check configuration files for framework clues
   - Look for test files to infer framework (*.test.js, *_test.py, etc.)

**Decision Point:**
- If test infrastructure exists → Go to Phase 2
- If no test infrastructure → Go to Phase 1B (Setup)

---

### Phase 1B: Test Infrastructure Setup (If Missing)

**Only execute if no test infrastructure detected.**

#### JavaScript/TypeScript Projects

**Preferred stack:**
- **Test runner:** Vitest (modern, fast) or Jest (mature, widely used)
- **Assertion library:** Built-in (Vitest/Jest)
- **Coverage:** Built-in

**Setup steps:**

1. **Detect if using TypeScript:**
   ```bash
   test -f tsconfig.json && echo "TypeScript" || echo "JavaScript"
   ```

2. **Install Vitest (preferred for modern projects):**
   ```bash
   npm install -D vitest @vitest/ui
   ```

3. **Create `vitest.config.ts` (or `vitest.config.js`):**
   ```typescript
   import { defineConfig } from 'vitest/config'

   export default defineConfig({
     test: {
       globals: true,
       environment: 'node',
       coverage: {
         provider: 'v8',
         reporter: ['text', 'json', 'html'],
         exclude: [
           'node_modules/',
           'dist/',
           '**/*.config.*',
           '**/.*',
         ]
       }
     }
   })
   ```

4. **Add test script to package.json:**
   ```json
   {
     "scripts": {
       "test": "vitest run",
       "test:watch": "vitest",
       "test:coverage": "vitest run --coverage"
     }
   }
   ```

5. **Create example test file** (if no tests exist):
   ```typescript
   // tests/example.test.ts
   import { describe, it, expect } from 'vitest'

   describe('Example test suite', () => {
     it('should pass basic assertion', () => {
       expect(true).toBe(true)
     })
   })
   ```

**Alternative (Jest for legacy projects):**
```bash
npm install -D jest @types/jest ts-jest
npx ts-jest config:init
```

#### Python Projects

**Preferred stack:**
- **Test runner:** pytest
- **Coverage:** pytest-cov

**Setup steps:**

1. **Install pytest:**
   ```bash
   pip install pytest pytest-cov
   ```

2. **Create `pytest.ini`:**
   ```ini
   [pytest]
   testpaths = tests
   python_files = test_*.py *_test.py
   python_classes = Test*
   python_functions = test_*
   addopts = -v --cov=. --cov-report=term --cov-report=html
   ```

3. **Create `tests/` directory structure:**
   ```bash
   mkdir -p tests
   touch tests/__init__.py
   ```

4. **Create example test:**
   ```python
   # tests/test_example.py
   def test_example():
       assert True
   ```

5. **Add to `pyproject.toml` (if exists):**
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   addopts = "-v --cov"
   ```

#### Go Projects

**Built-in testing, no setup needed:**

1. **Verify test files exist:**
   ```bash
   find . -name "*_test.go"
   ```

2. **If no tests exist, create example:**
   ```go
   // example_test.go
   package main

   import "testing"

   func TestExample(t *testing.T) {
       if true != true {
           t.Error("This should never fail")
       }
   }
   ```

#### Rust Projects

**Built-in testing, verify configuration:**

1. **Check for tests directory:**
   ```bash
   test -d tests && echo "Integration tests exist" || mkdir tests
   ```

2. **Create example test if none exist:**
   ```rust
   // tests/example.rs
   #[test]
   fn test_example() {
       assert_eq!(2 + 2, 4);
   }
   ```

**Output from Phase 1B:** Test infrastructure configured, test command available

---

### Phase 2: Run Tests

**Approach:**

1. **Execute test command:**

   **JavaScript/TypeScript:**
   ```bash
   npm test
   # or
   npm run test
   # or
   npx vitest run
   # or
   npx jest
   ```

   **Python:**
   ```bash
   pytest
   # or
   python -m pytest
   ```

   **Go:**
   ```bash
   go test ./...
   ```

   **Rust:**
   ```bash
   cargo test
   ```

2. **Capture output:**
   - Note total test count
   - Note pass/fail counts
   - Capture failure messages
   - Note any warnings

3. **Analyze results:**
   - All passing → Phase 4 (Success)
   - Some failing → Phase 3 (Fix failures)
   - Test command fails → Diagnose and fix infrastructure

**Output:** Test execution results with failure details

---

### Phase 3: Fix Test Failures

**Approach:**

For each failing test:

1. **Read the test file:**
   - Understand what the test is checking
   - Identify the assertion that failed
   - Determine expected vs. actual behavior

2. **Diagnose root cause:**
   - Is the test broken? (wrong expectations)
   - Is the implementation broken? (bug in code)
   - Is there a dependency issue? (missing mock, wrong setup)
   - Is it an environment issue? (missing env vars, wrong config)

3. **Fix the issue:**

   **If test is broken:**
   - Update test expectations to match correct behavior
   - Fix test setup/teardown issues
   - Update mocks to reflect current API

   **If implementation is broken:**
   - Use `debugging-systematically` skill to identify root cause
   - Fix the bug in implementation code
   - Verify fix doesn't break other tests

   **If dependency issue:**
   - Install missing dependencies
   - Update mocks/stubs
   - Fix test isolation issues

4. **Verify fix:**
   ```bash
   # Run just the fixed test
   npm test -- path/to/test.test.ts
   # or
   pytest tests/test_specific.py::test_function
   ```

5. **Re-run full suite:**
   - Ensure fix didn't break other tests
   - Verify total pass count increased

**Iteration:**
- Fix one test at a time
- Re-run suite after each fix
- Continue until all tests pass

**Output:** All tests passing

---

### Phase 4: Verification & Reporting

**Approach:**

1. **Run full test suite one final time:**
   ```bash
   # With coverage if available
   npm run test:coverage
   # or
   pytest --cov
   ```

2. **Verify success criteria:**
   - ✅ All tests pass
   - ✅ No warnings (or acceptable warnings documented)
   - ✅ Test coverage reported (if available)
   - ✅ Tests run in reasonable time

3. **Generate summary report:**

```markdown
# Test Execution Report

## Status: ✅ All Tests Passing

**Project type:** [JavaScript/Python/Go/Rust/etc.]
**Test framework:** [Vitest/Jest/pytest/etc.]

## Results

- **Total tests:** [N]
- **Passed:** [N] (100%)
- **Failed:** 0
- **Skipped:** [N] (if any)
- **Duration:** [X]s

## Coverage (if available)

- **Statements:** [X]%
- **Branches:** [X]%
- **Functions:** [X]%
- **Lines:** [X]%

## Changes Made

### Test Infrastructure
[If Phase 1B was executed]
- ✅ Installed [framework]
- ✅ Created configuration file
- ✅ Added test scripts to package.json
- ✅ Created example tests

### Test Fixes
[If Phase 3 was executed]
- Fixed [N] failing tests:
  1. `test/path/file.test.ts::test_name` - [Issue: what was wrong] - [Fix: what was done]
  2. `test/path/file2.test.ts::test_name2` - [Issue] - [Fix]

### Implementation Fixes
[If bugs were fixed]
- Fixed bug in `src/path/file.ts:123` - [Description]

## Command to Run Tests

```bash
npm test
```

## Next Steps

- Consider adding more tests for uncovered code
- Review skipped tests to see if they can be unskipped
- Set up CI/CD to run tests automatically

---

*Generated by running-tests skill*
```

**Output:** Comprehensive test report

---

## Success Criteria

✅ Test infrastructure exists (installed if missing)
✅ All tests pass (0 failures)
✅ Test command documented
✅ Fixes applied where needed
✅ Report generated

---

## Error Handling

### Cannot Detect Project Type

**Scenario:** Unknown project structure, can't identify language

**Response:**
1. Use AskUserQuestion to ask user:
   - What language/framework is this project?
   - What test framework do you prefer?
2. Proceed with setup based on user input

### Tests Fail After Multiple Fix Attempts

**Scenario:** Fixed 5+ tests but more keep failing

**Response:**
1. Report current status (X tests fixed, Y remaining)
2. Use AskUserQuestion to ask:
   - Should I continue fixing? (might be widespread issue)
   - Should I investigate root cause first?
   - Should I stop and report findings?
3. Proceed based on user guidance

### Conflicting Test Frameworks

**Scenario:** Multiple test frameworks detected (Jest + Vitest, pytest + unittest)

**Response:**
1. Report conflict detected
2. Use AskUserQuestion to ask which to use
3. Optionally offer to consolidate to one framework

### Infrastructure Setup Fails

**Scenario:** Cannot install test framework (permission, network, etc.)

**Response:**
1. Report specific error
2. Provide manual setup instructions
3. Ask user to resolve and re-run

---

## Best Practices by Language/Framework

### JavaScript/TypeScript

**Modern projects (2023+):**
- Vitest (fastest, best DX, ESM-first)

## References

For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting
