---
name: typescript-react
description: TypeScript/React conventions for dashboards
---

# TypeScript/React Conventions

## Stack Overview
- **Framework**: Next.js 12.x with React 17
- **Language**: TypeScript (strict mode)
- **State Management**: Redux Toolkit with Redux Persist
- **Styling**: SCSS modules with Sass
- **Testing**: Jest + React Testing Library + Playwright (E2E)

## Project Structure
```
├── components/       # Reusable UI components with SCSS modules
├── pageComponents/   # Page-specific complex components
├── pages/            # Next.js pages with API routes in pages/api/
├── redux/            # Redux store, actions, reducers, thunks
├── interfaces/       # TypeScript interface definitions
├── utilities/        # Helper functions and utilities
├── middlewares/      # API middleware functions
├── constants/        # Application constants and configuration
├── hooks/            # Custom React hooks
├── styles/           # Global SCSS styles and variables
```

## Path Aliases
Use path aliases instead of relative imports:
```typescript
// tsconfig.json paths
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import { OrderInterface } from '@/interfaces/Order';
```

Standard aliases:
- `@/components/*` → `components/*`
- `@/pages/*` → `pages/*`
- `@/redux/*` → `redux/*`
- `@/utilities/*` → `utilities/*`
- `@/interfaces/*` → `interfaces/*`
- `@/pageComponents/*` → `pageComponents/*`
- `@/middlewares/*` → `middlewares/*`
- `@/constants/*` → `constants/*`
- `@/styles/*` → `styles/*`
- `@/hooks/*` → `hooks/*`

## State Management

### Redux Toolkit Pattern
```typescript
// Use typed hooks
import { useAppDispatch, useAppSelector } from '@/redux/hooks';

// In components
const dispatch = useAppDispatch();
const orders = useAppSelector(state => state.orders.items);
```

### Thunk Pattern
```typescript
export const fetchOrders = createAsyncThunk(
  'orders/fetch',
  async (params: FetchParams, { rejectWithValue }) => {
    try {
      const response = await api.getOrders(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);
```

## Component Architecture

### SCSS Modules
```tsx
// Component.tsx
import styles from './Component.module.scss';

export const Component = () => (
  <div className={styles.container}>
    <h1 className={styles.title}>Title</h1>
  </div>
);
```

### TypeScript Interfaces
```typescript
// interfaces/Order.ts
export interface Order {
  id: number;
  appId: number;
  status: OrderStatus;
  createdAt: string;
}

// Component props
interface OrderCardProps {
  order: Order;
  onSelect: (id: number) => void;
}
```

## Testing

### Unit Tests
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### E2E Tests (Playwright)
```typescript
test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Commands
```bash
npm run dev          # Start development server
npm run build        # Build production
npm run lint         # Run ESLint
npm run lint:fix     # Auto-fix lint issues
npm run format       # Format with Prettier
npm test             # Run Jest tests
npm run test:e2e     # Run Playwright E2E tests
```

## Before Making Changes
1. Run `npm run lint` and `npm run format:check`
2. Ensure tests pass with `npm test`
3. Check type safety - project uses strict TypeScript
4. Follow SCSS module patterns for styling
5. Use path aliases instead of relative imports
