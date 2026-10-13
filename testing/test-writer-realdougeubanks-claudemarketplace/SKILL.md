---
name: test-writer
description: Generates comprehensive unit and integration tests for a given file or function, auto-detecting the project test framework and matching existing test style.
argument-hint: "[file-or-function]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Test Writer

Generate comprehensive unit and integration tests for a given file or function, auto-detecting the project test framework and matching the existing test style.

## Instructions

When invoked via `/test-writer`:

1. **Identify the target.** Ask the user: which file or function should tests be written for? Accept:
   - An absolute or relative file path (e.g. `src/utils/parser.ts`)
   - A function or method name (ask which file it lives in if ambiguous)

2. **Read the target file** using Read. Understand:
   - All exported/public functions, classes, and methods
   - Their parameter types, return types, and documented or inferred behavior
   - Dependencies (imports/requires) that will need to be mocked

3. **Detect the test framework** using Glob and Read:
   - **Jest**: look for `jest.config.*`, or `"jest"` key in `package.json`
   - **Vitest**: look for `vitest.config.*`, or `"vitest"` in `package.json` devDependencies
   - **pytest**: look for `pytest.ini`, `pyproject.toml` containing `[tool.pytest.ini_options]`, or `conftest.py`
   - **Go test**: look for `go.mod` and any existing `*_test.go` files
   - **PHPUnit**: look for `phpunit.xml` or `phpunit.xml.dist`, or `phpunit/phpunit` in `composer.json`
   - **Mocha**: look for `.mocharc.*`, or `"mocha"` in `package.json` devDependencies
   - **RSpec**: look for `.rspec`, `spec/spec_helper.rb`, or `rspec` in `Gemfile`
   - **JUnit**: look for `junit` in `pom.xml` or `build.gradle`/`build.gradle.kts`
   - **xUnit / NUnit / MSTest**: look for `xunit`, `NUnit`, or `MSTest` package references in `*.csproj`
   - If multiple are present, ask the user which to use.

4. **Match existing test style.** Use Glob to find existing test files matching `**/*.test.*`, `**/*.spec.*`, `**/*_test.*`, or `tests/**/*`. Read 1–2 representative test files to capture:
   - Describe/context block structure
   - Assertion library and style (`expect`, `assert`, `should`)
   - How mocks, stubs, and fixtures are set up
   - Import paths and module resolution patterns

5. **Determine the test file location and name:**
   - If existing tests are co-located (e.g. `src/foo.ts` → `src/foo.test.ts`), follow that pattern.
   - If existing tests live in a `tests/` or `__tests__/` directory, mirror the source path there.
   - If no existing tests exist, default to co-located.

6. **Generate tests** covering:
   - **Happy path**: normal, valid inputs produce the expected output
   - **Edge cases**: empty string/array, zero, `null`/`undefined`/`None`, maximum values, boundary conditions (e.g. off-by-one)
   - **Invalid input**: wrong type, missing required fields, malformed data — verify errors are thrown or returned correctly
   - **Error conditions**: simulate dependency failures using mocks/stubs; verify the function handles them gracefully
   - **All public functions/methods** in the target file — do not skip any exported surface

   Follow the detected framework's idioms exactly. Use the same describe block nesting, assertion style, and mock setup patterns found in existing tests.

7. **Write the test file:**
   - If the test file does not exist, use Write to create it.
   - If the test file already exists, use Read to review it, then use Edit to append new test cases — never overwrite existing tests.

8. **Run the tests** using Bash. For JS/TS frameworks, prefer the project's own test script or local binary — do not use `npx`, which can download and execute a package from the network if it isn't installed locally:
   - Jest/Vitest/Mocha: `npm test -- <testfile>` if `package.json` defines a test script; otherwise `node_modules/.bin/jest <testfile>` (or `vitest run` / `mocha`). If neither exists, ask the user before falling back to `npx`.
   - pytest: `python -m pytest <testfile> -v`
   - Go: `go test ./... -run <TestName>`
   - PHPUnit: `vendor/bin/phpunit <testfile>`
   - RSpec: `bundle exec rspec <testfile>`
   - JUnit: `mvn test -Dtest=<TestClass>` or `gradle test --tests <TestClass>`
   - xUnit/NUnit/MSTest: `dotnet test --filter <TestClass>`
   - Report pass/fail counts and any error output.
   - If tests fail, diagnose the root cause (missing mock, wrong import path, API mismatch) and fix before finishing. Do not leave the user with a broken test file.

## Output Format

After writing and running tests, summarize:

```
## Test Writer — <target file> — <date>

### Framework Detected
<framework name and version if available>

### Test File Written
`<path/to/test-file>`

### Coverage
| Function / Method | Tests Written |
|-------------------|---------------|
| functionName      | 4 (happy, edge, invalid, error) |
| anotherFunction   | 3 (happy, edge, error) |

### Run Results
Tests: X passed, Y failed, Z total

### Notes
<Any caveats — e.g. "mock for ExternalService is approximate; update if the interface changes">
```

## Notes

- This skill writes tests only — it does not modify production code.
- If the target file has no exports or public surface (e.g. it is a CLI entry point), generate integration-style tests that exercise the module end-to-end via its public interface or subprocess.
- Prefer deterministic tests. Avoid `Date.now()`, `Math.random()`, or other non-deterministic values in assertions without mocking them first.
