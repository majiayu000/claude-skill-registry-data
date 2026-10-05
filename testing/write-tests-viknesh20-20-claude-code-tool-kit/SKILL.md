---
name: write-tests
description: "Generates comprehensive unit and integration tests for a specified file or function. Auto-detects the test framework, follows existing patterns, and covers happy path, edge cases, error conditions, and async behavior. Use when adding tests to untested code or TDD-ing a new module."
argument-hint: "[file or function to test]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Write Tests

## Detect Project Test Environment

### Package/Project Files
!`ls package.json pytest.ini pyproject.toml setup.cfg tox.ini go.mod Cargo.toml *.csproj *.sln Gemfile build.gradle pom.xml mix.exs deno.json 2>/dev/null`

### Existing Tests
!`find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -name "*_test.*" -o -name "*_spec.*" -o -name "*Test.*" -o -name "*Spec.*" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" 2>/dev/null | head -20`

### Test Config
!`cat jest.config.* vitest.config.* pytest.ini pyproject.toml setup.cfg .rspec 2>/dev/null | head -50`

---

## Instructions

### Step 1: Analyze the Target
1. Read the file or function to be tested
2. Identify all public APIs, functions, methods, and classes
3. Map out the code paths: conditionals, loops, error throws, early returns
4. Identify external dependencies that need mocking

### Step 2: Determine Test Framework
Based on the detected project files:
- **JavaScript/TypeScript**: Jest, Vitest, Mocha, or Playwright (check package.json)
- **Python**: pytest, unittest (check pyproject.toml, pytest.ini)
- **Go**: standard `testing` package
- **Rust**: built-in `#[cfg(test)]` module
- **C#/.NET**: xUnit, NUnit, or MSTest
- **Ruby**: RSpec or Minitest
- **Java**: JUnit 5 or TestNG
- **Elixir**: ExUnit

### Step 3: Follow Existing Patterns
- Find the nearest existing test file for a similar module
- Match the structure: describe/it, test classes, test functions
- Match the mocking approach: jest.mock, unittest.mock, testify, etc.
- Match the assertion style: expect, assert, should
- Match the file naming convention and directory placement

### Step 4: Generate Tests
Write tests covering ALL of the following categories:

#### Happy Path
- Normal inputs produce expected outputs
- Standard use cases work correctly
- Return values and side effects are verified

#### Edge Cases
- Empty inputs (null, undefined, empty string, empty array, zero)
- Boundary values (min, max, off-by-one)
- Unicode and special characters where relevant
- Large inputs (performance boundary)

#### Error Conditions
- Invalid inputs produce appropriate errors
- Thrown exceptions match expected types and messages
- Error callbacks/handlers are invoked correctly
- Graceful degradation for partial failures

#### Async Behavior (if applicable)
- Promises resolve/reject correctly
- Async/await error handling
- Concurrent operations
- Timeout and cancellation

#### Mocking
- Mock external dependencies at module boundaries
- Verify mock calls (called with correct args, correct number of times)
- Reset mocks between tests
- Do NOT mock the unit under test

### Step 5: Test Quality Rules
- One assertion concept per test (multiple asserts OK if testing one thing)
- Test names are full English sentences describing the scenario
- Use `beforeEach`/`setUp` for shared setup; `afterEach`/`tearDown` for cleanup
- Tests must be deterministic — no random data, no time-dependent assertions
- Tests must be independent — no shared mutable state between tests

### Step 6: Output
Generate a complete, ready-to-save test file with:
- A header comment explaining what is tested
- All necessary imports
- Properly structured test suites
- The target coverage goal (aim for >80%)

Place the file following the project's test directory convention.
