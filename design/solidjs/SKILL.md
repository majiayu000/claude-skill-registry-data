---
name: solidjs
description: SolidJS reactive UI framework development. Use when building interactive frontends, creating reactive components, managing state with signals/stores, handling async data fetching, or implementing fine-grained reactivity. Covers best practices, DRY/SOLID principles, control flow components, and production patterns.
version: 1.0.0
---

# SolidJS Development Skill

A comprehensive guide to building reactive user interfaces with SolidJS, following DRY and SOLID principles for maintainable, scalable code.

## Overview

SolidJS is a reactive JavaScript library for building user interfaces with:
- **Fine-grained reactivity**: Only the specific DOM nodes affected by state changes update
- **No Virtual DOM**: Compiles to real DOM operations
- **~7KB bundle size**: Minimal overhead
- **Familiar syntax**: JSX like React, but fundamentally different execution model

**Key Mental Model**: Components run **ONCE** to set up the view. Only reactive primitives (signals, memos, effects) update.

---

## Quick Reference

| What You Need | Solution |
|---------------|----------|
| Local state | `createSignal()` |
| Complex nested state | `createStore()` |
| Derived/computed values | `createMemo()` |
| Side effects | `createEffect()` |
| Async data fetching | `createResource()` |
| Conditional rendering | `<Show when={...}>` |
| List rendering | `<For each={...}>` |
| Multiple conditions | `<Switch>` / `<Match>` |
| Error boundaries | `<ErrorBoundary>` |
| Loading states | `<Suspense>` |

---

## Core Reactive Primitives

### 1. Signals - Reactive State (SRP: Single source of truth)

Signals are the foundation of SolidJS reactivity. Each signal has one responsibility: hold and notify about a single piece of state.

```typescript
import { createSignal } from "solid-js";

// GOOD: Signal with clear, single purpose
function Counter() {
  const [count, setCount] = createSignal(0);

  const increment = () => setCount((prev) => prev + 1);
  const decrement = () => setCount((prev) => prev - 1);

  return (
    <div>
      <span>Count: {count()}</span>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

**CRITICAL**: Always call signals with `()` to read their value:

```typescript
// GOOD: Signal called with ()
<span>{count()}</span>

// BAD: Passing the getter function itself (won't update)
<span>{count}</span>
```

### 2. Effects - Side Effects (SRP: Handle one side effect)

Effects automatically track dependencies and re-run when those dependencies change.

```typescript
import { createSignal, createEffect } from "solid-js";

function Logger() {
  const [count, setCount] = createSignal(0);

  // GOOD: Effect with single responsibility - logging
  createEffect(() => {
    console.log("Count changed to:", count());
  });

  // GOOD: Separate effect for different side effect - document title
  createEffect(() => {
    document.title = `Count: ${count()}`;
  });

  return <button onClick={() => setCount((c) => c + 1)}>Increment</button>;
}
```

**WARNING**: Effects are synchronous. Async operations inside effects don't track dependencies:

```typescript
// BAD: Async code loses reactivity
createEffect(() => {
  setTimeout(() => {
    console.log(count()); // NOT tracked - won't re-run on count change
  }, 1000);
});

// GOOD: Read signal synchronously, then do async work
createEffect(() => {
  const currentCount = count(); // Tracked!
  setTimeout(() => {
    console.log("Count was:", currentCount);
  }, 1000);
});
```

### 3. Memos - Derived Values (DRY: Compute once, use everywhere)

Memos cache computed values and only recompute when dependencies change.

```typescript
import { createSignal, createMemo } from "solid-js";

function Cart() {
  const [items, setItems] = createSignal([
    { name: "Apple", price: 1.5, quantity: 3 },
    { name: "Banana", price: 0.5, quantity: 6 },
  ]);

  // GOOD: Derived value computed once, cached
  const total = createMemo(() =>
    items().reduce((sum, item) => sum + item.price * item.quantity, 0)
  );

  const itemCount = createMemo(() =>
    items().reduce((sum, item) => sum + item.quantity, 0)
  );

  return (
    <div>
      <p>Items: {itemCount()}</p>
      <p>Total: ${total().toFixed(2)}</p>
    </div>
  );
}
```

### 4. Stores - Complex State (OCP: Extend without modifying)

Stores handle nested reactive state. Only accessed properties are tracked.

```typescript
import { createStore, produce } from "solid-js/store";

interface Task {
  id: number;
  text: string;
  completed: boolean;
}

interface AppState {
  tasks: Task[];
  filter: "all" | "active" | "completed";
}

function TaskApp() {
  const [state, setState] = createStore<AppState>({
    tasks: [],
    filter: "all",
  });

  // GOOD: Add new task (extending state)
  const addTask = (text: string) => {
    setState("tasks", (tasks) => [
      ...tasks,
      { id: Date.now(), text, completed: false },
    ]);
  };

  // GOOD: Update specific task using path syntax
  const toggleTask = (id: number) => {
    setState(
      "tasks",
      (task) => task.id === id,
      "completed",
      (completed) => !completed
    );
  };

  // GOOD: Use produce for complex mutations
  const updateTask = (id: number, updates: Partial<Task>) => {
    setState(
      "tasks",
      (task) => task.id === id,
      produce((task) => {
        Object.assign(task, updates);
      })
    );
  };

  return (
    <ul>
      <For each={state.tasks}>
        {(task) => (
          <li onClick={() => toggleTask(task.id)}>
            {task.text} - {task.completed ? "Done" : "Pending"}
          </li>
        )}
      </For>
    </ul>
  );
}
```

**Store path syntax patterns:**

```typescript
// Update single property
setState("propertyName", newValue);

// Update nested property
setState("user", "profile", "name", "New Name");

// Update array item by index
setState("items", 0, "value", newValue);

// Update array item by predicate
setState("items", (item) => item.id === targetId, "value", newValue);

// Append to array
setState("items", (items) => [...items, newItem]);
```

---

## Control Flow Components

SolidJS uses components for control flow instead of JS expressions. This enables fine-grained updates.

### Show - Conditional Rendering

```typescript
import { Show, createSignal } from "solid-js";

function UserProfile() {
  const [user, setUser] = createSignal<User | null>(null);
  const [loading, setLoading] = createSignal(true);

  return (
    <Show
      when={!loading()}
      fallback={<div>Loading...</div>}
    >
      <Show
        when={user()}
        fallback={<div>No user found</div>}
      >
        {/* Access user safely with callback */}
        {(userData) => (
          <div>
            <h1>{userData().name}</h1>
            <p>{userData().email}</p>
          </div>
        )}
      </Show>
    </Show>
  );
}
```

**Keyed Show** - Force re-render when reference changes:

```typescript
// Re-renders entire child when user reference changes
<Show when={user()} keyed>
  <UserCard user={user()} />
</Show>
```

### For - List Rendering

```typescript
import { For, createSignal } from "solid-js";

interface Item {
  id: number;
  name: string;
}

function ItemList() {
  const [items, setItems] = createSignal<Item[]>([
    { id: 1, name: "Apple" },
    { id: 2, name: "Banana" },
    { id: 3, name: "Cherry" },
  ]);

  const removeItem = (id: number) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  };

  return (
    <ul>
      <For each={items()}>
        {(item, index) => (
          <li>
            {index() + 1}. {item.name}
            <button onClick={() => removeItem(item.id)}>Remove</button>
          </li>
        )}
      </For>
    </ul>
  );
}
```

**CRITICAL**: `For` provides `index` as a signal (call with `()`), but `item` is the raw value.

### Switch/Match - Multiple Conditions

```typescript
import { Switch, Match, createSignal } from "solid-js";

type Status = "idle" | "loading" | "success" | "error";

function StatusDisplay() {
  const [status, setStatus] = createSignal<Status>("idle");
  const [data, setData] = createSignal<string | null>(null);
  const [error, setError] = createSignal<Error | null>(null);

  return (
    <Switch fallback={<p>Unknown status</p>}>
      <Match when={status() === "idle"}>
        <p>Ready to load</p>
      </Match>
      <Match when={status() === "loading"}>
        <p>Loading...</p>
      </Match>
      <Match when={status() === "error"}>
        <p>Error: {error()?.message}</p>
      </Match>
      <Match when={status() === "success"}>
        <p>Data: {data()}</p>
      </Match>
    </Switch>
  );
}
```

### Dynamic - Runtime Component Selection

```typescript
import { Dynamic } from "solid-js/web";
import { createSignal, For } from "solid-js";

const RedDiv = () => <div style={{ color: "red" }}>Red</div>;
const GreenDiv = () => <div style={{ color: "green" }}>Green</div>;
const BlueDiv = () => <div style={{ color: "blue" }}>Blue</div>;

const components = {
  red: RedDiv,
  green: GreenDiv,
  blue: BlueDiv,
};

function ColorPicker() {
  const [selected, setSelected] = createSignal<keyof typeof components>("red");

  return (
    <>
      <select
        value={selected()}
        onInput={(e) => setSelected(e.currentTarget.value as keyof typeof components)}
      >
        <For each={Object.keys(components)}>
          {(color) => <option value={color}>{color}</option>}
        </For>
      </select>
      <Dynamic component={components[selected()]} />
    </>
  );
}
```

---

## Data Fetching with createResource

`createResource` is SolidJS's primitive for async data fetching with automatic loading/error states.

### Basic Usage

```typescript
import { createSignal, createResource, Show, Switch, Match } from "solid-js";

interface User {
  id: number;
  name: string;
  email: string;
}

const fetchUser = async (id: number): Promise<User> => {
  const response = await fetch(`https://api.example.com/users/${id}`);
  if (!response.ok) throw new Error("Failed to fetch user");
  return response.json();
};

function UserProfile() {
  const [userId, setUserId] = createSignal(1);
  const [user] = createResource(userId, fetchUser);

  return (
    <div>
      <input
        type="number"
        value={userId()}
        onInput={(e) => setUserId(parseInt(e.currentTarget.value))}
      />

      <Show when={user.loading}>
        <p>Loading...</p>
      </Show>

      <Switch>
        <Match when={user.error}>
          <p>Error: {(user.error as Error).message}</p>
        </Match>
        <Match when={user()}>
          <div>
            <h2>{user()!.name}</h2>
            <p>{user()!.email}</p>
          </div>
        </Match>
      </Switch>
    </div>
  );
}
```

### With Suspense and ErrorBoundary (Recommended Pattern)

```typescript
import { createResource, Suspense, ErrorBoundary, For } from "solid-js";

interface Post {
  id: number;
  title: string;
  body: string;
}

const fetchPosts = async (): Promise<Post[]> => {
  const response = await fetch("https://api.example.com/posts");
  if (!response.ok) throw new Error("Failed to fetch posts");
  return response.json();
};

function PostList() {
  const [posts] = createResource(fetchPosts);

  return (
    <ErrorBoundary fallback={(err) => <div>Error: {err.message}</div>}>
      <Suspense fallback={<div>Loading posts...</div>}>
        <ul>
          <For each={posts()}>
            {(post) => (
              <li>
                <h3>{post.title}</h3>
                <p>{post.body}</p>
              </li>
            )}
          </For>
        </ul>
      </Suspense>
    </ErrorBoundary>
  );
}
```

### Resource Actions: Mutate and Refetch

```typescript
import { createResource, For, createSignal, onCleanup } from "solid-js";

interface Task {
  id: number;
  text: string;
  completed: boolean;
}

const fetchTasks = async (): Promise<Task[]> => {
  const response = await fetch("/api/tasks");
  return response.json();
};

function TaskList() {
  const [tasks, { mutate, refetch }] = createResource(fetchTasks);

  // Optimistic update
  const toggleTask = async (id: number) => {
    // Optimistically update UI
    mutate((prev) =>
      prev?.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );

    // Then sync with server
    try {
      await fetch(`/api/tasks/${id}/toggle`, { method: "POST" });
    } catch (error) {
      // Revert on failure
      refetch();
    }
  };

  // Auto-refresh every 30 seconds
  const timer = setInterval(() => refetch(), 30000);
  onCleanup(() => clearInterval(timer));

  return (
    <ul>
      <For each={tasks()}>
        {(task) => (
          <li
            onClick={() => toggleTask(task.id)}
            style={{ "text-decoration": task.completed ? "line-through" : "none" }}
          >
            {task.text}
          </li>
        )}
      </For>
    </ul>
  );
}
```

---

## Component Architecture (SOLID Principles)

### Single Responsibility Principle (SRP)

Each component should have one reason to change.

```typescript
// BAD: Component doing too many things
function UserDashboard() {
  const [user, setUser] = createSignal(null);
  const [posts, setPosts] = createSignal([]);
  const [notifications, setNotifications] = createSignal([]);

  // Fetching logic, rendering logic, business logic all mixed
  // ...
}

// GOOD: Separated concerns
function UserDashboard() {
  return (
    <div>
      <UserHeader />
      <UserPosts />
      <NotificationList />
    </div>
  );
}

function UserHeader() {
  const [user] = createResource(fetchCurrentUser);
  return <Show when={user()}>{(u) => <h1>Welcome, {u().name}</h1>}</Show>;
}

function UserPosts() {
  const [posts] = createResource(fetchUserPosts);
  return <For each={posts()}>{(post) => <PostCard post={post} />}</For>;
}

function NotificationList() {
  const [notifications] = createResource(fetchNotifications);
  return <For each={notifications()}>{(n) => <NotificationItem notification={n} />}</For>;
}
```

### Open/Closed Principle (OCP)

Components should be open for extension but closed for modification.

```typescript
// GOOD: Extensible button component
interface ButtonProps {
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  onClick?: () => void;
  disabled?: boolean;
  children: JSX.Element;
}

function Button(props: ButtonProps) {
  const classes = () => {
    const base = "btn";
    const variant = `btn-${props.variant ?? "primary"}`;
    const size = `btn-${props.size ?? "md"}`;
    return `${base} ${variant} ${size}`;
  };

  return (
    <button
      class={classes()}
      onClick={props.onClick}
      disabled={props.disabled}
    >
      {props.children}
    </button>
  );
}

// Extending without modifying original
function IconButton(props: ButtonProps & { icon: string }) {
  return (
    <Button {...props}>
      <span class={`icon-${props.icon}`} />
      {props.children}
    </Button>
  );
}
```

### Dependency Inversion Principle (DIP)

Components depend on abstractions (props/context), not concrete implementations.

```typescript
// GOOD: Component depends on abstraction (fetcher function)
interface DataListProps<T> {
  fetcher: () => Promise<T[]>;
  renderItem: (item: T) => JSX.Element;
  fallback?: JSX.Element;
}

function DataList<T>(props: DataListProps<T>) {
  const [data] = createResource(props.fetcher);

  return (
    <Suspense fallback={props.fallback ?? <div>Loading...</div>}>
      <For each={data()}>{props.renderItem}</For>
    </Suspense>
  );
}

// Usage - inject dependencies
<DataList
  fetcher={fetchUsers}
  renderItem={(user) => <UserCard user={user} />}
/>

<DataList
  fetcher={fetchProducts}
  renderItem={(product) => <ProductCard product={product} />}
/>
```

---

## Context for Global State

Context provides dependency injection for shared state across the component tree.

```typescript
import { createContext, useContext, ParentComponent } from "solid-js";
import { createStore } from "solid-js/store";

// Define context type
interface AuthState {
  user: { id: string; name: string } | null;
  token: string | null;
}

interface AuthActions {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

type AuthContextValue = [AuthState, AuthActions];

// Create context with undefined default
const AuthContext = createContext<AuthContextValue>();

// Provider component
export const AuthProvider: ParentComponent = (props) => {
  const [state, setState] = createStore<AuthState>({
    user: null,
    token: null,
  });

  const actions: AuthActions = {
    async login(email, password) {
      const response = await fetch("/api/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      setState({ user: data.user, token: data.token });
    },
    logout() {
      setState({ user: null, token: null });
    },
  };

  return (
    <AuthContext.Provider value={[state, actions]}>
      {props.children}
    </AuthContext.Provider>
  );
};

// Consumer hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}

// Usage
function App() {
  return (
    <AuthProvider>
      <Header />
      <Main />
    </AuthProvider>
  );
}

function Header() {
  const [auth, { logout }] = useAuth();

  return (
    <header>
      <Show when={auth.user} fallback={<LoginButton />}>
        <span>Welcome, {auth.user!.name}</span>
        <button onClick={logout}>Logout</button>
      </Show>
    </header>
  );
}
```

---

## Anti-Patterns to Avoid

### 1. Destructuring Props (Breaks Reactivity)

```typescript
// BAD: Destructuring breaks reactivity
function BadComponent({ count, name }) {
  // count and name are static values, won't update
  return <div>{count} - {name}</div>;
}

// GOOD: Access props directly
function GoodComponent(props) {
  return <div>{props.count} - {props.name}</div>;
}

// GOOD: Use splitProps for selective destructuring
import { splitProps } from "solid-js";

function BetterComponent(props) {
  const [local, others] = splitProps(props, ["count", "name"]);
  return <div {...others}>{local.count} - {local.name}</div>;
}
```

### 2. Reading Signals Outside Tracking Scope

```typescript
// BAD: Reading outside reactive scope
function BadComponent() {
  const [count, setCount] = createSignal(0);

  // This only runs once during component creation
  const doubled = count() * 2; // Static value!

  return <div>{doubled}</div>; // Never updates
}

// GOOD: Read inside JSX or memo
function GoodComponent() {
  const [count, setCount] = createSignal(0);

  // Option 1: Inline in JSX
  return <div>{count() * 2}</div>;

  // Option 2: Use createMemo
  const doubled = createMemo(() => count() * 2);
  return <div>{doubled()}</div>;
}
```

### 3. Using Array.map Instead of For

```typescript
// BAD: array.map() recreates all elements on any change
function BadList() {
  const [items, setItems] = createSignal(["a", "b", "c"]);

  return (
    <ul>
      {items().map((item) => <li>{item}</li>)}
    </ul>
  );
}

// GOOD: For component has efficient reconciliation
function GoodList() {
  const [items, setItems] = createSignal(["a", "b", "c"]);

  return (
    <ul>
      <For each={items()}>
        {(item) => <li>{item}</li>}
      </For>
    </ul>
  );
}
```

### 4. Ternary Instead of Show

```typescript
// BAD: Ternary always evaluates both branches
function BadConditional() {
  const [show, setShow] = createSignal(false);

  return show() ? <HeavyComponent /> : <Fallback />;
}

// GOOD: Show only renders the active branch
function GoodConditional() {
  const [show, setShow] = createSignal(false);

  return (
    <Show when={show()} fallback={<Fallback />}>
      <HeavyComponent />
    </Show>
  );
}
```

### 5. Mutating Signals Directly

```typescript
// BAD: Direct mutation doesn't trigger updates
const [items, setItems] = createSignal([1, 2, 3]);
items().push(4); // Won't trigger reactivity

// GOOD: Create new reference
setItems([...items(), 4]);

// GOOD: Use setter function
setItems((prev) => [...prev, 4]);
```

---

## File Structure

```
src/
├── components/
│   ├── ui/                    # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   └── index.ts           # Barrel export
│   ├── layout/                # Layout components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Sidebar.tsx
│   └── features/              # Feature-specific components
│       ├── auth/
│       │   ├── LoginForm.tsx
│       │   └── RegisterForm.tsx
│       └── dashboard/
│           ├── Stats.tsx
│           └── Charts.tsx
├── context/                   # Context providers
│   ├── AuthContext.tsx
│   └── ThemeContext.tsx
├── hooks/                     # Custom reactive primitives
│   ├── useLocalStorage.ts
│   └── useMediaQuery.ts
├── services/                  # API and external services
│   ├── api.ts
│   └── auth.ts
├── utils/                     # Utility functions
│   └── formatters.ts
├── types/                     # TypeScript types
│   └── index.ts
├── App.tsx
└── index.tsx
```

---

## Testing

```typescript
import { render, screen, fireEvent } from "@solidjs/testing-library";
import { Counter } from "./Counter";

describe("Counter", () => {
  test("renders initial count", () => {
    render(() => <Counter />);
    expect(screen.getByText(/count: 0/i)).toBeInTheDocument();
  });

  test("increments on button click", async () => {
    render(() => <Counter />);
    const button = screen.getByRole("button", { name: /increment/i });

    fireEvent.click(button);

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });

  test("accepts initial value prop", () => {
    render(() => <Counter initialValue={10} />);
    expect(screen.getByText(/count: 10/i)).toBeInTheDocument();
  });
});
```

---

## Checklist Before Writing SolidJS Code

1. **Signals**: Am I calling signals with `()` to read values?
2. **Props**: Am I avoiding destructuring props?
3. **Effects**: Am I reading signals synchronously in effects?
4. **Lists**: Am I using `<For>` instead of `.map()`?
5. **Conditionals**: Am I using `<Show>` instead of ternary?
6. **Memos**: Am I using `createMemo` for derived values?
7. **DRY**: Is this logic duplicated? Should it be a shared hook/utility?
8. **SRP**: Does this component have a single responsibility?
9. **Testing**: Is this component testable in isolation?

---

## Resources

- [Official Docs](https://docs.solidjs.com)
- [SolidJS GitHub](https://github.com/solidjs/solid)
- [Solid Primitives](https://github.com/solidjs-community/solid-primitives)
- [SolidStart (Meta-framework)](https://docs.solidjs.com/solid-start)
