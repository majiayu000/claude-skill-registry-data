---
name: testing-strategist
version: "2.0"
trigger: testing strategy, test coverage, unit test, integration test, E2E
description: Comprehensive testing strategies including unit tests, integration tests, E2E tests, property-based testing, visual regression, and test automation. Use when writing tests, setting up testing frameworks, or designing test coverage strategies.
---

# Testing Strategist

## Testing Pyramid

```
    /\
   /  \  E2E Tests (Playwright) - 10%
  /____\
 /      \ Integration Tests - 30%
/________\
Unit Tests (Jest/Vitest) - 60%
```

## Unit Testing

### Component Tests
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('renders user information', () => {
    const user = { name: 'John', email: 'john@example.com' };
    render(<UserProfile user={user} />);
    
    expect(screen.getByText('John')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });
  
  it('handles edit action', () => {
    const onEdit = vi.fn();
    render(<UserProfile user={user} onEdit={onEdit} />);
    
    fireEvent.click(screen.getByText('Edit'));
    expect(onEdit).toHaveBeenCalled();
  });
});
```

### Custom Hook Tests
```typescript
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter(0));
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });
});
```

## Integration Testing

### API Route Tests
```typescript
import { createTestServer } from '@/test/utils';

describe('POST /api/users', () => {
  const server = createTestServer();
  
  it('creates user with valid data', async () => {
    const response = await server
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'Secure123!' })
      .expect(201);
    
    expect(response.body.data.email).toBe('test@example.com');
  });
  
  it('rejects invalid email', async () => {
    await server
      .post('/api/users')
      .send({ email: 'invalid', password: 'pass' })
      .expect(400);
  });
});
```

### Database Integration
```typescript
describe('UserRepository', () => {
  beforeEach(async () => {
    await db.delete(users);
  });
  
  it('creates and retrieves user', async () => {
    const user = await userRepo.create({
      email: 'test@example.com',
      name: 'Test User'
    });
    
    const retrieved = await userRepo.findById(user.id);
    expect(retrieved?.email).toBe('test@example.com');
  });
});
```

## E2E Testing (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('user can log in', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
  
  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrong');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('.error')).toContainText('Invalid credentials');
  });
});
```

## Property-Based Testing

```typescript
import { fc, test } from '@fast-check/vitest';

test.prop([fc.array(fc.integer())])('sort is idempotent', (arr) => {
  const sorted = [...arr].sort((a, b) => a - b);
  const sortedAgain = [...sorted].sort((a, b) => a - b);
  expect(sorted).toEqual(sortedAgain);
});
```

## Test Coverage Strategy

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
        statements: 80
      },
      exclude: [
        '**/*.config.*',
        '**/node_modules/**',
        '**/__tests__/**'
      ]
    }
  }
});
```

## Mocking Patterns

```typescript
// Mock external services
vi.mock('@/integrations/stripe', () => ({
  createPaymentIntent: vi.fn().mockResolvedValue({
    clientSecret: 'secret_123'
  })
}));

// Mock database
vi.mock('@/db', () => ({
  db: {
    query: {
      users: {
        findFirst: vi.fn()
      }
    }
  }
}));
```
