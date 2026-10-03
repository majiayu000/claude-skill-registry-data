---
name: unit-testing
description: Write and maintain Vitest unit tests for this codebase, including React Testing Library component tests, service and utility tests, API handler unit tests, mocks, fixtures, and jsdom setup patterns.
---

# Unit Testing Skill

When writing unit tests for this codebase, follow the established patterns using Vitest and React Testing Library.

## Overview

- **Framework**: Vitest (`tests/unit/*.unit.spec.ts`)
- **Environment**: jsdom (browser-like for components)
- **Libraries**: vi (Vitest built-in), React Testing Library for components
- **Setup**: `vitest.setup.tsx` with RTL configuration

## Directory Structure

```
tests/
├── unit/             # Unit tests (.unit.spec.ts)
│   ├── api/          # API handler unit tests
│   ├── config/       # Configuration unit tests
│   └── bugfixes/     # Bug-specific unit tests
└── vitest.setup.tsx  # RTL setup and global mocks
```

---

## Basic Test Structure

```typescript
import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';

describe('Analytics Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test('should consistently hash the same email', async () => {
    const { hashEmail } = await import('../../server/analytics/analyticsService');

    const email = 'test@example.com';
    const hash1 = await hashEmail(email);
    const hash2 = await hashEmail(email);

    expect(hash1).toBe(hash2);
    expect(hash1).toMatch(/^[a-f0-9]{64}$/);
  });
});
```

---

## Mocking External Dependencies

### Mock Entire Modules

```typescript
// Mock before importing the module under test
vi.mock('@server/stripe', () => ({
  stripe: {
    webhooks: {
      constructEventAsync: vi.fn(),
    },
  },
}));

vi.mock('@server/supabase', () => ({
  supabase: {
    from: vi.fn(() => ({
      select: vi.fn(() => ({
        eq: vi.fn(() => ({
          single: vi.fn(() => Promise.resolve({ data: null })),
        })),
      })),
    })),
  },
}));
```

### Mock with Specific Return Values

```typescript
const mockConstructEvent = vi.fn().mockResolvedValueOnce({
  type: 'invoice.payment_succeeded',
  data: { object: mockInvoice },
});

vi.mock('@server/stripe', () => ({
  stripe: {
    webhooks: {
      constructEventAsync: mockConstructEvent,
    },
  },
}));
```

### Spy on Existing Functions

```typescript
import { myService } from './myService';

test('should call service method', () => {
  const spy = vi.spyOn(myService, 'method');
  spy.mockResolvedValue({ data: 'test' });

  // Test code...

  expect(spy).toHaveBeenCalledWith(expectedArgs);
});
```

### Mock Environment Variables

```typescript
// Proxy-based env mocking
let mockEnv = {
  STRIPE_SECRET_KEY: 'sk_test_dummy_key',
  ENV: 'test',
};

vi.mock('@shared/config/env', () => ({
  serverEnv: new Proxy({} as Record<string, string>, {
    get(_, prop) {
      return mockEnv[prop as keyof typeof mockEnv];
    },
  }),
}));
```

### Dynamic Imports for Mock Control

Use dynamic imports to avoid module caching issues and get fresh modules:

```typescript
test('should process webhook', async () => {
  // Import inside test to get fresh module with mocks
  const { handleInvoicePaymentSucceeded } = await import('./handler');

  const result = await handleInvoicePaymentSucceeded(mockEvent);

  expect(result.success).toBeTruthy();
});
```

---

## Testing Services

```typescript
describe('Subscription Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('should calculate upgrade credits correctly', async () => {
    // Mock dependencies
    vi.mock('@server/stripe', () => ({
      stripe: {
        subscriptions: {
          retrieve: vi.fn(() => Promise.resolve(subscriptionData)),
        },
      },
    }));

    // Import after mocking
    const { calculateUpgradeCredits } = await import('./subscriptionService');

    const result = await calculateUpgradeCredits('sub_123');

    expect(result.creditsToAdd).toBe(100);
    expect(result.isLegitimate).toBe(true);
  });
});
```

---

## Testing API Handlers

```typescript
describe('Stripe Webhook Handler', () => {
  let mockEvent: Stripe.Event;

  beforeEach(() => {
    mockEvent = {
      type: 'invoice.payment_succeeded',
      data: { object: mockInvoice },
    } as Stripe.Event;

    vi.clearAllMocks();
  });

  test('should handle invoice.payment_succeeded', async () => {
    // Mock the webhook construction
    vi.mock('@server/stripe', () => ({
      stripe: {
        webhooks: {
          constructEventAsync: vi.fn(() => Promise.resolve(mockEvent)),
        },
      },
    }));

    // Import handler with mocks
    const { POST } = await import('./route');

    // Create mock request
    const request = new Request('https://example.com/api/webhooks/stripe', {
      method: 'POST',
      body: JSON.stringify(mockEvent),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.success).toBe(true);
  });
});
```

---

## Testing Utilities

```typescript
describe('Image Validation Utility', () => {
  test('should validate minimum image size', () => {
    const { isValidImageSize } = require('./imageValidation');

    expect(isValidImageSize(64, 64)).toBe(true);
    expect(isValidImageSize(32, 32)).toBe(false);
  });

  test('should validate mime type', () => {
    const { isValidMimeType } = require('./imageValidation');

    expect(isValidMimeType('image/png')).toBe(true);
    expect(isValidMimeType('image/jpeg')).toBe(true);
    expect(isValidMimeType('application/pdf')).toBe(false);
  });
});
```

---

## Testing Components (React Testing Library)

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Button } from './Button';

describe('Button Component', () => {
  test('should render children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  test('should call onClick handler', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByRole('button'));

    await waitFor(() => {
      expect(handleClick).toHaveBeenCalledTimes(1);
    });
  });

  test('should be disabled when loading', () => {
    render(<Button loading>Loading...</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

---

## Error Boundary Testing

```typescript
describe('Error Boundary', () => {
  test('should catch and render error', () => {
    const ThrowError = () => {
      throw new Error('Test error');
    };

    const { container } = render(
      <ErrorBoundary fallback={<div>Something went wrong</div>}>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  });
});
```

---

## Testing Async Code

```typescript
describe('Async Operations', () => {
  test('should handle promises', async () => {
    const { fetchData } = await import('./api');

    const result = await fetchData('/api/data');

    expect(result).toBeDefined();
  });

  test('should handle timeout', async () => {
    vi.useFakeTimers();

    const { delayedFunction } = await import('./utils');

    const promise = delayedFunction();
    vi.advanceTimersByTime(1000);

    await expect(promise).resolves.toBe('done');

    vi.useRealTimers();
  });
});
```

---

## Mock Implementation Patterns

### Webhook Mocking

```typescript
const getWebhookEventsMock = () => ({
  select: vi.fn(() => ({
    eq: vi.fn(() => ({
      single: vi.fn(() => Promise.resolve({ data: null })),
    })),
  })),
  insert: vi.fn(() => Promise.resolve({ error: null })),
});

vi.mock('@server/supabase', () => ({
  supabase: {
    from: vi.fn(() => getWebhookEventsMock()),
  },
}));
```

### Service Mocking

```typescript
vi.mock('@server/services/SubscriptionCredits', () => ({
  SubscriptionCreditsService: {
    calculateUpgradeCredits: vi.fn(() => ({
      creditsToAdd: 100,
      reason: 'Upgrade eligible',
      isLegitimate: true,
    })),
  },
}));
```

### Supabase Client Mocking

```typescript
vi.mock('@server/supabase/client', () => ({
  createClient: vi.fn(() => ({
    from: vi.fn(() => mockTable),
    auth: {
      getUser: vi.fn(() => Promise.resolve({ data: { user } })),
    },
  })),
}));
```

---

## Common Pitfalls to Avoid

### 1. Not Clearing Mocks

**Bad**: Mocks persist between tests

```typescript
test('first test', async () => {
  vi.mock('./module', () => ({ fn: vi.fn(() => 'first') }));
});

test('second test', async () => {
  // Still uses first test's mock!
  const { fn } = await import('./module');
});
```

**Good**: Always clear and restore

```typescript
beforeEach(() => {
  vi.clearAllMocks();
});

afterEach(() => {
  vi.restoreAllMocks();
});
```

### 2. Module Caching Issues

**Bad**: Static import loads module before mocks

```typescript
import { myFunction } from './module'; // Imported before mock!

vi.mock('./module');
```

**Good**: Dynamic import after mock

```typescript
vi.mock('./module');

test('should work', async () => {
  const { myFunction } = await import('./module'); // Fresh import
});
```

### 3. Not Testing Error Cases

**Bad**: Only happy path

```typescript
test('should succeed', async () => {
  const result = await myFunction();
  expect(result).toBe('success');
});
```

**Good**: Test failures too

```typescript
test('should succeed', async () => {
  const result = await myFunction();
  expect(result).toBe('success');
});

test('should handle errors', async () => {
  vi.mock('./dependency', () => ({
    dep: vi.fn(() => Promise.reject(new Error('API error'))),
  }));

  const { myFunction } = await import('./module');

  await expect(myFunction()).rejects.toThrow('API error');
});
```

### 4. Over-specifying Tests

**Bad**: Testing implementation details

```typescript
test('should call three functions', () => {
  myFunction();
  expect(fn1).toHaveBeenCalled();
  expect(fn2).toHaveBeenCalled();
  expect(fn3).toHaveBeenCalled();
});
```

**Good**: Test behavior/outcome

```typescript
test('should return correct result', () => {
  const result = myFunction(input);
  expect(result).toEqual(expectedOutput);
});
```

---

## Best Practices

### Test Organization

```typescript
describe('Feature Name', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Sub-feature', () => {
    test('specific behavior', async () => {
      // Test implementation
    });
  });
});
```

### Descriptive Test Names

```typescript
// Bad
test('works', () => {});

// Good
test('should return 400 when email is invalid', () => {});
test('should hash email consistently', () => {});
```

### AAA Pattern (Arrange, Act, Assert)

```typescript
test('should calculate total with tax', () => {
  // Arrange
  const subtotal = 100;
  const taxRate = 0.1;

  // Act
  const total = calculateTotal(subtotal, taxRate);

  // Assert
  expect(total).toBe(110);
});
```

---

## Testing Commands

```bash
# Run all unit tests
yarn test:unit

# Run specific test file
yarn test:unit tests/unit/api/stripe.unit.spec.ts

# Watch mode
yarn test:watch

# With coverage
yarn test:coverage

# Full verification
yarn verify
```

---

## Before Finishing

1. **Write tests** for your changes following the patterns above
2. **Mock all external dependencies** (Stripe, Supabase, APIs)
3. **Run tests**: `yarn test:unit`
4. **Run verify**: `yarn verify` (required before completing any task)

## Key Files to Reference

- `vitest.config.ts` - Vitest configuration
- `vitest.setup.tsx` - React Testing Library setup
- `tests/unit/` - Example unit tests for reference
