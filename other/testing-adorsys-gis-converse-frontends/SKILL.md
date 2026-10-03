---
name: testing
description: Generates comprehensive unit and integration tests following project conventions, covering happy paths, edge cases, and error scenarios.
---

# Testing Skill

When generating tests, follow these guidelines to produce high-quality, maintainable test suites.

## 1. Analyze Before Writing

- Read the source code thoroughly before writing any tests
- Identify all public methods, branches, and side effects
- Note external dependencies that need to be mocked
- Understand the expected behavior from docstrings, comments, and usage patterns
- Check existing tests in the project for conventions (naming, structure, assertion library)

## 2. Test Structure (AAA Pattern)

- **Arrange**: Set up test fixtures, mock dependencies, and prepare input data
- **Act**: Execute the single function or operation under test
- **Assert**: Verify the expected outcome with specific, descriptive assertions
- Separate the three sections with blank lines
- Each test should verify one behavior — if a test name contains "and", split it

## 3. Happy Path Tests

- Test the primary success path with valid, typical inputs
- Cover all documented return values and response shapes
- Verify side effects (database writes, events emitted, external calls made)
- Test with realistic data that resembles production values

## 4. Edge Case Tests

- Empty inputs: empty strings, empty arrays, empty objects
- Boundary values: zero, negative numbers, max int, min int, max length strings
- Null/undefined/None handling for optional parameters
- Unicode and special characters in string inputs
- Concurrent access patterns where applicable
- Large inputs that might trigger performance issues

## 5. Error Scenario Tests

- Invalid input types and malformed data
- Missing required fields
- External service failures (network errors, timeouts, 5xx responses)
- Permission/authorization failures
- Resource not found scenarios
- Duplicate/conflict scenarios (unique constraint violations)
- Rate limiting and quota exhaustion

## 6. Mocking Strategy

- Mock external HTTP clients, databases, file systems, and third-party services
- Use dependency injection to swap real implementations for test doubles
- Prefer stubs (return canned data) for queries; mocks (verify interactions) for commands
- Verify mock interactions: correct arguments, call count, call order when relevant
- Reset mocks between tests to prevent leaking state
- Avoid over-mocking — if mocking more than 3 dependencies, the unit may be too large

## 7. Test Quality Checklist

- Tests are deterministic (no random data without seeds, no time-dependent logic without mocking clocks)
- Tests are independent (can run in any order, no shared mutable state)
- Test names read as specifications: `should_return_404_when_user_not_found`
- No logic in tests (no conditionals, loops, or try/catch in test bodies)
- Use test data builders or factories for complex test fixtures
- Use parameterized/table-driven tests for testing the same logic with multiple inputs

## 8. Integration Tests

- Test real interactions between components (API endpoints, database queries)
- Use test containers or in-memory databases for isolation
- Test the full request/response cycle for API endpoints
- Verify database migrations run cleanly
- Clean up test data in teardown hooks
- Mark integration tests so they can be run separately from unit tests

## Output Format

- Group tests by the method or feature they cover
- Include setup/teardown if shared fixtures are needed
- Add brief comments explaining non-obvious test scenarios
- Follow the project's existing test file naming and directory conventions
