---
name: testing
description: Generate test suite for existing code
type: generate
project_types: [web-app, api, library, cli, tui]
trigger: "create test, generate tests, add testing"
inputs:
  - name: target
    description: File or directory to test
    required: true
  - name: type
    description: Test type (unit, integration, e2e)
    required: false
    default: "unit"
---

## Context

Project {{project_name}} uses {{stack}} with test framework {{test_framework}}.
Generate {{input.type}} tests for: {{input.target}}.

Read AGENTS.md for testing conventions.

## Instructions

1. **Analyze target code**
   - Read the file/directory to be tested: {{input.target}}
   - Identify: exports, functions, classes, side effects
   - Identify: dependencies that need to be mocked
   - Understand business logic and edge cases

2. **Analyze existing tests**
   - Read existing test files to understand patterns
   - Identify: test structure, naming convention, setup/teardown
   - Identify: mock patterns, fixture usage

3. **Generate test file**
   - Path: according to project convention
     - Co-located: `{{input.target}}.test.ts`
     - Separate: `tests/{{input.target}}.test.ts`
   - Structure:
     ```
     describe('[Module/Function name]', () => {
       describe('[method/scenario]', () => {
         it('should [expected behavior]', () => {})
       })
     })
     ```

4. **Test categories based on type:**

   **Unit tests:**
   - Happy path (expected input -> expected output)
   - Edge cases (empty, null, boundary values)
   - Error cases (invalid input, thrown errors)
   - Mock external dependencies

   **Integration tests:**
   - API endpoint tests (request -> response)
   - Database operations (CRUD + constraints)
   - Service interactions (service A calls service B)
   - Use real dependencies (test DB, not mocks)

   **E2E tests:**
   - User flows (register -> login -> use feature)
   - Browser interactions (click, type, navigate)
   - Visual verification (if applicable)

5. **Setup test utilities** (if not already present)
   - Test database setup/teardown (integration)
   - Common fixtures/factories
   - Mock helpers

## Validation

- [ ] Test file created in the correct location
- [ ] All tests passing
- [ ] Coverage increase for target files
- [ ] No skipped tests
- [ ] Test names descriptive and clear
- [ ] Mocks/fixtures clean (no leaked state between tests)
