---
name: react-expert
description: Deep React expertise for component architecture, hooks, state management, performance optimization, and testing. Use when building React applications.
---

# React Expert

Specialized expertise in React development, providing deep guidance on component architecture patterns, hooks design, state management strategies, performance optimization, testing with React Testing Library, TypeScript integration, accessibility, and React 19 features.

## When to Use This Skill

Use this skill for:

- Designing component architectures (composition, compound, render props)
- Writing and composing custom hooks
- Choosing and implementing state management (Context, Zustand, Redux Toolkit, Jotai)
- Optimizing rendering performance (memoization, code splitting, Suspense)
- Testing components with React Testing Library and MSW
- Integrating TypeScript with React patterns
- Building accessible UI with ARIA patterns and keyboard navigation
- Implementing error boundaries and recovery strategies
- Adopting React 19 features (Actions, use hook, Server Components)

**Trigger phrases**: "react component", "react hooks", "useEffect", "useState", "react performance", "react testing", "react typescript", "react accessibility", "zustand", "redux toolkit", "react memo", "suspense", "server components"

## What This Skill Does

Provides React expertise including:

- **Component Patterns**: Composition, compound components, render props, HOCs
- **Hooks**: Built-in hooks, custom hook design, rules and pitfalls
- **State Management**: Context API, Zustand, Redux Toolkit, Jotai
- **Performance**: React.memo, useMemo, useCallback, lazy loading, Suspense, concurrent features
- **Testing**: React Testing Library, user-event, MSW for network mocking
- **TypeScript**: Typed props, generic components, discriminated unions
- **Accessibility**: ARIA roles, keyboard navigation, focus management
- **Error Handling**: Error boundaries, recovery patterns
- **React 19**: Actions, use hook, optimistic updates, document metadata

## Instructions

### Step 1: Design Component Architecture

**Composition Pattern** (preferred for most cases):

```tsx
// Compose small, focused components instead of monolithic ones
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

function Card({ children, className }: CardProps) {
  return <div className={`card ${className ?? ""}`}>{children}</div>;
}

function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>;
}

function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>;
}

// Usage: composable, flexible
function UserProfile({ user }: { user: User }) {
  return (
    <Card>
      <CardHeader>
        <h2>{user.name}</h2>
      </CardHeader>
      <CardBody>
        <p>{user.bio}</p>
      </CardBody>
    </Card>
  );
}
```

**Compound Component Pattern** (for tightly coupled component families):

```tsx
import { createContext, useContext, useState, type ReactNode } from "react";

interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error("Tab components must be used within <Tabs>");
  return ctx;
}

function Tabs({ defaultTab, children }: { defaultTab: string; children: ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
}

function TabTrigger({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabs();
  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
}

function TabContent({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab } = useTabs();
  if (activeTab !== value) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach sub-components for clean API
Tabs.Trigger = TabTrigger;
Tabs.Content = TabContent;

// Usage
function SettingsPage() {
  return (
    <Tabs defaultTab="general">
      <Tabs.Trigger value="general">General</Tabs.Trigger>
      <Tabs.Trigger value="security">Security</Tabs.Trigger>
      <Tabs.Content value="general"><GeneralSettings /></Tabs.Content>
      <Tabs.Content value="security"><SecuritySettings /></Tabs.Content>
    </Tabs>
  );
}
```

**Render Props** (for sharing stateful logic with flexible rendering):

```tsx
interface MousePosition {
  x: number;
  y: number;
}

function MouseTracker({
  render,
}: {
  render: (pos: MousePosition) => ReactNode;
}) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  return (
    <div onMouseMove={(e) => setPosition({ x: e.clientX, y: e.clientY })}>
      {render(position)}
    </div>
  );
}

// Usage
<MouseTracker render={({ x, y }) => <Cursor x={x} y={y} />} />;
```

### Step 2: Master Hooks Patterns

**useState with complex state**:

```tsx
interface FormState {
  name: string;
  email: string;
  errors: Record<string, string>;
}

function useForm(initial: FormState) {
  const [state, setState] = useState<FormState>(initial);

  const setField = useCallback(
    <K extends keyof FormState>(field: K, value: FormState[K]) => {
      setState((prev) => ({ ...prev, [field]: value }));
    },
    []
  );

  const reset = useCallback(() => setState(initial), [initial]);

  return { state, setField, reset };
}
```

**useEffect: correct dependency management**:

```tsx
// Fetch data with cleanup and race condition protection
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;           // Guard against stale responses
    const controller = new AbortController();

    async function fetchUser() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`/api/users/${userId}`, {
          signal: controller.signal,
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: User = await res.json();
        if (!cancelled) setUser(data);
      } catch (err) {
        if (!cancelled && err instanceof Error && err.name !== "AbortError") {
          setError(err);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchUser();
    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [userId]);

  return { user, error, loading };
}
```

**Custom hook: debounced value**:

```tsx
function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debounced;
}

// Usage in search
function SearchInput() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebouncedValue(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery);
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

**useRef for imperative handles and stable references**:

```tsx
function VideoPlayer({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const previousSrc = useRef(src);

  useEffect(() => {
    if (previousSrc.current !== src) {
      videoRef.current?.load();
      previousSrc.current = src;
    }
  }, [src]);

  return (
    <div>
      <video ref={videoRef} src={src} />
      <button onClick={() => videoRef.current?.play()}>Play</button>
      <button onClick={() => videoRef.current?.pause()}>Pause</button>
    </div>
  );
}
```

### Step 3: Implement State Management

**Context API (suitable for low-frequency updates)**:

```tsx
interface ThemeContextValue {
  theme: "light" | "dark";
  toggle: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const toggle = useCallback(
    () => setTheme((t) => (t === "light" ? "dark" : "light")),
    []
  );
  // Memoize the context value to prevent unnecessary re-renders
  const value = useMemo(() => ({ theme, toggle }), [theme, toggle]);
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}
```

**Zustand (recommended for most applications)**:

```tsx
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: Omit<CartItem, "quantity">) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
  total: () => number;
}

export const useCartStore = create<CartStore>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],
        addItem: (item) =>
          set((state) => {
            const existing = state.items.find((i) => i.id === item.id);
            if (existing) {
              return {
                items: state.items.map((i) =>
                  i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
                ),
              };
            }
            return { items: [...state.items, { ...item, quantity: 1 }] };
          }),
        removeItem: (id) =>
          set((state) => ({
            items: state.items.filter((i) => i.id !== id),
          })),
        clearCart: () => set({ items: [] }),
        total: () =>
          get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
      }),
      { name: "cart-storage" }
    )
  )
);
```

### Step 4: Optimize Performance

**React.memo for expensive components**:

```tsx
interface DataTableProps {
  rows: DataRow[];
  columns: Column[];
  onSort: (column: string) => void;
}

const DataTable = React.memo(function DataTable({
  rows,
  columns,
  onSort,
}: DataTableProps) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key} onClick={() => onSort(col.key)}>
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id}>
            {columns.map((col) => (
              <td key={col.key}>{row[col.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
});
```

**Lazy loading with Suspense and code splitting**:

```tsx
import { lazy, Suspense } from "react";

// Split code at the route level
const AdminDashboard = lazy(() => import("./pages/AdminDashboard"));
const UserSettings = lazy(() => import("./pages/UserSettings"));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/settings" element={<UserSettings />} />
      </Routes>
    </Suspense>
  );
}
```

**Performance profiling steps**:

1. Open React DevTools Profiler tab
2. Click "Record" and perform the interaction
3. Review the flame graph: look for components that render unnecessarily
4. For each unnecessary render, determine whether it is caused by:
   - Unstable props (new object/array/function on every render)
   - Context value changing (split contexts or use selectors)
   - Parent re-rendering (wrap child in React.memo)
5. Apply the narrowest fix: useMemo/useCallback for prop stability, React.memo for the component, or context splitting

### Step 5: Test with React Testing Library

**Component testing fundamentals**:

```tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "./LoginForm";

describe("LoginForm", () => {
  it("submits credentials and shows success message", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockResolvedValue({ success: true });

    render(<LoginForm onSubmit={onSubmit} />);

    // Query by accessible role and label, not by test-id
    await user.type(screen.getByLabelText(/email/i), "user@example.com");
    await user.type(screen.getByLabelText(/password/i), "s3cret!");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: "user@example.com",
      password: "s3cret!",
    });

    await waitFor(() => {
      expect(screen.getByText(/welcome/i)).toBeInTheDocument();
    });
  });

  it("shows validation errors for empty fields", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={vi.fn()} />);

    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });
});
```

**Mocking network requests with MSW**:

```tsx
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

const server = setupServer(
  http.get("/api/users/:id", ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: "Jane Doe",
      email: "jane@example.com",
    });
  }),
  http.post("/api/users", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: "new-id", ...body }, { status: 201 });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test("displays user profile after fetch", async () => {
  render(<UserProfile userId="42" />);

  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText("Jane Doe")).toBeInTheDocument();
  });
});

test("handles server error gracefully", async () => {
  server.use(
    http.get("/api/users/:id", () => {
      return HttpResponse.json({ error: "Not found" }, { status: 404 });
    })
  );

  render(<UserProfile userId="999" />);

  await waitFor(() => {
    expect(screen.getByText(/user not found/i)).toBeInTheDocument();
  });
});
```

### Step 6: Integrate TypeScript

**Generic component with discriminated union props**:

```tsx
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage }: ListProps<T>) {
  if (items.length === 0) {
    return <p>{emptyMessage ?? "No items"}</p>;
  }
  return (
    <ul>
      {items.map((item, i) => (
        <li key={keyExtractor(item)}>{renderItem(item, i)}</li>
      ))}
    </ul>
  );
}

// Discriminated union for polymorphic props
type ButtonProps =
  | { variant: "link"; href: string; onClick?: never }
  | { variant: "button"; onClick: () => void; href?: never };

function ActionButton(props: ButtonProps & { children: ReactNode }) {
  if (props.variant === "link") {
    return <a href={props.href}>{props.children}</a>;
  }
  return <button onClick={props.onClick}>{props.children}</button>;
}
```

### Step 7: Implement Accessibility

**ARIA patterns and keyboard navigation**:

```tsx
function Modal({
  isOpen,
  onClose,
  title,
  children,
}: {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) {
      closeRef.current?.focus();                  // Move focus into modal
      const handleKey = (e: KeyboardEvent) => {
        if (e.key === "Escape") onClose();
      };
      document.addEventListener("keydown", handleKey);
      return () => document.removeEventListener("keydown", handleKey);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className="modal-backdrop" onClick={onClose} />
      <div className="modal-content">
        <h2 id="modal-title">{title}</h2>
        {children}
        <button ref={closeRef} onClick={onClose} aria-label="Close modal">
          Close
        </button>
      </div>
    </div>
  );
}
```

### Step 8: Error Boundaries

```tsx
import { Component, type ErrorInfo, type ReactNode } from "react";

interface ErrorBoundaryProps {
  fallback: (error: Error, reset: () => void) => ReactNode;
  children: ReactNode;
}

interface ErrorBoundaryState {
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("ErrorBoundary caught:", error, info.componentStack);
    // Send to error reporting service
  }

  reset = () => this.setState({ error: null });

  render() {
    if (this.state.error) {
      return this.props.fallback(this.state.error, this.reset);
    }
    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary
      fallback={(error, reset) => (
        <div role="alert">
          <p>Something went wrong: {error.message}</p>
          <button onClick={reset}>Try Again</button>
        </div>
      )}
    >
      <Dashboard />
    </ErrorBoundary>
  );
}
```

### Step 9: React 19 Features

**Actions and useActionState**:

```tsx
import { useActionState } from "react";

async function submitForm(
  _prevState: { message: string } | null,
  formData: FormData
) {
  const name = formData.get("name") as string;
  const res = await fetch("/api/contact", {
    method: "POST",
    body: JSON.stringify({ name }),
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) return { message: "Failed to submit" };
  return { message: `Thank you, ${name}!` };
}

function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      <input name="name" required disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? "Submitting..." : "Submit"}
      </button>
      {state?.message && <p>{state.message}</p>}
    </form>
  );
}
```

**useOptimistic for instant UI feedback**:

```tsx
import { useOptimistic } from "react";

function TodoList({ todos, onToggle }: {
  todos: Todo[];
  onToggle: (id: string) => Promise<void>;
}) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (currentTodos, toggledId: string) =>
      currentTodos.map((t) =>
        t.id === toggledId ? { ...t, done: !t.done } : t
      )
  );

  async function handleToggle(id: string) {
    addOptimistic(id);       // Immediate UI update
    await onToggle(id);      // Actual server call
  }

  return (
    <ul>
      {optimisticTodos.map((todo) => (
        <li key={todo.id}>
          <label>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => handleToggle(todo.id)}
            />
            {todo.title}
          </label>
        </li>
      ))}
    </ul>
  );
}
```

## Best Practices

- **Lift state up only as far as necessary** (keep state close to where it is used)
- **Prefer composition over prop drilling** (use children or render props)
- **Memoize expensive computations, not everything** (profile before optimizing)
- **Always clean up side effects** in useEffect return functions
- **Use keys correctly**: stable, unique identifiers (never array indices for dynamic lists)
- **Test user behavior, not implementation**: query by role/label, not test-ids
- **Split contexts by update frequency** to avoid unnecessary re-renders
- **Co-locate related code**: keep component, styles, tests, and types together

## Common Patterns

### Pattern 1: Data Fetching Hook with Caching

```tsx
const cache = new Map<string, { data: unknown; timestamp: number }>();
const STALE_TIME = 5 * 60 * 1000; // 5 minutes

function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(() => {
    const cached = cache.get(url);
    if (cached && Date.now() - cached.timestamp < STALE_TIME) {
      return cached.data as T;
    }
    return null;
  });
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(!data);

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();

    async function load() {
      try {
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (!cancelled) {
          cache.set(url, { data: json, timestamp: Date.now() });
          setData(json);
        }
      } catch (err) {
        if (!cancelled && err instanceof Error && err.name !== "AbortError") {
          setError(err);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; controller.abort(); };
  }, [url]);

  return { data, error, loading };
}
```

### Pattern 2: Controlled Form with Validation

```tsx
function useFormValidation<T extends Record<string, string>>(
  initialValues: T,
  validate: (values: T) => Partial<Record<keyof T, string>>
) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const handleChange = (field: keyof T) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setValues((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleBlur = (field: keyof T) => () => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    setErrors(validate(values));
  };

  const handleSubmit = (onSubmit: (values: T) => void) => (
    e: React.FormEvent
  ) => {
    e.preventDefault();
    const validationErrors = validate(values);
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length === 0) {
      onSubmit(values);
    }
  };

  return { values, errors, touched, handleChange, handleBlur, handleSubmit };
}
```

## Quality Checklist

- [ ] Components follow single-responsibility principle
- [ ] Custom hooks extract reusable stateful logic
- [ ] useEffect dependencies are complete and correct
- [ ] Side effects are cleaned up on unmount
- [ ] Lists use stable, unique keys (not array indices)
- [ ] Expensive renders are memoized with profiling evidence
- [ ] Tests query by accessible role/label, not test-id
- [ ] Error boundaries wrap critical UI sections
- [ ] Keyboard navigation and ARIA attributes are present
- [ ] TypeScript strict mode enabled, no `any` escape hatches
- [ ] Bundle size is audited; heavy dependencies are lazy loaded
- [ ] No prop drilling beyond two levels (use context or composition)

## Related Skills

- `nextjs-expert` - React framework with SSR, routing, and server components
- `javascript-cleanup` - JavaScript code quality and cleanup
- `unit-tests` - General unit testing strategies
- `performance-review` - Broad performance review methodology
- `test-cases` - Test case design patterns

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
