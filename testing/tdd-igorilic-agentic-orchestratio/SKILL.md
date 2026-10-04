---
name: tdd
description: >
  Strict test-driven development workflow. Use when implementing any feature,
  bug fix, or code change. Follows RED → GREEN → REFACTOR cycle with
  stack-aware test runner detection. Triggers on: implement, build, create,
  add feature, fix bug, write code for.
---

## TDD Workflow

Follow this cycle strictly for every code change.

### Phase 1: RED (Failing Tests)
1. Read the spec or requirement thoroughly
2. Identify acceptance criteria and edge cases
3. Create test file(s) in the appropriate location:
   - `.csproj`/`.sln` → `tests/Unit/` using xUnit + FluentAssertions
   - `go.mod` → `*_test.go` using testing + testify (table-driven)
   - `Cargo.toml` → `#[cfg(test)] mod tests` using built-in + tokio-test
   - `pyproject.toml` → `tests/unit/test_*.py` using pytest
   - `package.json` with react → `*.test.tsx` using Vitest + Testing Library
   - `package.json` with react-native → `*.test.tsx` using Jest + RNTL
   - `Package.swift`/`.xcodeproj` → `*Tests.swift` using XCTest
4. Write tests for: happy path, edge cases, error conditions
5. Run tests — confirm ALL FAIL
6. Commit: `test(<scope>): add failing tests for <feature>`

### Phase 2: GREEN (Minimum Implementation)
1. Pick ONE failing test
2. Write the minimum code to make it pass
3. Run tests — confirm that test passes
4. Repeat for each failing test
5. Commit: `feat(<scope>): implement <feature>`

### Phase 3: REFACTOR
1. Look for duplication, unclear naming, long functions (aim for < 20 lines)
2. Extract patterns, improve structure
3. Run tests after EACH change — must stay green
4. Commit: `refactor(<scope>): improve <description>`

### Phase 4: Integration Tests
1. Write integration tests for component interactions
2. Use TestContainers for database tests
3. Test with real service boundaries (not mocks)
4. Commit: `test(integration): add <feature> integration tests`

### Rules
- NEVER write production code without a failing test
- Each test tests ONE behavior
- Descriptive test names: `should_<behavior>_when_<condition>`
- If a test is hard to write, the design needs improvement
- If requirements are unclear, STOP and ask before writing tests
