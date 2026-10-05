---
name: jest
description: JavaScript testing with Jest — unit tests, mocks, spies, snapshot testing, code coverage, and configuration. Use when writing or running JavaScript/TypeScript tests, setting up a test suite with Jest, debugging failing tests, mocking modules or functions, measuring coverage, or configuring Jest in jest.config.*. Pairs with test-driven-development for the workflow/methodology. Works with React (Testing Library), Node.js, and any JS/TS project.
---

# Jest — JavaScript Testing

## Overview

Jest is the de-facto JavaScript/TypeScript test framework: zero-config setup, built-in mocking, snapshot testing, and parallel test execution. This skill is the **tool reference**; for the red-green-refactor *methodology* see [[test-driven-development]].

## Installation

```bash
# Node.js project
npm install --save-dev jest

# TypeScript
npm install --save-dev jest @types/jest ts-jest

# React (with Testing Library)
npm install --save-dev jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

## Configuration

```js
// jest.config.js (or jest.config.ts)
/** @type {import('jest').Config} */
export default {
  testEnvironment: 'node',        // or 'jsdom' for browser/React
  transform: {
    '^.+\\.tsx?$': 'ts-jest',     // TypeScript support
  },
  collectCoverageFrom: ['src/**/*.{js,ts,tsx}'],
  coverageThreshold: { global: { lines: 80 } },
};
```

Add to `package.json`:
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## Running Tests

```bash
jest                          # run all tests
jest --watch                  # watch mode (re-run on file changes)
jest --coverage               # with coverage report
jest path/to/test.spec.ts     # single file
jest -t "user login"          # filter by test name pattern
jest --bail                   # stop on first failure
jest --verbose                # detailed output
```

## Test Structure

```ts
// user.test.ts — files *.test.ts or *.spec.ts
import { createUser } from './user';

describe('createUser', () => {
  it('creates a user with a name', () => {
    const user = createUser('Alice');
    expect(user.name).toBe('Alice');
  });

  test('throws when name is empty', () => {
    expect(() => createUser('')).toThrow('Name required');
  });
});
```

## Common Matchers

```ts
expect(value).toBe(42);               // strict equality (===)
expect(obj).toEqual({ a: 1 });        // deep equality
expect(str).toMatch(/pattern/);       // regex
expect(arr).toContain('item');        // array inclusion
expect(fn).toThrow(Error);            // throws
expect(value).toBeDefined();
expect(value).toBeNull();
expect(num).toBeGreaterThan(0);
expect(arr).toHaveLength(3);
expect(obj).toHaveProperty('key', 'value');
```

## Mocking

```ts
// Mock a module
jest.mock('./api');
import { fetchUser } from './api';
(fetchUser as jest.Mock).mockResolvedValue({ id: 1, name: 'Alice' });

// Spy on a method
const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
// ... run code ...
expect(consoleSpy).toHaveBeenCalledWith('error message');
consoleSpy.mockRestore();

// Mock return values
const mockFn = jest.fn()
  .mockReturnValueOnce('first')
  .mockReturnValue('default');

// Mock async functions
const mockFetch = jest.fn().mockResolvedValue({ data: 'value' });
const mockFetchFail = jest.fn().mockRejectedValue(new Error('Network error'));
```

## Setup & Teardown

```ts
beforeAll(() => { /* runs once before all tests in block */ });
afterAll(() => { /* runs once after all tests in block */ });
beforeEach(() => { /* runs before each test */ });
afterEach(() => { /* runs after each test */ });

// Async setup
beforeEach(async () => {
  await db.connect();
});
afterEach(async () => {
  await db.disconnect();
});
```

## Snapshot Testing

```ts
// Creates/updates a snapshot file on first run
it('renders correctly', () => {
  // snapshot the DOM (asFragment), not the whole RenderResult object —
  // the latter serializes helper functions and makes noisy, brittle snapshots
  const { asFragment } = render(<Button label="Click me" />);
  expect(asFragment()).toMatchSnapshot();
});
```

```bash
# Update snapshots
jest --updateSnapshot   # or: jest -u
```

## Async Tests

```ts
// async/await
it('fetches user data', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});

// Promises
it('resolves with data', () => {
  return expect(fetchUser(1)).resolves.toMatchObject({ name: 'Alice' });
});

it('rejects on not found', () => {
  return expect(fetchUser(999)).rejects.toThrow('Not found');
});
```

## Testing React Components

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

it('calls onClick when clicked', async () => {
  const user = userEvent.setup();
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);

  await user.click(screen.getByRole('button', { name: 'Click me' }));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

it('shows loading state', () => {
  render(<Button loading>Submit</Button>);
  expect(screen.getByRole('button')).toBeDisabled();
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
```

## Coverage

```bash
jest --coverage
# Outputs: statements, branches, functions, lines coverage
# HTML report: coverage/lcov-report/index.html
```

```js
// jest.config.js — enforce thresholds
coverageThreshold: {
  global: { statements: 80, branches: 70, functions: 80, lines: 80 },
  './src/critical/**/*.ts': { lines: 95 },
}
```

## Common Patterns

```ts
// Test each with different inputs
it.each([
  [1, 1, 2],
  [2, 3, 5],
  [0, -1, -1],
])('add(%i, %i) = %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});

// Skip or focus
it.skip('pending test', () => { /* ... */ });
it.only('focused test', () => { /* ... */ });
describe.only('focused suite', () => { /* ... */ });

// Custom matchers (extend)
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return { pass, message: () => `expected ${received} to be within [${floor}, ${ceiling}]` };
  },
});
expect(100).toBeWithinRange(90, 110);
```

## Debugging Failing Tests

```bash
# Verbose output with full error traces
jest --verbose --no-coverage

# Run a single test file
jest src/components/Button.test.tsx --verbose

# Debug with Node inspector
node --inspect-brk node_modules/.bin/jest --runInBand

# Check mock calls
console.log(mockFn.mock.calls);    // all calls
console.log(mockFn.mock.results);  // all return values
```

## Related Skills

- [[test-driven-development]] — TDD methodology and workflow
- [[playwright-best-practices]] — End-to-end browser testing
- [[vitest]] — Faster alternative for Vite-based projects
- [[property-based-testing]] — Generative testing with property-based approaches
