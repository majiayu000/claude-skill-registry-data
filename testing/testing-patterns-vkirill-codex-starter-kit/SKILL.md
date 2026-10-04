---
name: testing-patterns
description: Jest/Vitest testing patterns, factory functions, mocking strategies, and TDD workflow. Use when writing unit tests, creating test factories, or following TDD red-green-refactor cycle.
stacks:
  - testing
packages:
  - "@playwright/test"
  - playwright
  - jest
  - vitest
tags:
  - testing
  - test
user-invocable: false
references: references/REFERENCE.md
assets: assets/vitest.config.template.ts
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when

- Writing unit or integration tests with Jest or Vitest
- Creating factory functions for test data or component props
- Setting up mocks for modules, API hooks, or external dependencies
- Following TDD red-green-refactor cycle

## Do not use this skill when

- Writing end-to-end tests with Playwright (consult Playwright docs directly)
- The project has no test framework installed

## Purpose

Testing patterns expert. Knows Jest and Vitest deeply — factory pattern, mocking strategies, render utilities, query patterns, and TDD workflow. Produces tests that verify behavior, not implementation details, and remain maintainable as code evolves.

## Capabilities

### Testing Philosophy

Test-Driven Development: write a failing test first, implement the minimal code to pass it, then refactor. Never write production code without a failing test covering the behavior.

Behavior-Driven Testing: test public APIs and business requirements, not internal implementation details. Use descriptive test names that read like specifications.

Factory Pattern: create `getMockX(overrides?: Partial<X>)` functions that provide sensible defaults and allow overriding specific properties. This keeps tests DRY and prevents inconsistent test data.

### Test Utilities

Create a custom render function that wraps components with required providers (ThemeProvider, Router, store). Import and use this wrapper in all component tests instead of bare `render`. This prevents duplicated provider setup across test files.

### Factory Pattern

Component props factories follow the pattern `getMockMyComponentProps(overrides?)` returning a complete props object merged with overrides. Data factories follow `getMockUser(overrides?): User` returning a typed object with realistic defaults. Always type factory return values explicitly.

Use factories when multiple tests need the same data shape. Avoid inline object literals that duplicate field names — a missing field in one test will silently produce incorrect behavior.

### Mocking Patterns

Mock entire modules with `jest.mock('module-path')`. When the mock needs a specific shape use the factory function form: `jest.mock('path', () => ({ ... }))`. Access the mock instance via `jest.requireMock('path')`.

For GraphQL or data-fetching hooks, mock the generated hook module, then in each test call `.mockReturnValue({ data: ..., loading: false, error: undefined })` to control what the component receives.

### Test Structure

Organize tests with nested `describe` blocks: outer block names the component or module, inner blocks group by behavior category (Rendering, User interactions, Edge cases). Use `beforeEach(() => jest.clearAllMocks())` to reset state between tests.

### Query Patterns

Use `getByText`, `getByRole`, `getByLabelText` for elements that must exist. Use `queryByText` for elements that may not exist (assert `toBeNull()`). Use `findBy*` variants (which return promises) for elements that appear asynchronously, wrapped in `await waitFor`.

### User Interaction Patterns

Simulate text input with `fireEvent.changeText`. Simulate taps and presses with `fireEvent.press`. For interactions that trigger async state updates, wrap assertions in `await waitFor(() => { expect(...) })`.

## Behavioral Traits

- Always creates factory functions rather than duplicating inline test objects
- Tests behavior and visible output, not which mocks were called
- Groups tests with `describe` and clears mocks in `beforeEach`
- Uses typed factory returns to catch missing fields at compile time
- Writes one focused assertion per test when possible

## Important Constraints

- NEVER test mock call counts as the primary assertion — test visible output instead
- ALWAYS use factory functions for props and data — inline objects with missing fields cause silent failures
- ALWAYS clear mocks between tests to prevent test-order dependencies
- NEVER import implementation details from the module under test — only public exports

## Integration with Other Skills

- **react-ui-patterns**: test all UI states (loading, error, empty, success)
- **systematic-debugging**: write a test that reproduces the bug before fixing it

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
