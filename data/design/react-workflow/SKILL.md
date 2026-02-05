---
name: react-workflow
description: React framework workflow guidelines. Activate when working with React components (.jsx, .tsx), React hooks (useState, useEffect), or React-specific patterns.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# React Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | Biome | `biome check .` |
| Format | Biome | `biome format --write .` |
| Test | Vitest + Testing Library | `vitest` |
| E2E | Playwright | `playwright test` |

---

## Component Architecture

### Functional Components Only

Components MUST be functional components. Class components MUST NOT be used.

```tsx
// CORRECT
function UserProfile({ user }: UserProfileProps) {
  return <div>{user.name}</div>;
}

// ALSO CORRECT
const UserProfile = ({ user }: UserProfileProps) => {
  return <div>{user.name}</div>;
};

// INCORRECT - MUST NOT use class components
class UserProfile extends Component { ... }
```

### Component Naming

- Component files MUST use PascalCase: `UserProfile.tsx`
- Components MUST be named exports for better tree-shaking
- One component per file SHOULD be the default; co-located helpers are OPTIONAL

### Props Interface

Props MUST be typed with explicit interfaces:

```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary';
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({ variant, disabled = false, children, onClick }: ButtonProps) {
  return (
    <button className={variant} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}
```

---

## React 19 Features

### useActionState

Server actions SHOULD use `useActionState` for form handling:

```tsx
import { useActionState } from 'react';

function LoginForm() {
  const [state, formAction, isPending] = useActionState(loginAction, null);

  return (
    <form action={formAction}>
      <input name="email" type="email" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Logging in...' : 'Log in'}
      </button>
      {state?.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

### useFormStatus

Form submission state SHOULD use `useFormStatus` in child components:

```tsx
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}
```

### useOptimistic

Optimistic updates SHOULD use `useOptimistic`:

```tsx
import { useOptimistic } from 'react';

function TodoList({ todos, addTodo }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  );

  async function handleAdd(formData: FormData) {
    const newTodo = { id: crypto.randomUUID(), text: formData.get('text') };
    addOptimisticTodo(newTodo);
    await addTodo(newTodo);
  }

  return (
    <form action={handleAdd}>
      {optimisticTodos.map(todo => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.text}
        </li>
      ))}
    </form>
  );
}
```

### use() Hook

The `use()` hook MAY be used to read promises and context:

```tsx
import { use, Suspense } from 'react';

function UserData({ userPromise }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}

// Usage with Suspense
<Suspense fallback={<Skeleton />}>
  <UserData userPromise={fetchUser(id)} />
</Suspense>
```

---

## Server Components (RSC)

### Default to Server Components

Components SHOULD be Server Components by default. Client Components MUST use the `'use client'` directive.

```tsx
// Server Component (default) - no directive needed
async function UserList() {
  const users = await db.users.findMany();
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Client Component - requires directive
'use client';

import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### RSC Patterns

- Data fetching SHOULD happen in Server Components
- Interactive elements MUST be Client Components
- Server Components MUST NOT use hooks or browser APIs
- Client Components SHOULD be pushed to the leaves of the component tree

---

## React Compiler

### Automatic Memoization

React Compiler handles memoization automatically. Manual memoization SHOULD NOT be used unless profiling shows a specific need:

```tsx
// RECOMMENDED - let React Compiler optimize
function ExpensiveList({ items, filter }) {
  const filtered = items.filter(filter);
  return <ul>{filtered.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}

// AVOID - unnecessary manual memoization
function ExpensiveList({ items, filter }) {
  const filtered = useMemo(() => items.filter(filter), [items, filter]);
  return <ul>{filtered.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

### Compiler Requirements

- Components MUST follow the Rules of React (pure rendering, immutable props)
- Side effects MUST be in useEffect or event handlers
- State updates MUST be immutable

---

## Testing

### Testing Library Patterns

Tests MUST use accessible queries. Priority order:

1. `getByRole` (RECOMMENDED)
2. `getByLabelText` (for form fields)
3. `getByPlaceholderText` (when no label)
4. `getByText` (for non-interactive elements)
5. `getByTestId` (last resort)

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits form with user data', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<LoginForm onSubmit={onSubmit} />);

  // CORRECT - uses accessible queries
  await user.type(screen.getByRole('textbox', { name: /email/i }), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'secret123');
  await user.click(screen.getByRole('button', { name: /log in/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'secret123'
  });
});
```

### User Event

User interactions MUST use `@testing-library/user-event` over `fireEvent`:

```tsx
// CORRECT
const user = userEvent.setup();
await user.click(button);
await user.type(input, 'text');

// AVOID
fireEvent.click(button);
fireEvent.change(input, { target: { value: 'text' } });
```

### Async Queries

Async operations MUST use `findBy*` or `waitFor`:

```tsx
// CORRECT
const successMessage = await screen.findByRole('alert');
expect(successMessage).toHaveTextContent('Saved!');

// CORRECT
await waitFor(() => {
  expect(screen.getByRole('list')).toHaveTextContent('Item 1');
});
```

---

## Accessibility

### ARIA Requirements

Interactive elements MUST have accessible names:

```tsx
// CORRECT
<button aria-label="Close dialog">
  <CloseIcon />
</button>

// CORRECT
<button>
  <CloseIcon aria-hidden="true" />
  <span className="sr-only">Close dialog</span>
</button>

// INCORRECT - no accessible name
<button>
  <CloseIcon />
</button>
```

### Keyboard Navigation

All interactive elements MUST be keyboard accessible:

```tsx
function Menu({ items }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex(i => Math.min(i + 1, items.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex(i => Math.max(i - 1, 0));
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        items[activeIndex].onSelect();
        break;
    }
  };

  return (
    <ul role="menu" onKeyDown={handleKeyDown}>
      {items.map((item, i) => (
        <li
          key={item.id}
          role="menuitem"
          tabIndex={i === activeIndex ? 0 : -1}
          aria-selected={i === activeIndex}
        >
          {item.label}
        </li>
      ))}
    </ul>
  );
}
```

### Focus Management

Focus MUST be managed appropriately for modals, dialogs, and dynamic content:

```tsx
function Dialog({ isOpen, onClose, children }) {
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      dialogRef.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      ref={dialogRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={e => e.key === 'Escape' && onClose()}
    >
      {children}
    </div>
  );
}
```

---

## State Management

### State Hierarchy

State SHOULD follow this hierarchy (simplest to most complex):

1. **Local state** (useState) - component-specific state
2. **Lifted state** - shared between siblings via parent
3. **Context** - deeply nested or cross-cutting state
4. **External store** (Zustand, Jotai) - complex global state

### Local State First

Simple state MUST use `useState`:

```tsx
function Toggle() {
  const [isOn, setIsOn] = useState(false);
  return <button onClick={() => setIsOn(!isOn)}>{isOn ? 'On' : 'Off'}</button>;
}
```

### Context Usage

Context SHOULD be used for theme, auth, or other cross-cutting concerns:

```tsx
const ThemeContext = createContext<Theme | null>(null);

function useTheme() {
  const theme = useContext(ThemeContext);
  if (!theme) throw new Error('useTheme must be used within ThemeProvider');
  return theme;
}

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

---

## Custom Hooks

### Extraction Pattern

Reusable logic SHOULD be extracted into custom hooks:

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

### Hook Naming

Custom hooks MUST start with `use`:

```tsx
// CORRECT
function useWindowSize() { ... }
function useFetch<T>(url: string) { ... }

// INCORRECT
function getWindowSize() { ... }
function fetchData<T>(url: string) { ... }
```

---

## Component Composition

### Children Pattern

Components SHOULD accept children for flexibility:

```tsx
function Card({ children, title }: { children: React.ReactNode; title: string }) {
  return (
    <article className="card">
      <h2>{title}</h2>
      <div className="card-content">{children}</div>
    </article>
  );
}
```

### Render Props

Render props MAY be used for sharing stateful logic:

```tsx
interface MouseTrackerProps {
  render: (position: { x: number; y: number }) => React.ReactNode;
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  return (
    <div onMouseMove={e => setPosition({ x: e.clientX, y: e.clientY })}>
      {render(position)}
    </div>
  );
}
```

### Compound Components

Related components MAY use the compound component pattern:

```tsx
const Tabs = ({ children }: { children: React.ReactNode }) => {
  const [activeTab, setActiveTab] = useState(0);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = function TabsList({ children }) { ... };
Tabs.Tab = function Tab({ children, index }) { ... };
Tabs.Panel = function TabPanel({ children, index }) { ... };
```

---

## Error Boundaries

### Error Boundary Implementation

Applications MUST have error boundaries for graceful error handling:

```tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Error boundary caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

Note: Error boundaries MUST be class components (the only exception to the functional-only rule).

---

## Suspense and Lazy Loading

### Code Splitting

Route-level components SHOULD use lazy loading:

```tsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Suspense Boundaries

Async operations MUST be wrapped in Suspense boundaries:

```tsx
function UserProfile({ userId }) {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <UserDetails userId={userId} />
      <Suspense fallback={<PostsSkeleton />}>
        <UserPosts userId={userId} />
      </Suspense>
    </Suspense>
  );
}
```

### Loading States

Suspense fallbacks SHOULD be meaningful skeleton states, not spinners:

```tsx
// RECOMMENDED
<Suspense fallback={<ArticleSkeleton />}>
  <Article />
</Suspense>

// AVOID
<Suspense fallback={<Spinner />}>
  <Article />
</Suspense>
```
