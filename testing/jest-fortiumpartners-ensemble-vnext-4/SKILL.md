---
name: jest
description: Execute and generate Jest tests for JavaScript/TypeScript projects
allowed-tools: Read, Bash, Grep, Glob
---

# Jest Testing Skill

Execute and generate Jest tests for JavaScript/TypeScript projects with support for unit, integration, and E2E testing.

## Test Execution

### Run All Tests

```bash
npm test
# or
npx jest
```

### Run Specific Tests

```bash
# Run tests matching a pattern
npx jest --testNamePattern="should create user"

# Run tests in a specific file
npx jest src/services/user.test.ts

# Run tests in watch mode
npx jest --watch

# Run with coverage
npx jest --coverage
```

### Common Options

```bash
# Verbose output
npx jest --verbose

# Run only changed files
npx jest --onlyChanged

# Update snapshots
npx jest --updateSnapshot

# Run in CI mode
npx jest --ci --coverage --reporters=default --reporters=jest-junit
```

## Test Patterns

### Basic Test Structure

```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepo = {
      findById: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    };
    service = new UserService(mockRepo);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('getUser', () => {
    it('should return user when found', async () => {
      const user = { id: '1', name: 'John' };
      mockRepo.findById.mockResolvedValue(user);

      const result = await service.getUser('1');

      expect(result).toEqual(user);
      expect(mockRepo.findById).toHaveBeenCalledWith('1');
    });

    it('should throw when user not found', async () => {
      mockRepo.findById.mockResolvedValue(null);

      await expect(service.getUser('999')).rejects.toThrow('User not found');
    });
  });
});
```

### Mocking

```typescript
// Mock a module
jest.mock('./api', () => ({
  fetchUser: jest.fn(),
}));

// Mock implementation
import { fetchUser } from './api';
const mockFetchUser = fetchUser as jest.MockedFunction<typeof fetchUser>;

beforeEach(() => {
  mockFetchUser.mockResolvedValue({ id: '1', name: 'Test' });
});

// Spy on methods
const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

// Mock timers
jest.useFakeTimers();
jest.advanceTimersByTime(1000);
jest.useRealTimers();
```

### Async Testing

```typescript
// Using async/await
it('fetches data asynchronously', async () => {
  const data = await fetchData();
  expect(data).toEqual({ id: 1 });
});

// Testing rejected promises
it('handles errors', async () => {
  await expect(fetchData()).rejects.toThrow('Network error');
});

// Waiting for side effects
it('updates state after fetch', async () => {
  render(<Component />);

  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
});
```

### React Component Testing

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText('Email'), 'test@example.com');
    await userEvent.type(screen.getByLabelText('Password'), 'password123');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('shows validation errors', async () => {
    render(<LoginForm onSubmit={jest.fn()} />);

    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(screen.getByText('Email is required')).toBeInTheDocument();
  });
});
```

## Configuration

### jest.config.js

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};
```

### jest.setup.ts

```typescript
import '@testing-library/jest-dom';

// Global mocks
global.fetch = jest.fn();

// Extend expect
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      message: () =>
        `expected ${received} ${pass ? 'not ' : ''}to be within range ${floor} - ${ceiling}`,
      pass,
    };
  },
});
```

## Troubleshooting

### Common Issues

1. **Tests hanging**: Check for unresolved promises or missing `done()` callbacks
2. **Mock not working**: Ensure mock is defined before importing the module
3. **Timeout errors**: Increase timeout with `jest.setTimeout(30000)`
4. **Memory issues**: Run with `--maxWorkers=2` or `--runInBand`
