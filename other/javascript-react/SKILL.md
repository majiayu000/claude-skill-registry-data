---
name: epci:javascript-react
description: >-
  Patterns for React islands in Django. Includes TypeScript, Vite, Zustand,
  React Query, Tailwind, accessibility. Use when: React TypeScript development, package json react detected, frontend react components.
  Not for: Vue framework, Angular projects, backend Node development.
user-invocable: false
---

# JavaScript/React Development Patterns

## Overview

React islands architecture for Django applications. React enhances interactive zones within server-rendered pages. See `references/` for detailed examples.

## Auto-detection

Loaded when detecting:
- `package.json` containing `react`
- Files: `*.tsx`, `*.jsx`, `vite.config.ts`
- Structure: `src/components/`, `src/hooks/`

## Islands Architecture

### Philosophy

Django renders pages → React enhances interactive zones. **Not an SPA.**

| Benefit | Description |
|---------|-------------|
| Single deployment | One Docker, one CI/CD |
| Django handles auth | Sessions, permissions, CSRF |
| No CORS issues | Same origin |
| SEO-friendly | Server-rendered HTML |

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/javascript-react/references/islands-architecture.md` for full patterns

### Component Mounting

```html
<!-- Django template -->
<div
    data-react-component="DataTable"
    data-react-props='{"endpoint": "/api/v1/lots/"}'
></div>
```

```tsx
// main.tsx - Component Registry
const COMPONENTS = { DataTable, KpiChart, LotForm };

document.querySelectorAll('[data-react-component]').forEach((el) => {
  const name = el.getAttribute('data-react-component')!;
  const props = JSON.parse(el.getAttribute('data-react-props') || '{}');
  createRoot(el).render(<COMPONENTS[name] {...props} />);
});
```

### Vite Configuration

```typescript
// vite.config.ts
export default defineConfig({
  base: '/static/assets/',           // Match Django STATIC_URL
  build: {
    outDir: '../backend/static/assets',
    manifest: true,
  },
});
```

## CSRF Token (Critical)

**All POST/PUT/DELETE to Django require CSRF token.**

```typescript
// utils/csrf.ts
export function getCsrfToken(): string {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || '';
}

// Usage with fetch
headers: {
  'Content-Type': 'application/json',
  'X-CSRFToken': getCsrfToken(),
}
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/javascript-react/references/state-data.md` for React Query integration

## State Management

### Decision Matrix

| Scope | Solution |
|-------|----------|
| Component local | `useState` |
| Complex local | `useReducer` |
| Island shared | React Context |
| Cross-component | **Zustand** |
| Server state | **React Query** |

### Zustand Pattern

```typescript
import { create } from 'zustand';

export const useLotStore = create((set) => ({
  selectedLots: [],
  selectLot: (lot) => set((s) => ({
    selectedLots: [...s.selectedLots, lot]
  })),
}));
```

### React Query Pattern

```typescript
const { data, isLoading } = useQuery({
  queryKey: ['lots'],
  queryFn: () => fetch('/api/v1/lots/').then(r => r.json()),
});

const mutation = useMutation({
  mutationFn: (data) => fetch('/api/v1/lots/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCsrfToken(), 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }),
});
```

## Components

### TypeScript Props

```tsx
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  onClick?: () => void;
  disabled?: boolean;
}

export function Button({ children, variant = 'primary', ...props }: ButtonProps) {
  return <button className={cn(baseClasses, variantClasses[variant])} {...props}>{children}</button>;
}
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/javascript-react/references/components-ui.md` for Tailwind, shadcn, accessibility

## Testing

```tsx
// Vitest + React Testing Library
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Button', () => {
  it('calls onClick when clicked', async () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);
    await userEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalled();
  });
});
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/javascript-react/references/testing.md` for hooks, React Query, mocking

## Commands

```bash
# Development
npm run dev         # Vite dev server with HMR
npm run build       # Production build
npm run preview     # Preview production build

# Testing
npm test            # Run all tests
npm test -- --watch # Watch mode
npm test -- --coverage

# Quality
npm run lint        # ESLint
npm run type-check  # TypeScript
```

## Quick Reference

| Task | Pattern |
|------|---------|
| Mount component | `data-react-component` + registry |
| Pass props | `data-react-props='{"key": "value"}'` |
| CSRF token | `X-CSRFToken: getCsrfToken()` |
| Client state | Zustand store |
| Server state | React Query |
| Styling | Tailwind + cn() utility |
| Forms | react-hook-form + zod |
| Animation | Framer Motion |
| Icons | Lucide React |

## Common Patterns

| Pattern | Example |
|---------|---------|
| Component registry | `const COMPONENTS = { ... }` in main.tsx |
| Conditional mount | `if (el) createRoot(el).render(...)` |
| Props from Django | `{{ data\|safe }}` in template |
| Error boundary | Wrap islands in `<ErrorBoundary>` |
| Loading states | `{ isLoading ? <Spinner /> : <Content /> }` |
| Optimistic updates | React Query `onMutate` |
| Form validation | zod schema + zodResolver |
| Accessibility | Radix UI primitives |

## Anti-patterns

| Anti-pattern | Why Avoid | Alternative |
|--------------|-----------|-------------|
| React Router SPA | Django handles routing | Islands pattern |
| Global Redux | Overkill for islands | Zustand per-feature |
| Inline styles | Hard to maintain | Tailwind classes |
| `any` types | No type safety | Explicit interfaces |
| Mix HTMX + React zones | Zone conflicts | Separate zones |
| Forget CSRF | 403 errors on mutations | Always include token |
| `getByTestId` first | Bad accessibility | `getByRole`, `getByLabelText` |
| Direct DOM manipulation | React state conflicts | Use React state |
| Hardcoded API URLs | Breaks environments | Pass via props |
| Skip error handling | Silent failures | Error boundaries + toasts |

## Zone Separation

**Critical**: Never mix HTMX and React on same element.

```html
<!-- HTMX zone -->
<div hx-get="/partials/notifications" hx-trigger="every 30s"></div>

<!-- React zone (separate) -->
<div data-react-component="DataTable"></div>
```

→ See `${CLAUDE_PLUGIN_ROOT}/skills/stack/javascript-react/references/islands-architecture.md` for decision matrix
