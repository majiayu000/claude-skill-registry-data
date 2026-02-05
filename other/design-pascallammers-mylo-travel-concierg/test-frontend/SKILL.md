---
name: Test Frontend
description: Run and verify frontend tests for the React/Vite application.
---

# Test Frontend

Run and verify frontend tests using Vitest and React Testing Library. This skill handles test execution, watches for changes, generates coverage reports, and helps diagnose test failures.

## Instructions

### Prerequisites

- Node.js and npm installed
- Frontend dependencies installed (`npm install` in `frontend/` directory)
- Project uses Vitest with jsdom environment
- Tests located in `frontend/src/tests/`

### Workflow

1. Navigate to the `frontend/` directory
2. Choose appropriate test command based on user needs:
   - `npm run test` - Run all tests once (CI/CD mode)
   - `npm run test:watch` - Run tests in watch mode (development)
   - `npm run test:coverage` - Run tests with coverage report
3. Analyze test results and report findings to user
4. If tests fail, investigate failures and suggest fixes
5. If requested, help write or update tests using Testing Library patterns

### Testing Stack

- **Test Runner**: Vitest
- **Testing Library**: @testing-library/react, @testing-library/jest-dom
- **Environment**: jsdom
- **Coverage**: Built-in Vitest coverage

## Examples

### Example 1: Run All Tests

User: "Run the frontend tests"
Assistant: I'll run the frontend test suite.
[Executes: `cd frontend && npm run test`]
[Reports results and any failures]

### Example 2: Run Tests with Coverage

User: "Check test coverage for the frontend"
Assistant: I'll run the tests with coverage reporting.
[Executes: `cd frontend && npm run test:coverage`]
[Reports coverage percentages and identifies untested code]

### Example 3: Debug Test Failure

User: "The AgentFlow tests are failing"
Assistant: Let me run the tests and investigate the failures.
[Executes: `cd frontend && npm run test`]
[Analyzes failure output, reads test file if needed]
[Suggests fixes based on error messages]

### Example 4: Watch Mode for Development

User: "Run tests in watch mode while I develop"
Assistant: I'll start the test watcher.
[Executes: `cd frontend && npm run test:watch`]
[Note: This runs in background, user can continue development]