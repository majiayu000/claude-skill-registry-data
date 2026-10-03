---
name: developing-with-react
description: React 18+ development with hooks, state management, component patterns, and accessibility
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# React Development Skill

Production-grade React development following strict quality standards.
Prefer accessibility and maintainability over convenience and cleverness.

## Scope

React 18+ functional components with hooks, state management, and styling.
Testing is covered in the jest skill.

## Primary Deliverables

- Source code with TypeScript types for all components and hooks
- Accessible, semantic HTML with ARIA attributes where needed
- Co-located CSS with CSS variables for theming
- Clear component documentation with usage examples

## Definition of Done

- All rules in this skill are followed
- All components are typed with TypeScript
- Components are keyboard navigable and screen reader friendly
- No console.log statements in production code
- Error boundaries wrap feature sections
- Loading and error states are handled

## Global Constraints

### Component Architecture

- Feature-based folder organization (not type-based)
- Single Responsibility: one component, one purpose
- Extract reusable logic into custom hooks
- Keep components under 200 lines; split if larger

### Component Types

- **Presentational**: Pure UI, receive data via props, no side effects
- **Container**: Data fetching, state management, business logic
- **Compound**: Related components sharing implicit state (Tabs, Accordion)

### State Management

- **Local state**: UI state, form inputs, component-specific data
- **Context**: Theme, auth, global UI state (sparingly)
- **Server state**: Use React Query or SWR for async data
- Lift state only when siblings need it; avoid prop drilling

### Effects Best Practices

- Always include cleanup functions for subscriptions/timers
- List all dependencies; use ESLint exhaustive-deps rule
- Avoid effects for data transformation (use useMemo)
- Prefer event handlers over effects for user actions

### Performance Guidelines

- Profile before optimizing; avoid premature optimization
- Use React.memo for expensive pure components
- Use useMemo for expensive computations
- Use useCallback for callbacks passed to memoized children
- Code split routes and heavy components with lazy/Suspense

## Prohibited Patterns

- useEffect for data fetching (prefer React Query/SWR)
- Prop drilling beyond 2-3 levels (use Context or composition)
- Missing dependency arrays in useEffect/useMemo/useCallback
- Hardcoded values that should be props or constants
- console.log for debugging in committed code
- Inline styles for complex styling (use CSS classes)
- Index as key for dynamic lists
- Direct DOM manipulation (use refs appropriately)

---

## Component Structure

Organize components with clear separation of concerns.

```tsx
// 1. Imports (grouped: react, external, internal, types)
import { useState, useCallback, type FC } from 'react';

import { useUserData } from '@/hooks/useUserData';
import { Button } from '@/components/Button';
import type { User } from '@/types';

import styles from './UserCard.module.css';

// 2. Types
interface UserCardProps {
  userId: string;
  onSelect?: (user: User) => void;
}

// 3. Component
export const UserCard: FC<UserCardProps> = ({ userId, onSelect }) => {
  // 4. Hooks (state, effects, custom hooks)
  const { user, loading, error } = useUserData(userId);
  const [isExpanded, setIsExpanded] = useState(false);

  // 5. Event handlers
  const handleToggle = useCallback(() => {
    setIsExpanded((prev) => !prev);
  }, []);

  const handleSelect = useCallback(() => {
    if (user && onSelect) {
      onSelect(user);
    }
  }, [user, onSelect]);

  // 6. Early returns (loading, error, empty states)
  if (loading) {
    return <div className={styles.skeleton} aria-busy="true" />;
  }

  if (error) {
    return (
      <div className={styles.error} role="alert">
        Failed to load user
      </div>
    );
  }

  if (!user) {
    return null;
  }

  // 7. Main render
  return (
    <article className={styles.card}>
      <h3 className={styles.name}>{user.name}</h3>
      <p className={styles.email}>{user.email}</p>
      <div className={styles.actions}>
        <Button onClick={handleToggle}>
          {isExpanded ? 'Collapse' : 'Expand'}
        </Button>
        <Button variant="primary" onClick={handleSelect}>
          Select
        </Button>
      </div>
      {isExpanded && (
        <div className={styles.details}>
          <p>{user.bio}</p>
        </div>
      )}
    </article>
  );
};
```

---

## CSS and Styling

Use CSS Modules with CSS variables for theming. No Tailwind.

### CSS Variables for Theming

```css
/* styles/variables.css */
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-secondary: #64748b;
  --color-success: #16a34a;
  --color-error: #dc2626;
  --color-warning: #d97706;

  /* Text */
  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-text-inverse: #ffffff;

  /* Backgrounds */
  --color-bg: #ffffff;
  --color-bg-secondary: #f3f4f6;
  --color-bg-elevated: #ffffff;

  /* Borders */
  --color-border: #e5e7eb;
  --color-border-focus: #2563eb;

  /* Spacing scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease;
}

/* Dark theme */
[data-theme='dark'] {
  --color-text: #f9fafb;
  --color-text-muted: #9ca3af;
  --color-bg: #111827;
  --color-bg-secondary: #1f2937;
  --color-bg-elevated: #374151;
  --color-border: #374151;
}
```

### Global Element Styles

```css
/* styles/globals.css */
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  color: var(--color-text);
  background-color: var(--color-bg);
  line-height: 1.5;
}

/* Focus styles for accessibility */
:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
}

/* Buttons */
button {
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Form elements */
input,
textarea,
select {
  font-family: inherit;
  font-size: inherit;
}
```

### Utility Classes

```css
/* styles/utilities.css */

/* Layout */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }

/* Spacing */
.m-0 { margin: 0; }
.p-4 { padding: var(--space-4); }
.mt-4 { margin-top: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }

/* Text */
.text-center { text-align: center; }
.text-muted { color: var(--color-text-muted); }
.font-medium { font-weight: 500; }
.font-bold { font-weight: 700; }

/* Visibility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Component CSS Module

```css
/* components/Button/Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-weight: 500;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast),
              border-color var(--transition-fast);
}

.button:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
}

/* Variants */
.primary {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
}

.primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.secondary {
  background-color: transparent;
  color: var(--color-text);
  border-color: var(--color-border);
}

.secondary:hover:not(:disabled) {
  background-color: var(--color-bg-secondary);
}

/* Sizes */
.small {
  padding: var(--space-1) var(--space-2);
  font-size: 0.875rem;
}

.large {
  padding: var(--space-3) var(--space-6);
  font-size: 1.125rem;
}
```

### Responsive Layout Patterns

```css
/* Mobile-first responsive design */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Stack on mobile, row on desktop */
.responsive-row {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

@media (min-width: 768px) {
  .responsive-row {
    flex-direction: row;
  }
}
```

---

## Custom Hooks

Extract reusable logic into custom hooks.

### Data Fetching Hook

```tsx
import { useState, useEffect, useCallback } from 'react';

interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useAsync<T>(
  asyncFn: () => Promise<T>,
  deps: unknown[] = []
): AsyncState<T> & { refetch: () => void } {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  const execute = useCallback(() => {
    let cancelled = false;
    setState((s) => ({ ...s, loading: true, error: null }));

    asyncFn()
      .then((data) => {
        if (!cancelled) {
          setState({ data, loading: false, error: null });
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setState({ data: null, loading: false, error });
        }
      });

    return () => {
      cancelled = true;
    };
  }, deps);

  useEffect(() => {
    return execute();
  }, [execute]);

  return { ...state, refetch: execute };
}
```

### Local Storage Hook

```tsx
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue;
    }
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch {
      // Storage full or unavailable
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}
```

### Debounced Value Hook

```tsx
import { useState, useEffect } from 'react';

export function useDebouncedValue<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}
```

---

## Error Boundaries

Wrap feature sections with error boundaries.

```tsx
import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.props.onError?.(error, errorInfo);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div role="alert" className="error-boundary">
            <h2>Something went wrong</h2>
            <p>Please try refreshing the page.</p>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary
      fallback={<ErrorFallback />}
      onError={(error) => logToService(error)}
    >
      <Dashboard />
    </ErrorBoundary>
  );
}
```

---

## Accessibility Patterns

### Accessible Form

```tsx
import { useState, useId, type FormEvent } from 'react';

import styles from './LoginForm.module.css';

interface FormErrors {
  email?: string;
  password?: string;
}

export function LoginForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const [errors, setErrors] = useState<FormErrors>({});
  const emailId = useId();
  const passwordId = useId();

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newErrors: FormErrors = {};

    if (!formData.get('email')) {
      newErrors.email = 'Email is required';
    }
    if (!formData.get('password')) {
      newErrors.password = 'Password is required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    onSubmit(formData);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={styles.form}
      aria-labelledby="login-heading"
      noValidate
    >
      <h2 id="login-heading">Login</h2>

      <div className={styles.field}>
        <label htmlFor={emailId}>
          Email <span aria-label="required">*</span>
        </label>
        <input
          id={emailId}
          type="email"
          name="email"
          autoComplete="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? `${emailId}-error` : undefined}
          required
        />
        {errors.email && (
          <span id={`${emailId}-error`} className={styles.error} role="alert">
            {errors.email}
          </span>
        )}
      </div>

      <div className={styles.field}>
        <label htmlFor={passwordId}>
          Password <span aria-label="required">*</span>
        </label>
        <input
          id={passwordId}
          type="password"
          name="password"
          autoComplete="current-password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? `${passwordId}-error` : undefined}
          required
        />
        {errors.password && (
          <span id={`${passwordId}-error`} className={styles.error} role="alert">
            {errors.password}
          </span>
        )}
      </div>

      <button type="submit" className={styles.submit}>
        Login
      </button>
    </form>
  );
}
```

### Accessible Dropdown

```tsx
import { useState, useRef, useCallback, type KeyboardEvent } from 'react';

import styles from './Dropdown.module.css';

interface DropdownProps {
  options: string[];
  value: string;
  onChange: (value: string) => void;
  label: string;
}

export function Dropdown({ options, value, onChange, label }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(0);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLUListElement>(null);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          if (!isOpen) {
            setIsOpen(true);
          } else {
            setFocusedIndex((prev) =>
              prev < options.length - 1 ? prev + 1 : 0
            );
          }
          break;
        case 'ArrowUp':
          e.preventDefault();
          setFocusedIndex((prev) =>
            prev > 0 ? prev - 1 : options.length - 1
          );
          break;
        case 'Enter':
        case ' ':
          e.preventDefault();
          if (isOpen) {
            onChange(options[focusedIndex]);
            setIsOpen(false);
            buttonRef.current?.focus();
          } else {
            setIsOpen(true);
          }
          break;
        case 'Escape':
          setIsOpen(false);
          buttonRef.current?.focus();
          break;
        case 'Tab':
          setIsOpen(false);
          break;
      }
    },
    [isOpen, focusedIndex, options, onChange]
  );

  return (
    <div className={styles.dropdown}>
      <span id="dropdown-label" className="sr-only">
        {label}
      </span>
      <button
        ref={buttonRef}
        type="button"
        className={styles.trigger}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-labelledby="dropdown-label"
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
      >
        {value || 'Select option'}
      </button>

      {isOpen && (
        <ul
          ref={menuRef}
          role="listbox"
          className={styles.menu}
          aria-labelledby="dropdown-label"
          onKeyDown={handleKeyDown}
        >
          {options.map((option, index) => (
            <li
              key={option}
              role="option"
              aria-selected={option === value}
              className={`${styles.option} ${
                index === focusedIndex ? styles.focused : ''
              }`}
              onClick={() => {
                onChange(option);
                setIsOpen(false);
                buttonRef.current?.focus();
              }}
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

## Bad Patterns and Corrections

### Missing useEffect Cleanup

```tsx
// Bad: No cleanup for subscription
useEffect(() => {
  const subscription = api.subscribe(handleUpdate);
}, []);

// Good: Cleanup prevents memory leaks
useEffect(() => {
  const subscription = api.subscribe(handleUpdate);
  return () => {
    subscription.unsubscribe();
  };
}, []);
```

### Wrong Dependency Array

```tsx
// Bad: Missing dependency causes stale closure
useEffect(() => {
  fetchData(userId);
}, []);

// Good: All dependencies listed
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

### Prop Drilling

```tsx
// Bad: Passing props through many levels
function App() {
  const [user, setUser] = useState(null);
  return <Layout user={user} setUser={setUser} />;
}
function Layout({ user, setUser }) {
  return <Sidebar user={user} setUser={setUser} />;
}

// Good: Use context for widely shared state
const UserContext = createContext(null);

function App() {
  const [user, setUser] = useState(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout />
    </UserContext.Provider>
  );
}
```

### Inline Styles for Complex Styling

```tsx
// Bad: Hard to maintain, no hover states, no theming
<button style={{
  padding: '8px 16px',
  backgroundColor: '#2563eb',
  color: 'white'
}}>
  Submit
</button>

// Good: CSS Module with theme variables
<button className={styles.primaryButton}>
  Submit
</button>
```

### Missing Error Boundary

```tsx
// Bad: Unhandled error crashes entire app
function App() {
  return <Dashboard />;
}

// Good: Error boundary contains failures
function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Dashboard />
    </ErrorBoundary>
  );
}
```

### Missing Loading State

```tsx
// Bad: No feedback while loading
function UserList() {
  const { data } = useFetch('/api/users');
  return <ul>{data?.map(user => <li>{user.name}</li>)}</ul>;
}

// Good: Show loading indicator
function UserList() {
  const { data, loading, error } = useFetch('/api/users');

  if (loading) return <Spinner aria-label="Loading users" />;
  if (error) return <Alert type="error">{error.message}</Alert>;
  if (!data?.length) return <EmptyState>No users found</EmptyState>;

  return (
    <ul>
      {data.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}
```

### Index as Key

```tsx
// Bad: Index as key causes issues when list changes
{items.map((item, index) => <Item key={index} {...item} />)}

// Good: Stable unique identifier
{items.map(item => <Item key={item.id} {...item} />)}
```

### Direct DOM Manipulation

```tsx
// Bad: Bypassing React's rendering
useEffect(() => {
  document.getElementById('title').textContent = title;
}, [title]);

// Good: Let React handle DOM updates
return <h1 id="title">{title}</h1>;
```

---

## Self-Check Before Finalizing

- [ ] All components typed with TypeScript interfaces?
- [ ] All interactive elements keyboard accessible?
- [ ] ARIA attributes added where semantic HTML insufficient?
- [ ] CSS uses variables for colors, spacing, and theming?
- [ ] No inline styles for complex styling?
- [ ] Error boundaries wrap feature sections?
- [ ] Loading and error states handled for async operations?
- [ ] useEffect cleanup functions provided where needed?
- [ ] All dependencies listed in useEffect/useMemo/useCallback?
- [ ] No prop drilling beyond 2-3 levels?
- [ ] No console.log statements in code?
- [ ] Unique keys used for list items (not index)?
- [ ] Form inputs have associated labels?
- [ ] Error messages use role="alert" for screen readers?

If any answer is no, revise the code until all criteria are satisfied.
